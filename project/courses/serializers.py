from .models import Course, CourseProgress, CoursesGroup
from rest_framework.serializers import ModelSerializer
from articles.serializers import ArticleListSerializerWithTest
from rest_framework import serializers
from articles.models import Article
from tests.models import Test


class CourseListSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "description", "date_create", "date_update", "position")


class CourseDetailSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "date_create",
            "date_update",
            "position",
            "articles",
        )


class CourseArticleSerializer(ArticleListSerializerWithTest):

    read = serializers.SerializerMethodField()

    class Meta(ArticleListSerializerWithTest.Meta):
        fields = ArticleListSerializerWithTest.Meta.fields + ["read"]

    def get_read(self, instance: Article):
        user = self.context["request"].user
        course_id = self.context["view"].kwargs.get("pk")
        if not CourseProgress.objects.filter(user=user, course_id=course_id).exists():
            return False
        course_progress = CourseProgress.objects.get(user=user, course_id=course_id)
        return course_progress.articles_read.filter(id=instance.id).exists()

    def get_test(self, instance: Article):
        data = super().get_test(instance)
        if data is None:
            return None
        user = self.context["request"].user
        course_id = self.context["view"].kwargs.get("pk")
        if not CourseProgress.objects.filter(user=user, course_id=course_id).exists():
            return data
        course_progress = CourseProgress.objects.get(user=user, course_id=course_id)
        data["passed"] = course_progress.passed_tests.filter(id=data["id"]).exists()
        return data


class CourseDetailRetrieveSerializer(CourseDetailSerializer):

    articles = CourseArticleSerializer(many=True)

    class Meta(CourseDetailSerializer.Meta):
        pass


class CourseGroupListSerializer(ModelSerializer):

    class Meta:
        model = CoursesGroup
        fields = ["id", "name"]


class CourseGroupDetailSerializer(CourseGroupListSerializer):
    courses = CourseDetailSerializer(many=True)

    class Meta(CourseGroupListSerializer.Meta):
        fields = CourseGroupListSerializer.Meta.fields + ["courses"]
