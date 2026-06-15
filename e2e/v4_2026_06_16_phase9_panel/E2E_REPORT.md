# E2E — Phase 9 이종 critic 패널 라이브 실증 (v4)

| 항목 | 내용 |
|------|------|
| 일시 | 2026-06-16 |
| 목적 | Phase 9 수렴 루프에 **cross-vendor critic 패널** 실제 배선 검증 |
| 대상 | clopidogrel+omeprazole **허가약물 공개 DDI** 계획서(v3 수렴본) |
| 호스트 | anthropic / 외부 critic: google(Gemini)·xai(Grok) |
| 분류 | REGULATORY_PUBLIC 선언 → egress 허용(공개 약물) |

## 흐름
`/llm-health` → `route_select`(능력 기반 배정) → `review_panel.py plan` → `run_review_panel.sh`(→ `ask_model.sh` → egress 게이트 → 실제 CLI) → `synthesize`(결정적 우선, 다수결 ❌).

배정(host=anthropic): regulatory_cross_check=**google**, citation_integrity=**google**, biostat_adversarial=**xai**, authoring=anthropic(host, critic 없음), judge=openai.

## 라이브 critic 결과 (실제 호출)

| critic | verdict | findings | 대표 발견 |
|--------|---------|---------:|----------|
| **Gemini** regulatory_cross_check | fail | 7 | Critical: Omeprazole 투여 요법(기간·빈도) 누락 / Major: 시험책임자·실시기관 정보 누락 |
| **Gemini** citation_integrity | concerns | 4 | Major: 용량 근거와 기술된 용량 불일치 |
| **Grok** biostat_adversarial | fail | 15 | Critical: 표본수 산출 전무 / 1차목적 ↔ no-effect 동등성 **모순** / GMR=1.0 가정 시 실제 효과(≈0.55)에서 검정력≈0 / estimand-분석 미연결 |

**취합(review_synthesis.json)**: Critical 5 · Major 14 · Minor 7 · 3 sources · 0 conflicts. 출처 태깅(`google:…`, `xai:…`), 다수결 없음.

## 핵심 입증 — 이종 교차검증의 가치
**Grok(biostat)가 Gemini가 놓친 5개 Critical을 포착**하고, Gemini(regulatory)는 Grok이 다루지 않은 규제 누락을 잡았다. 동일 모델 자기검증으로는 얻기 어려운 상호 보완. 작성 벤더(anthropic)와 검증 벤더(google/xai) 분리로 echo-chamber 완화.

## 발견·수정된 결함 (드라이버 견고성)
1. **stdin 소비 버그**: `while read` 루프 내 CLI가 루프 stdin을 삼켜 첫 critic만 실행 → 항목 사전 수집 + `</dev/null` 격리로 수정(3/3 실행 확인).
2. **산문 래핑 JSON**: Grok이 JSON 앞에 설명 문장을 붙여 strict 파싱 실패 → `_extract_json`(산문 속 균형 JSON 추출) 추가로 **Grok의 5 Critical 회수**(이전엔 "unparseable" Minor로 강등될 뻔). 일부 CLI가 엄격 JSON 계약을 지키지 않는다는 실증.

## 그레이스풀/보안
- 호스트 역할(authoring)·미가용 provider는 critic 생략, host qa-reviewer가 대체.
- 모든 외부 호출은 `ask_model.sh` → egress 게이트 통과. 기밀/안전핵심 마커면 호스트 무관 차단.
- 단일-LLM 사용자(`multi_llm=false`)는 이 단계를 건너뛰어 **v3 동등**.

## 검증
- `pytest .claude/scripts/` → **142 passed** (129 + review_panel 13)
- `ruff check .claude/scripts/llm/` → clean
- 산출물: `_workspace/review/vendor_*.json`, `review_synthesis.json`, `llm/review_panel_plan.json`

## 후속 1·2 (결정적 합류 + 수렴 루프 피드백)
- **Followup 1 — 결정적 findings 합류**: `review_panel.py deterministic`가 doc_lint/citation_verify/dose_safety를 실행해 `deterministic_findings.json`을 만들고 synthesize에 **최우선**으로 합류(`run_review_panel.sh --draft`가 자동 호출).
- **Followup 2 — 수렴 루프 피드백**: `review_panel.py fixplan`이 `review_synthesis.json` → `qa_fix_plan.md`(Critical 5 + Major 14, 출처·권고 포함)를 렌더 → Phase 9 actor(protocol-writer) 다음 반복 입력으로 배선.
- **"결정적 우선·다수결 없음" 가치 실증**: Gemini citation critic이 보존기간을 "3년"이라 **잘못** 주장(Major)했으나, 결정적 doc_lint(15년 KGCP, 의약품등의 안전에 관한 규칙 별표 4)가 우선이므로 qa-reviewer/actor는 doc_lint를 채택한다 — 벤더 critic의 오판을 결정적 앵커가 방어.

## 결론
Phase 9 actor-critic 루프에 이종 벤더 critic 패널 + 결정적 합류 + fixplan 피드백이 **실제 GPT/Gemini/Grok 호출로 작동**함을 확인. 결정적 우선 + 출처 태깅 + 그레이스풀 폴딩 + egress fail-closed + 수렴 루프 연결까지 완성.
