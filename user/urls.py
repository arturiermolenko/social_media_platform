from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CreateUserView, ManageUserView, FollowUnfollowView, ListUserView

urlpatterns = [
    path("all/", ListUserView.as_view(), name="list"),
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("follow_unfollow/", FollowUnfollowView.as_view(), name="follow_unfollow"),
]

app_name = "user"
