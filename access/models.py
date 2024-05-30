import uuid
from pathlib import Path

from django.conf import settings
from django.db import models

from exercises.models import Exercise


class User(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    token = models.SlugField(unique=True, default=uuid.uuid4)
    context = models.ForeignKey('access.Context', on_delete=models.PROTECT, related_name='users')

    class Meta:
        unique_together = ('name', 'context')

    def __str__(self):
        return self.name

    def get_exercise_folder(self, exercise: Exercise) -> Path:
        return self.context.folder / f'{exercise.slug}/{self.slug}/'


class Context(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)

    @property
    def folder(self):
        return settings.EXERCISE_UPLOAD_PATH / self.slug

    def __str__(self):
        return self.name
