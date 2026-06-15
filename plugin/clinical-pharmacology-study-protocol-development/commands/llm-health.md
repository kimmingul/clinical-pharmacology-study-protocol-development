---
name: llm-health
description: "보유한 LLM CLI(claude/codex/gemini/grok)를 라이브 probe로 점검하고(로그인·API 키 실제 동작 확인), 능력 기반 최적 Multi-LLM 조합을 제안한다. 세션 중 로그인이 풀렸을 때 재실행하여 라우팅을 갱신한다. /llm-health 또는 LLM 점검, 모델 상태 확인, 멀티LLM 조합 요청 시 사용."
---

# /llm-health — LLM 가용성 점검 & 조합 제안 (v4)

보유 LLM을 **존재 확인이 아니라 실제 호출(live probe)**로 검증하고, 능력 기반으로 최적 Multi-LLM 조합을 **제안**한다(최종 선택은 사용자). 세션 중 키 만료 시 재실행하면 라우팅이 갱신된다.

> 인자: `$ARGUMENTS` — `--refresh`(강제 재검증), `--host <provider>`(호스트 provider 지정; 미지정 시 이 플러그인을 구동하는 환경 = `anthropic`). 보안 게이트는 끌 수 없다(§데이터 거버넌스).

## 절차

### Step 1 — 라이브 헬스체크
```bash
PY=${CLAUDE_PLUGIN_ROOT}/scripts/.venv/bin/python      # 없으면 python3
$PY ${CLAUDE_PLUGIN_ROOT}/scripts/llm/health_check.py --workspace _workspace
$PY -c "import json;d=json.load(open('_workspace/llm/health.json'));[print(f\"  {k}: {v['status']} ({v.get('resolved_model','?')}, {v.get('latency_ms','?')}ms)\") for k,v in d['providers'].items()]"
```
각 CLI에 nonce+산술 JSON을 요구하는 초경량 프롬프트를 보내 **단순 echo가 아닌 실제 동작**(로그인/키)을 확인한다. 결과: `_workspace/llm/health.json` (`status: ok|auth_fail|timeout|missing`).

### Step 2 — 능력 기반 라우팅 제안
```bash
HOST=${ARG_HOST:-anthropic}   # 이 플러그인을 구동하는 환경의 provider
$PY ${CLAUDE_PLUGIN_ROOT}/scripts/llm/route_select.py --host "$HOST" --workspace _workspace
$PY -c "import json;d=json.load(open('_workspace/llm/routing_plan.json'));print('multi_llm:',d['multi_llm'],'| host:',d['host'],'| available:',d['available']);[print(f\"  {r}: {p}\") for r,p in d['assignment'].items()];[print('  ⚠',n) for n in d['notes']]"
```
`route_select.py`가 `health.json`(status=ok만) × `model_profiles.json`(역할별 점수) × `combination_profiles.json` presets로 **결정적으로** 최적 배정을 산출한다(호스트 LLM은 설명/제안만, 결정은 스크립트 → 재현성·자기편향 방지). 산출: `_workspace/llm/routing_plan.json`.

### Step 3 — 사용자 확정 (T2 게이트)
- 제안된 `assignment`(authoring=host, regulatory/citation/biostat/judge=능력별 best-available)와 대안(`alternatives`)을 사용자에게 제시한다.
- 사용자가 멀티‑LLM 사용 여부(전체/Phase별)와 배정을 확정한다. 확정값은 `goal_spec.json`의 `multi_llm` 블록에 기록한다:
  ```json
  "multi_llm": { "enabled": true, "host": "anthropic", "phase_overrides": {"9": true, "2": false}, "assignment": {"...": "..."} }
  ```
- `stale_warning`이 뜨면(모델 프로파일 `as_of`가 오래됨) 호스트 LLM이 자신의 최신 지식으로 점수를 재검토하도록 안내한다.

### Step 4 — 외부 호출 규칙 (항상 적용)
- 모든 외부 모델 호출은 `${CLAUDE_PLUGIN_ROOT}/scripts/llm/ask_model.sh`를 통해서만 한다(직접 CLI 호출 금지). 어댑터가 `egress_gate.py`로 **데이터 분류 → 허용 provider**를 fail‑closed로 검사한다.
- **기밀(SPONSOR_CONFIDENTIAL)·안전핵심(SAFETY_CRITICAL: NOAEL/MRSD/IB 등)은 외부 fan‑out 차단** — 호스트(또는 정책 allowed_providers)만. FIH는 호스트 단독 유지.

## 재실행 (세션 중 로그인 풀림 대비)
`/llm-health --refresh`를 다시 실행하면 health.json·routing_plan.json이 갱신된다. Phase 9 critic spawn 직전 자동 재검증을 권장하며, 호출 실패(auth/timeout) 시 해당 provider는 즉시 제외되고 차순위로 폴딩된다(필수 역할 공석이면 host‑solo로 강등, 파이프라인 중단 없음).

## Gotchas
- **CLI 설치 ≠ 키 유효**: 반드시 live probe 결과(status=ok)만 사용한다.
- **단일‑LLM 사용자**: `available`가 host 하나면 `multi_llm=false` → v3와 동일하게 Multi‑Persona만 작동(동작 동등).
- **벤더 중립**: 호스트가 Codex/Gemini여도 동일 — authoring=host, 검증은 비‑host 이종 패널. `--host`로 지정.
