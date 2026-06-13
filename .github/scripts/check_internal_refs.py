#!/usr/bin/env python3
"""Check that `.claude/...` file references inside the harness actually exist.

Scans every `.claude/**/*.md` for inline references to `.claude/<path>.<ext>`
(md / py / json) and fails if the referenced file is missing. This automates
the broken-reference class of consistency bugs (e.g. a renamed script or a
legacy `resources/` path) so they are caught in CI instead of at runtime.

Paths containing a `{placeholder}` are skipped (they are templates, not literal
references). Only `.md` and `.py` targets are checked — config files such as
`settings.local.json` are referenced advisorily (e.g. "do NOT store keys here")
and may legitimately not exist.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REF = re.compile(r"\.claude/[A-Za-z0-9_./-]+\.(?:md|py)")

missing = []
checked = 0

for md in glob.glob(os.path.join(ROOT, ".claude", "**", "*.md"), recursive=True):
    text = open(md, encoding="utf-8").read()
    for ref in REF.findall(text):
        if "{" in ref or "}" in ref:
            continue  # template placeholder, not a literal path
        checked += 1
        if not os.path.isfile(os.path.join(ROOT, ref)):
            missing.append(f"{os.path.relpath(md, ROOT)}  ->  {ref}")

if missing:
    print("BROKEN INTERNAL REFERENCES (referenced file does not exist):")
    for m in sorted(set(missing)):
        print("  -", m)
    sys.exit(1)
print(f"OK: internal references resolve ({checked} `.claude/...` path refs checked)")
