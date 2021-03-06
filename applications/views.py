import boto3, json, uuid, datetime

from datetime             import datetime
from django.db.models     import Q
from django.http          import JsonResponse
from drf_yasg             import openapi
from drf_yasg.utils       import swagger_auto_schema
from rest_framework       import parsers
from rest_framework.views import APIView

from core.decorators          import login_required, admin_only
from global_variable          import ADMIN_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME
from recruits.models          import Recruit
from users.models             import User
from applications.models      import Application, ApplicationAccessLog, Attachment, Comment
from applications.serializers import ApplicationSerializer, ApplicationAdminSerializer, ApplicationAdminPatchSerializer, CommentAdminSerializer

class CloudStorage:
    AWS_ACCESS_KEY_ID     = AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
    BUCKET_NAME           = BUCKET_NAME
    def __init__(self):
        self.client = boto3.client(
                's3',
                region_name           = 'ap-northeast-2',
                aws_access_key_id     = self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = self.AWS_SECRET_ACCESS_KEY,
            )
        self.resource = boto3.resource(
                's3',
                region_name           = 'ap-northeast-2',
                aws_access_key_id     = self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = self.AWS_SECRET_ACCESS_KEY,
            )

    def upload_file(self, file):
        file_key = str(uuid.uuid1()) + file.name
        self.client.upload_fileobj(
                        file,
                        self.BUCKET_NAME,
                        file_key,
                        ExtraArgs = {
                            "ContentType": file.content_type
                        }
        )
        return file_key

    def delete_file(self, application_id):
        file_key = Attachment.objects.get(application_id=application_id).file_url
        # bucket = self.resource.Bucket(name=BUCKET_NAME)
        # bucket.Object(file_key).delete()
        self.client.delete_object(
            Bucket=BUCKET_NAME,
            Key= file_key
        )

    def generate_presigned_url(self, application_id):
        if Attachment.objects.get(application_id=application_id).file_url:
            file_key = Attachment.objects.get(application_id=application_id).file_url
            url = self.client.generate_presigned_url(
                    ClientMethod='get_object', 
                    Params={'Bucket': self.BUCKET_NAME, 
                            'Key': file_key},
                    ExpiresIn=3600)
            return url

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
        responses         = {
            "200": ApplicationSerializer,
            "404": "NOT_FOUND",
            "401": "UNAUTHORIZED"
        },
        operation_id          = "?????? ????????? ?????? ????????? ??????",
        operation_description = "header??? ????????? ???????????????."
    )

    @login_required
    def get(self, request, recruit_id):
        cloud_storage   = CloudStorage()
        try:
            user        = request.user
            recruit     = Recruit.objects.get(id=recruit_id)
            application = recruit.applications.get(user=user)
            
            content      = application.content
            download_url = cloud_storage.generate_presigned_url(application.id)

            result = {"content": content, "download_url": download_url}

            return JsonResponse({"result": result}, status=200)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "RECRUIT_NOT_FOUND"}, status=404)
        except Application.DoesNotExist:
            return JsonResponse({"message": "APPLICATION_NOT_FOUND"}, status=404)

    @swagger_auto_schema (
        manual_parameters = [parameter_token, parameter_upload],
        request_body      = ApplicationSerializer,
        responses         = {
            "201": "SUCCESS",
            "404": "NOT_FOUND",
            "401": "UNAUTHORIZED",
            "400": "BAD_REQUEST"
        },
        operation_id          = " ?????? ????????? ?????? ????????? ??????",
        operation_description = "header??? ????????? ???????????????.\n"+
                                "formData??? json????????? ???????????? ???????????????.\n"+
                                "formData??? ????????? ????????? ??? ????????????."
    )
    
    @login_required
    def post(self, request, recruit_id):
        cloud_storage = CloudStorage()
        try:
            user    = request.user
            recruit = Recruit.objects.get(id=recruit_id)
            content = json.loads(request.POST['content'])
            status  = "ST1"
            file    = request.FILES

            User.objects.filter(id=request.user.id).update(
                name = content['basicInfo']['userName']
            )

            if recruit.applications.filter(user=user).exists():
                return JsonResponse({"message": "ALREADY_EXISTS"}, status=400)

            application = Application.objects.create(
                content = content,
                status  = status,
                user    = user,
            )
            application.recruits.add(recruit)

            if '' == (application.content['career'][0]['leavingDate'] and application.content['career'][0]['joinDate']) and application.content['basicInfo']['phoneNumber']:
                return JsonResponse ({"message":"DATA_NOT_FOUND"}, status=404)  

            if file:
                file_url = cloud_storage.upload_file(file["portfolio"])
                Attachment.objects.create(
                    file_url   = file_url,
                    application = application
                )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "RECRUIT_NOT_FOUND"}, status=404)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @swagger_auto_schema (
        manual_parameters = [parameter_token, parameter_upload],
        request_body      = ApplicationSerializer,
        responses         = {
            "200": "SUCCESS",
            "404": "NOT_FOUND",
            "401": "UNAUTHORIZED",
            "400": "BAD_REQUEST"
        },
        operation_id          = "?????? ????????? ?????? ????????? ??????",
        operation_description = "header??? ????????? ???????????????.\n"+
                                "formData??? json????????? ?????? ???????????? ???????????????.\n"+
                                "formData??? ????????? ????????? ??? ????????????."
    )
    
    @login_required
    def patch(self, request, recruit_id):
        cloud_storage = CloudStorage()
        try:
            user    = request.user
            file    = request.FILES
            content = json.loads(request.POST["content"])
            
            application         = Recruit.objects.get(id=recruit_id).applications.get(user=user)
            application.content = content
            application.save()
            
            if file:
                cloud_storage.delete_file(application.id)
                file_url = cloud_storage.upload_file(file["portfolio"])
                Attachment.objects.filter(application=application).update(
                    file_url   = file_url,
                )
            
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "RECRUIT_NOT_FOUND"}, status=404)
        except Application.DoesNotExist:
            return JsonResponse({"message": "APPLICATION_NOT_FOUND"}, status=404)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)   

    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        responses = {
            "200": "SUCCESS",
            "404": "NOT_FOUND",
            "401": "UNAUTHORIZED",
        },
        operation_id = "?????? ????????? ?????? ????????? ??????",
        operation_description = "header??? ????????? ???????????????"
    )
    
    @login_required
    def delete(self, request, recruit_id):
        cloud_storage = CloudStorage()
        try:
            user        = request.user
            application = Recruit.objects.get(id=recruit_id).applications.get(user=user)

            cloud_storage.delete_file(application.id)
            application.delete()

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "RECRUIT_NOT_FOUND"}, status=404)
        except Application.DoesNotExist:
            return JsonResponse({"message": "APPLICATION_NOT_FOUND"}, status=404)

