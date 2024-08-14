from rest_framework.permissions import BasePermission


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        if hasattr(obj, "section"):
            section_id = obj.section.id
        elif hasattr(obj, "id"):
            section_id = obj.id
        else:
            return False

        return request.user and (
            request.user.is_staff or (section_id in request.user.change_list)
        )


class UserEditPermissons(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False
