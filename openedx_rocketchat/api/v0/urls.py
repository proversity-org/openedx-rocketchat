"""
API v0 URLs.
"""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^credentials', views.RocketChatCredentials.as_view(), name='rocket_chat_credentials'),
    url(r'^subscriptions-id', views.RocketChatSubscriptionsId.as_view(), name='rocket_chat_subscriptions'),
    url(r'^change-role', views.RocketChatChangeRole.as_view(), name='rocket_chat_change_role'),
    url(r'^clean-token-cache', views.RocketChatCleanToken.as_view(), name='rocket_chat_clean_token_cache'),
]
