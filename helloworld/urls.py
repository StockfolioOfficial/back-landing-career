from django.urls import path

from helloworld.views import HelloWorld

urlpatterns = [
    path('', HelloWorld.as_view())
]
