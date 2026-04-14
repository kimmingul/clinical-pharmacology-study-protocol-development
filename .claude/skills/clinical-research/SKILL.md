---
name: clinical-research
description: "임상시험 배경 조사를 수행하는 스킬. IB 분석, ClinicalTrials.gov 유사 시험 검색, PubMed 문헌 조사, MFDS/FDA 가이드라인 조사, 약물 라벨 분석, ICD-10 코드 확인을 포함. 두 에이전트(clinical-pharmacologist, regulatory-expert)가 각자의 영역을 조사한다. 임상시험 조사, 문헌 검색, 배경 연구, 유사 시험 분석, 규제 자료 조사, 가이드라인 검색, 약물 라벨 조회 요청 시 사용."
---

# Clinical Research — 임상시험 배경 조사

네 개의 조사 에이전트(clinical-pharmacologist, regulatory-expert, clinician, translational-scientist)가 역할을 분담하여 배경 자료를 수집한다. 검색 영역이 명확히 분리되어 중복이 없다.

## 에이전트별 담당 영역

| 영역 | 담당 에이전트 | 검색 도구 |
|------|-------------|----------|
| **PK 자료** (반감기, 변동성, AUC/Cmax) | clinical-pharmacologist | PubMed, ClinicalTrials.gov |
| 대사 경로 (CYP/수송체) — 정성적 기여 | clinical-pharmacologist | PubMed |
| 약물상호작용 기전 | clinical-pharmacologist | PubMed |
| 유사 시험 설계 | clinical-pharmacologist | ClinicalTrials.gov |
| IB 분석/초기용량 (FIH) | clinical-pharmacologist | Read (IB 파일) |
| **PD 바이오마커** (작용 기전, 측정법) | translational-scientist | PubMed |
| **PK-PD 모델링** | translational-scientist | PubMed |
| **수용체 점유율** (PET 등) | translational-scientist | PubMed |
| **약물유전체학** (CYP/표적 다형성, 한국인 빈도) | translational-scientist | **PharmGKB + CPIC (WebFetch)** + PubMed (한국인 빈도) — `.claude/references/api_reference/{pharmgkb,cpic}.md` |
| **대사체학** (인체 특이 대사체, 내인성 바이오마커) | translational-scientist | PubMed |
| 규제 가이드라인 | regulatory-expert | MFDS/FDA/EMA 가이드라인 DB |
| 약물 라벨 정보 (PG 섹션 추출 포함) | regulatory-expert | **DailyMed + openFDA (WebFetch)** — `.claude/references/api_reference/{dailymed,openfda}.md` |
| ICD-10 코딩 | regulatory-expert | ICD-10 API |
| MFDS 승인현황 | regulatory-expert | **MFDS 의약품안전나라 (WebFetch)** — `nedrug.mfds.go.kr/searchClinic`, `.claude/references/api_reference/mfds.md` |
| 선정/제외 기준 근거 | clinician | PubMed |
| 안전성 프로파일·모니터링 근거 | clinician | PubMed |

## 시험 유형별 오믹스/PD 우선순위

translational-scientist의 조사 깊이는 시험 유형에 따라 차등 적용한다. 우선순위 "—"(생략)인 시험에서는 핵심 PD 정보만 간략 정리.

| 시험 유형 | PD 조사 | PG 조사 | 대사체 조사 | translational-scientist 참여 |
|----------|--------|--------|------------|--------------------------|
| **FIH/SAD** | ★★★ | ★★ | ★ | **참여** (PD 마커 + 표적 다형성) |
| **MAD** | ★★★ | ★★ | ★ | **참여** (정상상태 PD) |
| **DDI** | ★★ | **★★★** | ★★ | **참여** (CYP PM/EM 분류 + 내인성 바이오마커) |
| **BE** | ★ | ★ | — | **불참** (PG/PD 의미 낮음, 동등성이 1차 목적) |
| **FE** | ★ | ★ | — | **불참** (식이 영향이 1차 목적) |
| **QTc** | ★★ | ★★ | — | **참여** (C-QTc 모델 + KCNH2/SCN5A 다형성) |
| **ADME** | ★★ | ★★ | **★★★** | **참여** (MIST 준수, 인체 특이 대사체 핵심) |
| **Special Pop** | ★★ | ★★ | ★★ | **참여** (집단 차이 평가) |

