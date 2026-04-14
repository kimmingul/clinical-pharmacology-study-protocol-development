---
name: trial-doc-orchestrator
description: "임상약리 임상시험 문서(계획서, 동의설명서, 동의서, 개인정보 동의서) 개발을 조율하는 오케스트레이터. 8개 전문 에이전트를 10단계 파이프라인으로 실행한다. 임상시험 문서 작성, 계획서 개발, 프로토콜 개발, 동의설명서 개발, 시험 문서 생성 요청 시 사용. 후속 작업: 문서 수정, 계획서 수정, 동의설명서 수정, 프로토콜 업데이트, 문서 보완, 다시 실행, 재실행, 특정 섹션만 다시, 이전 결과 개선, QA 피드백 반영 요청 시에도 반드시 이 스킬을 사용."
---

# Trial Document Orchestrator

8개 전문 에이전트와 10단계 워크플로우로 임상약리 임상시험 문서를 개발한다. 메인 에이전트가 전체를 조율하고, 사용자 검토 게이트를 통해 단계 진행을 제어한다.

> 이 스킬은 **메인 에이전트(Claude 자신)**가 직접 실행한다. 사용자와의 대화, 정보 수집, 서브 에이전트 호출 모두 메인 에이전트가 수행한다.

## Command → Phase 매핑

| Command | Phase | 기능 | 전제 조건 |
|---------|-------|------|----------|
| `/research` | 2-3 | 병렬 자료 수집 + 사용자 검토 게이트 | 약물명 + 시험 유형 |
| `/design` | 4-5 | 대화형 설계 협의 + 통계 설계 | 자료 조사 완료 |
| `/synopsis` | 6 | Synopsis 생성 (인자로 변형 지정 가능) | 설계 협의 완료 |
| `/compare` | 6 | 여러 Synopsis 비교표 제시 | Synopsis 2개 이상 |
| `/protocol` | 8 | Full Protocol 작성 | Synopsis 승인 완료 (Phase 7) |
| `/review` | 9 | 다중 에이전트 병렬 리뷰 | Protocol 작성 완료 |
| `/icf` | 10 | ICF 작성 (별도 명령 필요) | Protocol 존재 |

> 전체 파이프라인 실행 요청 시 Phase 1→10 순서로 진행하되, 각 게이트에서 반드시 사용자 승인을 받는다. 개별 Command로 특정 Phase만 실행할 수도 있다.

## 에이전트 구성

### 조사 에이전트 (Research)

| 에이전트 | model | 역할 | 참여 | 스킬 |
|---------|-------|------|------|------|
| clinical-pharmacologist | sonnet | PK(반감기·변동성·생체이용률), 대사 경로 정성, 약물상호작용 기전, 용량 근거, FIH 초기 용량 | 항상 | clinical-research |
| translational-scientist | sonnet | PD 바이오마커, PK-PD 모델링, 약물유전체학(PG), 대사체학, 수용체 점유율 | **조건부** — BE/FE 불참 | clinical-research |
| regulatory-expert | sonnet | MFDS/FDA 가이드라인, 약물 라벨(PG 섹션 추출 포함), ICD-10 | 항상 | clinical-research |
| clinician | sonnet | 선정/제외 기준, 안전성 프로파일, 임상 절차 | 항상 | clinical-research |
| biostatistician | sonnet | 연구설계 옵션, sample size 계산 | 항상 (Phase 5) | — |

### 작성 에이전트 (Writing)

| 에이전트 | model | 역할 | 스킬 |
|---------|-------|------|------|
| protocol-writer | opus | Synopsis + 자료 기반 Full Protocol | protocol-drafting |
| icf-writer | opus | 계획서 기반 동의문서 | icf-drafting |

### 검토 에이전트 (Review)

| 에이전트 | model | 역할 | 스킬 |
|---------|-------|------|------|
| qa-reviewer | opus | 개별 리뷰 취합, 우선순위 분류, 수정 조율 | regulatory-review |

> **실행 방식**: 모든 에이전트는 `general-purpose` 타입으로 호출한다. 에이전트 정의(`${CLAUDE_PLUGIN_ROOT}/agents/*.md`)와 스킬을 Read로 로드하는 방식이다.

## 산출물

