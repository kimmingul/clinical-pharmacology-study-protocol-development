---
name: review
description: "다중 에이전트 병렬 리뷰. 4-5명의 전문가가 계획서를 각자 관점에서 검토하고, QA가 취합하여 Critical/Major/Minor로 분류한다. /review 또는 리뷰, 검토 요청 시 사용."
---

# /review — 다중 에이전트 리뷰 (Phase 9)

## 전제 조건
- `_workspace/03_protocol_draft.md`가 존재해야 함
- 미존재 시: "먼저 /protocol로 계획서를 작성해주세요"

## 리뷰어 구성 (시험 유형별)

| 리뷰어 | 참여 조건 |
|--------|----------|
| clinical-pharmacologist | 항상 |
| clinician | 항상 |
| regulatory-expert | 항상 |
| biostatistician | 항상 |
| **translational-scientist** | **조건부** — BE/FE **불참**, 그 외(FIH/SAD/MAD/DDI/QTc/ADME/Special Pop) **참여** |

> translational-scientist 참여 조건은 자료 수집 단계의 참여 조건과 동일하다 (`.claude/skills/clinical-research/SKILL.md`의 "시험 유형별 오믹스/PD 우선순위" 표 참조).

## 워크플로우

### Step 1: 리뷰 디렉토리 준비
```bash
mkdir -p _workspace/review
```

### Step 2: 병렬 리뷰
시험 유형을 확인하여 리뷰어 목록을 결정한 후, 해당 에이전트들을 **동시에** 호출한다.

**항상 참여 (4명):**
```
Agent(
  description: "임상약리학 관점 계획서 리뷰",
  model: "sonnet",
  name: "clinical-pharmacologist",
  prompt: "먼저 .claude/agents/clinical-pharmacologist.md를 Read하라.
.claude/skills/regulatory-review/SKILL.md를 Read하여 리뷰 절차를 따르라.

[리뷰 모드] 계획서를 임상약리학 관점에서 검토하라.
검토 초점: PK 설계 적절성, 채혈 시점, 약물상호작용 평가, 용량 근거, washout 기간.

계획서: _workspace/03_protocol_draft.md를 Read하라.
배경 자료: _workspace/01_research_report.md를 Read하라.

산출물을 _workspace/review/review_clinical_pharmacologist.md에 Write하라."
)
```

```
Agent(
  description: "규제 관점 계획서 리뷰",
  model: "sonnet",
  name: "regulatory-expert",
  prompt: "먼저 .claude/agents/regulatory-expert.md를 Read하라.
.claude/skills/regulatory-review/SKILL.md를 Read하여 리뷰 절차를 따르라.

[리뷰 모드] 계획서를 규제 관점에서 검토하라.
검토 초점: ICH E6(R3) Annex 1 필수 요소, MFDS/FDA 가이드라인 준수, 규제 용어 적절성.

계획서: _workspace/03_protocol_draft.md를 Read하라.

산출물을 _workspace/review/review_regulatory_expert.md에 Write하라."
)
```

```
Agent(
  description: "통계 관점 계획서 리뷰",
  model: "sonnet",
  name: "biostatistician",
  prompt: "먼저 .claude/agents/biostatistician.md를 Read하라.
.claude/skills/regulatory-review/SKILL.md를 Read하여 리뷰 절차를 따르라.

[리뷰 모드] 계획서를 통계 관점에서 검토하라.
검토 초점: 통계 섹션 완결성, sample size 정당성, 분석 방법, 무작위화, 결측치 처리.

계획서: _workspace/03_protocol_draft.md를 Read하라.
통계 설계: _workspace/00_input/statistical_design.md를 Read하라.

산출물을 _workspace/review/review_biostatistician.md에 Write하라."
)
```

