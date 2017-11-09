"""
WSGI config for ds project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('e:/WebProjects/ds.com/ds/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ds.settings")

application = get_wsgi_application()
