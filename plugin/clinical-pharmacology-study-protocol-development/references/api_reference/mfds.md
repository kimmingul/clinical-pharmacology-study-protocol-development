# MFDS 의약품안전나라 — 임상시험 승인현황 조회 (searchClinic)

식품의약품안전처(MFDS)가 운영하는 의약품안전나라의 임상시험 승인현황 검색 페이지(`/searchClinic`)를 **WebFetch/curl 기반 HTML 크롤링**으로 조회한다. 공식 OpenAPI(`data.go.kr`)는 `serviceKey` 발급이 필요하지만, 본 경로는 인증 없이 즉시 사용 가능하다.

> **2026-04-14 리버스엔지니어링 재검증 완료**. 이전 레시피의 `searchType` 코드 매핑 오류와 hidden 날짜 파라미터 누락이 수정되었다. 실제 검색 결과 수신 확인됨.

## 기본 정보

| 항목 | 내용 |
|------|------|
| URL | `https://nedrug.mfds.go.kr/searchClinic` |
| HTTP 메서드 | GET |
| 인증 | **불필요** (stateless, 세션 쿠키는 선택) |
| 응답 형식 | **서버 렌더링 HTML** (AJAX/JSON 아님 — `<tbody>`에 결과 행이 직접 삽입됨) |
| 언어 | 한국어 (시험 제목은 영문 병기되는 경우 있음) |
| 페이지당 건수 | **10건** |
| 최대 날짜 범위 | **3년 (1096일)** — 초과 시 서버 alert로 차단 |
| Rate Limit | 명시 없음 (상식적 요청 간격 권장) |

## 쿼리 파라미터 — 완전 세트 (실측 기반)

### 반드시 함께 전송해야 하는 파라미터 (필수)

| 파라미터 | 설명 | 타입 | 비고 |
|---------|------|------|------|
| `page` | 페이지 번호 | hidden | `1`부터 시작 |
| `searchYn` | 검색 실행 플래그 | hidden | `true` (첫 검색) 또는 공백 (페이지 이동) |
| **`approvalStart`** | 승인일 시작 (**실제 DB 쿼리용**) | hidden | `YYYY-MM-DD` — **핵심** |
| **`approvalEnd`** | 승인일 종료 (**실제 DB 쿼리용**) | hidden | `YYYY-MM-DD` — **핵심** |
| `approvalDtStart` | 승인일 시작 (UI date picker) | visible | `YYYY-MM-DD` — `approvalStart`와 같은 값 |
| `approvalDtEnd` | 승인일 종료 (UI date picker) | visible | `YYYY-MM-DD` — `approvalEnd`와 같은 값 |
| `searchType` | 검색 대상 유형 | select | **아래 표 참조** |
| `searchKeyword` | 검색어 | text | (빈 문자열이면 전체) |
| `localList` | 실시기관 지역 | select | `000` (전체) 기본 |

> ⚠️ **가장 빈번한 오류**: `approvalStart`/`approvalEnd` (hidden)와 `approvalDtStart`/`approvalDtEnd` (UI) 둘 다 전송해야 한다. **hidden 쪽이 실제 DB 쿼리에 사용**되고 이것만 전송되지 않으면 모든 검색이 "총 0건"으로 반환된다. 과거 레시피 결함의 근본 원인.

### searchType 코드 — 실측 매핑 (★)

```
ST1 = 의뢰자 (기본 선택)
ST2 = 제품명
ST3 = 임상시험 제목
ST4 = 실시기관
```

> ⚠️ 이전 레시피는 `ST1=제품명, ST3=시험제목, ST4=의뢰자, ST5=실시기관`으로 **전부 틀림**. 2026-04-14 HTML `<select>` 옵션 직접 파싱으로 정정됨.

### 선택 파라미터 (필터)

