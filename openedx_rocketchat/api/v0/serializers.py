from rest_framework import serializers


class RocketChatCredentialsSerializer(serializers.Serializer):
    url_service = serializers.CharField()
    auth_token = serializers.CharField()
    user_id = serializers.CharField()
    room_ids = serializers.ListField(child=serializers.CharField())


class RocketChatChangeRoleSerializer(serializers.Serializer):
    username = serializers.CharField()
    role = serializers.CharField()
