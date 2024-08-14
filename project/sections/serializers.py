from rest_framework import serializers
from .models import Section


class SectionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            "id",
            "name",
            "description",
            "position",
            "date_update",
            "date_created",
        ]
