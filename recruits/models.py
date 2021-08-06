from django.db import models

from core.models import TimeStampModel

class Recruit(TimeStampModel):
    TYPE_CHOICES = (
        ('N', '신입'),
        ('C', '경력'),
        ('NC', '신입/경력'),
    )

    position     = models.CharField(max_length=50, null=False)
    description  = models.TextField()
    stacks       = models.ManyToManyField('Stack', through='RecruitStack', related_name='recruits')
    applications = models.ManyToManyField('applications.Application', through='RecruitApplication', related_name='recruits')
    type         = models.CharField(max_length=3, choices=TYPE_CHOICES, default='NC')
    deadline     = models.DateField(null=True, blank=True)
    
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