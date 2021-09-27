from django.db import models

from core.models import TimeStampModel

class Application(TimeStampModel):
    STATUS_CHOICES  = (
        ('ST1', '서류제출'),
        ('ST2', '1차면접'),
        ('ST3', '2차면접'),
        ('ST4', '합격'),
        ('ST5', '불합격'),
    )

    content = models.JSONField(null=False)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status  = models.CharField(max_length=3, choices=STATUS_CHOICES, default='ST1')

    class Meta:
        db_table = 'applications'

class Attachment(models.Model):
    file_url    = models.URLField()
    application = models.ForeignKey('Application', on_delete=models.CASCADE)

    class Meta:
        db_table = 'attachments'

class Comment(TimeStampModel):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    application = models.ForeignKey('Application', on_delete=models.CASCADE)
    score       = models.PositiveIntegerField(default=2)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'comments'

class ApplicationAccessLog(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    application = models.ForeignKey('Application', on_delete=models.CASCADE)
    log_at      = models.DateTimeField(auto_now_add=True)           
