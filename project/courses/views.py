from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db.models.query import Q
from rest_framework.response import Response
from .models import Course, CourseProgress, TestLog
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStaffOrReadOnly
from rest_framework.decorators import action
from .serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    CourseDetailRetrieveSerializer,
)
from articles.models import Article
from tests.models import Test


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    @action(detail=True, methods=["POST"], url_path="article-read")
    def article_read(self, request, pk=None):
        data = request.data.copy()

        article_id = data.get(
            "article_id",
        )
        course = Course.objects.get(id=pk)
        if article_id == None:
            return Response(
                {"Error": "There is no article_id in the request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not Article.objects.filter(
            id=article_id, section__project=self.request.user.project
        ).exists():
            return Response(
                {"Error": "Article not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if not course.articles.filter(id=article_id).exists():
            return Response(
                {"Error": "Article not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if not CourseProgress.objects.filter(
            user=self.request.user, course_id=pk
        ).exists():
            CourseProgress.objects.create(user=self.request.user, course_id=pk)
        course_progress = CourseProgress.objects.get(
            user=self.request.user, course_id=pk
        )
        course_progress.articles_read.add(article_id)
        course_progress.save()
        return Response({"Result": "Oke"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="test-passed")
    def passed_test(self, request, pk=None):
        data = request.data.copy()

        test_id = data.get("test_id")
        if test_id is None:
            return Response({"Error": "test_id is expected in the request body"})
        time_spend = data.get("time_spend")
        if time_spend is None:
            return Response({"Error": "time_spend is expected in the request body"})
        number_of_errors = data.get("number_of_errors")
        if number_of_errors is None:
            return Response(
                {"Error": "number_of_errors is expected in the request body"}
            )
        course = Course.objects.get(id=pk)
        if not Test.objects.filter(id=test_id).exists():
            return Response(
                {"Error": "Article not found"}, status=status.HTTP_404_NOT_FOUND
            )
        test = Test.objects.get(id=test_id)
        article = test.article
        if not course.articles.filter(id=article.id).exists():
            return Response(
                {"Error": "The test does not belong to the course"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not CourseProgress.objects.filter(
            user=self.request.user, course_id=pk
        ).exists():
            CourseProgress.objects.create(user=self.request.user, course_id=pk)
        TestLog.objects.create(
            test=test,
            course=course,
            user=self.request.user,
            time_spend=time_spend,
            number_of_errors=number_of_errors,
        )
        if number_of_errors == 0:
            course_progress = CourseProgress.objects.get(
                user=self.request.user, course_id=pk
            )
            course_progress.passed_tests.add(test_id)
            course_progress.save()
        return Response({"Result": "Oke"}, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return (
                Course.objects.filter(project=user.project)
                .order_by("position")
                .prefetch_related("project")
                .prefetch_related("articles")
                .prefetch_related("articles__section")
                .prefetch_related("articles__section__project")
            )
        return (
            Course.objects.filter(Q(id__in=user.view_list) & Q(project=user.project))
            .order_by("position")
            .prefetch_related("project")
            .prefetch_related("articles")
            .prefetch_related("articles__section")
            .prefetch_related("articles__section__project")
        )

    def get_serializer_class(self):
        print(self.action)
        if self.action == "list":
            return CourseListSerializer
        if self.action == "retrieve":
            return CourseDetailRetrieveSerializer
        return CourseDetailSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied(
                detail="You do not have permission to create this course."
            )
        project = self.request.user.project
        serializer.save(project=project)

    def perform_update(self, serializer):
        self.check_object_permissions(self.request, serializer.instance)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"result": "deleted"}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.delete()

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                raise PermissionDenied(
                    detail=f"You do not have permission to perform this action on {obj}."
                )
