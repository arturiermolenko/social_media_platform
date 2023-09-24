from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an account to edit it.
    """
    def has_object_permission(self, request, view, user):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        if request.method == "POST":
            return True
        if request.method in ("PUT", "PATCH", "DELETE"):
            return request.user == user
