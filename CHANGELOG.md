# Changelog

All notable changes to this project are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/). The detailed design-evolution
log lives in `CLAUDE.md` (진화 로그); this file tracks user-facing releases.

## [Unreleased] — enterprise-grade hardening

### Fixed (statistics — regulatory-critical)
- **RSABE scaled-limit formula** (`replicate_crossover_be.py`): corrected the
  reference-scaled limit from `σ₀·σ_w` to `(ln(1.25)/σ₀)·σ_w` (FDA k=0.8926).
  The previous formula understated the margin ~3.57×. Added a "not validated
  for regulatory submission" `RuntimeWarning` pending a simulation-based method.
- **2×2 crossover BE factor-of-2 over-estimation** (`crossover_2x2_be.py`):
  the total-N formula was applied as a per-sequence count and then doubled
  (e.g. CV25%/GMR0.95/80% returned 52 instead of 28). Replaced with an **exact
  TOST** sample size (noncentral-t / chi-square integration) validated against
  the PowerTOST package.
- **2×2 crossover DDI factor-of-2** (`crossover_2x2_ddi.py`): same bug; the
  equivalence path now reuses the exact TOST engine, the fold-change path no
  longer doubles a total formula.
- **Williams 6×3 bidirectional DDI joint power** (`williams_6x3_ddi.py`):
  removed the incorrect claim that IUT guarantees joint power. The co-primary
  (both-directions-pass) target now inflates per-direction power to √(target)
  and the result reports both marginal and joint power.

### Added
- Single source of truth for exact TOST power/sample size in
  `utils/power_analysis.py` (`tost_power_2x2`, `solve_n_2x2_tost`).
- pytest suite (`.claude/scripts/tests/`, 48 tests) validating sample-size and
  FIH dose formulas against PowerTOST and FDA-guidance values.
- `.claude/scripts/requirements.txt` (scipy, numpy, pytest).
- Root `.claude-plugin/marketplace.json` (correct marketplace location).
- `LICENSE` (MIT), `SECURITY.md`, `CONTRIBUTING.md`, `.env.example`.
- README: Installation section, corrected agent count (8), updated Phase 2
  diagram.

### Changed
- Plugin packaging: `marketplace.json` moved from inside the plugin directory
  to the repository root; `claude plugin validate` passes for both the plugin
  and marketplace manifests. The deployable `.zip` is no longer committed
  (published as a GitHub Release asset; `plugin/**/*.zip` git-ignored).
- Harness consistency: `clinician` is now uniformly documented as **always
  participating** (removed the contradictory "healthy-subject = excluded" note
  in `clinical-research/SKILL.md`).

## [2.0.0] — 2026-04-15
- Initial Claude Code plugin packaging (see `CLAUDE.md` 진화 로그 for the full
  development history: 8-agent team, 10-phase pipeline, guideline library,
  Web API recipes, Williams 6×3 bidirectional DDI design).
