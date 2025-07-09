from django.apps import AppConfig


class GuardiansConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guardians'

    def ready(self):
        import guardians.signals
