# Clinical Trial Protocol Generator

임상약리 임상시험 문서를 체계적으로 개발하는 Claude Code 하네스 프로젝트.

7개의 전문 에이전트가 역할 기반으로 협업하여 **배경 조사**, **시험 설계**, **Synopsis**, **계획서(Protocol)**, **동의설명서/동의서(ICF)**를 생성합니다. 시험 유형에 따라 두 가지 워크플로우로 분기합니다:

- **FIH/SAD/MAD (신약)**: IB(시험자자료집) 기반 — 초기 용량 산출 포함
- **DDI/BE/FE/QTc/ADME (허가 약물)**: 약물명 기반 — 문헌·공개 DB 조사로 충분

---

## 산출물

| 문서 | 설명 |
|------|------|
| **배경 조사 보고서** | 문헌, 유사 시험, 규제 가이드라인, 약물 라벨 정보 종합 |
| **Synopsis** | 핵심 시험 설계 요약 (연구설계, 평가변수, 대상자 수, 통계분석 등) |
| **계획서 (Protocol)** | ICH E6(R3) Annex 1 구조 기반 임상시험 계획서 |
| **동의설명서/동의서 (ICF)** | 시험대상자용 동의설명서 + 서명 페이지 |
| **개인정보 동의서** | 개인정보 수집·이용·제3자 제공 동의서 (PIPA 요건) |

---

## 에이전트 팀

### 조사 에이전트 (Research Agents)

| 에이전트 | model | 역할 |
|---------|-------|------|
| **clinical-pharmacologist** | sonnet | PK 자료 수집(반감기, 변동성, 생체이용률), 대사 경로 정성적 기여, 약물상호작용 기전, 용량 근거, FIH 초기 용량 산출 |
| **translational-scientist** | sonnet | PD 바이오마커, PK-PD 모델링, 약물유전체학(CYP·표적 다형성), 대사체학(인체 특이 대사체, 내인성 바이오마커), 수용체 점유율 (**조건부 참여** — BE/FE 불참, 그 외 시험 유형별 우선순위 차등) |
| **regulatory-expert** | sonnet | MFDS/FDA/EMA 가이드라인, 임상시험 승인현황, 약물 라벨(PG 섹션 포함), 규제 전략 |
| **clinician** | sonnet | 선정/제외 기준, 안전성 모니터링, 임상 절차, 이상반응 관리 (**항상 참여**) |
| **biostatistician** | sonnet | 연구설계 옵션, sample size 계산 (Python 코드), 무작위화, 통계분석방법 |

### 작성 에이전트 (Writing Agents)

| 에이전트 | model | 역할 |
|---------|-------|------|
| **protocol-writer** | opus | Synopsis + 자료 보고서를 기반으로 Full Protocol 작성 |
| **icf-writer** | opus | 계획서 기반 동의설명서/동의서/개인정보 동의서 작성 |

### 검토 에이전트 (Review Agent)

| 에이전트 | model | 역할 |
|---------|-------|------|
| **qa-reviewer** | opus | 다중 에이전트 리뷰 취합, 우선순위 분류, 수정 조율 |

### 조건부 참여 규칙

| 시험 유형 | clinical-pharmacologist | translational-scientist | regulatory-expert | clinician | biostatistician |
|----------|------------------------|-----------------------|-------------------|-----------|-----------------|
| FIH/SAD/MAD | **참여** (IB 분석, 초기용량) | **참여** (PD 마커, 표적 다형성) | **참여** | **참여** | **참여** |
| DDI | **참여** (대사 기전) | **참여** (CYP PM/EM, 내인성 바이오마커) | **참여** | **참여** | **참여** |
| BE | **참여** (PK 특성, BCS) | **불참** | **참여** | **참여** | **참여** |
| FE | **참여** (흡수 특성, BCS) | **불참** | **참여** | **참여** | **참여** |
| QTc | **참여** (hERG 안전성 약리) | **참여** (C-QTc 모델, 채널 다형성) | **참여** | **참여** | **참여** |
| ADME | **참여** (PK 정성) | **참여** (인체 특이 대사체, MIST) | **참여** | **참여** | **참여** |
| PK Special Pop | **참여** | **참여** (집단 차이, 표적 발현) | **참여** | **참여** | **참여** |

