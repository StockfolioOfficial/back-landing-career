from django.db import models

from core.models import TimeStampModel, SoftDeleteModel

class Application(TimeStampModel):
    content = models.JSONField(null=False)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'applications'

class Attachment(models.Model):
    file_url    = models.URLField()
    application = models.ForeignKey('Application', on_delete=models.CASCADE)

    class Meta:
        db_table = 'attachments'