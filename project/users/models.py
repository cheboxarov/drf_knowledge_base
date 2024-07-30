from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
    amo_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    change_list = ArrayField(models.PositiveIntegerField(), default=list, blank=True)
    view_list = ArrayField(models.PositiveIntegerField(), default=list, blank=True)
    amo_uuid = models.TextField(null=True, blank=True, db_index=True)
    last_sub_url = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username
