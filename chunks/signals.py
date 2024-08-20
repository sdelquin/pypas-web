from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from assignments.models import Assignment

from .models import Chunk


@receiver(pre_save, sender=Chunk)
def rename_assignment_folder(sender, instance, **kwargs):
    for assignment in Assignment.objects.all():
        assignment.rename_chunk_folder(instance)


@receiver(post_save, sender=Chunk)
def fix_order_within_frame_post_save(sender, instance, **kwargs):
    if instance.order != instance.cached_order or instance.order == 0:
        post_save.disconnect(fix_order_within_frame_post_save, sender=Chunk)
        try:
            if instance.order == 0:
                instance.order = Chunk.objects.filter(frame=instance.frame).last().order + 1
                instance.save()
            else:
                Chunk.fix_order(within_frame=instance.frame)
        except Exception as err:
            raise err
        finally:
            post_save.connect(fix_order_within_frame_post_save, sender=Chunk)


@receiver(post_delete, sender=Chunk)
def fix_order_within_frame_post_delete(sender, instance, **kwargs):
    post_save.disconnect(fix_order_within_frame_post_save, sender=Chunk)
    try:
        Chunk.fix_order(within_frame=instance.frame)
    except Exception as err:
        raise err
    finally:
        post_save.connect(fix_order_within_frame_post_save, sender=Chunk)
