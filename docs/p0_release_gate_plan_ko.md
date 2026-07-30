# P0 Fail-Closed Release Gate 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `/finalize`의 release 판정을 자연어 SOP에서 결정적 실행 파일 `finalize_run.py`로 이전하여, 검사 누락·검사기 크래시가 "통과"로 집계되지 않게 한다.

**Architecture:** `finalize_run.py`가 기존 검사기 3종을 `import`로 호출하고(subprocess 아님), 검사기는 사실(finding)만 반환하며 심각도 판정은 게이트가 프로파일(`draft`/`submission`)에 따라 소유한다. 5개 차원을 각각 try/except로 감싸 실행하고, 하나라도 차단 상태면 non-zero로 종료한다.

**Tech Stack:** Python 3.12, 표준 라이브러리만(`argparse`/`json`/`os`/`re`/`sys`), pytest, monkeypatch

**설계 문서:** `docs/p0_release_gate_design_ko.md` (커밋 `e4e60ef`)

## Global Constraints

- **신규 의존성 추가 금지.** 표준 라이브러리만 사용한다. `.claude/scripts/requirements.txt`를 수정하지 않는다.
- **검사기 3종을 수정하지 않는다**: `.claude/scripts/qa/doc_lint.py`, `citation_verify.py`, `dose_safety_guard.py`. 또한 `.claude/hooks/draft_advisory_hook.py`와 `.github/workflows/ci.yml`도 수정하지 않는다.
- **런타임 경로는 `__file__` 기준 상대경로로 해석한다.** `sync_plugin.sh:44`는 `*.md`만 경로 치환하므로 `.py`에 `.claude/` 런타임 경로를 하드코딩하면 plugin 복사본에서 깨진다.
- **테스트는 네트워크 I/O를 하지 않는다.** 기존 `.claude/scripts/tests/test_citation_verify.py`의 규약("NO test performs network I/O")을 따른다. online 경로는 `citation_verify.verify_online`을 monkeypatch한다.
- **상태 문자열 상수 (정확히 이 6개):** `PASS`, `FAIL`, `SKIPPED`, `FORMAT_ONLY`, `NOT_IMPLEMENTED`, `ERROR`
- **종료코드:** `0` = 통과, `1` = 판정했고 불합격, `2` = 판정 불가(입력 오류·검사기 크래시·리포트 쓰기 실패). `ERROR`와 `FAIL`이 동시 존재하면 **2가 우선**한다.
- **프로파일 이름 (정확히 이 2개):** `draft`(기본값), `submission`
- **리포트 경로:** `<workspace>/verification/release_gate.json`, `schema` 필드 값은 정확히 `release_gate/v1`
- **커밋 메시지 말미:** `🗿 MoAI`
- 문서·주석·사용자 메시지는 한국어, 식별자·코드는 영어 (프로젝트 language 관례)

---

## File Structure

| 파일 | 책임 |
|------|------|
| `.claude/scripts/qa/finalize_run.py` (신규) | 게이트 전체 — 상태 상수, 차원 러너 5개, 집계, 리포트, CLI |
| `.claude/scripts/tests/test_finalize_run.py` (신규) | 게이트 테스트 전량 |
| `.claude/scripts/tests/fixtures/gate/` (신규) | fixture 문서 6종 + goal_spec 변형 |
| `.claude/commands/finalize.md` (수정) | 판정 로직 제거 → 실행 파일 호출 래퍼 |

`finalize_run.py`를 단일 파일로 두는 이유: 차원 러너가 각 20행 내외이고 전체가 250행 미만이며, 판정 로직이 흩어지면 "release를 결정하는 유일한 곳"이라는 설계 목표가 약해진다. 기존 `qa/` 스크립트들도 모두 단일 파일 구조다.

---

## Task 1: 골격 — 상태 상수, CLI, 입력 검증(exit 2 경로)

**Files:**
- Create: `.claude/scripts/qa/finalize_run.py`
- Test: `.claude/scripts/tests/test_finalize_run.py`

**Interfaces:**
- Consumes: 없음 (첫 태스크)
- Produces:
  - 상수 `PASS`, `FAIL`, `SKIPPED`, `FORMAT_ONLY`, `NOT_IMPLEMENTED`, `ERROR` (모두 자기 이름과 같은 문자열)
  - 상수 `PROFILES = ("draft", "submission")`, `EXIT_OK = 0`, `EXIT_REJECTED = 1`, `EXIT_UNDECIDABLE = 2`
  - `_dim(dim_id, status, findings=None, **extra) -> dict` — `{"id", "status", "findings", **extra}`
  - `main(argv=None) -> int` — 종료코드를 반환(호출하지 않음)

`.claude/scripts/tests/conftest.py`가 이미 `.claude/scripts/qa/`를 `sys.path`에 넣으므로 테스트에서 `import finalize_run`이 바로 된다.

- [ ] **Step 1: 실패하는 테스트 작성**

`.claude/scripts/tests/test_finalize_run.py`:

```python
"""Tests for the fail-closed release gate (qa/finalize_run.py).

Design: docs/p0_release_gate_design_ko.md
NO test performs network I/O: the submission profile's online citation check is
always monkeypatched (same convention as test_citation_verify.py).
"""
import json
import os

import finalize_run as fr


def test_missing_target_exits_undecidable(tmp_path):
    code = fr.main([str(tmp_path / "nope.md"), "--workspace", str(tmp_path)])
    assert code == fr.EXIT_UNDECIDABLE


def test_status_constants_are_self_named():
    assert fr.PASS == "PASS"
    assert fr.FAIL == "FAIL"
    assert fr.SKIPPED == "SKIPPED"
    assert fr.FORMAT_ONLY == "FORMAT_ONLY"
    assert fr.NOT_IMPLEMENTED == "NOT_IMPLEMENTED"
    assert fr.ERROR == "ERROR"


def test_exit_codes():
    assert (fr.EXIT_OK, fr.EXIT_REJECTED, fr.EXIT_UNDECIDABLE) == (0, 1, 2)


def test_dim_helper_shape():
    d = fr._dim("citation", fr.PASS, ["x"], detail={"total": 1})
    assert d["id"] == "citation"
    assert d["status"] == "PASS"
    assert d["findings"] == ["x"]
    assert d["detail"] == {"total": 1}


def test_dim_helper_defaults_findings_to_empty_list():
    d = fr._dim("dose", fr.SKIPPED)
    assert d["findings"] == []
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인**

Run: `cd /Users/min/Projects/clinical-pharmacology-study-protocol-development && python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'finalize_run'`

- [ ] **Step 3: 최소 구현 작성**

`.claude/scripts/qa/finalize_run.py`:

```python
#!/usr/bin/env python3
"""Fail-closed release gate for generated protocol / ICF drafts.

Design: docs/p0_release_gate_design_ko.md

The checkers (doc_lint, citation_verify, dose_safety_guard) report facts only;
this module owns the severity policy — which finding blocks a release, per
profile. The engines are located by a path relative to this file so the module
works both in the development tree and in the synced plugin copy.

Usage:
    finalize_run.py <target> [--profile draft|submission]
                             [--workspace _workspace]
                             [--goal-spec PATH] [--mrsd-json PATH]

Exit codes:
    0  release gate passed
    1  judged and rejected  -> fix the document
    2  undecidable          -> fix the gate or its inputs
"""
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# Status vocabulary. "checker not run" is never conflated with "passed".
PASS = "PASS"
FAIL = "FAIL"
SKIPPED = "SKIPPED"
FORMAT_ONLY = "FORMAT_ONLY"
NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
ERROR = "ERROR"

