from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Assignment


@receiver(post_delete, sender=Assignment)
def remove_folder(sender, instance, **kwargs):
    instance.remove_folder()
