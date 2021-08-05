from django.urls import path

from users.views import SignupView, UserMyPageView

urlpatterns = [
    path('/mypage', UserMyPageView.as_view()),
    path("/signup", SignupView.as_view()),
]