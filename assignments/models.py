from __future__ import annotations

import datetime
import shlex
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest
from django.conf import settings
from django.db import models

from access.models import Context


class Assignment(models.Model):
    user = models.ForeignKey('access.User', on_delete=models.PROTECT, related_name='assignments')
    exercise = models.ForeignKey(
        'exercises.Exercise', on_delete=models.PROTECT, related_name='assignments'
    )
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    frame = models.ForeignKey(
        'assignments.Frame',
        on_delete=models.PROTECT,
        related_name='assignments',
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('user', 'exercise')

    @property
    def folder(self) -> Path:
        return (
            settings.ASSIGNMENT_UPLOADS_PATH
            / self.frame.context.slug
            / self.frame.bucket.slug
            / self.exercise.slug
            / self.user.slug
        )

    def remove_folder(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def unzip(self, file: Path) -> None:
        self.folder.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(file) as zip_ref:
            zip_ref.extractall(self.folder)

    def test(self) -> bool:
        ret = subprocess.run(shlex.split(settings.PYTEST_CMD), cwd=self.folder)
        return ret.returncode == pytest.ExitCode.OK

    def __str__(self):
        return f'{self.user} at {self.exercise}'

    def save(self, *args, **kwargs):
        if self.frame is None:
            self.frame = Frame.get_active_frame(self.user.context)
        super().save(*args, **kwargs)


class Frame(models.Model):
    context = models.ForeignKey('access.Context', on_delete=models.CASCADE, related_name='frames')
    bucket = models.ForeignKey(
        'assignments.Bucket', on_delete=models.CASCADE, related_name='frames'
    )
    start = models.DateField()
    end = models.DateField()
    num_exercises = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.context} ({self.bucket})'

    @classmethod
    def get_active_frame(cls, context: Context) -> Frame:
        today = datetime.date.today()
        return cls.objects.get(start__lte=today, end__gte=today, context=context)


class Bucket(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name
