from django.db import models


class Chunk(models.Model):
    frame = models.ForeignKey('frames.Frame', on_delete=models.PROTECT, related_name='chunks')
    exercise = models.ForeignKey(
        'exercises.Exercise', on_delete=models.PROTECT, related_name='chunks'
    )
    puttable = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.frame} - {self.exercise}'

    class Meta:
        unique_together = ('frame', 'exercise')
