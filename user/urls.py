from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import (
    FollowUnfollowView,
    UserCreateView,
    UserListView,
    UserDetailView,
    UserFollowersView,
    UserFollowingView,
    UserLikedPostsView,
)

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("register/", UserCreateView.as_view(), name="user-create"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("<int:pk>/followers/", UserFollowersView.as_view(), name="user-followers"),
    path("<int:pk>/following/", UserFollowingView.as_view(), name="user-following"),
    path(
        "<int:pk>/liked_posts/", UserLikedPostsView.as_view(), name="user-liked-posts"
    ),
    path("follow_unfollow/", FollowUnfollowView.as_view(), name="follow_unfollow"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

app_name = "user"
