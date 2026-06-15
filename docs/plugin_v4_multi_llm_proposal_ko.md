# 플러그인 고도화 제안서 v4 — Multi-LLM + Multi-Persona 하이브리드

| 항목 | 내용 |
|------|------|
| 대상 | `clinical-pharmacology-study-protocol-development` (현 v3.0.0 → v4 방향) |
| 작성일 | 2026-06-15 |
| 자문(실제 병렬 실행) | **Claude Opus 4.8** · **GPT(codex 0.139)** · **Gemini 0.46** · **Grok 0.2.51** |
| 상태 | 제안 (검토용) — 구현 전 |

> **자문 방법**: 동일 프롬프트로 GPT·Gemini·Grok을 병렬 호출하고, Claude(본인)의 독립 설계와 대조했다. 네 관점이 거의 동일한 결론에 수렴했다.

---

## 0. 자문 합의 (4-모델)

| 합의 사항 | GPT | Gemini | Grok | Claude |
|---|:--:|:--:|:--:|:--:|
| 작성기(writer)는 단일 LLM(Claude opus) 유지 | ✅ | ✅ | ✅ | ✅ |
| 멀티-LLM은 **검증/리뷰 레이어**에 (특히 Phase 9) | ✅ | ✅ | ✅ | ✅ |
| **이종 교차검증**(작성≠검증 벤더)이 최고 임팩트 | ✅ | ✅ | ✅ | ✅ |
| **기밀 IB/용량 데이터 외부 fan-out 금지**가 최대 리스크 | ✅ | ✅ | ✅ | ✅ |
| 결정적 도구(doc_lint/citation/dose)가 판정 우선, 숫자는 LLM-judge 금지 | ✅ | ✅ | ✅ | ✅ |
| manifest에 provider·정확한 버전·temp·prompt/IO 해시 기록 | ✅ | ✅ | ✅ | ✅ |

> **OMC 전제 검증**: OMC는 `omc ask <claude|codex|gemini>`·`omc team N:codex|gemini`·`/ccg`로 cross-vendor 오케스트레이션을 실제 제공한다. 단 OMC의 model routing은 Claude 티어(haiku/sonnet/opus)뿐이며 **grok·GPT-직접은 1급 미지원** → 커스텀 어댑터 필요. 메커니즘 본질은 **외부 CLI(codex/gemini/grok)를 어댑터로 감싸 호출**하는 것.

---

## 1. 핵심 원칙 — 선택적 하이브리드 (전면 교체 ❌)

**"작성은 단일, 검증은 다중."** 멀티-LLM은 *독립적 오류 프로파일*이 가치를 내는 곳(반박·교차검증·해석 차이 탐지)에만 적용한다. 정형 생성·결정적 검사는 그대로 둔다(비용·지연·변동성·환각 분산 방지).

## 2. 모델 ↔ 역할 라우팅 (각 모델 자가 평가 반영)

| 모델 (현 CLI) | 강점 | 배치 |
|---|---|---|
| **Claude Opus 4.8** | 장문·문체 일관·규제 추론·기밀 IB | **주 작성자**(protocol/icf-writer) + **오케스트레이터/판관** + FIH IB 추론 |
| **GPT (codex 0.139)** | 구조화·정책 대조·결함 분류·provenance | **규제/QA 적대적 리뷰어**, traceability 감사, 통계·코드 검증 |
| **Gemini (0.46)** | 초대형 컨텍스트·문헌/가이드라인 일괄 대조 | **citation_verify 보조**, ICH/MFDS/FDA/EMA 가이드라인 교차검토 |
| **Grok (0.2.51)** | 정량·contrarian·freshness | **biostat 반박 critic** + red-team 검토(공개자료 한정) |

## 3. 적용 지도 (Phase별)

| 영역 | 방식 | 근거 |
|---|---|---|
| doc_lint / dose_safety / citation 형식 | **코드(LLM 없음)** | 이미 결정적·최고 신뢰 |
| protocol/icf 작성 | **단일(Opus)** | 문체·일관성, 멀티는 문서 파편화 |
| **Phase 9 리뷰 + 수렴 루프** | **이종 critic 패널**(Opus+GPT+Gemini, Grok 반박) | blind-spot 최대 감소 — 1순위 |
| dose·sample size·citation 내용 일치 | **cross-vendor 적대적 검증** | 환자안전 직결 |
| Phase 4 설계 / synopsis 변형 | **debate→Claude 판관** | 해 공간 넓음 |
| Phase 2 연구(허가약물) | 2모델 병렬 → citation_verify로 merge | 사실성↑ (후순위) |
| FIH IB 분석·MRSD·Phase 7 게이트 | **Opus 단독(기밀)** | §5 게이트 |

