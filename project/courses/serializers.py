from .models import Course
from rest_framework.serializers import ModelSerializer


class CourseDetailSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'