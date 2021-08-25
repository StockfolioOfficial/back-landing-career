import boto3
import json
import uuid

from django.db.models     import Q
from django.http          import JsonResponse
from drf_yasg             import openapi
from drf_yasg.utils       import swagger_auto_schema
from rest_framework       import parsers
from rest_framework.views import APIView

from core.decorators          import login_required, admin_only
from global_variable          import ADMIN_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from recruits.models          import Recruit
from applications.models      import Application, Attachment
from applications.serializers import ApplicationSerializer, ApplicationAdminSerializer, ApplicationAdminPatchSerializer

class ApplicationView(APIView):
    parameter_token = openapi.Parameter (
                                        "Authorization", 
                                        openapi.IN_HEADER, 
                                        description = "access_token", 
                                        type        = openapi.TYPE_STRING,
                                        default     = ADMIN_TOKEN
    )
    parameter_upload = openapi.Parameter(
                                        "portfolio",
                                        openapi.IN_FORM,
                                        description = "upload_file",
                                        type        = openapi.TYPE_FILE
    )
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

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
            user        = request.user
            recruit     = Recruit.objects.get(id=recruit_id)
            application = recruit.applications.get(user=user)
            attachment  = Attachment.objects.get(application=application)
            
            content = eval(application.content)
            content["portfolio"]["portfolioUrl"] = attachment.file_url

            result = {"content": content}

            return JsonResponse({"result": result}, status=200)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)
        except Application.DoesNotExist:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)

    @swagger_auto_schema (
        manual_parameters = [parameter_token, parameter_upload],
        request_body= ApplicationSerializer,
        responses = {
            "201": "SUCCESS",
            "404": "NOT_FOUND",
            "401": "UNAUTHORIZED",
            "400": "BAD_REQUEST"
        },
        operation_id = "해당 공고에 대한 지원서 생성",
        operation_description = "header에 토큰이 필요합니다.\n"+
                                "formData에 json형식의 데이터가 필요합니다.\n"+
                                "formData에 파일을 첨부할 수 있습니다."
    )
    
    @login_required
    def post(self, request, recruit_id):
        try:
            user    = request.user
            recruit = Recruit.objects.get(id=recruit_id)
            content = request.POST['content']
            status  = "ST1"

            if recruit.applications.filter(user=user).exists():
                return JsonResponse({"message": "ALREADY_EXISTS"}, status=400)

            if not request.FILES:
                content_dict = eval(content)
                file_url     = content_dict["portfolio"]["portfolioUrl"]

                application = Application.objects.create(
                                        content = content,
                                        status  = status,
                                        user    = user,
                )
                application.recruits.add(recruit)

                Attachment.objects.create(
                    file_url    = file_url,
                    application = application
                )

                return JsonResponse({"message": "SUCCESS"}, status=201)

            portfolio = request.FILES['portfolio']
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id     = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            )

            file_name = str(uuid.uuid1())
            
            s3_client.upload_fileobj(
                portfolio,
                "stockers-bucket",
                file_name,
                ExtraArgs={
                    "ContentType": portfolio.content_type
                }
            )

            file_url = "stockfolio.coo6llienldy.ap-northeast-2.rds.amazonaws.com/" + file_name

            application = Application.objects.create(
                content = content,
                status  = status,
                user    = user,
            )
            application.recruits.add(recruit)

            Attachment.objects.create(
                file_url    = file_url,
                application = application
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "NOT_FOUND"}, status=404)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @swagger_auto_schema (
        manual_parameters = [parameter_token, parameter_upload],
        request_body= ApplicationSerializer,
        responses = {
            "200": "SUCCESS",
            "404": "NOT_FOUND",
            "401": "UNAUTHORIZED",
            "400": "BAD_REQUEST"
        },
        operation_id = "해당 공고에 대한 지원서 수정",
        operation_description = "header에 토큰이 필요합니다.\n"+
                                "formData에 json형식의 수정 데이터가 필요합니다.\n"+
                                "formData에 파일을 첨부할 수 있습니다."
    )
    
    @login_required
    def patch(self, request, recruit_id):
        try:
            user    = request.user
            recruit = Recruit.objects.get(id=recruit_id)
            
            content = request.POST["content"]

            application = recruit.applications.get(user=user)
            application.content = content
            application.save()

            attachment = Attachment.objects.get(application=application)

            s3_client = boto3.client(
                's3',
                aws_access_key_id     = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            )

            if request.FILES:
                portfolio = request.FILES["portfolio"]
                file_name = str(uuid.uuid1())
            
                s3_client.upload_fileobj(
                    portfolio,
                    "stockers-bucket",
                    file_name,
                    ExtraArgs={"ContentType": portfolio.content_type}
                )

                file_url = "stockfolio.coo6llienldy.ap-northeast-2.rds.amazonaws.com/" + file_name
                
            else:
                content_dict = eval(content)
                file_url     = content_dict["portfolio"]["portfolioUrl"]

            if "stockfolio.coo6llienldy.ap-northeast-2.rds.amazonaws.com/" in attachment.file_url:
                if not file_url == attachment.file_url:
                    key = attachment.file_url.replace("stockfolio.coo6llienldy.ap-northeast-2.rds.amazonaws.com/", "")
                    s3_client.delete_object(Bucket="stockers-bucket", Key=key)
                
            attachment.file_url = file_url
            attachment.save()
                
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
        career_type = request.GET.get('career_type', None)
        position_title    = request.GET.get('position', None)
        status      = request.GET.get('status', None)

        q = Q()

        if career_type:
            q.add(Q(recruits__career_type = career_type), q.AND)
        
        if position_title:
            q.add(Q(recruits__position_title = position_title), q.AND)

        if status:
            q.add(Q(status = status), q.AND)

        applications = Application.objects.filter(q).order_by('-created_at')

        results = [
            {
                'content'       : application.content,
                'status'        : application.status,
                'created_at'    : application.created_at,
                'updated_at'    : application.updated_at,
                'recruit_id'    : [recruits.id for recruits in application.recruits.all()],
                'job_openings'  : [recruits.job_openings for recruits in application.recruits.all()],
                'author'        : [recruits.author for recruits in application.recruits.all()],
                'work_type'     : [recruits.work_type for recruits in application.recruits.all()],
                'career_type'   : [recruits.career_type for recruits in application.recruits.all()],
                'position_title': [recruit.position_title for recruit in application.recruits.all()],
                'position'      : [recruits.position for recruits in application.recruits.all()],
                'deadline'      : [recruits.deadline for recruits in application.recruits.all()]
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
                'id'            : application_id,
                'content'       : application.content,
                'status'        : application.status,
                'created_at'    : application.created_at,
                'updated_at'    : application.updated_at,
                'user_id'       : application.user.id,
                'user_email'    : application.user.email,
                'recruit_id'    : [recruits.id for recruits in application.recruits.all()],
                'job_openings'  : [recruits.job_openings for recruits in application.recruits.all()],
                'author'        : [recruits.author for recruits in application.recruits.all()],
                'work_type'     : [recruits.work_type for recruits in application.recruits.all()],
                'career_type'   : [recruits.career_type for recruits in application.recruits.all()],
                'position_title': [recruits.position_type for recruits in application.recruits.all()],
                'position'      : [recruits.position for recruits in application.recruits.all()],
                'deadline'      : [recruits.deadline for recruits in application.recruits.all()]
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

        except Application.DoesNotExist:
            return JsonResponse({'message': 'NOT_FOUND'}, status=404)