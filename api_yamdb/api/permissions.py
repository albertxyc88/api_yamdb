from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.role == 'USER':
            return True
        return False


class ModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.role == 'MODERATOR':
            return True
        return False


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and (user.role == 'ADMIN' or user.is_superuser):
            return True
        return False


class OwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj.author
        return False


class IsAdminOrSuperUser(permissions.BasePermission):
    """Права доступа для администратора"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.role == 'ADMIN':
            return True


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'ADMIN')