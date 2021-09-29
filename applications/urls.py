from django.urls import path

from applications.views import ApplicationAdminListView, ApplicationView, ApplicationAdminDetailView,\
     CommentAdminView,CommentAdminModifyView, ApplicatorAdminView, RecruitApplicatorView

urlpatterns = [
    path('/user/<int:recruit_id>', ApplicationView.as_view()),
    path('/detail/<int:application_id>', ApplicationAdminDetailView.as_view()),
    
    path('/admin/list', ApplicationAdminListView.as_view()),
    path('/admin/<int:recruit_id>', RecruitApplicatorView.as_view()),
    path('/admin/applicator',ApplicatorAdminView.as_view()),

    path('/comments/<int:application_id>', CommentAdminView.as_view()),
    path('/comments/<int:application_id>/<int:comment_id>', CommentAdminModifyView.as_view()),
]