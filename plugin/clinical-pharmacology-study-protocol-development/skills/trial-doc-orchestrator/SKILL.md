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
| `/review` | 9 | 다중 에이전트 병렬 리뷰 (v3: 수렴 루프) | Protocol 작성 완료 |
| `/finalize` | 9.5 | (v3) T0 최종 가드레일 — doc_lint strict + citation + dose | Protocol/ICF 초안 존재 |
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
| `_workspace/review/qa_fix_plan.md` | (v3) 수렴 루프 각 반복의 수정 계획 |
| `_workspace/00_input/goal_spec.json` | (v3) 기계 판독형 성공명세 (채점·가드레일 기준) |
| `_workspace/00_input/ib_manifest.json` | (v3) IB 해시·허용 섹션·기밀 플래그 (FIH) |
| `_workspace/verification/citation_audit.json` | (v3) 인용(PMID/NCT/setid/URL) 독립 검증 결과 |
| `_workspace/verification/source_provenance.json` | (v3) 외부 fetch 스냅샷 해시·조회일·URL |
| `_workspace/pipeline_manifest.json` | 재현성 매니페스트 (단계별 provenance) |

## 재현성 매니페스트 (provenance — 권장)

규제 문서의 추적성을 위해, 각 산출물 생성 단계 직후 `${CLAUDE_PLUGIN_ROOT}/scripts/qa/pipeline_manifest.py`로 실행 이력을 기록한다. 매니페스트는 단계·에이전트·모델·입력/출력 파일과 그 SHA-256·UTC 타임스탬프·하네스 버전을 남겨, "어느 모델·버전이 어떤 입력으로 어떤 산출물을 만들었는가"를 사후에 확인할 수 있게 한다.

```bash
# Phase 1 입력 확정 직후 1회
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/qa/pipeline_manifest.py init --trial "{약물}+{시험유형}"

# 산출물을 만드는 각 Phase(2/3 조사, 5 통계, 6 synopsis, 8 protocol, 9 review, 10 icf) 직후
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/qa/pipeline_manifest.py record \
  --phase 8 --agent protocol-writer --model opus \
  --output _workspace/03_protocol_draft.md \
  --inputs _workspace/02_synopsis.md _workspace/01_research_report.md \
  --note "{선택: 수정/재실행 사유}"
```

> 부분 재실행 시에도 record를 추가하면 출력 SHA-256 변화로 어떤 산출물이 갱신되었는지 추적된다. 스키마: `${CLAUDE_PLUGIN_ROOT}/references/schemas/pipeline_manifest.schema.json`.

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
3. **goal_spec 작성 (v3)**: `${CLAUDE_PLUGIN_ROOT}/references/schemas/goal_spec.example.json`을 참고하여 이번 시험의 성공명세 `_workspace/00_input/goal_spec.json`을 작성한다 (drug·trial_type·primary_objective·estimand·acceptable_ci_bounds·target_power·required_ich_sections·retention_years_min·pg_or_biobank_required). 이 파일은 채점·가드레일·수렴 루프의 기준이 되며 Phase 4에서 갱신·재승인할 수 있다.
4. IB 제공 시 (FIH/SAD/MAD) — **zero-trust 최소권한 (v3)**:
   - IB를 `_workspace/00_input/`에 복사한다.
   - **IB manifest 작성**: `_workspace/00_input/ib_manifest.json`에 파일명·SHA-256·비공개(confidential) 플래그·에이전트별 허용 섹션을 기록한다 (예: clinical-pharmacologist=비임상 PK/독성/약리 섹션만). IB는 **기밀 자료**이므로, 필요한 에이전트에게 필요한 섹션만 인용하도록 프롬프트를 제한하고, IB 원문을 외부 도구(WebFetch·외부 API)로 전송하지 않는다. 상세 정책은 `SECURITY.md` 참조.

### Phase 2: 병렬 자료 수집

여러 조사 에이전트를 **병렬로** 호출한다. 검색 영역이 분리되어 중복이 없다. **clinical-pharmacologist, regulatory-expert, clinician은 항상 참여**하며, **translational-scientist는 BE/FE 외 시험에서만 참여**한다.

#### Phase 2 실행 순서 (Dependency Edge)

Phase 2는 병렬이지만 한 가지 dependency edge가 있습니다:

