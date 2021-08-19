import json

from django.http          import JsonResponse
from drf_yasg             import openapi
from drf_yasg.utils       import swagger_auto_schema
from rest_framework.views import APIView

from core.decorators     import login_required
from my_settings         import ADMIN_TOKEN
from recruits.models     import Recruit
from applications.models import Application

from applications.serializers import ApplicationSerializer

class ApplicationView(APIView):
    parameter_token = openapi.Parameter (
                                        "Authorization", 
                                        openapi.IN_HEADER, 
                                        description = "access_token", 
                                        type        = openapi.TYPE_STRING,
                                        default     = ADMIN_TOKEN
    )

    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        responses = {
            "200": ApplicationSerializer,
            "404": "NOT_FOUND",
            "401": "UNAUTHORIZED"
        },
        operation_id = "해당 공고에 대한 지원서 조회",
        operation_description = "header에 토큰이 필요합니다."
    )
    @login_required
    def get(self, request, recruit_id):
        try:
            user    = request.user
            recruit = Recruit.objects.get(id=recruit_id)

            application = recruit.applications.get(user=user)

            result = {"content": application.content}

            return JsonResponse({"result": result}, status=200)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)
        except Application.DoesNotExist:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)

    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        request_body= ApplicationSerializer,
        responses = {
            "201": "SUCCESS",
            "404": "NOT_FOUND",
            "401": "UNAUTHORIZED",
            "400": "BAD_REQUEST"
        },
        operation_id = "해당 공고에 대한 지원서 생성",
        operation_description = "header에 토큰이, body에 json형식 데이터가 필요합니다."
    )
    @login_required
    def post(self, request, recruit_id):
        try:
            user    = request.user
            recruit = Recruit.objects.get(id=recruit_id)
            
            data    = json.loads(request.body)
            content = data["content"]
            status  = "ST1"

            application = Application.objects.create(
                content = content,
                status  = status,
                user    = user,
            )
            application.recruits.add(recruit)
            
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        request_body= ApplicationSerializer,
        responses = {
            "200": "SUCCESS",
            "404": "NOT_FOUND",
            "401": "UNAUTHORIZED",
            "400": "BAD_REQUEST"
        },
        operation_id = "해당 공고에 대한 지원서 수정",
        operation_description = "header에 토큰이, body에 json형식 데이터가 필요합니다."
    )
    @login_required
    def patch(self, request, recruit_id):
        try:
            user    = request.user
            recruit = Recruit.objects.get(id=recruit_id)
            
            data    = json.loads(request.body)
            content = data["content"]

            application = recruit.applications.get(user=user)
            application.content = content
            application.save()
            
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)
        except Application.DoesNotExist:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)    

    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        responses = {
            "200": "SUCCESS",
            "404": "NOT_FOUND",
            "401": "UNAUTHORIZED",
        },
        operation_id = "해당 공고에 대한 지원서 삭제",
        operation_description = "header에 토큰이 필요합니다"
    )
    @login_required
    def delete(self, request, recruit_id):
        try:
            user    = request.user
            recruit = Recruit.objects.get(id=recruit_id)

            application = recruit.applications.get(user=user)
            application.delete()

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)
        except Application.DoesNotExist:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)
        