"""
WSGI config for MyWeb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyWeb.settings')

# Run migrations on startup
try:
    from migrate import run_migrations
    run_migrations()
except Exception as e:
    print(f"Error running migrations: {e}", file=sys.stderr)

application = get_wsgi_application()
