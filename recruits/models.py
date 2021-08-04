from django.db import models

from core.models import TimeStampModel

class Recruit(TimeStampModel):
    position     = models.CharField(max_length=50, null=False)
    description  = models.TextField()
    stacks       = models.ManyToManyField('Stack', through='RecruitStack', related_name='recruits')
    applications = models.ManyToManyField('applications.Application', through='RecruitApplication', related_name='recruits')
    
    class Meta:
        db_table = 'recruits'

class Stack(models.Model):
    name    = models.CharField(max_length=256, null=False)
    hash_id = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'stacks'

class RecruitStack(models.Model):
    recruit = models.ForeignKey('Recruit', on_delete=models.CASCADE)
    stack   = models.ForeignKey('Stack', on_delete=models.CASCADE)

    class Meta:
        db_table = 'recruits_stacks'

class RecruitApplication(models.Model):
    recruit     = models.ForeignKey('Recruit', on_delete=models.CASCADE)
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE)

    class Meta:
        db_table = 'recruits_applications'