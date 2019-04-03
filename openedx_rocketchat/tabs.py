import waffle

from django.utils.translation import ugettext_noop

from courseware.tabs import EnrolledTab
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers


class RocketChatTab(EnrolledTab):
    """
    The representation of the course rocketchat view type.
    """

    type = "rocketchat"
    title = ugettext_noop("Chat")
    view_name = "rocketchat:rocket_chat_discussion"
    is_dynamic = True

    @classmethod
    def is_enabled(cls, course, user=None):
        """
        Returns true if rocketChat feature is enabled in the course.
        """
        is_enabled = configuration_helpers.get_value(
            'ENABLE_ROCKET_CHAT_SERVICE',
            waffle.switch_is_active('rocket_chat_tab')
        )
        is_enrolled = super(RocketChatTab, cls).is_enabled(course, user)
        return is_enabled and is_enrolled
