#!/usr/bin/env python3
"""Live LLM-CLI health probe — confirm login/key actually works.

The v4 Multi-LLM pipeline routes roles across the installed CLIs (claude, codex,
gemini, grok). A CLI being *installed* (on PATH) does not mean it is *usable* —
the key may be missing, the login expired, or the binary may echo input without
reasoning. This probe sends a tiny arithmetic+nonce challenge to each CLI and
verifies the model actually reasoned over it, so route_select.py only ever
assigns roles to providers proven to work.

The probe asks the model to reply with EXACTLY
``{"probe":"<nonce>","sum":17}`` where 17 = 8 + 9. An echo-only or broken model
fails because it cannot both round-trip the random nonce *and* compute the sum.

Usage
-----
    health_check.py [--workspace _workspace] [--profiles <path>] \
        [--timeout 15] [--only anthropic,openai]

Reads the provider definitions from
``.claude/references/llm/model_profiles.json`` (override with --profiles),
runs a real probe per provider, writes ``<workspace>/llm/health.json``
(schema ``llm_health/v1``), and prints a one-line summary.

Only ``_run`` touches the network/subprocess; every other function is pure and
accepts an injected ``runner`` so the whole module is testable offline.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import time
import uuid
from datetime import datetime, timezone

DEFAULT_PROFILES = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))),
    "references", "llm", "model_profiles.json",
)

EXPECTED_SUM = 17  # 8 + 9 — small enough to be unambiguous, not memorisable

_AUTH_PATTERNS = re.compile(r"auth|login|unauthorized|\bkey\b", re.IGNORECASE)


def _utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def make_probe(nonce):
    """Return (prompt, expected) for a given nonce.

    The model must echo the random nonce *and* compute 8 + 9, so a model that
    merely echoes the prompt (or is broken) cannot satisfy both checks.
    """
    prompt = (
        "Compute 8 + 9. Reply with EXACTLY this JSON and nothing else: "
        '{"probe":"' + nonce + '","sum":<the sum>}'
    )
    expected = {"probe": nonce, "sum": EXPECTED_SUM}
    return prompt, expected


def _find_json_object(text):
    """Return the first parseable top-level JSON object found in text, or None.

    Scans for balanced ``{...}`` spans so surrounding prose (a chatty model)
    does not defeat the check.
    """
    if not text:
        return None
    for start in (m.start() for m in re.finditer(r"\{", text)):
        depth = 0
        for i in range(start, len(text)):
            ch = text[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(text[start:i + 1])
                    except ValueError:
                        break
                    if isinstance(obj, dict):
                        return obj
                    break
    return None


def evaluate_probe(stdout, nonce):
    """Classify probe stdout.

    Returns (status, detail) with status in {"ok", "bad_output"}. "ok" iff a
    JSON object is present with probe == nonce AND sum == 17. ("auth_fail" and
    "timeout"/"missing" are decided by probe_provider, not here.)
    """
    obj = _find_json_object(stdout)
    if obj is None:
        return "bad_output", "no JSON object in output"
    if obj.get("probe") != nonce:
        return "bad_output", f"nonce mismatch (got {obj.get('probe')!r})"
    try:
        got_sum = int(obj.get("sum"))
    except (TypeError, ValueError):
        return "bad_output", f"sum not an integer (got {obj.get('sum')!r})"
    if got_sum != EXPECTED_SUM:
        return "bad_output", f"wrong sum (got {got_sum}, expected {EXPECTED_SUM})"
    return "ok", "probe ok"


def _run(cmd, stdin_text, timeout):
    """Run a CLI command feeding stdin_text; return (rc, stdout, stderr).

    The only impure function in this module. Tests inject a fake runner.
    """
    proc = subprocess.run(
        cmd,
        input=stdin_text,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _cli_version(version_cmd, runner, timeout):
    """Best-effort CLI version string (None on any failure)."""
    if not version_cmd:
        return None
    try:
        rc, out, err = runner(list(version_cmd), "", timeout)
    except Exception:
        return None
    text = (out or err or "").strip()
    return text.splitlines()[0].strip() if text else None


def probe_provider(provider, profile, nonce, timeout=15, runner=_run):
    """Live-probe one provider; return a result dict.

    status is one of: ok | bad_output | auth_fail | timeout | missing.
    "missing" is decided up-front via shutil.which (no run attempted).
    """
    cli = profile.get("cli")
    resolved_model = profile.get("resolved_model")
    result = {
        "provider": provider,
        "cli": cli,
        "resolved_model": resolved_model,
        "cli_version": None,
        "status": "missing",
        "latency_ms": None,
        "probed_at": _utc_now(),
        "detail": "",
    }

    if not cli or shutil.which(cli) is None:
        result["detail"] = f"CLI {cli!r} not found on PATH"
        return result

    result["cli_version"] = _cli_version(
        profile.get("version_cmd"), runner, timeout)

    prompt, _expected = make_probe(nonce)
    cmd = list(profile.get("probe_cmd") or [cli])
    # Convention: a trailing "-" means the CLI reads the prompt from stdin
    # (e.g. `codex exec -`); otherwise pass the prompt as the final CLI
    # argument (e.g. `claude -p <prompt>`, `gemini -p <prompt>`, `grok -p <prompt>`).
    if cmd and cmd[-1] == "-":
        stdin_text = prompt
    else:
        cmd = cmd + [prompt]
        stdin_text = ""

    start = time.monotonic()
    try:
        rc, out, err = runner(cmd, stdin_text, timeout)
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["latency_ms"] = int((time.monotonic() - start) * 1000)
        result["detail"] = f"probe timed out after {timeout}s"
        return result
    except Exception as exc:  # pragma: no cover - defensive
        result["status"] = "bad_output"
        result["latency_ms"] = int((time.monotonic() - start) * 1000)
        result["detail"] = f"probe raised {type(exc).__name__}: {exc}"
        return result

    result["latency_ms"] = int((time.monotonic() - start) * 1000)

    # Evaluate stdout FIRST: a valid nonce+arithmetic response means the model
    # actually answered, so treat it as ok even if the CLI emitted noisy stderr
    # or a non-zero rc (some CLIs print transient worker warnings yet still
    # return a correct answer on stdout).
    status, detail = evaluate_probe(out, nonce)
    if status == "ok":
        result["status"] = "ok"
        result["detail"] = detail
        return result

    # Not a valid answer -> classify the failure.
    if _AUTH_PATTERNS.search(err or "") or (rc != 0 and _AUTH_PATTERNS.search(out or "")):
        result["status"] = "auth_fail"
        result["detail"] = f"auth error (rc={rc}): {(err or out or '').strip()[:120]}"
        return result

    if rc != 0:
        detail = f"{detail} (rc={rc})"
    result["status"] = status
    result["detail"] = detail
    return result


def check_all(profiles, providers=None, runner=_run, timeout=15):
    """Probe every provider (or the subset in ``providers``)."""
    defined = profiles.get("providers", {})
    keys = providers if providers else list(defined.keys())
    results = {}
    for key in keys:
        profile = defined.get(key)
        if profile is None:
            results[key] = {
                "provider": key,
                "cli": None,
                "resolved_model": None,
                "cli_version": None,
                "status": "missing",
                "latency_ms": None,
                "probed_at": _utc_now(),
                "detail": "provider not defined in model_profiles.json",
            }
            continue
        nonce = uuid.uuid4().hex[:12]
        results[key] = probe_provider(
            key, profile, nonce, timeout=timeout, runner=runner)
    return {
        "schema": "llm_health/v1",
        "probed_at": _utc_now(),
        "providers": results,
    }


def write_health(health, workspace="_workspace"):
    out_dir = os.path.join(workspace, "llm")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "health.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(health, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path


def _load_profiles(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(
        description="Live-probe each LLM CLI to confirm login/key works.")
    ap.add_argument("--workspace", default="_workspace")
    ap.add_argument("--profiles", default=DEFAULT_PROFILES)
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--only", default=None,
                    help="comma-separated provider subset, e.g. anthropic,openai")
    args = ap.parse_args()

    profiles = _load_profiles(args.profiles)
    only = [p.strip() for p in args.only.split(",") if p.strip()] if args.only else None

    health = check_all(profiles, providers=only, timeout=args.timeout)
    path = write_health(health, args.workspace)

    summary = ", ".join(
        f"{k}:{v['status']}" for k, v in health["providers"].items())
    ok = sum(1 for v in health["providers"].values() if v["status"] == "ok")
    print(f"health: {ok}/{len(health['providers'])} ok [{summary}] -> {path}")


if __name__ == "__main__":
    main()
