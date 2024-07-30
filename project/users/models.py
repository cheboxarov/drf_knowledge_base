from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
    amo_id = models.PositiveIntegerField(null=True, blank=True)
    change_list = ArrayField(models.PositiveIntegerField(), default=list, blank=True)
    view_list = ArrayField(models.PositiveIntegerField(), default=list, blank=True)
    last_amo_token = models.TextField(null=True, blank=True, db_index=True)

    def __str__(self):
        return self.username
