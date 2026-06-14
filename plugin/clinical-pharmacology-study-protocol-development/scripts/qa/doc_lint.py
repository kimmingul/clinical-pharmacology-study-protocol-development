#!/usr/bin/env python3
"""Deterministic quality lint for generated trial documents (protocol / ICF).

Single source of truth used by BOTH:
  - CI (the GitHub Actions workflow) as a --strict gate on the golden fixtures, and
  - the PostToolUse advisory hook (hooks/draft_advisory_hook.py) which warns
    (never blocks) right after a draft is written.

Encodes the qa-reviewer checklist as code so output-quality regressions are
caught automatically: ICH E6(R3) Appendix B section coverage, the recurring
3년-vs-15년 document-retention error, BE/DDI 90% CI bounds, unresolved
placeholders, and unverified-citation markers.

Usage:
    doc_lint.py <file.md> [--strict] [--type protocol|icf]
    doc_lint.py <file.md> --score [--goal-spec goal_spec.json]

Without --strict it prints a report and exits 0 (advisory). With --strict it
exits 1 on any ERROR (or, equivalently, on any score_file critical). The
document type is inferred from the filename when --type is omitted.

--score prints a deterministic score dict (see score_file) as JSON and exits 0.
--goal-spec optionally points at a trial_goal_spec/v1 instance
(.claude/references/schemas/trial_goal_spec.schema.json) whose targets are
enforced additively by score_file / --strict.

Note: `[시험기관명]` is an intentional, documented placeholder (filled after IRB
approval) and is NOT treated as unresolved.
"""
import argparse
import json
import os
import re
import sys

REQUIRED_SECTIONS = [f"B.{i}" for i in range(1, 17)]  # ICH E6(R3) Appendix B

PLACEHOLDER_PATTERNS = [
    r"\[추가 정보 필요",
    r"\[작성 필요",
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bXXX\b",
    r"lorem ipsum",
]

# Harness markers that flag a citation/datum still needs verification.
UNVERIFIED_MARKERS = [
    r"\[출처 미확인",
    r"\[출처 확인 필요",
    r"\[발행일 확인 필요",
    r"\[IB 확인 필요",
    r"\[미수집",
    r"\[확인 필요",
]


def _reference_warnings(text):
    """Conservative citation checks (advisory). Avoids flagging the bare words
    'PMID'/'NCT' in prose — only clearly malformed ids or placeholder tokens."""
    warnings = []
    n_unverified = sum(len(re.findall(p, text)) for p in UNVERIFIED_MARKERS)
    if n_unverified:
        warnings.append(
            f"{n_unverified} unverified-citation marker(s) (e.g. [출처 미확인]) "
            f"— confirm or remove before finalizing"
        )
    # Placeholder ids left in citations (PMID/NCT followed by TBD/xxx/?/미상).
    if re.search(r"\b(?:PMID|NCT)\s*[:#]?\s*(?:TBD|xxx|XXX|\?+|미상)", text):
        warnings.append("placeholder citation id (PMID/NCT: TBD/xxx/?) — fill in real id")
    # Malformed NCT: NCT followed by 1-7 digits (valid is exactly 8).
    if re.search(r"\bNCT[0-9]{1,7}\b(?![0-9])", text):
        warnings.append("NCT id with wrong digit count (valid is NCT + 8 digits) — verify")
    return warnings


def _placeholder_warnings(text):
    out = []
    for pat in PLACEHOLDER_PATTERNS:
        for m in re.finditer(pat, text):
            out.append(f"unresolved placeholder marker: {m.group(0)!r}")
    return out


def lint_protocol(text):
    """Return (errors, warnings) for a protocol draft."""
    errors, warnings = [], []

    present = {f"B.{n}" for n in re.findall(r"^#+\s*B\.(\d+)\b", text, re.M)}
    missing = [s for s in REQUIRED_SECTIONS if s not in present]
    if missing:
        errors.append(
            f"ICH E6(R3) Appendix B sections missing: {', '.join(missing)} "
            f"({len(present)}/16 present)"
        )

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

    if re.search(r"90%\s*(?:신뢰구간|CI)", text) or "동등성" in text:
        if not ("80.00" in text and "125.00" in text):
            warnings.append(
                "90% CI / equivalence referenced but '80.00' and '125.00' "
                "bounds not both present"
            )

    warnings += _placeholder_warnings(text)
    warnings += _reference_warnings(text)
    return errors, warnings


def lint_icf(text):
    """Return (errors, warnings) for an ICF draft (softer; advisory-focused)."""
    errors, warnings = [], []

    if "개인정보" not in text:
        warnings.append("ICF: no '개인정보' (PIPA) consent content detected")

    # If genomic / metabolomic / human-derived-material analysis is mentioned,
    # an optional-consent (Part 4) section is expected (생명윤리법).
    if re.search(r"유전체|약물유전|대사체|인체유래물|잔여\s*검체", text):
        if not re.search(r"Part\s*4|선택\s*동의|별도\s*동의", text):
            warnings.append(
                "ICF mentions PG/metabolomic/biobank but no optional-consent "
                "(Part 4 / 선택 동의) section detected — 생명윤리법"
            )

    warnings += _placeholder_warnings(text)
    warnings += _reference_warnings(text)
    return errors, warnings