★★★ 필수, ★★ 권장, ★ 선택, — 생략

## Step 0: 시험 유형별 조사 전략

시험 유형에 따라 1차 자료 수집 방법이 달라진다.

### A. FIH/SAD/MAD (신약) — IB 기반 조사

`_workspace/00_input/` 디렉토리에서 IB 파일을 Read로 읽어 핵심 정보를 추출한다:

| IB 추출 항목 | clinical-pharmacologist 담당 |
|-------------|----------------------------|
| 비임상 약리 | 작용 기전, in vitro/in vivo 약리 |
| 비임상 독성 | NOAEL, 표적 장기, 가역성 |
| 비임상 PK | 흡수, 분포, 대사(CYP 관여), 배설 |
| 기존 임상 데이터 | PK 파라미터, 안전성 프로파일, 용량-반응 |
| 안전성 약리 | hERG, CNS, 호흡기, 심혈관 |

**초기 용량 산출 (FIH):**
- MRSD 방법: NOAEL → HED (체표면적 환산) → Safety Factor → MRSD
- MABEL 방법: 바이오의약품/면역조절제에 적용
- `.claude/scripts/fih/starting_dose_calculation.py`를 참조하여 코드로 수행

IB 미제공 신약: 약물 계열(drug class)과 MOA를 기반으로 유사 약물의 공개 데이터를 수집. "[IB 미제공 — 공개 데이터 기반]" 표시.

### B. DDI/BE/FE/QTc/ADME (허가 약물) — 문헌 기반 조사

IB 불필요. 약물명만으로 배경 자료를 수집한다.

**시험 유형별 특화 조사:**

| 시험 유형 | clinical-pharmacologist 초점 | regulatory-expert 초점 |
|----------|----------------------------|----------------------|
| **DDI** | 대사 효소(CYP), 수송체(P-gp, OATP), 기존 DDI 연구 결과, in vitro 데이터 | FDA DDI 가이드라인, MFDS 약물상호작용 평가 가이드라인 |
| **BE** | BCS 분류, 용출 프로파일, 원개발사 PK 데이터, 기존 BE 시험 | MFDS 생동성시험 가이드라인, 동등성 한계, 고변동약물 가이드라인 |
| **FE** | BCS 분류, 흡수 특성, 식이 영향 관련 기존 데이터 | FDA FE 가이드라인, 식이 조건 요건 |
| **QTc** | hERG 데이터(안전성 약리), 기존 QTc 연구의 PK 측면 (PK-QTc 정량 모델은 translational-scientist) | ICH E14, FDA QT/QTc 가이드라인 |
| **ADME** | 대사 경로·배설 경로 정성 (방사성 표지 관련 PK) | 방사성의약품 관련 규제 요건 |
| **FIH** | IB 분석(PK·독성 요약), 초기 용량 산출, 용량 증량 설계 (비임상 약리·PD 평가는 translational-scientist) | FDA/EMA/MFDS FIH 가이드라인, 안전성 보고 요건 |

## clinical-pharmacologist 절차

### Step 1: PubMed 문헌 검색

**검색 전략 (순차 실행, 결과 없으면 확장):**
1. `search_articles(query="{약물명} pharmacokinetics")` — PK 데이터
2. `search_articles(query="{약물명} safety OR tolerability")` — 안전성
3. `search_articles(query="{약물명} dose-response OR dose-finding")` — 용량-반응
4. `search_articles(query="{약물명} drug interaction OR CYP")` — DDI (해당 시)
5. 결과 없으면 → `search_articles(query="{약물 계열} {적응증} {MOA}")` — 유사 약물

