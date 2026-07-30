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
