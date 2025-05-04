from django.db.models.signals import pre_save
from django.dispatch import receiver

from assignments.models import Assignment

from .models import Chunk


@receiver(pre_save, sender=Chunk)
def rename_assignment_folder(sender, instance, **kwargs):
    if not instance.pk:
        return
    old_instance = Chunk.objects.get(pk=instance.pk)
    if str(instance.exercise) != str(old_instance.exercise):
        for assignment in Assignment.objects.all():
            assignment.rename_chunk_folder(instance)
