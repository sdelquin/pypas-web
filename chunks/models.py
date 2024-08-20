from django.core.exceptions import ValidationError
from django.db import models

from frames.models import Frame


class Chunk(models.Model):
    frame = models.ForeignKey('frames.Frame', on_delete=models.PROTECT, related_name='chunks')
    exercise = models.ForeignKey(
        'exercises.Exercise', on_delete=models.PROTECT, related_name='chunks'
    )
    puttable = models.BooleanField(default=True)
    order = models.FloatField(default=0)
    hits = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ('frame', 'exercise')
        ordering = ('frame', 'order', 'exercise')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cached_order = self.order

    def __str__(self):
        return f'{self.frame} - {self.exercise}'

    def validate_unique(self, exclude=None) -> None:
        super().validate_unique(exclude=exclude)
        if (
            getattr(self, 'frame', False)
            and self.__class__.objects.filter(
                frame__context=self.frame.context, exercise=self.exercise
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                message=f'Chunk with context "{self.frame.context}" and exercise "{self.exercise}" already exists.'
            )

    @classmethod
    def get_frame(cls, context, exercise):
        return cls.objects.get(frame__context=context, exercise=exercise)

    @classmethod
    def fix_order(cls, within_frame: Frame) -> None:
        order = 1
        for chunk in cls.objects.filter(frame=within_frame):
            chunk.order = order
            chunk.save()
            order += 1
