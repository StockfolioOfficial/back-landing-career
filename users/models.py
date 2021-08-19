from django.db import models

from core.models import TimeStampModel, SoftDeleteModel

class User(TimeStampModel, SoftDeleteModel):
    email    = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=200, null=False)
    role     = models.CharField(max_length=15, default='common')

    class Meta:
        db_table = 'users'

class UserTemp(models.Model):
    email      = models.EmailField()
    code       = models.CharField(max_length=10)
    expired_at = models.DateTimeField()

    class Meta:
        db_table = 'usertemps'