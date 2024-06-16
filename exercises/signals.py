from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Exercise


@receiver(post_delete, sender=Exercise)
def remove_folder(sender, instance, **kwargs):
    instance.remove_folder()
