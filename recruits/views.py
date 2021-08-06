from inspect import stack
import json, sys, hashlib, sha3

from django.http  import JsonResponse

from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg       import openapi

from recruits.models import Recruit, Stack
from core.decorators import query_debugger
from recruits.serializers import RecruitSerializer

class RecruitListView(APIView):
    recruits_get_response = openapi.Response("results", RecruitSerializer)
    
    @swagger_auto_schema(
        responses = {
            "200": recruits_get_response,
            "404": "NOT_FOUND"
        },
        operation_id = "채용 목록 조회",
        operation_description = "모든 채용 목록을 조회합니다."
    )
    @query_debugger
    def get(self, request):
        recruits = Recruit.objects.prefetch_related('stacks').all()

        results = [
            {
                "id"         : recruit.id,
                "position"   : recruit.position,
                "description": recruit.description,
                "created_at" : recruit.created_at,
                "updated_at" : recruit.updated_at,
                "stacks"     : [ stack.name for stack in recruit.stacks.all() ]
            }
            for recruit in recruits
        ]
        return JsonResponse({"results": results}, status=200)

    @query_debugger
    def post(self, request):
        try:
            data        = json.loads(request.body)
            position    = data["position"]
            description = data["description"]
            stack_names = data["stacks"]

            stacks = []
            
            for stack_name in stack_names:
                s = hashlib.sha3_256()
                s.update(stack_name.encode())
                hash_id = s.hexdigest()

                object, is_created = Stack.objects.get_or_create(hash_id=hash_id)

                if is_created:
                    object.name = stack_name
                    object.save()

                stacks.append(object)


            recruit = Recruit.objects.create(
                position = position,
                description = description,
            )

            recruit.stacks.add(*stacks)


            return JsonResponse({"test" : stack_names}, status=201)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        

class RecruitView(APIView):
    recruit_get_response = openapi.Response("result", RecruitSerializer)

    @swagger_auto_schema(
        responses = {
            "200": recruit_get_response,
            "400": "RECRUIT_DOES_NOT_EXISTS",
            "404": "NOT_FOUND"
        },
        operation_id = "채용 상세 조회",
        operation_description = "특정 채용 정보를 조회합니다."
    )
    @query_debugger
    def get(self, request, recruit_id):
        try:
            recruit = Recruit.objects.prefetch_related('stacks').get(id=recruit_id)

            result = {
                "id"         : recruit.id,
                "position"   : recruit.position,
                "description": recruit.description,
                "created_at" : recruit.created_at,
                "updated_at" : recruit.updated_at,
                "stacks"     : [ stack.name for stack in recruit.stacks.all() ]
            }

            return JsonResponse({"result": result}, status=200)

        except Recruit.DoesNotExist:
            return JsonResponse({"message": "RECRUIT_DOES_NOT_EXISTS"}, status=400)