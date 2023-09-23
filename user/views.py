from django.conf import settings
from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ListUserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class FollowUnfollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def current_user(self):
        try:
            return User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            raise Http404

    @staticmethod
    def other_user(pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
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
