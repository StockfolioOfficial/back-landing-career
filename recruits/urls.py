from django.urls import path

from applications.views import ApplicationView
from recruits.views     import RecruitListView, RecruitView, AdmipageDashboardView

urlpatterns = [
    path('', RecruitListView.as_view()),
    path('/<int:recruit_id>', RecruitView.as_view()),
    path('/<int:recruit_id>/applications', ApplicationView.as_view()),
    path('/admin/dashboard', AdmipageDashboardView.as_view())
]