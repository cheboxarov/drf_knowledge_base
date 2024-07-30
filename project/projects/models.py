from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    suburl = models.CharField(max_length=255, db_index=True, unique=True)
    amo_id = models.PositiveBigIntegerField(unique=True)
    is_active = models.BooleanField(default=False)
    amo_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
