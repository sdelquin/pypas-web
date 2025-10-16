from django.core.exceptions import ValidationError
from django.db import models

from frames.models import Frame


class Chunk(models.Model):
    frame = models.ForeignKey('frames.Frame', on_delete=models.PROTECT, related_name='chunks')
    exercise = models.ForeignKey(
        'exercises.Exercise', on_delete=models.PROTECT, related_name='chunks'
    )
    puttable = models.BooleanField(default=True)
    pass_to_put = models.BooleanField(
        default=False, help_text='If True, the exercise must pass the tests to be puttable.'
    )
    order = models.PositiveIntegerField(default=0)
    hits = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ('frame', 'exercise')
        ordering = ('order',)

    def __str__(self):
        return f'{self.frame} - {self.exercise}'

    @property
    def display(self):
        return f'{self.exercise}@{self.frame.bucket.slug}'

    def validate_unique(self, exclude=None) -> None:
        super().validate_unique(exclude=exclude)
        if (
            getattr(self, 'frame', False)
            and self.__class__.objects.filter(
                frame__context=self.frame.context, exercise__pk=self.exercise.pk
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
    def last_order(cls, within_frame: Frame) -> int:
        try:
            return cls.objects.aggregate(models.Max('order'))['order__max']
        except AttributeError:
            return 0
