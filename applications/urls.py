from django.urls import path

from applications.views import ApplicationAdminView, ApplicationAdminDetailView, ApplicatorAdminView, RecruitApplicatorView

urlpatterns = [
    path('', ApplicationAdminView.as_view()),
    path('/<int:application_id>', ApplicationAdminDetailView.as_view()),
    path('/admin/applicator',ApplicatorAdminView.as_view()),
    path('/admin/<int:recruit_id>', RecruitApplicatorView.as_view()),
]