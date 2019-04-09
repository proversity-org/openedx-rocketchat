"""
Common settings for openedx-rocketchat project.
"""


def plugin_settings(settings):
    """
    Backend settings
    """
    settings.ROCKETCHAT_DATA_KEY = "rocket_chat_data_key"
    settings.ROCKETCHAT_CONFIGURATION_HELPERS = 'openedx_rocketchat.edxapp_wrapper.backends.get_configuration_helpers'
    settings.ROCKETCHAT_COURSEWARE = 'openedx_rocketchat.edxapp_wrapper.backends.get_courseware'
    settings.ROCKETCHAT_EDXMAKO_MODULE = 'openedx_rocketchat.edxapp_wrapper.backends.edxmako_rocketchat_module'
    settings.ROCKETCHAT_STUDENT_MODELS = 'openedx_rocketchat.edxapp_wrapper.backends.get_student_models'
