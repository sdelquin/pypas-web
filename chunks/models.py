from django.core.exceptions import ValidationError
from django.db import models


class Chunk(models.Model):
    frame = models.ForeignKey('frames.Frame', on_delete=models.PROTECT, related_name='chunks')
    exercise = models.ForeignKey(
        'exercises.Exercise', on_delete=models.PROTECT, related_name='chunks'
    )
    puttable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.frame} - {self.exercise}'

    class Meta:
        unique_together = ('frame', 'exercise')
        ordering = ('frame', 'exercise')

    @classmethod
    def get_frame(cls, context, exercise):
        return cls.objects.get(frame__context=context, exercise=exercise)

    def validate_unique(self, exclude=None) -> None:
        super().validate_unique(exclude=exclude)
        if (
            self.__class__.objects.filter(frame__context=self.frame.context, exercise=self.exercise)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                message=f'Chunk with context "{self.frame.context}" and exercise "{self.exercise}" already exists.'
            )
