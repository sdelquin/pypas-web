from django.conf import settings
from django.db import models


class Exercise(models.Model):
    slug = models.SlugField(max_length=128, unique=True)
    available = models.BooleanField(default=True)

    @property
    def path(self):
        return settings.REPOSITORY_PATH / self.slug

    def __str__(self):
        return self.slug
