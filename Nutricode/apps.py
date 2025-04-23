from django.apps import AppConfig

class NutricodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Nutricode'

    def ready(self):
        try:
            import Nutricode.signals  # Import signals only if you have a signals.py file
        except ImportError:
            pass  # If signals.py is not needed, this avoids an error
