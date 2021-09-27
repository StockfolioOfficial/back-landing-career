from django.urls import path

from applications.views import ApplicationAdminView, ApplicationAdminDetailView,CommentAdminView,CommentAdminModifyView, RecruitApplicatorView

urlpatterns = [
    path('', ApplicationAdminView.as_view()),
    path('/<int:application_id>', ApplicationAdminDetailView.as_view()),
    path('/<int:application_id>/comments', CommentAdminView.as_view()),
    path('/<int:application_id>/comment/<int:comment_id>', CommentAdminModifyView.as_view()),

    path('/admin/<int:recruit_id>', RecruitApplicatorView.as_view()),
]