| 파라미터 | 설명 | 값 |
|---------|------|------|
| `clinicStepCode` | 임상 단계 | 빈 문자열(전체) / `0`(0상) / `1`(1상) / `2`(2상) / `3`(3상) / `4`(4상) / `5`(1/2상) / `6`(1/2a상) / `7`(1/3상) / `8`(2/3상) / … |
| `examFinish` | 종료 여부 | 빈 문자열(전체) / 모집중·진행중·종료 세분값 |
| `domestic` | 국내외 구분 | 빈 문자열(전체) |
| `gender` | 성별 | 빈 문자열(전체) |
| `age` | 연령 | 빈 문자열(전체) |
| `localList2` | 세부 실시기관 지역 | 빈 문자열(전체) |
| `notSearchKeyword` | 결과 내 제외 검색어 | 빈 문자열 |

## 키워드 선택 가이드 (실측)

| searchType | 권장 키워드 언어 | 예시 (3년 범위 결과) |
|-----------|----------------|--------------------|
| ST1 (의뢰자) | **한국어**. 국내 제약사 공식 한글명 | `한미약품` → 17건, `Pfizer` → 0건 (한글 "화이자" 필요) |
| ST2 (제품명) | **한국어**. 국내 제품은 한글 상품명 또는 한글 성분명 | `클로피도그렐` → 7건, `플라빅스` → 3건, `clopidogrel` → 0건 |
| ST3 (시험제목) | **한국어 우선, 영문도 일부 매칭** (시험명에 영문 약물명 병기되는 경우) | `클로피도그렐` → 8건, `clopidogrel` → 3건 |
| ST4 (실시기관) | **한국어**. 기관 공식 한글명 | `서울대학교병원` → 1,142건 |

**실무 권고**: 국내 규제 검색에서는 **한글 키워드를 기본으로 사용**하고, 보완적으로 영문도 시도한다. ST3(시험제목)은 상대적으로 관대하므로 1차 스캔에 유용.

## 3년 범위 제한 + 반복 검색 전략 (★)

서버는 `approvalStart`–`approvalEnd` 간격이 **1096일(3년+1일) 이하**만 허용한다. 3년 이상의 기간을 조사하려면 **중복 없이 구간을 분할**하여 여러 번 호출한다.

### 표준 분할 예시 (과거 9년 조사)

```
구간 1: 2017-04-15 ~ 2020-04-14  (3년)
구간 2: 2020-04-15 ~ 2023-04-14  (3년)
구간 3: 2023-04-15 ~ 2026-04-14  (3년, 최신)
```

- 각 구간은 **1일 겹치지 않도록** 시작일을 전 구간 종료일 +1일로 설정
- 결과는 중복되지 않으므로 단순 합산 가능
- 각 구간의 페이지네이션을 끝까지 돈 뒤 다음 구간으로 이동

### 반복 검색 의사코드

```python
def search_mfds_full_history(drug_name, start_year, end_year, search_type="ST3"):
    all_rows = []
    today = "YYYY-MM-DD"  # 동적으로
    chunks = []
    cur = start_year
    while cur < end_year:
        chunk_end_year = min(cur + 3, end_year)
        chunks.append((f"{cur}-01-01", f"{chunk_end_year-1}-12-31"))
        cur = chunk_end_year
    for s, e in chunks:
        page = 1
        while True:
            rows = fetch_page(drug_name, s, e, search_type, page)
            if not rows: break
            all_rows.extend(rows)
            if len(rows) < 10: break  # 마지막 페이지
            page += 1
    return all_rows
```

## curl 검증 예시 (실제 작동)

### 예시 1: 제품명으로 클로피도그렐 최근 3년

```bash
curl -sS -A "Mozilla/5.0" -H "Referer: https://nedrug.mfds.go.kr/searchClinic" --get \
  --data-urlencode "page=1" \
  --data-urlencode "searchYn=true" \
  --data-urlencode "approvalStart=2023-04-15" \
  --data-urlencode "approvalEnd=2026-04-14" \
  --data-urlencode "searchType=ST2" \
  --data-urlencode "searchKeyword=클로피도그렐" \
  --data-urlencode "approvalDtStart=2023-04-15" \
  --data-urlencode "approvalDtEnd=2026-04-14" \
  --data-urlencode "localList=000" \
  "https://nedrug.mfds.go.kr/searchClinic"
```

응답에서 `총 <strong>7</strong> 건` 확인.

### 예시 2: 시험명으로 Clopidogrel (영문) 최근 3년

