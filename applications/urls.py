from django.urls import path

from applications.views import ApplicationAdminView, ApplicationAdminDetailView, ApplicatorAdminView

urlpatterns = [
    path('', ApplicationAdminView.as_view()),
    path('/<int:application_id>', ApplicationAdminDetailView.as_view()),
    path('/applicator', ApplicatorAdminView.as_view())
]