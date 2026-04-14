---
name: research
description: "임상시험 배경 자료 수집. 약물의 PK/PD, 유사 시험, 규제 가이드라인, 약물 라벨 정보를 병렬로 조사하고 사용자 검토 게이트를 실행한다. /research 또는 자료조사, 문헌검색, 배경조사 요청 시 사용."
---

# /research — 배경 자료 수집 (Phase 2-3)

## 전제 조건
- 약물명과 시험 유형이 확인되어야 함
- 확인되지 않았으면 사용자에게 질문하여 수집

## 워크플로우

### Step 1: 입력 확인
`_workspace/00_input/trial_info.md` 존재 여부를 확인한다.
- 존재하면 Read하여 시험 정보 파악
- 미존재하면 사용자에게 필수 정보 질문 후 Write로 저장:
  - 약물명 (필수)
  - 시험 유형 (필수): FIH, SAD/MAD, DDI, BE, FE, QTc, ADME 등
  - 적응증 (필수)
  - FIH/SAD/MAD인 경우: IB 파일 경로 (필수)
  - 기타: 약물 계열, 의뢰자명, 투여 경로 등 (권장)

### Step 1.5: Reference 디렉토리 생성
```bash
mkdir -p _workspace/01_references/trials
mkdir -p _workspace/01_references/literature
mkdir -p _workspace/01_references/guidelines
mkdir -p _workspace/01_references/labels
mkdir -p _workspace/01_references/safety
mkdir -p _workspace/01_references/pd_biomarkers
mkdir -p _workspace/01_references/pharmacogenomics
mkdir -p _workspace/01_references/metabolomics
```

### Step 2: 병렬 자료 수집
조사 에이전트들을 **동시에** 실행한다. 각 에이전트는 **개별 reference 파일을 먼저 생성**한 후 요약 보고서를 작성한다.

> **translational-scientist 참여 조건**: `.claude/skills/clinical-research/SKILL.md`의 "시험 유형별 오믹스/PD 우선순위" 표를 따른다. BE/FE에서는 불참, FIH/SAD/MAD/DDI/QTc/ADME/Special Pop에서는 참여.

