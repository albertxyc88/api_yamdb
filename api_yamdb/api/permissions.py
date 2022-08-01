from lib2to3.pytree import Base
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


User = get_user_model()


class IsAdminOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        access_roles = ('admin',)
        return (
            user.is_authenticated and 
            (user.role in access_roles or user.is_superuser or user.is_staff)
        )


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        access_roles = ('admin',)
        if request.method in SAFE_METHODS:
            return True
        return (
            user.is_authenticated and 
            (user.role in access_roles or user.is_superuser or user.is_staff)
        )


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
