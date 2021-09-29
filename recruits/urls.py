from django.urls import path

from applications.views import ApplicationView
from recruits.views     import RecruitListView, RecruitView, AdmipageDashboardView, AdminRecruitListView, \
     AdminPageRecruitView, RecruitListInquireView


urlpatterns = [
    path('', RecruitListView.as_view()),
    path('/<int:recruit_id>', RecruitView.as_view()),

    path('/admin/dashboard', AdmipageDashboardView.as_view()),
    path('/admin/recruit-list', AdminPageRecruitView.as_view()),
    path('/admin/lookup', RecruitListInquireView.as_view()),

    path('/all/admin/recruit-list',AdminRecruitListView.as_view()),
]