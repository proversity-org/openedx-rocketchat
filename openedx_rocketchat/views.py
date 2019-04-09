"""Views for openedx_rocketchat django plugin. """
import hashlib
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from openedx_rocketchat.edxapp_wrapper.edxmako_module import render_to_response
from openedx_rocketchat.edxapp_wrapper.get_configuration_helpers import get_configuration_helpers
from openedx_rocketchat.edxapp_wrapper.get_courseware import (
    get_course_with_access,
    has_access
)
from openedx_rocketchat.edxapp_wrapper.get_student_models import (
    get_course_enrollment,
    get_course_enrollment_manager
)

from .utils import (
    create_course_group,
    create_token,
    get_course_from_string,
    get_rocket_chat_settings,
    initialize_api_rocket_chat
)

LOG = logging.getLogger(__name__)


@login_required
def rocket_chat_discussion(request, course_id):   # pylint: disable=too-many-locals
    """
    This view renders the rocketchat tab template.
    """
    configuration_helpers = get_configuration_helpers()
    course_enrollment = get_course_enrollment()
    course_enrollment_manager = get_course_enrollment_manager()

    course_key = get_course_from_string(course_id)

    user = request.user
    course = get_course_with_access(user, 'load', course_key)

    is_enabled = configuration_helpers.get_value(
        'ENABLE_ROCKET_CHAT_SERVICE',
        course.other_course_settings.get('enable_rocketchat_tab')
    )

    if not is_enabled:
        raise Http404

    staff_access = has_access(user, 'staff', course)
    user_is_enrolled = course_enrollment.is_enrolled(user, course.id)

    key = hashlib.sha1("{}_{}".format(settings.ROCKETCHAT_DATA_KEY, user.username)).hexdigest()

    context = {
        'request': request,
        'course': course,
        'course_title': course.display_name_with_default,
        'staff_access': staff_access,
        'user_is_enrolled': user_is_enrolled,
        'beacon_rc': key,
        "users_enrolled": course_enrollment_manager().users_enrolled_in(course_key) if staff_access else None,
        'rocket_chat_error_message': 'Rocket chat service is currently not available',
    }

    rocket_chat_settings = get_rocket_chat_settings()

    api_rocket_chat = initialize_api_rocket_chat(rocket_chat_settings)

    if api_rocket_chat:

        response = create_token(api_rocket_chat, user, course_key)

        if response:
            try:
                if response.get('success'):

                    context['rocket_chat_data'] = response['data']
                    context['rocket_chat_url'] = rocket_chat_settings['public_url_service']
                    context['rocket_chat_error_message'] = None

                    create_course_group(api_rocket_chat, course_id, response['data']['userId'], user.username)

                elif 'error' in response:
                    context['rocket_chat_error_message'] = response['error']

            except AttributeError:
                context['rocket_chat_error_message'] = 'status_code = {}'.format(
                    response.status_code
                )

    return render_to_response('rocket_chat.html', context)
