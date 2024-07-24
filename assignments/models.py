from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

import django_rq
from django.conf import settings
from django.db import models

from . import jobs


class Assignment(models.Model):
    user = models.ForeignKey('access.User', on_delete=models.PROTECT, related_name='assignments')
    exercise = models.ForeignKey(
        'exercises.Exercise', on_delete=models.PROTECT, related_name='assignments'
    )
    passed = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'exercise']
        ordering = ['created_at']

    # @property
    # def frame(self):
    #     frames1 = self.user.context.frames
    #     frames2 = self.exercise.frames

    @property
    def folder(self) -> Path:
        return (
            settings.ASSIGNMENT_UPLOADS_PATH
            / self.frame.context.slug
            # / self.frame.bucket.slug
            / self.exercise.slug
            / self.user.slug
        )

    def remove_folder(self) -> None:
        shutil.rmtree(self.folder, ignore_errors=True)
        folder = self.folder.parent
        while folder != settings.ASSIGNMENT_UPLOADS_PATH:
            if not list(folder.glob('*')):  # folder is empty!
                shutil.rmtree(folder, ignore_errors=True)
                folder = folder.parent
            else:
                break

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

    # def save(self, *args, **kwargs):
    #     if self.frame is None: # TODO
    #         self.frame = Frame.get_active_frame(self.user.context)
    #     super().save(*args, **kwargs)

    # @classmethod
    # def log(cls, user: User, verbose: bool = False) -> list[dict]:
    #     logdata = []
    #     for frame in Frame.get_frames(user.context):
    #         frame_assignments = cls.objects.filter(user=user, frame=frame, exercise__available=True)
    #         info = dict(
    #             name=frame.bucket.name,
    #             uploaded=frame_assignments.count(),
    #             passed=frame_assignments.filter(passed=True).count(),
    #             failed=frame_assignments.filter(passed=False).count(),
    #             waiting=frame_assignments.filter(passed__isnull=True).count(),
    #             available=frame.num_available_exercises, #TODO
    #         )
    #         if verbose:
    #             info['assignments'] = list(frame_assignments.values('exercise__slug', 'passed'))
    #         logdata.append(info)
    #     return logdata
