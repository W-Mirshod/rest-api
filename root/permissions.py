from rest_framework import permissions


class CustomPermissions(permissions.BasePermission):
    message = 'You do not have permission to enter this page.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if request.method in ['PATCH', 'PUT']:
                return True

            if request.method in ['DELETE'] and request.user.is_superuser:
                return True