PROFILES = ("draft", "submission")

EXIT_OK = 0
EXIT_REJECTED = 1
EXIT_UNDECIDABLE = 2


def _dim(dim_id, status, findings=None, **extra):
    """Build one dimension result."""
    out = {"id": dim_id, "status": status, "findings": list(findings or [])}
    out.update(extra)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Fail-closed release gate for protocol / ICF drafts.")
    ap.add_argument("target")
    ap.add_argument("--profile", default="draft", choices=PROFILES)
    ap.add_argument("--workspace", default="_workspace")
    ap.add_argument("--goal-spec", default=None)
    ap.add_argument("--mrsd-json", default=None)
    args = ap.parse_args(argv)

    if not os.path.isfile(args.target):
        print(f"⛔ 최종화 거부: 대상 파일이 없습니다 — {args.target}", file=sys.stderr)
        return EXIT_UNDECIDABLE

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

`--profile`에 잘못된 값이 오면 `argparse`가 자체적으로 종료코드 2로 끝내므로 별도 처리가 필요없다 (`EXIT_UNDECIDABLE`과 일치).

- [ ] **Step 4: 테스트를 실행해 통과를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v`
Expected: 5 passed

- [ ] **Step 5: 커밋**

```bash
git add .claude/scripts/qa/finalize_run.py .claude/scripts/tests/test_finalize_run.py
git commit -m "$(cat <<'EOF'
feat(qa): release gate 골격 — 상태 상수 + CLI + 입력 검증

대상 파일 없음/프로파일 오류를 exit 2(판정 불가)로 처리.

🗿 MoAI
EOF
)"
```

---

## Task 2: 차원 1 `structure` + 집계 + exit 0/1

**Files:**
- Modify: `.claude/scripts/qa/finalize_run.py`
- Modify: `.claude/scripts/tests/test_finalize_run.py`
- Create: `.claude/scripts/tests/fixtures/gate/protocol_missing_b7.md`
- Create: `.claude/scripts/tests/fixtures/gate/protocol_clean.md`

**Interfaces:**
- Consumes: Task 1의 `_dim`, 상태 상수, 종료코드 상수
- Produces:
  - `dim_structure(target, profile, ctx) -> dict` — `doc_type`을 extra로 실어 보냄
  - `DIMENSIONS` — `(dim_id, callable)` 튜플의 시퀀스
  - `_BLOCKING` — `{profile: set(차단 상태)}`
  - `run_gate(target, profile, workspace, goal_spec_path=None, mrsd_json=None) -> dict`
    — `{"result", "exit_code", "profile", "doc_type", "dimensions", "warnings", "score_informational"}`
  - `FIXTURES` 디렉터리 관례: `.claude/scripts/tests/fixtures/gate/`

`doc_lint.lint_file(path)`는 `(doc_type, errors, warnings)` 3-튜플을 반환한다. `doc_type`은 파일명에 `icf`가 있으면 `"icf"`, 아니면 `"protocol"`이다.

- [ ] **Step 1: fixture 2개 작성**

`.claude/scripts/tests/fixtures/gate/protocol_clean.md` — 모든 차원이 깨끗한 양성 대조. 보존기간 문장을 쓰지 않으므로 `_retention_errors`가 걸리지 않는다.

```markdown
# 임상시험 계획서 (게이트 테스트용 fixture — 내용은 최소)

# B.1 General Information
# B.2 Background
# B.3 Objectives
# B.4 Trial Design
# B.5 Selection of Participants
# B.6 Interventions
# B.7 Discontinuation
# B.8 Assessment of Efficacy
# B.9 Assessment of Safety
# B.10 Statistics
# B.11 Direct Access
# B.12 Quality Control
# B.13 Ethics
# B.14 Data Handling
# B.15 Financing
# B.16 Publication
```

`.claude/scripts/tests/fixtures/gate/protocol_missing_b7.md` — `B.7`만 빠진 것. **다른 차원은 건드리지 않는다** (설계 §10.1 단일 결함 원칙).

```markdown
# 임상시험 계획서 (게이트 테스트용 fixture — B.7 누락)

# B.1 General Information
# B.2 Background
# B.3 Objectives
# B.4 Trial Design
# B.5 Selection of Participants
# B.6 Interventions
# B.8 Assessment of Efficacy
# B.9 Assessment of Safety
# B.10 Statistics
# B.11 Direct Access
# B.12 Quality Control
# B.13 Ethics
# B.14 Data Handling
# B.15 Financing
# B.16 Publication
```

- [ ] **Step 2: 실패하는 테스트 추가**

`.claude/scripts/tests/test_finalize_run.py`에 추가:

```python
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "fixtures", "gate")


def fixture(name):
    return os.path.join(FIXTURES, name)


def test_clean_protocol_passes_draft(tmp_path):
    code = fr.main([fixture("protocol_clean.md"),
                    "--profile", "draft", "--workspace", str(tmp_path)])
    assert code == fr.EXIT_OK


def test_missing_section_fails_both_profiles(tmp_path):
    for profile in ("draft", "submission"):
        report = fr.run_gate(fixture("protocol_missing_b7.md"),
                             profile, str(tmp_path))
        structure = next(d for d in report["dimensions"]
                         if d["id"] == "structure")
        assert structure["status"] == fr.FAIL
        assert report["exit_code"] == fr.EXIT_REJECTED


def test_structure_dimension_reports_doc_type(tmp_path):
    report = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path))
    assert report["doc_type"] == "protocol"
```

- [ ] **Step 3: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v`
Expected: FAIL — `AttributeError: module 'finalize_run' has no attribute 'run_gate'`

- [ ] **Step 4: 구현 — `dim_structure` + `run_gate`**

`finalize_run.py`의 import 블록에 추가 (`_HERE` sys.path 삽입 **뒤에** 와야 함):

```python
import doc_lint  # noqa: E402  (engine on sys.path via _HERE)
```

`_dim` 정의 뒤에 추가:

```python
def dim_structure(target, profile, ctx):
    """doc_lint ERROR — 구조·법정 보존기간 등 하드 결함. 프로파일 무관."""
    doc_type, errors, _warnings = doc_lint.lint_file(target)
    status = FAIL if errors else PASS
    return _dim("structure", status, errors, doc_type=doc_type)


DIMENSIONS = (
    ("structure", dim_structure),
)

# 프로파일별 차단 상태 집합. SKIPPED/NOT_IMPLEMENTED는 어느 쪽도 차단하지 않는다.
_BLOCKING = {
    "draft": {FAIL, ERROR},
    "submission": {FAIL, ERROR, FORMAT_ONLY},
}


def _utc_now():
    """UTC ISO-8601. datetime.now(timezone.utc)로 naive datetime을 피한다."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_gate(target, profile, workspace, goal_spec_path=None, mrsd_json=None):
    """모든 차원을 실행하고 집계한다. 예외를 밖으로 내보내지 않는다."""
    ctx = {
        "target": target,
        "profile": profile,
        "workspace": workspace,
        "goal_spec": doc_lint.load_goal_spec(goal_spec_path),
        "mrsd_json": mrsd_json,
    }

    dims = []
    for dim_id, fn in DIMENSIONS:
        try:
            dims.append(fn(target, profile, ctx))
        except Exception as exc:  # noqa: BLE001 — 크래시는 통과가 아니다
            dims.append(_dim(dim_id, ERROR,
                             [f"{type(exc).__name__}: {exc}"]))

    blocking = _BLOCKING[profile]
    has_error = any(d["status"] == ERROR for d in dims)
    blocked = [d["id"] for d in dims if d["status"] in blocking]

    if has_error:
        result, exit_code = "UNDECIDABLE", EXIT_UNDECIDABLE
    elif blocked:
        result, exit_code = "FAIL", EXIT_REJECTED
    else:
        result, exit_code = "PASS", EXIT_OK

    doc_type = next((d.get("doc_type") for d in dims if d.get("doc_type")),
                    None)

    return {
        "schema": "release_gate/v1",
        "generated_utc": _utc_now(),
        "target": target,
        "doc_type": doc_type,
        "profile": profile,
        "result": result,
        "exit_code": exit_code,
        "blocked_dimensions": blocked,
        "dimensions": dims,
        "warnings": [],
    }
```

