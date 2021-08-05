from rest_framework import serializers

from users.models import User

class SignupBodySerializer(serializers.Serializer):
    email          = serializers.EmailField()
    password       = serializers.CharField()
    password_check = serializers.CharField()

class MyPageGetSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['email', 'created_at', 'updated_at']

class MyPagePatchBodySerializer(serializers.Serializer):
    new_password       = serializers.CharField()
    new_password_check = serializers.CharField()