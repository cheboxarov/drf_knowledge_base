from django.contrib import admin
from .models import Course, CourseProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "date_create", "date_update")


admin.site.register(CourseProgress)
