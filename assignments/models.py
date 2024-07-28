from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

import django_rq
import toml
from django.conf import settings
from django.db import models

from access.models import User
from frames.models import Frame

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

    @property
    def frame(self):
        return self.user.context.get_chunk(self.exercise).frame

    @property
    def context_folder(self) -> Path:
        return settings.ASSIGNMENT_UPLOADS_PATH / self.frame.context.slug

    @property
    def bucket_folder(self) -> Path:
        return self.context_folder / self.frame.bucket.slug

    @property
    def exercise_folder(self) -> Path:
        return self.bucket_folder / self.exercise.slug

    @property
    def user_folder(self) -> Path:
        return self.exercise_folder / self.user.slug

    @property
    def folder(self) -> Path:
        return self.context_folder / self.bucket_folder / self.exercise_folder / self.user_folder

    @property
    def config_path(self) -> Path:
        return self.folder / settings.EXERCISE_CONFIG_FILE

    @property
    def config(self) -> dict:
        if not getattr(self, '_cfg', None) or not self._cfg:  # type: ignore
            self._cfg = self.load_config()
        return self._cfg

    def load_config(self) -> dict:
        with open(self.config_path) as f:
            return toml.load(f)

    def dump_config(self) -> None:
        with open(self.config_path, 'w') as f:
            toml.dump(self.config, f)

    def rename_context_folder(self, context) -> None:
        if self.frame.context == context:
            if (p := self.context_folder).exists():
                p.rename(p.parent / context.slug)

    def rename_bucket_folder(self, bucket) -> None:
        if self.frame.bucket == bucket:
            if (p := self.bucket_folder).exists():
                p.rename(p.parent / bucket.slug)

    def rename_exercise_folder(self, exercise) -> None:
        if self.exercise == exercise:
            if (p := self.exercise_folder).exists():
                self.config['slug'] = exercise.slug
                self.dump_config()
                p.rename(p.parent / exercise.slug)

    def rename_user_folder(self, user) -> None:
        if self.user == user:
            if (p := self.user_folder).exists():
                p.rename(p.parent / user.slug)

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

    @classmethod
    def log(cls, user: User, frame_ref: str, verbose: bool = False) -> list[dict]:
        logdata = []
        if frame_ref:
            frames = Frame.objects.filter(context=user.context).byref(frame_ref).active()
        else:
            frames = user.context.frames.active()
        for frame in frames:
            frame_assignments = cls.objects.filter(user=user, exercise__in=frame.exercises)
            info = dict(
                name=frame.name,
                uploaded=frame_assignments.count(),
                passed=frame_assignments.filter(passed=True).count(),
                failed=frame_assignments.filter(passed=False).count(),
                waiting=frame_assignments.filter(passed__isnull=True).count(),
                available=frame.exercises.count(),
            )
            if verbose:
                info['assignments'] = list(frame_assignments.values('exercise__slug', 'passed'))
            logdata.append(info)
        return logdata
