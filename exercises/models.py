from __future__ import annotations

import glob
import io
import shutil
import zipfile
from pathlib import Path
from typing import Iterator

import toml
from django.conf import settings
from django.db import models

from frames.models import Frame

from .querysets import ExerciseQuerySet


class Exercise(models.Model):
    slug = models.SlugField(max_length=128, unique=True)
    topic = models.ForeignKey(
        'exercises.Topic', on_delete=models.PROTECT, related_name='exercises', blank=True, null=True
    )

    # MANAGERS
    objects = ExerciseQuerySet.as_manager()

    class Meta:
        ordering = ['topic', 'slug']

    @property
    def folder(self) -> Path:
        return settings.REPOSITORY_PATH / self.slug

    @property
    def config_path(self) -> Path:
        return self.folder / settings.EXERCISE_CONFIG_FILE

    @property
    def config(self) -> dict:
        if not getattr(self, '_cfg', None) or not self._cfg:  # type: ignore
            self._cfg = self.load_config()
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
        # pre-save signal implemented!
        super().save(*args, **kwargs)
        self.config['slug'] = self.slug
        self.dump_config()

    def load_config(self) -> dict:
        with open(self.config_path) as f:
            return toml.load(f)

    def dump_config(self) -> None:
        with open(self.config_path, 'w') as f:
            toml.dump(self.config, f)

    def remove_folder(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    @classmethod
    def list(cls, context, frame_ref: str, primary_topic: str, secondary_topic: str) -> list[dict]:
        listdata = []
        if frame_ref:
            frames = Frame.objects.filter(context=context).byref(frame_ref).active()
        else:
            frames = context.frames.active()
        topics = Topic.filter_by_levels(primary_topic, secondary_topic)
        for frame in frames:
            exercises = frame.exercises.filter(topic__in=topics)
            exercises_data = [dict(slug=e.slug, topic=str(e.topic)) for e in exercises]
            info = dict(name=frame.name, exercises=exercises_data)
            listdata.append(info)
        return listdata


class Topic(models.Model):
    primary = models.SlugField(max_length=128)
    secondary = models.SlugField(max_length=128)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('primary', 'secondary')
        ordering = ('order',)

    def __str__(self):
        return f'{self.primary}/{self.secondary}'

    @classmethod
    def filter_by_levels(cls, primary_topic: str, secondary_topic: str):
        if primary_topic and secondary_topic:
            return cls.objects.filter(primary=primary_topic, secondary=secondary_topic)
        if primary_topic and not secondary_topic:
            return cls.objects.filter(primary=primary_topic)
        if not primary_topic and secondary_topic:
            return cls.objects.filter(secondary=secondary_topic)
        return cls.objects.all()
