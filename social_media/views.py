from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from social_media.models import Post, Comment
from social_media.serializers import (
    PostSerializer,
    PostCreateSerializer,
    PostListSerializer,
    CommentDetailSerializer, CommentListSerializer,
)
from user.permissions import IsPostOwnerOrReadOnly


class PostListView(generics.ListAPIView):
    queryset = (
        Post.objects.prefetch_related("liked_by", "comments").
        select_related("author")
    )
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


class CommentListView(generics.ListAPIView):
    queryset = (
        Comment.objects.
        select_related("author", "post",).
        prefetch_related("liked_by")
    )
    serializer_class = CommentListSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return queryset.filter(post=post)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentDetailSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.validated_data["author"] = self.request.user
        serializer.validated_data["post_id"] = self.kwargs.get("post_id")
        serializer.save()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return Comment.objects.filter(post=post)
