# MFDS 의약품안전나라 — 임상시험 승인현황 조회 (searchClinic)

식품의약품안전처(MFDS)가 운영하는 의약품안전나라의 임상시험 승인현황 검색 페이지를 **WebFetch로 직접 조회**하는 방법. 공식 OpenAPI(`data.go.kr`)는 `serviceKey` 발급이 필요하지만, 본 경로는 인증 없이 즉시 사용 가능하다.

## 기본 정보

| 항목 | 내용 |
|------|------|
| URL | `https://nedrug.mfds.go.kr/searchClinic` |
| HTTP 메서드 | GET |
| 인증 | **불필요** (stateless, 세션/쿠키/CSRF 토큰 없음) |
| 응답 형식 | 서버 렌더링 **HTML** (AJAX/JSON 아님) |
| 언어 | 한국어 (시험 제목은 영문 병기되는 경우 있음) |
| Rate Limit | 명시 없음 (과도한 호출 시 차단 가능성, 상식적 요청 간격 권장) |
| robots.txt | 공개 검색 페이지이지만, 대량 조사 시에는 data.go.kr OpenAPI 경로 권장 (TODO.md 참조) |

## 쿼리 파라미터

### 주요 파라미터

| 파라미터 | 설명 | 예시 값 |
|---------|------|--------|
| `searchYn` | 검색 실행 플래그 | `true` (필수) |
| `page` | 페이지 번호 | `1` |
| `searchType` | 검색 대상 유형 | `ST3` (시험 제목), `ST1` (제품명), `ST4` (의뢰자), `ST5` (실시기관) |
| `searchKeyword` | 검색어 | (빈 문자열이면 전체) |
| `approvalDtStart` | 승인일 시작 | `YYYY-MM-DD` |
| `approvalDtEnd` | 승인일 종료 | `YYYY-MM-DD` |
| `clinicStepCode` | 임상 단계 | (공란이면 전체; 1/2/3/4상 등) |
| `domestic` | 국내외 | (공란이면 전체) |
| `gender` | 성별 | (공란이면 전체) |
| `age` | 연령 | (공란이면 전체) |
| `localList` | 지역 코드 | `000` (전체) |
| `localList2` | 세부 지역 | (공란이면 전체) |
| `examFinish` | 종료 여부 | (공란이면 전체) |

### 예시 URL

**전체 조회 (최근 승인):**
```
https://nedrug.mfds.go.kr/searchClinic?searchYn=true&page=1&approvalDtStart=2024-01-01&approvalDtEnd=2024-12-31&localList=000
```

**특정 약물명 검색:**
```
https://nedrug.mfds.go.kr/searchClinic?searchYn=true&page=1&searchType=ST1&searchKeyword=메트포르민
```

**의뢰자별 검색:**
```
https://nedrug.mfds.go.kr/searchClinic?searchYn=true&page=1&searchType=ST4&searchKeyword=한국아이큐비아
```

## WebFetch 쿼리 레시피

### 레시피 A: 특정 약물의 국내 승인 임상 조회

```
WebFetch(
  url="https://nedrug.mfds.go.kr/searchClinic?searchYn=true&page=1&searchType=ST1&searchKeyword={drug_name}",
  prompt="HTML 응답에서 총 검색 건수('총 N건') 추출. 결과 테이블에서 각 시험의 제목, 의뢰자, 승인일, 임상 단계, 실시기관, 시험 상태(모집 중/종료 등)를 표로 정리"
)
```

### 레시피 B: 최근 1년 국내 유사 시험 동향

```
WebFetch(
  url="https://nedrug.mfds.go.kr/searchClinic?searchYn=true&page=1&approvalDtStart=2024-01-01&approvalDtEnd=2024-12-31&searchType=ST3&searchKeyword={질환명 or MOA}",
  prompt="최근 승인된 유사 시험의 연도별 빈도, 주요 의뢰자, 가장 흔한 임상 단계를 요약"
)
```

### 레시피 C: 특정 의뢰자의 파이프라인 확인

```
WebFetch(
  url="https://nedrug.mfds.go.kr/searchClinic?searchYn=true&page=1&searchType=ST4&searchKeyword={sponsor_name}&approvalDtStart=2023-01-01&approvalDtEnd=2024-12-31",
  prompt="해당 의뢰자의 최근 2년간 임상시험 승인 목록. 시험명·약물·단계·승인일 추출"
)
```

