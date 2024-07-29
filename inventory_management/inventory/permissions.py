import logging
from rest_framework.permissions import BasePermission

logger = logging.getLogger('myapp')

class IsAdminUserOrReadOnlyForItems(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':  # anyone can access get api's even if they are not logged in
            return True 
        is_admin = request.user and (request.user.is_staff or request.user.is_superuser)
        if not is_admin:
            logger.warning(f'Permission denied for user: {request.user}')
        return is_admin

class IsAdminUserOrReadOnlyForSuppliers(BasePermission):
    def has_permission(self, request, view):
        is_admin = request.user and (request.user.is_staff or request.user.is_superuser)
        if not is_admin:
            logger.warning(f'Permission denied for user: {request.user}')
        return is_admin
