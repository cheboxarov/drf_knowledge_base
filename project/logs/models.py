from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from users.models import User


class LogEntryBase(models.Model):
    class Type(models.TextChoices):
        EDIT = "edit", "Edit"
        DELETE = "delete", "Delete"
        CREATE = "create", "Create"
        UPDATE = "update", "Update"

    type = models.CharField(max_length=10, choices=Type.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs_logentry_set",
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="logs_logentry_set"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True


class LogEntry(LogEntryBase):
    # Дополнительные поля, если необходимо
    pass
