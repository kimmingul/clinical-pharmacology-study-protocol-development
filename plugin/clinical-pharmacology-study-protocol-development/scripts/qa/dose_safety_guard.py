#!/usr/bin/env python3
"""Deterministic dose-safety guardrail (zero-trust, T0-blocking).

For First-in-Human (FIH/SAD/MAD) protocols, a stated starting or escalation dose
that exceeds the computed Maximum Recommended Starting Dose (MRSD) is a
patient-safety defect. This guard treats any numeric dose written into a protocol
as UNTRUSTED and checks it against an independently computed MRSD
(`.claude/scripts/fih/starting_dose_calculation.py` -> a provenance JSON, or an
explicit --mrsd-mg).

Design choices (high precision, low false-positive):
  * Only doses that are clearly LABELLED as a starting/initial dose are checked
    (시작/초기/개시 용량, "starting dose", "initial dose", "MRSD"). Generic dose
    mentions are ignored so multi-dose escalation tables don't trip the guard.
  * If no MRSD is available (non-FIH trials: DDI/BE/FE/QTc/ADME), the guard
    returns status "skipped" — it is a NO-OP, never a violation.
  * Unit-aware: mg and µg/mcg/ug are normalized to mg.

Usage
-----
    dose_safety_guard.py <protocol.md> --mrsd-mg 29.0
    dose_safety_guard.py <protocol.md> --mrsd-json _workspace/00_input/mrsd.json
    # exit 0 = ok or skipped; exit 1 = violation (with --strict)

The MRSD JSON is the dataclass dump of MRSDResult; this reads
`mrsd_mg_rounded` (preferred) or `mrsd_mg`.
"""
import argparse
import json
import os
import re
import sys

# A dose labelled as starting/initial within a short window of a number+unit.
# We scan for the label, then look for the nearest "<number> <unit>" on the
# same line / adjacent text.
_START_LABELS = re.compile(
    r"(시작\s*용량|초기\s*용량|개시\s*용량|첫\s*용량|starting\s+dose|initial\s+dose|"
    r"first\s+dose|MRSD|최대\s*권장\s*시작\s*용량)",
    re.IGNORECASE,
)

# number + unit (mg, mcg/µg/ug). Allows comma thousands and decimals.
# Trailing (?![a-zA-Z]) instead of \b so a Korean particle right after the unit
# (e.g. "10 mg으로") still matches, while "mg" inside a latin word does not.
_DOSE = re.compile(
    r"([0-9][0-9,]*\.?[0-9]*)\s*(mg|밀리그램|µg|μg|ug|mcg|microgram|마이크로그램)(?![a-zA-Z])",
    re.IGNORECASE,
)

_UG_UNITS = {"µg", "μg", "ug", "mcg", "microgram", "마이크로그램"}


def _to_mg(value_str, unit):
    val = float(value_str.replace(",", ""))
    if unit.lower() in _UG_UNITS:
        return val / 1000.0
    return val


def mrsd_from_json(path):
    """Read an MRSD (mg) from a starting_dose_calculation MRSDResult dump."""
    if not path or not os.path.isfile(path):
        return None
    try:
        data = json.load(open(path, encoding="utf-8"))
    except (ValueError, OSError):
        return None
    for key in ("mrsd_mg_rounded", "mrsd_mg"):
        if isinstance(data.get(key), (int, float)):
            return float(data[key])
    return None


def extract_starting_doses(text):
    """Return [{"label","dose_mg","raw","line"}] for clearly-labelled starting doses.

    For each starting/initial-dose label we capture the first dose token that
    appears within 60 characters after the label (same sentence in practice).
    """
    found = []
    for m in _START_LABELS.finditer(text):
        window = text[m.end(): m.end() + 60]
        dm = _DOSE.search(window)
        if not dm:
            continue
        dose_mg = _to_mg(dm.group(1), dm.group(2))
        line = text.count("\n", 0, m.start()) + 1
        found.append({
            "label": m.group(0),
            "dose_mg": dose_mg,
            "raw": f"{dm.group(1)} {dm.group(2)}",
            "line": line,
        })
    return found


def check_doses(text, mrsd_mg, tolerance=1e-9):
    """Compare labelled starting doses against MRSD.

    Returns {"status": "ok"|"violation"|"skipped", "mrsd_mg":..., "violations":[...]}.
    'skipped' when mrsd_mg is None (e.g. non-FIH trial — no MRSD to check against).
    """
    if mrsd_mg is None:
        return {"status": "skipped", "mrsd_mg": None, "violations": []}
    violations = []
    for d in extract_starting_doses(text):
        if d["dose_mg"] > mrsd_mg + tolerance:
            violations.append({
                **d,
                "mrsd_mg": mrsd_mg,
                "message": (
                    f"시작 용량 {d['raw']} (≈{d['dose_mg']:g} mg) > MRSD {mrsd_mg:g} mg "
                    f"— line {d['line']} ('{d['label']}'). 자원자 안전 위험."
                ),
            })
    return {
        "status": "violation" if violations else "ok",
        "mrsd_mg": mrsd_mg,
        "violations": violations,
    }


def check_file(path, mrsd_mg=None, mrsd_json=None):
    text = open(path, encoding="utf-8").read()
    if mrsd_mg is None:
        mrsd_mg = mrsd_from_json(mrsd_json)
    return check_doses(text, mrsd_mg)


def main():
    ap = argparse.ArgumentParser(description="FIH dose-safety guardrail (MRSD check).")
    ap.add_argument("path")
    ap.add_argument("--mrsd-mg", type=float, default=None)
    ap.add_argument("--mrsd-json", default=None,
                    help="MRSDResult JSON dump (mrsd_mg_rounded/mrsd_mg)")
    ap.add_argument("--strict", action="store_true", help="exit 1 on violation")
    args = ap.parse_args()

    res = check_file(args.path, mrsd_mg=args.mrsd_mg, mrsd_json=args.mrsd_json)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if args.strict and res["status"] == "violation":
        sys.exit(1)


if __name__ == "__main__":
    main()
