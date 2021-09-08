from django.urls import path

from users.views import SignupView, SigninView, UserMyPageView, VerificationView, SuperAdminView, SuperAdminModifyView

urlpatterns = [
    path('/mypage', UserMyPageView.as_view()),
    path("/signin", SigninView.as_view()),
    path("/signup", SignupView.as_view()),
    path("/verification", VerificationView.as_view()),
    path('/admins', SuperAdminView.as_view()),
    path('/admin/<int:user_id>', SuperAdminModifyView.as_view()),
]