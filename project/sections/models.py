from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    project_id = models.PositiveBigIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    description = models.TextField()
    position = models.PositiveIntegerField(default=0, db_index=True)

    def __str__(self):
        return self.name