> **clinician은 항상 참여**하여 안전성을 전담합니다. **translational-scientist**는 시험 목적이 동등성/식이 영향에 한정된 BE/FE에서 불참하고, 신약·DDI·QTc·ADME·특수 집단에서 PD/약력학 및 오믹스 자료를 수집합니다.

---

## 워크플로우

### 전체 파이프라인

```
Phase 1: 입력
    사용자: 약물명 + 시험 유형 (+ 선택적 자료)
         │
         ▼
Phase 2: 병렬 자료 수집
    ┌─ clinical-pharmacologist
    │   PubMed: PK, 대사, 약물상호작용
    │   ClinicalTrials.gov: 기존 유사 시험
    │   [FIH: IB 분석, 초기 용량 산출]
    │
    └─ regulatory-expert
        MFDS 승인현황 + 가이드라인
        FDA/EMA 가이드라인
        약물 라벨 정보
    
    ※ 모든 자료에 reference 필수 (PMID, NCT, URL)
         │
         ▼
Phase 3: 자료 종합 + ★ 사용자 검토 게이트 ★
    핵심 발견사항 요약 제시
    → 승인 / 추가 조사 요청 / 자료 직접 제공
    → 승인될 때까지 반복
         │
         ▼
Phase 4: 대화형 설계 협의
    수집 자료 기반 설계 옵션 제시 + 사용자 결정
    Step 1 ★ 선정/제외기준 (최우선) — 표준 템플릿 기반 항목별 협의
            └─ .claude/references/templates/inclusion_exclusion_criteria.md
    Step 2 연구설계 (parallel, crossover 유형 등)
    Step 3 세부 요소:
            - PK 채혈 시점
            - 평가변수 (1차/2차)
            - 유효성/약력학(PD) 평가 항목 (시험 유형별 PD 마커, GMR, ddQTcF 등)
            - 안전성 평가 항목
            - washout 기간, 투여 조건 등
         │
         ▼
Phase 5: 통계 설계 (biostatistician)
    - Sample size 계산 (Python 코드 실행 + 코드 제시)
    - 무작위화 방법
    - 통계 분석 방법
    → 사용자 확인
         │
         ▼
Phase 6: Synopsis 작성
    _workspace/synopsis_{variant}.md
    - 다양한 설계 변형으로 복수 synopsis 생성 가능
    - synopsis 간 비교표 제공
         │
         ▼
Phase 7: ★ Synopsis 승인 (Hard Gate) ★
    사용자가 명시적으로 승인해야 다음 단계 진행
         │
         ▼
Phase 8: Full Protocol 작성
    Synopsis + 자료 보고서를 모두 입력으로 사용
    → 정보 손실 방지
         │
         ▼
Phase 9: 다중 에이전트 리뷰 (병렬)
    ┌─ clinical-pharmacologist: PK 설계, 채혈 시점, 용량 근거
    ├─ clinician: 선정/제외, 안전성, 임상 절차 (조건부)
    ├─ regulatory-expert: ICH/MFDS 필수 요소, 규제 용어
    └─ biostatistician: 통계 섹션, sample size, 분석 방법
         │
         ▼
    qa-reviewer: 4개 리뷰 취합 → Critical/Major/Minor 분류
    → 수정 → 재리뷰 (Critical 해소까지)
         │
         ▼
Phase 10: ICF 작성 (별도 지시 시)
    계획서가 존재할 때만 실행 가능
```

### 시험 유형별 분기

#### FIH/SAD/MAD (신약)

```
IB 입력 (필수)
    → IB 분석 + 초기 용량 산출 (MRSD, MABEL)
    → 용량 증량 스킴 설계 (3+3, mTPI, BOIN 등)
    → Synopsis → Protocol → Review → (ICF)
```

#### DDI/BE/FE/QTc/ADME (허가 약물)

```
약물명 + 시험 유형 입력 (IB 불필요)
    → 문헌·공개 DB 기반 자료 수집
    → 대화형 설계 협의
    → 통계 설계 (sample size 등)
    → Synopsis → Protocol → Review → (ICF)
```

---

## Commands

단계별 commands로 워크플로우 전체를 제어합니다. 전체 파이프라인을 한번에 실행하거나, 개별 단계를 독립적으로 실행할 수 있습니다.

