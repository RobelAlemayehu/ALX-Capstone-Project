from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the activity
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners to access their own objects.
    """
    def has_object_permission(self, request, view, obj):
        # Only the owner can access their own object
        return obj.user == request.user


class IsUserOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own profile.
    """
    def has_object_permission(self, request, view, obj):
        # Users can only access their own profile
        return obj == request.user