| 파일 | 내용 |
|------|------|
| `_workspace/00_input/trial_info.md` | 수집된 입력 정보 |
| `_workspace/01_research_report.md` | 통합 자료 조사 보고서 |
| `_workspace/02_synopsis.md` | Synopsis (변형: `synopsis_*.md`) |
| `_workspace/03_protocol_draft.md` | Full Protocol |
| `_workspace/04_icf_draft.md` | 동의설명서/동의서/개인정보 동의서 |
| `_workspace/review/review_{agent}.md` | 에이전트별 리뷰 |
| `_workspace/review/qa_review_report.md` | QA 통합 리뷰 보고서 |

## 워크플로우

### Phase 0: 컨텍스트 확인

Bash로 `ls _workspace/ 2>/dev/null` 실행하여 실행 모드를 결정한다:

- **`_workspace/` 미존재** → **초기 실행**. Phase 1로 진행
- **`_workspace/` 존재 + 부분 수정 요청** → **부분 재실행**. 의존성 규칙:
  - "자료 조사 보완" → Phase 2-3부터 하류 전체 재실행
  - "설계 변경" → Phase 4부터
  - "synopsis 수정" → Phase 6부터
  - "계획서 수정" → Phase 8 (protocol-writer) → Phase 9 (review)
  - "동의설명서 수정" → Phase 10 (icf-writer)만
  - "리뷰 다시" → Phase 9만
- **`_workspace/` 존재 + 새 시험 정보** → Bash로 `mv _workspace/ _workspace_$(date +%Y%m%d_%H%M%S)/` 후 Phase 1

### Phase 1: 입력 수집 (메인 에이전트 직접)

> 서브 에이전트가 아닌 **메인 에이전트가 사용자와 직접 대화**한다. 모든 필수 정보가 수집될 때까지 Phase 2로 진행하지 않는다.

**시험 유형에 따른 필수 항목:**

| 항목 | FIH/SAD/MAD (신약) | DDI/BE/FE/QTc/ADME (허가 약물) |
|------|-------------------|-------------------------------|
| 약물명 | **필수** | **필수** |
| 시험 유형 | **필수** | **필수** |
| 적응증 | **필수** | **필수** |
| 시험 단계 | **필수** | **필수** (통상 Phase 1) |
| 약물 계열/MOA | **필수** | 권장 (문헌에서 확인 가능) |
| IB 파일 | **필수** (신약의 유일한 1차 자료) | 불필요 |
| 의뢰자명 | 권장 | 권장 |
| 투여 경로/제형 | 권장 | 권장 |

> **참고**: 유전체/인체유래물(PG·대사체) 분석 포함 여부는 Phase 1 입력이 아닌 **Phase 4 설계 협의**에서 translational-scientist 조사 결과를 바탕으로 결정한다. Phase 1에서 미리 결정하면 배경 자료를 보기 전에 판단을 강요하게 된다.

**필수 정보 확보 시:**
1. `mkdir -p _workspace/00_input`
2. Write로 `_workspace/00_input/trial_info.md` 저장
3. IB 제공 시 `_workspace/00_input/`에 복사

### Phase 2: 병렬 자료 수집

여러 조사 에이전트를 **병렬로** 호출한다. 검색 영역이 분리되어 중복이 없다. **clinical-pharmacologist, regulatory-expert, clinician은 항상 참여**하며, **translational-scientist는 BE/FE 외 시험에서만 참여**한다.

**clinical-pharmacologist 호출:**
```
Agent(
  description: "PK/PD 자료 수집 및 약동학 분석",
  model: "sonnet",
  name: "clinical-pharmacologist",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/clinical-pharmacologist.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/clinical-research/SKILL.md를 Read하여 조사 절차를 따르라.

[담당 영역: PK/PD 전문가 파트]
- PubMed: PK 파라미터, 대사 경로(CYP), 수송체, 약물상호작용
- ClinicalTrials.gov: 기존 유사 시험 설계, 용량, 엔드포인트
{FIH 시: - IB 분석: _workspace/00_input/ 에서 IB를 Read하여 비임상 PK/독성/약리 추출, 초기 용량 산출}

시험 정보:
- 약물: {약물명}
- 적응증: {적응증}
- 시험 단계: {단계}
- 시험 유형: {유형}
- 약물 계열/MOA: {MOA}

산출물을 _workspace/01_research_cp.md에 Write하라."
)
```

