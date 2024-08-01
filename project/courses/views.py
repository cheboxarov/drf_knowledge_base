from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.db.models.query import Q
from rest_framework.response import Response

from .models import Course
from .serializers import CourseDetailSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStaffOrReadOnly
from rest_framework.decorators import action


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.filter(project=user.project).order_by('position')
        return Course.objects.filter(Q(id__in=user.view_list) & Q(project=user.project)).order_by('position')

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied(detail="You do not have permission to create this course.")
        project = self.request.user.project
        serializer.save(project=project)

    def perform_update(self, serializer):
        self.check_object_permissions(self.request, serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.delete()

    @action(detail=True, methods=['get', 'post', 'delete'], url_path='articles')
    def articles(self, request, *args, **kwargs):
        return Response({"asd":"asdasd"})

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                raise PermissionDenied(detail=f"You do not have permission to perform this action on {obj}.")