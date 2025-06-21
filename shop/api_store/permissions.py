from rest_framework import permissions

class IsViewAndEditOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return request.user.groups.filter(name='ViewAndEdit').exists()
        if request.method in ['PATCH', 'PUT']:
            return request.user.groups.filter(name='ViewAndEdit').exists()
        return False

class IsViewAndDeleteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name='ViewAndDelete').exists()
        if request.method == 'DELETE':
            return request.user.groups.filter(name='ViewAndDelete').exists()
        return False

class IsViewAndDeleteOnlyRole3(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name='ViewAndDeleteRole3').exists()
        if request.method == 'DELETE':
            return request.user.groups.filter(name='ViewAndDeleteRole3').exists()
        return False