| Command | Phase | 기능 | 전제 조건 |
|---------|-------|------|----------|
| `/research` | 2-3 | 자료 수집 + 사용자 검토 게이트 | 약물명 + 시험 유형 |
| `/design` | 4-5 | 대화형 설계 협의 + 통계 설계 | 자료 조사 완료 |
| `/synopsis` | 6 | Synopsis 생성 (인자로 변형 지정) | 설계 협의 완료 |
| `/compare` | 6 | 여러 Synopsis를 비교표로 제시 | Synopsis 2개 이상 |
| `/protocol` | 8 | Full Protocol 작성 | Synopsis 승인 완료 |
| `/review` | 9 | 다중 에이전트 리뷰 실행 | Protocol 작성 완료 |
| `/icf` | 10 | ICF 작성 (동의설명서 + 동의서 + 개인정보 동의서) | Protocol 존재 |

### Command 사용 예시

```bash
# 전체 파이프라인 실행
Metformin과 Rifampin의 DDI 시험 문서를 작성해줘

# 개별 단계 실행
/research                          # 자료 수집 시작
/design                            # 설계 협의 시작
/synopsis crossover 2x2            # 2×2 crossover synopsis 생성
/synopsis parallel                 # parallel design synopsis 생성
/compare                           # 위 두 synopsis 비교
/protocol                          # 승인된 synopsis 기반 계획서 작성
/review                            # 다중 에이전트 리뷰
/icf                               # 동의문서 작성
```

### Synopsis 변형 옵션

`/synopsis` command에 인자를 전달하여 다양한 설계 변형을 탐색할 수 있습니다:

| 인자 예시 | 설명 |
|----------|------|
| `crossover 2x2` | 2-sequence, 2-period crossover |
| `crossover 2x3` | 2-sequence, 3-period replicate design |
| `crossover 2x4` | 2-sequence, 4-period replicate design |
| `crossover 3x3` | 3-sequence, 3-period Latin square design |
| `crossover 4x4` | 4-sequence, 4-period (Williams) design |
| `crossover 6x3` | 6-sequence, 3-period (Williams) design |
| `one-sequence` | 단일 순서 (DDI 시험에서 흔용) |
| `parallel` | 병렬 설계 |

각 변형마다 장단점, 유사 시험 사례, 예상 sample size가 함께 제시됩니다.

---

## 자료 수집 전략

### 검색 영역 분리

에이전트 간 검색 중복을 방지하기 위해 자료 수집 영역을 명확히 분리합니다:

| 영역 | 담당 에이전트 | 검색 도구 | 수집 항목 |
|------|-------------|----------|----------|
| PK/PD 자료 | clinical-pharmacologist | PubMed, ClinicalTrials.gov | PK 파라미터, 대사 경로(CYP), 수송체(P-gp, OATP), 반감기, 생체이용률 |
| 약물상호작용 | clinical-pharmacologist | PubMed | DDI 기전, inhibition/induction 데이터, 기존 DDI 연구 결과 |
| 유사 시험 설계 | clinical-pharmacologist | ClinicalTrials.gov | 시험 설계, 용량, 엔드포인트, 선정/제외 기준 |
| 규제 가이드라인 | regulatory-expert | MFDS/FDA/EMA 가이드라인 DB | 시험 유형별 규제 요건, 필수 평가 항목 |
| 임상시험 승인현황 | regulatory-expert | MFDS (의약품안전나라) | 한국 내 유사 시험 승인 사례, 승인 조건 |
| 약물 라벨 정보 | regulatory-expert | DailyMed/openFDA | 허가사항, 용법용량, 금기, 약물상호작용 섹션 |
| ICD-10 코딩 | regulatory-expert | ICD-10 API | 적응증 진단 코드 |

### 시험 유형별 특화 조사

| 시험 유형 | clinical-pharmacologist 초점 | regulatory-expert 초점 |
|----------|----------------------------|----------------------|
| **DDI** | 대사 효소(CYP), 수송체(P-gp, OATP), 기존 DDI 연구 결과, in vitro 데이터 | FDA DDI 가이드라인, MFDS 약물상호작용 평가 가이드라인 |
| **BE** | BCS 분류, 용출 프로파일, 원개발사 PK 데이터, 기존 BE 시험 | MFDS 생동성시험 가이드라인, 동등성 한계, 시험식이 요건 |
| **FE** | BCS 분류, 흡수 특성, 식이 영향 관련 기존 데이터 | FDA FE 가이드라인, 식이 조건 요건 |
| **QTc** | hERG 데이터, 기존 QTc 연구, PK-QTc 관계 | ICH E14, FDA QT/QTc 가이드라인 |
| **ADME** | 방사성 표지 연구 문헌, 대사 경로, 배설 경로 | 방사성의약품 관련 규제 요건 |
| **FIH** | IB 분석 (비임상 PK/독성/약리), 초기 용량 산출, 용량 증량 설계 | FDA/EMA/MFDS FIH 가이드라인, 안전성 보고 요건 |

