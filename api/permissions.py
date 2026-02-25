from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'profile') and 
                   request.user.profile.role == 'admin')
    
    def has_object_permission(self, request):
        return bool(request.user and request.user.is_authenticated and 
                   hasattr(request.user, 'profile') and 
                   request.user.profile.role == 'admin')
    

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is admin
        is_admin = bool(request.user and request.user.is_authenticated and 
                       hasattr(request.user, 'profile') and 
                       request.user.profile.role == 'admin')
        
        return obj.user == request.user or is_admin
    
