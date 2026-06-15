# E2E v3 — Clopidogrel + Omeprazole DDI (수렴 루프 · 가드레일 실증)

| 항목 | 내용 |
|------|------|
| 일시 | 2026-06-15 |
| 시험 | Clopidogrel(victim, CYP2C19 기질) + Omeprazole(perpetrator, CYP2C19 저해), 2×2 crossover DDI |
| 목적 | v3.0.0 신규 machinery — **actor-critic 수렴 루프**와 **3-tier 가드레일 / zero-trust 검증**을 실제 산출물로 실증 |
| actor | 실제 opus `protocol-writer` 에이전트 |
| critic | 결정적 `doc_lint.py --score --goal-spec` |

> 본 E2E는 v3 신규 제어 계층의 실증이다. 의도적으로 결함을 시드한 초안(v0)에서 출발해
> 1회 actor 반복으로 수렴함을 보인다(전체 10-Phase 신규 작성은 `e2e/v2_*` 참조).

## 수렴 루프 — score 궤적

| 단계 | score | passed | critical | major | minor | 비고 |
|------|------:|:------:|:--------:|:-----:|:-----:|------|
| **iter 1 (critic)** | **10** | ✗ | 4 | 1 | 1 | B.14–16 누락, 보존 3년, CI 경계 누락, placeholder |
| **iter 1 (actor)** | — | — | — | — | — | opus protocol-writer가 `qa_fix_plan.md` 작성 후 수정 |
| **iter 2 (critic)** | **100** | ✓ | 0 | 0 | 0 | **수렴** (Critical=0 & score≥90) |

종료조건 `Critical==0 AND score≥90` 충족 → 1회 반복으로 수렴. 설계 결정(2×2 crossover,
clopidogrel 300mg 부하+75mg, omeprazole 80mg)은 불변 입력으로 보존됨.

## 가드레일 — T0 차단 → 통과

| 검사 | iter 1 (결함) | iter 2 (수정 후) |
|------|--------------|-----------------|
| 3-tier hook (PostToolUse) | **⛔ decision: block** (보존 3년 = T0) | (무출력 — clean) |
| `doc_lint --strict` | exit 1 (ERROR) | **exit 0** |
| `dose_safety_guard` (DDI) | `skipped` (MRSD 없음 — 오탐 없음) | `skipped` |
| `/finalize` T0 게이트 | 거부 | **전부 통과** |

- T0 차단은 **positively-wrong 불변식**(보존<15년)에만 발동 — 부분 초안의 섹션 누락은
  advisory(T1)로 처리되어 작성 중 오탐을 피함. 섹션 완전성은 `/finalize`에서 강제.

## Zero-trust 인용 검증 (독립 재조회)

| 인용 | 형식 | **온라인 재조회** | 판정 |
|------|:----:|:----------------:|------|
| PMID 19915222 | OK | **verified** (PubMed eutils) | 실재 확인 |
| NCT00352877 | OK | **not-found** (ClinicalTrials.gov v2) | **미해결 → load-bearing 사용 차단** |

→ "인용 번호가 형식상 올바르다 ≠ 실재한다"를 실증. 검증 계층이 비해결 인용을 자동 포착.
offline 형식검증은 항상 수행되고, online은 graceful(네트워크 실패 시 `unverified-network`).

## Provenance

`_workspace/pipeline_manifest.json`에 iter1 critic→actor→iter2 critic→finalize의 4개
phase가 score·critical 궤적과 함께 SHA-256·UTC로 기록됨. 인용 audit은
`_workspace/verification/citation_audit.json`.

## 결론

v3 제어 계층이 실제 DDI 산출물에서 의도대로 작동함을 확인:
**결함 초안 → critic 채점/차단 → actor 수정 → 수렴(100점) → 최종 게이트 통과**,
그리고 **zero-trust 검증이 비해결 인용을 포착**.