```bash
# searchType=ST3, searchKeyword=clopidogrel → 3건 반환 (시험명에 영문 약물명 병기된 것만)
```

### 예시 3: 페이지 2 이동 (의뢰자 한미약품, 10건 초과 건)

```bash
curl -sS ... \
  --data-urlencode "page=2" \
  --data-urlencode "searchYn=" \  # 페이지 이동 시 빈 값
  --data-urlencode "searchType=ST1" \
  --data-urlencode "searchKeyword=한미약품" \
  ...
```

> 참고: 첫 검색은 `searchYn=true`, 이후 페이지 이동은 `searchYn=` (빈 값). 실제로는 `searchYn=true`로 계속 보내도 작동 확인됨(호환성 여유).

## WebFetch 레시피

### 레시피 A: 특정 약물 국내 승인 임상 조회 (3년)

```
WebFetch(
  url="https://nedrug.mfds.go.kr/searchClinic?page=1&searchYn=true&approvalStart=2023-04-15&approvalEnd=2026-04-14&searchType=ST2&searchKeyword=클로피도그렐&approvalDtStart=2023-04-15&approvalDtEnd=2026-04-14&localList=000",
  prompt="총 건수('총 N건') 추출. <tbody> 내 각 <tr>에서 시험 제목(첫 <a> 태그 텍스트), 의뢰자, 승인일, 임상 단계, 실시기관을 표로 정리. <a> href 파라미터에서 clinicExamNo, receiptNo, approvalDt, clinicExamSeq도 함께 추출"
)
```

### 레시피 B: 의뢰자 기준 파이프라인 조회 (3년)

```
WebFetch(
  url="https://nedrug.mfds.go.kr/searchClinic?page=1&searchYn=true&approvalStart=2023-04-15&approvalEnd=2026-04-14&searchType=ST1&searchKeyword=한미약품&approvalDtStart=2023-04-15&approvalDtEnd=2026-04-14&localList=000",
  prompt="의뢰자 '한미약품'의 최근 3년 국내 승인 임상시험 목록. 시험명·제품명·단계·승인일·실시기관 추출"
)
```

### 레시피 C: 장기간 조사 (최근 9년 = 3구간 반복)

메인 에이전트가 3번 WebFetch 호출하여 결과 병합:

```
# 구간 1 (2017-04-15 ~ 2020-04-14)
WebFetch(url="...&approvalStart=2017-04-15&approvalEnd=2020-04-14&...", prompt="...")

# 구간 2 (2020-04-15 ~ 2023-04-14)
WebFetch(url="...&approvalStart=2020-04-15&approvalEnd=2023-04-14&...", prompt="...")

# 구간 3 (2023-04-15 ~ 2026-04-14)
WebFetch(url="...&approvalStart=2023-04-15&approvalEnd=2026-04-14&...", prompt="...")
```

각 구간에서 페이지당 10건 초과 시 page=2, 3, … 반복.

## HTML 파싱 힌트 (실측 구조)

### 총 건수 위치
```html
<p ... title="총 7건">총 <strong>7</strong> 건</p>
```
→ 정규식: `총\s*<strong>\s*([0-9,]+)\s*</strong>\s*건`

### 결과 테이블 구조
```html
<tbody>
  <tr>
    <td>번호</td>
    <td><a href="/pbp/CCBBC01/nexacroPageOpen?...clinicExamSeq=202500754&clinicExamNo=102926&receiptNo=20250148830&approvalDt=2025-10-02...">
      시험 제목 (한글)
    </a></td>
    <td>제품명</td>
    <td>임상 단계</td>
    <td>승인일</td>
    <td>의뢰자</td>
    <td>실시기관</td>
    ...
  </tr>
  ...
</tbody>
```

### 결과 0건 표시
```html
<tbody>
  <tr><td colspan="9">조회 결과가 없습니다.</td></tr>
</tbody>
```

