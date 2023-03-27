from rest_framework import permissions


class isOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user == obj.author


class isModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class isAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class isOwnerModeratorAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user == obj or request.user == obj.author
                or request.user.role == 'moderator'
                or request.user.role == 'admin')


class isOwnerAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj or request.user == obj.author
                or request.user.role == 'admin')


class isModeratorAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator' or request.user.role == 'admin'
