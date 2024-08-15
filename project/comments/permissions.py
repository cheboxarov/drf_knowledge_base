from rest_framework.permissions import BasePermission


class IsStaffOrOwner(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author_id == request.user.amo_id
