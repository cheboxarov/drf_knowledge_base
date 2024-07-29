from rest_framework.exceptions import PermissionDenied

from .models import Section
from rest_framework import viewsets
from .serializers import SectionDetailSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStaffOrReadOnly


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionDetailSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Section.objects.all()
        return Section.objects.filter(id__in=user.view_list)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied(detail="You do not have permission to create this section.")
        serializer.save()

    def perform_update(self, serializer):
        self.check_object_permissions(self.request, serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.delete()

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                raise PermissionDenied(detail=f"You do not have permission to perform this action on {obj}.")