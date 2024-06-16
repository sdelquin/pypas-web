import glob
import io
import shutil
import zipfile
from pathlib import Path
from typing import Iterator

import toml
from django.conf import settings
from django.db import models


class Exercise(models.Model):
    slug = models.SlugField(max_length=128, unique=True)
    available = models.BooleanField(default=True)
    topic = models.ForeignKey(
        'exercises.Topic', on_delete=models.PROTECT, related_name='exercises', blank=True, null=True
    )

    @property
    def folder(self) -> Path:
        return settings.REPOSITORY_PATH / self.slug

    @property
    def config_path(self) -> Path:
        return self.folder / settings.EXERCISE_CONFIG_FILE

    @property
    def config(self) -> dict:
        if not getattr(self, '_cfg', None) or not self._cfg:  # type: ignore
            with open(self.config_path) as f:
                self._cfg = toml.load(f)
        return self._cfg

    @property
    def bundle(self) -> Iterator[str]:
        for b in self.config['bundle'] + [settings.EXERCISE_CONFIG_FILE]:
            globs = glob.glob(b, root_dir=self.folder)
            for g in globs:
                yield g

    @property
    def zipname(self) -> str:
        return f'{self.slug}.zip'

    def build_full_path(self, relative_path: str) -> Path:
        return self.folder / relative_path

    def zip(self) -> io.BytesIO:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            for f in self.bundle:
                archive.write(self.build_full_path(f), f)
        buffer.seek(0)
        return buffer

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.folder.exists():
            shutil.copytree(settings.EXERCISE_TEMPLATE_FOLDER, self.folder)
            self.config['slug'] = self.slug
            self.save_config()
        super().save(*args, **kwargs)

    def save_config(self):
        with open(self.config_path, 'w') as f:
            toml.dump(self.config, f)

    def remove_folder(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    @classmethod
    def get_num_exercises(cls):
        return cls.objects.count()


class Topic(models.Model):
    primary = models.SlugField(max_length=128)
    secondary = models.SlugField(max_length=128)

    class Meta:
        unique_together = ('primary', 'secondary')

    def __str__(self):
        return f'{self.primary}/{self.secondary}'
