import json, bcrypt, jwt, binascii, os, sendgrid

from django.utils         import timezone
from django.http          import JsonResponse
from drf_yasg             import openapi
from drf_yasg.utils       import swagger_auto_schema
from rest_framework.views import APIView

from sendgrid.helpers.mail import *

from core.decorators   import login_required
from my_settings       import SECRET_KEY, ALGORITHM, SENDGRID_API_KEY, EMAIL_DOMAIN
from users.models      import User, UserTemp
from users.validation  import validate_email, validate_password
from users.serializers import SigninBodySerializer, SignupBodySerializer, MyPageGetSerializer, MyPagePatchBodySerializer, VerificationSerializer, VerificationResponseSerializer, ChangePasswordSerializer

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
        responses = {
            "200": "SUCCESS",
            "400": "BAD_REQUEST"
        },
        operation_id = "로그인",
        operation_description = "이메일과 비밀번호 입력이 필요합니다."
    )
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        password = data['password']

        if not (validate_email(email) and validate_password(password)):
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)          

        user, is_created = User.objects.get_or_create(email= email)

        if is_created:
            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user.password    = hashed_password.decode('utf-8')
            user.save()

            access_token = jwt.encode({'user_id': user.id, 'role': user.role}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'access_token': access_token}, status=200)
        
        encoded_password = password.encode('utf-8')
        hashed_password  = user.password.encode('utf-8')

        if bcrypt.checkpw(encoded_password, hashed_password):
            access_token = jwt.encode({'user_id': user.id, 'role': user.role}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'access_token': access_token}, status=200)

        return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)            

class VerificationView(APIView):
    verification_response = openapi.Response("SUCCESS", VerificationResponseSerializer)

    @swagger_auto_schema (
        request_body = VerificationSerializer,
        responses = {
            "200": verification_response,
            "400": "BAD_REQUEST",
            "404": "NOT_FOUND"
        },
        operation_id = "비밀번호 찾기 위한 이메일 입력",
        operation_description = "유효한 이메일을 입력해주세요."
    )
    def post(self, request):
        try:
            data  = json.loads(request.body)
            email = data['email']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'NOT_FOUND'}, status=404)
            
            code = binascii.hexlify(os.urandom(4)).decode()

            UserTemp.objects.filter(email=email).delete()

            UserTemp.objects.create(
                email      = email,
                code       = code,
                expired_at = timezone.now() + timezone.timedelta(minutes=10)
            )

            sg   = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
            data = {
                "personalizations": [
                    {
                        "to": [{"email": "grondin@naver.com"}], # => "email": email
                        "subject": "인증 코드를 확인해 주세요."
                    }
                ],
                "from": {"email": f"noreply@{EMAIL_DOMAIN}"},
                "content": [
                    {
                        "type" : "text/plain",
                        "value": f"인증 코드: {code}"
                    }
                ]
            }
            sg.client.mail.send.post(request_body=data)

            return JsonResponse({'email': email, 'code': code}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    @swagger_auto_schema (
        request_body = ChangePasswordSerializer,
        responses = {
            "200": "SUCCESS",
            "400": "BAD_REQUEST",
            "404": "NOT_FOUND"
        },
        operation_id = "비밀번호 변경",
        operation_description = "이메일, 인증코드, 새로운 비밀번호를 입력하세요."
    )
    def patch(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            code         = data['code']
            new_password = data['new_password']

            user_temp = UserTemp.objects.get(email=email)
            
            if user_temp.code != code:
                return JsonResponse({'message': 'INVALID_CODE'}, status=400)
            if user_temp.expired_at < timezone.now():
                return JsonResponse({'message': 'EXPIRED_CODE'}, status=401)
            if not validate_password(new_password):
                return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

            hashed_password  = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            user          = User.objects.get(email=email)
            user.password = hashed_password.decode('utf-8')
            user.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message': 'NOT_FOUND'}, status=404)
        except UserTemp.DoesNotExist:
            return JsonResponse({'message': 'NOT_FOUND'}, status=404)
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
