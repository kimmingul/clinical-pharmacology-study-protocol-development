# Changelog

All notable changes to this project are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/). The detailed design-evolution
log lives in `CLAUDE.md` (진화 로그); this file tracks user-facing releases.

## [Unreleased]

### Added — fail-closed release 게이트 (`/finalize`)

- **`.claude/scripts/qa/finalize_run.py` 신설.** `/finalize`의 판정 로직이 커맨드
  마크다운(에이전트 해석)에서 결정적 실행 파일로 옮겨졌다. 5개 차원
  (`structure`/`citation`/`dose`/`advisory`/`approval`)을 실행하고
  `<workspace>/verification/release_gate.json`(`schema: release_gate/v1`)에 기록한다.
- **프로파일 2종.** `--profile draft`(기본)는 placeholder·미확인 인용을 표시만 하고,
  `--profile submission`은 미해결 권고·online 미검증 인용을 차단한다.
- **종료코드 3분기.** `0` 통과 / `1` 판정했고 불합격 / `2` 판정 불가(대상 없음·검사기
  크래시·리포트 기록 실패). `ERROR`가 `FAIL`보다 우선하므로 게이트 고장이 문서 불량으로
  보고되지 않는다.

### Changed — 사용자 계약 변경

- `/finalize`는 이제 종료코드를 재해석하지 않는 얇은 래퍼다. 통과 시에만
  `pipeline_manifest.py record --phase finalize`로 provenance를 남긴다.
- 상태 어휘는 정확히 `PASS`/`FAIL`/`SKIPPED`/`FORMAT_ONLY`/`NOT_IMPLEMENTED`/`ERROR`
  6개다. 검사기가 실행되지 않은 상태를 '통과'로 부르지 않는 것이 이 게이트의 목적이다.
- **게이트 통과는 '제출 가능'을 뜻하지 않는다.** 사람 승인 차원(`approval`)은
  서명 이벤트 스토어 미구현으로 `NOT_IMPLEMENTED`이며, 매 실행 경고로 노출된다.
  `submission` 프로파일의 online 인용 검증도 PMID·NCT만 조회하고 DailyMed setid·URL은
  형식만 확인하므로 `FORMAT_ONLY`로 표기된다(제출 프로파일에서는 차단).

## [4.2.0] — 2026-06-29 — 버그픽스: agy 마이그레이션 + 명시 모델 핀

Multi-LLM 어댑터의 가용성·정확성 버그 3건을 수정한 유지보수 릴리스. 핀할 4개
모델 id를 모두 실제 CLI 호출로 검증한 뒤 반영했다. (조사·라우팅 로직·capability
점수는 불변 — 순수 버그픽스.)

### Fixed — Multi-LLM 어댑터
- **gemini CLI → agy(antigravity) 강제 마이그레이션**: Google이 2026-06-18부로
  `gemini` CLI 서비스를 중단(공식 전환). `model_profiles.json` google provider를
  `cli:"agy"`·`version_cmd:["agy","--version"]`로 교체. agy는 IDE형 에이전트라
  대용량 응답을 brain 아티팩트에 쓰고 stdout엔 요약+`file://` 경로만 출력 →
  `ask_model.sh` google 분기를 **stdin 입력(ARG_MAX 무관) + 아티팩트 경로 파싱**
  어댑터로 재작성. agy 시작 지연 대응으로 `health_check.py`에 **per-provider
  `probe_timeout`** 추가(google=70)하여 healthy provider가 false `timeout`으로
  분류되는 것 방지.
- **Anthropic 모델 명시 핀 + Fable 차단 (provenance 무결성)**: `ask_model.sh`가
  `resolved_model`을 **dispatch 앞에서 읽어 `--model`로 전달** → "기록한 모델 =
  실제 호출 모델"이 구조적으로 보장(기존엔 provenance에 opus를 기록하면서 실제로는
  CLI 기본 모델을 호출 → Fable일 경우 거짓 기록 + 수출통제 위반 위험). anthropic에
  `availability_constraint`(Fable 5/Mythos 5 수출통제→Opus 4.8 고정, 자동 latest
  금지) 명문화.
- **각 회사 최신 고성능 모델을 날짜 스냅샷으로 명시 핀** (B3, 사용자 선택=스냅샷):
  anthropic `claude-opus-4-8` · openai `gpt-5.5` · google `gemini-3.5-pro-002`(스냅샷)
  · xai `grok-build`. `resolved_model`을 서술 문자열에서 **바레 `--model` id**로 정리.
  probe_cmd도 동일 `--model`을 핀해 health probe가 실제 호출 모델을 검증. (codex/grok
  CLI는 dated snapshot을 미노출하여 alias 핀 + `model_note`로 사유 기록.)

### Security — agy 어댑터 하드닝 (커밋 보안 리뷰 반영)
- **자율 에이전트 sandboxing**: agy는 로컬 도구를 실행할 수 있는 IDE형 자율
  에이전트라, `ask_model.sh`·probe에서 **`--dangerously-skip-permissions`를 절대
  쓰지 않고 `--sandbox`로 실행**(codex `--sandbox read-only`와 동일 원칙). ask_model
  프롬프트에는 외부 fetch 콘텐츠가 섞일 수 있어, prompt-injection이 **로컬 코드
  실행으로 번지는 경로를 차단**.
- **아티팩트 경로 검증**: agy stdout에서 파싱한 `file://…md` 경로를 무검증으로 `cp`
  하던 것을, **agy 자신의 brain 디렉토리(`~/.gemini/antigravity-cli/brain`) 하위로
  canonical(realpath) 검증** 후에만 회수 — 주입으로 밀반입된 임의 로컬 `.md` 읽기 차단,
  벗어나면 stdout 요약으로 안전 폴백.