**regulatory-expert 호출 (병렬):**
```
Agent(
  description: "규제 자료 수집 및 가이드라인 분석",
  model: "sonnet",
  name: "regulatory-expert",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/regulatory-expert.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/clinical-research/SKILL.md를 Read하여 조사 절차를 따르라.

[담당 영역: 규제전문가 파트]
- MFDS/FDA/EMA 가이드라인, 시험 유형별 규제 요건
- 약물 라벨 정보 (허가사항, 약물상호작용 섹션)
- ICD-10 적응증 코딩
- MFDS 임상시험 승인현황

시험 정보:
- 약물: {약물명}
- 적응증: {적응증}
- 시험 단계: {단계}
- 시험 유형: {유형}

산출물을 _workspace/01_research_reg.md에 Write하라."
)
```

**clinician 호출 (항상 참여):**
```
Agent(
  description: "임상적 판단 및 안전성 프로파일 자료 수집",
  model: "sonnet",
  name: "clinician",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/clinician.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/clinical-research/SKILL.md를 Read하여 조사 절차를 따르라.

[담당 영역: 임상의사 파트]
- 선정/제외 기준의 임상적 타당성
- 안전성 프로파일 체계적 수집 (AE/SAE, class effect)
- 안전성 모니터링 계획 및 이상반응 관리
- 중지 기준(stopping rules) 임상 근거

시험 정보: {동일}

_workspace/01_references/safety/ 디렉토리에 개별 안전성 reference 파일을 생성한 후,
요약 보고서를 _workspace/01_research_clin.md에 Write하라."
)
```

**translational-scientist 호출 (BE/FE 외 시험, 조건부):**

BE/FE 시험이 아닌 경우 (FIH/SAD/MAD/DDI/QTc/ADME/Special Pop)에 호출한다. 시험 유형별 조사 깊이는 `${CLAUDE_PLUGIN_ROOT}/skills/clinical-research/SKILL.md`의 "시험 유형별 오믹스/PD 우선순위" 표에 따른다:
```
Agent(
  description: "PD/오믹스 자료 수집 (PK-PD, PG, 대사체)",
  model: "sonnet",
  name: "translational-scientist",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/translational-scientist.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/clinical-research/SKILL.md를 Read하여 조사 절차와 시험 유형별 우선순위를 확인하라.

[담당 영역: 중개의학·PD/오믹스 파트]
- PD 바이오마커 후보 발굴 (작용 기전 기반), 측정 방법, 검증 상태
- PK-PD 모델링 문헌 (Emax, sigmoid Emax, indirect response 등)
- 수용체 점유율 자료 (PET tracer, 표적 결합; CNS/항암제 중심)
- 약물유전체학: CYP/표적 다형성, 한국인 대립유전자 빈도, 라벨 PG 권고
- 대사체학: 인체 특이 대사체(MIST), 내인성 바이오마커 (해당 시)

시험 정보: {동일}

_workspace/01_references/{pd_biomarkers,pharmacogenomics,metabolomics}/ 디렉토리에
개별 reference 파일을 생성한 후, 요약 보고서를 _workspace/01_research_ts.md에 Write하라.

★ MCP 도구 한계 솔직 표시: PharmGKB/HMDB 직접 접근 불가 시 '[데이터베이스 직접 접근 불가 — PubMed/라벨 기반]' 명시."
)
```

### Phase 3: 자료 종합 + 사용자 검토 게이트

1. 메인 에이전트가 각 에이전트의 산출물을 Read로 읽는다:
   - `_workspace/01_research_cp.md`
   - `_workspace/01_research_reg.md`
   - `_workspace/01_research_clin.md`
   - `_workspace/01_research_ts.md` (BE/FE 외 시험)
2. 핵심 발견사항을 통합하여 `_workspace/01_research_report.md`에 Write한다
3. 사용자에게 **핵심 발견사항 요약**을 제시한다

**사용자 선택지:**
- **승인** → Phase 4로 진행
- **추가 조사 요청** → 요청 내용에 따라 **가장 적합한 에이전트**를 재호출:
  - PK/약물/유사 시험 → clinical-pharmacologist
  - PD/약력학/약물유전체/대사체 → translational-scientist
  - 규제/가이드라인/라벨 → regulatory-expert
  - 임상적 판단/안전성 → clinician
- **자료 직접 제공** → 사용자 제공 정보를 통합 보고서에 추가

