# users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Nutricode'

    def ready(self):
        import Nutricode.signals  # Change 'users' to your app name
