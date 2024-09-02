from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import LogEntry, LogEntryBase
import sys


@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if "migrate" in sys.argv or "migrate --run-syncdb" in sys.argv:
        return
    if not isinstance(instance.pk, int):
        return
    user = kwargs.get("user")
    if user is None:
        return
    if not issubclass(sender, LogEntry):
        action = LogEntry.Type.CREATE if created else LogEntry.Type.UPDATE
        LogEntry.objects.create(
            type=action,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            content_object=instance,
            user=user,
        )


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if "migrate" in sys.argv or "migrate --run-syncdb" in sys.argv:
        return
    if not isinstance(instance.pk, int):
        return
    user = kwargs.get("user")
    if user is None:
        return
    if not issubclass(sender, LogEntry):
        LogEntry.objects.create(
            type=LogEntry.Type.DELETE,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            content_object=instance,
            user=user,
        )
