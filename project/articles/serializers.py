import django.core.exceptions
from rest_framework import serializers
from .models import Article
from tests.models import Test


class ArticleListSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["id", "name", "position", "parent", "section", "can_edit"]

    def get_can_edit(self, obj):
        user = self.context["request"].user
        if user.is_staff:
            return True
        return obj.section.id in user.change_list


class ArticleDetailSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "name",
            "section",
            "parent",
            "author",
            "position",
            "content",
            "date_created",
            "date_update",
            "can_edit",
        ]

    def get_can_edit(self, obj):
        user = self.context["request"].user
        if user.is_staff:
            return True
        return obj.section.id in user.change_list

    def validate(self, data):
        parent = data.get("parent")
        section = data.get("section")

        if parent and parent.section != section:
            raise serializers.ValidationError(
                "The section of the parent article must match the section of the article being modified."
            )
        return data


class ArticleListSerializerWithTest(ArticleListSerializer):
    test_id = serializers.SerializerMethodField()

    class Meta(ArticleListSerializer.Meta):
        fields = ArticleListSerializer.Meta.fields + ["test_id"]

    def get_test_id(self, obj):
        try:
            test = Test.objects.get(article_id=obj.id)
            return test.id
        except django.core.exceptions.ObjectDoesNotExist:
            return None
