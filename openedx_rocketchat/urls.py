"""
Openedx Rocketchat URL configuration.
"""
from django.conf import settings
from django.conf.urls import include, url

from .views import rocket_chat_discussion

urlpatterns = [  # pylint: disable=invalid-name
    url(
        r'^api/',
        include('openedx_rocketchat.api.urls', namespace='api'),
    ),
    url(
        r'^{}/discussion/'.format(
            settings.COURSE_ID_PATTERN,
        ),
        rocket_chat_discussion,
        name='rocket_chat_discussion'
    ),
]
