**COMMIT CONVENTION**

"type"("optional scope"): "description"

example:

- add(productdetail): 상품 목록 api                 //1st commit
- add(productdetail): 상품 캐싱 db, dao             //2nd commit
- add(productdetail): 상품 repository 및 페이징 처리  //3rd commit
- add(productdetail): ...


**TYPE**

- add: 새로운 기능 추가
- fix: 버그 수정
- docs: 문서 수정
- style: 코드 포맷팅
- chore: 빌드 스크립트 설정 변경, 패키지 매니저 수정
- test: 테스트 코드, 리팩토링 테스트 코드 추가
- refactor: 코드 리팩토링
- ci: ci 관련 스크립트 파일 수정
- merge: merge 시 사용


### git rebase 이용하여 commit message 정리
