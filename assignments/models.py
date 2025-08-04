from __future__ import annotations

import shutil
import tempfile
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
    chunk = models.ForeignKey('chunks.Chunk', on_delete=models.PROTECT, related_name='assignments')
    passed = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        unique_together = ['user', 'chunk']

    @property
    def context_folder(self) -> Path:
        return settings.ASSIGNMENT_UPLOADS_PATH / self.user.context.slug

    @property
    def bucket_folder(self) -> Path:
        return self.context_folder / self.chunk.frame.bucket.slug

    @property
    def exercise_folder(self) -> Path:
        return self.bucket_folder / self.chunk.exercise.slug

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

    @property
    def zipname(self) -> str:
        return f'{self.chunk.exercise.slug}.zip'

    @property
    def zippath(self) -> Path:
        return self.folder / self.zipname

    def load_config(self) -> dict:
        with open(self.config_path) as f:
            return toml.load(f)

    def dump_config(self) -> None:
        with open(self.config_path, 'w') as f:
            toml.dump(self.config, f)

    def rename_context_folder(self, new_context, *, force=False) -> None:
        if self.chunk.frame.context == new_context or force:
            if (p := self.context_folder).exists():
                p.rename(p.parent / new_context.slug)

    def rename_bucket_folder(self, new_bucket, *, force=False) -> None:
        if self.chunk.frame.bucket == new_bucket or force:
            if (p := self.bucket_folder).exists():
                p.rename(p.parent / new_bucket.slug)

    def rename_exercise_folder(self, new_exercise, *, force=False) -> None:
        if self.chunk.exercise == new_exercise or force:
            if (p := self.exercise_folder).exists():
                self.config['slug'] = new_exercise.slug
                self.dump_config()
                p.rename(p.parent / new_exercise.slug)

    def rename_user_folder(self, new_user, *, force=False) -> None:
        if self.user == new_user or force:
            if (p := self.user_folder).exists():
                p.rename(p.parent / new_user.slug)

    def rename_chunk_folder(self, chunk) -> None:
        if self.chunk == chunk:
            self.rename_exercise_folder(chunk.exercise, force=True)
            self.rename_bucket_folder(chunk.frame.bucket, force=True)
            self.rename_context_folder(chunk.frame.context, force=True)

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

    def copy(self, file) -> None:
        self.folder.parent.mkdir(parents=True, exist_ok=True)
        with open(self.zippath, 'wb') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

    def test(self) -> None:
        self.passed = None
        self.save()
        django_rq.enqueue(jobs.test_assignment, self)

    def dump_test(self) -> None:
        passed = Path(self.folder / settings.PASSED_PLACEHOLDER_FILENAME)
        failed = Path(self.folder / settings.FAILED_PLACEHOLDER_FILENAME)
        if self.passed:
            failed.unlink(missing_ok=True)
            passed.touch()
        else:
            passed.unlink(missing_ok=True)
            failed.touch()

    def __str__(self):
        return f'{self.user} at {self.chunk.exercise}'

    @classmethod
    def log(cls, user: User, frame_ref: str, verbose: bool = False) -> list[dict]:
        logdata = []
        if frame_ref:
            frames = Frame.objects.filter(context=user.context).byref(frame_ref).active()
        else:
            frames = user.context.frames.active()
        for frame in frames:
            user_frame_assignments = cls.objects.filter(user=user, chunk__in=frame.chunks.all())
            info = dict(
                name=str(frame),
                slug=frame.bucket.slug,
                uploaded=user_frame_assignments.count(),
                passed=user_frame_assignments.filter(passed=True).count(),
                failed=user_frame_assignments.filter(passed=False).count(),
                waiting=user_frame_assignments.filter(passed__isnull=True).count(),
                available=frame.chunks.count(),
            )
            if verbose:
                assignments = []
                for chunk in frame.chunks.all():
                    try:
                        assignment = user_frame_assignments.get(chunk=chunk)
                        passed = assignment.passed
                    except cls.DoesNotExist:
                        passed = None
                    assignments.append(dict(slug=chunk.exercise.slug, passed=passed))
                info['assignments'] = assignments
            logdata.append(info)
        return logdata

    @classmethod
    def zip_frame_assignments_for_user(cls, frame: Frame, user: User) -> Path:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            for assignment in user.assignments.filter(chunk__frame=frame):
                dst_folder = tmp_path / assignment.chunk.exercise.slug
                with zipfile.ZipFile(assignment.zippath) as archive:
                    archive.extractall(dst_folder)
            output_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
            output_zip_path = Path(output_zip.name)
            with zipfile.ZipFile(output_zip_path, 'w') as archive:
                for file in tmp_path.rglob('*'):
                    arcname = file.relative_to(tmp_path)
                    archive.write(file, arcname)
        return output_zip_path
