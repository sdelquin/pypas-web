from django.db import models
from django.db.models import Q


class FrameQuerySet(models.QuerySet):
    def active(self):
        frames = [f.pk for f in self.all() if f.is_active]
        return self.filter(pk__in=frames)

    def byref(self, ref: str):
        return self.filter(Q(bucket__slug__iexact=ref) | Q(bucket__name__iexact=ref))
