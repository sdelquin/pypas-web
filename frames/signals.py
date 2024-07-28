from django.db.models.signals import pre_save
from django.dispatch import receiver

from assignments.models import Assignment

from .models import Bucket


@receiver(pre_save, sender=Bucket)
def rename_assignment_bucket_folder(sender, instance, **kwargs):
    for assignment in Assignment.objects.all():
        assignment.rename_bucket_folder(instance)