### MFDS 자료 조사

regulatory-expert 에이전트가 수행하는 한국 규제 자료 조사:

**임상시험 승인현황 조사**
- 의약품안전나라(nedrug.mfds.go.kr)에서 동일/유사 약물의 국내 임상시험 승인 사례 검색
- 승인 조건, 시험 설계, 대상자 수 등 참고 정보 수집
- 국내 임상시험 환경(기관, 규모)에 대한 맥락 파악

**MFDS 가이드라인 조사**
- 시험 유형별 해당 MFDS 가이드라인 확인 및 핵심 요건 정리
- FDA/EMA 가이드라인과의 차이점 비교
- 주요 참조 가이드라인:
  - 생동성시험 기본 가이드라인
  - 약물상호작용 평가 가이드라인
  - 초회 인체적용 시험 가이드라인
  - 임상약리시험 일반 가이드라인
  - 생물학적동등성시험 통계 가이드라인
  - 고변동 약물의 생동성시험 가이드라인

---

## Reference 관리

### 원칙

모든 조사 자료에는 **검증 가능한 출처**를 반드시 명시합니다. 에이전트가 MCP 도구 검색 결과에서 확인된 자료만 인용하며, 기억이나 추측으로 참고문헌을 생성하지 않습니다.

### Reference 형식

| 자료 유형 | 형식 | 예시 |
|----------|------|------|
| 학술 문헌 | `[저자 et al., 연도, PMID: 12345678]` | `[Smith et al., 2023, PMID: 37654321]` |
| 임상시험 | `[NCT번호, 시험 제목 요약]` | `[NCT04123456, Metformin DDI with Rifampin]` |
| 규제 가이드라인 | `[문서명, 발행기관, 발행일]` | `[Drug Interaction Studies Guidance, FDA, 2020]` |
| 약물 라벨 | `[약물명 Label/SPC, 발행기관, 개정일]` | `[Metformin HCl Label, FDA, 2024-03]` |
| IB | `[IB 섹션 번호, 페이지]` | `[IB Section 5.3, p.42-45]` |
| MFDS 가이드라인 | `[가이드라인명, 식약처, 발행일]` | `[생동성시험 가이드라인, 식약처, 2023-12]` |

### 미확인 정보 처리

출처를 확인하지 못한 정보는 반드시 아래와 같이 표기합니다:

```
[출처 미확인 — 검증 필요]
```

절대로 존재하지 않는 PMID나 NCT 번호를 생성하지 않습니다.

### 사전 수록 규제 가이드라인 라이브러리

`.claude/references/guidelines/`에 ICH/FDA/EMA/MFDS 주요 가이드라인 요약과 국내 법령(약사법, KGCP, PIPA, 생명윤리법)이 사전 수록되어 있습니다. 에이전트는 매번 웹 검색을 수행하지 않고 이 라이브러리를 우선 참조합니다.

| 디렉토리 | 내용 |
|---------|------|
| `ich/` | ICH E6(R3), E8(R1), E14, M13A — Step 4 최종본 요약 |
| `fda/` | FDA BE, DDI, FIH, FE, QTc, BMV 가이드라인 핵심 요건 |
| `ema/` | EMA BE, DDI, FIH, BMV 가이드라인 핵심 요건 |
| `mfds/` | MFDS BE, DDI, FIH, 임상약리 일반, 통계 가이드라인 |
| `regulations/` | 국내 법령 (약사법, KGCP, PIPA, 생명윤리법) |
| `by_study_type/` | 시험 유형별 cross-agency 비교표 (BE, DDI, FIH, QTc, FE, PK 일반) |

마스터 인덱스: `.claude/references/guidelines/index.md` — 시험 유형별 우선순위와 cross-agency 비교표 안내. 사용자 PDF 제공이 필요한 항목은 `needs_user_input.md` 참조.

