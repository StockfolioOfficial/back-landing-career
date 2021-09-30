from django.db.models.query import QuerySet
from rest_framework import serializers

from recruits.models import Recruit
        
class RecruitSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Recruit
        fields = ['position', 'position_title', 'description', 'created_at', 'updated_at', 
                  'stacks', 'career_type', 'work_type', 'author','deadline']

class RecruitCreateBodySerializer(serializers.Serializer):
    position       = serializers.CharField()
    position_title = serializers.CharField()
    description    = serializers.CharField()
    work_type      = serializers.CharField()
    career_type    = serializers.ChoiceField(choices=("신입", "경력", "신입/경력"), default="신입/경력")
    deadline       = serializers.DateField(default="9999-12-31")

class RecruitQuerySerializer(serializers.Serializer):
    position_title = serializers.CharField(allow_blank=True, allow_null=True, default="")
    sort           = serializers.CharField(allow_blank=True, allow_null=True, default="")