### 상세 페이지 URL (추출 가능 메타데이터)
각 시험의 첫 `<a>` href에서 쿼리 파라미터로 다음 메타데이터 추출:
- `clinicExamSeq`: 내부 시험 식별 번호 (예: `202500754`)
- `clinicExamNo`: 공식 임상시험 번호 (예: `102926`)
- `receiptNo`: 접수번호
- `approvalDt`: 승인일자 (YYYY-MM-DD)
- 기존 검색 조건이 모두 복제되어 포함됨

## 산출물 저장 형식

`_workspace/01_references/mfds_clinical_trials/{search_topic}_approval_list.md`:

```markdown
# MFDS 국내 임상시험 승인현황 — {검색 주제}

## 조회 정보
- 검색일: YYYY-MM-DD
- 출처: https://nedrug.mfds.go.kr/searchClinic
- 검색 파라미터:
  - 검색 유형: {ST1/ST2/ST3/ST4}
  - 검색어: {keyword}
  - 승인 기간: {start} ~ {end} (구간 분할한 경우 각각 명시)
- 총 건수: {N}건 (구간별 합산)

## 결과 테이블

| # | clinicExamNo | 시험명 | 제품명 | 의뢰자 | 단계 | 실시기관 | 승인일 |
|---|-------------|-------|-------|-------|------|---------|-------|
| 1 | 102926 | ... | ... | ... | ... | ... | 2025-10-02 |
| ... |

## 주요 관찰 사항
- 연도별 승인 빈도
- 주요 의뢰자 (상위 5개)
- 임상 단계 분포
- 본 시험 설계에의 시사점
```

## Gotchas

- **3년 제한 초과 요청**: 서버가 `alert("승인일자는 최대 3년까지만 가능합니다.")`를 발생시키고 검색을 차단. JS 검증이지만 서버도 동일 규칙 적용 추정. 1096일 이내로 구간 분할 필수
- **한글 URL 인코딩**: `--data-urlencode`가 자동 처리. URL에 직접 한글을 쓰는 경우 %EA%B3%A0 같은 UTF-8 퍼센트 인코딩 필수
- **영문 키워드의 낮은 매칭률**: 국내 허가 제품은 한글 성분명·상품명으로 등록. 영문은 시험 제목에만 일부 병기. 한글 우선 권장
- **ST 코드 암묵적 매핑**: MFDS가 공식 문서화하지 않음. 본 레시피는 HTML `<select>` 옵션 파싱 기반. 의약품안전나라 UI 개편 시 재검증 필요
- **페이지당 10건 고정**: `pageUnit` 같은 파라미터로 변경 시도했으나 무시됨. 10건 × N 페이지 반복만 가능
- **승인일자 공란 불허**: `approvalStart`/`approvalEnd` 둘 다 필수. 한쪽만 비우면 0건 반환
- **검색 후 정렬**: 기본 승인일 역순(최신). 정렬 파라미터는 확인되지 않음
- **UI 개편 리스크**: 의약품안전나라는 주기적으로 개편됨. HTML 구조 변경 시 `searchType` 매핑과 hidden 필드 이름 재검증 필요 (`<form id="searchForm">` 내부 `<input name=...>` 목록과 `<select>` `<option>` 직접 파싱)

## 상세 페이지 크롤링 — Nexacro SOAP 직접 호출 (★ 완전 가능)

검색 결과 리스트의 각 시험 항목 `<a>` href는 다음과 같다:

```
/pbp/CCBBC01/nexacroPageOpen?...&clinicExamSeq=202600092&clinicExamNo=103126&receiptNo=20250200086&approvalDt=2026-02-05
```

상세 페이지는 **Nexacro Platform** 기반 SPA(iframe + xfdl)이지만, **Nexacro의 SOAP transaction endpoint를 HTTP POST로 직접 호출하면 XML 응답을 받을 수 있다**. 헤드리스 브라우저 불필요.

### 상세 페이지 구조 (실측, 참고용)

```
/pbp/CCBBC01/nexacroPageOpen  (HTML wrapper, 81 KB)
  └─ <iframe id="frmnxa" src="/NEXACRO/launch.html?formpath=CCAAK02F010">
      └─ Nexacro17 runtime → CCAAK02F010.xfdl (Master, 2개 탭)
          ├─ Tab 1 "임상시험계획"  → CCAAK02F010_PLAN.xfdl (또는 _PLAN_ORI.xfdl)
          └─ Tab 2 "임상시험결과"  → CCAAK02F010_RESULT.xfdl
```

