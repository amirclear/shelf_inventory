"""
WSGI config for inventory_mvp project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_mvp.settings')

application = get_wsgi_application()

