from django.db import models, transaction
from django.db.models import Max, F


class Section(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    description = models.TextField()
    position = models.PositiveIntegerField(default=0, db_index=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.pk:
                # Это новая секция, устанавливаем позицию на максимальное значение + 1
                max_position = Section.objects.aggregate(Max('position'))['position__max']
                self.position = (max_position or 0) + 1
            else:
                # Получаем текущую позицию из базы данных
                current_position = Section.objects.get(pk=self.pk).position

                if self.position != current_position:
                    if self.position > current_position:
                        # Сдвигаем секции вниз
                        Section.objects.filter(position__gt=current_position, position__lte=self.position).update(position=F('position') - 1)
                    else:
                        # Сдвигаем секции вверх
                        Section.objects.filter(position__lt=current_position, position__gte=self.position).update(position=F('position') + 1)

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Сдвигаем секции вверх
            Section.objects.filter(position__gt=self.position).update(position=F('position') - 1)
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