### SOAP 호출 형식 (★ 표준 패턴)

| 항목 | 값 |
|------|---|
| Method | **POST** |
| Base URL | `https://nedrug.mfds.go.kr/` |
| Path | xfdl의 `var sUrl = "..."` 값을 그대로 (예: `ext/CCAAK02F010/clinicExamPlanReport`) |
| Content-Type | `text/xml; charset=UTF-8` |
| Body | Nexacro 표준 XML (아래 템플릿) |
| 응답 Content-Type | `text/xml` |
| 응답 형식 | Nexacro 표준 XML — `<Root xmlns="http://www.nexacroplatform.com/platform/dataset">` |
| 인증 | **불필요** (검색 리스트와 동일, 세션 쿠키 선택) |

### 요청 Body 템플릿

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Root xmlns="http://www.nexacroplatform.com/platform/dataset">
  <Parameters>
    <Parameter id="clinicExamSeq">{clinicExamSeq}</Parameter>
    <Parameter id="clinicExamNo">{clinicExamNo}</Parameter>
    <!-- 추가 파라미터 (mode, receiptNo 등) endpoint별 차이 -->
  </Parameters>
</Root>
```

### 응답 구조 (실측)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Root xmlns="http://www.nexacroplatform.com/platform/dataset">
  <Parameters>
    <Parameter id="ErrorCode" type="int">0</Parameter>  <!-- 0이면 성공 -->
  </Parameters>
  <Dataset id="datasetName1">
    <ColumnInfo>
      <Column id="colName" type="string" size="32"/>
      ...
    </ColumnInfo>
    <Rows>
      <Row>
        <Col id="colName">value</Col>
        ...
      </Row>
      ...
    </Rows>
  </Dataset>
  <Dataset id="datasetName2">...</Dataset>
  ...
</Root>
```

> **Whitespace 인코딩 주의**: 한글 텍스트 안 공백이 `&#32;`(HTML entity)로 인코딩됨. 파싱 시 `html.unescape()` 또는 단순 `replace("&#32;", " ")` 처리 필요. 줄바꿈은 `&#10;`.

### 탭별 endpoint 매핑 (실증 완료 — 모두 HTTP 200 검증)

| Tab | Endpoint (POST) | 추가 파라미터 | 응답 데이터셋 (실측) |
|-----|----------------|--------------|------------------|
| 공통 | `/ext/CCAAK02F010/clinicExamOpenChk` | — | `planOpenChk`, `resultOpenChk` (공개 여부: OP02=공개) |
| **Tab1 PLAN** | `/ext/CCAAK02F010/clinicExamPlanReport` | (mode 생략 = 계획) | `clinicExamPlanReport` (시험 메타), **`chooseEx1List` (선정 기준)**, **`chooseEx2List` (제외 기준)**, `compDrugList` (시험약), `clinicStudyList`, `materialList`, `forgeryList`, `formCodeList` |
| **Tab1 PLAN** | `/ext/CCAAJ01F010/clinicExamOpenItem` | `receiptNo`, `mode=CCAAK02F010_PLAN` | `clinicExamOpenInfo` (공개 항목 메타) |
| **Tab1 PLAN** | `/ext/CCAAJ01F010/clinicExamTermList` | (없음) | `clinicExamTermList` (용어 사전) |
| **Tab2 RESULT** | `/ext/CCAAK02F010/clinicExamPlanReport` | **`mode=RESULT_INFO`** | `clinicExamPlanReport`, `resultDetail` (결과 본문) |
| **Tab2 RESULT** | `/ext/CCAAK01F010/comCodeDetail` | `classCode`, `likeCodeNo` | (공통 코드 lookup) |

> **핵심 입력 키**: `clinicExamSeq` + `clinicExamNo` (모든 endpoint 공통). 검색 리스트의 `<a>` href URL 쿼리에서 그대로 추출.

### 완전한 curl 예시 (실증)

