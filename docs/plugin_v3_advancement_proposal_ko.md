# 플러그인 고도화 제안서 v3.0.0 — loop · goal · zero-trust · guardrail

> ✅ **구현 완료 (v3.0.0, 2026-06-14)** — 본 제안서의 제안 1·2·3이 모두 구현·머지되었다([CHANGELOG v3.0.0](../CHANGELOG.md), PR #2). 본 문서는 v3.0.0의 설계 근거로 유효하다.

| 항목 | 내용 |
|------|------|
| 대상 | `clinical-pharmacology-study-protocol-development` → **v3.0.0** |
| 작성일 | 2026-06-14 |
| 리뷰어 | **Claude**(코드 직접 정독) · **Codex 0.139**(레포 직접 read) · **Gemini 0.46**(레포 직접 read) |
| 선행 문서 | `docs/plugin_overview_3model_review_ko.md` (작동원리·프로세스·자료조사·페르소나·출처) |
| 결론(합의) | 이미 성숙한 harness 위에 **loop·goal·zero-trust·guardrail** 4축을 얹어, 환자안전·규제 적합성·재현성을 "절차/권고"가 아니라 **아키텍처로 강제**한다 |

> **리뷰 방식**: 세 모델로 현재 상태를 각각 독립 리뷰했고, "loop·goal·zero-trust·guardrail 네 축이 아직 절차·권고 수준에 머물러 있다"는 같은 진단에 도달했다. 본 문서는 그 위에서 "앞으로 어디로"를 정의하고, v3.0.0에서 제안 1·2·3을 모두 구현한다.

---

## 1. 현재 상태 진단 — 트렌드별 빈틈

| 트렌드 | v2.1.0에서 구현된 것 | 빈틈 |
|--------|---------------------|------|
| **Harness** | 8 페르소나 · 10단계 · 2 게이트 (성숙) | — (아래 세 축의 토대) |
| **Loop** | Phase 9 QA 후 "Critical 자동수정 **최대 1회**" 하드캡 | 수렴 조건 없음. 1회 후 Critical 잔존 시 그냥 보고. actor-critic·예산·plateau 감지 부재 |
| **Goal** | 체크리스트(Appendix B 16, 리뷰어 초점표), `doc_lint` | "절차 수행 여부"가 중심. 작성자가 최적화할 **기계 판독형 성공명세** 없음 |
| **Zero-trust** | "날조 금지", `[출처 미확인]`, NCT 자릿수 형식 검사 | 인용 PMID/NCT가 **실재·일치하는지 독립 검증 없음**. 외부 fetch 스냅샷 해시 없음. **IB(기밀)를 클라우드에 그대로 전송** |
| **Guardrail** | hook 1개 — **advisory(비차단)**, doc_lint 경고만 표면화 | 안전·규제 핵심 불변식에 대한 **차단형 가드레일 없음**. 도구 최소권한 없음 |

---

## 2. 제안 1 — Goal-spec 기반 Actor-Critic 수렴 루프 (Loop + Goal)

> **앵커: loop 엔지니어링 + goal-oriented.** 세 모델 모두 1순위.

### 무엇이 바뀌나
- **신규 `.claude/references/schemas/trial_goal_spec.schema.json`** + `goal_spec.example.json`: Phase 1/4에서 시험별 "성공 정의"를 기계 판독형으로 확정 — `primary_objective`, `estimand`(ICH E9 R1), `acceptable_ci_bounds`(80.00–125.00), `target_power`(≥0.8), `required_ich_sections`(B.1~B.16), `retention_years_min`(15), `pg_or_biobank_required`, `icf_readability_target`, `must_cite_types`. **goal_spec 자체를 게이트 승인 대상**으로 삼아 "잘못된 목표를 일관되게 최적화"하는 것을 방지.
- **`doc_lint.py` → 점수화 critic**: `score_file()`가 `{score 0–100, critical[], major[], minor[], passed}`를 결정적으로 산출. goal_spec을 주면 필수 섹션 누락·보존연한 미달을 critical로 추가.
- **오케스트레이터 Phase 9 재설계**: `max 1 revision` → 예산형 `iterate-until-convergence`:

```
protocol-writer(actor) ──► qa-reviewer + doc_lint score(critic) ──► score
        ▲ qa_fix_plan.md 먼저 작성 후 수정             │
        └──── 종료조건: Critical=0 & score≥90 ─────────┘
             또는 max_iterations 소진 / score plateau → 사람 에스컬레이션
   ※ Phase 7 승인 synopsis · design_decisions.md = 불변 입력(락)
```

### 왜 중요한가
용량근거·washout·ICF Part 4 반영 누락처럼 한 번 수정이 연쇄 오류를 부르는 항목을 실제 QA처럼 수렴. 품질 관리가 "초안 품질"이 아니라 **"수정 후 잔존 위험"**으로 바뀌고, 점수 궤적이 매니페스트에 남아 감사 추적이 "무엇을 만들었나 → 무엇을 만족했나"로 확장.

### 리스크/트레이드오프
① 토큰·시간 증가 → 하드 예산 + plateau 감지. ② **Goodhart**(루브릭 과최적화) → critic 다양성 + Phase 7 사람 게이트 보존. ③ 루프 중 설계 합의 임의 변경 → synopsis immutable 락.

---

## 3. 제안 2 — Zero-Trust 근거·출처 검증 계층 (Zero-trust)

> **앵커: zero-trust.** "인용 번호가 있다 ≠ 근거가 맞다." Gemini=환자안전 직결, Codex=1순위 개선.

### 무엇이 바뀌나
- **신규 `.claude/scripts/qa/citation_verify.py`**: `01_references/**`, `01_research_report.md`, `03_protocol_draft.md`, `04_icf_draft.md`의 PMID/NCT/DailyMed setid/URL을 **PubMed efetch·ClinicalTrials.gov v2로 독립 재조회**(실재·일치) → `_workspace/verification/citation_audit.json`. 검증 실패 인용은 dose justification 등 load-bearing 용도에서 차단. **offline-graceful**(네트워크 실패는 `unverified-network`로 표시, 예외 미발생).
- **신규 `.claude/scripts/qa/source_snapshot.py`**: MFDS/DailyMed/openFDA/PharmGKB 응답을 **조회일·URL·콘텐츠 SHA-256으로 스냅샷** → 사이트 구조 변경에도 재현성 유지(Codex 핵심 지적: WebFetch 레시피 → provenance 고정).
- **수치 untrusted 취급**: MRSD·sample size를 산문 신뢰가 아니라 Python 스크립트로 독립 재계산 대조(제안 3의 dose-safety guard와 연결).
- **IB least-privilege**: `_workspace/00_input/ib_manifest.json`에 파일 해시·허용 섹션·비공개 플래그만 남기고, Phase 2에서 에이전트별 **필요한 IB 섹션만** 읽도록 규칙화. `SECURITY.md`에 데이터 취급 명문화.

### 왜 중요한가
**용량 환각은 자원자 안전에 직결되는 최고위험 실패**(Gemini). 독립 검증 + provenance가 규제 증거 무결성·재현성·IB 기밀성을 동시에 확보.

### 리스크/트레이드오프
외부 API 변동·rate limit·레이턴시 → 검증 실패는 "근거 불명"으로 **표시**하되 최종 차단은 문서 위험도별 정책으로 분리. 페이월/MFDS HTML 등은 graceful degradation.

---

## 4. 제안 3 — 계층형 가드레일 / 정책 엔진 (Guardrail)

> **앵커: guardrail.** advisory→enforcement 승격. zero-trust의 "verify-then-allow"를 실행 계층에서 강제.

### 무엇이 바뀌나
- **단일 advisory hook → 3-tier**:
  - **T0 (차단)**: 안전·규제 핵심 불변식만 block — 보존기간 <15년, **명시 시작/증량 용량 > 계산된 MRSD**, ICF 식별정보(PII) 유출, **최종화 시** Appendix B 섹션 누락, CI 경계 오류. (정밀도 위해 차단 집합은 작게 + allow-list: `[시험기관명]`처럼 의도된 placeholder는 예외.)
  - **T1 (권고)**: 기존 advisory 동작 — 표현·minor.
  - **T2 (사람 게이트 트리거)**.
- **신규 `.claude/scripts/qa/dose_safety_guard.py`**: 프로토콜 내 모든 시작/증량 용량이 `starting_dose_calculation.py` 산출 MRSD 이하임을 결정적 검증, 위반 시 block.
- **신규 `/finalize` 커맨드**: `doc_lint --strict`(+ goal_spec)를 **실제 생성 초안**에 적용 → T0 실패 문서의 "최종 승인" 차단. (기존 CI strict는 golden fixture에만 적용되었음.)
- **PreToolUse 최소권한 정책**: 에이전트별 allow/deny(예: writer는 외부 fetch 금지, 조사 에이전트는 protocol 파일 Write 금지) + 기밀 IB egress 가드.

### 왜 중요한가
현재 가드레일은 advisory라 모델이 무시 가능. 환자안전·규제 핵심 불변식은 하드 강제되어야 함.

### 리스크/트레이드오프
false positive로 정당한 편집 차단 위험 → 차단 집합을 **작고 고정밀**하게 유지하고 예외 명시. 과도한 가드레일이 제안 1 루프를 방해하지 않도록 T0 최소화.

---

## 5. 통합 그림 & 구현 순서

세 방향은 맞물린다 — goal_spec(1)이 critic 점수·가드레일 기준(3)을 정의하고, provenance(2)가 가드레일의 verify 입력이 된다.

```
goal_spec.json ──► critic 점수(루프, 1) ──► T0 가드레일(3)
       └────────► citation/provenance 검증(2) ──┘
```

**의존성 기반 최적 순서 (v3.0.0 구현 순서와 동일)**:
1. **goal_spec 스키마 + doc_lint 채점** (기준 정의 — 다른 모든 것의 입력)
2. **citation_verify + source_snapshot + IB least-privilege** (zero-trust — 가드레일 입력 제공)
3. **계층 가드레일 + dose-safety + /finalize** (1·2를 소비)
4. **Phase 9 actor-critic 수렴 루프** (가장 침습적 — 채점·가드레일 통합)
5. (가로지름) 전 에이전트 opus 전환 + 페르소나 v3 갱신

---

## 6. 한계 및 후속 (책임 경계)

- 본 시스템은 판단을 **구조화·가속·검증**할 뿐, 과학적·규제적 최종 책임은 임상약리 전문가에게 있다.
- citation_verify는 인용의 **실재·형식**을 검증하나, 과학적 해석의 타당성까지 보증하지 않는다.
- T0 가드레일은 의도적으로 좁다(고정밀 우선). 나머지는 T1 권고로 사람·루프가 처리한다.
- 후속 과제: WebFetch 레시피 → 공식 MCP/`data.go.kr` API 전환, estimand의 분석계획 자동 연결, 다국가(MFDS↔FDA↔EMA) 동시 적합성 매트릭스.

---

## 부록 — 리뷰 출처
- 신선 리뷰: Codex 0.139 / Gemini 0.46 (레포 직접 read, 2026-06-14)
- 코드 정독: `.claude/`(agents·skills·commands·hooks·scripts·references) + `CLAUDE.md`
- 선행 개요: `docs/plugin_overview_3model_review_ko.md`
- 저자 교과서 원고: `docs/manuscript_designing_clinical_pharmacology_studies_using_ai_textbook_ko.md`
