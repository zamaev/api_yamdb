from rest_framework import permissions


class isOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user == obj.author


class isModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'M'


class isAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'A'


class isOwnerModeratorAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj or request.user == obj.author
                or request.user.role == 'M' or request.user.role == 'A')


class isOwnerAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj or request.user == obj.author
                or request.user.role == 'A')


class isModeratorAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'M' or request.user.role == 'A'