```
regulatory-expert (라벨 PG 추출 → _workspace/00_input/label_pgx.md 작성)
        │
        └──→ translational-scientist (PG 마커·라벨 PGx 의존)

clinical-pharmacologist ────────────────→ (독립, 즉시 spawn)
clinician ─────────────────────────────→ (독립, 즉시 spawn)
```

**2-wave 패턴**:
- **Wave 1 (즉시 spawn)**: clinical-pharmacologist, regulatory-expert, clinician (BE/FE 외이면 regulatory-expert에게 label_pgx.md 작성 요청 포함)
- **Wave 2 (regulatory-expert의 `_workspace/00_input/label_pgx.md` 완성 후)**: translational-scientist (BE/FE 외 시험인 경우에만)

> **오케스트레이터 지시**: regulatory-expert 프롬프트에 "라벨 PG 섹션을 `_workspace/00_input/label_pgx.md`에 별도 저장하라"를 명시한다. regulatory-expert 완료 후 translational-scientist를 spawn하며, 이때 프롬프트에 "label_pgx.md가 존재하면 Read하여 활용하라"를 포함한다. BE/FE 시험이면 Wave 2 자체를 생략한다.

**clinical-pharmacologist 호출:**
```
Agent(
  description: "PK/PD 자료 수집 및 약동학 분석",
  model: "opus",
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

**regulatory-expert 호출 (병렬, Wave 1):**
```
Agent(
  description: "규제 자료 수집 및 가이드라인 분석",
  model: "opus",
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

★ 라벨 PG 섹션 별도 저장 (translational-scientist 인계용):
약물 라벨에 Pharmacogenomics(PGx) 섹션이 있으면 해당 내용을 _workspace/00_input/label_pgx.md에 별도 Write하라.
(없으면 '본 약물 라벨에 PGx 섹션 없음' 1줄을 해당 파일에 Write하라 — translational-scientist가 파일 존재 여부로 완료를 확인한다.)

산출물을 _workspace/01_research_reg.md에 Write하라."
)
```

**clinician 호출 (항상 참여):**
```
Agent(
  description: "임상적 판단 및 안전성 프로파일 자료 수집",
  model: "opus",
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

**translational-scientist 호출 (BE/FE 외 시험, 조건부 — Wave 2):**

> **Wave 2**: regulatory-expert가 완료되어 `_workspace/00_input/label_pgx.md`가 생성된 후에 호출한다. BE/FE 시험이면 이 에이전트 호출 자체를 생략한다.

BE/FE 시험이 아닌 경우 (FIH/SAD/MAD/DDI/QTc/ADME/Special Pop)에 호출한다. 시험 유형별 조사 깊이는 `${CLAUDE_PLUGIN_ROOT}/skills/clinical-research/SKILL.md`의 "시험 유형별 오믹스/PD 우선순위" 표에 따른다:
```
Agent(
  description: "PD/오믹스 자료 수집 (PK-PD, PG, 대사체)",
  model: "opus",
  name: "translational-scientist",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/translational-scientist.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/clinical-research/SKILL.md를 Read하여 조사 절차와 시험 유형별 우선순위를 확인하라.

[담당 영역: 중개의학·PD/오믹스 파트]
- PD 바이오마커 후보 발굴 (작용 기전 기반), 측정 방법, 검증 상태
- PK-PD 모델링 문헌 (Emax, sigmoid Emax, indirect response 등)
- 수용체 점유율 자료 (PET tracer, 표적 결합; CNS/항암제 중심)
- 약물유전체학: CYP/표적 다형성, 한국인 대립유전자 빈도, 라벨 PG 권고
- 대사체학: 인체 특이 대사체(MIST), 내인성 바이오마커 (해당 시)

★ 라벨 PG 선행 자료: _workspace/00_input/label_pgx.md가 존재하면 Read하여 regulatory-expert가 추출한 라벨 PGx 섹션을 활용하라. 중복 수집 불필요.

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
3. **zero-trust 인용 검증 (v3)** — Bash로 인용을 독립 검증한다:
   ```bash
   PY=${CLAUDE_PLUGIN_ROOT}/scripts/.venv/bin/python   # 없으면 python3
   $PY ${CLAUDE_PLUGIN_ROOT}/scripts/qa/citation_verify.py audit \
       _workspace/01_research_report.md _workspace/01_references/**/*.md \
       --workspace _workspace --online    # 네트워크 불가 시 --online 생략(형식 검증만)
   ```
   `citation_audit.json`의 `format_fail`/`not-found`가 있으면 해당 인용을 `[출처 미확인]`으로 강등하고, dose/안전성 등 load-bearing 근거에는 사용하지 않는다.
4. 사용자에게 **핵심 발견사항 요약** + 인용 검증 결과(검증/미검증 수)를 제시한다

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
  model: "opus",
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

#### Sentinel 파일 정책 (Hard Gate 무결성 보장)

사용자가 Synopsis를 **명시적으로 승인**하면 즉시 아래를 수행한다:

```bash
# sentinel 파일 생성 (부분 재실행 시 stale 검출용)
mkdir -p _workspace
echo "approved_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
synopsis_file: _workspace/02_synopsis.md
synopsis_variant: {승인된 변형 ID, 기본이면 'default'}
drug: {약물명}
trial_type: {시험 유형}
git_sha_or_hash: $(git rev-parse --short HEAD 2>/dev/null || md5sum _workspace/02_synopsis.md | cut -c1-8)" \
> _workspace/.synopsis_approved
```

**하류 명령(protocol, review, icf)은 실행 시작 시 sentinel을 검사한다:**

| 상태 | 조치 |
|------|------|
| `_workspace/.synopsis_approved` 미존재 | 실행 거부 — "Synopsis 승인이 필요합니다. `/synopsis` 실행 후 명시 승인해주세요" 안내 |
| sentinel 존재, 단 `_workspace/02_synopsis.md`(또는 해당 변형 파일)의 수정시각이 sentinel보다 새로움 | 실행 거부 — "Synopsis가 sentinel 이후 수정되었습니다. `/synopsis` 재확인 후 다시 승인해주세요" 안내 |
| sentinel 존재 + mtime 정상 | 정상 진행 |

> **목적**: 자연어 응답에만 의존하던 Phase 7 게이트를 파일시스템 sentinel로 보강하여 부분 재실행 시 하류 산출물의 stale 상태를 자동 검출한다.

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
  model: "opus",
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

> **Multi-LLM 패널 (v4, 조건부)**: `_workspace/llm/routing_plan.json`이 있고 `multi_llm=true`이면, qa-reviewer 호출 **전에** 이종 벤더 critic 패널을 실행하여 `review_synthesis.json`을 만든다(상세: `${CLAUDE_PLUGIN_ROOT}/commands/review.md` Step 2.5). 없으면 단일‑LLM(Claude)로 진행(v3 동등). 기밀/안전핵심은 egress 게이트가 차단하고 host qa-reviewer가 해당 역할을 대체한다.
> ```bash
> PY=${CLAUDE_PLUGIN_ROOT}/scripts/.venv/bin/python
> $PY ${CLAUDE_PLUGIN_ROOT}/scripts/llm/review_panel.py plan --routing _workspace/llm/routing_plan.json \
>     --roles ${CLAUDE_PLUGIN_ROOT}/references/llm/review_roles.json --draft _workspace/03_protocol_draft.md \
>     --host "$(${PY} -c "import json;print(json.load(open('_workspace/llm/routing_plan.json'))['host'])")" --workspace _workspace
> # egress 선언은 시험 유형으로: 허가약물 공개(DDI/BE/FE/QTc)만 `--classification REGULATORY_PUBLIC`,
> # FIH/SAD/MAD·IB 존재 시 생략(fail-closed). ask_model.sh가 ib_manifest.confidential을 강제 floor로 적용(이중 안전).
> CLASS=""   # 허가약물 공개 연구로 확인된 경우에만 REGULATORY_PUBLIC
> ${CLAUDE_PLUGIN_ROOT}/scripts/llm/run_review_panel.sh --workspace _workspace $CLASS \
>     --draft _workspace/03_protocol_draft.md --goal-spec _workspace/00_input/goal_spec.json
> ```
> 패널은 결정적 도구(doc_lint/citation/dose) findings를 먼저 합류시키고 `review_synthesis.json` + `qa_fix_plan.md`(Critical/Major)를 만든다. **`qa_fix_plan.md`는 아래 Step 3 수렴 루프의 actor(protocol-writer) 입력**으로 연결된다.

```
Agent(
  description: "리뷰 취합 및 우선순위 분류",
  model: "opus",
  name: "qa-reviewer",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/qa-reviewer.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/regulatory-review/SKILL.md를 Read하여 'QA 취합 절차' 섹션을 따르라.
존재하면 _workspace/review/review_synthesis.json(v4 이종 벤더 critic 취합)도 Read하여 결정적 도구 우선 + 출처 태깅으로 반영하라.

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

**Step 3: Actor-Critic 수렴 루프 (v3 — 예산형)**

> **변경 (v3.0.0)**: 기존 "Critical 자동 수정 최대 1회" 하드캡을 **예산형 수렴 루프**로 대체한다. protocol-writer(actor)와 qa-reviewer + `doc_lint`(critic)가 종료조건을 만족할 때까지 반복하되, 예산·plateau로 무한 루프를 막는다.

**루프 파라미터 (기본값)**:
- `max_iterations = 3`
- 종료(수렴): `Critical == 0` **AND** `doc_lint score ≥ 90`
- 조기 종료(plateau): 직전 대비 score 개선 `< 2`점 **AND** Critical 미감소 → 사람 에스컬레이션
- **불변 입력(락)**: `_workspace/02_synopsis.md`(또는 승인 변형)과 `_workspace/00_input/design_decisions.md`는 루프 중 변경 금지. 작성자가 설계 합의를 임의로 바꾸지 못하게 한다.

**각 반복(iteration k)**:

1. **결정적 채점 먼저(critic A)** — Bash로 실행하여 객관 점수를 얻는다:
   ```bash
   PY=${CLAUDE_PLUGIN_ROOT}/scripts/.venv/bin/python   # 없으면 python3
   GOAL=_workspace/00_input/goal_spec.json
   $PY ${CLAUDE_PLUGIN_ROOT}/scripts/qa/doc_lint.py _workspace/03_protocol_draft.md --score \
       ${GOAL:+--goal-spec "$GOAL"}
   ```
   `score`, `critical[]`을 기록한다.
2. **QA 취합(critic B)** — 위 Step 2(qa-reviewer)로 `qa_review_report.md`를 갱신한다. qa-reviewer는 **직전 보고서 대비 신규/잔존/해소된 이슈를 구분**한다.
3. **종료 판정**: 종료조건 충족 → 루프 종료(성공). plateau → 종료(에스컬레이션). 그 외 → 4로.
4. **수정(actor)** — protocol-writer를 재호출한다. 수정 전 **`qa_fix_plan.md`를 먼저 작성**하게 하여 어떤 Critical/Major를 어떻게 고칠지 명시한 뒤 본문을 수정한다:
   ```
   [수정 모드 — iteration {k}]
   불변 입력(변경 금지): _workspace/02_synopsis.md, _workspace/00_input/design_decisions.md
   이전 산출물: _workspace/03_protocol_draft.md를 Read하라.

   수정 계획: _workspace/review/qa_fix_plan.md가 존재하면(v4 패널 자동 생성 — review_synthesis 기반 Critical/Major) Read하여 그대로 사용하고, 없으면 직접 작성하라.
   그 다음 아래 우선순위로 _workspace/03_protocol_draft.md를 수정하라.

   1) 결정적 도구 findings (doc_lint/citation_verify/dose_safety) — 최우선
   2) review_synthesis.json의 벤더 critic Critical/Major (출처 태깅)
   3) QA 피드백:
   - [C-1] {제목}: {내용} → 권고: {수정 방향}
   ...
   설계 결정(synopsis/design_decisions)은 보존하라.
   ```
5. provenance 기록(권장): `pipeline_manifest.py record --phase 9 --note "iter {k}: score {s}, critical {n}"`.
6. k+1로.

**루프 종료 후**:
- **수렴 성공**: 사용자에게 "Critical 0, score N/100 — 수렴(iter k)" 보고. `/finalize`로 T0 최종 게이트 권유.
- **예산 소진/plateau**: 잔존 Critical/Major와 score 궤적을 제시하고 **사용자 판단을 요청**(전문가 개입 지점). 임의로 "완료" 처리하지 않는다.

> **Goodhart 주의**: 루프는 `doc_lint`/QA 루브릭을 최적화하나, 루브릭이 과학적 타당성 전부를 포착하지는 못한다. Phase 7 사람 게이트와 다양한 critic(5인 리뷰 + 결정적 린트)을 유지하여 단일 지표 과최적화를 방지한다.

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