---

## Sample Size 계산

### 개요

biostatistician 에이전트가 사전 검증된 Python 코드 템플릿을 사용하여 sample size를 계산합니다. 코드 자체와 실행 결과를 모두 산출물에 포함하여 투명성을 확보합니다.

### 디자인-엔드포인트 매트릭스

| 디자인 | BE (AUC/Cmax) | DDI (GMR) | 연속형 (평균 비교) | 이분형 |
|--------|--------------|-----------|-----------------|--------|
| Parallel | ✓ | ✓ | ✓ | ✓ |
| Crossover 2×2 | ✓ | ✓ | ✓ | — |
| Replicate 2×3 | ✓ | — | — | — |
| Replicate 2×4 | ✓ (RSABE) | — | — | — |
| Crossover 4×4 (Williams) | ✓ | ✓ | ✓ | — |
| One-sequence | — | ✓ | — | — |

### 코드 템플릿 구조

```
.claude/scripts/sample_size/
├── parallel_continuous.py          # 병렬 설계, 연속형 엔드포인트
├── parallel_binary.py              # 병렬 설계, 이분형 엔드포인트
├── crossover_2x2_be.py             # 2×2 crossover, BE (AUC/Cmax)
├── crossover_2x2_ddi.py            # 2×2 crossover, DDI (GMR)
├── replicate_crossover_be.py       # Replicate crossover, BE (RSABE 포함)
├── williams_4x4.py                 # Williams 4×4 design
├── one_sequence_ddi.py             # One-sequence DDI
└── utils/
    ├── power_analysis.py           # 공통 검정력 분석 함수
    └── dropout_adjustment.py       # 탈락률 보정
```

### 주요 파라미터

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `intra_cv` | 개체 내 변동계수 (%) | 25% |
| `inter_cv` | 개체 간 변동계수 (%) | 35% |
| `equivalence_limits` | 동등성 한계 | (0.80, 1.25) |
| `power` | 검정력 | 0.80, 0.90 |
| `alpha` | 유의수준 | 0.05 |
| `dropout_rate` | 예상 탈락률 (%) | 10%, 20% |
| `gmr` | 기하평균비 (예상) | 0.95, 1.00 |
| `effect_size` | DDI에서 예상 변화 배수 | 1.25-fold |

### 사용 흐름

1. Phase 4 (설계 협의)에서 사용자와 디자인, 엔드포인트 확정
2. Phase 5에서 biostatistician이 해당 코드 템플릿에 파라미터를 채워 실행
3. 결과와 함께 **코드 전체**를 사용자에게 제시
4. 사용자가 파라미터 변경을 요청하면 즉시 재실행 가능

> **주의**: 이 코드는 시험 설계 지원 도구이며, 규제 제출용 공식 산출물이 아닙니다. 최종 sample size는 통계 전문가의 검증을 거쳐야 합니다.

---

## FIH 특수 절차

FIH/SAD/MAD 시험에서는 추가적인 안전성 절차가 적용됩니다.

### 초기 용량 산출 (Starting Dose Calculation)

clinical-pharmacologist 에이전트가 IB 데이터를 기반으로 수행합니다:

**MRSD (Maximum Recommended Starting Dose) 방법**
```
NOAEL (mg/kg, 동물)
  → HED (Human Equivalent Dose, 체표면적 환산)
  → Safety Factor 적용 (통상 1/10)
  → MRSD (mg, 사람)
```

- 체표면적 환산 계수: 종(species)별 Km 값 적용
  - 마우스: ÷12.3, 랫드: ÷6.2, 개: ÷1.8, 원숭이: ÷3.1
- Safety factor: 통상 1/10, 약물 특성에 따라 조정

**MABEL (Minimum Anticipated Biological Effect Level) 방법**
- 바이오의약품 및 면역조절제에 적용
- in vitro EC10/EC50, receptor occupancy 기반 산출

**Python 코드 지원**
- 체표면적 환산, safety factor 적용, MRSD 계산을 코드로 수행
- `.claude/scripts/fih/starting_dose_calculation.py`

### 용량 증량 스킴 (Dose Escalation Schemes)

