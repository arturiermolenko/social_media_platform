from django.urls import path

from social_media.views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    CommentListView,
    CommentCreateView,
    CommentDetailView,
    LikeUnlikeView,
)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="posts-list"),
    path("posts/create/", PostCreateView.as_view(), name="posts-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="posts-detail"),
    path("posts/<int:pk>/like_unlike/", LikeUnlikeView.as_view(), name="like-unlike"),
    path(
        "posts/<int:post_id>/comments/", CommentListView.as_view(), name="comment-list"
    ),
    path(
        "posts/<int:post_id>/comments/add/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "posts/<int:post_id>/comments/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
]

app_name = "social_media"