## 4. 메커니즘

1. **모델 어댑터 레이어** `.claude/scripts/llm/ask_model.sh <provider> <prompt> <out>` — claude/codex/gemini/grok CLI를 정규화 I/O(`{content, provider, version, temp, prompt_hash}`)로 감싸 `_workspace/exchange/*.json`에 표준 스키마로 기록.
2. **Provenance**: `pipeline_manifest.py` 확장 — provider·정확 버전·temp=0·prompt_hash·input_sha·output_sha·**data_classification·redaction_level·policy_decision** 필수.
3. **Adjudication 순서**: ① 결정적(doc_lint score≥90 & Critical=0, citation 통과, dose exit 0) → ② 해석 충돌만 LLM-judge(작성과 **다른** 벤더 + goal_spec 루브릭) → ③ 미해결 시 **사람 게이트**. **용량·안전성 숫자는 LLM-judge 단독 금지.**

## 5. ★ 데이터 거버넌스 게이트 (4-모델 공통 최대 리스크)

기밀 FIH IB·용량 데이터를 OpenAI/Google/xAI로 fan-out하면 **v3에서 막은 IB least-privilege가 붕괴**한다.

- **데이터 분류**: `PUBLIC / REGULATORY_PUBLIC / SPONSOR_CONFIDENTIAL / SAFETY_CRITICAL`.
- **`ib_manifest.json` 확장**: `confidential: true`, `allowed_providers: ["anthropic"]`, `external_forbidden: true`.
- **Pre-spawn T0 게이트**: confidential/FIH-dosing 산출물이면 외부 호출 **즉시 차단**, Opus 강제. `draft_advisory_hook`·`/finalize`에서 재검증.
- **멀티-LLM 기본 대상 = 허가약물 연구(DDI/BE/FE/QTc)**. FIH는 공개 파생물(가이드라인·라벨)만 선택적 다중화.
- **Redaction**: 외부엔 *약물명+계열만*. NOAEL/노출마진/독성표 절대 금지. **Zero-Data-Retention(학습 미사용) Enterprise API만**. 조직 정책상 금지 시 **Opus 단독 옵션** 명시.

## 6. 패턴 · 재현성 · 비용

- **패턴**: Phase 9 = *cross-vendor 적대적 검증 + judge-panel*. 설계/synopsis = 경량 debate/ensemble. *맹목적 다수결은 낭비*(4-모델 공통).
- **재현성**: 정확 버전 pinning + temp=0 + 해시 기록. 프론티어 모델은 비결정적 → "기록하되 동일성 가정 금지", 결정적 critic이 재현성 백본.
- **비용/지연**: `/review`·핵심 연구·Critical/Major 섹션에만, 입력 SHA 캐시, 예산 바운드(Phase 9 루프와 동일).

## 7. 단계적 롤아웃

- **Phase A (즉시 추천)** — Phase 9 `qa-reviewer`를 **이종 critic 패널**(Opus+GPT+Gemini)로 전환. writer 경로 무변경, 허가약물 연구 한정. 어댑터 1개 + manifest 필드. 안전가치 최대·신규 표면 최소.
- **Phase B** — non-IB 연구(Phase 2) 2모델 병렬 + 설계/synopsis debate→판관.
- **Phase C** — 데이터 분류·redaction·egress T0 게이트 프로덕션화 후, 승인 벤더 한정 기밀 워크플로우에 전면 적용. grok 어댑터·SECURITY.md 데이터 거버넌스 절 추가.

## 8. 결론

- **#1 권고**: 멀티-LLM을 *작성기가 아니라* **Phase 8–9 독립 안전·규제 검증 레이어(이종 교차검증)**로 도입.
- **#1 리스크**: 기밀 FIH 용량 근거의 다수 벤더 확산 → **데이터 분류·egress T0 게이트를 어떤 멀티-LLM보다 먼저** 구축.
- **부가 리스크**: "consensus theater" → 동일 프롬프트 복제 대신 *역할·관점을 다르게* 부여, 결정적 앵커 유지.

## 9. 사용자 LLM 환경별 — 벤더 중립 조합 (4-모델 자문 반영, PoC 구현됨)

> 2차 4-모델 자문(2026-06-15)에서 **"호스트=작성자=판관" 고정은 벤더 락인**이라는 만장일치 교정. 이 플러그인은 Codex/Gemini CLI에서도 호스팅될 수 있으므로 Claude 중심 설계는 폐기. 아래는 PoC로 구현·테스트 완료(`scripts/llm/`, 126 tests green).