핵심 논문 3-5편에 대해 `get_article_metadata`. `get_full_text_article`은 Open Access만 전문 제공 — 대부분 초록 기반 추출.

### Step 2: 유사 시험 검색 (ClinicalTrials.gov)

**검색 전략:**
1. `search_trials(condition="{적응증}", intervention="{약물명 또는 계열}")` — 동일 약물
2. `search_trials(condition="{적응증}", phase="PHASE1")` — 동일 적응증
3. 결과 없으면 → 약물 계열명/MOA/표적으로 확장
4. `search_by_sponsor(sponsor="{의뢰자}")` — 의뢰자 파이프라인 (선택)

주요 시험 3-5개 선정 → `get_trial_details` + `analyze_endpoints`

**수집 항목 (시험당):**

| 항목 | 내용 |
|------|------|
| NCT 번호 | 고유 식별자 |
| 시험 설계 | 맹검, 무작위화, 대조군 유형 |
| 대상자 수 | 등록 목표/실제 |
| 용량 범위 | 시작 용량, 최대 용량, 증량 간격 |
| 1차 평가 변수 | PK, 안전성, 내약성 등 |
| 2차 평가 변수 | PD 마커, 탐색적 등 |
| 선정 기준 핵심 | 연령, BMI, 건강 상태 |

## regulatory-expert 절차

### Step 1: ICD-10 적응증 코딩

```
search_codes(query="{적응증명}", code_type="diagnosis") → lookup_code(code="{코드}")
```

### Step 2: 규제 가이드라인 조사

시험 유형별 해당 가이드라인을 확인하고 핵심 요건을 정리한다:

**규제 가이드라인 참조 (사전 수록):**
- 시작점: `.claude/references/guidelines/index.md` — 전체 인덱스 (ICH/FDA/EMA/MFDS, 국내 법령, 시험 유형별 cross-agency 비교)
- MFDS: `.claude/references/guidelines/mfds/` (BE, DDI, FIH, 임상약리 일반, 통계)
- FDA: `.claude/references/guidelines/fda/` (BE, DDI, FIH, FE, QTc, BMV)
- EMA: `.claude/references/guidelines/ema/` (BE, DDI, FIH, BMV)
- ICH: `.claude/references/guidelines/ich/` (E6 R3, E8 R1, E14, M13A)
- Cross-Agency 비교: `.claude/references/guidelines/by_study_type/` — 시험 유형별 4개 기관 차이점 통합 비교
- 국내 법령: `.claude/references/guidelines/regulations/` (약사법, KGCP, PIPA, 생명윤리법)

### Step 3: 약물 라벨 정보 (허가 약물) — WebFetch 기반

허가된 약물의 경우 **DailyMed (1차)** + **openFDA (보완)** WebFetch로 라벨·허가 정보 조회. 상세 쿼리 레시피는 `.claude/references/api_reference/{dailymed,openfda}.md` 참조.

**Step 3-A: DailyMed SPL 라벨 수집**
1. `GET https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={name}&pagesize=5` → 최신 setid 선택
2. `GET https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml` → 라벨 전문 추출
3. 추출 필드: 적응증, 용법용량, 금기, 경고/주의, 약물상호작용, 약동학, **약물유전체(PG, 있을 시)**, 특수 집단, 임상시험
4. 저장: `_workspace/01_references/labels/{drug_name}_DailyMed.md`

**Step 3-B: openFDA 허가 메타데이터 + FAERS**
1. `GET https://api.fda.gov/drug/drugsfda.json?search=openfda.generic_name:{name}` → NDA 번호, 최초 승인일, 현재 상태
2. `GET https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{NAME}&count=patient.reaction.reactionmeddrapt.exact&limit=20` → FAERS 상위 이상반응 (참고용, 공식 빈도는 라벨 참조)
3. 저장: `_workspace/01_references/labels/{drug_name}_openFDA.md`

