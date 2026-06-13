#!/usr/bin/env python3
"""Lint a generated protocol draft against ICH E6(R3) Appendix B structure and
key MFDS/KGCP regulatory constants.

Deterministic encoding of the qa-reviewer checklist, so output-quality
regressions (missing required sections, the recurring 3년-vs-15년 document
retention error, missing BE/DDI CI bounds, unresolved placeholders) are caught
automatically — by CI on the golden fixtures and as a gate on new drafts.

Usage:
    protocol_lint.py <protocol.md> [--strict]

Without --strict it prints a report and always exits 0 (advisory).
With --strict it exits 1 if any ERROR is found.

Note: `[시험기관명]` is an intentional, documented placeholder (filled after IRB
approval) and is NOT treated as an unresolved placeholder.
"""
import argparse
import re
import sys

REQUIRED_SECTIONS = [f"B.{i}" for i in range(1, 17)]  # ICH E6(R3) Appendix B

# Real "left something unfinished" markers. `[시험기관명]` is deliberately excluded.
PLACEHOLDER_PATTERNS = [
    r"\[추가 정보 필요",
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bXXX\b",
    r"lorem ipsum",
    r"\[작성 필요",
]


def lint(text):
    errors, warnings = [], []

    # 1. ICH E6(R3) Appendix B section coverage (headings like "# B.7 ...")
    present = {f"B.{n}" for n in re.findall(r"^#+\s*B\.(\d+)\b", text, re.M)}
    missing = [s for s in REQUIRED_SECTIONS if s not in present]
    if missing:
        errors.append(
            f"ICH E6(R3) Appendix B sections missing: {', '.join(missing)} "
            f"({len(present)}/16 present)"
        )

    # 2. Document retention period — KGCP requires 15 years, not 3.
    for m in re.finditer(r"(?:보존|보유)\s*기간[^\n]*", text):
        line = m.group(0)
        if re.search(r"3\s*년", line) and "15년" not in line:
            errors.append(
                f"document retention looks like 3년 (KGCP requires 15년): "
                f"'{line.strip()[:90]}'"
            )
    for m in re.finditer(r"최소\s*3\s*년[^\n]*KGCP", text):
        errors.append(
            f"retention '최소 3년 ... KGCP' must be 15년: '{m.group(0).strip()[:90]}'"
        )

    # 3. BE/DDI equivalence CI bounds present when a 90% CI / equivalence claim is made.
    if re.search(r"90%\s*(?:신뢰구간|CI)", text) or "동등성" in text:
        if not ("80.00" in text and "125.00" in text):
            warnings.append(
                "90% CI / equivalence referenced but '80.00' and '125.00' "
                "bounds not both present"
            )

    # 4. Unresolved placeholders (excluding the intentional [시험기관명]).
    for pat in PLACEHOLDER_PATTERNS:
        for m in re.finditer(pat, text):
            warnings.append(f"unresolved placeholder marker: {m.group(0)!r}")

    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any ERROR")
    args = ap.parse_args()

    text = open(args.path, encoding="utf-8").read()
    errors, warnings = lint(text)

    print(f"Protocol lint: {args.path}")
    if errors:
        print(f"  ERRORS ({len(errors)}):")
        for e in errors:
            print(f"    - {e}")
    if warnings:
        print(f"  warnings ({len(warnings)}):")
        for w in warnings:
            print(f"    - {w}")
    if not errors and not warnings:
        print("  OK — 16/16 sections, retention 15년, CI bounds present, no placeholders")

    if args.strict and errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
