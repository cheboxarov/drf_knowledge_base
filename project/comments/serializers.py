from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author_id", "date_created", "text", "article"]
        read_only_fields = ["author_id", "article"]
