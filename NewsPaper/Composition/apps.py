from django.apps import AppConfig


class CompositionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Composition'

    def ready(self):
        from . import signals


