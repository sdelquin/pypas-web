from django.apps import AppConfig


class ExercisesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exercises'

    def ready(self):
        from . import signals  # noqa
