---
name: finalize
description: "생성된 계획서/ICF 초안을 최종 승인 전에 결정적 가드레일(T0)로 검증한다. doc_lint --strict(+goal_spec), citation_verify, dose_safety_guard를 실제 산출물에 적용하여 통과 시에만 '최종'으로 표시. /finalize 또는 최종 검증, 마감, finalize 요청 시 사용."
---

# /finalize — 최종화 가드레일 (T0 enforcement)

생성된 산출물(`_workspace/03_protocol_draft.md`, `_workspace/04_icf_draft.md`)을
**실제 파일에 대해** 결정적으로 검증한다. CI의 strict 게이트가 golden fixture에만
적용되던 것과 달리, 이 커맨드는 **방금 만든 문서**가 T0(안전·규제 핵심 불변식)를
통과하는지 확인하고, **통과할 때만 최종 승인**을 허용한다.

> 인자: `$ARGUMENTS` (없으면 protocol 기본). 예: `/finalize icf`, `/finalize protocol`.

## 절차

### Step 1 — 대상 결정
- 인자에 `icf`가 있으면 `_workspace/04_icf_draft.md`, 아니면 `_workspace/03_protocol_draft.md`.
- 파일이 없으면 거부: "최종화할 산출물이 없습니다. 먼저 `/protocol`(또는 `/icf`)을 실행하세요."

### Step 2 — 결정적 가드레일 실행 (Bash)

```bash
WS=_workspace
PY=.claude/scripts/.venv/bin/python      # 없으면 python3
GOAL=$WS/00_input/goal_spec.json         # 있으면 사용

# (a) doc_lint --strict (+ goal_spec): 섹션 누락(최종화 시 T0)·보존 15년·CI 경계·placeholder
$PY .claude/scripts/qa/doc_lint.py "$WS/03_protocol_draft.md" --strict \
    ${GOAL:+--goal-spec "$GOAL"}; LINT=$?

# (b) 채점 (참고용 — score≥90 권장)
$PY .claude/scripts/qa/doc_lint.py "$WS/03_protocol_draft.md" --score \
    ${GOAL:+--goal-spec "$GOAL"}

# (c) zero-trust 인용 검증 (네트워크 가능 시 --online, 실패는 unverified로 표시)
$PY .claude/scripts/qa/citation_verify.py audit \
    "$WS/03_protocol_draft.md" "$WS/01_research_report.md" --workspace "$WS"

# (d) FIH 용량 안전 가드 (MRSD JSON 있을 때만 의미; 없으면 skipped)
$PY .claude/scripts/qa/dose_safety_guard.py "$WS/03_protocol_draft.md" \
    --mrsd-json "$WS/00_input/mrsd.json" --strict; DOSE=$?
```

(ICF 대상이면 (a)·(c)를 `04_icf_draft.md`로 바꾸고 (d)는 생략.)

### Step 3 — 판정 (T0 게이트)

| 검사 | 통과 기준 | 실패 시 |
|------|----------|--------|
| doc_lint `--strict` (LINT=0) | ERROR 0건 (Appendix B 16섹션·보존 15년·CI 경계·placeholder) | **차단** |
| citation_audit | `format_fail`/`not-found` = 0 (또는 모두 해명됨) | **차단** (해명 불가 인용) |
| dose_safety (DOSE=0) | violation 0건 또는 `skipped`(비-FIH) | **차단** |
| score | ≥ 90 권장 | 90 미만이면 경고 + 사용자 확인 |

- **전부 통과** → 최종 승인. provenance 기록:
  ```bash
  $PY .claude/scripts/qa/pipeline_manifest.py record \
    --phase finalize --agent finalize --model opus \
    --output "$WS/03_protocol_draft.md" \
    --inputs "$WS/02_synopsis.md" "$WS/00_input/goal_spec.json" \
    --note "T0 가드레일 통과 (lint strict + citation + dose)"
  ```
  사용자에게 "✅ 최종화: 모든 T0 가드레일 통과 (score N/100)"로 보고.
- **하나라도 실패** → "⛔ 최종화 거부"로 보고하고, 실패 항목과 위치를 제시한 뒤
  Phase 9 수렴 루프(또는 protocol-writer 재호출)로 수정한다. **사용자가 강제
  override를 명시하지 않는 한 '최종'으로 표시하지 않는다.**

## Gotchas
- 이 커맨드는 **실제 산출물**을 검사한다 — 작성 중(부분 초안)에는 섹션 누락이
  정상이므로 `/finalize`는 작성 완료 후에만 의미가 있다.
- citation `--online`은 rate limit·네트워크에 영향받는다. offline 결과(형식 검증)는
  항상 수행되며, online 실패는 차단이 아니라 `unverified-network`로 표시된다.
- venv가 없으면 `python3`로 대체 실행한다.
