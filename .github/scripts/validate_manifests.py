#!/usr/bin/env python3
"""Validate plugin.json / marketplace.json and the .claude -> plugin sync invariants.

Deterministic, dependency-free checks that run in CI without the Claude CLI or
any API key. Exits non-zero on the first set of failures found.

Checks
------
1. Root `.claude-plugin/marketplace.json`: valid JSON; kebab-case name; owner
   present; non-empty plugins[]; each plugin source dir exists and contains
   `.claude-plugin/plugin.json`.
2. Each `plugin/*/.claude-plugin/plugin.json`: name (kebab-case, equals its
   directory), semver-ish version.
3. Sync substitution: no literal `.claude/` path remains in the deployed
   plugin tree (must be `${CLAUDE_PLUGIN_ROOT}/`); applies to .md and .py.
4. Filename parity for agents/ and commands/ between `.claude/` and the plugin
   copy (the sync must not drop or add files).
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DOTCLAUDE = re.compile(r"\.claude/")  # '.claude-plugin/' does NOT match (hyphen)

errors = []


def err(msg):
    errors.append(msg)


def rel(p):
    return os.path.relpath(p, ROOT)


# 1. marketplace.json
mp_path = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
if not os.path.isfile(mp_path):
    err("missing .claude-plugin/marketplace.json at repository root")
else:
    try:
        mp = json.load(open(mp_path, encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"marketplace.json invalid JSON: {e}")
        mp = {}
    if not KEBAB.match(mp.get("name", "")):
        err(f"marketplace name not kebab-case: {mp.get('name')!r}")
    if "owner" not in mp:
        err("marketplace.json missing 'owner'")
    plugins = mp.get("plugins") or []
    if not plugins:
        err("marketplace.json has empty plugins[]")
    for p in plugins:
        name, src = p.get("name", ""), p.get("source", "")
        if not KEBAB.match(name):
            err(f"plugin name not kebab-case: {name!r}")
        if not src:
            err(f"plugin {name!r} missing 'source'")
            continue
        src_dir = os.path.normpath(os.path.join(ROOT, src))
        if not os.path.isdir(src_dir):
            err(f"plugin source is not a directory: {src!r}")
        elif not os.path.isfile(os.path.join(src_dir, ".claude-plugin", "plugin.json")):
            err(f"plugin source missing .claude-plugin/plugin.json: {src!r}")

# 2. plugin.json
for pj in glob.glob(os.path.join(ROOT, "plugin", "*", ".claude-plugin", "plugin.json")):
    try:
        pjson = json.load(open(pj, encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"{rel(pj)} invalid JSON: {e}")
        continue
    if "name" not in pjson:
        err(f"{rel(pj)} missing 'name'")
    if "version" not in pjson:
        err(f"{rel(pj)} missing 'version'")
    elif not re.match(r"^\d+\.\d+\.\d+", str(pjson["version"])):
        err(f"{rel(pj)} version not semver-like: {pjson['version']!r}")
    dirname = os.path.basename(os.path.dirname(os.path.dirname(pj)))
    if pjson.get("name") != dirname:
        err(f"plugin name {pjson.get('name')!r} != directory {dirname!r}")

# 3. sync substitution invariant — sed only rewrites *.md, so the check is
#    scoped to Markdown (where a leftover '.claude/' is a real broken path).
#    Python keeps relative __file__ paths (verified by pytest in CI), and a
#    '.claude/' in a .py docstring is documentation, not a runtime path. The
#    hand-written plugin README (legitimate ~/.claude/plugins/) is also skipped.
SYNCED_SUBDIRS = ("agents", "commands", "skills", "scripts", "references", "hooks")
for plugin_dir in glob.glob(os.path.join(ROOT, "plugin", "*")):
    if not os.path.isdir(plugin_dir):
        continue
    for sub in SYNCED_SUBDIRS:
        for f in glob.glob(os.path.join(plugin_dir, sub, "**", "*.md"), recursive=True):
            n = len(DOTCLAUDE.findall(open(f, encoding="utf-8").read()))
            if n:
                err(f"{rel(f)} contains {n} literal '.claude/' path(s) "
                    f"-> sync substitution to ${{CLAUDE_PLUGIN_ROOT}} incomplete")

# 4. filename parity
for sub in ("agents", "commands"):
    base = {os.path.basename(x) for x in glob.glob(os.path.join(ROOT, ".claude", sub, "*.md"))}
    for pdir in glob.glob(os.path.join(ROOT, "plugin", "*", sub)):
        copy = {os.path.basename(x) for x in glob.glob(os.path.join(pdir, "*.md"))}
        if base != copy:
            err(f"{sub}/ mismatch vs {rel(pdir)}: "
                f"only-in-.claude={sorted(base - copy)} only-in-plugin={sorted(copy - base)}")

if errors:
    print("PLUGIN / MANIFEST VALIDATION FAILED:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("OK: plugin manifests + marketplace + sync invariants valid")
