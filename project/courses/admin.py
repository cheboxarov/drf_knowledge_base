from django.contrib import admin
from .models import Course, CourseProgress, CoursesGroup


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "date_create", "date_update")


@admin.register(CoursesGroup)
class CoursesGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project", "date_create", "date_update")


admin.site.register(CourseProgress)