**Step 3-C: PG 섹션 translational-scientist 인계**
라벨에 PG 섹션이 있으면 별도 추출하여 translational-scientist에게 참고자료로 전달 (해석·한국인 빈도 분석은 TS 담당).

### Step 4: MFDS 임상시험 승인현황 — WebFetch 기반

**URL**: `https://nedrug.mfds.go.kr/searchClinic` (인증 불필요, GET 요청, HTML 응답)

**쿼리 예시:**
```
GET https://nedrug.mfds.go.kr/searchClinic?searchYn=true&page=1&searchType=ST1&searchKeyword={약물명}&approvalDtStart=2023-01-01&approvalDtEnd=2024-12-31
```

**추출 항목**: 총 건수, 각 시험의 제목·의뢰자·임상 단계·실시기관·승인일

**산출물**: `_workspace/01_references/mfds_clinical_trials/{topic}_approval_list.md`

상세 쿼리 레시피·HTML 파싱 힌트·파라미터 목록은 `.claude/references/api_reference/mfds.md` 참조.

- 동일/유사 약물의 국내 임상시험 승인 사례
- 승인 조건, 시험 설계, 대상자 수 참고

## clinician 절차 (모든 시험에서 참여)

모든 시험에서 안전성 전문 조사와 임상적 검토를 수행한다.

### Step 1: 선정/제외 기준 임상 근거

- 대상자(건강인 또는 환자)의 임상적 특성 조사
- 안전성 관점의 제외 기준 근거 (약물 특이 위험 반영)

### Step 2: 안전성 프로파일 체계적 수집

PubMed에서 안전성 키워드로 집중 검색 (PK 검색은 CP 담당, 중복 방지):
1. `"{약물명} adverse events"` — 이상반응 빈도별·기관계별 분류
2. `"{약물명} serious adverse event"` — SAE 사례 분석
3. `"{약물 계열} class effect safety"` — 계열 공통 이상반응
4. `"{약물명} safety monitoring"` — 모니터링 근거
5. `"{약물명} stopping rule discontinuation"` — 중지 기준 근거

### Step 3: 개별 안전성 reference 파일 생성

`_workspace/01_references/safety/` 디렉토리에 아래 파일을 생성한다:

| 파일 | 내용 |
|------|------|
| `AE_profile_{약물명}.md` | 이상반응 빈도별 분류 (Very common ≥10%, Common 1-10%, Uncommon 0.1-1%, Rare), 기관계별(SOC) 정리 |
| `SAE_cases_{약물명}.md` | 중대한 이상반응 사례 (발생률, 인과관계, 결과), 사망 사례 유무 |
| `class_effect_{약물계열}.md` | 약물 계열 공통 이상반응 (예: DHP CCB → 말초 부종, 어지러움, 홍조) |
| `safety_monitoring_rationale.md` | 활력징후/ECG/Lab 측정 시점의 과학적 근거, 약물 특이 모니터링 항목 |
| `stopping_rules_rationale.md` | 개인 수준 + 시험 수준 중지 기준의 문헌 근거 |

### Step 4: 안전성 모니터링 계획 근거

- 이상반응 관리 프로토콜
- 중지 기준(stopping rules) 임상 근거
- 응급 처치 절차 (약물 특이)

## 산출물 구조

### ★ 개별 Reference 파일 분리 (필수)

각 에이전트는 조사한 **모든 reference를 개별 MD 파일로 분리 저장**한다. 요약 보고서는 이 개별 파일들을 참조하는 형태로 작성한다.