### Tests
- `test_llm_router.py`에 v4.2 불변식 고정 테스트 6건 추가(agy cli, 바레 id, probe의
  `--model` 핀 일치, Fable 금지, per-provider probe_timeout). **전체 152 passed.**

## [4.1.0] — 2026-06-16 — 4-모델 리뷰 반영 (정확성·적절성·정합성·시의성)

Opus·Codex·Gemini 4축 교차 검토 지적을 검증 후 일괄 수정한 릴리스. (외부 모델이
자기 CLI/모델명을 오인한 부분은 실측으로 기각.)

### Fixed — 안전 (P0)
- **egress 하드코딩 제거**: `/review`·SKILL Phase 9의 `--classification REGULATORY_PUBLIC`
  하드코딩을 시험유형 기반 선언으로 교체. `egress_gate.py`에 **`confidential_context`
  (ib_manifest) 강제 floor** 추가 — FIH/IB 초안은 선언과 무관하게 외부 전송 차단.
  `ask_model.sh`가 `ib_manifest.json`을 자동 적용(이중 안전).

### Fixed — 정확성/정합성 (P1)
- **`ask_model.sh` stdin/`--prompt-file` 디스패치**: 프로토콜 전문을 CLI 인자로 넘기던
  ARG_MAX(E2BIG) 위험 제거(Linux 이식성). provenance에 model id·prompt_sha·egress 기록.
- **보존기간 법령 근거화**: `doc_lint`에 `RETENTION_LEGAL_BASIS`(「의약품등의 안전에 관한
  규칙」 별표 4·KGCP, 15년) + 공유 `_retention_errors`(보존/보유/보관), **ICF에도 적용**.
  `icf-template`의 "최소 3년" → 법령 인용 15년. 임계값은 `goal_spec.retention_years_min`로 조정.
- `/finalize icf`가 실제 `04_icf_draft.md` 검사(기존 03 고정 버그). judge_synth = host 역할
  명시. `/review` Step 4 "최대 1회" → 수렴 루프. model_profiles resolved_model 현행화.

### Fixed — 정합성/시의성 (P2)
- egress 마커 **단어경계 매칭**(ASCII) → 'ib'의 calibration/fibrosis 오탐 제거.
- v4 제안서 "구현 완료" 배지, README 구조에 `scripts/llm`·`references/llm`·`/llm-health`·
  `/finalize` 반영. ICH E6(R3) **Annex 2 Step 4(2026-06-03)**·**M12 Step 4(2024-05-21)** 표기 정정.

### Verified
- `pytest .claude/scripts/` → **152 passed**, ruff clean. 라이브 재검증(egress IB 차단·
  단어경계·ask_model stdin·ICF 보존) 통과.

## [4.0.0] — 2026-06-16 — Multi-LLM + Multi-Persona 하이브리드 (벤더 중립)

Single-LLM(Multi-Persona) → **Multi-LLM + Multi-Persona 하이브리드**로의 메이저 릴리스.
4-모델 자문(Claude Opus · GPT/codex · Gemini · Grok)에 기반. 설계 근거:
`docs/plugin_v4_multi_llm_proposal_ko.md`. **단일-LLM 사용자는 v3와 동작 동등**
(`multi_llm=false`); 다중 보유자는 환경에 맞는 조합으로 작동.

### Added — 벤더 중립 Multi-LLM 라우팅 (`.claude/scripts/llm/`)
- **`health_check.py`** + **`/llm-health`** — 각 LLM CLI에 nonce+산술 probe로
  **로그인/키 실동작** 검증(존재 확인 ❌), 재실행 가능(세션 중 만료 대비), 자동 폴딩.
- **`route_select.py`** — `health × capability_scores`로 결정적 **벤더 중립** 배정.
  authoring=host, biostat=Grok 1순위, judge≠author. 호스트는 제안만.
- **`egress_gate.py`** — **fail-closed** 데이터 분류 게이트. 선언 floor + 마커는
  상향만. 벤더명 하드코딩 없음(`host`/`*`/literal). 기밀 IB/안전핵심은 호스트 무관 차단.
- **`ask_model.sh`** — 모든 외부 호출 단일 게이트(egress→dispatch→manifest).
- 데이터: `.claude/references/llm/{model_profiles,combination_profiles,egress_policy,review_roles}.json`
  — 강점을 **편집 가능 데이터**로(모델 진화 대응, `as_of`).

### Added — Phase 9 cross-vendor critic 패널
- **`review_panel.py`** — `build_panel`(역할→비-host 배정) + `synthesize`(결정적
  우선·출처 태깅·상충 플래그·다수결 ❌) + `_extract_json`(산문 래핑 JSON 회수) +
  `collect_deterministic`(doc_lint/citation/dose findings 합류) + `fixplan`
  (synthesis→`qa_fix_plan.md`, 수렴 루프 actor 입력).
- **`run_review_panel.sh`** — 패널 드라이버(egress 경유). `/review` Step 2.5 +
  SKILL Phase 9에 배선. 미가용/host 역할·기밀은 host qa-reviewer로 폴딩.

### Changed
- `/review`·orchestrator Phase 9가 `multi_llm` + routing_plan 존재 시 이종 패널 실행.
- `plugin.json` / `marketplace.json` 버전 **4.0.0**.

### Verified (live, 실제 4개 CLI)
- `/llm-health` 4/4 ok; 라우팅 벤더 중립(Grok=biostat); egress fail-closed 허용/차단/상향.
- Phase 9 라이브 패널(clopidogrel+omeprazole 공개 DDI): Gemini+Grok critic 실호출,
  **Grok이 Gemini가 놓친 5개 Critical 포착**(이종 교차검증 가치). 결정적 우선이 벤더
  오판(보존 "3년") 방어. `pytest 146 passed`, ruff clean.

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