class AdminApplicationDetailView(APIView):
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
        responses         = {
            "200": application_admin_response,
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED"
        },
        operation_id          = "(????????? ??????) ?????? ???????????? ??????",
        operation_description = "header??? ????????? ???????????????."
    )
    
    @admin_only
    def get(self, request, application_id):
        cloud_storage = CloudStorage()
        application   = Application.objects.get(id=application_id)
        
        content                              = application.content
        content["portfolio"]["portfolioUrl"] = cloud_storage.generate_presigned_url(application.id)

        attachment  = Attachment.objects.get(application=application)
        
        content                              = application.content
        content["portfolio"]["portfolioUrl"] = attachment.file_url
        
        results = {   
                'id'            : application_id,
                'content'       : application.content,
                'status'        : application.status,
                'created_at'    : application.created_at,
                'updated_at'    : application.updated_at,
                'user_id'       : application.user.id,
                'user_email'    : application.user.email,
                'recruit_id'    : Recruit.objects.get(applications=application).id,
                'job_openings'  : Recruit.objects.get(applications=application).job_openings,
                'author'        : Recruit.objects.get(applications=application).author,
                'work_type'     : Recruit.objects.get(applications=application).work_type,
                'career_type'   : Recruit.objects.get(applications=application).get_career_type_display(),
                'position_title': Recruit.objects.get(applications=application).position_title,
                'position'      : Recruit.objects.get(applications=application).position,
                'deadline'      : Recruit.objects.get(applications=application).deadline
            }

        ApplicationAccessLog.objects.create(   
                user_id        = request.user.id,
                application_id = application_id,
            )

        return JsonResponse({'results': results}, status=200)
    
    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        request_body      = ApplicationAdminPatchSerializer,
        responses         = {
            "200": "SUCCESS",
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED"
        },
        operation_id          = "(????????? ??????) ?????? ?????? ??????",
        operation_description = "header??? ?????????, body??? json?????? ???????????? ???????????????.\n" +
                                "?????? ????????? status ????????? ??? : ST1, ST2, ST3, ST4, ST5\n"
    )

    @admin_only
    def patch(self, request, application_id): 
        data = json.loads(request.body)

        try:
            application               = Application.objects.filter(id=application_id)
            application.update(status = data['status'])
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except Application.DoesNotExist:
            return JsonResponse({'message': 'APPLICATION_NOT_FOUND'}, status=404)