```
_workspace/01_references/
├── trials/                          ← ClinicalTrials.gov 각 시험별
│   ├── NCT02974439.md
│   └── ...
├── literature/                      ← PubMed 각 논문별
│   ├── PMID_32034814.md
│   └── ...
├── guidelines/                      ← 규제 가이드라인별
│   ├── MFDS_BE_guideline_summary.md
│   └── ...
├── labels/                          ← 약물 라벨별
│   ├── Norvasc_FDA_label.md
│   └── ...
├── safety/                          ← 안전성 자료 (clinician)
│   ├── AE_profile_{drug}.md
│   ├── SAE_cases_{drug}.md
│   └── ...
├── pd_biomarkers/                   ← PD 바이오마커 (translational-scientist)
│   ├── 4-beta-OH-cholesterol.md
│   └── ...
├── pharmacogenomics/                ← 약물유전체 (translational-scientist)
│   ├── CYP2C19.md
│   ├── CYP2D6.md
│   └── ...
└── metabolomics/                    ← 대사체 (translational-scientist, 해당 시)
    ├── coproporphyrin_I.md
    └── ...
```

#### 임상시험 개별 파일 구조 (`trials/NCTxxxxxxxx.md`)

```markdown
# NCTxxxxxxxx — [시험 제목 요약]

## 기본 정보
| 항목 | 내용 |
|------|------|
| NCT 번호 | NCTxxxxxxxx |
| 등록일 | YYYY-MM-DD |
| 상태 | Completed / Recruiting / ... |
| 의뢰자 | |
| 출처 | ClinicalTrials.gov |

## 연구 목적
(시험의 1차/2차 목적 상세 기술)

## 시험 설계
| 항목 | 내용 |
|------|------|
| 설계 유형 | (예: 무작위, 공개, 2×2 교차) |
| 맹검 | |
| 무작위화 | |
| 대조군 유형 | |
| Washout 기간 | |

## 대상자
### 선정 기준
(번호 매기기로 상세 나열)
### 제외 기준
(번호 매기기로 상세 나열)
### Sample size
- 등록 목표: N명
- 실제 등록/완료: N명

## 시험약 / 대조약
| 구분 | 약물명 | 용량 | 투여 경로 |
|------|--------|------|----------|

## 채혈 일정 (PK Sampling)
| 시점 # | 투여 후 시간 | 비고 |
|--------|------------|------|
(모든 시점 나열, 가능하면)

## 평가변수 (Endpoints)
### 1차 평가변수
### 2차 평가변수

## 통계 분석 방법
(분석 모형, 동등성 한계, 변환 방법 등)

## 결과 (공개된 경우)
### PK 결과
(Cmax, AUC, Tmax, t½ 등 수치)
### 동등성/안전성 결과
### 안전성 결과

## 본 시험 설계에의 시사점
(이 유사 시험의 설계에서 참고할 점, 차이점, 개선 방향)
```

#### 문헌 개별 파일 구조 (`literature/PMID_xxxxxxxx.md`)

```markdown
# PMID: xxxxxxxx — [1저자 et al., 연도]

## 서지 정보
| 항목 | 내용 |
|------|------|
| 저자 | |
| 제목 | |
| 저널 | |
| 출판일 | |
| PMID | |
| DOI | |
| Open Access | Yes / No |

## 연구 목적

## 연구 방법
### 시험 설계
### 대상자
### 투여 방법
### PK 분석 방법

## 주요 결과
### PK 파라미터
(Cmax, AUC, Tmax, t½, CV% 등 수치 테이블)
### 안전성 결과
### 기타 결과

## 본 시험 설계에의 시사점
(이 문헌에서 추출할 수 있는 설계 근거: CV%, 채혈 시점, washout 등)
```

#### 가이드라인 개별 파일 구조 (`guidelines/*.md`)

```markdown
# [가이드라인명] — [발행기관, 발행일]

## 출처
- 문서명: 
- 발행기관: 
- 발행일: 
- URL: 

## 핵심 요건 요약
(시험 유형별 주요 요건을 테이블로 정리)

## 본 시험에 적용되는 항목
(해당 시험 유형에서 반드시 충족해야 할 요건 목록)

## 다른 가이드라인과의 차이점
(MFDS vs FDA, MFDS vs EMA 비교)
```

