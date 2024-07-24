from __future__ import annotations

import datetime

from django.db import models

from access.models import Context
from exercises.models import Exercise


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

    @property
    def num_available_exercises(self) -> int:
        return self.packs.filter(exercise__available=True).count()

    @classmethod
    def get_active_frame(cls, context: Context) -> Frame:
        today = datetime.date.today()
        return cls.objects.get(start__lte=today, end__gte=today, context=context)

    @classmethod
    def get_frames(cls, context: Context):
        return cls.objects.filter(context=context)

    def save(self, *args, **kwargs):
        if self.num_exercises is None:
            self.num_exercises = Exercise.get_num_exercises()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['context', 'start']


class Bucket(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name
