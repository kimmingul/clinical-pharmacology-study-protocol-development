#!/usr/bin/env python3
"""Deterministic Multi-LLM routing — the host PROPOSES, this script DECIDES.

Given a health report (which CLIs actually work) and the capability scores in
model_profiles.json, this computes a reproducible role->provider assignment so
the routing decision is auditable and not left to a non-deterministic LLM call.

Rules
-----
- authoring goes to the host (combination_profiles.host_default_role); this
  minimises data egress and context fragmentation.
- every other role goes to the highest-capability *available* provider for that
  role (ties broken alphabetically by provider key).
- judge_synth must differ from the authoring provider
  (judge_must_differ_from_author); if the top judge == author, pick the next,
  else null (defer to deterministic/human synthesis).
- citation_integrity is deterministic-first (citation_verify.py); the assigned
  LLM is only an assist.
- multi_llm is true iff >= 2 providers are available; with only the host, every
  role collapses to the host (single-LLM = Multi-Persona).

Usage
-----
    route_select.py --host anthropic [--workspace _workspace] \
        [--health <path>] [--profiles <path>] [--combos <path>] \
        [--today 2026-06-15]

Reads <workspace>/llm/health.json plus the two profile files, writes
<workspace>/llm/routing_plan.json (schema llm_routing/v1), prints a summary.
"""
import argparse
import json
import os
from datetime import date

_REF = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))),
    "references", "llm",
)
DEFAULT_PROFILES = os.path.join(_REF, "model_profiles.json")
DEFAULT_COMBOS = os.path.join(_REF, "combination_profiles.json")


def available_providers(health):
    """Provider keys whose probe status is 'ok', sorted for determinism."""
    providers = health.get("providers", {})
    return sorted(k for k, v in providers.items() if v.get("status") == "ok")


def rank_for_role(role, candidates, profiles):
    """Rank candidates for a role: capability score desc, then key asc."""
    defined = profiles.get("providers", {})

    def score(key):
        return defined.get(key, {}).get("capability_scores", {}).get(role, 0)

    return sorted(candidates, key=lambda k: (-score(k), k))


def _parse_date(s):
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def _is_stale(as_of, today, warn_days):
    d_asof = _parse_date(as_of)
    d_today = _parse_date(today)
    if d_asof is None or d_today is None or not warn_days:
        return False
    return (d_today - d_asof).days > warn_days


def select_routing(health, profiles, combos, host, today=None):
    """Compute the routing plan dict (schema llm_routing/v1)."""
    available = available_providers(health)
    # The host is always the orchestrator even if its own probe did not pass.
    host_ok = host in available
    if host not in available:
        available = sorted(set(available) | {host})

    roles = combos.get("roles", [])
    # multi_llm requires >=2 genuinely-available (status=ok) providers; the
    # host counts only if its own probe passed.
    truly_available = available_providers(health)
    multi_llm = len(truly_available) >= 2

    notes = []
    if not host_ok:
        notes.append(
            f"host {host!r} probe not ok — treated as orchestrator with a "
            f"warning; verify the host CLI before relying on authoring")

    assignment = {}
    alternatives = {}

    if not multi_llm:
        # Single-LLM: every role collapses to the host (Multi-Persona only).
        for role in roles:
            assignment[role] = host
            alternatives[role] = []
        notes.append(
            "single-LLM mode: only the host is available; all roles run on the "
            "host as Multi-Persona (no external critic)")
    else:
        author = host  # host_default_role = authoring
        for role in roles:
            if role == "authoring":
                assignment[role] = host
                alternatives[role] = rank_for_role(
                    "authoring", available, profiles)[1:3]
                continue

            ranked = rank_for_role(role, available, profiles)

            if role == "judge_synth" and combos.get("judge_must_differ_from_author"):
                pick = next((p for p in ranked if p != author), None)
                assignment[role] = pick
                if pick is None:
                    notes.append(
                        "judge_synth: no provider differs from the author; "
                        "defer to deterministic/human synthesis")
                elif ranked and ranked[0] == author:
                    notes.append(
                        f"judge_synth: top candidate is the author ({author}); "
                        f"picked next-best {pick} to keep judge independent")
                alternatives[role] = [p for p in ranked if p != author][1:3]
            else:
                assignment[role] = ranked[0] if ranked else None
                alternatives[role] = ranked[1:3]

            if role == "citation_integrity":
                notes.append(
                    "citation_integrity: deterministic-first (citation_verify.py); "
                    f"LLM {assignment[role]} assists only")

    as_of = profiles.get("as_of")
    warn_days = profiles.get("staleness_warn_days")
    stale = _is_stale(as_of, today, warn_days)
    if stale:
        notes.append(
            f"model_profiles as_of {as_of} is older than {warn_days} days "
            f"(today {today}); host should re-check with current knowledge")

    return {
        "schema": "llm_routing/v1",
        "host": host,
        "available": truly_available,
        "multi_llm": multi_llm,
        "assignment": assignment,
        "alternatives": alternatives,
        "as_of": as_of,
        "stale_warning": stale,
        "notes": notes,
    }


def write_routing(plan, workspace):
    out_dir = os.path.join(workspace, "llm")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "routing_plan.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(
        description="Deterministically compute the Multi-LLM routing plan.")
    ap.add_argument("--host", required=True,
                    help="provider running the plugin (anthropic|openai|google|xai)")
    ap.add_argument("--workspace", default="_workspace")
    ap.add_argument("--health", default=None,
                    help="path to health.json (default <workspace>/llm/health.json)")
    ap.add_argument("--profiles", default=DEFAULT_PROFILES)
    ap.add_argument("--combos", default=DEFAULT_COMBOS)
    ap.add_argument("--today", default=date.today().isoformat(),
                    help="YYYY-MM-DD used for staleness check")
    args = ap.parse_args()

    health_path = args.health or os.path.join(
        args.workspace, "llm", "health.json")
    health = _load(health_path)
    profiles = _load(args.profiles)
    combos = _load(args.combos)

    plan = select_routing(health, profiles, combos, args.host, today=args.today)
    path = write_routing(plan, args.workspace)

    mode = "multi-LLM" if plan["multi_llm"] else "single-LLM"
    assigns = ", ".join(f"{r}={p}" for r, p in plan["assignment"].items())
    print(f"routing ({mode}, host={plan['host']}): {assigns} -> {path}")
    if plan["stale_warning"]:
        print("  WARNING: model_profiles is stale; re-check capability scores")


if __name__ == "__main__":
    main()
