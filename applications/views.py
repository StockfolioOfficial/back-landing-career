import json

from django.db.models     import Q
from django.http          import JsonResponse
from drf_yasg             import openapi
from drf_yasg.utils       import swagger_auto_schema
from rest_framework.views import APIView

from core.decorators          import login_required, admin_only
from my_settings              import ADMIN_TOKEN
from recruits.models          import Recruit
from applications.models      import Application
from applications.serializers import ApplicationSerializer, ApplicationAdminSerializer, ApplicationAdminPatchSerializer

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

class ApplicationAdminView(APIView):
    parameter_token = openapi.Parameter (
                                        "Authorization",
                                        openapi.IN_HEADER,
                                        description = "access_token", 
                                        type        = openapi.TYPE_STRING,
                                        default     = ADMIN_TOKEN
    )
    
    application_admin_response = openapi.Response("result", ApplicationAdminSerializer)

    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        responses = {
            "200": application_admin_response,
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED",
        },
        operation_id = "(관리자 전용) 지원목록 조회",
        operation_description = "header에 토큰이 필요합니다."
    )

    @admin_only
    def get(self, request):
        type     = request.GET.get('type', None)
        position = request.GET.get('position', None)
        status   = request.GET.get('status', None)

        q = Q()

        if type:
            q.add(Q(recruits__type = type), q.AND)
        
        if position:
            q.add(Q(recruits__position = position), q.AND)

        if status:
            q.add(Q(status = status), q.AND)

        applications = Application.objects.filter(q).order_by('-created_at')

        results = [
            {
                'content'   : application.content,
                'status'    : application.status,
                'created_at': application.created_at,
                'updated_at': application.updated_at,
                'recruit_id': [recruit.id for recruit in application.recruits.all()],
                'type'      : [recruits.type for recruits in application.recruits.all()],
                'position'  : [recruits.position for recruits in application.recruits.all()],
                'deadline'  : [recruits.deadline for recruits in application.recruits.all()]
            }
        for application in applications]

        return JsonResponse({'results': results}, status=200)

class ApplicationAdminDetailView(APIView):
    parameter_token = openapi.Parameter (
                                        "Authorization", 
                                        openapi.IN_HEADER, 
                                        description = "access_token", 
                                        type        = openapi.TYPE_STRING,
                                        default     = ADMIN_TOKEN
    )
    
    application_admin_response = openapi.Response("result", ApplicationAdminSerializer)

    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        responses = {
            "200": application_admin_response,
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED"
        },
        operation_id = "(관리자 전용) 지원 세부사항 조회",
        operation_description = "header에 토큰이 필요합니다."
    )
    
    @admin_only
    def get(self, request, application_id):
        application = Application.objects.get(id=application_id)

        results = [
            {   
                'id'        : application_id,
                'content'   : application.content,
                'status'    : application.status,
                'created_at': application.created_at,
                'updated_at': application.updated_at,
                'user_id'   : application.user.id,
                'user_email': application.user.email,
                'recruit_id': [recruit.id for recruit in application.recruits.all()],
                'type'      : [recruits.type for recruits in application.recruits.all()],
                'position'  : [recruits.position for recruits in application.recruits.all()],
                'deadline'  : [recruits.deadline for recruits in application.recruits.all()]
            }
        ]

        return JsonResponse({'results': results}, status=200)
    
    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        request_body = ApplicationAdminPatchSerializer,
        responses = {
            "200": "SUCCESS",
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED"
        },
        operation_id = "(관리자 전용) 지원 상태 수정",
        operation_description = "header에 토큰이, body에 json형식 데이터가 필요합니다.\n" +
                                "입력 가능한 status 데이터 값 : ST1, ST2, ST3, ST4, ST5\n"
    )

    @admin_only
    def patch(self, request, application_id): 
        data = json.loads(request.body)

        try:
            application = Application.objects.filter(id=application_id)
            application.update(status = data['status'])
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Application.DoesNotExist:
            return JsonResponse({'message': 'NOT_FOUND'}, status=404)