| 방법 | 설명 | 적용 |
|------|------|------|
| Modified Fibonacci | 고정 비율 증량 (100%, 67%, 50%, 33%...) | 전통적 SAD |
| 3+3 | 3명→DLT 평가→3명 추가 또는 증량 | 소분자 Phase 1 |
| mTPI-2 | 모델 기반 독성 구간법 | 종양 Phase 1 |
| BOIN | Bayesian Optimal Interval | 종양 Phase 1 |
| CRM | Continual Reassessment Method | 모델 기반 |

### 참조 가이드라인

| 가이드라인 | 발행 기관 | 핵심 내용 |
|-----------|----------|----------|
| Estimating the Maximum Safe Starting Dose in Initial Clinical Trials (2005) | FDA | NOAEL→HED→MRSD 방법론 |
| Strategies to Identify and Mitigate Risks for First-in-Human and Early Clinical Trials (2017) | EMA | 위험 경감 전략, 센티넬 투여 |
| 초회 인체적용 시험 가이드라인 | MFDS | 국내 규제 요건 |

---

## 다중 에이전트 리뷰

### 프로세스

Full Protocol 작성 완료 후, 4명의 전문가 에이전트가 **병렬로** 계획서를 리뷰합니다.

```
Protocol 완성
       │
       ├─→ clinical-pharmacologist 리뷰
       ├─→ clinician 리뷰 (조건부)
       ├─→ regulatory-expert 리뷰
       └─→ biostatistician 리뷰
              │
              ▼
       qa-reviewer: 취합 + 우선순위 분류
              │
              ▼
       수정 → 재리뷰 (Critical 해소까지)
```

### 리뷰 범위

각 리뷰어의 검토 범위를 명확히 분리하여 중복을 방지합니다:

| 리뷰어 | 검토 초점 |
|--------|----------|
| **clinical-pharmacologist** | PK 설계 적절성, 채혈 시점, 약물상호작용 평가 방법, 용량 근거, washout 기간 |
| **clinician** | 선정/제외 기준의 임상적 타당성, 안전성 모니터링 계획, 이상반응 관리, 중지 기준 |
| **regulatory-expert** | ICH E6(R3) Annex 1 필수 요소 충족, MFDS/FDA 가이드라인 준수, 규제 용어 적절성 |
| **biostatistician** | 통계 섹션 완결성, sample size 정당성, 무작위화 방법, 1차/2차 분석 방법, 결측치 처리 |

### 분류 체계

qa-reviewer가 4개 리뷰를 취합하여 아래 기준으로 분류합니다:

| 등급 | 정의 | 처리 |
|------|------|------|
| **Critical** | 규제 요건 미충족, 대상자 안전 위험, 과학적 결함 | 자동 수정 후 재리뷰 |
| **Major** | 설계 적절성 문제, 주요 정보 누락 | 사용자에게 수정 권고 |
| **Minor** | 표현 개선, 일관성 사소한 불일치 | 수정 제안 (선택적) |

리뷰어 간 **상충 의견** 발생 시, qa-reviewer가 양쪽 근거를 비교하여 사용자에게 판단을 요청합니다.

---

## 사용자 검토 게이트

워크플로우에 두 개의 명시적 사용자 검토 게이트가 있습니다:

### 게이트 1: 자료 조사 완료 후 (Phase 3)

자료 수집이 완료되면 핵심 발견사항 요약을 사용자에게 제시합니다.

**사용자 선택지:**
- **승인** → Phase 4 (설계 협의)로 진행
- **추가 조사 요청** → 요청 내용에 따라 최적의 에이전트가 추가 작업 수행:
  - PK/약물 관련 → clinical-pharmacologist
  - 규제/가이드라인 → regulatory-expert
  - 임상적 판단 → clinician
  - 통계/설계 → biostatistician
- **자료 직접 제공** → 사용자가 문헌/데이터를 추가 입력

추가 조사 후 다시 사용자 검토 → **승인될 때까지 반복**.

### 게이트 2: Synopsis 승인 (Phase 7)

Synopsis가 작성되면 사용자의 **명시적 승인**이 있어야 Full Protocol 작성으로 진행합니다. 이 게이트는 건너뛸 수 없습니다.

---

## 프로젝트 구조

