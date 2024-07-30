from rest_framework import serializers
from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'name', 'position', 'parent', 'section', 'can_edit']

    def get_can_edit(self, obj):
        user = self.context['request'].user
        if user.is_staff:
            return True
        return obj.section.id in user.change_list


class ArticleDetailSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [field.name for field in Article._meta.get_fields() if field.name != 'article'] + ['can_edit']

    def get_can_edit(self, obj):
        user = self.context['request'].user
        if user.is_staff:
            return True
        return obj.section.id in user.change_list

    def validate(self, data):
        parent = data.get('parent')
        section = data.get('section')

        if parent and parent.section != section:
            raise serializers.ValidationError(
                "The section of the parent article must match the section of the article being modified.")
        return data
