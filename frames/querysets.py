from django.db import models


class FrameQuerySet(models.QuerySet):
    def active(self):
        frames = [f.pk for f in self.all() if f.is_active]
        return self.filter(pk__in=frames)