```
Agent(
  description: "임상약리학 배경 조사",
  model: "sonnet",
  name: "clinical-pharmacologist",
  prompt: "먼저 .claude/agents/clinical-pharmacologist.md를 Read하여 역할을 숙지하라.
그 다음 .claude/skills/clinical-research/SKILL.md를 Read하여 조사 절차와 개별 reference 파일 구조를 따르라.
시험 정보: _workspace/00_input/trial_info.md를 Read하라.
[FIH인 경우: IB 파일이 _workspace/00_input/에 있으면 Read로 분석하라.]

★ 중요: 조사한 모든 reference를 개별 MD 파일로 분리 저장하라:
- ClinicalTrials.gov 각 시험 → _workspace/01_references/trials/NCTxxxxxxxx.md
  (연구목적, 설계, 선정/제외 기준, sample size, 채혈일정, endpoint, 결과 등 상세 기술)
- PubMed 각 논문 → _workspace/01_references/literature/PMID_xxxxxxxx.md
  (서지정보, 연구방법, PK 파라미터, CV%, 주요 결과, 시사점 등 상세 기술)
개별 파일 구조는 clinical-research SKILL.md의 템플릿을 따르라.

개별 파일 생성 후, 요약 보고서를 _workspace/01_research_cp.md에 Write하라.
요약 보고서에서 개별 파일을 참조: → 상세: [01_references/trials/NCTxxxxxxxx.md]"
)

Agent(
  description: "규제 자료 조사",
  model: "sonnet",
  name: "regulatory-expert",
  prompt: "먼저 .claude/agents/regulatory-expert.md를 Read하여 역할을 숙지하라.
그 다음 .claude/skills/clinical-research/SKILL.md를 Read하여 조사 절차와 개별 reference 파일 구조를 따르라.
시험 정보: _workspace/00_input/trial_info.md를 Read하라.
.claude/references/guidelines/index.md를 Read하여 사전 수록된 규제 가이드라인 인덱스를 확인하고, 시험 유형에 해당하는 MFDS/FDA/EMA/ICH 가이드라인 파일과 cross-agency 비교표를 Read하라.

★ 중요: 조사한 모든 reference를 개별 MD 파일로 분리 저장하라:
- 규제 가이드라인별 → _workspace/01_references/guidelines/{guideline_name}.md
  (출처, 핵심 요건, 본 시험 적용 항목, 다른 가이드라인과 차이점 등 상세 기술)
- 약물 라벨별 → _workspace/01_references/labels/{drug_label}.md
  (허가사항, 용법용량, PK 섹션, 약물상호작용 섹션, 금기 등 상세 기술)
개별 파일 구조는 clinical-research SKILL.md의 템플릿을 따르라.

개별 파일 생성 후, 요약 보고서를 _workspace/01_research_reg.md에 Write하라.
요약 보고서에서 개별 파일을 참조: → 상세: [01_references/guidelines/{name}.md]"
)

Agent(
  description: "안전성 자료 조사",
  model: "sonnet",
  name: "clinician",
  prompt: "먼저 .claude/agents/clinician.md를 Read하여 역할을 숙지하라.
그 다음 .claude/skills/clinical-research/SKILL.md를 Read하여 조사 절차와 개별 reference 파일 구조를 따르라.
시험 정보: _workspace/00_input/trial_info.md를 Read하라.

★ 중요: 안전성 관련 자료를 체계적으로 수집하라:
- PubMed에서 안전성 키워드로 집중 검색 (adverse events, safety, tolerability, SAE, class effect, monitoring)
- PK 파라미터 검색(CP 담당)이나 규제 가이드라인(REG 담당)과 중복되지 않도록 안전성에 집중

★ 개별 reference 파일을 반드시 생성하라:
- _workspace/01_references/safety/AE_profile_{약물명}.md — 이상반응 빈도별·기관계별 분류
- _workspace/01_references/safety/SAE_cases_{약물명}.md — 중대한 이상반응 사례
- _workspace/01_references/safety/class_effect_{약물계열}.md — 계열 공통 이상반응
- _workspace/01_references/safety/safety_monitoring_rationale.md — 모니터링 시점·항목 근거
- _workspace/01_references/safety/stopping_rules_rationale.md — 중지 규칙 근거
- 안전성 관련 논문 → _workspace/01_references/literature/PMID_xxxxxxxx.md

개별 파일 생성 후, 요약 보고서를 _workspace/01_research_clin.md에 Write하라."
)

Agent(
  description: "PD/오믹스 자료 조사 (조건부)",
  model: "sonnet",
  name: "translational-scientist",
  prompt: "먼저 .claude/agents/translational-scientist.md를 Read하여 역할을 숙지하라.
그 다음 .claude/skills/clinical-research/SKILL.md를 Read하여 '시험 유형별 오믹스/PD 우선순위' 표를 확인하라.
시험 정보: _workspace/00_input/trial_info.md를 Read하라.

★ 시험 유형 확인 후, 본인 참여 여부 판단:
- 본 시험 유형이 BE 또는 FE라면: '본 시험 유형은 PG/PD 조사 우선순위 낮음 — 참여 생략' 메시지를 _workspace/01_research_ts.md에 1줄로 Write하고 종료
- 그 외 시험 유형(FIH/SAD/MAD/DDI/QTc/ADME/Special Pop): 우선순위 표에 따라 조사 깊이 조정

★ 중요: 조사한 모든 reference를 개별 MD 파일로 분리 저장하라:
- PD 바이오마커 → _workspace/01_references/pd_biomarkers/{biomarker_name}.md
- 약물유전체 → _workspace/01_references/pharmacogenomics/{gene_name}.md
  (예: CYP2C19.md — 한국인 대립유전자 빈도, 표현형 분류, 라벨 권고)
- 대사체 (해당 시) → _workspace/01_references/metabolomics/{topic}.md
- PD/PG/대사체 관련 PubMed 논문 → _workspace/01_references/literature/PMID_xxxxxxxx.md
개별 파일 구조는 translational-scientist.md의 템플릿을 따르라.

★ MCP 도구 한계 솔직 표시: PharmGKB/HMDB 직접 접근 불가 시 '[데이터베이스 직접 접근 불가 — PubMed/라벨 기반]' 명시.

개별 파일 생성 후, 요약 보고서를 _workspace/01_research_ts.md에 Write하라."
)
```

### Step 3: 자료 종합
모든 조사 에이전트 완료 후:
1. `_workspace/01_references/` 내 생성된 개별 파일 목록을 확인 (Glob)
2. `_workspace/01_research_cp.md`, `_workspace/01_research_reg.md`, `_workspace/01_research_clin.md`, `_workspace/01_research_ts.md`(존재 시)를 Read
3. 중복 제거 및 병합하여 `_workspace/01_research_report.md`에 Write
   - 통합 보고서에서 모든 개별 reference 파일을 목록으로 참조
   - 안전성, PD/약력학, 약물유전체, 대사체 섹션을 각각 독립 섹션으로 포함 (translational-scientist 참여 시)
4. 핵심 발견사항 요약과 함께 **수집된 reference 파일 목록**을 사용자에게 제시

### Step 4: 사용자 검토 게이트 ★
사용자에게 세 가지 선택지 제시:
- **승인** → 완료. `/design`으로 진행 가능
- **추가 조사 요청** → 요청 내용에 따라 최적 에이전트 재호출:
  - PK/약물/유사 시험 → clinical-pharmacologist
  - 규제/가이드라인/라벨 → regulatory-expert
  - 임상적 판단/안전성 → clinician
  - PD/약력학/약물유전체/대사체 → translational-scientist
  - 통계/설계 → biostatistician
- **자료 직접 제공** → 사용자가 문헌/데이터를 추가 입력

추가 조사 후 다시 Step 4로 돌아가 승인될 때까지 반복한다.

## 산출물
- `_workspace/01_research_report.md` — 종합 배경 조사 보고서
- 모든 자료에 reference 필수 (PMID, NCT, URL, 가이드라인 인용)
