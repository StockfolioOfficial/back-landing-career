from django.urls import path

from applications.views import ApplicationView
from recruits.views     import RecruitListView, RecruitView, AdminPageView, AdminRecruitListView, AdminPageRecruitView

urlpatterns = [
    path('', RecruitListView.as_view()),
    path('/<int:recruit_id>', RecruitView.as_view()),
    path('/<int:recruit_id>/applications', ApplicationView.as_view()),
    path('/admin/dashboard',AdminPageView.as_view()),
    path('/admin', AdminPageRecruitView.as_view()),
    path('/adminRecruit',AdminRecruitListView.as_view())
]