from django.urls import path

from applications.views import  ApplicationView, AdminApplicationDetailView, AdminApplicationListView,\
    RecentApplicantsListView, RecruitApplicantsListView, AdminCommentView, AdminCommentModifyView

urlpatterns = [
    path('/user/<int:recruit_id>', ApplicationView.as_view()),
    path('/admin/<int:application_id>', AdminApplicationDetailView.as_view()),

    path('/admin', AdminApplicationListView.as_view()),
    path('/admin/recent',RecentApplicantsListView.as_view()),
    
    path('/admin/recruits/<int:recruit_id>', RecruitApplicantsListView.as_view()),

    path('/admin/<int:application_id>/comments', AdminCommentView.as_view()),
    path('/admin/<int:application_id>/comment/<int:comment_id>', AdminCommentModifyView.as_view()),
]