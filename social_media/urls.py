from django.urls import path

from social_media.views import PostListView, PostCreateView, PostDetailView

urlpatterns = [
    path("posts/", PostListView.as_view(), name="posts-list"),
    path("posts/create/", PostCreateView.as_view(), name="posts-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="posts-detail"),

]

app_name = "social_media"
