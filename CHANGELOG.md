# Changelog

All notable changes to this project are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/). The detailed design-evolution
log lives in `CLAUDE.md` (진화 로그); this file tracks user-facing releases.

## [Unreleased]

_No unreleased changes._

## [3.0.0] — 2026-06-14 — loop · goal · zero-trust · guardrail

3-모델 리뷰(Claude · Codex 0.139 · Gemini 0.46)에 기반해 최신 에이전트 엔지니어링
동향을 하네스에 반영한 메이저 릴리스. 설계 근거는
`docs/plugin_v3_advancement_proposal_ko.md` 참조.

### Added — 제안 1 (Goal + Loop engineering)
- `.claude/references/schemas/trial_goal_spec.schema.json` + `goal_spec.example.json`
  — estimand(ICH E9 R1)·CI 경계·검정력·필수 ICH 섹션·보존연한을 기계 판독형
  **성공명세**로 정의. Phase 1/4에서 확정하고 게이트 승인 대상으로 삼는다.
- `doc_lint.py`에 결정적 채점 `score_file()` + `--score`/`--goal-spec` CLI 추가
  (기존 `lint_file` API는 불변).
- 오케스트레이터 Phase 9를 `max 1 revision` → **예산형 actor-critic 수렴 루프**로
  재설계 (종료조건: Critical=0 & score≥90, 또는 budget 소진 / score plateau →
  사람 에스컬레이션). synopsis·design_decisions.md는 불변 입력으로 락.

### Added — 제안 2 (Zero-trust 근거·provenance)
- `.claude/scripts/qa/citation_verify.py` — PMID/NCT/DailyMed setid/URL을 추출하고
  PubMed eutils·ClinicalTrials.gov v2로 **독립 재조회**(offline-graceful),
  `_workspace/verification/citation_audit.json` 생성.
- `.claude/scripts/qa/source_snapshot.py` — 외부 fetch를 SHA-256·조회일·URL로
  스냅샷하여 `source_provenance.json`에 append (사이트 구조 변경에도 재현성 유지).
- IB least-privilege: `_workspace/00_input/ib_manifest.json` + Phase 2 섹션 제한 규칙,
  `SECURITY.md`에 기밀 데이터 취급 명문화.

### Added — 제안 3 (계층형 Guardrail)
- advisory 단일 hook을 **3-tier**로 승격: T0 차단(보존<15년, 명시 용량>MRSD,
  ICF PII, 최종화 시 Appendix B 섹션 누락), T1 권고(기존), T2 사람 게이트.
- `.claude/scripts/qa/dose_safety_guard.py` — 프로토콜 내 시작/증량 용량이 산출된
  MRSD 이하인지 결정적 검증.
- `/finalize` 커맨드 — `doc_lint --strict`를 **실제 생성 초안**에 적용하여 T0 실패
  문서의 "최종 승인"을 차단.

### Changed
- **전 에이전트(8종) opus(최신) 전환** — 조사·작성·검토 전 단계 최고 추론 모델.
- 8개 페르소나(`.claude/agents/*.md`)에 v3 역할(goal_spec 충족 매핑, zero-trust
  인용 검증, 가드레일 tier, 수렴 루프 actor/critic) 주입.
- `plugin.json` / `marketplace.json` 버전 **3.0.0**.

## [2.1.0] — 2026-06-14 — enterprise-grade hardening

Released as **v2.1.0** (`plugin.json` / `marketplace.json`). Merged to `main`
via **PR #1** (CI green). Integrates this cycle's hardening with parallel work
already on `main`; see "Integration" below.

### Added

- **CI/CD pipeline** (`.github/workflows/ci.yml`): pytest + doctest, ruff
  (critical errors), plugin/manifest validation, harness internal-reference
  check, protocol output lint, and gitleaks secret scan. (EA-2)
- **Output-quality linter** (`.claude/scripts/qa/doc_lint.py`): ICH E6(R3)
  Appendix B 16-section coverage, KGCP 15-year document retention, BE/DDI
  90% CI 80.00–125.00% bounds, unresolved placeholders, and conservative
  citation checks. Used both as a strict CI gate on the golden fixtures and as
  an advisory hook. (EA-1)
- **Advisory validation hook** (`.claude/hooks/`): non-blocking PostToolUse
  warnings on the protocol/ICF drafts right after they are written. (EA-4)
