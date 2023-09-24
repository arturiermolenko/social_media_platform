from django.contrib.auth import get_user_model
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.permissions import IsAccountOwnerOrReadOnly
from user.serializers import (
    UserListSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
)


class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["email", "first_name", "last_name"]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["email"]


class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAccountOwnerOrReadOnly,)
    serializer_class = UserDetailSerializer


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
