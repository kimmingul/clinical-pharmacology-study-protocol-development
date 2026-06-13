# Security & Data-Handling Policy

This project generates **regulatory clinical-trial documents** (Protocol, ICF,
Synopsis) and queries public biomedical APIs. The following policies apply.
They are partly enforced by tooling and partly by agent instruction; see the
roadmap (Phase 6) for the planned automated enforcement (validation hooks, CI
secret scanning).

## Secrets & API keys

- **Never commit secrets.** API keys live in environment variables only
  (`MFDS_SERVICE_KEY`, `OPENFDA_API_KEY`). See `.env.example`; copy to `.env`
  (git-ignored).
- Do not place keys in `settings.json` / `settings.local.json` or any tracked
  file. CI should run a secret scanner (e.g. gitleaks) on every push.

## Reference integrity (no fabrication)

- Every PMID / NCT / guideline citation in a generated document must be
  **verified** from an actual tool/API result, never produced from memory.
- Unverified items must be marked `[출처 미확인 — 검증 필요]` rather than guessed.
- Planned enforcement: a PreToolUse/Stop hook validating citations before a
  document is written (Phase 6, EA-4).

## Participant data / PII (생명윤리·개인정보)

- Generated artifacts are design documents, not subject data. Do **not** paste
  real participant identifiers, initials, or institution-linked identifiers
  into trial inputs or `_workspace/` outputs.
- Pharmacogenomic / metabolomic (PG/오믹스) and retained-sample plans trigger
  **bioethics-law** obligations: ICF Part 4 (optional consent) and possible
  institutional bioethics-committee review. See
  `.claude/references/guidelines/regulations/korea_bioethics_act.md` and
  `korea_pipa.md`.
- `_workspace/` is git-ignored at the repository root; treat its contents as
  potentially sensitive and do not share without review.

## Output handling

- Markdown outputs are plain text and shareable; they may contain sensitive
  trial-design details. Apply your organization's access controls before
  distribution.
- These documents are **drafts for expert review**, not validated regulatory
  submissions. Statistical calculators that are not yet validated against
  reference software emit an explicit "not for regulatory submission" warning
  (e.g. RSABE in `replicate_crossover_be.py`).

## Reporting a vulnerability

Open a private security advisory or contact the maintainer (see `plugin.json`
author). Please do not file public issues for sensitive disclosures.
