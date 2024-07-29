from rest_framework.exceptions import PermissionDenied

from .models import Article
from .serializers import ArticleDetailSerializer, ArticleListSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStaffOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Article.objects.all()
        if not user.is_staff:
            queryset = queryset.filter(section_id__in=user.view_list)

        section_id = self.request.query_params.get('section')
        if section_id is not None:
            queryset = queryset.filter(section_id=section_id)

        return queryset

    def perform_create(self, serializer):
        section_id = serializer.validated_data.get('section').id
        if not self.request.user.is_staff and section_id not in self.request.user.change_list:
            raise PermissionDenied(detail="You do not have permission to create this article.")
        serializer.save()

    def perform_update(self, serializer):
        if not serializer.validated_data.get('section').id in self.request.user.change_list:
            raise PermissionDenied(detail="You do not have permission to move to this section.")
        self.check_object_permissions(self.request, serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.delete()

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                raise PermissionDenied(detail=f"You do not have permission to perform this action on {obj}.")