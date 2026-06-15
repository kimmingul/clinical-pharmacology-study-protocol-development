#!/usr/bin/env python3
"""Provenance snapshots for external fetches (zero-trust: pin what was fetched).

Whenever the harness pulls content from an external source (a DailyMed label, a
ClinicalTrials.gov record, a PubMed summary, a guideline page) it can pin the
exact bytes it relied on: the raw content is written verbatim to
<workspace>/verification/sources/<sha12>.snapshot and an append-only entry is
added to <workspace>/verification/source_provenance.json. Re-running the same
content is idempotent (same sha -> same snapshot file), so the provenance trail
answers "what exactly did we read, from where, and when".

Usage
-----
    source_snapshot.py add --url URL --file PATH [--workspace _workspace]
    source_snapshot.py show [--workspace _workspace]

stdlib only.
"""
import argparse
import hashlib
import json
import os
from datetime import datetime, timezone

PROVENANCE_NAME = "source_provenance.json"


def _utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _as_bytes(content):
    if isinstance(content, bytes):
        return content
    return content.encode("utf-8")


def _provenance_path(workspace):
    return os.path.join(workspace, "verification", PROVENANCE_NAME)


def _load_provenance(workspace):
    p = _provenance_path(workspace)
    if os.path.isfile(p):
        return json.load(open(p, encoding="utf-8"))
    return {"schema": "source_provenance/v1", "sources": []}


def _save_provenance(workspace, doc):
    p = _provenance_path(workspace)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")


def snapshot(content, url, workspace="_workspace"):
    """Pin `content` fetched from `url`: write the raw bytes + provenance entry.

    Returns the entry {url, sha256, retrieved_utc, bytes, path}.
    """
    raw = _as_bytes(content)
    sha = hashlib.sha256(raw).hexdigest()

    sources_dir = os.path.join(workspace, "verification", "sources")
    os.makedirs(sources_dir, exist_ok=True)
    snap_path = os.path.join(sources_dir, f"{sha[:12]}.snapshot")
    with open(snap_path, "wb") as f:
        f.write(raw)

    entry = {
        "url": url,
        "sha256": sha,
        "retrieved_utc": _utc_now(),
        "bytes": len(raw),
        "path": snap_path,
    }

    doc = _load_provenance(workspace)
    doc.setdefault("schema", "source_provenance/v1")
    doc.setdefault("sources", [])
    doc["sources"].append(entry)
    _save_provenance(workspace, doc)
    return entry


def main():
    ap = argparse.ArgumentParser(description="Source provenance snapshots.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("--url", required=True)
    p_add.add_argument("--file", required=True)
    p_add.add_argument("--workspace", default="_workspace")

    p_show = sub.add_parser("show")
    p_show.add_argument("--workspace", default="_workspace")

    args = ap.parse_args()

    if args.cmd == "add":
        with open(args.file, "rb") as f:
            content = f.read()
        entry = snapshot(content, args.url, workspace=args.workspace)
        print(
            f"snapshot sha256:{entry['sha256'][:12]} "
            f"({entry['bytes']} bytes) -> {entry['path']}"
        )
    elif args.cmd == "show":
        doc = _load_provenance(args.workspace)
        print(json.dumps(doc, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