```
.
├── CLAUDE.md                              # 하네스 설정 (도메인 지식, 규제, 실행 규칙)
├── README.md
├── .claude/
│   ├── agents/                            # 에이전트 정의 (8개)
│   │   ├── clinical-pharmacologist.md     # 임상약리학자 (PK 측면)
│   │   ├── translational-scientist.md     # 중개의학자 (PD/PG/대사체, 조건부)
│   │   ├── regulatory-expert.md           # 규제전문가
│   │   ├── clinician.md                   # 임상의사
│   │   ├── biostatistician.md             # 생물통계학자
│   │   ├── protocol-writer.md             # 계획서 작성자
│   │   ├── icf-writer.md                  # 동의문서 작성자
│   │   └── qa-reviewer.md                 # QA 검토자
│   ├── skills/                            # 스킬 정의
│   │   ├── trial-doc-orchestrator/        # 파이프라인 오케스트레이터
│   │   ├── clinical-research/             # 배경 조사
│   │   ├── protocol-drafting/             # 계획서 작성
│   │   ├── icf-drafting/                  # 동의문서 작성
│   │   └── regulatory-review/             # 규제 검토
│   ├── commands/                          # 단계별 commands
│   │   ├── research.md
│   │   ├── design.md
│   │   ├── synopsis.md
│   │   ├── compare.md
│   │   ├── protocol.md
│   │   ├── review.md
│   │   └── icf.md
│   ├── memory/                            # 세션 간 메모리 (사용자 선호, 도메인 지식)
│   │   ├── MEMORY.md                      # 메모리 인덱스
│   │   └── *.md                           # 개별 메모리 파일
│   ├── references/                        # 사전 수록 자료
│   │   ├── guidelines/                    # 규제 가이드라인
│   │   │   ├── index.md                   # 마스터 인덱스
│   │   │   ├── ich/                       # ICH (E6 R3, E8 R1, E14, M13A)
│   │   │   ├── fda/                       # FDA (BE, DDI, FIH, FE, QTc, BMV)
│   │   │   ├── ema/                       # EMA (BE, DDI, FIH, BMV)
│   │   │   ├── mfds/                      # MFDS (BE, DDI, FIH, 임상약리, 통계)
│   │   │   ├── regulations/               # 국내 법령 (약사법, KGCP, PIPA, 생명윤리법)
│   │   │   ├── by_study_type/             # 시험 유형별 cross-agency 비교
│   │   │   │   ├── be_cross_agency.md
│   │   │   │   ├── ddi_cross_agency.md
│   │   │   │   ├── fih_cross_agency.md
│   │   │   │   ├── qtc_cross_agency.md
│   │   │   │   ├── fe_cross_agency.md
│   │   │   │   └── pk_general_cross_agency.md
│   │   │   └── needs_user_input.md        # 사용자 PDF 제공 필요 항목
│   │   └── templates/                     # 표준 템플릿 (선정/제외기준 등)
│   │       └── inclusion_exclusion_criteria.md
│   └── scripts/                           # 실행 가능한 Python 스크립트
│       ├── README.md                      # 스크립트 인덱스
│       ├── sample_size/                   # Sample size 계산
│       │   ├── parallel_continuous.py
│       │   ├── crossover_2x2_be.py
│       │   ├── crossover_2x2_ddi.py
│       │   ├── replicate_crossover_be.py
│       │   ├── williams_4x4.py
│       │   ├── one_sequence_ddi.py
│       │   └── utils/power_analysis.py
│       └── fih/                           # FIH 산출 코드
│           ├── starting_dose_calculation.py
│           └── dose_escalation.py
├── _workspace/                            # 중간 산출물
│   ├── 00_input/                          # 입력 자료 (IB, 사용자 제공 자료)
│   ├── 01_research_report.md              # 자료 종합 보고서
│   ├── 02_synopsis.md                     # Synopsis (변형: synopsis_*.md)
│   ├── 03_protocol_draft.md               # Full Protocol
│   ├── 04_icf_draft.md                    # ICF (별도 지시 시)
│   └── review/                            # 리뷰 산출물
│       ├── review_clinical_pharmacologist.md
│       ├── review_clinician.md
│       ├── review_regulatory_expert.md
│       ├── review_biostatistician.md
│       └── qa_review_report.md
└── docs/                                  # 참고 자료 및 템플릿
```

---

## 지원하는 시험 유형

