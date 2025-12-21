from __future__ import annotations

import shutil
import zipfile
from pathlib import Path
from typing import Iterator, List

import pathspec
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
    objects = ExerciseQuerySet.as_manager()  # type: ignore

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
        spec = pathspec.PathSpec.from_lines('gitwildmatch', self.config['bundle'])
        yield from spec.match_tree(self.folder)
        yield settings.EXERCISE_CONFIG_FILE

    @property
    def zipname(self) -> str:
        return f'{self.slug}.zip'

    @property
    def zippath(self) -> Path:
        return self.folder / self.zipname

    @property
    def exercise_last_modification(self) -> float:
        return max(self.build_full_path(f).stat().st_mtime for f in self.bundle)

    @property
    def zip_last_modification(self) -> float:
        return self.zippath.stat().st_mtime

    def build_full_path(self, relative_path: str) -> Path:
        return self.folder / relative_path

    def zip(self) -> None:
        if (
            not self.zippath.exists()
            or self.exercise_last_modification > self.zip_last_modification
        ):
            with zipfile.ZipFile(self.zippath, 'w') as archive:
                for f in self.bundle:
                    archive.write(self.build_full_path(f), f)

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
    def list(cls, context, frame_ref: str, primary_topic: str, secondary_topic: str) -> List[dict]:
        listdata = []
        if frame_ref:
            frames = Frame.objects.filter(context=context).byref(frame_ref).active()
        else:
            frames = context.frames.active()
        topics = Topic.filter_by_levels(primary_topic, secondary_topic)
        for frame in frames:
            frame_chunks = frame.chunks.filter(exercise__topic__in=topics).order_by(
                'exercise__topic', 'order'
            )
            exercises_data = [
                dict(slug=c.exercise.slug, topic=str(c.exercise.topic)) for c in frame_chunks
            ]
            info = dict(name=str(frame), slug=frame.bucket.slug, exercises=exercises_data)
            listdata.append(info)
        return listdata

    @property
    def version(self) -> str:
        return str(self.config.get('version', settings.DEFAULT_EXERCISE_VERSION))


class Topic(models.Model):
    primary = models.SlugField(max_length=128)
    secondary = models.SlugField(max_length=128)
    order = models.PositiveIntegerField(default=0)

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
