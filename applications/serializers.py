from rest_framework import serializers

class ApplicationSerializer(serializers.Serializer):
    content = serializers.JSONField()