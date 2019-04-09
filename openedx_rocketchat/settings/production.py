"""
Settings for openedx_rocketchat
"""

from __future__ import absolute_import, unicode_literals


def plugin_settings(settings):
    """
    Defines openedx_rocketchat settings when app is used as a plugin to edx-platform.
    See: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.ROCKETCHAT_COURSEWARE = getattr(settings, 'ENV_TOKENS', {}).get(
        'ROCKETCHAT_COURSEWARE',
        settings.ROCKETCHAT_COURSEWARE
    )
    settings.ROCKETCHAT_CONFIGURATION_HELPERS = getattr(settings, 'ENV_TOKENS', {}).get(
        'ROCKETCHAT_CONFIGURATION_HELPERS',
        settings.ROCKETCHAT_CONFIGURATION_HELPERS
    )
    settings.ROCKETCHAT_EDXMAKO_MODULE = getattr(settings, 'ENV_TOKENS', {}).get(
        'ROCKETCHAT_EDXMAKO_MODULE',
        settings.ROCKETCHAT_EDXMAKO_MODULE
    )
    settings.ROCKETCHAT_STUDENT_MODELS = getattr(settings, 'ENV_TOKENS', {}).get(
        'ROCKETCHAT_STUDENT_MODELS',
        settings.ROCKETCHAT_STUDENT_MODELS
    )
    settings.ROCKETCHAT_DATA_KEY = getattr(settings, 'ENV_TOKENS', {}).get(
        'ROCKETCHAT_DATA_KEY',
        settings.ROCKETCHAT_DATA_KEY
    )
