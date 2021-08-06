from django.urls import path

<<<<<<< HEAD
from users.views import UserMyPageView

urlpatterns = [
    path('/mypage', UserMyPageView.as_view()),
=======
from users.views import SignupView, SigninView, UserMyPageView

urlpatterns = [
    path('/mypage', UserMyPageView.as_view()),
    path("/signin", SigninView.as_view()),
    path("/signup", SignupView.as_view()),
>>>>>>> edbd58c ( - #10 Add(Signin): 로그인 EndPoint, API 구현)
]