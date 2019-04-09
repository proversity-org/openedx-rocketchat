"""
File configuration for openedx-rocketchat.
"""
from django.apps import AppConfig


class OpenEdxRocketChatExtensionConfig(AppConfig):
    """
    App configuration
    """
    name = 'openedx_rocketchat'
    verbose_name = "Openedx RocketChat Discussion."

    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'rocketchat',
                'regex': r'^rocketchat/',
                'relative_path': 'urls',
            },
        },
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'aws': {'relative_path': 'settings.aws'},
                'production': {'relative_path': 'settings.production'},
            },
        },
    }
