###스톡폴리오 채용관리 1.0 authors
##1.0 사용자의 채용지원

@이재성 (스톡폴리오 백엔드)  
swagger api 셋업  
도커 스크립트  
전체 프로젝트 리뷰 및 관리  

@김예랑  
(사용자) ApplicationView(patch, delete) : 지원서 수정, 삭제  
(사용자) RecruitListView :  채용공고 목록 조회, 필터링, 정렬  
(사용자, 관리자) RecruitView : (사용자, 관리자) 채용공고 조회, (관리자) 채용공고 생성/수정/삭제    
(사용자) VerificationView : 비밀번호 재설정 이메일 발송  
(사용자) UserMyPageView : 회원정보 조회 및 수정  
aws/s3 포트폴리오 파일 첨부 기능 수정  
Serializer, modeling 수정  
유저/어드민 데코레이터 작성  
Swagger api 작성  
Readme.md 작성  

@최명준  
(사용자) 회원가입, 로그인  
(사용자) ApplicationView(get, post) : 지원서 조회, 생성  
(관리자) ApplicationAdminView : 지원이력관리  
(관리자) ApplicationAdminDetailView: 지원서 상세 조회  
aws/s3 포트폴리오 파일 첨부 기능  
Serializer, modeling 수정  
Swagger api 작성  
초기 세팅  

##스톡폴리오 채용관리 1.1 authors
###1.1 어드민 관련 기능 구현 (어드민 페이지, 슈퍼 어드민, 지원자 평가)

@김도담(PM)
(관리자) AdminPageNumberView : 어드민 페이지 대시보드 : 채용 관련 정보 도식화  
(관리자) AdminPageRecruitListView : 어드민 페이지 내부 채용 공고  
(관리자) AdminRecruitListView : 어드민 전용 채용 공고 조회  
(관리자) AdminPageApplicatorAdminView : 어드민 페이지 최근 지원자 조회 (이름/경력/휴대폰번호 등 요약 정보 표시, 경력 계산 로직 구현, 읽지않은 지원서 New 표시)  
(관리자)  ApplicationAdminDetailView: 어드민 지원자 세부사항 조회 Access_log 추가 (어드민이 지원서를 읽으면 log기록 => 읽지않은 지원서 New 표시)  
(관리자) RecruitApplicatorView: 특정 공고 지원자 목록 조회 (읽지않은 지원서 New 라벨 붙이기, 경력 로직 구현)  
(관리자) ApplicationView : 지원서 에러 핸들링 (필수정보 빈 값 들어올 시 에러 반환)  
전체 코드 에러 핸들링  
Swagger api 작성  
Authors.md 작성  

@고유영
(슈퍼관리자) SuperAdminView, SuperAdminModifyView : 슈퍼어드민의 어드민 계정관리 CRUD  
(관리자) AdminCommentView: 지원서 평가용 코멘트(점수) CRUD  
(관리자) AdminApplicationDetailView: 지원서 세부사항 뷰(AWS s3 파일 CRUD, 조회용 임시 url 생성)   
(관리자) AdminRecruitDetailView: 채용공고 상세 조회  
(관리자) MyRecruitListView: 내가 올린 채용공고 목록 조회  
aws/s3 관련 코드 리팩토링  
슈퍼어드민 데코레이터 추가  
Swagger api 작성  
