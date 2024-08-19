from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from assignments.models import Assignment

from .models import Chunk


@receiver(pre_save, sender=Chunk)
def rename_assignment_folder(sender, instance, **kwargs):
    for assignment in Assignment.objects.all():
        assignment.rename_chunk_folder(instance)


@receiver(post_save, sender=Chunk)
def fix_order_within_frame(sender, instance, **kwargs):
    post_save.disconnect(fix_order_within_frame, sender=Chunk)
    try:
        if instance.order == 0:
            instance.order = Chunk.objects.filter(frame=instance.frame).count()
            instance.save()
        else:
            order = 1
            for chunk in Chunk.objects.filter(frame=instance.frame):
                chunk.order = order
                chunk.save()
                order += 1
    except Exception as err:
        raise err
    finally:
        post_save.connect(fix_order_within_frame, sender=Chunk)
