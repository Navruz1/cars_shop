from rest_framework.permissions import IsAuthenticated, BasePermission

# User or Admin
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user

# Admin
class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return False

# Owner
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user