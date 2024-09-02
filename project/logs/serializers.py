from rest_framework import serializers
from .models import LogEntry


class LogEntryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogEntry
        fields = ("id", "type", "timestamp", "user", "content_type", "object_id")