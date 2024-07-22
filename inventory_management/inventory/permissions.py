from rest_framework.permissions import BasePermission

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only methods
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Allow admin users to perform write operations
        return request.user and (request.user.is_staff or request.user.is_superuser)
