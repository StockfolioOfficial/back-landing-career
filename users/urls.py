from django.urls import path

from users.views import SignupView, SigninView, UserMyPageView, VerificationView, SuperadminView

urlpatterns = [
    path('/mypage', UserMyPageView.as_view()),
    path("/signin", SigninView.as_view()),
    path("/signup", SignupView.as_view()),
    path("/verification", VerificationView.as_view()),
    path('/admins', SuperadminView.as_view()),
    path('/admin/<int:user_id>', SuperadminView.as_view()),
]