""" RocketChat Serializers """
from rest_framework import serializers


# pylint: disable=abstract-method
class RocketChatCredentialsSerializer(serializers.Serializer):
    """
    Serializer for RocketChatCredentials view.
    """
    url_service = serializers.CharField()
    auth_token = serializers.CharField()
    user_id = serializers.CharField()


class RocketChatSubscriptionsIdSerializer(serializers.Serializer):
    """
    Serializer for RocketChatSubscriptionsId view.
    """
    subscriptions_id = serializers.ListField(child=serializers.CharField())


class RocketChatChangeRoleSerializer(serializers.Serializer):
    """
    Serializer for RocketChatChangeRole view.
    """
    username = serializers.CharField()
    role = serializers.CharField()