`main()`의 `return EXIT_OK`를 교체:

```python
    report = run_gate(args.target, args.profile, args.workspace,
                      goal_spec_path=args.goal_spec, mrsd_json=args.mrsd_json)
    print(f"release gate ({args.profile}): {report['result']}")
    for d in report["dimensions"]:
        print(f"  [{d['id']}] {d['status']}")
        for f in d["findings"]:
            print(f"      - {f}")
    return report["exit_code"]
```

`_utc_now`를 함수 안에서 import하는 이유: 모듈 최상단 import를 늘리지 않고, 이 스크립트에서 시간이 필요한 곳이 한 군데뿐이다. 기존 `citation_verify.py`도 동일한 `_utc_now` 헬퍼 관례를 쓴다.

- [ ] **Step 5: 테스트를 실행해 통과를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v`
Expected: 8 passed

- [ ] **Step 6: 커밋**

```bash
git add .claude/scripts/qa/finalize_run.py .claude/scripts/tests/
git commit -m "$(cat <<'EOF'
feat(qa): release gate 차원 structure + 집계/종료코드

doc_lint ERROR를 차단 조건으로 강제. ERROR 상태가 통과로 집계되지 않도록
차원별 try/except로 감싸고 프로파일별 차단 집합을 분리.

🗿 MoAI
EOF
)"
```

---

## Task 3: 차원 4 `advisory` — 프로파일 분기 + ICF fixture

**Files:**
- Modify: `.claude/scripts/qa/finalize_run.py`
- Modify: `.claude/scripts/tests/test_finalize_run.py`
- Create: `.claude/scripts/tests/fixtures/gate/protocol_unverified_marker.md`
- Create: `.claude/scripts/tests/fixtures/gate/icf_no_pipa.md`
- Create: `.claude/scripts/tests/fixtures/gate/icf_pg_without_part4.md`

**Interfaces:**
- Consumes: Task 1의 `_dim`/상수, Task 2의 `DIMENSIONS`/`_BLOCKING`/`run_gate`
- Produces: `dim_advisory(target, profile, ctx) -> dict`

`doc_lint.lint_file()`의 3번째 반환값(warnings)이 대상이다. 설계 D5에 따라 **warning 전체**를 submission 차단 대상으로 삼는다 — 어떤 warning이 차단인지 분류하지 않는다.

fixture 파일명에 `icf`가 들어가면 `doc_lint.lint_file`이 자동으로 ICF 린트를 적용한다.

- [ ] **Step 1: fixture 3개 작성**

`.claude/scripts/tests/fixtures/gate/protocol_unverified_marker.md` — B.1~B.16 완비 + `[출처 미확인]` 하나만 추가:

```markdown
# 임상시험 계획서 (게이트 테스트용 fixture — 미확인 인용 마커)

# B.1 General Information
# B.2 Background
반감기는 약 8시간이다 [출처 미확인].
# B.3 Objectives
# B.4 Trial Design
# B.5 Selection of Participants
# B.6 Interventions
# B.7 Discontinuation
# B.8 Assessment of Efficacy
# B.9 Assessment of Safety
# B.10 Statistics
# B.11 Direct Access
# B.12 Quality Control
# B.13 Ethics
# B.14 Data Handling
# B.15 Financing
# B.16 Publication
```

`.claude/scripts/tests/fixtures/gate/icf_no_pipa.md` — `개인정보`라는 단어가 없는 ICF. 보존기간 문장을 쓰지 않아 `_retention_errors`를 피한다:

```markdown
# 시험대상자 동의설명서 (게이트 테스트용 fixture — PIPA 내용 없음)

## 1. 연구의 목적
본 시험은 건강한 성인에서 약물의 약동학을 평가한다.

## 2. 시험 절차
채혈은 총 12회 시행한다.

## 3. 예상되는 위험
채혈 부위의 멍, 어지러움이 발생할 수 있다.

## 4. 참여 철회
언제든지 참여를 철회할 수 있다.
```

`.claude/scripts/tests/fixtures/gate/icf_pg_without_part4.md` — `개인정보`는 있고 `유전체`를 언급하지만 `Part 4`/`선택 동의`/`별도 동의`가 없는 ICF:

```markdown
# 시험대상자 동의설명서 (게이트 테스트용 fixture — PG 언급, 선택동의 없음)

## 1. 연구의 목적
본 시험은 건강한 성인에서 약물의 약동학을 평가한다.

## 2. 시험 절차
채혈은 총 12회 시행하며, 약물유전체 분석을 위한 유전체 검사를 포함한다.

## 3. 예상되는 위험
채혈 부위의 멍, 어지러움이 발생할 수 있다.

## 4. 개인정보 보호
수집된 개인정보는 연구 목적으로만 이용된다.

## 5. 참여 철회
언제든지 참여를 철회할 수 있다.
```

- [ ] **Step 2: 실패하는 테스트 추가**

```python
import pytest


ADVISORY_FIXTURES = [
    "protocol_unverified_marker.md",
    "icf_no_pipa.md",
    "icf_pg_without_part4.md",
]


@pytest.mark.parametrize("name", ADVISORY_FIXTURES)
def test_advisory_findings_pass_draft_but_block_submission(name, tmp_path):
    draft = fr.run_gate(fixture(name), "draft", str(tmp_path))
    assert draft["exit_code"] == fr.EXIT_OK
    draft_advisory = next(d for d in draft["dimensions"]
                          if d["id"] == "advisory")
    assert draft_advisory["status"] == fr.PASS
    assert draft_advisory["findings"], "draft에서도 findings는 기록되어야 함"

    sub = fr.run_gate(fixture(name), "submission", str(tmp_path))
    sub_advisory = next(d for d in sub["dimensions"] if d["id"] == "advisory")
    assert sub_advisory["status"] == fr.FAIL
    assert sub["exit_code"] == fr.EXIT_REJECTED


def test_clean_protocol_advisory_passes_submission(tmp_path):
    report = fr.run_gate(fixture("protocol_clean.md"), "submission",
                         str(tmp_path))
    advisory = next(d for d in report["dimensions"] if d["id"] == "advisory")
    assert advisory["status"] == fr.PASS
    assert advisory["findings"] == []
