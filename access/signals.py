from django.db.models.signals import pre_save
from django.dispatch import receiver

from assignments.models import Assignment

from .models import Context, User


@receiver(pre_save, sender=User)
def rename_assignment_user_folder(sender, instance, **kwargs):
    for assignment in Assignment.objects.all():
        assignment.rename_user_folder(instance)


@receiver(pre_save, sender=Context)
def rename_assignment_context_folder(sender, instance, **kwargs):
    for assignment in Assignment.objects.all():
        assignment.rename_context_folder(instance)