- **Reproducibility manifest** (`.claude/scripts/qa/pipeline_manifest.py`
  + JSON schema): per-phase provenance — agent, model, input/output SHA-256,
  UTC timestamp, harness version. (EA-3)
- **Extension guide** (`.claude/EXTENSION_GUIDE.md`): file-by-file checklist for
  adding a trial type, sample-size design, agent, or Web API recipe. (EA-8)
- **Harness validators** (`.github/scripts/validate_manifests.py`,
  `check_internal_refs.py`) automating the manual consistency checks.
- Single source of truth for exact TOST power/sample size in
  `utils/power_analysis.py` (`tost_power_2x2`, `solve_n_2x2_tost`).
- pytest suites (73 tests) validating sample-size and FIH dose formulas against
  PowerTOST, FDA guidance, and Monte-Carlo references.
- `.claude/scripts/requirements.txt`; root `.claude-plugin/marketplace.json`;
  `LICENSE` (MIT), `SECURITY.md`, `CONTRIBUTING.md`, `.env.example`.
- API robustness: PharmGKB HTTP-400 → CPIC official fallback; DailyMed/openFDA
  license & attribution notes.
- README: Installation section, corrected agent count (8), updated Phase 2
  diagram.

### Fixed (statistics — regulatory-critical)

- **2×2 crossover BE/DDI factor-of-2 over-estimation**: the total-N formula was
  applied as a per-sequence count and then doubled (CV25%/GMR0.95/80% returned
  52 instead of 28). Replaced with an **exact TOST** engine (noncentral-t /
  chi-square integration), validated against PowerTOST + Monte Carlo.
- **RSABE scaled-limit formula** (`replicate_crossover_be.py`): corrected from
  `σ₀·σ_w` to `(ln(1.25)/σ₀)·σ_w` (FDA k = 0.8926; ~3.57× margin error). Added a
  "not validated for regulatory submission" warning pending a simulation method.
- **Williams 6×3 bidirectional DDI joint power**: removed the incorrect claim
  that IUT guarantees joint power; the co-primary target now inflates per-
  direction power to √(target) and reports both marginal and joint power.
- **Normal-approximation under-powering at GMR = 1.0**: surfaced while
  reconciling the parallel branch's test — for CV30%/GMR1.0/80% the true minimum
  is **N = 32** (Monte-Carlo verified), but the normal approximation suggested
  ~24 (≈ 0.64 power). The exact-TOST engine was adopted and the affected test
  corrected.
- **KGCP document-retention error** (3년 → **15년**) in the e2e v2 DDI golden
  protocol fixture, caught by the new linter.

### Changed

- **Packaging**: `marketplace.json` moved from inside the plugin directory to
  the repository root (`claude plugin validate` passes for the plugin and
  marketplace manifests); the deployable `.zip` is no longer committed
  (`plugin/**/*.zip` git-ignored; publish as a GitHub Release asset).
- **Consistency**: `clinician` uniformly documented as **always participating**;
  regulatory constants (KGCP 15y, SAE 7+8 day, 90% CI 80.00–125.00%) and the
  Phase-1 terminology guide reinforced in `protocol.md`.
- **Regulatory precision**: ICH E6(R3) **Annex 2 reached Step 4 (2026-06-03)**
  reflected (was "Step 2 draft, expected end-2025"); CYP2C19 Korean allele
  frequencies expressed as ranges; SAE fatal/life-threatening 7-day + 8-day
  clock clarified; anaphylaxis dosing citation added.

### Integration (PR #1)

Both this branch and `main` independently fixed the same factor-of-2 / RSABE /
Williams / clinician issues. The merge kept the **exact-TOST** engine (more
precise) and preserved `main`'s unique additions: `.githooks/pre-commit`,
`trial_info_input.md`, the Phase 2 `label_pgx` dependency edge, the
`.omc/research/` 3-model review, and the README quickstart. The deployable
`plugin/` tree was regenerated from the merged source via `sync_plugin.sh`.

## [2.0.0] — 2026-04-15

- Initial Claude Code plugin packaging (see `CLAUDE.md` 진화 로그 for the full
  development history: 8-agent team, 10-phase pipeline, guideline library,
  Web API recipes, Williams 6×3 bidirectional DDI design).
