from .views import rocket_chat_discussion

from django.conf import settings
from django.conf.urls import url, include

urlpatterns = [
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
