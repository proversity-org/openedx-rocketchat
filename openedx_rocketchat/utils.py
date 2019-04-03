import hashlib
import logging
import re

from django.conf import settings
from django.core.cache import cache

from openedx_rocketchat.edxapp_wrapper.get_configuration_helpers import get_configuration_helpers
from openedx_rocketchat.edxapp_wrapper.get_student_models import anonymous_id_for_user, get_user

from rocketchat_API.rocketchat import RocketChat as ApiRocketChat
from rocketchat_API.APIExceptions.RocketExceptions import RocketAuthenticationException, RocketConnectionException


LOG = logging.getLogger(__name__)
CACHE_TIMEOUT = get_configuration_helpers().get_value("ROCKET_CHAT_CACHE_TIMEOUT", 86400)
ROCKET_CHAT_DATA = "rocket_chat_data"


def get_rocket_chat_settings():
    """Return dict with rocket chat settings"""
    try:
        return settings.ROCKET_CHAT_SETTINGS
    except AttributeError, settings_error:
        LOG.warning('Get settings warning: %s', settings_error)
        pass
    try:
        xblock_settings = settings.XBLOCK_SETTINGS
        return xblock_settings.get('RocketChatXBlock', None)
    except AttributeError, xblock_settings_error:
        LOG.warning('Get settings warning: %s', xblock_settings_error)
        pass

    return None


def create_user(api_rocket_chat, user, course_key):
    """Create a user in rocketChat"""
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
    Add an user to the course group
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
        pass


def initialize_api_rocket_chat(rocket_chat_settings):

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
    return {"status": "fall"}


def create_token(api_rocket_chat, user):

    key = hashlib.sha1("{}_{}".format(ROCKET_CHAT_DATA, user.username)).hexdigest()
    response = cache.get(key)
    if not response:
        response = api_rocket_chat.users_create_token(
            username=user.username)
        try:
            response = response.json()
            cache.set(key, response, CACHE_TIMEOUT)
            return response
        except AttributeError:
            return None
    return response


def user_api_rocket_chat(auth_token, user_id):
    url_service = get_rocket_chat_settings().get('private_url_service', None)
    user_api_rocket_chat = ApiRocketChat(server_url=url_service)
    user_api_rocket_chat.headers['X-Auth-Token'] = auth_token
    user_api_rocket_chat.headers['X-User-Id'] = user_id
    return user_api_rocket_chat
