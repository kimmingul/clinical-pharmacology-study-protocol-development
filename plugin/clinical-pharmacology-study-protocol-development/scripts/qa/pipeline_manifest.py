#!/usr/bin/env python3
"""Pipeline reproducibility manifest — an append-only provenance trail.

Gives the generated regulatory documents a traceable lineage: for each pipeline
phase it records the agent, model, input files, the output file and its
SHA-256, a UTC timestamp, and the harness version. The main agent calls this at
the end of each phase so that, given a `_workspace/`, anyone can answer "which
model/version produced which artifact from which inputs, and has it changed?".

Usage
-----
    pipeline_manifest.py init  [--workspace _workspace] [--trial "..."]
    pipeline_manifest.py record --phase 8 --agent protocol-writer --model opus \
        --output _workspace/03_protocol_draft.md \
        [--inputs _workspace/02_synopsis.md _workspace/01_research_report.md] \
        [--note "Critical 1건 수정 반영"]
    pipeline_manifest.py show   [--workspace _workspace]

The manifest itself is JSON at <workspace>/pipeline_manifest.json and validates
against .claude/schema/pipeline_manifest.schema.json.
"""
import argparse
import hashlib
import json
import os
from datetime import datetime, timezone

MANIFEST_NAME = "pipeline_manifest.json"


def _utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sha256(path):
    if not path or not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _harness_version(start=None):
    """Best-effort lookup of the harness version from a nearby manifest."""
    here = os.path.abspath(start or os.getcwd())
    for _ in range(6):
        for rel in (
            os.path.join(".claude-plugin", "plugin.json"),
            os.path.join(".claude-plugin", "marketplace.json"),
        ):
            cand = os.path.join(here, rel)
            if os.path.isfile(cand):
                try:
                    data = json.load(open(cand, encoding="utf-8"))
                    if "version" in data:
                        return str(data["version"])
                    md = data.get("metadata", {})
                    if "version" in md:
                        return str(md["version"])
                except (ValueError, OSError):
                    pass
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return "unknown"


def _path(workspace):
    return os.path.join(workspace, MANIFEST_NAME)


def _load(workspace):
    p = _path(workspace)
    if os.path.isfile(p):
        return json.load(open(p, encoding="utf-8"))
    return None


def _save(workspace, manifest):
    os.makedirs(workspace, exist_ok=True)
    with open(_path(workspace), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")


def init(workspace, trial=None):
    manifest = {
        "schema": "pipeline_manifest/v1",
        "harness_version": _harness_version(workspace),
        "trial": trial or "",
        "created_utc": _utc_now(),
        "phases": [],
    }
    _save(workspace, manifest)
    return manifest


def record(workspace, *, phase, agent, model, output=None, inputs=None, note=""):
    manifest = _load(workspace) or init(workspace)
    entry = {
        "phase": phase,
        "agent": agent,
        "model": model,
        "timestamp_utc": _utc_now(),
        "inputs": [
            {"path": p, "sha256": _sha256(p)} for p in (inputs or [])
        ],
        "output": (
            {"path": output, "sha256": _sha256(output)} if output else None
        ),
        "note": note,
    }
    manifest["phases"].append(entry)
    _save(workspace, manifest)
    return entry


def main():
    ap = argparse.ArgumentParser(description="Pipeline reproducibility manifest.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--workspace", default="_workspace")
    p_init.add_argument("--trial", default=None)

    p_rec = sub.add_parser("record")
    p_rec.add_argument("--workspace", default="_workspace")
    p_rec.add_argument("--phase", required=True)
    p_rec.add_argument("--agent", required=True)
    p_rec.add_argument("--model", required=True)
    p_rec.add_argument("--output", default=None)
    p_rec.add_argument("--inputs", nargs="*", default=[])
    p_rec.add_argument("--note", default="")

    p_show = sub.add_parser("show")
    p_show.add_argument("--workspace", default="_workspace")

    args = ap.parse_args()

    if args.cmd == "init":
        m = init(args.workspace, args.trial)
        print(f"initialized {_path(args.workspace)} (harness {m['harness_version']})")
    elif args.cmd == "record":
        e = record(
            args.workspace, phase=args.phase, agent=args.agent, model=args.model,
            output=args.output, inputs=args.inputs, note=args.note,
        )
        out = e["output"]["sha256"][:12] if e["output"] else "-"
        print(f"recorded phase {e['phase']} ({e['agent']}/{e['model']}) output sha256:{out}")
    elif args.cmd == "show":
        m = _load(args.workspace)
        if not m:
            print(f"no manifest at {_path(args.workspace)}")
            return
        print(json.dumps(m, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
