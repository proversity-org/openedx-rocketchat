"""
Utility functions used by openexd_rocketchat.
"""
import hashlib
import logging
import re

from django.conf import settings
from django.core.cache import cache
from opaque_keys.edx.keys import CourseKey
from openedx_rocketchat.edxapp_wrapper.get_configuration_helpers import \
    get_configuration_helpers
from openedx_rocketchat.edxapp_wrapper.get_student_models import (anonymous_id_for_user,
                                                                  get_user)
from rocketchat_API.APIExceptions.RocketExceptions import (RocketAuthenticationException,
                                                           RocketConnectionException)
from rocketchat_API.rocketchat import RocketChat as ApiRocketChat

LOG = logging.getLogger(__name__)
CACHE_TIMEOUT = get_configuration_helpers().get_value("ROCKET_CHAT_CACHE_TIMEOUT", 86400)


def get_rocket_chat_settings():
    """
    Returns a dict with rocket chat settings. This try to get from the general settings and xblock settings.
    **Example**:

        ROCKET_CHAT_SETTINGS = {
            'private_url_service': 'http://localhost:3000',
            'public_url_service': 'localhost:3000',
            'admin_user': 'rocketchat_admin_user',
            "admin_pass": 'pass1234',
            "username":"staff",
            "password":"edx",
        }

        XBLOCK_SETTINGS = {
            'RocketChatXBlock': {
                'private_url_service': 'http://localhost:3000',
                'public_url_service': 'localhost:3000',
                'admin_user': 'rocketchat_admin_user',
                "admin_pass": 'pass1234',
                "username":"staff",
                "password":"edx",
            }
        }
    """
    try:
        return settings.ROCKET_CHAT_SETTINGS
    except AttributeError, settings_error:
        LOG.warning('Get settings warning: %s', settings_error)

    xblock_settings = getattr(settings, "XBLOCK_SETTINGS", {})
    return xblock_settings.get('RocketChatXBlock', {})


def create_user(api_rocket_chat, user, course_key):
    """
    Create a user in rocketChat
    """
    user, u_prof = get_user(user.email)
    anonymous_id = anonymous_id_for_user(user, course_key)
    return api_rocket_chat.users_create(
        email=user.email,
        name=u_prof.name if u_prof.name != "" else user.username,
        password=anonymous_id,
        username=user.username
    )


def create_course_group(api_rocket_chat, course_id, user_id, username):
    """
    Add a user to the course group
    """
    course = re.sub('[^A-Za-z0-9]+', '', course_id)
    room_name = "{}__{}".format("General", course)
    response = api_rocket_chat.groups_info(room_name=room_name)
    try:
        response = response.json()

        if response['success']:
            api_rocket_chat.groups_invite(response['group']['_id'], user_id)
        else:
            kwargs = {
                'members': [username],
                'customFields': {
                    'course': course,
                    'team': None,
                    'topic': None,
                    'specificTeam': False,
                }
            }
            api_rocket_chat.groups_create(name=room_name, **kwargs)

    except AttributeError:
        LOG.error("Create Course Group error: response with status code = %s", response.status_code)


def initialize_api_rocket_chat(rocket_chat_settings):
    """
    Returns an ApirocketChat instance using the given settings
    """
    admin_user = rocket_chat_settings.get('admin_user', None)
    admin_pass = rocket_chat_settings.get('admin_pass', None)
    url_service = rocket_chat_settings.get('public_url_service', None)

    if not admin_user or not admin_pass or not url_service:
        LOG.error('RocketChat settings error: The rocketChat credentials can not be accessed')
        return None

    try:
        api_rocket_chat = ApiRocketChat(
            admin_user,
            admin_pass,
            url_service
        )
    except RocketAuthenticationException:
        LOG.error('ApiRocketChat error: RocketAuthenticationException')
        return None
    except RocketConnectionException:
        LOG.error('ApiRocketChat error: RocketConnectionException')
        return None

    return api_rocket_chat


def get_subscriptions_rids(auth_token, user_id, unread=False):
    """
    This method allow to get the roomid for every subscrition
    """
    response = user_api_rocket_chat(auth_token, user_id)._RocketChat__call_api_get('subscriptions.get')
    try:
        response = response.json()
    except AttributeError:
        return
    if response['success']:
        subscriptions = response.get('update', [])
        for subscription in subscriptions:
            if not unread:
                yield subscription['rid']
            elif subscription['unread'] > 0:
                yield subscription['rid']


def logout(auth_token, user_id):
    """
    Invalidate the REST API authentication token.
    """
    try:
        return user_api_rocket_chat(auth_token, user_id).logout().json()
    except AttributeError:
        pass
    return {"status": "fail"}


def create_token(api_rocket_chat, user, course_key):
    """
    **Returns the authentication data required for rocketchat authentication process.**
        Use Case :These credentials could be used to make api calls and rocketchat authentication on browsers.
    **Return Example**
        {
          "data": {
            "userId": "BsNr28znDkG8aeo7W",
            "authToken": "2jdk99wuSjXPO201XlAks9sjDjAhSJmskAKW301mSuj9Sk",
          },
          "success": true
        }
    """

    key = hashlib.sha1("{}_{}".format(settings.ROCKETCHAT_DATA_KEY, user.username)).hexdigest()
    response = cache.get(key)

    if not response:

        user_info = api_rocket_chat.users_info(username=user.username)

        try:
            user_info = user_info.json()
            if not user_info.get('success'):
                create_user(api_rocket_chat, user, course_key)
        except AttributeError:
            LOG.error("Rocketchat API can not get the user information")
            return None

        response = api_rocket_chat.users_create_token(
            username=user.username
        )
        try:
            response = response.json()

            if response.get("success"):
                cache.set(key, response, CACHE_TIMEOUT)

            return response
        except AttributeError:
            return response

    return response


def user_api_rocket_chat(auth_token, user_id):
    """
    Returns an ApirocketChat instance using the given auth_token and user_id
    """
    url_service = get_rocket_chat_settings().get('private_url_service', None)
    user_api_rocket_chat = ApiRocketChat(server_url=url_service)  # pylint: disable=redefined-outer-name
    user_api_rocket_chat.headers['X-Auth-Token'] = auth_token
    user_api_rocket_chat.headers['X-User-Id'] = user_id
    return user_api_rocket_chat


def get_course_from_string(*args, **kwargs):
    """Return a course for a given course_id"""
    return CourseKey.from_string(*args, **kwargs)
