from rest_framework import serializers
from .models import Section


class SectionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'