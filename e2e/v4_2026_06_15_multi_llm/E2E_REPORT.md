# E2E v4 — Multi-LLM 라우팅·헬스체크·Egress 게이트 실증 (벤더 중립)

| 항목 | 내용 |
|------|------|
| 일시 | 2026-06-16 |
| 목적 | v4 PoC 실증 — **라이브 헬스체크**, **능력 기반 벤더 중립 라우팅**, **fail-closed egress 게이트** |
| 호스트 | anthropic (이 세션) — 단, 설계·코드는 호스트 무관 |
| 대상 | 4개 CLI 실제 호출: claude · codex(GPT) · gemini · grok |

## 1. 라이브 헬스체크 (`/llm-health`) — 존재 확인 ❌ → 실제 동작 ✅

`health_check.py`가 각 CLI에 nonce+산술 JSON 요구 프롬프트를 보내 **로그인/키 실동작**을 검증:

| provider | status | latency |
|----------|--------|---------|
| anthropic | **ok** | ~9.7s |
| openai (codex) | **ok** | ~6.5s |
| google (gemini) | **ok** | ~25.8s |
| xai (grok) | **ok** | ~10.0s |

> **발견·수정**: 초기 probe는 모든 provider에 프롬프트를 stdin으로 전달해 gemini/grok(`-p`는 프롬프트를 **인자**로 받음)이 `bad_output`으로 false-negative 처리됨. 호출 규약 수정(trailing `-`=stdin, else 인자) + "stdout에 유효 응답이면 stderr 노이즈·nonzero rc 무관하게 ok"(grok 대응)로 **4/4 ok** 달성. → 라이브 probe의 필요성 자체가 실증됨.

## 2. 능력 기반 벤더 중립 라우팅 (`route_select.py`)

host=anthropic, 4/4 ok 기준 결정적 산출:

| 역할 | 배정 | 근거 |
|------|------|------|
| authoring | **anthropic** (host) | egress·context 최소화 |
| regulatory_cross_check | **google** | 대용량 가이드라인 sweep |
| citation_integrity | **google** (+ `citation_verify.py` 결정적 우선) | 인용 무결성 |
| biostat_adversarial | **xai (Grok)** ★ | 정량 반박 — Grok 1순위 승격 |
| judge_synth | **openai** | 작성 벤더(anthropic)와 다름 |

→ "host=작성자=판관" 고정 폐기 확인. Grok이 1급 역할(biostat)에 배정됨.

## 3. Fail-closed Egress 게이트 (`egress_gate.py`, 호스트 무관)

| 입력 | 선언 | 분류 | 비-host(openai) |
|------|------|------|------|
| 마커 없는 일반 텍스트 | (없음) | SPONSOR_CONFIDENTIAL(기본) | **차단** (fail-closed) |
| 허가약물 공개 DDI | REGULATORY_PUBLIC | REGULATORY_PUBLIC | **허용** (exit 0) |
| "public … NOAEL 30mg/kg MRSD" | PUBLIC | **SAFETY_CRITICAL**(상향) | **차단** (exit 3) |
| FIH NOAEL/MRSD | (없음) | SAFETY_CRITICAL | **차단** |

→ **선언 floor + 마커는 상향만** 규칙: 호출자가 공개 연구를 명시 선언하면 cross-vendor 가능, 그러나 기밀/안전핵심 마커가 섞이면 선언을 무시하고 차단. 벤더명 하드코딩 없음(host/`*`/literal).

## 4. 검증
- `pytest .claude/scripts/` → **129 passed** (97 기존 + 32 신규)
- `ruff check .claude/scripts/llm/` → clean
- 산출물: `_workspace/llm/health.json`, `routing_plan.json`

## 결론
라이브 헬스체크 → 벤더 중립 능력 기반 라우팅 → fail-closed egress가 **실제 4개 CLI로 작동**함을 확인. 단일-LLM 사용자는 `multi_llm=false`로 v3 동등, 다중 보유자는 환경에 맞는 조합 자동 제안. 기밀 IB/안전핵심은 호스트가 누구든 외부 전송 차단.
