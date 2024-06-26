from __future__ import annotations

import datetime
import shutil
import zipfile
from pathlib import Path

import django_rq
from django.conf import settings
from django.db import models

from access.models import Context, User
from exercises.models import Exercise

from . import jobs


class Assignment(models.Model):
    user = models.ForeignKey('access.User', on_delete=models.PROTECT, related_name='assignments')
    exercise = models.ForeignKey(
        'exercises.Exercise', on_delete=models.PROTECT, related_name='assignments'
    )
    passed = models.BooleanField(blank=True, null=True)
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
        unique_together = ['user', 'exercise']
        ordering = ['created_at']

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

    def test(self) -> None:
        self.passed = None
        self.save()
        django_rq.enqueue(jobs.test_assignment, self)

    def __str__(self):
        return f'{self.user} at {self.exercise}'

    def save(self, *args, **kwargs):
        if self.frame is None:
            self.frame = Frame.get_active_frame(self.user.context)
        super().save(*args, **kwargs)

    @classmethod
    def log(cls, user: User, verbose: bool = False) -> list[dict]:
        logdata = []
        for frame in Frame.get_frames(user.context):
            frame_assignments = cls.objects.filter(user=user, frame=frame)
            info = dict(
                name=frame.bucket.name,
                uploaded=frame_assignments.count(),
                passed=frame_assignments.filter(passed=True).count(),
                failed=frame_assignments.filter(passed=False).count(),
                waiting=frame_assignments.filter(passed__isnull=True).count(),
                available=frame.num_available_exercises,
            )
            if verbose:
                info['assignments'] = list(user.assignments.values('exercise__slug', 'passed'))
            logdata.append(info)
        return logdata


class Frame(models.Model):
    context = models.ForeignKey('access.Context', on_delete=models.CASCADE, related_name='frames')
    bucket = models.ForeignKey(
        'assignments.Bucket', on_delete=models.CASCADE, related_name='frames'
    )
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f'{self.context} ({self.bucket})'

    @property
    def num_exercises(self) -> int:
        return self.packs.count()

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


class Pack(models.Model):
    frame = models.ForeignKey('assignments.Frame', on_delete=models.PROTECT, related_name='packs')
    exercise = models.ForeignKey(
        'exercises.Exercise', on_delete=models.PROTECT, related_name='packs'
    )
    uploadable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.frame} - {self.exercise}'

    class Meta:
        unique_together = ('frame', 'exercise')
