from django.db import models


class FrameQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
