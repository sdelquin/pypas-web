import glob
import io
import zipfile
from pathlib import Path
from typing import Iterator

import tomllib
from django.conf import settings
from django.db import models


class Exercise(models.Model):
    slug = models.SlugField(max_length=128, unique=True)
    available = models.BooleanField(default=True)

    @property
    def path(self) -> Path:
        return settings.REPOSITORY_PATH / self.slug

    @property
    def config(self) -> dict:
        if not getattr(self, '_cfg', None) or not self._cfg:  # type: ignore
            with open(self.path / settings.EXERCISE_CONFIG_FILE, 'rb') as f:
                self._cfg = tomllib.load(f)
        return self._cfg

    @property
    def bundle(self) -> Iterator[str]:
        for b in self.config['bundle'] + [settings.EXERCISE_CONFIG_FILE]:
            globs = glob.glob(b, root_dir=self.path)
            for g in globs:
                yield g

    @property
    def zipname(self) -> str:
        return f'{self.slug}.zip'

    def build_full_path(self, relative_path: str) -> Path:
        return self.path / relative_path

    def zip(self) -> io.BytesIO:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            for f in self.bundle:
                archive.write(self.build_full_path(f), f'{self.slug}/{f}')
        buffer.seek(0)
        return buffer

    def __str__(self):
        return self.slug
