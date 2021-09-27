from django.urls import path

from applications.views import ApplicationView, ApplicationAdminView, ApplicationAdminDetailView,CommentAdminView,CommentAdminModifyView

urlpatterns = [
    path('', ApplicationAdminView.as_view()),
    path('/<int:application_id>', ApplicationAdminDetailView.as_view()),
    path('/<int:application_id>/comments', CommentAdminView.as_view()),
    path('/<int:application_id>/comment/<int:comment_id>', CommentAdminModifyView.as_view()),

    path('/<int:recruit_id>/applications', ApplicationView.as_view()), #해당 공고에 대한 지원서 조회
]