import django.core.exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from .models import Article, Comment
from .serializers import (
    ArticleDetailSerializer,
    ArticleListSerializer,
    ArticleListSerializerWithTest,
    CommentSerializer
)
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStaffOrReadOnly
from rest_framework.response import Response
from tests.models import Test
from tests.serializers import TestSerializerDetail
from rest_framework.exceptions import NotFound


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            w = self.request.query_params.get("with")
            if w is not None:
                if w == "test":
                    return ArticleListSerializerWithTest
            return ArticleListSerializer
        return ArticleDetailSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Article.objects.all().order_by("position").prefetch_related("section")
        )
        if not user.is_staff:
            queryset = (
                queryset.filter(section_id__in=user.view_list)
                .order_by("position")
                .prefetch_related("section")
            )
        section_id = self.request.query_params.get("section")
        if section_id is not None:
            queryset = queryset.filter(section_id=section_id)
        return queryset

    def perform_create(self, serializer):
        section_id = serializer.validated_data.get("section").id
        if (
            not self.request.user.is_staff
            and section_id not in self.request.user.change_list
        ):
            raise PermissionDenied(
                detail="You do not have permission to create this article."
            )
        serializer.save()

    def perform_update(self, serializer):
        section = serializer.validated_data.get("section")
        if section is not None:
            if (
                not section.id in self.request.user.change_list
                and not self.request.user.is_staff
            ):
                raise PermissionDenied(
                    detail="You do not have permission to move to this section."
                )
        self.check_object_permissions(self.request, serializer.instance)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"result": "deleted"}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.delete()

    @action(detail=True, methods=["get", "post", "delete", "patch"], url_path="comments")
    def comments(self, request, pk: int = None):
        if request.method == "GET":
            comments = Comment.objects.filter(article_id=pk).all()
            serializer = CommentSerializer(instance=comments, many=True)
            return Response(serializer.data)
        if request.method == "POST":
            data = request.data.copy()
            data["article"] = pk
            serializer = CommentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.validated_data)
            return Response(serializer.data)


    @action(detail=True, methods=["get", "post", "patch", "delete"], url_path="test")
    def test(self, request, pk=None):
        if request.method == "GET":
            try:
                test = Test.objects.get(article_id=pk)
            except django.core.exceptions.ObjectDoesNotExist:
                raise NotFound()
            serializer = TestSerializerDetail(instance=test)
            return Response(serializer.data)
        elif request.method == "POST":
            data = request.data.copy()
            print(pk)
            data["article"] = pk
            serializer = TestSerializerDetail(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.validated_data)
            return Response(serializer.data)
        elif request.method == "PATCH":
            data = request.data.copy()
            print(data)
            data["article"] = pk
            try:
                instance = Test.objects.get(article_id=pk)
            except django.core.exceptions.ObjectDoesNotExist:
                raise NotFound()
            serializer = TestSerializerDetail(instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == "DELETE":
            try:
                instance = Test.objects.get(article_id=pk)
            except django.core.exceptions.ObjectDoesNotExist:
                raise NotFound()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                raise PermissionDenied(
                    detail=f"You do not have permission to perform this action on {obj}."
                )
