from rest_framework import serializers
from .models import Section


class SectionDetailSerializer(serializers.ModelSerializer):

    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = [
            "id",
            "name",
            "description",
            "position",
            "date_update",
            "date_created",
            "can_edit",
        ]

    def get_can_edit(self, obj):
        user = self.context["request"].user
        if user.is_staff:
            return True
        return obj.id in user.change_list
