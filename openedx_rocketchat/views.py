import hashlib
import logging
import waffle

from django.http import Http404
from django.contrib.auth.decorators import login_required

from openedx_rocketchat.edxapp_wrapper.edxmako_module import render_to_response
from openedx_rocketchat.edxapp_wrapper.get_configuration_helpers import get_configuration_helpers
from openedx_rocketchat.edxapp_wrapper.get_courseware import get_course_with_access, has_access
from openedx_rocketchat.edxapp_wrapper.get_opaque_keys import get_course_from_string
from openedx_rocketchat.edxapp_wrapper.get_student_models import get_course_enrollment, get_course_enrollment_manager

from .utils import (
    create_course_group,
    initialize_api_rocket_chat,
    create_user,
    get_rocket_chat_settings,
    create_token,
)

LOG = logging.getLogger(__name__)
ROCKET_CHAT_DATA = "rocket_chat_data"


@login_required
def rocket_chat_discussion(request, course_id):

    configuration_helpers = get_configuration_helpers()
    course_enrollment = get_course_enrollment()
    course_enrollment_manager = get_course_enrollment_manager()

    is_enabled = configuration_helpers.get_value(
        'ENABLE_ROCKET_CHAT_SERVICE',
        waffle.switch_is_active('rocket_chat_tab')
    )

    if not is_enabled:
        raise Http404

    course_key = get_course_from_string(course_id)

    user = request.user
    course = get_course_with_access(user, 'load', course_key)

    staff_access = has_access(user, 'staff', course)
    user_is_enrolled = course_enrollment.is_enrolled(user, course.id)

    course_homepage_invert_title = configuration_helpers.get_value(
        'COURSE_HOMEPAGE_INVERT_TITLE', False)

    course_title = course.display_name_with_default
    if course_homepage_invert_title:
        course_title = course.display_number_with_default

    key = hashlib.sha1("{}_{}".format(ROCKET_CHAT_DATA, user.username)).hexdigest()

    context = {
        'request': request,
        'cache': None,
        'course': course,
        'course_title': course_title,
        'staff_access': staff_access,
        'user_is_enrolled': user_is_enrolled,
        'beacon_rc': key,
    }

    rocket_chat_settings = get_rocket_chat_settings()

    api_rocket_chat = initialize_api_rocket_chat(rocket_chat_settings)

    if api_rocket_chat:

        user_info = api_rocket_chat.users_info(username=user.username)

        try:
            user_info = user_info.json()
        except AttributeError:
            create_user(api_rocket_chat, user, course_key)

        if 'success' in user_info and not user_info['success']:
            create_user(api_rocket_chat, user, course_key)

        response = create_token(api_rocket_chat, user)

        if not response:
            try:
                response = response.json()
            except AttributeError:
                context['rocket_chat_error_message'] = 'status_code = {}'.format(
                    response.status_code)
                return render_to_response('rocket_chat.html', context)

        if response['success']:
            context['rocket_chat_data'] = response['data']
            context['rocket_chat_url'] = rocket_chat_settings['public_url_service']
            context['rocket_chat_error_message'] = None

            create_course_group(api_rocket_chat, course_id, response['data']['userId'], user.username)

        elif 'error' in response:
            context['rocket_chat_error_message'] = response['error']

        if user.is_staff:
            context["users_enrolled"] = course_enrollment_manager().users_enrolled_in(course_key)

        return render_to_response('rocket_chat.html', context)

    context['rocket_chat_error_message'] = 'Rocket chat service is currently not available'

    return render_to_response('rocket_chat/rocket_chat.html', context)
