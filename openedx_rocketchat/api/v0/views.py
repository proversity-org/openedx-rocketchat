import logging

from django.core.cache import cache

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from openedx_rocketchat.edxapp_wrapper.get_opaque_keys import get_course_from_string

from openedx_rocketchat.utils import (
    get_rocket_chat_settings,
    initialize_api_rocket_chat,
    get_subscriptions_rids,
    logout,
    create_token,
)
from .serializers import *

LOG = logging.getLogger(__name__)


class RocketChatCredentials(APIView):

    authentication_classes = (
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Get rocketchat user credentials in order to use rocketchat methods outside the server.

        **Example Requests**:

            GET /rocketchat/api/v0/credentials?courseId=course-v1:ExampleX+Subject101+2015

        **Response Values**:

            * url_servie: Rocketchat url where the services is allocated

            * auth_token: Rocketchat authorization token.

            * user_id: the unique rocketchat identifier for the user.

        """
        user = request.user
        course_id = request.GET.get("courseId")

        if not course_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        course_key = get_course_from_string(course_id)

        rocket_chat_settings = get_rocket_chat_settings()

        api_rocket_chat = initialize_api_rocket_chat(rocket_chat_settings)

        if api_rocket_chat:

            response = create_token(api_rocket_chat, user, course_key)

            if not response:
                LOG.error("Rocketchat API can not create a user's token")
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            url_service = rocket_chat_settings.get('public_url_service', None)

            data = response.get('data', {})

            auth_token = data.get('authToken', None)
            user_id = data.get('userId', None)

            serializer = RocketChatCredentialsSerializer(
                data={
                    "url_service": url_service,
                    "auth_token": auth_token,
                    "user_id": user_id,
                }
            )
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)

        LOG.error("Rocketchat API object can not be initialized")
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RocketChatSubscriptionsId(APIView):

    authentication_classes = (
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Retrieve the rooms' id for every user subscription.

        **Example Requests**:

            GET /rocketchat/api/v0/subscriptions-id?unread=true&authToken=asdjfsdhfgasdas&&userId=86435f4asd56f4a

            * unread : True to retrieve only subscription where the user has unread mentions.userId
            * authToken : Rocketchat authorization token.
            * userId : The unique rocketchat identifier for the user.

        **Response Values**:

            * subscriptions_id : A list with the room's id for every user subscription.

        """
        try:
            unread = request.GET.get("unread")
            auth_token = request.GET.get("authToken")
            user_id = request.GET.get("userId")
            serializer = RocketChatSubscriptionsIdSerializer(
                data={
                    "subscriptions_id": list(get_subscriptions_rids(auth_token, user_id, unread))
                }
            )
            if serializer.is_valid():

                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as error:
            LOG.error("Rocketchat Subscriptions couldn't be got due to %s", error)
            pass

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class RocketChatChangeRole(APIView):

    authentication_classes = (
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        This methods allows to change the rocketchat role for a specific user

        **Example Requests**:

            POST /rocketchat/api/v0/change-role

            * data = {
                "username": "edx",
                "role": "admin",
            }

        **Response Values**:

            * It doesn't return data

        """
        if not request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = RocketChatChangeRoleSerializer(data=request.data)

        if not serializer.is_valid():
            return Response("Data is not valid", status=status.HTTP_400_BAD_REQUEST)

        username = serializer.data["username"]
        role = serializer.data["role"]

        rocket_chat_settings = get_rocket_chat_settings()

        api_rocket_chat = initialize_api_rocket_chat(rocket_chat_settings)

        if api_rocket_chat:

            user_info = api_rocket_chat.users_info(username=username)

            try:
                user_info = user_info.json()
                if not user_info.get('success', False):
                    return Response(user_info.get("error"), status=status.HTTP_400_BAD_REQUEST)

                user = user_info.get("user")
                data = {"roles": [role]}
                response = api_rocket_chat.users_update(user.get("_id"), **data)
                if response.status_code == 200:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response(response.json().get("error"), status=status.HTTP_400_BAD_REQUEST)

            except AttributeError:
                LOG.error("Rocketchat API can not get the user information")
                return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

        LOG.error("Rocketchat API object can not be initialized")
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RocketChatCleanToken(APIView):

    authentication_classes = (
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Invalidate the rocketchat user data store on the server.

        **Example Requests**:

            GET /rocketchat/api/v0/clean-token-cache?beacon_rc=86435f4asd56f4a

            * beacon_rc : A unique user identifier. This is created from ROCKET_CHAT_DATA and username

        **Response Values**:

            * It doesn't return data

        """
        key = request.GET.get('beacon_rc')
        response = cache.get(key)

        if response:
            data = response.get('data', {})
            auth_token = data.get('authToken', None)
            user_id = data.get('userId', None)
            logout_status = logout(auth_token, user_id)

            if logout_status.get("status") == "success":
                cache.delete(key)
                return Response(status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
