from django.db import models, transaction
from django.db.models import Max, F

class Article(models.Model):
    name = models.CharField(max_length=255, blank=True, db_index=True)
    section = models.ForeignKey('sections.Section', on_delete=models.CASCADE, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    author = models.PositiveBigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    content = models.TextField()
    position = models.PositiveIntegerField(default=0, db_index=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.pk:
                # Это новая статья, устанавливаем позицию на максимальное значение + 1 в рамках секции
                max_position = Article.objects.filter(section=self.section).aggregate(Max('position'))['position__max']
                self.position = (max_position or 0) + 1
            else:
                # Получаем текущую позицию из базы данных
                current_position = Article.objects.get(pk=self.pk).position

                if self.position != current_position:
                    if self.position > current_position:
                        # Сдвигаем статьи вниз в рамках секции
                        Article.objects.filter(section=self.section, position__gt=current_position, position__lte=self.position).update(position=F('position') - 1)
                    else:
                        # Сдвигаем статьи вверх в рамках секции
                        Article.objects.filter(section=self.section, position__lt=current_position, position__gte=self.position).update(position=F('position') + 1)

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Сдвигаем статьи вверх в рамках секции
            Article.objects.filter(section=self.section, position__gt=self.position).update(position=F('position') - 1)
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
