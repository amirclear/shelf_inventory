"""
ASGI config for inventory_mvp project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_mvp.settings')

application = get_asgi_application()

