#!/usr/bin/env python3
"""Phase 9 cross-vendor critic panel — build prompts and synthesize findings.

Two pure stages, both stdlib-only:

build_panel
    Given a deterministic routing plan (from route_select.py) and the role
    templates in review_roles.json, decide for each panel role whether the
    critic runs on the host (inline qa-reviewer), on an external verified
    provider (write a prompt file + reserve an out_file), or is skipped
    (provider not available). The host is never sent its own prompt file — it
    reviews inline.

synthesize
    Aggregate findings WITHOUT a majority vote. Deterministic guardrail
    findings (doc_lint / citation_verify / dose_safety) are AUTHORITATIVE and
    listed first; each external critic's parsed findings are appended and
    tagged by ``<provider>:<role>``. Unparseable critic output never raises —
    it degrades to a Minor finding. Conflicts (same section, differing
    severity across sources) are surfaced for the host to adjudicate.

Usage
-----
    review_panel.py plan --routing <p> --roles <p> --draft <p> --host <prov> \
        [--workspace _workspace] [--classification REGULATORY_PUBLIC]
    review_panel.py synthesize [--workspace _workspace] \
        [--vendor f ...] [--deterministic <json file>]
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

_REF = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))),
    "references", "llm",
)
DEFAULT_ROLES = os.path.join(_REF, "review_roles.json")

_SEVERITIES = ("Critical", "Major", "Minor")


def _now_iso(now=None):
    """Resolve an ISO timestamp; tests inject ``now`` to stay deterministic.

    datetime.now() with no tz is blocked in this environment, so the live path
    always uses timezone-aware UTC.
    """
    if now is not None:
        return now
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _prompt_text(roles_cfg, role, draft_text):
    """Compose the adversarial prompt: role instruction + output contract +
    the full protocol draft."""
    instruction = roles_cfg["roles"][role]["instruction"]
    contract = roles_cfg["output_contract"]
    return (f"{instruction}\n\n{contract}\n\n"
            f"=== PROTOCOL DRAFT ===\n{draft_text}")


def build_panel(routing_plan, roles_cfg, draft_path, host,
                workspace="_workspace", classification=None, now=None):
    """Build the per-role critic panel plan and write external prompt files.

    For each panel role:
      - provider None or == host -> mode "host" (qa-reviewer inline, no file).
      - provider in routing available -> mode "external"; write prompt file,
        reserve out_file for the vendor's JSON response.
      - otherwise -> mode "skipped" (provider_unavailable).
    """
    assignment = routing_plan.get("assignment", {})
    available = routing_plan.get("available", [])

    with open(draft_path, encoding="utf-8") as f:
        draft_text = f.read()

    panel_dir = os.path.join(workspace, "review", "panel")
    review_dir = os.path.join(workspace, "review")

    entries = []
    for role in roles_cfg.get("panel_roles", []):
        provider = assignment.get(role)
        if provider is None or provider == host:
            entries.append({"role": role, "provider": provider, "mode": "host"})
            continue
        if provider in available:
            os.makedirs(panel_dir, exist_ok=True)
            prompt_file = os.path.join(
                panel_dir, f"prompt_{provider}_{role}.txt")
            out_file = os.path.join(
                review_dir, f"vendor_{provider}_{role}.json")
            with open(prompt_file, "w", encoding="utf-8") as f:
                f.write(_prompt_text(roles_cfg, role, draft_text))
            entries.append({
                "role": role,
                "provider": provider,
                "mode": "external",
                "prompt_file": prompt_file,
                "out_file": out_file,
            })
            continue
        entries.append({
            "role": role,
            "provider": provider,
            "mode": "skipped",
            "reason": "provider_unavailable",
        })

    return {
        "schema": "review_panel/v1",
        "host": host,
        "draft": draft_path,
        "classification": classification,
        "entries": entries,
        "generated_at": _now_iso(now),
    }


def write_panel(plan, workspace="_workspace"):
    out_dir = os.path.join(workspace, "llm")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "review_panel_plan.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path


def _source_from_path(path):
    """Derive ``<provider>:<role>`` from a vendor_<provider>_<role>.json name.

    Falls back to the bare filename if the convention does not match (e.g. a
    role key itself contains underscores is handled by splitting on the
    leading ``vendor_`` prefix and the trailing ``.json`` suffix, then on the
    FIRST underscore: provider then role)."""
    name = os.path.basename(path)
    stem = name
    if stem.startswith("vendor_"):
        stem = stem[len("vendor_"):]
    if stem.endswith(".json"):
        stem = stem[:-len(".json")]
    if "_" in stem:
        provider, role = stem.split("_", 1)
        return f"{provider}:{role}"
    return name


def _classify_finding(finding):
    """Map a finding's severity onto one of Critical/Major/Minor (default
    Minor for anything unexpected)."""
    sev = finding.get("severity")
    return sev if sev in _SEVERITIES else "Minor"


def _extract_json(text):
    """Parse JSON, tolerating prose around a single JSON object. Critics often
    prepend an explanatory sentence before the JSON they were asked to emit."""
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        pass
    start = text.find("{")
    while start != -1:
        depth, in_str, esc = 0, False, False
        for i in range(start, len(text)):
            c = text[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except ValueError:
                        break
        start = text.find("{", start + 1)
    raise ValueError("no JSON object found in critic output")


def synthesize(deterministic_findings, vendor_paths, workspace="_workspace"):
    """Aggregate deterministic + vendor findings deterministic-first.

    Never raises on malformed vendor output: it is recorded as a Minor finding
    so the host still sees that a critic ran but produced unusable output.
    """
    buckets = {"Critical": [], "Major": [], "Minor": []}
    by_source = {}
    sources_used = []
    sources_skipped = []
    # section -> list of (source, severity) for conflict detection.
    section_index = {}

    def _record(finding, source):
        finding = dict(finding)
        finding["source"] = source
        sev = _classify_finding(finding)
        buckets[sev].append(finding)
        by_source[source] = by_source.get(source, 0) + 1
        section = finding.get("section")
        if section:
            section_index.setdefault(section, []).append((source, sev))

    # Deterministic guardrail findings are authoritative -> listed FIRST.
    for finding in deterministic_findings or []:
        _record(finding, finding.get("source", "deterministic"))

    for path in vendor_paths:
        if not os.path.exists(path):
            sources_skipped.append(path)
            continue
        source = _source_from_path(path)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        try:
            data = _extract_json(text)
            findings = data.get("findings", [])
            if not isinstance(findings, list):
                raise ValueError("findings is not a list")
        except (ValueError, AttributeError):
            _record(
                {"issue": "critic output unparseable", "severity": "Minor"},
                source)
            sources_used.append(source)
            continue
        for finding in findings:
            if isinstance(finding, dict):
                _record(finding, source)
        sources_used.append(source)

    conflicts = []
    for section, entries in section_index.items():
        severities = {sev for _, sev in entries}
        sources = sorted({src for src, _ in entries})
        if len(severities) > 1 and len(sources) > 1:
            conflicts.append({"section": section, "sources": sources})

    return {
        "schema": "review_synthesis/v1",
        "critical": buckets["Critical"],
        "major": buckets["Major"],
        "minor": buckets["Minor"],
        "by_source": by_source,
        "conflicts": conflicts,
        "sources_used": sources_used,
        "sources_skipped": sources_skipped,
    }


def write_synthesis(result, workspace="_workspace"):
    out_dir = os.path.join(workspace, "review")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "review_synthesis.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path


def _qa_module(name):
    """Import a deterministic QA module from ../qa (sibling of this llm/ dir)."""
    qa = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "qa")
    if qa not in sys.path:
        sys.path.insert(0, qa)
    return __import__(name)


def collect_deterministic(draft_path, goal_spec_path=None, mrsd_json=None):
    """Run the deterministic guardrails on a draft and return their findings as
    authoritative entries (source=doc_lint|citation_verify|dose_safety). These
    feed synthesize() FIRST so the panel never overrides machine-checkable facts.
    Offline only (no network, no writes)."""
    findings = []
    doc_lint = _qa_module("doc_lint")
    gs = doc_lint.load_goal_spec(goal_spec_path) if goal_spec_path else None
    res = doc_lint.score_file(draft_path, goal_spec=gs)
    for sev, key in (("Critical", "critical"), ("Major", "major"), ("Minor", "minor")):
        for msg in res.get(key, []):
            findings.append({"severity": sev, "source": "doc_lint", "issue": msg})

    cv = _qa_module("citation_verify")
    with open(draft_path, encoding="utf-8") as f:
        text = f.read()
    for item in cv.classify_offline(cv.extract_citations(text)):
        if not item.get("format_ok", True):
            findings.append({
                "severity": "Major", "source": "citation_verify",
                "issue": f"인용 형식 오류: {item.get('type')} {item.get('value')} "
                         f"({item.get('reason')})"})

    if mrsd_json and os.path.exists(mrsd_json):
        ds = _qa_module("dose_safety_guard")
        r = ds.check_file(draft_path, mrsd_json=mrsd_json)
        for v in r.get("violations", []):
            findings.append({"severity": "Critical", "source": "dose_safety",
                             "issue": v.get("message", "dose > MRSD")})
    return findings


def fixplan_markdown(synthesis):
    """Render the Critical/Major findings of a synthesis into a fix plan the
    actor (protocol-writer) addresses on the next convergence-loop turn."""
    lines = ["# QA 수정 계획 (자동 생성 — review_synthesis.json 기반)", ""]
    for sev, key in (("Critical", "critical"), ("Major", "major")):
        items = synthesis.get(key, [])
        lines.append(f"## {sev} ({len(items)})")
        if not items:
            lines.append("- (없음)")
        for i, f in enumerate(items, 1):
            src = f.get("source", "?")
            sec = f.get("section", "-")
            issue = str(f.get("issue", "")).strip()
            rec = str(f.get("recommendation", "")).strip()
            lines.append(f"{i}. [{src}] §{sec}: {issue}"
                         + (f" → 권고: {rec}" if rec else ""))
        lines.append("")
    lines.append("> protocol-writer는 위 Critical→Major 순으로 본문을 수정한다. "
                 "synopsis·design_decisions의 설계 결정은 불변. 결정적 도구(doc_lint/"
                 "citation_verify/dose_safety) 항목이 최우선.")
    return "\n".join(lines) + "\n"


def write_fixplan(md, workspace="_workspace"):
    out_dir = os.path.join(workspace, "review")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "qa_fix_plan.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    return path


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _discover_vendor_files(workspace):
    """Find <workspace>/review/vendor_*.json, sorted for determinism."""
    review_dir = os.path.join(workspace, "review")
    if not os.path.isdir(review_dir):
        return []
    return sorted(
        os.path.join(review_dir, n)
        for n in os.listdir(review_dir)
        if n.startswith("vendor_") and n.endswith(".json"))


def _cmd_plan(args):
    routing_plan = _load(args.routing)
    roles_cfg = _load(args.roles)
    plan = build_panel(
        routing_plan, roles_cfg, args.draft, args.host,
        workspace=args.workspace, classification=args.classification)
    path = write_panel(plan, args.workspace)

    modes = {"external": 0, "host": 0, "skipped": 0}
    for entry in plan["entries"]:
        modes[entry["mode"]] = modes.get(entry["mode"], 0) + 1
    print(f"panel (host={plan['host']}): {modes['external']} external, "
          f"{modes['host']} host, {modes['skipped']} skipped -> {path}")


def _cmd_synthesize(args):
    deterministic = _load(args.deterministic) if args.deterministic else []
    vendor_paths = args.vendor or _discover_vendor_files(args.workspace)
    result = synthesize(deterministic, vendor_paths, workspace=args.workspace)
    path = write_synthesis(result, args.workspace)
    print(f"synthesis: {len(result['critical'])} Critical, "
          f"{len(result['major'])} Major, {len(result['minor'])} Minor; "
          f"{len(result['sources_used'])} sources, "
          f"{len(result['conflicts'])} conflicts -> {path}")


def _cmd_deterministic(args):
    findings = collect_deterministic(
        args.draft, goal_spec_path=args.goal_spec, mrsd_json=args.mrsd_json)
    out_dir = os.path.join(args.workspace, "review")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "deterministic_findings.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(findings, f, ensure_ascii=False, indent=2)
        f.write("\n")
    n = {"Critical": 0, "Major": 0, "Minor": 0}
    for x in findings:
        n[x["severity"]] = n.get(x["severity"], 0) + 1
    print(f"deterministic: {n['Critical']} Critical, {n['Major']} Major, "
          f"{n['Minor']} Minor -> {path}")


def _cmd_fixplan(args):
    synthesis = _load(os.path.join(args.workspace, "review", "review_synthesis.json"))
    md = fixplan_markdown(synthesis)
    path = write_fixplan(md, args.workspace)
    print(f"fixplan: {len(synthesis.get('critical', []))} Critical + "
          f"{len(synthesis.get('major', []))} Major -> {path}")


def main():
    ap = argparse.ArgumentParser(
        description="Phase 9 cross-vendor critic panel build + synthesis.")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("plan", help="build the critic panel + prompt files")
    p.add_argument("--routing", required=True, help="path to routing_plan.json")
    p.add_argument("--roles", default=DEFAULT_ROLES)
    p.add_argument("--draft", required=True, help="path to the protocol draft")
    p.add_argument("--host", required=True,
                   help="orchestrator provider (anthropic|openai|google|xai)")
    p.add_argument("--workspace", default="_workspace")
    p.add_argument("--classification", default=None,
                   help="caller-declared egress floor (e.g. REGULATORY_PUBLIC)")
    p.set_defaults(func=_cmd_plan)

    s = sub.add_parser("synthesize", help="aggregate deterministic + vendor")
    s.add_argument("--workspace", default="_workspace")
    s.add_argument("--vendor", action="append", default=[],
                   help="explicit vendor JSON file(s); repeatable")
    s.add_argument("--deterministic", default=None,
                   help="JSON file of authoritative guardrail findings")
    s.set_defaults(func=_cmd_synthesize)

    d = sub.add_parser("deterministic",
                       help="run doc_lint/citation/dose guards -> findings json")
    d.add_argument("--draft", required=True)
    d.add_argument("--workspace", default="_workspace")
    d.add_argument("--goal-spec", default=None)
    d.add_argument("--mrsd-json", default=None)
    d.set_defaults(func=_cmd_deterministic)

    fp = sub.add_parser("fixplan",
                        help="render review_synthesis.json -> qa_fix_plan.md")
    fp.add_argument("--workspace", default="_workspace")
    fp.set_defaults(func=_cmd_fixplan)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
