from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from assignments.models import Assignment
from shared.utils import DisabledSignal

from .models import Chunk


@receiver(pre_save, sender=Chunk)
def rename_assignment_folder(sender, instance, **kwargs):
    for assignment in Assignment.objects.all():
        assignment.rename_chunk_folder(instance)


@receiver(post_save, sender=Chunk)
def fix_order_within_frame_post_save(sender, instance, **kwargs):
    if instance.order != instance.cached_order or instance.order == 0:
        with DisabledSignal(post_save, fix_order_within_frame_post_save, Chunk):
            if instance.order == 0:
                instance.order = Chunk.objects.filter(frame=instance.frame).last().order + 1
                instance.save()
            else:
                Chunk.fix_order(within_frame=instance.frame)


@receiver(post_delete, sender=Chunk)
def fix_order_within_frame_post_delete(sender, instance, **kwargs):
    with DisabledSignal(post_save, fix_order_within_frame_post_save, Chunk):
        Chunk.fix_order(within_frame=instance.frame)