#### 약물 라벨 개별 파일 구조 (`labels/*.md`)

```markdown
# [약물명] Label/SPC — [발행기관, 개정일]

## 출처
- 약물명: 
- 발행기관: 
- 개정일: 
- URL: 

## 허가 적응증

## 용법용량

## 약동학 섹션
(PK 파라미터 테이블)

## 약물상호작용 섹션

## 금기 / 주의사항

## 본 시험 설계에의 시사점
```

### 에이전트 역할 분담 (개별 reference 파일 생성)

- **clinical-pharmacologist**: `trials/`, `literature/` (PK 관련) 파일 생성
- **regulatory-expert**: `guidelines/`, `labels/` 파일 생성 + ICD-10 관련은 요약 보고서에 직접 기재
- **clinician**: `safety/` 파일 + 안전성 관련 `literature/` 파일
- **translational-scientist** (조건부): `pd_biomarkers/`, `pharmacogenomics/`, `metabolomics/` 파일 + PD/PG/대사체 관련 `literature/` 파일

### 요약 보고서와의 관계

각 에이전트는:
1. **먼저** 개별 reference 파일들을 `_workspace/01_references/` 하위에 생성한다
2. **그 다음** 개별 파일들을 참조하는 요약 보고서를 자신의 산출물 파일에 작성한다
3. 요약 보고서에서 개별 파일을 참조할 때: `→ 상세: [01_references/trials/NCTxxxxxxxx.md]` 형식으로 링크

메인 에이전트가 이를 합쳐 `_workspace/01_research_report.md`로 통합한다.

---

각 에이전트는 자신의 산출물 파일에 아래 구조로 작성한다. 메인 에이전트가 이를 합쳐 `_workspace/01_research_report.md`로 통합한다.

### clinical-pharmacologist 산출물

```markdown
# PK/PD 자료 조사 보고서

## 1. 약물 기본 정보
- 약물명, 계열, 작용 기전

## 2. IB 핵심 요약 (제공된 경우)
- 비임상 약리/독성/PK 요약
- 기존 임상 데이터
- 안전성 약리 (hERG, CNS, 심혈관)
(IB 미제공 시: "[IB 미제공 — 공개 데이터 기반]")

## 3. FIH 초기 용량 산출 (해당 시)
- MRSD/MABEL 계산 과정 및 결과
- 용량 증량 스킴 제안

## 4. PK/PD 문헌 요약
### 4.1 약동학(PK) 파라미터
### 4.2 대사 경로 (CYP, 수송체)
### 4.3 약물상호작용 데이터
### 4.4 용량-반응 관계
### 4.5 PK 변동성 (intra-subject CV%)

## 5. PK 기반 시험 설계 파라미터 도출
### 5.1 채혈 시점 설계
- Tmax 기반 밀집 구간 정의
- t½ 기반 총 채혈 기간 산출
- 절단 AUC 적용 여부 판단 (t½ > 24시간 시 AUC₀₋₇₂ₕ 검토)
- 권장 채혈 시점표 (시점별 근거 명시)
### 5.2 휴약기 산출 근거
- t½(max) × 10 이상으로 산출
- 잔류 농도 추정 (< 0.1% Cmax 보장)
- 규제 요건과의 비교
- 최종 휴약기 설정값 및 근거
### 5.3 절단 AUC 적용 검토 (해당 시)
- 적용 조건 충족 여부 (t½ > 24시간)
- 절단 시점 (통상 72시간) 및 근거
- FDA/MFDS 규제 상태
- 실무적 이점 (입원 기간, 채혈량, 비용)

## 6. 유사 시험 분석
### 6.1 시험 목록 요약표
### 6.2 주요 시험 상세 분석
### 6.3 엔드포인트 비교

## 7. 참고 문헌
```

### regulatory-expert 산출물

