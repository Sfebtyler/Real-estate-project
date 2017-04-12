import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      '{{ project_name }}.settings.dev')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# log and raise an exception if email settings aren't configured in production
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
if not settings.DEBUG and not settings.EMAIL_HOST:
    import logging
    logger = logging.getLogger('wsgi')
    logger.critical('Email settings appear to be invalid. Please check them!')
    raise ImproperlyConfigured('settings.EMAIL_HOST not set!')
