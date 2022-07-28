from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
    
    def has_object_permission(self, request, view, obj):

        if obj.author != request.user:
            return False

        return True
