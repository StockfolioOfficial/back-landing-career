from django.db.models.query import QuerySet
from rest_framework import serializers

from recruits.models import Recruit
        
class RecruitSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Recruit
        fields = ['position', 'description', 'created_at', 'updated_at', 'stacks']
