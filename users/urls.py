from django.urls import path

from users.views import SignupView, SigninView, UserMyPageView

urlpatterns = [
    path('/mypage', UserMyPageView.as_view()),
    path("/signin", SigninView.as_view()),
    path("/signup", SignupView.as_view()),
]