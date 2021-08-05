from django.urls import path

from users.views import UserMyPageView

urlpatterns = [
    path('/mypage', UserMyPageView.as_view()),
]