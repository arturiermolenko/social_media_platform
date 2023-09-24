from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import FollowUnfollowView, UserViewSet

router = routers.DefaultRouter()
router.register("users", UserViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("follow_unfollow/", FollowUnfollowView.as_view(), name="follow_unfollow"),
]

app_name = "user"

