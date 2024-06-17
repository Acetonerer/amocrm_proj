"""
ASGI config for amocrm_proj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

import dotenv
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amocrm_proj.settings')

application = get_asgi_application()
