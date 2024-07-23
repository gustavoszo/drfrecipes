from rest_framework import permissions

class MyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)

    def has_permission(self, request, view):
        return True if request.method == 'POST' else False