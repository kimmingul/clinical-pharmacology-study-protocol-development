# references/llm — Multi-LLM 라우팅 데이터 (v4, 벤더 중립)

LLM별 강점을 **코드가 아니라 데이터로** 둔다. 모델은 계속 진화하므로 이 파일들을 갱신하고 `as_of`를 올리면 라우팅이 자동으로 따라온다. provider 키: `anthropic | openai | google | xai`.

| 파일 | 역할 | 소비자 |
|------|------|--------|
| `model_profiles.json` | provider별 CLI·probe_cmd·`resolved_model`·역할별 `capability_scores`(0–10)·`as_of` | `health_check.py`, `route_select.py` |
| `combination_profiles.json` | 역할 목록·`host_default_role`·`phase_map`·subset presets | `route_select.py` |
| `egress_policy.json` | 데이터 분류 → 허용 provider(`*`/`host`/literal), 마커, `fail_closed` | `egress_gate.py`, `ask_model.sh` |

## 설계 원칙

- **호스트 중립**: "Claude=작성자=판관" 하드코딩 없음. authoring은 기본 host(데이터 egress·context 단편화 최소화), 나머지 역할은 능력 기반 best‑available에 배정. judge는 작성 벤더와 달라야 함.
- **데이터 우선**: 강점/약점은 `capability_scores`로만 표현. `route_select.py`가 `health.json`(실측 status=ok) × scores로 결정적 랭킹.
- **호스트는 제안만**: 최종 배정 결정은 결정적 스크립트(재현성·자기편향 방지). `as_of`가 `staleness_warn_days`보다 오래되면 호스트 LLM이 최신 지식으로 재검토하도록 경고.
- **fail‑closed egress**: 분류 불명/마커 모호 시 외부 전송 차단. 기밀(IB)·안전핵심(NOAEL/MRSD)은 host(또는 정책 allowed)만.

## 갱신 방법 (모델 진화 시)

1. `model_profiles.json`의 해당 provider `resolved_model`·`capability_scores` 수정.
2. `as_of`를 오늘로 갱신, `sources`에 근거 추가.
3. (선택) `route_select.py --today YYYY-MM-DD`로 새 배정 확인.

> 점수는 **상대 비교용**이며 절대 성능 지표가 아니다. 역할 정의(authoring/regulatory_cross_check/citation_integrity/biostat_adversarial/judge_synth)는 `combination_profiles.roles`와 일치해야 한다.
