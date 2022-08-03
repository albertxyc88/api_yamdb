from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

User = get_user_model()


class IsAdminOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser
            )
        )


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser
                )
            )
        )


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ModeratorOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)
