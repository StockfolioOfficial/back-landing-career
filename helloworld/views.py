from django.http import JsonResponse

from rest_framework.views import APIView


class HelloWorld(APIView):
    def get(self, request):
        return JsonResponse({"hello": "world"}, status=200)
