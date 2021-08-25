"""
WSGI config for stockers project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application
from stockers.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockers.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=BASE_DIR)
application.add_files(os.path.join(BASE_DIR, 'static/'), prefix='')
