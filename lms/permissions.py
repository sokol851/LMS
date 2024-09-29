from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="Moderator").exists():
            return True
