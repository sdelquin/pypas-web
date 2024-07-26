from __future__ import annotations

from django.db import models
from django.utils import timezone

from exercises.models import Exercise

from .querysets import FrameQuerySet


class Frame(models.Model):
    context = models.ForeignKey('access.Context', on_delete=models.CASCADE, related_name='frames')
    bucket = models.ForeignKey('frames.Bucket', on_delete=models.CASCADE, related_name='frames')
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    # MANAGERS
    objects = FrameQuerySet.as_manager()

    class Meta:
        ordering = ['context', 'start']

    def __str__(self):
        return f'{self.context} ({self.bucket})'

    @property
    def name(self):
        return self.bucket.name

    @property
    def num_exercises(self) -> int:
        return self.chunks.count()

    @property
    def is_active(self) -> bool:
        now = timezone.now()
        if self.start is None:
            if self.end is None:
                return True
            return self.end >= now
        if self.end is None:
            if self.start is None:
                return True
            return self.start <= now
        return self.start <= now <= self.end

    @property
    def exercises(self):
        return Exercise.objects.filter(pk__in=self.chunks.values('exercise'))


class Bucket(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name