추가 조사 후 다시 사용자 검토 → **승인될 때까지 반복**.

### Phase 4: 대화형 설계 협의 (메인 에이전트 직접)

> 이 단계는 **서브 에이전트가 아닌 메인 에이전트가 사용자와 직접 대화**하며 설계 결정을 내린다. 상세 절차는 `${CLAUDE_PLUGIN_ROOT}/commands/design.md`를 참조한다.

수집된 자료를 기반으로 설계 옵션을 제시하고, 사용자와 함께 결정한다:

1. **선정/제외기준 (최우선)**: `${CLAUDE_PLUGIN_ROOT}/references/templates/inclusion_exclusion_criteria.md` 표준 템플릿을 사용자에게 제시하고 항목별 협의 (시험별 커스터마이징 가이드 A~F)
2. **연구설계 옵션**: 시험 유형에 따른 후보 설계를 장단점과 함께 제시
   - Crossover 유형: one-sequence, 2x2, 2x3, 2x4, 4x4 (Williams), 6x3
   - Parallel, Adaptive 등
   - 유사 시험 사례 참조하여 근거 제시
3. **PK 채혈 시점**: 예상 반감기 기반 시점 설계
4. **평가변수**: 1차/2차/탐색적
5. **유효성/약력학(PD) 평가 항목**: 시험 유형별 PD 마커 (DDI의 GMR, QTc의 ddQTcF, DDI/ADME의 내인성 바이오마커 등)
6. **안전성 평가 항목**: 활력징후, ECG, 실험실 검사 등
7. **유전체/대사체 분석 계획** (BE/FE 외): PG 분석 대상 유전자, 대사체 측정 방법, 인체유래물 보관 정책 (생명윤리법 적용 검토, ICF Part 4와 연계)
8. **기타**: washout 기간, 투여 조건, 식이 조건 등

각 항목에 대해 사용자 결정을 받은 뒤 `_workspace/00_input/design_decisions.md`에 기록하고 Phase 5로 진행한다.

### Phase 5: 통계 설계 (biostatistician)

```
Agent(
  description: "Sample size 계산 및 통계 설계",
  model: "sonnet",
  name: "biostatistician",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/biostatistician.md를 Read하여 역할과 원칙을 숙지하라.

Phase 4에서 확정된 설계:
- 연구설계: {설계 유형}
- 1차 평가변수: {변수}
- 기타: {washout, 코호트 수 등}

${CLAUDE_PLUGIN_ROOT}/scripts/sample_size/ 디렉토리의 해당 코드 템플릿을 Read하여 파라미터를 채워 Bash로 실행하라.
실행된 코드 전체와 결과를 사용자에게 제시하라.

산출물 형식:
- 코드 (어떤 템플릿을 사용했는지)
- 파라미터 설정 근거
- 계산 결과 (대상자 수, 검정력)
- 무작위화 방법
- 통계 분석 방법 요약"
)
```

메인 에이전트가 결과를 사용자에게 제시. 파라미터 변경 요청 시 즉시 재실행.

### Phase 6: Synopsis 작성

메인 에이전트가 Phase 1-5의 모든 결정 사항을 종합하여 Synopsis를 작성한다.

- 기본 출력: `_workspace/02_synopsis.md`
- `/synopsis crossover 2x2` 등 인자 지정 시: `_workspace/synopsis_crossover_2x2.md` 등 변형별 파일
- `/compare` 시: 여러 synopsis를 비교표로 제시

사용자에게 Synopsis를 제시하고 검토를 요청한다.

### Phase 7: Synopsis 승인 (Hard Gate)

> **이 게이트는 건너뛸 수 없다.** 사용자가 명시적으로 "승인", "진행", "OK" 등의 의사를 밝혀야 Phase 8로 진행한다.

사용자가 수정을 요청하면 Synopsis를 수정하고 다시 검토를 요청한다. 승인될 때까지 반복.

### Phase 8: Full Protocol 작성

