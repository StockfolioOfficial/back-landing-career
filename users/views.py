import json, bcrypt, jwt

from django.http          import JsonResponse
from drf_yasg             import openapi
from drf_yasg.utils       import swagger_auto_schema
from rest_framework.views import APIView

from core.decorators   import login_required
from my_settings       import SECRET_KEY, ALGORITHM
from users.models      import User
from users.validation  import validate_email, validate_password
from users.serializers import SigninBodySerializer, SignupBodySerializer, MyPageGetSerializer, MyPagePatchBodySerializer

class SignupView(APIView):
    @swagger_auto_schema (
        request_body = SignupBodySerializer, 
        responses = {
            "201": "SUCCESS",
            "400": "BAD_REQUEST" 
        },
        operation_id = "회원가입",
        operation_description = "이메일(abc@def.com 등의 이메일 형식), 패스워드(영문, 숫자, 특수기호) validation이 적용되어 있습니다."
    )
    
    def post(self, request):
        try: 
            data = json.loads(request.body)

            if not validate_email(data['email']):
                return JsonResponse({'message': 'INVALID_EMAIL_FORMAT'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'ALREADY_EXISTED_EMAIL'}, status=400)           
            
            if not validate_password(data['password']):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'}, status=400)
            
            password       = data['password']
            password_check = data['password_check'] 
            
            if password != password_check:
                return JsonResponse({'message': 'BAD_REQUEST'}, status=400) 

            encoded_password = data['password'].encode('utf-8')
            hashed_password  = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            
            user = User.objects.create(
                email    = data['email'],
                password = hashed_password.decode('utf-8')
            )

            access_token = jwt.encode({'user_id': user.id, 'role': user.role}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SigninView(APIView):
    @swagger_auto_schema (
        request_body = SigninBodySerializer,
        response = {
            "200": "SUCCESS",
            "400": "BAD_REQUEST"
        },
        operation_id = "로그인",
        operation_description = "이메일과 비밀번호 입력이 필요합니다."
    )
    
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'NOT_EXISTED_EMAIL'}, status=400)

            user = User.objects.get(email=email)
            
            encoded_password = password.encode('utf-8')
            hashed_password  = user.password.encode('utf-8')

            if not bcrypt.checkpw(encoded_password, hashed_password):
                return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

            access_token = jwt.encode({'user_id': user.id, 'role': user.role}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class UserMyPageView(APIView):
    parameter_token = openapi.Parameter (
                                        "Authorization", 
                                        openapi.IN_HEADER, 
                                        description = "access_token", 
                                        type        = openapi.TYPE_STRING
    )

    mypage_get_response = openapi.Response("result", MyPageGetSerializer)

    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        responses = {
            "200": mypage_get_response,
            "400": "BAD_REQUEST",
            "401": "INVALID_TOKEN"
        },
        operation_id = "회원정보 조회",
        operation_description = "header에 토큰이 필요합니다."
    )
    @login_required
    def get(self, request):    
        user = request.user
        
        result = {
            "email"     : user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

        return JsonResponse({"result": result}, status=200)

    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        request_body      = MyPagePatchBodySerializer,
        responses = {
            "200": "SUCCESS",
            "400": "BAD_REQUEST",
            "401": "INVALID_TOKEN"
        },
        operation_id = "회원정보 수정",
        operation_description = "header에 토큰, body에 수정 값이 필요합니다."
    )
    @login_required
    def patch(self, request):
        user = request.user
        data = json.loads(request.body)

        new_password       = data["new_password"]
        new_password_check = data["new_password_check"]

        if not (new_password and new_password_check):
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        if not new_password == new_password_check:
            return JsonResponse({"message": "BAD_REQUEST"}, status=400)

        if not validate_password(new_password):
            return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

        encoded_new_password = new_password.encode('utf-8')
        hashed_new_password  = bcrypt.hashpw(encoded_new_password, bcrypt.gensalt()).decode('utf-8')

        user.password = hashed_new_password
        user.save()

        return JsonResponse({"message": "SUCCESS"}, status=200)
