from django.db.models.query import QuerySet
from rest_framework import serializers

from recruits.models import Recruit
        
class RecruitSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Recruit
        fields = ['position', 'description', 'created_at', 'updated_at', 
                  'stacks', 'career_type', 'work_type', 'author', 'job_openings','deadline', 'minimum_salary', 'maximum_salary']

class RecruitCreateBodySerializer(serializers.Serializer):
    position       = serializers.CharField()
    description    = serializers.CharField()
    stacks         = serializers.ListField()
    job_openings   = serializers.CharField()
    work_type      = serializers.CharField()
    career_type    = serializers.ChoiceField(choices=("신입", "경력", "신입/경력"), default="신입/경력")
    deadline       = serializers.DateField(default="9999-12-31")
    minimum_salary = serializers.DecimalField(max_digits=13, decimal_places=2, default=0)
    maximum_salary = serializers.DecimalField(max_digits=13, decimal_places=2, default=0)
    

class RecruitQuerySerializer(serializers.Serializer):
    position = serializers.CharField(allow_blank=True, allow_null=True, default="")
    sort     = serializers.CharField(allow_blank=True, allow_null=True, default="")