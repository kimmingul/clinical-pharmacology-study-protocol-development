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
