from rest_framework import permissions

class IsChefAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'chef_agent'

class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'agent'


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'


class IsChefManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'chef_manager'
