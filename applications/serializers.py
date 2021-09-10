from rest_framework import serializers

from applications.models import Application

class ApplicationSerializer(serializers.Serializer):
    content   = serializers.JSONField()
    portfolio = serializers.FileField()

class ApplicationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Application
        fields = ['content', 'user', 'status', 'created_at', 'updated_at', 'recruits']

class ApplicationAdminPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Application
        fields = ['status']

class CommentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment