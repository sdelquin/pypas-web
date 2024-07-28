from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from assignments.models import Assignment

from .models import Exercise


@receiver(post_delete, sender=Exercise)
def remove_folder(sender, instance, **kwargs):
    instance.remove_folder()


@receiver(pre_save, sender=Exercise)
def rename_assignment_exercise_folder(sender, instance, **kwargs):
    for assignment in Assignment.objects.all():
        assignment.rename_exercise_folder(instance)
