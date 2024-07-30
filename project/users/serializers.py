from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['amo_id', 'change_list', 'view_list', 'is_staff']