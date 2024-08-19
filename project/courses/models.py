from django.db import models, transaction
from django.db.models import Max, F
from articles.models import Article
from tests.models import Test


class Course(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, null=True)
    articles = models.ManyToManyField(Article)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    position = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.pk:
                # Это новая секция, устанавливаем позицию на максимальное значение + 1
                max_position = Course.objects.aggregate(Max("position"))[
                    "position__max"
                ]
                self.position = (max_position or 0) + 1
            else:
                # Получаем текущую позицию из базы данных
                current_position = Course.objects.get(pk=self.pk).position

                if self.position != current_position:
                    if self.position > current_position:
                        # Сдвигаем секции вниз
                        Course.objects.filter(
                            position__gt=current_position, position__lte=self.position
                        ).update(position=F("position") - 1)
                    else:
                        # Сдвигаем секции вверх
                        Course.objects.filter(
                            position__lt=current_position, position__gte=self.position
                        ).update(position=F("position") + 1)

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Сдвигаем секции вверх
            Course.objects.filter(position__gt=self.position).update(
                position=F("position") - 1
            )
            super().delete(*args, **kwargs)


class CourseProgress(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    articles_read = models.ManyToManyField("articles.Article", null=True, blank=True)
    passed_tests = models.ManyToManyField("tests.Test", null=True, blank=True)

    def __str__(self):
        return f"Прогресс по курсу {self.course.name} от {self.user.username}"


class TestLog(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    time_spend = models.PositiveIntegerField(default=0)
    number_of_errors = models.PositiveIntegerField(default=0)
