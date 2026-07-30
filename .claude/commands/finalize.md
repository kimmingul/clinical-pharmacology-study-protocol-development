---
name: finalize
description: "생성된 계획서/ICF 초안을 결정적 release 게이트로 검증한다. finalize_run.py가 5개 차원(structure/citation/dose/advisory/approval)을 실행하고 종료코드로 판정한다. /finalize 또는 최종 검증, 마감, finalize 요청 시 사용."
---

# /finalize — release 게이트 실행

판정은 `.claude/scripts/qa/finalize_run.py`가 수행한다. 이 커맨드는 대상을 결정하고
실행 파일을 호출한 뒤 결과를 보고하는 래퍼다. **에이전트가 "통과했다"고 판단하지 않는다
— 판정은 종료코드와 `release_gate.json`만으로 이루어진다.**

> 인자: `$ARGUMENTS`. 예: `/finalize`, `/finalize icf`, `/finalize submission`,
> `/finalize icf submission`

## 절차

### Step 1 — 대상과 프로파일 결정

- 인자에 `icf`가 있으면 `_workspace/04_icf_draft.md`, 아니면 `_workspace/03_protocol_draft.md`
- 인자에 `submission`이 있으면 `--profile submission`, 아니면 `--profile draft`

### Step 2 — 게이트 실행

```bash
WS=_workspace
PY=.claude/scripts/.venv/bin/python      # 없으면 python3
case "$ARGUMENTS" in *icf*) TARGET="$WS/04_icf_draft.md";; *) TARGET="$WS/03_protocol_draft.md";; esac
case "$ARGUMENTS" in *submission*) PROFILE=submission;; *) PROFILE=draft;; esac

$PY .claude/scripts/qa/finalize_run.py "$TARGET" \
    --profile "$PROFILE" \
    --workspace "$WS" \
    --goal-spec "$WS/00_input/goal_spec.json" \
    --mrsd-json "$WS/00_input/mrsd.json"
GATE=$?
```

### Step 3 — 보고

종료코드를 그대로 전달한다. 재해석하지 않는다.

| GATE | 의미 | 보고 |
|------|------|------|
| 0 | 통과 | "✅ release 게이트 통과 (`profile`)" + 미구현 차원 경고를 함께 전달 |
| 1 | 판정했고 불합격 | "⛔ 최종화 거부" + 차단된 차원과 findings 제시 → Phase 9 수렴 루프로 수정 |
| 2 | 판정 불가 | "⛔ 판정 불가" + 원인(대상 없음/검사기 크래시/리포트 기록 실패) 제시 → 게이트나 입력을 고쳐야 함 |

`GATE=1`일 때 사용자가 강제 override를 명시하지 않는 한 '최종'으로 표시하지 않는다.

`GATE=0`일 때만 provenance를 기록한다. 기록은 판정의 재해석이 아니라 통과 사실의
추적성 확보이며, `trial-doc-orchestrator`가 산출물 생성 단계마다 요구한다.

```bash
if [ "$GATE" = "0" ]; then
  $PY .claude/scripts/qa/pipeline_manifest.py record \
      --workspace "$WS" \
      --phase finalize --agent finalize --model opus \
      --output "$TARGET" \
      --inputs "$WS/02_synopsis.md" "$WS/00_input/goal_spec.json" \
      --note "release gate 통과 (profile=$PROFILE)"
fi
```

## Gotchas

- **프로파일을 구분한다.** 작성 중에는 `draft`(기본)를 쓴다. `draft`는 placeholder와
  미확인 인용을 표시만 하고 통과시킨다 — 초안 단계에서는 정상 상태이기 때문이다.
  제출 직전에만 `submission`을 쓴다.
- **`submission`은 네트워크가 필요하다.** 인용 id를 실제 레지스트리에 조회하며,
  네트워크 불가는 통과가 아니라 차단(`unverified_network`)이다. 폐쇄망에서는
  `draft`로 구조·권고 사항만 점검하고, 인용 검증은 외부망에서 별도로 수행한다.
- **`dose` 차원은 ICF 대상에도 적용된다.** 이전 `/finalize`가 용량 검사를 protocol로만
  한정했던 것과 달리, 게이트는 대상 종류를 가리지 않고 5개 차원을 모두 실행한다.
  ICF에는 보통 시작 용량 표기가 없어 실질적으로 `SKIPPED`이지만, FIH goal_spec에
  MRSD가 없으면 submission에서 ICF도 차단될 수 있다 — 의도된 fail-closed 동작이다.
- **승인 차원은 아직 미구현이다.** 게이트가 통과해도 사람 승인은 검증되지 않았으므로
  "제출 가능"을 의미하지 않는다. 게이트 출력의 경고를 사용자에게 그대로 전달한다.
- **score는 판정에 쓰이지 않는다.** 참고 수치로만 출력된다. `score 100`이 규제
  적합성을 의미하지 않는다는 것이 이 게이트를 만든 이유다.
- venv가 없으면 `python3`로 대체 실행한다.
