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
import re
import sys
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import doc_lint  # noqa: E402
import citation_verify  # noqa: E402
import dose_safety_guard  # noqa: E402

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


# trial_type은 스키마상 자유 서술 문자열이므로 부분 일치가 필요하지만,
# 단어 경계 없이 매칭하면 다른 단어 속 SAD/MAD를 오탐한다.
_FIH_RE = re.compile(r"\b(FIH|SAD|MAD)\b", re.IGNORECASE)


def _is_fih(goal_spec):
    """FIH 계열 여부. goal_spec이 없으면 None('알 수 없음')을 돌려준다."""
    if not goal_spec:
        return None
    return bool(_FIH_RE.search(str(goal_spec.get("trial_type", ""))))


def dim_structure(target, profile, ctx):
    """doc_lint ERROR — 구조·법정 보존기간 등 하드 결함. 프로파일 무관."""
    doc_type, errors, _warnings = doc_lint.lint_file(target)
    status = FAIL if errors else PASS
    return _dim("structure", status, errors, doc_type=doc_type)


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


DIMENSIONS = (
    ("structure", dim_structure),
    ("citation", dim_citation),
    ("dose", dim_dose),
    ("advisory", dim_advisory),
)

# 프로파일별 차단 상태 집합. SKIPPED/NOT_IMPLEMENTED는 어느 쪽도 차단하지 않는다.
_BLOCKING = {
    "draft": {FAIL, ERROR},
    "submission": {FAIL, ERROR, FORMAT_ONLY},
}


def _utc_now():
    """UTC ISO-8601. 형식은 citation_verify._utc_now()와 동일해야 한다 —
    두 산출물이 같은 _workspace/verification/ 디렉토리에서 같은 generated_utc
    필드명을 쓰므로 형식이 갈리면 안 된다 (citation_verify.py:59-60 참조).
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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

    report = run_gate(args.target, args.profile, args.workspace,
                      goal_spec_path=args.goal_spec, mrsd_json=args.mrsd_json)
    print(f"release gate ({args.profile}): {report['result']}")
    for d in report["dimensions"]:
        print(f"  [{d['id']}] {d['status']}")
        for f in d["findings"]:
            print(f"      - {f}")
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
