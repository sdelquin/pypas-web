import uuid

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    token = models.UUIDField(unique=True, default=uuid.uuid4)
    context = models.ForeignKey('access.Context', on_delete=models.PROTECT, related_name='users')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'context')


class Context(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name
