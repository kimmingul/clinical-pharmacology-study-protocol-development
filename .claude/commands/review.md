---
name: review
description: "다중 에이전트 병렬 리뷰. 4명의 전문가가 계획서를 각자 관점에서 검토하고, QA가 취합하여 Critical/Major/Minor로 분류한다. /review 또는 리뷰, 검토 요청 시 사용."
---

# /review — 다중 에이전트 리뷰 (Phase 9)

## 전제 조건
- `_workspace/03_protocol_draft.md`가 존재해야 함
- 미존재 시: "먼저 /protocol로 계획서를 작성해주세요"

## 워크플로우

### Step 1: 리뷰 디렉토리 준비
```bash
mkdir -p _workspace/review
```

### Step 2: 4명 전문가 병렬 리뷰
시험 유형에 따라 clinician 참여 여부를 결정한 후, 해당 에이전트들을 **동시에** 호출한다.

**항상 참여:**
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
- _workspace/review/review_clinician.md (존재하면)

4명의 리뷰를 취합하여 Critical/Major/Minor로 분류하라.
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
- `_workspace/review/review_clinician.md` (조건부)
- `_workspace/review/qa_review_report.md` — 통합 QA 보고서