```

`test_advisory_findings_pass_draft_but_block_submission`의 draft 단정에서 `EXIT_OK`를 기대할 수 있는 이유는 이 fixture들이 단일 결함 원칙을 지켜 다른 차원을 위반하지 않기 때문이다.

- [ ] **Step 3: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v -k advisory`
Expected: FAIL — `StopIteration` (advisory 차원이 `DIMENSIONS`에 없음)

- [ ] **Step 4: 구현 — `dim_advisory`**

`dim_structure` 뒤에 추가:

```python
def dim_advisory(target, profile, ctx):
    """doc_lint WARNING 전체. draft는 표시만, submission은 0건이어야 한다.

    warning을 분류하지 않는 것이 의도다 (설계 D5): 제출 직전에 미해결 권고가
    남아 있으면 종류를 따지지 않고 차단한다. placeholder·미확인 인용·PIPA
    누락·PG 선택동의 누락·CI 경계 표기 누락이 이 한 규칙으로 모두 커버된다.
    """
    _doc_type, _errors, warnings = doc_lint.lint_file(target)
    if not warnings:
        return _dim("advisory", PASS)
    if profile == "submission":
        return _dim("advisory", FAIL, warnings)
    return _dim("advisory", PASS, warnings,
                reason="draft — 권고 사항 표시만 (submission에서는 차단)")
```

`DIMENSIONS`를 교체:

```python
DIMENSIONS = (
    ("structure", dim_structure),
    ("advisory", dim_advisory),
)
```

- [ ] **Step 5: 테스트를 실행해 통과를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v`
Expected: 12 passed

- [ ] **Step 6: 커밋**

```bash
git add .claude/scripts/qa/finalize_run.py .claude/scripts/tests/
git commit -m "$(cat <<'EOF'
feat(qa): release gate 차원 advisory — 프로파일별 심각도 분기

doc_lint warning 전체를 submission 차단 대상으로. PIPA 누락·PG 선택동의
누락은 doc_lint에서 warning이므로 structure 차원으로는 잡히지 않음.

🗿 MoAI
EOF
)"
```

---

## Task 4: 차원 2 `citation` — FORMAT_ONLY + online monkeypatch

**Files:**
- Modify: `.claude/scripts/qa/finalize_run.py`
- Modify: `.claude/scripts/tests/test_finalize_run.py`
- Create: `.claude/scripts/tests/fixtures/gate/protocol_bad_pmid.md`

**Interfaces:**
- Consumes: Task 1~3의 전체
- Produces: `dim_citation(target, profile, ctx) -> dict` — `detail`에 `{total, format_fail, not_found, unverified_network}`

`citation_verify.audit_files([target], workspace=..., online=bool)`는 `{"summary": {"total", "format_fail", "not_found", "unverified_network"}, ...}`를 반환하고 `<workspace>/verification/citation_audit.json`에 쓴다. `not_found`/`unverified_network`는 `online=True`일 때만 채워진다.

`citation_verify.verify_online(citations, timeout=8)`는 `[{"type", "value", "exists", "status", "detail"}]`를 반환하며 `status` ∈ `"verified"` / `"not-found"` / `"unverified-network"` / `"bad-format"`.

- [ ] **Step 1: fixture 작성**

`.claude/scripts/tests/fixtures/gate/protocol_bad_pmid.md` — 형식은 올바르지만 존재하지 않는 PMID. 형식이 올바르므로 `format_fail=0`이고 `_reference_warnings`도 걸리지 않아 advisory를 오염시키지 않는다:

```markdown
# 임상시험 계획서 (게이트 테스트용 fixture — 미존재 PMID)

# B.1 General Information
# B.2 Background
선행 연구에서 반감기는 약 8시간으로 보고되었다 (PMID: 99999999).
# B.3 Objectives
# B.4 Trial Design
# B.5 Selection of Participants
# B.6 Interventions
# B.7 Discontinuation
# B.8 Assessment of Efficacy
# B.9 Assessment of Safety
# B.10 Statistics
# B.11 Direct Access
# B.12 Quality Control
# B.13 Ethics
# B.14 Data Handling
# B.15 Financing
# B.16 Publication
```

- [ ] **Step 2: 실패하는 테스트 추가**

```python
import citation_verify


def _mock_online(status):
    """verify_online 대체 — 네트워크 접근 없이 지정 status를 돌려준다."""
    def _fake(citations, timeout=8):
        out = []
        for kind in ("pmid", "nct"):
            for value in citations.get(kind, []):
                out.append({"type": kind, "value": value,
                            "exists": status == "verified",
                            "status": status, "detail": "mocked"})
        return out
    return _fake