```markdown
# 규제 자료 조사 보고서

## 1. 적응증 코딩
- ICD-10 코드, 역학, 현재 치료 옵션

## 2. 규제 가이드라인 요약
### 2.1 MFDS 가이드라인
### 2.2 FDA/EMA 가이드라인
### 2.3 가이드라인 간 차이점

## 3. 약물 라벨 정보 (허가 약물)
- 허가사항, 약물상호작용 섹션, 금기

## 4. MFDS 임상시험 승인현황
- 국내 유사 시험 승인 사례

## 5. 규제 고려사항
- 시험 유형별 필수 요건

## 6. 참고 문헌
```

### 통합 보고서 구조 (`01_research_report.md`)

```markdown
# 임상시험 배경 조사 보고서

## 1. 적응증 개요
(regulatory-expert)

## 2. IB 핵심 요약 / 초기 용량 산출
(clinical-pharmacologist, FIH 해당 시)

## 3. PK 자료 요약
(clinical-pharmacologist)

## 4. PD/약력학 자료 요약
(translational-scientist, 해당 시)

## 5. 유사 시험 분석
(clinical-pharmacologist)

## 6. 규제 가이드라인 요약
(regulatory-expert)

## 7. 약물 라벨 정보 (PG 섹션 포함)
(regulatory-expert)

## 8. MFDS 임상시험 승인현황
(regulatory-expert)

## 9. 임상적 고려사항·안전성 프로파일
(clinician)

## 10. 약물유전체학(PG) 자료
(translational-scientist, 해당 시)

## 11. 대사체 자료
(translational-scientist, ADME/DDI 해당 시)

## 12. 종합 고려사항
- PD 평가 권장 항목 (Phase 4 협의 입력)
- PG 분석 권장 여부
- 대사체 분석 권장 여부
- 추가 동의 필요 여부 (생명윤리법 적용 검토)

## 13. 참고 문헌 (통합)
```

## Reference 형식

모든 자료에 검증 가능한 출처를 반드시 명시한다. MCP 도구 검색 결과에서 확인된 것만 인용한다.

| 자료 유형 | 형식 |
|----------|------|
| 학술 문헌 | `[저자 et al., 연도, PMID: 12345678]` |
| 임상시험 | `[NCT번호, 시험 제목 요약]` |
| 규제 가이드라인 | `[문서명, 발행기관, 발행일]` |
| 약물 라벨 | `[약물명 Label/SPC, 발행기관, 개정일]` |
| IB | `[IB 섹션 번호, 페이지]` |
| MFDS 가이드라인 | `[가이드라인명, 식약처, 발행일]` |

**미확인 정보:** `[출처 미확인 — 검증 필요]`로 표기. 존재하지 않는 PMID/NCT 번호를 절대 생성하지 않는다.

## Gotchas

- **검색 영역 침범 금지**: clinical-pharmacologist가 가이드라인을 조사하거나, regulatory-expert가 PK 문헌을 검색하면 중복·혼란 발생
- **FIH에서 IB 없이 진행 시**: 반드시 "[IB 미제공 — 공개 데이터 기반]"을 문서 전체에 명시. 초기 용량 산출은 IB 없이 불가
- **Reference 날조**: MCP 검색 결과에서 확인되지 않은 PMID/NCT를 기억이나 추측으로 적지 말 것
- **Open Access 전문**: `get_full_text_article`은 OA 논문만 전문 반환. 대부분 초록만 사용 가능
- **시험 유형 미확인**: Step 0에서 시험 유형을 반드시 확인하고 해당 전략을 선택해야 한다
- **MCP 도구명**: 시스템에서 제공하는 실제 도구명(예: `mcp__claude_ai_ICD-10_Codes__search_codes`)을 사용한다. 이 문서의 약칭은 설명용
- **clinician 호출 조건**: 건강한 성인 대상(DDI, BE, FE)에서는 clinician이 불참. 환자 대상 시험에서만 참여

## References

시험 유형별 상세 검색 키워드 및 MFDS 가이드라인 목록은 `references/` 디렉토리를 참조한다.