```
Agent(
  description: "임상시험 계획서 작성",
  model: "opus",
  name: "protocol-writer",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/protocol-writer.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/protocol-drafting/SKILL.md를 Read하여 작성 가이드를 따르라.
상세 템플릿이 필요하면 ${CLAUDE_PLUGIN_ROOT}/skills/protocol-drafting/references/protocol-template.md도 Read하라.

[입력 — 둘 다 반드시 Read하라]
1. Synopsis (설계의 기준): _workspace/02_synopsis.md
2. 자료 보고서 (보충 데이터): _workspace/01_research_report.md

시험 정보:
- 약물: {약물명}
- 적응증: {적응증}
- 시험 단계: {단계}
- 시험 유형: {유형}
- 의뢰자: {의뢰자명}
{추가 요구사항}

Synopsis에서 확정된 설계 결정(연구설계, 평가변수, 대상자 수, 통계 방법)은
그대로 보존하라. 자료 보고서의 데이터로 배경, 용량 근거, 안전성 정보를 보충하라.

산출물을 _workspace/03_protocol_draft.md에 Write하라.
문서가 매우 길면 여러 번의 Write/Edit 호출로 나누어 작성해도 된다."
)
```

### Phase 9: 다중 에이전트 리뷰

4-5명의 전문가가 **병렬로** 계획서를 리뷰한 후, qa-reviewer가 취합한다. translational-scientist는 BE/FE 외 시험에서만 참여한다.

**Step 1: 병렬 리뷰** — 각 에이전트를 병렬 호출한다:

```
Agent(
  description: "{에이전트 역할} 관점의 계획서 리뷰",
  model: "sonnet",
  name: "{agent-name}",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/{agent-name}.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/regulatory-review/SKILL.md를 Read하여 '개별 리뷰어 절차' 섹션을 따르라.

대상 문서: _workspace/03_protocol_draft.md를 Read하라.
참조 자료: _workspace/01_research_report.md, _workspace/02_synopsis.md도 Read하라.

[리뷰 초점: {에이전트별 초점 — 아래 표 참조}]

산출물을 _workspace/review/review_{agent_name}.md에 Write하라."
)
```

리뷰어별 초점:

| 에이전트 | 초점 | 참여 |
|---------|------|------|
| clinical-pharmacologist | PK 설계, 채혈 시점, 약물상호작용 평가, 용량 근거, washout | 항상 |
| translational-scientist | PD 평가 섹션, PK-PD 모델링, PG 분석 계획, 대사체 분석, ICF Part 4 정합성 | **BE/FE 외** |
| clinician | 선정/제외 기준, 안전성 모니터링, 이상반응 관리, 중지 기준 | 항상 |
| regulatory-expert | ICH E6(R3) Annex 1 필수 요소, MFDS/FDA 준수, 규제 용어 | 항상 |
| biostatistician | 통계 섹션, sample size, 무작위화, 분석 방법, 결측치 처리 | 항상 |

**Step 2: QA 취합**

```
Agent(
  description: "리뷰 취합 및 우선순위 분류",
  model: "opus",
  name: "qa-reviewer",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/qa-reviewer.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/regulatory-review/SKILL.md를 Read하여 'QA 취합 절차' 섹션을 따르라.

다음 파일들을 모두 Read하라:
- _workspace/review/review_clinical_pharmacologist.md
- _workspace/review/review_regulatory_expert.md
- _workspace/review/review_biostatistician.md
- _workspace/review/review_clinician.md
- _workspace/review/review_translational_scientist.md (존재하면 — BE/FE 외 시험)
- _workspace/03_protocol_draft.md (원문 대조용)

산출물을 _workspace/review/qa_review_report.md에 Write하라."
)
```

**Step 3: Critical 자동 수정 (조건부)**

QA 보고서를 Read하여 Critical 사항을 확인한다.

Critical 존재 시:
1. Critical 위치(어느 섹션)를 파악한다
2. protocol-writer를 Agent로 재호출하여 수정:
   ```
   [수정 모드]
   이전 산출물: _workspace/03_protocol_draft.md를 Read하고, 아래 QA Critical 사항을 반영하여 수정하라.

   QA 피드백 (Critical 사항):
   - [C-1] {제목}: {내용} → 권고: {수정 방향}
   ...

   수정된 문서를 같은 파일에 Write하라.
   ```
3. 수정 후 Phase 9 리뷰를 1회 재실행한다
4. **최대 1회만**. 재검토 후에도 Critical이 있으면 사용자에게 보고한다

Critical이 없으면 사용자에게 결과 보고.

### Phase 10: ICF 작성 (별도 `/icf` 명령)

> Phase 8-9 완료 후 자동 실행되지 않는다. 사용자가 `/icf`로 명시적으로 요청해야 한다.

