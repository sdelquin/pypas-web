import uuid

from django.db import models

from chunks.models import Chunk
from exercises.models import Exercise


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

    def __str__(self):
        return self.name

    def get_active_exercises(self):
        return Exercise.objects.filter(
            pk__in=Chunk.objects.filter(frame__in=self.frames.active()).values('exercise')
        )

    def get_chunk(self, exercise: Exercise) -> Chunk | None:
        try:
            return Chunk.objects.filter(frame__in=self.frames.all()).get(exercise=exercise)
        except Chunk.DoesNotExist:
            return None
