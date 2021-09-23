from django.urls import path

from applications.views import ApplicationView
from recruits.views     import RecruitListView, RecruitView, RecruitAdminView

urlpatterns = [
    path('', RecruitListView.as_view()),
    path('/<int:recruit_id>', RecruitView.as_view()),
    path('/admin/<int:recruit_id>', RecruitAdminView.as_view()),
    path('/<int:recruit_id>/applications', ApplicationView.as_view()),
]