**항상 참여 (모든 시험):**
```
Agent(
  description: "임상의학·안전성 관점 계획서 리뷰",
  model: "sonnet",
  name: "clinician",
  prompt: "먼저 .claude/agents/clinician.md를 Read하라.
.claude/skills/regulatory-review/SKILL.md를 Read하여 리뷰 절차를 따르라.

[리뷰 모드] 계획서를 임상의학·안전성 관점에서 검토하라.
검토 초점: 선정/제외 기준의 임상적 타당성, 안전성 모니터링 계획의 적절성, 이상반응 관리, 중지 기준, 안전성 정보의 충분성.

계획서: _workspace/03_protocol_draft.md를 Read하라.
안전성 자료: _workspace/01_references/safety/ 디렉토리의 파일들을 Read하여 계획서와 대조하라.

산출물을 _workspace/review/review_clinician.md에 Write하라."
)
```

**조건부 참여 (BE/FE 외):**
```
Agent(
  description: "중개의학·PD/오믹스 관점 계획서 리뷰",
  model: "sonnet",
  name: "translational-scientist",
  prompt: "먼저 .claude/agents/translational-scientist.md를 Read하라.
.claude/skills/regulatory-review/SKILL.md를 Read하여 리뷰 절차를 따르라.

[리뷰 모드] 계획서를 중개의학·PD/오믹스 관점에서 검토하라.
검토 초점:
- PD 평가 섹션의 적절성 (바이오마커 선정 근거, 측정 시점, 분석 방법)
- PK-PD 모델링 계획의 타당성 (해당 시)
- 약물유전체(PG) 분석 계획 (대상 유전자, 한국인 빈도 반영, 표현형별 해석)
- 대사체 분석 계획 (MIST 준수, 내인성 바이오마커 측정법)
- ICF Part 4(PG/오믹스 동의)와의 정합성 — 계획서에 명시된 분석 항목이 ICF에 빠짐없이 반영되었는가

계획서: _workspace/03_protocol_draft.md를 Read하라.
PD/오믹스 배경: _workspace/01_research_ts.md가 존재하면 Read하라.
설계 결정: _workspace/00_input/design_decisions.md를 Read하여 유전체/대사체 분석 계획 확인.

산출물을 _workspace/review/review_translational_scientist.md에 Write하라."
)
```

> **시험 유형이 BE/FE인 경우** translational-scientist는 호출하지 않는다 (PG/PD 의미 낮음).

### Step 3: QA 취합
모든 리뷰 완료 후:
```
Agent(
  description: "리뷰 취합 및 QA 보고서 작성",
  model: "opus",
  name: "qa-reviewer",
  prompt: "먼저 .claude/agents/qa-reviewer.md를 Read하라.
.claude/skills/regulatory-review/SKILL.md를 Read하여 QA 절차를 따르라.

다음 파일을 모두 Read하라:
- _workspace/03_protocol_draft.md
- _workspace/review/review_clinical_pharmacologist.md
- _workspace/review/review_regulatory_expert.md
- _workspace/review/review_biostatistician.md
- _workspace/review/review_clinician.md
- _workspace/review/review_translational_scientist.md (존재하면 — BE/FE 외 시험)

참여한 4-5명의 리뷰를 취합하여 Critical/Major/Minor로 분류하라.
리뷰어 간 상충 의견이 있으면 양쪽 근거를 비교하여 기록하라.

산출물을 _workspace/review/qa_review_report.md에 Write하라."
)
```

### Step 4: Critical 자동 수정 (조건부)
`_workspace/review/qa_review_report.md`를 Read하여 Critical 사항을 확인한다.

**Critical이 있으면:**
1. Critical의 위치(계획서 섹션)를 파악
2. protocol-writer를 재호출하여 수정 (피드백 포함)
3. 수정 후 qa-reviewer를 1회 재호출
4. **최대 1회만 수행.** 재검토 후에도 Critical이 있으면 사용자에게 보고

**Critical이 없으면:** Step 5로 진행

### Step 5: 결과 보고
QA 보고서 요약을 사용자에게 제시:
- Critical / Major / Minor 건수
- 주요 발견 사항
- 상충 의견 (있는 경우)
- 수정 권고 사항

## 산출물
- `_workspace/review/review_clinical_pharmacologist.md`
- `_workspace/review/review_regulatory_expert.md`
- `_workspace/review/review_biostatistician.md`
- `_workspace/review/review_clinician.md`
- `_workspace/review/review_translational_scientist.md` (조건부 — BE/FE 외 시험)
- `_workspace/review/qa_review_report.md` — 통합 QA 보고서