| 시험 유형 | 입력 요건 | 설명 |
|----------|----------|------|
| **FIH** (First-in-Human) | IB 필수 | 초기 용량 산출, 용량 증량 설계 포함 |
| **SAD/MAD** | IB 필수 | 단회/반복 투여 용량 증량 |
| **DDI** (Drug-Drug Interaction) | 약물명 (2개) | 약물상호작용 연구. One-sequence, crossover 설계 |
| **BA/BE** (Bioequivalence) | 약물명 | 생물학적 동등성. 2×2, replicate crossover 등 |
| **FE** (Food Effect) | 약물명 | 식이 효과. Crossover 설계 |
| **QTc** | 약물명 | 심전도 영향. ICH E14 준수 |
| **ADME** | 약물명 | 흡수·분포·대사·배설. 방사성 표지 연구 |
| **적응형 설계** | IB 또는 약물명 | Adaptive Design |
| **PK Special Population** | 약물명 | 간장애, 신장애, 소아, 고령자 등 |

---

## 준수 규정

### 국제 가이드라인

| 규정 | 적용 범위 |
|------|----------|
| **ICH E6(R3)** | GCP, Annex 1 프로토콜 필수 요소 |
| **ICH E8(R1)** | 임상시험의 일반적 고려사항 |
| **ICH E14** | QTc 시험 (해당 시) |
| **헬싱키 선언** | 윤리적 원칙 |

### 한국 규제

| 규정 | 적용 범위 |
|------|----------|
| **KGCP** (임상시험 관리기준) | 식약처 고시 |
| **약사법** | 제30조~34조 (임상시험 관련) |
| **PIPA** (개인정보 보호법) | 개인정보 수집·이용·제3자 제공 |
| **생명윤리법** | 인체유래물 연구, 유전체 분석 |
| **MFDS 가이드라인** | 시험 유형별 개별 가이드라인 (BE, DDI, FIH 등) |

### 미국/유럽 규제 (참조)

| 규정 | 적용 범위 |
|------|----------|
| **FDA Guidance** | DDI, BE, FE, FIH 등 시험 유형별 가이드라인 |
| **EMA Guideline** | FIH 위험 경감, DDI 평가, BE 등 |

---

## MCP 도구

이 프로젝트에서 활용하는 외부 데이터 소스:

| MCP 서버 | 용도 |
|----------|------|
| **Clinical Trials** (ClinicalTrials.gov API v2) | 유사 시험 검색, 프로토콜 설계 참고, 엔드포인트 분석 |
| **PubMed** | 문헌 검색 — PK/PD, 안전성, 용량 설정 근거 |
| **ICD-10** | ICD-10-CM/PCS 코드 조회 — 적응증 코딩 |
| **DailyMed/openFDA** (예정) | 약물 라벨 정보 — 허가사항, 약물상호작용 섹션 |
| **MFDS** (예정) | 임상시험 승인현황, 가이드라인 검색 |

---

## 진행 현황 및 향후 계획

### 완료된 항목

- ✅ **하네스 7-에이전트 재구성** — 역할 기반 구조 (조사 4 + 작성 2 + 검토 1)
- ✅ **Commands 구현** — 7개 단계별 commands (`/research`, `/design`, `/synopsis`, `/compare`, `/protocol`, `/review`, `/icf`)
- ✅ **Sample size 코드 템플릿** — 7개 디자인별 Python 스크립트 (`.claude/scripts/sample_size/`)
- ✅ **FIH 산출 코드** — 초기 용량 산출 + 용량 증량 스킴 (`.claude/scripts/fih/`)
- ✅ **규제 가이드라인 라이브러리 구축** — ICH/FDA/EMA/MFDS 가이드라인 + 국내 법령 + 시험 유형별 cross-agency 비교표 (`.claude/references/guidelines/`)
- ✅ **E2E 검증** — 실제 시험 문서 1건 생성 및 다중 에이전트 리뷰 (`e2e/` 디렉토리)

### 진행 중·향후 계획

1. **MCP 도구 확장** — DailyMed/openFDA, MFDS 의약품안전나라 API 통합
2. **추가 cross-agency 비교** — ADME, 집단 PK(PopPK), 신장/간 기능 저하, 소아 시험 비교표
3. **ICH 원문 수집** — 사용자 PDF 제공이 필요한 항목 보강 (`.claude/references/guidelines/needs_user_input.md` 참조)
4. **Plugin 변환** — 검증 완료된 하네스를 Claude Code plugin으로 변환하여 범용 배포

---

## 라이선스

Private - All rights reserved.