```bash
# Tab 1 — 임상시험계획 본문 (선정/제외 기준, 시험약 등 8개 dataset)
cat > /tmp/payload.xml <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<Root xmlns="http://www.nexacroplatform.com/platform/dataset">
  <Parameters>
    <Parameter id="clinicExamSeq">202600092</Parameter>
    <Parameter id="clinicExamNo">103126</Parameter>
  </Parameters>
</Root>
EOF

curl -sS -A "Mozilla/5.0" \
  -H "Referer: https://nedrug.mfds.go.kr/" \
  -H "Content-Type: text/xml; charset=UTF-8" \
  -X POST --data-binary @/tmp/payload.xml \
  "https://nedrug.mfds.go.kr/ext/CCAAK02F010/clinicExamPlanReport"

# Tab 2 — 임상시험결과 본문
# 동일 endpoint, mode=RESULT_INFO 추가
```

응답 32 KB XML → 8개 dataset → 하나의 시험에 대한 한국어 본문 전체 확보.

### 파이썬 파싱 예시

```python
import requests
import xml.etree.ElementTree as ET
import html

NS = {"nx": "http://www.nexacroplatform.com/platform/dataset"}

def fetch_clinic_detail(clinic_exam_seq, clinic_exam_no, receipt_no, *, mode=None):
    """단일 시험의 모든 탭 데이터를 dict로 반환."""
    base = "https://nedrug.mfds.go.kr"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://nedrug.mfds.go.kr/",
        "Content-Type": "text/xml; charset=UTF-8",
    }

    def call(path, params):
        param_xml = "".join(
            f'<Parameter id="{k}">{v}</Parameter>' for k, v in params.items()
        )
        body = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Root xmlns="http://www.nexacroplatform.com/platform/dataset">'
            f'<Parameters>{param_xml}</Parameters>'
            '</Root>'
        )
        r = requests.post(f"{base}/{path}", data=body.encode("utf-8"), headers=headers)
        r.raise_for_status()
        return parse_nexacro(r.text)

    common = {"clinicExamSeq": clinic_exam_seq, "clinicExamNo": clinic_exam_no}
    return {
        "openChk": call("ext/CCAAK02F010/clinicExamOpenChk", common),
        "plan":    call("ext/CCAAK02F010/clinicExamPlanReport", common),
        "openItem": call("ext/CCAAJ01F010/clinicExamOpenItem",
                         {**common, "receiptNo": receipt_no, "mode": "CCAAK02F010_PLAN"}),
        "result":  call("ext/CCAAK02F010/clinicExamPlanReport",
                        {**common, "mode": "RESULT_INFO"}),
    }


def parse_nexacro(xml_text: str) -> dict:
    """Nexacro 응답 XML → {dataset_id: [row_dict, ...]}."""
    root = ET.fromstring(xml_text)
    out = {"errorCode": None, "datasets": {}}
    for p in root.findall("nx:Parameters/nx:Parameter", NS):
        if p.get("id") == "ErrorCode":
            out["errorCode"] = int(p.text or 0)
    for ds in root.findall("nx:Dataset", NS):
        ds_id = ds.get("id")
        rows = []
        for row in ds.findall("nx:Rows/nx:Row", NS):
            rows.append({
                col.get("id"): html.unescape((col.text or "").replace("&#32;", " "))
                for col in row.findall("nx:Col", NS)
            })
        out["datasets"][ds_id] = rows
    return out
```

### 검색 리스트 → 상세 자동 follow 전략

검색 결과 리스트의 각 행에서 추출한 `clinicExamSeq`, `clinicExamNo`, `receiptNo`를 그대로 사용하여 위 4개 endpoint를 호출. N건 리스트 → 최대 N × 4 SOAP 호출.

### 산출물 저장 형식 (확장)

`_workspace/01_references/mfds_clinical_trials/{topic}/`:

```
{topic}/
├── _list.md                  # 검색 리스트 요약
├── {clinicExamNo}_plan.md    # 시험별 — Tab 1 본문 (선정/제외, 시험약, 평가변수)
├── {clinicExamNo}_result.md  # 시험별 — Tab 2 결과 본문
└── ...
```

### 운영상 권고

