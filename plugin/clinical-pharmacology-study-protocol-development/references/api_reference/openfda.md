# openFDA API 레퍼런스

FDA가 운영하는 공식 데이터 API. 약물 라벨·이상반응(FAERS)·허가 정보(drugsfda)·NDC·리콜을 제공. 임상시험 문서 작성 시 **허가일·NDA 번호 조회**, **FAERS 이상반응 빈도 집계**, **DailyMed 보완용 라벨 검색**에 사용한다.

## 기본 정보

| 항목 | 내용 |
|------|------|
| Base URL | `https://api.fda.gov/drug/` |
| 인증 | 선택 (API key 미등록 시 1,000 req/day, 등록 시 120,000 req/hour) |
| API Key 발급 | https://open.fda.gov/apis/authentication/ (무료, 이메일 등록만 필요) |
| Rate Limit | 무키: 240 req/min + 1,000/day; 유키: 240/min + 120,000/hour |
| 형식 | JSON |
| 문서 | https://open.fda.gov/apis/drug/ |

> **API key 사용 시**: 모든 요청 URL 끝에 `&api_key={KEY}` 추가. key가 없어도 대부분 조사는 무키로 충분.

## 주요 엔드포인트 (5개)

### 1. 약물 라벨 (`/drug/label.json`)

현재 승인 약물의 라벨 정보. DailyMed와 중복되나 **쿼리 파라미터로 정밀 검색** 가능.

```
GET /drug/label.json?search=openfda.generic_name:"metformin"&limit=1
```

**주요 검색 필드:**
- `openfda.generic_name` — 성분명 (소문자)
- `openfda.brand_name` — 브랜드명 (예: "NORVASC")
- `openfda.manufacturer_name` — 제조사
- `openfda.substance_name` — 원료명
- `openfda.product_type` — "HUMAN PRESCRIPTION DRUG"

**반환 주요 필드:**
- `results[].indications_and_usage` — 적응증
- `results[].dosage_and_administration` — 용법용량
- `results[].contraindications` — 금기
- `results[].drug_interactions` — 약물상호작용
- `results[].clinical_pharmacology` — 약동학
- `results[].clinical_studies` — 임상시험
- `results[].pharmacogenomics` — PG (있을 시)
- `results[].use_in_specific_populations` — 특수 집단
- `results[].openfda.application_number` — NDA/ANDA 번호
- `results[].openfda.nui` — Unique Ingredient Identifier

### 2. 이상반응 FAERS (`/drug/event.json`)

FDA Adverse Event Reporting System. 시판 후 이상반응 보고.

```
GET /drug/event.json?search=patient.drug.medicinalproduct:"METFORMIN"&count=patient.reaction.reactionmeddrapt.exact&limit=20
```

**예시 목적: 상위 20개 이상반응 MedDRA PT 빈도**

**주요 쿼리 패턴:**
- `search=patient.drug.medicinalproduct:"{NAME}"` — 보고 내 해당 약물 포함 여부
- `count=patient.reaction.reactionmeddrapt.exact` — MedDRA Preferred Term 집계
- `count=patient.reaction.reactionoutcome` — 결과(사망/입원 등) 집계
- `search=...AND receivedate:[20200101+TO+20241231]` — 기간 필터

**용도 제한**:
> FAERS는 **자발적 보고**이므로 인과관계 확정이 아님. 단순 "신호 탐지"에 해당. 이상반응 빈도를 라벨의 공식 빈도와 **구분**하여 해석.

### 3. NDC 정보 (`/drug/ndc.json`)

National Drug Code 정보. 제품 식별·제형·포장 정보.

```
GET /drug/ndc.json?search=generic_name:"metformin"&limit=10
```

**주요 필드:**
- `results[].product_ndc` — NDC 번호
- `results[].generic_name`, `brand_name`
- `results[].dosage_form` — 제형 (TABLET, CAPSULE 등)
- `results[].route` — 투여 경로
- `results[].marketing_category` — NDA/ANDA/OTC MONOGRAPH
- `results[].active_ingredients[].strength` — 함량

### 4. 허가 정보 (`/drug/drugsfda.json`)

FDA 승인 이력, NDA/ANDA 번호, 승인일자.

```
GET /drug/drugsfda.json?search=openfda.generic_name:"metformin"&limit=5
```

**주요 필드:**
- `results[].application_number` — NDA 번호 (예: "NDA019787")
- `results[].sponsor_name` — 신청사
- `results[].products[].marketing_status` — "Prescription" / "Discontinued"
- `results[].submissions[].submission_status_date` — 제출 상태 변경일
- `results[].submissions[].submission_type` — "ORIG-1" (초기 승인) 등

**용도**: 허가 이력·신약 승인일·브랜드 변경 추적.

### 5. 리콜 (`/drug/enforcement.json`)

리콜·시장 조치 기록.

```
GET /drug/enforcement.json?search=product_description:"metformin"+AND+status:"Ongoing"&limit=10
```

안전성 프로파일 보완, 제조 품질 이슈 확인에 사용.

## WebFetch 쿼리 레시피

### 레시피 A: 약물의 핵심 허가 정보 조회

