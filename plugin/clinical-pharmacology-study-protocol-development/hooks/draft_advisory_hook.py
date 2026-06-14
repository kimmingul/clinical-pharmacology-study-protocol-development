#!/usr/bin/env python3
"""PostToolUse tiered guardrail — fires after a protocol/ICF draft is written.

v3 tiering (zero-trust "verify-then-allow"):
  * T0 (BLOCKING): positively-wrong, patient-safety / regulatory invariants that
    are wrong *when present* — a document-retention period stated below 15년, a
    BE/DDI equivalence boundary that is wrong, and (FIH) a stated starting dose
    above the computed MRSD. These return a PostToolUse `decision: block`, so the
    model must fix them before proceeding.
  * T1 (ADVISORY): everything else, including ICH Appendix B section coverage.
    Section-completeness is intentionally NOT blocking here because a protocol is
    written in multiple chunks and an in-progress draft legitimately lacks
    sections; full coverage is enforced at `/finalize` (doc_lint --strict).

This hook never raises: any internal error is swallowed (exit 0) so it can never
disrupt a session. The shared engines (scripts/qa/doc_lint.py,
scripts/qa/dose_safety_guard.py) are located by a path relative to this file, so
the hook works identically in the dev tree and the deployed plugin.
"""
import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "scripts", "qa"))

TARGET_BASENAMES = ("03_protocol_draft.md", "04_icf_draft.md")

# Substrings that mark a lint ERROR as a T0 positively-wrong invariant (blocking).
# "Appendix B sections missing" is deliberately excluded (partial-draft tolerant).
_BLOCKING_ERROR_HINTS = ("retention", "보존", "보유", "15년", "90% CI", "80.00", "125.00")


def _emit_block(reason):
    print(json.dumps({
        "decision": "block",
        "reason": reason,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": reason,
        },
    }, ensure_ascii=False))
    sys.exit(0)


def _emit_advisory(context):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    }, ensure_ascii=False))
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)

    file_path = (data.get("tool_input") or {}).get("file_path", "")
    base = os.path.basename(file_path)
    if base not in TARGET_BASENAMES or not os.path.isfile(file_path):
        sys.exit(0)

    blocking, advisory = [], []
    doc_type = "protocol" if base.startswith("03") else "icf"

    # --- doc_lint (deterministic) ---
    try:
        import doc_lint
        doc_type, errors, warnings = doc_lint.lint_file(file_path)
        for e in errors:
            if any(h in e for h in _BLOCKING_ERROR_HINTS):
                blocking.append(e)
            else:
                advisory.append(f"[중요] {e}")
        advisory.extend(warnings)
    except Exception:
        pass  # never disrupt the session

    # --- dose-safety guard (FIH; T0-blocking) ---
    if base.startswith("03"):
        try:
            import dose_safety_guard
            workspace = os.path.dirname(file_path)
            mrsd_json = os.path.join(workspace, "00_input", "mrsd.json")
            res = dose_safety_guard.check_file(file_path, mrsd_json=mrsd_json)
            for v in res.get("violations", []):
                blocking.append(v["message"])
        except Exception:
            pass

    if blocking:
        lines = [f"⛔ T0 가드레일 차단 ({doc_type} 초안: {base}) — 아래는 자원자 안전·규제 핵심 불변식 위반입니다. 반드시 수정 후 진행하세요:"]
        lines += [f"  • {b}" for b in blocking]
        if advisory:
            lines.append("(추가 권고 — 비차단:)")
            lines += [f"  • {a}" for a in advisory]
        _emit_block("\n".join(lines))

    if advisory:
        lines = [f"⚠ 자동 품질 검증 ({doc_type} 초안: {base}) — advisory(비차단):"]
        lines += [f"  • {a}" for a in advisory]
        lines.append("위 항목을 검토·수정한 뒤 진행하세요. (이 경고는 작업을 막지 않습니다.)")
        _emit_advisory("\n".join(lines))

    sys.exit(0)  # clean draft -> silent


if __name__ == "__main__":
    main()
