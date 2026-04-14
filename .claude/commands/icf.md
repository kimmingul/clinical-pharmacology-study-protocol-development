---
name: icf
description: "동의설명서(ICF), 동의서, 개인정보 동의서를 작성한다. 계획서가 존재할 때만 실행 가능. /icf 또는 동의설명서 작성, 동의서 작성, ICF 작성 요청 시 사용."
---

# /icf — 동의문서 작성 (Phase 10)

## 전제 조건
- `_workspace/03_protocol_draft.md`가 존재해야 함
- 미존재 시: "먼저 /protocol로 계획서를 작성해주세요. 동의설명서는 계획서를 기반으로 작성됩니다."

## 워크플로우

### Step 1: 생명윤리법 적용 여부 확인
`_workspace/00_input/trial_info.md`를 Read하여 유전체/인체유래물 연구 포함 여부를 확인한다.
- 포함 → Part 4 (선택 동의) 작성 필요
- 미포함 → Part 1-3만 작성

### Step 2: ICF Writer 에이전트 호출
```
Agent(
  description: "동의설명서/동의서 작성",
  model: "opus",
  name: "icf-writer",
  prompt: "먼저 .claude/agents/icf-writer.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 .claude/skills/icf-drafting/SKILL.md를 Read하여 작성 가이드를 따르라.
상세 템플릿이 필요하면 .claude/skills/icf-drafting/references/icf-template.md도 Read하라.

{유전체/인체유래물 포함 시: '유전체 분석이 포함된 시험이다. 생명윤리법에 따른 선택 동의(Part 4)를 반드시 포함하라.'}

계획서: _workspace/03_protocol_draft.md를 Read하라.
배경 자료: _workspace/01_research_report.md를 Read하라.

산출물을 _workspace/04_icf_draft.md에 Write하라."
)
```

### Step 3: 산출물 확인
`_workspace/04_icf_draft.md`를 Read하여:
- 4개 Part가 모두 포함되었는지 (Part 4는 해당 시)
- 계획서의 시험 절차가 빠짐없이 반영되었는지
- 쉬운 언어로 작성되었는지

### Step 4: 결과 보고
"동의문서 작성이 완료되었습니다."
- Part 1: 동의설명서
- Part 2: 동의서 서명 페이지
- Part 3: 개인정보 수집·이용·제3자 제공 동의서
- Part 4: 선택 동의 (해당 시)
- "수정이 필요한 부분이 있으면 말씀해주세요."

## 산출물
- `_workspace/04_icf_draft.md` — 동의문서 전체 (Part 1-4)
