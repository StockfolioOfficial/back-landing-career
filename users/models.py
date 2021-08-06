from django.db import models

from core.models import TimeStampModel, SoftDeleteModel

class User(TimeStampModel, SoftDeleteModel):
    email    = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=200, null=False)
    role     = models.CharField(max_length=15, default='common')

    class Meta:
        db_table = 'users'