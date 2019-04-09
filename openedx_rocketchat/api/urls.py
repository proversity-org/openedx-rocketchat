"""
Api URLs.
"""
from django.conf.urls import include, url

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^v0/', include('openedx_rocketchat.api.v0.urls', namespace='v0')),
]
