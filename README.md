# back-landing-career
## 프로젝트 소개
- 영상 편집 및 구독 서비스 기업 <a href="https://stockfolio.ai" target="_blank">스톡폴리오(stock folio)</a>의 채용 페이지를 구현한 오픈소스 프로젝트입니다.
- 스톡폴리오에서 제공해주신 UX/UI 디자인을 바탕으로 API를 구현했습니다.
### 개발 인원 및 기간
- 개발 기간 : 2021-08-02 ~ 2021-08-25
- 개발 인원 : 최명준, 김예랑
## 적용 기술 및 구현 기능
#### 기술 스택
- Python, Django, MySQL, Sendgrid, s3(AWS storage)
#### API 문서화
- Swagger (with drf-yasg)
#### 협업 도구
- Git + GitHub, Github Issues, Github Projects
#### 배포 관련
- Docker, Github Actions, AWS(ECR, EC2, RDS)
### 구현 기능
- 유저 회원가입/로그인, 정보 조회/수정, 비밀번호 변경 관련 API
- 채용 목록 조회/생성, 채용 상세 조회/수정/삭제 API 
- 지원서 작성, 조회, 수정, 삭제 API
- 지원 이력 관리(관리자 전용) API
## 참고 자료
### 테이블 관계도
![stockers TableRelationship](https://user-images.githubusercontent.com/74804995/130888892-e298b03c-eb24-4fe4-bc74-59b79f9a8281.png)
### ERD
![stockers ERD](https://user-images.githubusercontent.com/74804995/130889001-ac4e9b6b-c104-4e05-8d4c-296657b52c7a.png)


## Reference
- 오픈소스 프로젝트로 누구나 어떤 목적으로든 프로젝트를 보고, 사용하고, 수정하고, 배포할 수 있습니다. 
- 관련 권한은 <a href="https://opensource.org/licenses" target="_blank">open source license</a>를 통해 적용됩니다.
