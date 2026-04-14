# DailyMed API 레퍼런스

NIH/NLM가 운영하는 미국 FDA 승인 의약품 라벨 DB. **Structured Product Labeling (SPL)** 원문을 제공하며, 임상시험 문서 작성 시 약물 라벨의 정식 내용을 WebFetch로 직접 조회하는 데 사용한다.

## 기본 정보

| 항목 | 내용 |
|------|------|
| Base URL | `https://dailymed.nlm.nih.gov/dailymed/services/v2/` |
| 인증 | 불필요 (공개 API) |
| Rate Limit | 공식 명시 없음 (상식적 수준의 요청 권장) |
| 형식 | JSON (기본) / XML |
| 문서 | https://dailymed.nlm.nih.gov/dailymed/app-support-mapping-guide.cfm |

## 주요 엔드포인트

### 1. 약물명으로 SPL 검색

```
GET /v2/spls.json?drug_name={name}&pagesize=10
```

**예시:**
```
https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=metformin&pagesize=10
```

**반환 주요 필드:**
- `data[].setid` — SPL 고유 ID (이후 상세 조회에 사용)
- `data[].title` — 라벨 제목 (약물명 + 제형 + 제조사)
- `data[].published_date` — 최신 개정일
- `data[].spl_version` — SPL 버전 번호

### 2. SPL 상세 조회 (라벨 전문)

```
GET /v2/spls/{setid}.json
```

**예시:**
```
https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/abd6a2ca-40c2-485c-bc53-db1c652505ed.json
```

반환 구조는 SPL 표준에 따른 섹션 트리. 본문은 XML이 기본이며 JSON은 메타데이터. **라벨 전문 텍스트는 XML 버전이 완전함**:

```
GET /v2/spls/{setid}.xml
```

### 3. NDA 번호로 SPL 검색

```
GET /v2/applicationnumbers/{number}.json
```

FDA NDA 번호를 이미 알고 있을 때 사용.

### 4. 약물명 목록 조회

```
GET /v2/drugnames.json?drug_name={partial}
```

약물명 부분 일치로 후보 목록 조회. 검색 전 예비 단계에서 유용.

## WebFetch 쿼리 레시피

### 레시피 A: 약물명 → 최신 라벨 전문

**Step 1**: 약물명으로 SPL ID 검색
```
WebFetch(
  url="https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=metformin&pagesize=5",
  prompt="각 SPL의 setid, title, published_date를 추출. 가장 최신 개정본을 선택"
)
```

**Step 2**: setid로 라벨 전문 조회
```
WebFetch(
  url="https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml",
  prompt="라벨 본문에서 '약물상호작용(DRUG INTERACTIONS)', '약동학(CLINICAL PHARMACOLOGY)', '금기(CONTRAINDICATIONS)', '특수 집단(USE IN SPECIFIC POPULATIONS)', '약물유전체(PHARMACOGENOMICS)' 섹션을 추출"
)
```

### 레시피 B: 약물유전체(PG) 섹션 추출

PG 정보는 SPL의 "12.5 Pharmacogenomics" 섹션 또는 라벨 전체에 산재할 수 있다:

```
WebFetch(
  url="https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml",
  prompt="다음 키워드 주변 컨텍스트를 모두 추출: 'CYP2C19', 'CYP2D6', 'CYP2C9', 'CYP3A4/5', 'poor metabolizer', 'intermediate metabolizer', 'extensive metabolizer', 'ultra-rapid metabolizer', 'PM', 'IM', 'EM', 'UM', 'genotype', 'polymorphism'. 각 키워드 발견 시 해당 단락 전체를 인용"
)
```

### 레시피 C: 약물상호작용 섹션만 타겟 추출

```
WebFetch(
  url="https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml",
  prompt="'7 DRUG INTERACTIONS' 또는 '약물상호작용' 섹션 하위 전체 텍스트를 추출. 각 하위 섹션(7.1, 7.2 등)의 제목과 내용을 보존"
)
```

## 필드 추출 가이드

라벨 전문에서 임상시험 설계에 필요한 필드:

| 필드 | SPL 섹션 (번호는 관례) | regulatory-expert 활용 |
|------|--------------------|----------------------|
| 적응증 | 1. INDICATIONS AND USAGE | 시험 대상 질환 확인 |
| 용법용량 | 2. DOSAGE AND ADMINISTRATION | 임상시험 용량 범위 결정 근거 |
| 금기 | 4. CONTRAINDICATIONS | 제외 기준 근거 |
| 경고/주의사항 | 5. WARNINGS AND PRECAUTIONS | 안전성 모니터링 항목 |
| 이상반응 | 6. ADVERSE REACTIONS | clinician 참고 자료 |
| 약물상호작용 | 7. DRUG INTERACTIONS | DDI 시험 설계 |
| 특수 집단 | 8. USE IN SPECIFIC POPULATIONS | Special Pop 시험 설계 |
| 약동학 | 12.3 CLINICAL PHARMACOLOGY / PK | PK 파라미터 검증 |
| **약물유전체** | **12.5 PHARMACOGENOMICS** | **translational-scientist 인계** |
| 임상시험 | 14. CLINICAL STUDIES | 유사 시험 참고 |

## 산출물 저장 형식

`_workspace/01_references/labels/{drug_name}_DailyMed.md`:

```markdown
# {약물명} Label — DailyMed

## 출처
- SPL setid: {setid}
- URL: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={setid}
- Published Date: YYYY-MM-DD
- SPL Version: {N}
- 제조사: {제조사}

## 1. 적응증 (INDICATIONS AND USAGE)
...

## 2. 용법용량 (DOSAGE AND ADMINISTRATION)
...

## 3. 금기 (CONTRAINDICATIONS)
...

## 4. 약물상호작용 (DRUG INTERACTIONS)
...

## 5. 약동학 (CLINICAL PHARMACOLOGY)
...

## 6. 약물유전체 (PHARMACOGENOMICS) — translational-scientist에 전달
...

## 7. 본 시험 설계에의 시사점
(regulatory-expert가 추출한 핵심 요건과 본 시험 적용 항목)
```

## Gotchas

- **JSON vs XML**: JSON은 메타데이터 위주, **라벨 전문은 XML에서만 완전**. WebFetch 시 URL 확장자로 형식 지정
- **setid가 여러 개**: 같은 약물이라도 제조사·제형·용량별로 별도 SPL. 최신 + 해당 제형만 선택
- **섹션 번호 불일치**: SPL 구조는 표준화되어 있으나 섹션 번호는 약물별로 차이 가능 (예: "12.5 Pharmacogenomics"가 없는 약물도 있음 — 이 경우 라벨 전체에서 CYP 키워드 검색)
- **개정 빈도**: 라벨은 수시 개정됨. `published_date`를 반드시 산출물에 기록
- **WebFetch 크기 한계**: XML 파일이 매우 클 수 있음 (수 MB). `prompt`에서 필요 섹션만 지정해서 추출해야 토큰 절약
- **Reference 날조 금지**: setid는 UUID 형식. 추측으로 생성하지 말 것. 반드시 Step 1 검색 결과에서 획득
