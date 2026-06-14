#!/usr/bin/env python3
"""PostToolUse advisory hook — warns (never blocks) after a protocol/ICF draft
is written.

Fires on Write|Edit. If the written file is the protocol or ICF draft, it runs
the shared deterministic linter (scripts/qa/doc_lint.py) and surfaces any
findings to the model via PostToolUse `additionalContext` so it can self-correct.
This is ADVISORY: it always exits 0 and never blocks the tool call. Any internal
error is swallowed (exit 0) so the hook can never disrupt a session.

The linter is located by a path relative to this file, so the hook works
identically from the development tree and the deployed plugin without any path
substitution (both keep the layout hooks/ + scripts/qa/).
"""
import json
import os
import sys

# Locate the shared lint engine: <root>/scripts/qa/doc_lint.py relative to
# this hook at <root>/hooks/draft_advisory_hook.py — same layout in the dev
# tree and the deployed plugin, so no path substitution is needed.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "scripts", "qa"))

TARGET_BASENAMES = ("03_protocol_draft.md", "04_icf_draft.md")


def _emit(context):
    """Emit non-blocking advisory context to the model and exit 0."""
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    }))
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
    if base not in TARGET_BASENAMES:
        sys.exit(0)

    if not os.path.isfile(file_path):
        sys.exit(0)

    try:
        import doc_lint  # from scripts/qa on sys.path
        doc_type, errors, warnings = doc_lint.lint_file(file_path)
    except Exception:
        sys.exit(0)  # never disrupt the session

    if not errors and not warnings:
        sys.exit(0)  # clean draft -> stay silent

    lines = [f"⚠ 자동 품질 검증 ({doc_type} 초안: {base}) — advisory(비차단):"]
    for e in errors:
        lines.append(f"  • [중요] {e}")
    for w in warnings:
        lines.append(f"  • {w}")
    lines.append("위 항목을 검토·수정한 뒤 진행하세요. (이 경고는 작업을 막지 않습니다.)")
    _emit("\n".join(lines))


if __name__ == "__main__":
    main()
