from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from social_media.models import Post
from social_media.serializers import (
    PostSerializer,
    PostCreateSerializer,
    PostListSerializer,
)
from user.permissions import IsPostOwnerOrReadOnly


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PostListSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.validated_data["author"] = self.request.user
        serializer.save()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsPostOwnerOrReadOnly,)
    serializer_class = PostSerializer

