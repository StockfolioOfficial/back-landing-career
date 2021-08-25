import os

IS_DEBUG = os.getenv("IS_PRODUCTION", "False") not in ["True", "true"]

if IS_DEBUG:
    import my_settings as settings
else:
    import live_settings as settings


DATABASES = settings.DATABASES

SECRET_KEY = settings.SECRET_KEY

ALGORITHM = settings.ALGORITHM

ADMIN_TOKEN = settings.ADMIN_TOKEN

SENDGRID_API_KEY = settings.SENDGRID_API_KEY

EMAIL_DOMAIN = settings.EMAIL_DOMAIN

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