```
WebFetch(
  url="https://api.fda.gov/drug/drugsfda.json?search=openfda.generic_name:metformin&limit=5",
  prompt="각 application_number, sponsor_name, 최초 승인일(submissions 중 submission_type='ORIG-1'의 submission_status_date), marketing_status를 추출"
)
```

### 레시피 B: PG 섹션 타겟 조회

```
WebFetch(
  url="https://api.fda.gov/drug/label.json?search=openfda.generic_name:clopidogrel&limit=1",
  prompt="results[0]의 pharmacogenomics 필드 전체와 boxed_warning 필드 전체를 추출. 추가로 dosage_and_administration에서 'CYP2C19' 관련 단락도 추출"
)
```

### 레시피 C: FAERS 이상반응 상위 빈도

```
WebFetch(
  url="https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:METFORMIN&count=patient.reaction.reactionmeddrapt.exact&limit=20",
  prompt="상위 20개 이상반응 MedDRA PT와 보고 건수를 표로 정리. 총 보고 수 포함"
)
```

> **주의**: FAERS 결과는 해석에 주의. "자주 보고됨"이 반드시 "흔함(Common)"을 의미하지 않음. 이상반응 빈도의 공식 근거는 **라벨 6. ADVERSE REACTIONS 섹션**.

### 레시피 D: 약물상호작용 신속 조회

```
WebFetch(
  url="https://api.fda.gov/drug/label.json?search=openfda.generic_name:warfarin&limit=1",
  prompt="results[0]의 drug_interactions 필드와 clinical_pharmacology 필드 중 'CYP2C9', 'VKORC1' 관련 단락 전체를 추출"
)
```

## 필드 추출 가이드

| 필드 (openfda label) | 용도 |
|-------------------|------|
| `indications_and_usage` | 적응증 |
| `dosage_and_administration` | 용법용량·용량 조정 지침 |
| `contraindications` | 제외 기준 근거 |
| `warnings`, `boxed_warning` | 안전성 주의사항, 블랙박스 경고 |
| `adverse_reactions` | 이상반응 프로파일 |
| `drug_interactions` | DDI 시험 설계 근거 |
| `clinical_pharmacology` | PK 파라미터 |
| `pharmacogenomics` | **translational-scientist 인계** |
| `use_in_specific_populations` | Special Pop 설계 근거 |
| `clinical_studies` | 유사 시험 |
| `openfda.application_number` | NDA 번호 (허가 근거 문헌 추적) |

## 산출물 저장 형식

DailyMed 라벨이 이미 수집된 경우 openFDA는 **허가 메타데이터 + FAERS만** 별도 저장:

`_workspace/01_references/labels/{drug_name}_openFDA.md`:

```markdown
# {약물명} — openFDA 메타데이터

## 허가 정보 (drugsfda)
- NDA 번호: NDA{번호}
- 신청사: {제조사}
- 최초 승인일: YYYY-MM-DD
- 현재 상태: Prescription / Discontinued
- 브랜드명: {브랜드}

## NDC/제형 정보
| NDC | 제형 | 경로 | 함량 |
|-----|------|------|------|

## FAERS 이상반응 상위 20개 (참고)
| 순위 | MedDRA PT | 보고 건수 |
|------|-----------|---------|

> FAERS는 자발적 보고. 공식 빈도는 라벨 참조.

## 라벨 PG 섹션 (DailyMed 미수집 시)
(pharmacogenomics 필드 전문)
```

## Gotchas

- **대소문자 일관성**: `openfda.generic_name`은 **소문자**, `patient.drug.medicinalproduct`는 **대문자**로 저장되어 있는 경향. 일단 결과 0건이면 대소문자 바꿔 재시도
- **String literal 쿼리**: 따옴표 필수. `openfda.generic_name:metformin` vs `openfda.generic_name:"metformin"`은 동작이 다를 수 있음 (스페이스 포함 시 따옴표 필수)
- **Rate Limit 초과 시**: HTTP 429 반환. 무키 1,000/day 소진 시 다음날까지 대기 또는 API key 발급. 프로젝트에서 대량 조사가 필요하면 key 발급 권장
- **업데이트 지연**: openFDA는 FDA 원본 대비 수 주~수 개월 지연 가능. 최신 라벨이 중요하면 DailyMed 우선
- **FAERS 해석 주의**: 자발적 보고이므로 실제 발생률 아님. 단순 "어떤 이상반응이 보고되고 있는가" 수준으로만 활용
- **`pharmacogenomics` 필드 부재**: 이 필드가 없는 약물이 많음. 대안으로 `clinical_pharmacology` 또는 `use_in_specific_populations`에서 CYP 키워드 검색
- **API key 저장**: key 발급 시 **`${CLAUDE_PLUGIN_ROOT}/settings.local.json`에 저장하지 말 것** (git 추적됨). 환경변수 `OPENFDA_API_KEY` 사용 권장. 현재는 무키로 충분하므로 key 불필요

## 참고 링크

- API 문서: https://open.fda.gov/apis/
- 필드 사전: https://open.fda.gov/apis/drug/label/reference/
- 쿼리 구문: https://open.fda.gov/apis/query-syntax/
- Status dashboard: https://open.fda.gov/apis/status/