### 9.1 원칙 — 호스트 중립 + 데이터 우선 + 호스트는 제안만
- **역할을 능력으로 정의**: `authoring / regulatory_cross_check / citation_integrity / biostat_adversarial / judge_synth`. authoring 기본=**HOST**(egress·context 단편화 최소화), 나머지는 best‑available에 배정, judge는 작성 벤더와 다름.
- **강점은 코드가 아니라 DATA**: `references/llm/model_profiles.json`(역할별 `capability_scores` 0–10, `as_of`). 모델 진화 시 데이터만 갱신. `as_of`가 오래되면 호스트가 최신 지식으로 재검토(경고).
- **호스트는 제안만, 결정은 결정적 스크립트**: `route_select.py`가 `health.json`×scores로 재현적 배정 → 사용자 T2 확정.

### 9.2 라이브 헬스체크 (존재 확인 ❌ → 실제 동작 ✅) — 재실행 커맨드
- **`/llm-health`** + `scripts/llm/health_check.py`: 각 CLI에 nonce+산술 JSON 요구 probe(temp=0, timeout) → `_workspace/llm/health.json`(`ok|auth_fail|timeout|missing`). 세션 중 로그인 풀림 → 재실행으로 라우팅 갱신, 실패 provider 자동 폴딩(공석이면 host‑solo, 중단 없음).

### 9.3 벤더 중립 역할 → 모델 (최신 능력 기준)

| 역할 | 1순위 | 비고 |
|------|------|------|
| authoring | **HOST**(기본) | 비기밀 시 더 강한 모델로 override 가능 |
| regulatory_cross_check | **Gemini** | 대용량 가이드라인·MFDS sweep |
| citation_integrity | **`citation_verify.py`(결정적)** → Gemini | LLM은 보조 |
| biostat_adversarial | **Grok** ★ | 정량 반박·red‑team (Grok 1순위 승격) |
| judge_synth | **비‑작성 벤더** (GPT 우선) | 작성 벤더와 동일 금지 |

호스트별 예: **Codex 호스트** = Codex 작성/판정·Claude 규제·Gemini citation·Grok biostat / **Gemini 호스트** = Gemini 작성+citation·GPT 판정·Grok biostat·Claude 자가검토 / **Claude 호스트** = Claude 작성·GPT 규제/판정·Gemini citation·Grok biostat.

### 9.4 호스트 무관 Egress 게이트 (fail‑closed)
- `scripts/llm/egress_gate.py` + `references/llm/egress_policy.json`: 데이터 분류(`PUBLIC/REGULATORY_PUBLIC/SPONSOR_CONFIDENTIAL/SAFETY_CRITICAL`) → 허용 provider(`*`/`host`/literal). **벤더명 하드코딩 삭제**(Codex 호스트면 정책으로 교체). 모든 외부 호출은 **`ask_model.sh` 단일 게이트**를 통과 — native CLI 직접 호출 금지(우회 시 IB 유출 = v4 최대 실패 모드). 기밀/안전핵심은 host(또는 정책 allowed)만, FIH는 host‑solo.

### 9.5 호스트 중립의 현실 (이식 코어 vs 호스트 어댑터)
오케스트레이션(`skills/`·`commands/`·`hooks/`)은 Claude Code 전용 구문이다. 진짜 멀티‑호스트는 **이식 가능 코어**(persona MD + 결정적 Python + `references/llm/*.json` 데이터 + 라우팅 로직 — 이미 중립)와 **얇은 호스트 어댑터**(CC=skills, Codex=AGENTS.md, Gemini=GEMINI.md) 분리로 달성. 본 PoC의 `scripts/llm/*`·`references/llm/*`은 호스트 무관 코어다.

### 9.6 최대 리스크 (자문 만장일치)
① 어댑터 우회 native CLI로 IB 유출 → **egress 게이트·어댑터를 어떤 멀티‑LLM보다 먼저**(fail‑closed). ② 4 CLI 간 `_workspace` 경유 컨텍스트 단편화·토큰 중복 과금 → 기본 host‑작성 + 원문 대신 요약 전달. ③ stale 프로파일 → `as_of` + 호스트 재검토.

---

## 부록 — 자문 출처
- 신선 자문(2026-06-15): GPT(`codex exec` 0.139) · Gemini(`gemini -p` 0.46) · Grok(`grok -p` 0.2.51), read-only.
- 선행 설계: `docs/plugin_v3_advancement_proposal_ko.md`(v3 zero-trust/guardrail/loop), `CLAUDE.md`.
- OMC 레퍼런스: `omc ask`/`omc team codex|gemini`/`/ccg` (cross-vendor 오케스트레이션 프리미티브).
