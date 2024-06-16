from django.db import models


class ExerciseQuerySet(models.QuerySet):
    def available(self):
        return self.filter(available=True)
