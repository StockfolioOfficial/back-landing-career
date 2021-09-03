##BRANCH ROLE
“브랜치이름” “/” “기능범위” “-” “설명”
master/ develop/ feature/ hotfix/ refactoring
###예시:
feat/docs-convention
refactoring/aws-s3
refactoring/error-handling
feat/application-search  

##COMMIT CONVENTION
“이슈번호” “타입” “(작업하는 부분)“: “설명”
###예시:
\#1 add(application admin view): 상품 목록 api 
\#2 edit(loginview): 로그아웃 유지되도록 처리
\#41 feat(my_settings): 외부에서 시크릿 설정 주입하는 부분 추가
\#96 docs(contributor) : 커밋 컨벤션

###TYPE
add: 새로운 기능 추가
update: 기능 부분 업데이트
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
chore: 빌드 스크립트 설정 변경, 패키지 매니저 수정
test: 테스트 코드, 리팩토링 테스트 코드 추가
refactor: 코드 리팩토링
ci: ci 관련 스크립트 파일 수정
merge: merge 시 사용 (edited)#