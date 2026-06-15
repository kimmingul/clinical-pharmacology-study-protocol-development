#!/usr/bin/env bash
# run_review_panel.sh — drive the Phase 9 cross-vendor critic panel (v4).
#
# Reads the panel plan produced by review_panel.py and invokes each external
# critic through ask_model.sh (which enforces the fail-closed egress gate). Host
# roles and unavailable providers are skipped (the host qa-reviewer covers them
# inline). Then synthesizes deterministic + vendor findings (no majority vote).
#
# Usage:
#   run_review_panel.sh --workspace _workspace --host anthropic \
#       [--classification REGULATORY_PUBLIC] [--deterministic <json>]
#
# Prereqs: _workspace/llm/review_panel_plan.json (review_panel.py plan ...).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PY="$ROOT/.claude/scripts/.venv/bin/python"; [ -x "$PY" ] || PY="python3"
LLM="$ROOT/.claude/scripts/llm"

WORKSPACE="_workspace" HOST="anthropic" CLASSIFICATION="" DETERMINISTIC=""
while [ $# -gt 0 ]; do
  case "$1" in
    --workspace) WORKSPACE="$2"; shift 2;;
    --host) HOST="$2"; shift 2;;
    --classification) CLASSIFICATION="$2"; shift 2;;
    --deterministic) DETERMINISTIC="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

PLAN="$WORKSPACE/llm/review_panel_plan.json"
[ -f "$PLAN" ] || { echo "panel plan not found: $PLAN (run review_panel.py plan first)" >&2; exit 2; }

# Collect external entries FIRST (provider<TAB>prompt_file<TAB>out_file). We must
# not pipe directly into `while read`, because the CLIs invoked inside the loop
# (gemini/grok/claude) would consume the loop's stdin and drop remaining entries.
ENTRIES="$("$PY" - "$PLAN" <<'PYEOF'
import json, sys
plan = json.load(open(sys.argv[1], encoding="utf-8"))
for e in plan.get("entries", []):
    if e.get("mode") == "external":
        print(f"{e['provider']}\t{e['prompt_file']}\t{e['out_file']}")
PYEOF
)"

while IFS=$'\t' read -r PROVIDER PROMPT OUT; do
  [ -n "$PROVIDER" ] || continue
  echo "→ critic: $PROVIDER"
  # </dev/null isolates the loop's stdin from the dispatched CLI.
  if "$LLM/ask_model.sh" --provider "$PROVIDER" --host "$HOST" \
        --prompt-file "$PROMPT" --out "$OUT" --workspace "$WORKSPACE" \
        ${CLASSIFICATION:+--classification "$CLASSIFICATION"} </dev/null; then
    :
  else
    rc=$?
    # egress-blocked (3) or dispatch error: leave a SKIPPED marker, keep going.
    printf '{"role":"?","verdict":"skipped","findings":[],"_skipped":"ask_model rc=%s (egress block or CLI error)"}' "$rc" > "$OUT"
    echo "  ⚠ skipped $PROVIDER (rc=$rc) — host qa-reviewer가 해당 역할을 대체"
  fi
done <<< "$ENTRIES"

# Synthesize deterministic + vendor critic findings (deterministic-first).
"$PY" "$LLM/review_panel.py" synthesize --workspace "$WORKSPACE" \
  ${DETERMINISTIC:+--deterministic "$DETERMINISTIC"}
echo "panel done -> $WORKSPACE/review/review_synthesis.json"
