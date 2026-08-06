"""ASGI config for Mercadinho da Isis."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mercadinho.settings")

application = get_asgi_application()
