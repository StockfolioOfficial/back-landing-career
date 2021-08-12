from django.urls import path

from applications.views import ApplicationView

urlpatterns = [
    path('/<int:recruit_id>/applications', ApplicationView.as_view()),
]