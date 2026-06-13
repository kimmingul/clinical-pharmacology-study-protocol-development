# Contributing

This is a Claude Code plugin/harness for developing clinical-pharmacology trial
documents. Contributions are welcome — please keep the following in mind.

## Repository layout

- `.claude/` — **the single source of truth** (agents, commands, skills,
  references, scripts). Develop here.
- `plugin/clinical-pharmacology-study-protocol-development/` — deployable copy
  generated from `.claude/` by `./sync_plugin.sh` (paths rewritten to
  `${CLAUDE_PLUGIN_ROOT}`). Do not edit by hand.
- `.claude-plugin/marketplace.json` — marketplace manifest (repository root).
- `e2e/` — end-to-end run artifacts kept as regression fixtures.
- `docs/` — guidance source documents and the AI-textbook manuscript.

## Statistical / calculation code (`.claude/scripts/`)

Sample-size and dose calculations feed regulatory documents, so correctness is
non-negotiable.

```bash
cd .claude/scripts
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -q        # all must pass
```

- Any change to a formula **must** be accompanied by a test that pins the
  expected value against an independent reference (PowerTOST, FDA guidance
  examples, or a documented simulation).
- Calculators not yet validated against reference software must emit a
  "not for regulatory submission" warning and say so in the docstring.

## Plugin packaging

After changing anything under `.claude/`:

```bash
./sync_plugin.sh                                   # regenerate plugin/ copy
claude plugin validate plugin/clinical-pharmacology-study-protocol-development
claude plugin validate .                           # marketplace manifest
```

## Commits

Conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).
Keep document body language Korean (medical/regulatory terms with English in
parentheses), code and config in English.

## Reference integrity

Never fabricate PMIDs/NCTs/guideline citations. See `SECURITY.md`.
