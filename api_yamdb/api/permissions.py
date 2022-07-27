from rest_framework import permissions

class AdminOrAuthorOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and (user.role == 'admin' or user.is_superuser):
            return True
        return False