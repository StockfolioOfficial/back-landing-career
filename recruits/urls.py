from django.urls     import path

from recruits.views  import RecruitListView, RecruitListAdminView, RecruitMyListAdminView, DashboardAdminView, RecruitDetailView, RecruitDetailAdminView, RecruitCreateView, RecruitModifyView


urlpatterns = [
    path('', RecruitListView.as_view()), #(유저)채용공고 목록 조회
    path('/admin/list', RecruitListAdminView.as_view()),#(관리자)채용공고 목록 조회
    path('/admin/my', RecruitMyListAdminView.as_view()),#(관리자)내가 올린 채용공고 목록 조회
    path('/admin/dashboard', DashboardAdminView.as_view()),#(관리자)어드민 대시보드 페이지 조회

    path('/<int:recruit_id>', RecruitDetailView.as_view()),#(유저)공고 상세 조회
    path('/admin/<int:recruit_id>', RecruitDetailAdminView.as_view()),#(관리자)공고 상세 조회

    path('/admin', RecruitCreateView.as_view()),#(관리자)공고 생성
    path('/admin/<int:recruit_id>', RecruitModifyView.as_view()),#(관리자)공고 수정 및 삭제
]