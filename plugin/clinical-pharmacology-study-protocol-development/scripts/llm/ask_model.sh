#!/usr/bin/env bash
# ask_model.sh — vendor-neutral single gate for ALL external LLM calls (v4).
#
# Every cross-vendor call MUST go through here (never call the native CLI
# directly). Before dispatch it runs the fail-closed egress gate, so confidential
# IB / safety-critical dosing data can never leak to a non-allowed provider —
# regardless of which vendor is the host.
#
# Usage:
#   ask_model.sh --provider <anthropic|openai|google|xai> --host <provider> \
#       --prompt-file <path> --out <path> [--workspace _workspace] [--policy <path>]
#
# Exit: 0 ok | 3 blocked by egress gate | 2 usage/dispatch error
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"   # repo root
PY="$ROOT/.claude/scripts/.venv/bin/python"; [ -x "$PY" ] || PY="python3"
GATE="$ROOT/.claude/scripts/llm/egress_gate.py"
MANIFEST="$ROOT/.claude/scripts/qa/pipeline_manifest.py"

PROVIDER="" HOST="anthropic" PROMPT_FILE="" OUT="" WORKSPACE="_workspace" POLICY="" CLASSIFICATION=""
while [ $# -gt 0 ]; do
  case "$1" in
    --provider) PROVIDER="$2"; shift 2;;
    --host) HOST="$2"; shift 2;;
    --prompt-file) PROMPT_FILE="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --workspace) WORKSPACE="$2"; shift 2;;
    --policy) POLICY="$2"; shift 2;;
    --classification) CLASSIFICATION="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$PROVIDER" ] && [ -n "$PROMPT_FILE" ] && [ -n "$OUT" ] || { echo "usage: --provider --host --prompt-file --out" >&2; exit 2; }
[ -f "$PROMPT_FILE" ] || { echo "prompt file not found: $PROMPT_FILE" >&2; exit 2; }

# 1) Egress gate (fail-closed). Blocks confidential/safety-critical to non-allowed providers.
if ! "$PY" "$GATE" --provider "$PROVIDER" --host "$HOST" --file "$PROMPT_FILE" ${CLASSIFICATION:+--classification "$CLASSIFICATION"} ${POLICY:+--policy "$POLICY"} >/dev/null; then
  echo "⛔ egress gate BLOCKED provider=$PROVIDER (host=$HOST). 기밀/안전핵심 데이터는 외부 전송 불가." >&2
  exit 3
fi

mkdir -p "$(dirname "$OUT")"
PROMPT="$(cat "$PROMPT_FILE")"

# 2) Dispatch (vendor-neutral). Each CLI in headless/single-shot mode.
case "$PROVIDER" in
  anthropic) claude -p "$PROMPT" > "$OUT";;
  openai)    printf '%s' "$PROMPT" | codex exec --sandbox read-only --skip-git-repo-check - > "$OUT";;
  google)    gemini -p "$PROMPT" > "$OUT";;
  xai)       grok -p "$PROMPT" > "$OUT";;
  *) echo "unknown provider: $PROVIDER" >&2; exit 2;;
esac

# 3) Provenance (best-effort; never fails the call).
"$PY" "$MANIFEST" record --workspace "$WORKSPACE" --phase llm-call \
  --agent "ask_model:$PROVIDER" --model "$PROVIDER" --output "$OUT" --inputs "$PROMPT_FILE" \
  --note "vendor=$PROVIDER host=$HOST egress=ok" >/dev/null 2>&1 || true

echo "ok provider=$PROVIDER -> $OUT"
