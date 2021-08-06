from rest_framework import serializers

from users.models import User

<<<<<<< HEAD
=======
class SignupBodySerializer(serializers.Serializer):
    email          = serializers.EmailField()
    password       = serializers.CharField()
    password_check = serializers.CharField()

class SigninBodySerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField()

>>>>>>> edbd58c ( - #10 Add(Signin): 로그인 EndPoint, API 구현)
class MyPageGetSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['email', 'created_at', 'updated_at']

class MyPagePatchBodySerializer(serializers.Serializer):
    new_password       = serializers.CharField()
    new_password_check = serializers.CharField()