import glob
import io
import zipfile
from pathlib import Path
from typing import Iterator

from django.conf import settings
from django.db import models


class Exercise(models.Model):
    slug = models.SlugField(max_length=128, unique=True)
    available = models.BooleanField(default=True)

    @property
    def path(self) -> Path:
        return settings.REPOSITORY_PATH / self.slug

    @property
    def bundle(self) -> Iterator[str]:
        f = open(self.path / '.bundle')
        for line in f:
            globs = glob.glob(line.strip(), root_dir=self.path)
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
