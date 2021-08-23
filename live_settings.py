import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    },
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
    }
}

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALGORITHM = os.environ['JWT_ALG']

ADMIN_TOKEN = os.environ['JWT_SECRET']

SENDGRID_API_KEY = os.environ['SG_API_KEY']

EMAIL_DOMAIN = os.environ['EMAIL_SENDER']