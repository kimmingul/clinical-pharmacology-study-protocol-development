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

# 1) Egress gate (fail-closed). An IB manifest marking the study confidential
# forces a SPONSOR_CONFIDENTIAL floor regardless of --classification, so a FIH/IB
# draft can never be downgraded to PUBLIC for external egress.
IB_MANIFEST="$WORKSPACE/00_input/ib_manifest.json"
if ! "$PY" "$GATE" --provider "$PROVIDER" --host "$HOST" --file "$PROMPT_FILE" \
      ${CLASSIFICATION:+--classification "$CLASSIFICATION"} \
      ${POLICY:+--policy "$POLICY"} \
      $([ -f "$IB_MANIFEST" ] && echo --ib-manifest "$IB_MANIFEST") >/dev/null; then
  echo "⛔ egress gate BLOCKED provider=$PROVIDER (host=$HOST). 기밀/안전핵심 데이터는 외부 전송 불가." >&2
  exit 3
fi

mkdir -p "$(dirname "$OUT")"

# 2) Resolve the PINNED model id (v4.2). resolved_model is read BEFORE dispatch
# and passed to every CLI via --model, so the model we *record* (provenance,
# step 3) is provably the model we *call* — and never a CLI default that could
# silently be an ineligible model (e.g. export-controlled Fable on Anthropic).
PROFILES="$ROOT/.claude/references/llm/model_profiles.json"
MODELID="$("$PY" -c "import json,sys;print(json.load(open(sys.argv[1]))['providers'].get(sys.argv[2],{}).get('resolved_model',sys.argv[2]))" "$PROFILES" "$PROVIDER" 2>/dev/null || echo "$PROVIDER")"

# 3) Dispatch (vendor-neutral) via STDIN / --prompt-file — never command-line
# args for the PROMPT, so a large protocol/ICF draft can't trip ARG_MAX (E2BIG).
# The pinned model id goes via --model (all four CLIs accept it).
case "$PROVIDER" in
  anthropic) claude --model "$MODELID" -p < "$PROMPT_FILE" > "$OUT";;
  openai)    codex exec --model "$MODELID" --sandbox read-only --skip-git-repo-check - < "$PROMPT_FILE" > "$OUT";;
  google)
    # agy (antigravity) replaced the gemini CLI (forced 2026-06-18). It is an
    # IDE-style AUTONOMOUS agent that can run local tools, so it MUST be
    # sandboxed — NEVER --dangerously-skip-permissions. The prompt may carry
    # untrusted fetched content (web/labels), and a prompt-injection there must
    # not gain local code execution. --sandbox keeps headless operation while
    # restricting tool/terminal access (parallels codex's --sandbox read-only).
    # Read stdin for the prompt (no ARG_MAX).
    RAW="$(mktemp)"
    agy --model "$MODELID" --sandbox --print-timeout 290s -p "" < "$PROMPT_FILE" > "$RAW" 2>/dev/null || true
    # Large replies are written to a "brain" artifact whose file:// path agy
    # prints on stdout. SECURITY: only accept an artifact agy ITSELF wrote — a
    # canonical path under its own brain dir — never a path smuggled into the
    # model's stdout by an injection (which could read an arbitrary local .md).
    ART="$(grep -oE 'file://[^ )]+\.md' "$RAW" | head -1 | sed 's#^file://##' || true)"
    SAFE_ART="$("$PY" -c 'import os,sys
p=os.path.realpath(sys.argv[1]) if sys.argv[1] else ""
b=os.path.realpath(os.path.expanduser("~/.gemini/antigravity-cli/brain"))
print(p if p and (p==b or p.startswith(b+os.sep)) else "")' "$ART" 2>/dev/null || echo "")"
    if [ -n "$SAFE_ART" ] && [ -f "$SAFE_ART" ]; then cp "$SAFE_ART" "$OUT"; else cp "$RAW" "$OUT"; fi
    rm -f "$RAW"
    ;;
  xai)       grok --model "$MODELID" --prompt-file "$PROMPT_FILE" > "$OUT";;
  *) echo "unknown provider: $PROVIDER" >&2; exit 2;;
esac

# 4) Provenance (best-effort; never fails the call). Records the pinned model id,
# prompt hash, and egress decision per the v4 reproducibility requirement.
PHASH="$("$PY" -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()[:16])" "$PROMPT_FILE" 2>/dev/null || echo '?')"
"$PY" "$MANIFEST" record --workspace "$WORKSPACE" --phase llm-call \
  --agent "ask_model:$PROVIDER" --model "$MODELID" --output "$OUT" --inputs "$PROMPT_FILE" \
  --note "vendor=$PROVIDER host=$HOST egress=ok class=${CLASSIFICATION:-auto} prompt_sha=$PHASH" >/dev/null 2>&1 || true

echo "ok provider=$PROVIDER -> $OUT"
