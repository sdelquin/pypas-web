import uuid

from django.conf import settings
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    token = models.SlugField(unique=True, default=uuid.uuid4)
    context = models.ForeignKey('access.Context', on_delete=models.PROTECT, related_name='users')

    class Meta:
        unique_together = ('name', 'context')

    def __str__(self):
        return f'{self.name} ({self.context})'

    @property
    def alias(self) -> str:
        return f'{self.slug}@{self.context.slug}'

    @property
    def num_uploaded_exercises(self) -> int:
        return self.assignments.all().count()

    @property
    def num_passed_exercises(self) -> int:
        return self.assignments.filter(passed=True).count()


class Context(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)

    @property
    def folder(self):
        return settings.EXERCISE_UPLOAD_PATH / self.slug

    def __str__(self):
        return self.name