전제 조건: `_workspace/03_protocol_draft.md`가 존재해야 한다.

```
Agent(
  description: "동의설명서/동의서 작성",
  model: "opus",
  name: "icf-writer",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/icf-writer.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/icf-drafting/SKILL.md를 Read하여 작성 가이드를 따르라.
상세 템플릿이 필요하면 ${CLAUDE_PLUGIN_ROOT}/skills/icf-drafting/references/icf-template.md도 Read하라.

★ 필수: _workspace/00_input/design_decisions.md를 Read하여 '유전체/대사체 분석 계획' 섹션을 확인하라.
- PG 분석·대사체 분석·잔여 검체 보관 중 하나라도 포함 → 생명윤리법에 따른 Part 4(선택 동의) 작성
- 전부 미포함 → Part 1-3만 작성

[입력]
계획서: _workspace/03_protocol_draft.md를 Read하라.
배경: _workspace/01_research_report.md도 참조하라.

산출물을 _workspace/04_icf_draft.md에 Write하라."
)
```

## 부분 재실행 시 피드백 전달

사용자의 수정 요청을 에이전트 프롬프트에 주입하는 형식:

```
[수정 모드]
이전 산출물: _workspace/{파일명}을 Read하고, 아래 사용자 피드백을 반영하여 수정하라.

사용자 피드백:
"{사용자의 원문 피드백}"

수정된 문서를 같은 파일에 Write하라.
```

## Gotchas

- **Phase 7 게이트를 건너뛰지 말 것**: Synopsis 승인 없이 Protocol을 작성하면 대규모 재작업이 발생한다
- **Phase 2에서 에이전트 검색 영역이 겹치면 안 된다**:
  - clinical-pharmacologist: PubMed/ClinicalTrials.gov 기반 PK, 대사 경로 정성, DDI 기전
  - translational-scientist: PubMed 기반 PD 바이오마커, PK-PD 모델, PG(다형성, 한국인 빈도), 대사체
  - regulatory-expert: 가이드라인/라벨(PG 섹션 추출 포함)/ICD-10
  - clinician: 안전성 프로파일, 선정/제외 임상 근거
- **translational-scientist 호출 조건**: BE/FE는 불참(PG/PD 의미 낮음). 그 외 시험(FIH/SAD/MAD/DDI/QTc/ADME/Special Pop)에서 참여. 우선순위는 `${CLAUDE_PLUGIN_ROOT}/skills/clinical-research/SKILL.md`의 "시험 유형별 오믹스/PD 우선순위" 표에 따른다
- **clinician은 항상 참여**: 건강한 성인 시험에서도 안전성 프로파일 체계적 수집은 필수
- **Phase 9 리뷰에서 translational-scientist 누락 금지**: BE/FE 외 시험에서 PG/PD 섹션을 검토하는 리뷰어가 빠지면 계획서-ICF 간 PG/오믹스 일관성 검증 공백
- **Protocol 입력 누락**: protocol-writer에게 Synopsis만 주고 research report를 빠뜨리면 배경/근거가 빈약해진다. 항상 둘 다 제공
- **ICF는 자동 실행되지 않는다**: 반드시 `/icf` 명령이 있어야 Phase 10 진행
- **산출물 파일 미생성**: 에이전트가 실패하면 해당 파일이 없다. 다음 단계 진행 전 Bash로 `ls _workspace/` 확인
- **대용량 출력 잘림**: 에이전트 산출물을 Read로 확인하여 불완전하면 재호출하여 보완
- **Reference 날조 금지**: 에이전트가 MCP 검색 결과에서 확인된 것만 인용해야 한다. PMID/NCT 없이 인용하면 신뢰성이 훼손

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| MCP 도구 호출 실패 (일시적) | 1회 재시도 |
| MCP 도구 호출 실패 (API 한도) | "[미수집 - API 한도]" 표시, 진행 |
| 에이전트 응답 없음/에러 | 1회 재시도. 재실패 시 사용자에게 알리고 진행 |
| 검색 결과 0건 | 약물 계열/MOA로 확장 검색, "[공개 데이터 없음]" 표시 |
| 산출물 불완전 (출력 잘림) | Read로 확인 후 에이전트 재호출하여 누락 섹션 보완 |
| 리뷰어 간 상충 의견 | qa-reviewer가 양쪽 근거를 비교하여 사용자에게 판단 요청 |
