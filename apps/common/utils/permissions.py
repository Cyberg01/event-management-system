from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission class to check if user is admin.
    
    Used to protect admin-only endpoints such as:
    - Create user account
    - List users
    - Delete user
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated and has ADMIN role"""
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class to check if user is owner or admin.
    
    Owner can modify own profile, Admin can modify any profile.
    """
    
    def has_permission(self, request, view):
        """User must be authenticated"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """User can access if owner or admin"""
        return obj == request.user or request.user.role == 'ADMIN'


class IsSuperUser(permissions.BasePermission):
    """
    Permission class to check if user is a superuser.
    
    Only superuser can create, list, and manage admin accounts.
    Used to protect sensitive admin management endpoints:
    - Create admin account
    - List admin accounts
    - Delete admin account
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated and is a superuser"""
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )