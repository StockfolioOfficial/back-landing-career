from django.urls import path, re_path, include
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg       import openapi

schema_view = get_schema_view( 
    openapi.Info( 
        title            = "Stockers API", 
        default_version  = "v1", 
        description      = "Stockers API 문서", 
        terms_of_service = "https://www.google.com/policies/terms/", 
        contact          = openapi.Contact(email="test@test.com"), 
        license          = openapi.License(name="김예랑, 최명준"), 
    ), 

    public             = True, 
    permission_classes = (permissions.AllowAny,), 
)

urlpatterns = [
    path('users', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]