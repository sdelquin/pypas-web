from django.apps import AppConfig


class ChunksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chunks'

    def ready(self):
        from . import signals  # noqa
