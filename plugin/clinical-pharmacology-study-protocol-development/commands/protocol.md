---
name: protocol
description: "승인된 Synopsis를 기반으로 Full Protocol을 작성한다. Synopsis 승인이 필수 전제 조건이다. /protocol 또는 계획서 작성, 프로토콜 작성 요청 시 사용."
---

# /protocol — Full Protocol 작성 (Phase 8)

## 전제 조건 (Hard Gate)
1. `_workspace/02_synopsis.md`가 존재해야 함
2. Synopsis가 사용자에 의해 **명시적으로 승인**되어야 함

미충족 시:
- Synopsis 미존재 → "/synopsis로 먼저 Synopsis를 생성해주세요"
- Synopsis 미승인 → "Synopsis를 검토하시고 승인해주세요. 승인 후 /protocol을 다시 실행합니다"

## 워크플로우

### Step 1: Synopsis 승인 확인
사용자에게 Synopsis 승인 여부를 확인한다:
- "Synopsis(`_workspace/02_synopsis.md`)를 최종 검토하셨나요? 이 Synopsis를 기반으로 Full Protocol을 작성합니다."
- 승인 확인 후 진행

### Step 2: Protocol Writer 에이전트 호출
```
Agent(
  description: "임상시험 계획서 작성",
  model: "opus",
  name: "protocol-writer",
  prompt: "먼저 ${CLAUDE_PLUGIN_ROOT}/agents/protocol-writer.md를 Read하여 역할과 원칙을 숙지하라.
그 다음 ${CLAUDE_PLUGIN_ROOT}/skills/protocol-drafting/SKILL.md를 Read하여 작성 가이드를 따르라.
상세 템플릿이 필요하면 ${CLAUDE_PLUGIN_ROOT}/skills/protocol-drafting/references/protocol-template.md도 Read하라.

Synopsis: _workspace/02_synopsis.md를 Read하라. Synopsis의 설계 결정을 정확히 반영하라.
배경 자료: _workspace/01_research_report.md를 Read하라. 세부 근거 데이터를 활용하라.
시험 정보: _workspace/00_input/trial_info.md를 Read하라.
설계 결정: _workspace/00_input/design_decisions.md를 Read하라.
통계 설계: _workspace/00_input/statistical_design.md를 Read하라.

산출물을 _workspace/03_protocol_draft.md에 Write하라.
문서가 매우 길면 여러 번의 Write/Edit 호출로 나누어 작성해도 된다."
)
```

### Step 3: 산출물 확인
`_workspace/03_protocol_draft.md`를 Read하여:
- Synopsis 결정 사항이 정확히 반영되었는지 확인
- 주요 섹션이 누락되지 않았는지 확인
- 문제 발견 시 protocol-writer 재호출

### Step 4: 리뷰 안내
"Protocol 작성이 완료되었습니다. /review로 다중 에이전트 리뷰를 실행할 수 있습니다."

## 산출물
- `_workspace/03_protocol_draft.md` — ICH E6(R3) Annex 1 기반 Full Protocol
