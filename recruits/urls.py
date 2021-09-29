from django.urls import path

from recruits.views     import RecruitListView, RecruitView, AdminRecruitListView, AdminpageNumberView,  \
     AdminPageRecruitListView, MyRecruitListView, AdminRecruitDetailView


urlpatterns = [
    path('/user', RecruitListView.as_view()),
    path('/user/<int:recruit_id>', RecruitView.as_view()),

    path('/admin',AdminRecruitListView.as_view()),
    path('/admin/number', AdminpageNumberView.as_view()),
    path('/admin/list', AdminPageRecruitListView.as_view()),
    path('/admin/my', MyRecruitListView.as_view()),
    path('/admin/<int:recruit_id>', AdminRecruitDetailView.as_view())
]