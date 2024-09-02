import django.core.exceptions
from rest_framework import serializers
from .models import Article
from tests.models import Test
from tests.serializers import TestSerializerDetail
from logs.signals import log_save


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

    def create(self, validated_data):
        user = validated_data.pop("user")
        instance = super().create(validated_data)
        log_save(sender=self.Meta.model, instance=instance, created=True, user=user)
        return instance

    def update(self, instance, validated_data):
        user = validated_data.pop("user", None)
        instance = super().update(instance, validated_data)
        log_save(sender=self.Meta.model, instance=instance, created=False, user=user)
        return instance

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
    test = serializers.SerializerMethodField()

    class Meta(ArticleListSerializer.Meta):
        fields = ArticleListSerializer.Meta.fields + ["test"]

    def get_test(self, obj):
        try:
            test = (
                Test.objects.select_related("article")
                .select_related("article__section")
                .select_related("article__section__project")
                .get(article_id=obj.id)
            )
            return TestSerializerDetail(test).data
        except Test.DoesNotExist:
            return None
