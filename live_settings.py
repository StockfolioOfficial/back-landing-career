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

ALGORITHM = os.environ['JWT_ALG']

SECRET_KEY = os.environ["JWT_SECRET"]

# dummy token
ADMIN_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' \
              '.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ' \
              '.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c '

SENDGRID_API_KEY = os.environ['SG_API_KEY']

EMAIL_DOMAIN = os.environ['EMAIL_SENDER']

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

BUCKET_NAME = 'stockers-bucket'