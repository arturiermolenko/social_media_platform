from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.permissions import IsAccountOwnerOrReadOnly
from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserRetrieveSerializer,
)


class UserViewSet(
    viewsets.ModelViewSet
):
    queryset = get_user_model().objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAccountOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer

        if self.action == "create":
            return UserCreateSerializer

        if self.action in ("update", "partial_update"):
            return UserUpdateSerializer

        if self.action == "retrieve":
            return UserRetrieveSerializer

        return UserSerializer


class FollowUnfollowView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def current_user(self):
        try:
            return get_user_model().objects.get(id=self.request.user.id)
        except get_user_model().DoesNotExist:
            raise Http404

    @staticmethod
    def other_user(pk):
        try:
            return get_user_model().objects.get(id=pk)
        except get_user_model().DoesNotExist:
            raise Http404

    def post(self, request):
        pk = request.data.get("id")
        req_type = request.data.get("type")

        current_user = self.current_user()
        other_user = self.other_user(pk)

        if req_type == "follow":
            current_user.following.add(other_user)
            other_user.followers.add(current_user)
            return Response(
                {"Following": "Following success!!"}, status=status.HTTP_200_OK
            )
        elif req_type == "unfollow":
            current_user.following.remove(other_user)
            other_user.followers.remove(current_user)
            return Response(
                {"Unfollow": "Unfollow success!!"}, status=status.HTTP_200_OK
            )
