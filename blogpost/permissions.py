from rest_framework.permissions import BasePermission
SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.created_by == request.user:
            return True
        return False