class AdminApplicationListView(APIView):
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
        operation_id = "(????????? ??????) ???????????? ??????",
        operation_description = "header??? ????????? ???????????????."
    )

    @admin_only
    def get(self, request):
        career_type       = request.GET.get('career_type', None)
        position_title    = request.GET.get('position', None)
        status            = request.GET.get('status', None)

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
                'career_type'   : [recruits.get_career_type_display() for recruits in application.recruits.all()],
                'position_title': [recruit.position_title for recruit in application.recruits.all()],
                'position'      : [recruits.position for recruits in application.recruits.all()],
                'deadline'      : [recruits.deadline for recruits in application.recruits.all()]
            }
        for application in applications]

        return JsonResponse({'results': results}, status=200)

class RecentApplicantsListView(APIView):
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
        responses         = {
            "200": application_admin_response,
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED"
        },
        operation_id          = "(????????? ??????) ????????? ????????? ?????? ????????? ???",
        operation_description = "header??? ????????? ???????????????." 
    )

    @admin_only
    def get(self, request):
        applications = Application.objects.all().order_by('-created_at')
        results      = [{
            "application_id"    : application.id,
            "created_at"        : application.created_at,
            "user_name"         : application.user.name if application.user.name else application.user.email.split('@')[0],
            "user_email"        : application.user.email,
            "user_phoneNumber"  : application.content['basicInfo']['phoneNumber'],
            "position_title"    : [recruit.position_title for recruit in Recruit.objects.filter(applications=application)],
            "career_type"       : [recruit.get_career_type_display() for recruit in Recruit.objects.filter(applications=application)],
            "log"               : ApplicationAccessLog.objects.filter(user_id=request.user.id, application_id=application.id).exists(),           
            "career_date"       : self.career(application=application),
        } for application in applications]         
        return JsonResponse({'results': results}, status=200)

    def career(self, application):
        try:
            for i in range(0,len(application.content['career'])): 
                total        = 0
                end_date     = datetime.strptime(application.content['career'][i]['leavingDate'],"%Y/%m/%d")
                start_date   = datetime.strptime(application.content['career'][i]['joinDate'],"%Y/%m/%d")
                total        = ((end_date - start_date).days)
                years        = int(total) // 365
                months       = int(total) %365/30
            return '%d??? %d??????' % (years ,months)
        except Exception as e:
            print(e)
            return "?????? ??????"

class RecruitApplicantsListView(APIView): 
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
        responses         = {
            "200": application_admin_response,
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED",
        },
        operation_id          = "(????????? ??????) ?????? ????????? ????????? ?????? ??????",
        operation_description = "header??? ????????? ???????????????."
    )

    @admin_only
    def get(self, request,recruit_id):

        applications = Application.objects.filter(recruits=Recruit.objects.get(id=recruit_id)).order_by('-created_at')
        results = [{
        "recruit_id"        : recruit_id,
        "application_id"    : application.id,
        "created_at"        : application.created_at,
        "user_name"         : application.user.name if application.user.name else application.user.email.split('@')[0],
        "user_email"        : application.user.email,
        "user_phoneNumber"  : application.content['basicInfo']['phoneNumber'],
        "position_title"    : [recruit.position_title for recruit in Recruit.objects.filter(applications=application)],
        "career_type"       : [recruit.get_career_type_display() for recruit in Recruit.objects.filter(applications=application)],
        "log"               : ApplicationAccessLog.objects.filter(user_id=request.user.id, application_id=application.id).exists(),           
        "career_date"       : self.career(application = application),
        } for application in applications]         
        return JsonResponse({'results': results}, status=200)

    def career(self, application):
        try:
            for i in range(0,len(application.content['career'])): 
                total        = 0
                end_date     = datetime.strptime(application.content['career'][i]['leavingDate'],"%Y/%m/%d")
                start_date   = datetime.strptime(application.content['career'][i]['joinDate'],"%Y/%m/%d")
                total        = ((end_date - start_date).days)
                years        = int(total) // 365
                months       = int(total) %365/30
            return '%d??? %d??????' % (years,months)
        except Exception as e:
            print(e)
            return "?????? ??????"

