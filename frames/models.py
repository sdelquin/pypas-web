from __future__ import annotations

from django.db import models


class Frame(models.Model):
    context = models.ForeignKey('access.Context', on_delete=models.CASCADE, related_name='frames')
    bucket = models.ForeignKey('frames.Bucket', on_delete=models.CASCADE, related_name='frames')
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    exercises = models.ManyToManyField('exercises.Exercise', related_name='frames')

    def __str__(self):
        return f'{self.context} ({self.bucket})'

    @property
    def num_exercises(self) -> int:
        return self.chunks.count()

    class Meta:
        ordering = ['context', 'start']


class Bucket(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name
