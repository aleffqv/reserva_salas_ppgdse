from django.apps import AppConfig
from django.db.models.signals import post_migrate
import os


class SalasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'salas'

    def ready(self):
        post_migrate.connect(create_superuser, sender=self)


def create_superuser(sender, **kwargs):
    if os.environ.get("CREATE_SUPERUSER") != "1":
        return

    from django.contrib.auth import get_user_model

    User = get_user_model()

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

    if not username or not password:
        return

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
