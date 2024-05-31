import shlex
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest
from django.conf import settings
from django.db import models


class Assignment(models.Model):
    user = models.ForeignKey('access.User', on_delete=models.PROTECT, related_name='assignments')
    exercise = models.ForeignKey(
        'exercises.Exercise', on_delete=models.PROTECT, related_name='assignments'
    )
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'exercise')

    @property
    def folder(self) -> Path:
        return self.user.context.folder / f'{self.exercise.slug}/{self.user.slug}/'

    def put(self, file: Path) -> None:
        shutil.rmtree(self.folder, ignore_errors=True)
        self.folder.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(file) as zip_ref:
            zip_ref.extractall(self.folder)

    def test(self) -> bool:
        ret = subprocess.run(shlex.split(settings.PYTEST_CMD), cwd=self.folder)
        return ret.returncode == pytest.ExitCode.OK

    def __str__(self):
        return f'{self.user} at {self.exercise}'