def lint_file(path, doc_type=None):
    text = open(path, encoding="utf-8").read()
    if doc_type is None:
        base = os.path.basename(path)
        doc_type = "icf" if "icf" in base.lower() else "protocol"
    if doc_type == "icf":
        return ("icf",) + lint_icf(text)
    return ("protocol",) + lint_protocol(text)


# Warning substrings that escalate a lint WARNING to Major (vs. Minor).
_MAJOR_WARNING_HINTS = (
    "retention", "보존", "보유",
    "ci", "80.00", "125.00", "동등성",
    "생명윤리", "pipa", "개인정보",
    "appendix", "section", "part 4", "선택 동의",
)


def load_goal_spec(path):
    """Safely load a trial_goal_spec/v1 JSON instance.

    Returns the parsed dict, or None if the path is missing/unreadable or the
    content is not a JSON object. Never raises for ordinary I/O or parse errors.
    """
    if not path:
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _dedup_keep_order(items):
    seen, out = set(), []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)
    return out


def _goal_spec_findings(text, doc_type, goal_spec):
    """Additional Critical/Major findings derived from a goal_spec.

    Returns (critical, major). Additive to the base lint output; deduped by the
    caller. Empty when goal_spec is falsy.
    """
    critical, major = [], []
    if not goal_spec:
        return critical, major

    required = goal_spec.get("required_ich_sections")
    if isinstance(required, list) and required:
        present = {f"B.{n}" for n in re.findall(r"^#+\s*B\.(\d+)\b", text, re.M)}
        missing = [s for s in required if s not in present]
        if missing:
            critical.append(
                f"goal_spec required ICH section(s) missing: {', '.join(missing)}"
            )

    min_years = goal_spec.get("retention_years_min")
    if isinstance(min_years, int):
        for m in re.finditer(r"(?:보존|보유)\s*기간[^\n]*?(\d+)\s*년", text):
            if int(m.group(1)) < min_years:
                critical.append(
                    f"retention period {m.group(1)}년 below goal_spec minimum "
                    f"{min_years}년: '{m.group(0).strip()[:90]}'"
                )

    if goal_spec.get("pg_or_biobank_required") and doc_type == "icf":
        if not re.search(r"Part\s*4|선택\s*동의|별도\s*동의", text):
            major.append(
                "goal_spec requires PG/biobank consent but ICF has no "
                "Part 4 / 선택 동의 section (생명윤리법)"
            )

    return critical, major


def score_file(path, doc_type=None, goal_spec=None):
    """Score a document deterministically from the base lint output.

    Scoring rule:
      - start at 100.
      - each base lint ERROR -> critical, -20 each (score floored at 0).
      - each base lint WARNING mentioning retention / CI / '80.00' /
        생명윤리 / PIPA / Appendix / section (see _MAJOR_WARNING_HINTS)
        -> major, -8 each; every other warning -> minor, -2 each.
      - if goal_spec is given, add findings from _goal_spec_findings:
        missing required_ich_sections -> critical; a 보존/보유 기간 ... N년 with
        N < retention_years_min -> critical; pg_or_biobank_required on an ICF
        lacking Part 4 / 선택 동의 -> major. These are additive and deduped
        against the base findings, and each contributes the same point penalty
        as its base-tier equivalent (critical -20, major -8).
      - passed = (no critical) and (score >= 90).

    Returns a dict: doc_type, score (int 0..100), critical, major, minor, passed.
    """
    doc_type, errors, warnings = lint_file(path, doc_type)

    critical = list(errors)
    major, minor = [], []
    for w in warnings:
        lw = w.lower()
        if any(h in lw for h in _MAJOR_WARNING_HINTS):
            major.append(w)
        else:
            minor.append(w)

    text = open(path, encoding="utf-8").read()
    gs_critical, gs_major = _goal_spec_findings(text, doc_type, goal_spec)

    critical = _dedup_keep_order(critical + gs_critical)
    major = _dedup_keep_order(major + gs_major)
    minor = _dedup_keep_order(minor)

    score = 100 - 20 * len(critical) - 8 * len(major) - 2 * len(minor)
    score = max(0, min(100, score))

    return {
        "doc_type": doc_type,
        "score": score,
        "critical": critical,
        "major": major,
        "minor": minor,
        "passed": len(critical) == 0 and score >= 90,
    }


def main():
    ap = argparse.ArgumentParser(description="Lint a generated protocol/ICF draft.")
    ap.add_argument("path")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any ERROR")
    ap.add_argument("--type", choices=["protocol", "icf"], default=None)
    ap.add_argument("--score", action="store_true",
                    help="print the score dict as JSON and exit 0")
    ap.add_argument("--goal-spec", default=None,
                    help="path to a trial_goal_spec/v1 JSON (used by --score/--strict)")
    args = ap.parse_args()

    goal_spec = load_goal_spec(args.goal_spec)

    if args.score:
        result = score_file(args.path, args.type, goal_spec)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    doc_type, errors, warnings = lint_file(args.path, args.type)
    print(f"Doc lint ({doc_type}): {args.path}")
    if errors:
        print(f"  ERRORS ({len(errors)}):")
        for e in errors:
            print(f"    - {e}")
    if warnings:
        print(f"  warnings ({len(warnings)}):")
        for w in warnings:
            print(f"    - {w}")
    if not errors and not warnings:
        print("  OK")

    if args.strict and score_file(args.path, args.type, goal_spec)["critical"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