def test_citation_is_format_only_in_draft(tmp_path):
    report = fr.run_gate(fixture("protocol_bad_pmid.md"), "draft",
                         str(tmp_path))
    citation = next(d for d in report["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.FORMAT_ONLY
    assert citation["detail"]["not_found"] == 0
    assert report["exit_code"] == fr.EXIT_OK


def test_citation_not_found_blocks_submission(tmp_path, monkeypatch):
    monkeypatch.setattr(citation_verify, "verify_online",
                        _mock_online("not-found"))
    report = fr.run_gate(fixture("protocol_bad_pmid.md"), "submission",
                         str(tmp_path))
    citation = next(d for d in report["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.FAIL
    assert citation["detail"]["not_found"] == 1
    assert report["exit_code"] == fr.EXIT_REJECTED


def test_citation_network_failure_blocks_submission(tmp_path, monkeypatch):
    monkeypatch.setattr(citation_verify, "verify_online",
                        _mock_online("unverified-network"))
    report = fr.run_gate(fixture("protocol_bad_pmid.md"), "submission",
                         str(tmp_path))
    citation = next(d for d in report["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.FAIL
    assert citation["detail"]["unverified_network"] == 1


def test_citation_verified_passes_submission(tmp_path, monkeypatch):
    monkeypatch.setattr(citation_verify, "verify_online",
                        _mock_online("verified"))
    report = fr.run_gate(fixture("protocol_bad_pmid.md"), "submission",
                         str(tmp_path))
    citation = next(d for d in report["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.PASS
```

- [ ] **Step 3: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v -k citation`
Expected: FAIL — `StopIteration` (citation 차원 없음)

- [ ] **Step 4: 구현 — `dim_citation`**

import 블록에 추가:

```python
import citation_verify  # noqa: E402
```

`dim_advisory` 뒤에 추가:

```python
_SUMMARY_KEYS = ("total", "format_fail", "not_found", "unverified_network")


def dim_citation(target, profile, ctx):
    """인용 검증. draft는 형식만(FORMAT_ONLY), submission은 online 필수.

    offline에서는 not_found가 구조적으로 항상 0이므로 '통과'라고 부르지 않고
    FORMAT_ONLY로 표기한다. submission 프로파일에서 FORMAT_ONLY는 차단이다
    (_BLOCKING 참조).
    """
    online = (profile == "submission")
    audit = citation_verify.audit_files(
        [target], workspace=ctx["workspace"], online=online)
    s = audit["summary"]
    detail = {k: s[k] for k in _SUMMARY_KEYS}

    findings = []
    if s["format_fail"]:
        findings.append(f"format_fail={s['format_fail']} — 잘못된 형식의 인용 id")

    if not online:
        return _dim("citation", FORMAT_ONLY, findings, detail=detail,
                    reason="offline — id 실제 존재 여부 미검증")

    if s["not_found"]:
        findings.append(f"not_found={s['not_found']} — 레지스트리에 없는 인용 id")
    if s["unverified_network"]:
        findings.append(
            f"unverified_network={s['unverified_network']} — 네트워크 검증 불가")

    return _dim("citation", FAIL if findings else PASS, findings, detail=detail)
```

`DIMENSIONS`를 교체:

```python
DIMENSIONS = (
    ("structure", dim_structure),
    ("citation", dim_citation),
    ("advisory", dim_advisory),
)
```

- [ ] **Step 5: 테스트를 실행해 통과를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v`
Expected: 16 passed

`test_clean_protocol_advisory_passes_submission`이 `protocol_clean.md`에 인용이 없어 여전히 통과함을 확인한다 (`total=0` → findings 없음 → PASS).

- [ ] **Step 6: 커밋**

```bash
git add .claude/scripts/qa/finalize_run.py .claude/scripts/tests/
git commit -m "$(cat <<'EOF'
feat(qa): release gate 차원 citation — FORMAT_ONLY / online 필수 분리

offline에서 not_found가 항상 0이므로 '통과'로 부르지 않고 FORMAT_ONLY로
표기하고, submission 프로파일에서는 이를 차단 상태로 집계.

🗿 MoAI
EOF
)"
```

---

## Task 5: 차원 3 `dose` + `goal_spec.trial_type` 판별

**Files:**
- Modify: `.claude/scripts/qa/finalize_run.py`
- Modify: `.claude/scripts/tests/test_finalize_run.py`
- Create: `.claude/scripts/tests/fixtures/gate/goal_spec_fih.json`
- Create: `.claude/scripts/tests/fixtures/gate/goal_spec_ddi.json`

**Interfaces:**
- Consumes: Task 1~4의 전체. `ctx["goal_spec"]`는 Task 2의 `run_gate`가 `doc_lint.load_goal_spec()`으로 이미 채워 둠 (경로가 없거나 깨져도 `None`, 예외 없음)
- Produces:
  - `_FIH_RE` — `re.compile(r"\b(FIH|SAD|MAD)\b", re.IGNORECASE)`
  - `_is_fih(goal_spec) -> bool | None` — `None`은 "알 수 없음"
  - `dim_dose(target, profile, ctx) -> dict`

`dose_safety_guard.check_file(path, mrsd_mg=None, mrsd_json=None)`는 `{"status": "ok"|"violation"|"skipped", "mrsd_mg": float|None, "violations": [{"message", ...}]}`를 반환한다. `mrsd_mg`가 `None`이면 `status="skipped"`다.

- [ ] **Step 1: goal_spec fixture 2개 작성**

`.claude/scripts/tests/fixtures/gate/goal_spec_fih.json`:

```json
{
  "schema": "trial_goal_spec/v1",
  "drug": "TEST-001",
  "trial_type": "FIH (SAD/MAD 포함)",
  "primary_objective": "건강한 성인에서 단회 상승 용량의 안전성·내성 평가"
}
```

`.claude/scripts/tests/fixtures/gate/goal_spec_ddi.json`:

```json
{
  "schema": "trial_goal_spec/v1",
  "drug": "TEST-002",
  "trial_type": "DDI",
  "primary_objective": "CYP2C19 기질과의 약물상호작용 평가"
}
```

- [ ] **Step 2: 실패하는 테스트 추가**

```python
def test_is_fih_word_boundary():
    assert fr._is_fih({"trial_type": "FIH (SAD/MAD 포함)"}) is True
    assert fr._is_fih({"trial_type": "sad"}) is True
    assert fr._is_fih({"trial_type": "DDI"}) is False
    assert fr._is_fih({"trial_type": "NOMADIC"}) is False, "부분 문자열 오탐 금지"
    assert fr._is_fih(None) is None, "goal_spec 없음은 '알 수 없음'"


def test_fih_without_mrsd_blocks_submission_only(tmp_path):
    draft = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path),
                        goal_spec_path=fixture("goal_spec_fih.json"))
    dose = next(d for d in draft["dimensions"] if d["id"] == "dose")
    assert dose["status"] == fr.SKIPPED
    assert draft["exit_code"] == fr.EXIT_OK

    sub = fr.run_gate(fixture("protocol_clean.md"), "submission",
                      str(tmp_path),
                      goal_spec_path=fixture("goal_spec_fih.json"))
    dose = next(d for d in sub["dimensions"] if d["id"] == "dose")
    assert dose["status"] == fr.FAIL
    assert sub["exit_code"] == fr.EXIT_REJECTED


def test_non_fih_dose_is_skipped_in_both_profiles(tmp_path):
    for profile in ("draft", "submission"):
        report = fr.run_gate(fixture("protocol_clean.md"), profile,
                             str(tmp_path),
                             goal_spec_path=fixture("goal_spec_ddi.json"))
        dose = next(d for d in report["dimensions"] if d["id"] == "dose")
        assert dose["status"] == fr.SKIPPED


def test_missing_goal_spec_blocks_submission(tmp_path):
    draft = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path))
    dose = next(d for d in draft["dimensions"] if d["id"] == "dose")
    assert dose["status"] == fr.SKIPPED

    sub = fr.run_gate(fixture("protocol_clean.md"), "submission",
                      str(tmp_path))
    dose = next(d for d in sub["dimensions"] if d["id"] == "dose")
    assert dose["status"] == fr.FAIL
    assert "trial_type" in " ".join(dose["findings"])


def test_dose_violation_blocks_both_profiles(tmp_path):
    mrsd = tmp_path / "mrsd.json"
    mrsd.write_text(json.dumps({"mrsd_mg": 1.0}), encoding="utf-8")
    doc = tmp_path / "protocol_overdose.md"
    doc.write_text(
        "\n".join(f"# B.{i} section" for i in range(1, 17))
        + "\n시작 용량: 50 mg\n", encoding="utf-8")

    for profile in ("draft", "submission"):
        report = fr.run_gate(str(doc), profile, str(tmp_path),
                             goal_spec_path=fixture("goal_spec_fih.json"),
                             mrsd_json=str(mrsd))
        dose = next(d for d in report["dimensions"] if d["id"] == "dose")
        assert dose["status"] == fr.FAIL
```

`mrsd.json`의 키 이름은 확인 완료다. `dose_safety_guard.mrsd_from_json`은
`("mrsd_mg_rounded", "mrsd_mg")` 순서로 찾아 첫 숫자 값을 쓰므로, 위 테스트의
`{"mrsd_mg": 1.0}`이 유효하다. 파일이 없거나 JSON이 깨져도 예외 없이 `None`을 반환한다.

- [ ] **Step 3: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v -k "fih or dose or goal_spec"`
Expected: FAIL — `AttributeError: module 'finalize_run' has no attribute '_is_fih'`

- [ ] **Step 4: 구현 — `_is_fih` + `dim_dose`**

import 블록에 추가:

```python
import re  # noqa: E402  (표준 라이브러리이므로 최상단 import 블록에 둔다)
import dose_safety_guard  # noqa: E402
```

`_dim` 뒤에 추가:

```python
# trial_type은 스키마상 자유 서술 문자열이므로 부분 일치가 필요하지만,
# 단어 경계 없이 매칭하면 다른 단어 속 SAD/MAD를 오탐한다.
_FIH_RE = re.compile(r"\b(FIH|SAD|MAD)\b", re.IGNORECASE)


def _is_fih(goal_spec):
    """FIH 계열 여부. goal_spec이 없으면 None('알 수 없음')을 돌려준다."""
    if not goal_spec:
        return None
    return bool(_FIH_RE.search(str(goal_spec.get("trial_type", ""))))
```

`dim_citation` 뒤에 추가:

```python
def dim_dose(target, profile, ctx):
    """FIH 시작 용량 대 MRSD. 시험유형을 모르면 submission에서 판정 불가로 차단."""
    fih = _is_fih(ctx["goal_spec"])
    mrsd_path = ctx["mrsd_json"]
    has_mrsd = bool(mrsd_path) and os.path.isfile(mrsd_path)

    if fih is None:
        if profile == "submission":
            return _dim("dose", FAIL,
                        ["goal_spec 없음 — trial_type을 확인할 수 없어 제출 판정 불가"])
        return _dim("dose", SKIPPED, reason="goal_spec 없음 (draft 허용)")

    if fih and not has_mrsd:
        if profile == "submission":
            return _dim("dose", FAIL,
                        ["FIH 계열이나 mrsd.json이 없어 MRSD 대조 불가"])
        return _dim("dose", SKIPPED,
                    reason="FIH이나 mrsd.json 없음 (draft 허용)")

    res = dose_safety_guard.check_file(
        target, mrsd_json=mrsd_path if has_mrsd else None)
    if res["status"] == "violation":
        return _dim("dose", FAIL, [v["message"] for v in res["violations"]],
                    mrsd_mg=res["mrsd_mg"])
    if res["status"] == "skipped":
        return _dim("dose", SKIPPED, reason="MRSD 없음 — 대조 대상 없음")
    return _dim("dose", PASS, mrsd_mg=res["mrsd_mg"])
```

`DIMENSIONS`를 교체:

```python
DIMENSIONS = (
    ("structure", dim_structure),
    ("citation", dim_citation),
    ("dose", dim_dose),
    ("advisory", dim_advisory),
)
```

- [ ] **Step 5: 테스트를 실행해 통과를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v`
Expected: 21 passed

- [ ] **Step 6: 커밋**

```bash
git add .claude/scripts/qa/finalize_run.py .claude/scripts/tests/
git commit -m "$(cat <<'EOF'
feat(qa): release gate 차원 dose + goal_spec trial_type 판별

FIH 계열인데 mrsd.json이 없으면 submission에서 차단. goal_spec 자체가 없으면
시험유형 확인 불가이므로 submission에서 '판정 불가'가 아니라 차단으로 처리.
trial_type 매칭은 단어 경계 정규식으로 오탐 방지.

🗿 MoAI
EOF
)"
```

---

## Task 6: 차원 5 `approval` + ERROR 우선순위 + score 참고 출력

**Files:**
- Modify: `.claude/scripts/qa/finalize_run.py`
- Modify: `.claude/scripts/tests/test_finalize_run.py`

**Interfaces:**
- Consumes: Task 1~5의 전체
- Produces:
  - `dim_approval(target, profile, ctx) -> dict` — 항상 `NOT_IMPLEMENTED`
  - `run_gate` 반환에 `score_informational` 키 (int 또는 `None`)
  - `run_gate` 반환의 `warnings` 리스트에 미구현 경고 문장

- [ ] **Step 1: 실패하는 테스트 추가**

```python
def test_approval_dimension_is_not_implemented(tmp_path):
    for profile in ("draft", "submission"):
        report = fr.run_gate(fixture("protocol_clean.md"), profile,
                             str(tmp_path),
                             goal_spec_path=fixture("goal_spec_ddi.json"))
        approval = next(d for d in report["dimensions"]
                        if d["id"] == "approval")
        assert approval["status"] == fr.NOT_IMPLEMENTED
        assert report["exit_code"] == fr.EXIT_OK, "미구현은 차단하지 않는다"
        assert any("승인" in w for w in report["warnings"]), \
            "미구현 통제는 매 실행마다 경고로 노출되어야 함"


def test_checker_crash_yields_undecidable(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("simulated engine crash")

    monkeypatch.setattr(doc_lint_module, "lint_file", boom)
    report = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path))
    statuses = {d["id"]: d["status"] for d in report["dimensions"]}
    assert statuses["structure"] == fr.ERROR
    assert report["result"] == "UNDECIDABLE"
    assert report["exit_code"] == fr.EXIT_UNDECIDABLE


def test_error_takes_precedence_over_fail(tmp_path, monkeypatch):
    """structure는 ERROR, dose는 FAIL — exit는 2여야 한다."""
    def boom(*a, **k):
        raise RuntimeError("simulated engine crash")

    monkeypatch.setattr(doc_lint_module, "lint_file", boom)
    report = fr.run_gate(fixture("protocol_clean.md"), "submission",
                         str(tmp_path))
    statuses = {d["id"]: d["status"] for d in report["dimensions"]}
    assert statuses["structure"] == fr.ERROR
    assert statuses["dose"] == fr.FAIL, "goal_spec 없음 → submission FAIL"
    assert report["exit_code"] == fr.EXIT_UNDECIDABLE


def test_score_is_informational_only(tmp_path):
    report = fr.run_gate(fixture("protocol_clean.md"), "submission",
                         str(tmp_path),
                         goal_spec_path=fixture("goal_spec_ddi.json"))
    assert isinstance(report["score_informational"], int)
    assert "score" not in [d["id"] for d in report["dimensions"]], \
        "score는 차원이 아니다"
```

테스트 파일 상단 import에 추가 (monkeypatch 대상 모듈을 별칭으로 잡는다 — `finalize_run`이 `import doc_lint`로 같은 모듈 객체를 참조하므로 별칭 패치가 게이트에도 적용된다):

```python
import doc_lint as doc_lint_module
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v -k "approval or crash or precedence or score"`
Expected: FAIL — `StopIteration` (approval 차원 없음), `KeyError: 'score_informational'`

- [ ] **Step 3: 구현 — `dim_approval` + score + 경고**

`dim_advisory` 뒤에 추가:

```python
def dim_approval(target, profile, ctx):
    """사람 승인 이벤트. 서명 이벤트 스토어(P0-5)가 없어 아직 판정할 수 없다.

    이 차원을 조용히 빼는 대신 NOT_IMPLEMENTED로 매 실행 출력에 노출시킨다.
    이 게이트가 고치려는 문제 자체가 '검사가 있는 척'이었으므로, 같은 종류의
    공백을 새로 만들지 않는다.
    """
    return _dim("approval", NOT_IMPLEMENTED,
                reason="서명 이벤트 스토어 미구현 (P0-5)")
```

`DIMENSIONS`를 교체:

```python
DIMENSIONS = (
    ("structure", dim_structure),
    ("citation", dim_citation),
    ("dose", dim_dose),
    ("advisory", dim_advisory),
    ("approval", dim_approval),
)
```

`run_gate`의 `doc_type = ...` 줄 뒤, `return` 앞에 추가:

```python
    # score는 참고 수치이며 판정에 사용하지 않는다 (설계 D2). 계산이 실패해도
    # 차단하지 않고 None으로 둔다.
    try:
        score = doc_lint.score_file(target, goal_spec=ctx["goal_spec"])["score"]
    except Exception:  # noqa: BLE001 — 참고 수치이므로 실패를 삼킨다
        score = None

    gate_warnings = []
    if any(d["status"] == NOT_IMPLEMENTED for d in dims):
        gate_warnings.append(
            "미구현 차원이 있습니다 (사람 승인) — 이 결과는 '제출 가능'을 의미하지 않습니다")
```

`return` 딕셔너리의 `"warnings": []`를 교체하고 `score_informational`을 추가:

```python
        "score_informational": score,
        "warnings": gate_warnings,
```

`main()`의 출력 루프 뒤에 추가:

```python
    if report["score_informational"] is not None:
        print(f"  score {report['score_informational']}/100 (참고, 판정 미사용)")
    for w in report["warnings"]:
        print(f"  ⚠️  {w}")
```

- [ ] **Step 4: 테스트를 실행해 통과를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v`
Expected: 26 passed

- [ ] **Step 5: 커밋**

```bash
git add .claude/scripts/qa/finalize_run.py .claude/scripts/tests/
git commit -m "$(cat <<'EOF'
feat(qa): release gate 차원 approval(NOT_IMPLEMENTED) + ERROR 우선순위

미구현 통제를 조용히 빠뜨리지 않고 매 실행 출력에 노출. ERROR와 FAIL이
동시 존재하면 exit 2 우선 — 검사기가 깨진 상태에서 FAIL 목록이 완전하다고
주장할 수 없기 때문.

🗿 MoAI
EOF
)"
```

---

## Task 7: `release_gate.json` 리포트 + 쓰기 실패 exit 2

**Files:**
- Modify: `.claude/scripts/qa/finalize_run.py`
- Modify: `.claude/scripts/tests/test_finalize_run.py`

**Interfaces:**
- Consumes: Task 1~6의 전체
- Produces: `_write_report(report, workspace) -> str` (기록된 절대/상대 경로 반환, 실패 시 예외 전파)

- [ ] **Step 1: 실패하는 테스트 추가**

```python
def test_report_is_written_with_schema_and_all_dimensions(tmp_path):
    code = fr.main([fixture("protocol_clean.md"),
                    "--profile", "draft",
                    "--workspace", str(tmp_path),
                    "--goal-spec", fixture("goal_spec_ddi.json")])
    assert code == fr.EXIT_OK

    out = tmp_path / "verification" / "release_gate.json"
    assert out.is_file()
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["schema"] == "release_gate/v1"
    assert saved["profile"] == "draft"
    assert saved["result"] == "PASS"
    assert saved["exit_code"] == 0
    assert [d["id"] for d in saved["dimensions"]] == [
        "structure", "citation", "dose", "advisory", "approval"]
    assert saved["warnings"], "approval NOT_IMPLEMENTED 경고가 기록되어야 함"


def test_report_write_failure_is_undecidable(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise OSError("read-only filesystem")

    monkeypatch.setattr(fr, "_write_report", boom)
    code = fr.main([fixture("protocol_clean.md"),
                    "--workspace", str(tmp_path)])
    assert code == fr.EXIT_UNDECIDABLE


def test_report_records_failure_details(tmp_path):
    code = fr.main([fixture("protocol_missing_b7.md"),
                    "--profile", "draft",
                    "--workspace", str(tmp_path)])
    assert code == fr.EXIT_REJECTED

    saved = json.loads(
        (tmp_path / "verification" / "release_gate.json").read_text(
            encoding="utf-8"))
    assert saved["result"] == "FAIL"
    assert "structure" in saved["blocked_dimensions"]
    structure = next(d for d in saved["dimensions"]
                     if d["id"] == "structure")
    assert structure["findings"], "차단 사유가 리포트에 남아야 함"
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v -k report`
Expected: FAIL — `AssertionError: assert False` (`release_gate.json`이 생성되지 않음)

- [ ] **Step 3: 구현 — `_write_report` + `main` 연결**

`run_gate` 뒤에 추가:

```python
def _write_report(report, workspace):
    """리포트를 <workspace>/verification/release_gate.json에 기록한다.

    실패 시 예외를 전파한다 — 증거를 남기지 못하면 통과를 주장하지 않는다.
    """
    out = os.path.join(workspace, "verification", "release_gate.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return out
```

`main()`에서 `report = run_gate(...)` 뒤, 출력 루프 앞에 추가:

```python
    try:
        report_path = _write_report(report, args.workspace)
    except OSError as exc:
        print(f"⛔ 최종화 거부: 리포트 기록 실패 — {exc}", file=sys.stderr)
        print("   증거를 남기지 못하면 통과를 주장하지 않습니다.", file=sys.stderr)
        return EXIT_UNDECIDABLE
```

`main()`의 마지막 `return report["exit_code"]` 앞에 추가:

```python
    print(f"  -> {report_path}")
```

- [ ] **Step 4: 테스트를 실행해 통과를 확인**

Run: `python3 -m pytest .claude/scripts/tests/test_finalize_run.py -v`
Expected: 29 passed

- [ ] **Step 5: 커밋**

```bash
git add .claude/scripts/qa/finalize_run.py .claude/scripts/tests/
git commit -m "$(cat <<'EOF'
feat(qa): release_gate.json 리포트 + 쓰기 실패 시 exit 2

증거를 남기지 못하면 통과를 주장하지 않는다 — 리포트 기록 실패를
판정 불가로 처리.

🗿 MoAI
EOF
)"
```

---

## Task 8: `finalize.md` 래퍼 축소 + 수용 기준 전량 검증 + plugin 동기화

**Files:**
- Modify: `.claude/commands/finalize.md` (전체 재작성)
- Modify: `plugin/clinical-pharmacology-study-protocol-development/**` (`./sync_plugin.sh` 결과)

**Interfaces:**
- Consumes: Task 1~7이 만든 `finalize_run.py` CLI
- Produces: 없음 (최종 태스크)

- [ ] **Step 1: v2 golden fixture 회귀 테스트 추가**

`.claude/scripts/tests/test_finalize_run.py`에 추가. 저장소 루트를 `__file__` 기준으로 올라가 찾는다:

```python
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
V2_GOLDEN = os.path.join(
    _REPO_ROOT, "e2e", "v2_2026_04_14_DDI", "_workspace",
    "03_protocol_draft.md")


def test_v2_golden_fixture_passes_draft(tmp_path):
    """기존 산출물 회귀 방지 — CI가 --strict로 통과시키는 파일."""
    assert os.path.isfile(V2_GOLDEN), V2_GOLDEN
    report = fr.run_gate(V2_GOLDEN, "draft", str(tmp_path))
    assert report["exit_code"] == fr.EXIT_OK, report["blocked_dimensions"]
```

- [ ] **Step 2: 테스트 실행 — 전량 통과 확인**

Run: `python3 -m pytest .claude/scripts/tests/ -v`
Expected: 30 passed (신규 30개 + 기존 테스트 전량). 기존 테스트가 하나라도 깨지면 검사기를 건드린 것이므로 되돌린다.

- [ ] **Step 3: `finalize.md`를 래퍼로 재작성**

`.claude/commands/finalize.md` 전체를 다음으로 교체:

```markdown
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

## Gotchas

- **프로파일을 구분한다.** 작성 중에는 `draft`(기본)를 쓴다. `draft`는 placeholder와
  미확인 인용을 표시만 하고 통과시킨다 — 초안 단계에서는 정상 상태이기 때문이다.
  제출 직전에만 `submission`을 쓴다.
- **`submission`은 네트워크가 필요하다.** 인용 id를 실제 레지스트리에 조회하며,
  네트워크 불가는 통과가 아니라 차단(`unverified_network`)이다. 폐쇄망에서는
  `draft`로 구조·권고 사항만 점검하고, 인용 검증은 외부망에서 별도로 수행한다.
- **승인 차원은 아직 미구현이다.** 게이트가 통과해도 사람 승인은 검증되지 않았으므로
  "제출 가능"을 의미하지 않는다. 게이트 출력의 경고를 사용자에게 그대로 전달한다.
- **score는 판정에 쓰이지 않는다.** 참고 수치로만 출력된다. `score 100`이 규제
  적합성을 의미하지 않는다는 것이 이 게이트를 만든 이유다.
- venv가 없으면 `python3`로 대체 실행한다.
```

- [ ] **Step 4: plugin 동기화 + 불변식 검증**

```bash
./sync_plugin.sh
python3 .github/scripts/validate_manifests.py; echo "validate_manifests exit=$?"
python3 .github/scripts/check_internal_refs.py; echo "check_internal_refs exit=$?"
```

Expected: `validate_manifests exit=0`, `check_internal_refs exit=0`

`sync_plugin.sh`가 `finalize.md`의 `.claude/` 참조를 `${CLAUDE_PLUGIN_ROOT}/`로 치환한다. `finalize_run.py`는 `__file__` 상대경로만 쓰므로 치환 대상이 없다.

- [ ] **Step 5: 수용 기준 7개 전량 검증**

설계 §11의 기준을 순서대로 확인한다.

```bash
# 기준 1 — fixture 6종이 submission에서 전부 exit != 0
for f in protocol_bad_pmid protocol_unverified_marker icf_no_pipa \
         icf_pg_without_part4 protocol_missing_b7; do
  python3 .claude/scripts/qa/finalize_run.py \
    .claude/scripts/tests/fixtures/gate/$f.md \
    --profile submission --workspace /tmp/gate-check >/dev/null 2>&1
  echo "$f submission exit=$?"
done
# FIH+mrsd 없음은 goal_spec이 필요하다
python3 .claude/scripts/qa/finalize_run.py \
  .claude/scripts/tests/fixtures/gate/protocol_clean.md \
  --profile submission --workspace /tmp/gate-check \
  --goal-spec .claude/scripts/tests/fixtures/gate/goal_spec_fih.json >/dev/null 2>&1
echo "fih_no_mrsd submission exit=$?"
```
Expected: 6줄 모두 `exit=1`

```bash
# 기준 2 — draft에서는 protocol_missing_b7만 exit != 0
for f in protocol_bad_pmid protocol_unverified_marker icf_no_pipa \
         icf_pg_without_part4 protocol_missing_b7; do
  python3 .claude/scripts/qa/finalize_run.py \
    .claude/scripts/tests/fixtures/gate/$f.md \
    --profile draft --workspace /tmp/gate-check >/dev/null 2>&1
  echo "$f draft exit=$?"
done
```
Expected: `protocol_missing_b7 draft exit=1`, 나머지 4개 `exit=0`

```bash
# 기준 3·4·6·7 — pytest가 커버
python3 -m pytest .claude/scripts/tests/ -q
# 기준 5 — plugin 동기화 불변식
python3 .github/scripts/validate_manifests.py; echo "exit=$?"
```
Expected: pytest 전량 통과, `exit=0`

기준 3(검사기 크래시 → exit 2)은 `test_checker_crash_yields_undecidable`,
기준 4(v2 golden draft 통과)는 `test_v2_golden_fixture_passes_draft`,
기준 7(리포트 스키마·차원 5개·경고)은 `test_report_is_written_with_schema_and_all_dimensions`가 각각 검증한다.

- [ ] **Step 6: 커밋**

```bash
git add .claude/commands/finalize.md .claude/scripts/tests/ plugin/
git commit -m "$(cat <<'EOF'
refactor(finalize): /finalize를 release 게이트 래퍼로 축소

판정 로직을 finalize_run.py로 이전. 커맨드는 대상·프로파일을 결정하고
종료코드를 재해석 없이 전달한다. --profile draft/submission 안내 추가.

수용 기준 7개 검증:
- submission에서 fixture 6종 전부 exit 1
- draft에서는 구조 결함(B.7 누락)만 exit 1
- 검사기 크래시 exit 2, v2 golden draft 통과
- validate_manifests / check_internal_refs exit 0

🗿 MoAI
EOF
)"
```

---

## Self-Review 결과

**1. 스펙 커버리지** — 설계 문서 각 절이 어느 태스크에 대응하는지:

| 스펙 절 | 태스크 |
|--------|-------|
| §3 D1 (import 호출) | Task 2·4·5의 import 블록 |
| §3 D2 (score 제거) | Task 6 (`score_informational`, `test_score_is_informational_only`) |
| §3 D3 (게이트가 심각도 소유) | Task 3 (`dim_advisory`의 profile 분기) |
| §3 D4 (두 프로파일) | Task 4 (`dim_citation`), Task 3, Task 5 |
| §3 D5 (advisory = warning 전체) | Task 3 |
| §5 상태 어휘 6개 | Task 1 (`test_status_constants_are_self_named`) |
| §6 차원 1 structure | Task 2 |
| §6 차원 2 citation | Task 4 |
| §6 차원 3 dose | Task 5 |
| §6 차원 4 advisory | Task 3 |
| §6 차원 5 approval | Task 6 |
| §6.1 trial_type 판별 | Task 5 (`_is_fih`, 단어 경계 테스트 포함) |
| §7 오류 처리·종료코드 | Task 1(입력), Task 6(크래시·우선순위), Task 7(리포트 실패) |
| §8 release_gate.json | Task 7 |
| §9 finalize.md 축소 | Task 8 |
| §10 테스트 계획 | Task 1~8에 분산 |
| §10.1 단일 결함 원칙 | Task 2·3·4의 fixture 본문에 반영 |
| §11 수용 기준 7개 | Task 8 Step 5 |
| §12 변경 파일 | Task 8 Step 4 (sync) |

누락 없음.

**2. 플레이스홀더 스캔** — "TBD"/"적절히 처리"/"위 내용에 대한 테스트 작성"/"Task N과 유사" 없음. 모든 코드 스텝에 실제 코드 블록이 있다. Task 5의 `mrsd.json` 키 이름은 `dose_safety_guard.mrsd_from_json`을 읽어 확정했다(`mrsd_mg_rounded` 또는 `mrsd_mg`). 미확인 항목은 남아 있지 않다.

**3. 타입 일관성** — 태스크 간 이름 대조:

- `_dim(dim_id, status, findings=None, **extra)` — Task 1 정의, Task 2~6에서 동일 시그니처로 호출
- `run_gate(target, profile, workspace, goal_spec_path=None, mrsd_json=None)` — Task 2 정의, Task 3~7 테스트에서 동일 인자명 사용
- `ctx` 키 `{target, profile, workspace, goal_spec, mrsd_json}` — Task 2 정의, Task 4가 `ctx["workspace"]`, Task 5가 `ctx["goal_spec"]`/`ctx["mrsd_json"]` 사용
- `DIMENSIONS` — Task 2에서 1개로 시작, Task 3·4·5·6에서 각각 교체하며 최종 5개. 매번 전체 튜플을 다시 적어 순서를 고정했다
- 상태 상수 이름이 전 태스크에서 `fr.PASS` 등으로 일관
- `detail` 키는 `dim_citation`만 사용하며 `_SUMMARY_KEYS`의 4개 키로 고정

불일치 없음.
