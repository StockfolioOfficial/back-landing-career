from django.urls import path

from applications.views import ApplicationAdminView, ApplicationAdminDetailView, ApplicatorAdminView, RecruitApplicatorView
from applications.views import ApplicationAdminView, ApplicationAdminDetailView,CommentAdminView,CommentAdminModifyView

urlpatterns = [
    path('', ApplicationAdminView.as_view()),
    path('/<int:application_id>', ApplicationAdminDetailView.as_view()),
    path('/admin/applicator',ApplicatorAdminView.as_view()),
    path('/admin/<int:recruit_id>', RecruitApplicatorView.as_view()),
    path('/<int:application_id>/comments', CommentAdminView.as_view()),
    path('/<int:application_id>/comment/<int:comment_id>', CommentAdminModifyView.as_view()),
]