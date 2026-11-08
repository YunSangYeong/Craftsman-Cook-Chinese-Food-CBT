# Craftsman-Cook-Chinese-Food-CBT

중식조리기능사 필기 학습용 CBT. React / TypeScript / Vite 정적 앱.

## 구현과 표준

전기기능사 앱 `b9a682ccff1b460334b78d5bfad9375b7ec4fbb6`의 화면·모델·테스트를 재사용했다. 표준 스킬은 최신 main `76b990b8720adfa85c22a0a8f699b17094aa357b`의 v1.4.0 폴더 전체를 복사했다. 원본 앱 MIT 고지를 보존했다. 계정 공통 스킬 설치를 뜻하지 않는다. 기존 저장소는 README만 있었고 AGENTS.md는 새로 연결했다.

- 실전 모의시험, 절대 종료 시각 타이머·자동 제출·답안 수정·결과/해설
- 랜덤 즉시 채점, 오답 복습, 북마크, 통계, 새로고침 이어하기
- 두 모드 답안 선택 후 Space 다음 문제, 마지막 문항 자동 제출 없음
- 학습 기준/자료 연도 선택 메뉴 없음. 상단 상시 면책 배너 없음
- JSON/CSV 로컬 등록, 중복 제거, 검증 대기·근거 입력 승인, 검색·내보내기
- 메뉴 독립 세로 스크롤, 100vh/100dvh, 작은 세로·가로 화면 휠/터치 회귀 검사
- localStorage: `Craftsman-Cook-Chinese-Food-CBT:v1`. 최근 응답 5,000개·시험 30회. 백업 다운로드와 확인 후 초기화 제공. 백업 복원 UI 없음. 손상 저장 원본 자동 덮어쓰기 방지·저장 오류 경고 유지. iframe/다른 origin/저장 차단 환경은 기록 공유를 보장하지 않는다.

## 시험 규칙: 공식 확인 대기

Q-Net 조회 시도: `https://www.q-net.or.kr/crf005.do?id=crf00503&jmCd=7912`.
현재 환경에서 `curl: (56) CONNECT tunnel failed, response 403`, HTTP 코드 000으로 원문을 읽지 못했다. URL의 응답 내용과 자격 코드도 원문 대조하지 못했다. 다른 교재나 공식 출제기준을 읽었다고 주장하지 않는다.

`src/qualification.ts`의 **학습용 잠정 설정**: 중식 재료관리, 음식조리 및 위생관리 통합 과목, 60문항·60분·4지선다·100점 만점·60점 합격·과락 없음. 미응답은 오답, 표시 점수는 소수 첫째 자리, 합격은 반올림 전 비율로 계산한다. 이 값은 공식 확인 완료 사실이 아니다. 공식 시험 규칙·과목·출제기준의 최신 원문 확인이 남아 있다. 공식 단원별 비중과 난이도 재현은 확인하지 않았다. 상세 한계는 문제은행 관리 화면에 표시한다.

## 실제 문제은행: 1,000문항

`src/data/questions.json`에 통합 과목 1,000문항. ID·정규화 본문/보기 중복 0, 검증 대기 0, 부족 0. 모두 **자체 제작·내부 검수**이며 공식/외부 전문가 검수를 뜻하지 않는다.

| 구분 | 문항 수 |
| --- | ---: |
| 원문 기출 | 0 |
| 복원 | 0 |
| 자체 제작 개념형 | 60 |
| 자체 제작 숫자 조건 변형 | 940 |
| 합계 | 1,000 |

계산 유형은 질량 변환, 부피 변환, 가식부 수율, 인원별 필요량, 배합 확대, 소금물 질량 백분율, 손질 손실량, 인분당 재료비, 탄수화물 에너지, 지방 에너지의 **10유형 × 94조건**이다. 독립 개념 1,000개나 기출 1,000개가 아니다. 이 구성은 기초 개념·계산 연습에 치우쳐 있어 공식 시험 전 범위의 충분한 문제은행으로 간주할 수 없다.

AI 일반 조리 지식으로 작성했다. 외부 문제 사이트를 복제하지 않았다. 연도·회차는 모두 null. 저장소 URL은 작성 위치이며 외부 정답 근거가 아니다. 개념형은 본문·정답·오답·해설 내부 대조 및 의미 중복 검토(고기 결 관련 유사 원고 1개 교체)를 했다. 계산은 Python Decimal 생성, TypeScript 별도 역산·단위·보기·해설 결과 대조를 수행한다. 전문가의 독립적인 문장·개념 검수와 공식 출제기준 대조는 미완료다. 법령 수치를 확인 없이 만들지 않았다. 모든 신규 문항은 CC BY 4.0, 저작자 표시는 중식조리기능사 CBT 프로젝트. 외부 문항을 가져올 경우 이용 권한을 별도 확인해야 한다.

시험은 60개 고유 ID를 추출한다. 기본 은행에서는 계산 family를 한 번만 출제한다. 가져온 은행의 독립 family가 부족하면 미선정 고유 ID로 보충한다. 계산 변형을 94개 독립 유형으로 취급하지 않는다.

## 개발

Node >=22.12, 고정 런타임 `.node-version` 24.19.0. 현재 검증 머신 Node 24.22.1, npm 11.9.0, Python 3.

```sh
npm ci --cache /tmp/cbt-npm-cache
npm run dev
npm test
npm run build
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npx playwright test
# Chromium 미설치 환경: npx playwright install --with-deps chromium
```

재생성: `python scripts/author-bank.py` 다음 `python scripts/calculation-bank.py`.
후자는 계산형을 교체하며 동일 ID·순서·내용을 재현한다. 개념형 생성만 실행하면 60문항이므로 두 명령을 함께 실행한다. 테스트도 재생성 동일성을 검사한다. 테스트는 Python 3가 필요하다.

## 배포 상태

main push → 검증 → GitHub Pages 자동 배포, PR은 검증만 수행하도록 원본 workflow를 구성했다. 공개 요청은 받았지만 사전 확인의 첫 명령
`gh api repos/YunSangYeong/Craftsman-Cook-Chinese-Food-CBT --jq '{permissions,default_branch,has_pages}'`가
`Get "https://api.github.com/repos/YunSangYeong/Craftsman-Cook-Chinese-Food-CBT": Forbidden`을 반환했다.

요청한 첫 차단 중단 정책에 따라 main 푸시, workflow 수동 실행, 대체 경로 배포 및 재시도는 하지 않는다. CI/Pages 미실행, 기존 게시 여부 미확인. 배포 성공·공개 화면 확인을 주장하지 않는다. 소스 보존은 자동 배포가 없는 별도 브랜치만 사용한다.

예상 기본 주소(게시 확인 아님): https://YunSangYeong.github.io/Craftsman-Cook-Chinese-Food-CBT/
사용자가 다음으로 할 최소 동작: 클라우드 환경 설정에서 **인터넷 허용 도메인에 `api.github.com`이 포함되는지 확인**한다. 현재 적용된 허용 목록에는 이 도메인이 없다. API의 Forbidden만으로 GitHub 권한 부족 또는 Pages 미설정이라고 단정하지 않는다. 본 에이전트는 재시도하지 않으며 이후 배포는 사용자가 마무리한다.

검증 결과와 미실행 범위는 [검증 기록](docs/validation.md)을 참고한다.
