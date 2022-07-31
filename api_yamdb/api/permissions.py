from rest_framework import permissions


class Is_AuthorAdminModeratorCreate_Or_ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
    
    def has_object_permission(self, request, view, obj):

        if (
            request.user != obj.author or
            request.user.role == 'moderator' or
            request.user.role == 'admin'
        ):
            return False

        return True

class AllowwAnyPlease(permissions.BasePermission):
    def has_permission(self, request, view):
        if self.request.method == 'GET':
            return True
