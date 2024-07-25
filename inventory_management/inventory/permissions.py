from rest_framework.permissions import BasePermission

class IsAdminUserOrReadOnlyForItems(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and (request.user.is_staff or request.user.is_superuser)

class IsAdminUserOrReadOnlyForSuppliers(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user and (request.user.is_staff or request.user.is_superuser)
        return request.user and (request.user.is_staff or request.user.is_superuser)