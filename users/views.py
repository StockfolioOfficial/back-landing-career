import json, bcrypt

from django.http  import JsonResponse

from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg       import openapi

from core.decorators   import login_required
from users.validation  import validate_password
from users.serializers import MyPageGetSerializer, MyPagePatchBodySerializer

class UserMyPageView(APIView):
    parameter_token = openapi.Parameter (
                                        "Authorization", 
                                        openapi.IN_HEADER, 
                                        description = "access_token", 
                                        type        = openapi.TYPE_STRING
    )

    mypage_get_response = openapi.Response("SUCCESS", MyPageGetSerializer)

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