- **호출량 제한**: N건 리스트 × 4 endpoint = 큰 호출량. 1회 조사 N ≤ 30 권장. 초과 시 `data.go.kr` OpenAPI(§5)로 전환
- **세션 쿠키**: 첫 GET `/searchClinic`로 받은 `JSESSIONID` 재사용 권장 (필수는 아님, 안정성 보강)
- **에러 처리**: `<Parameter id="ErrorCode" type="int">0</Parameter>`만 신뢰. ErrorCode≠0이면 응답 dataset 무시하고 재시도
- **HTML entity 디코딩**: 한글 결과의 공백·줄바꿈을 반드시 unescape
- **xfdl 구조 변경 리스크**: MFDS UI 개편 시 service URL 또는 dataset 스키마 변경 가능. `/NEXACRO/Work/Ext/Apr/ccaak02/CCAAK02F010_PLAN.xfdl.js` 등을 GET하여 `var sUrl = "..."` 패턴 재추출 필요

### 크롤링 가능성 매트릭스 (최종)

| 방법 | 가능 여부 | 권고 |
|------|---------|------|
| 검색 결과 리스트 HTTP 크롤링 | ✅ | **메인 경로** |
| **상세 페이지 SOAP 직접 호출** | ✅ **완전 가능 (실증)** | **★ 권장 — 헤드리스 브라우저 불필요** |
| 헤드리스 브라우저 (Playwright) | ✅ | 폴백 (xfdl/endpoint 변경 시) |
| data.go.kr OpenAPI (`15056835`) | ✅ | 대량 조사·공식 인용용 (§5) |

## 폴백 전략

- **장기간·대량 조사 시**: `data.go.kr` OpenAPI (serviceKey 발급, 10,000 req/day 개발계정) 검토 — `TODO.md §5`
- **상세 정보 필요 시**: (1) 헤드리스 브라우저 별도 환경 구축 또는 (2) data.go.kr OpenAPI 우선 — 본 레시피의 SOAP 호출 직접 구현은 권장하지 않음
- **HTML 구조 변경으로 파싱 실패**: 상단 "2026-04-14 검증" 기준으로 재확인. ST 코드 실제 option 값은 `/searchClinic` 첫 페이지 로드 후 `<select name="searchType">` `<option>` 직접 추출
- **국제 데이터 교차 확인**: ClinicalTrials.gov API v2에서 `query.locn="South Korea"` + `query.intr={drug}` 검색

## 참고 링크

- 검색 페이지: https://nedrug.mfds.go.kr/searchClinic
- 공공데이터 포털 MFDS 임상시험 API: https://www.data.go.kr/data/15056835/openapi.do
- 의약품안전나라 메인: https://nedrug.mfds.go.kr/

## 변경 이력

| 날짜 | 변경 내용 |
|------|----------|
| 2026-04-14 | **전면 재작성**: ST 코드 매핑 정정(ST1 의뢰자 / ST2 제품명 / ST3 시험제목 / ST4 실시기관), hidden 날짜 파라미터(`approvalStart`/`approvalEnd`)와 UI 파라미터(`approvalDtStart`/`approvalDtEnd`) 구분, 3년 제한 + 반복 검색 전략 추가, 페이지당 10건 확인, 실측 예시·파싱 힌트 전면 갱신. 이전 버전의 ST 매핑·파라미터 누락 결함을 완전 해결. |
| 2026-04-14 | **상세 페이지 분석 추가**: `nexacroPageOpen`이 Nexacro Platform 기반 SPA로 iframe + xfdl + SOAP transaction 구조. Master xfdl `CCAAK02F010.xfdl`이 2개 탭("임상시험계획", "임상시험결과")을 가지며 각각 별도 xfdl(`_PLAN.xfdl`, `_PLAN_ORI.xfdl`, `_RESULT.xfdl`)에서 transaction 호출. 6개 service URL 식별(`clinicExamPlanReport`, `clinicExamOpenChk`, `clinicExamOpenItem`, `clinicExamTermList`, `comCodeDetail`). 결론: HTTP 크롤링은 검색 리스트까지만 가능, 상세는 헤드리스 브라우저 또는 data.go.kr OpenAPI 필요. |