class AdminCommentView(APIView):
    parameter_token = openapi.Parameter (
                                        "Authorization", 
                                        openapi.IN_HEADER, 
                                        description = "access_token", 
                                        type        = openapi.TYPE_STRING,
                                        default     = ADMIN_TOKEN
    )
    comment_admin_response = openapi.Response("result", CommentAdminSerializer)

    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        responses         = {
            "200": comment_admin_response,
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED"
        },
        operation_id          = "(????????? ??????) ????????? ????????? ??? ?????? ??????",
        operation_description = "header??? ????????? ???????????????."
    )

    @admin_only
    def get(self, request, application_id):
        try:
            application = Application.objects.get(id=application_id)
            
            results = {  
                'comments' : [{
                        'id'         : comment.id,
                        'admin_id'   : comment.user_id,
                        'admin_name' : User.objects.get(id=comment.user_id).name if User.objects.get(id=comment.user_id).name else User.objects.get(id=comment.user_id).email.split('@')[0],
                        'created_at' : comment.created_at,
                        'updated_at' : comment.updated_at,
                        'description': comment.description,
                        'score'      : comment.score  
                } for comment in Comment.objects.filter(application=application)]
            }
            return JsonResponse({'results': results}, status=200)

        except Application.DoesNotExist:
            return JsonResponse({'message': 'APPLICATION_NOT_FOUND'}, status=404)
        except Comment.DoesNotExist:
            return JsonResponse({'message': 'COMMENT_NOT_FOUND'}, status=404)
    
    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        request_body      = CommentAdminSerializer,
        responses         = {
            "200": comment_admin_response,
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED"
        },
        operation_id          = "(????????? ??????) ????????? ????????? ??? ?????? ??????",
        operation_description = "header??? ?????????, body??? description??? score????????? ???????????????.\n"
    )

    @admin_only
    def post(self, request, application_id):
        data        = json.loads(request.body)
        application = Application.objects.get(id=application_id)
        
        Comment.objects.create(
            user_id        = request.user.id,
            application_id = application.id,
            description    = data['description'],
            score          = data['score'],  
        )

        return JsonResponse({'message': 'SUCCESS'}, status=200)
    
class AdminCommentModifyView(APIView):
    parameter_token = openapi.Parameter (
                                        "Authorization", 
                                        openapi.IN_HEADER, 
                                        description = "access_token", 
                                        type        = openapi.TYPE_STRING,
                                        default     = ADMIN_TOKEN
    )
    comment_admin_response = openapi.Response("result", CommentAdminSerializer)
    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        request_body      = CommentAdminSerializer,
        responses         = {
            "200": "SUCCESS",
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED"
        },
        operation_id          = "(????????? ??????) ????????? ????????? ??? ?????? ??????",
        operation_description = "header??? ?????????, body??? description??? score????????? ???????????????.\n"
    )

    @admin_only
    def patch(self, request, application_id, comment_id): 
        try:
            data    = json.loads(request.body)
            user    = request.user
            comment = Comment.objects.get(id = comment_id)

            if not user.id == comment.user_id:
                return JsonResponse({'message': 'NOT_AUTHORIZED'}, status=403)
            
            Comment.objects.filter(id = comment_id).update(
                description    = data['description'],
                score          = data['score']
            )
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except Comment.DoesNotExist:
            return JsonResponse({'message': 'NOT_FOUND'}, status=404)
    
    @swagger_auto_schema (
        manual_parameters = [parameter_token],
        responses         = {
            "200": "SUCCESS",
            "400": "BAD_REQUEST",
            "401": "UNAUTHORIZED"
        },
        operation_id          = "(????????? ??????) ????????? ????????? ??? ?????? ??????",
        operation_description = "header??? ?????????, body??? description??? score????????? ???????????????.\n"
    )
    
    @admin_only
    def delete(self, request, application_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)

            if not request.user.id == comment.user_id:
                return JsonResponse({'message': 'NOT_AUTHORIZED'}, status=403)

            comment.delete()

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except Comment.DoesNotExist:
            return JsonResponse({'message': 'NOT_FOUND'}, status=404)