## HTML 파싱 힌트

`searchClinic` 응답 HTML에서 다음 요소 주변을 탐색:

| 추출 대상 | HTML 위치·키워드 |
|---------|-----------------|
| 총 건수 | 페이지 상단 "총 **N**건" 텍스트 |
| 각 시험 제목 | 결과 테이블 첫 번째 컬럼 (일반적으로 `<a>` 태그 내부) |
| 의뢰자 | 결과 테이블의 "의뢰자" 컬럼 |
| 승인일 | "승인일자" 또는 "승인일" 컬럼 (YYYY-MM-DD) |
| 임상 단계 | "단계" 컬럼 (1상/2상/3상/4상/생동성 등) |
| 실시기관 | "실시기관" 컬럼 |
| 페이지네이션 | 하단 페이지 번호 링크 (`page` 파라미터 증가) |

## 산출물 저장 형식

`_workspace/01_references/mfds_clinical_trials/{search_topic}_approval_list.md`:

```markdown
# MFDS 국내 임상시험 승인현황 — {검색 주제}

## 조회 정보
- 검색일: YYYY-MM-DD
- 출처: https://nedrug.mfds.go.kr/searchClinic
- 검색 파라미터:
  - 검색 유형: {searchType}
  - 검색어: {keyword}
  - 기간: {start} ~ {end}
- 총 건수: {N}건

## 결과 요약 테이블

| # | 시험명 | 의뢰자 | 단계 | 실시기관 | 승인일 |
|---|-------|-------|------|---------|-------|
| 1 | ... | ... | ... | ... | ... |

## 주요 관찰 사항
- 연도별 승인 빈도: (표)
- 주요 의뢰자 (상위 5개):
- 임상 단계 분포:
- 본 시험 설계에의 시사점:
```

## Gotchas

- **HTML 구조 변경 위험**: 의약품안전나라는 UI 개편이 주기적으로 발생. HTML 파싱이 실패하면 `WebFetch prompt`를 조정하거나 `data.go.kr` OpenAPI 경로로 전환 (TODO.md 참조)
- **대량 페이지네이션**: 결과가 많으면 `page=2`, `page=3` 순차 호출 필요. WebFetch 호출이 많아지면 rate limit 주의
- **검색어 인코딩**: 한글 검색어는 URL 인코딩 필요. WebFetch가 자동 처리하나 특수문자는 수동 확인
- **승인일 범위 필수 아님**: 파라미터 생략 시 전체 기간. 단, 범위 없이 전체 조회하면 결과가 매우 많아 파싱 부담 증가
- **`searchType` 코드 비공식**: `ST1/ST3/ST4/ST5` 매핑은 리버스엔지니어링으로 파악된 것. MFDS가 코드 변경 시 재조사 필요
- **공식 통계 아님**: searchClinic은 검색 UI의 결과이며, 공식 통계는 MFDS 연간 보고서 또는 `data.go.kr` OpenAPI 기반. 계획서에 인용 시 "의약품안전나라 검색 결과 기준" 명시
- **개인정보 포함 없음**: 승인 목록은 공개 정보이나, 시험대상자·연구자 개인 정보는 포함되지 않음 (검색 결과에도 나타나지 않음)

## 폴백 전략

- **searchClinic HTML 파싱 실패 시**: WebSearch로 `site:nedrug.mfds.go.kr {drug_name}` 검색
- **더 구조화된 데이터 필요 시**: `data.go.kr`의 `15056835` OpenAPI 검토 (serviceKey 발급 필요, TODO.md 참조)
- **국제 데이터로 보완**: ClinicalTrials.gov MCP로 한국 실시 시험(`country=South Korea`) 조회

## 참고 링크

- 검색 페이지: https://nedrug.mfds.go.kr/searchClinic
- 의약품안전나라 공공데이터 목록: https://nedrug.mfds.go.kr/pbp/CCBGA01
- 공공데이터포털 MFDS 임상시험 API (정식 경로, 향후): https://www.data.go.kr/data/15056835/openapi.do
