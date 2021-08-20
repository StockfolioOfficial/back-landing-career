from django.urls import path

from applications.views import ApplicationAdminView, ApplicationAdminDetailView

urlpatterns = [
    path('', ApplicationAdminView.as_view()),
    path('/<int:application_id>', ApplicationAdminDetailView.as_view())
]