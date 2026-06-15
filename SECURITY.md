# Security & Data-Handling Policy

This project generates **regulatory clinical-trial documents** (Protocol, ICF,
Synopsis) and queries public biomedical APIs. The following policies apply.
They are enforced both by tooling and by agent instruction. As of **v3.0.0**
the automated enforcement is implemented: a **3-tier guardrail hook**
(`.claude/hooks/draft_advisory_hook.py` — T0 blocking / T1 advisory),
deterministic `doc_lint.py` (CI `--strict` gate), independent citation
verification (`citation_verify.py`), source provenance (`source_snapshot.py`),
and a dose-safety guard (`dose_safety_guard.py`). CI also runs a secret scanner
(gitleaks) on every push.

## Secrets & API keys

- **Never commit secrets.** API keys live in environment variables only
  (`MFDS_SERVICE_KEY`, `OPENFDA_API_KEY`). See `.env.example`; copy to `.env`
  (git-ignored).
- Do not place keys in `settings.json` / `settings.local.json` or any tracked
  file. CI should run a secret scanner (e.g. gitleaks) on every push.

## Reference integrity (zero-trust, v3)

- Every PMID / NCT / guideline citation in a generated document is **untrusted by
  default** and must be **verified** from an actual tool/API result, never
  produced from memory.
- Independent verification is enforced by `.claude/scripts/qa/citation_verify.py`
  (PMID via NCBI eutils, NCT via ClinicalTrials.gov v2), which writes
  `_workspace/verification/citation_audit.json`. Items that fail format or
  resolution are marked `[출처 미확인 — 검증 필요]` and must **not** be used as
  load-bearing evidence (dose justification, safety claims).
- External fetches (MFDS / DailyMed / openFDA / PharmGKB) are snapshotted by
  `.claude/scripts/qa/source_snapshot.py` (content SHA-256 + retrieval URL + UTC),
  so a document's provenance does not depend on a live, mutable website.

## Confidential IB (least-privilege, v3 — FIH/SAD/MAD)

- A new-drug Investigator's Brochure (IB) is **confidential** and is the only
  primary source for FIH dosing. Treat it as least-privilege data:
  - Record only its hash + allowed sections per agent in
    `_workspace/00_input/ib_manifest.json`; do not duplicate raw IB text into
    multiple outputs.
  - Pass each agent **only the IB sections it needs** (e.g. clinical-pharmacologist
    → nonclinical PK/tox/pharmacology only).
  - **Never** send raw IB content to external tools/APIs (WebFetch, openFDA,
    PharmGKB, etc.). External calls use only the non-confidential drug name/class.
  - Cloud-LLM exposure of confidential IB is the operator's risk decision; keep
    IB local where organizational policy requires.
- Stated FIH starting/escalation doses are checked against the independently
  computed MRSD by `.claude/scripts/qa/dose_safety_guard.py` (T0-blocking).

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
