> 🗄️ **[ARCHIVED — v2.0.0 기준, 2026-05-22]** 지적사항 대부분은 v3.0.0에서 해결되었다. 현행 상태는 `CHANGELOG.md`·`docs/plugin_v3_advancement_proposal_ko.md` 참조. 히스토리 보존용.

# 3-Model 협력 리뷰 종합 보고서 — clinical-pharmacology-study-protocol-development

**Date**: 2026-05-22
**Project version**: v2.0.0 (Claude Code plugin marketplace 배포 구조)
**Reviewers**:
- **Claude Opus 4.7** (`claude_harness_report.md`) — 에이전트 정의·스킬·워크플로우 정합성
- **Codex CLI 0.133.0 (GPT-5)** (`codex_report.md`) — Python 스크립트 통계 정확성·재현성
- **Gemini 2.x (0.43.0)** (`gemini_report.md`) — 외부 사용자 관점 문서·UX·플러그인 배포

---

## TL;DR

| 등급 | 건수 | 대표 발견 |
|------|------|-----------|
| **Critical** | 2 | (1) `crossover_2x2_be.py` N 2배 과대 산출, (2) `clinical-research/SKILL.md:596`의 clinician 참여 정책 모순 |
| **Major** | 7 | RSABE 부정확, ICH E6(R3) Appendix B 16개 섹션과 protocol-drafting 구조 불일치, Phase 2 소프트 데드락, Reference 가드레일 부재, Williams 6×3 joint power 미산출, Hard Gate sentinel 부재, sync_plugin.sh 수동 의존 |
| **Minor** | 9 | scipy lock 부재, 테스트 부재, FIH 입력 검증 부재, README quickstart 약함, Disclaimer 미강조, TODO §2 (TS BE/FE 옵트인), QTc 책임자 회색지대, `regulatory-review` 명명 혼란, 등 |

---

## 1. Critical 결함 (즉시 수정 권고)

### C1. BE/DDI 2×2 crossover 표본수 **2배 과대 산출** [Codex]

**위치**: `.claude/scripts/sample_size/crossover_2x2_be.py:104-110`, `crossover_2x2_ddi.py` (동일 구조 추정)

**문제**: 표준 공식
```
N_total = ⌈(z_α + z_β)² · 2 · σ_w² / margin²⌉
```
를 코드는 `n_per_seq`로 명명한 뒤 다시 `n_total = 2 × n_per_seq` 처리.

**검증** (CV=25%, GMR=0.95, power=0.80, α=0.05):
- 표준 답: N_total=26, n/seq=13
- 코드 출력: n_per_seq=26, n_total=52

**오염 범위**: `e2e/v1_2026_04_06_BE/_workspace/00_input/statistical_design.md:40-42`에 잘못된 공식 그대로 인용. v1 BE protocol draft는 수동 보정(36명)으로 우회되었으나 산식 자체가 commit되어 향후 자동 산출 시 100% 재발.

**조치**:
```python
# Before
n_per_seq = math.ceil((z_alpha + z_beta) ** 2 * 2.0 * sigma_w ** 2 / margin ** 2)
n_total = 2 * n_per_seq

# After
n_total = math.ceil((z_alpha + z_beta) ** 2 * 2.0 * sigma_w ** 2 / margin ** 2)
if n_total % 2 == 1:
    n_total += 1  # 두 sequence 짝수 분배
n_per_seq = n_total // 2
```

회귀 fixture로 PowerTOST `sampleN.TOST(CV=0.25, theta0=0.95, targetpower=0.80)` = 28 (TOST t-기반) 또는 normal 근사 26과 비교.

### C2. `clinician 참여 정책` 모순 [Claude]

**위치**: `.claude/skills/clinical-research/SKILL.md:596`

**문제**: 한 곳의 Gotcha 항목이 "DDI/BE/FE에서 clinician 불참" 으로 명시되어 있으나, 다른 7곳 (`clinician.md:3,10`, `trial-doc-orchestrator/SKILL.md:35,451`, `commands/research.md`, `commands/review.md:88`, `clinical-research/SKILL.md:28-29`)이 모두 **"clinician 항상 참여"** 명시. CLAUDE.md, README.md 표도 "항상".

**영향**: 서브에이전트가 Read로 SKILL.md를 로드할 때 596줄을 우선 신뢰하면 BE/DDI/FE 시험에서 안전성 전담자 누락 → 선정/제외 기준 미흡, 안전성 모니터링 정책 누락.

**조치**: 1줄 삭제 또는 정정. PR 한 번으로 처리 가능.

---

## 2. Major 결함

### M1. ICH E6(R3) Appendix B 16개 섹션과 protocol-drafting 구조 불일치 [Claude]

- `.claude/skills/protocol-drafting/SKILL.md:39-56`의 "필수 16개 섹션"이 ICH 원문 B.1–B.16과 1:1 매핑 안 됨
- B.6 Discontinuation, B.11 Direct Access, B.15 Financing, B.16 Publication policy가 별도 섹션으로 분리되어 있지 않음
- `regulatory-review/SKILL.md:67-84` (리뷰어 체크리스트)는 ICH 원문과 정확히 일치 → **작성자 vs 리뷰어 구조 mismatch** → QA에서 Critical 지적 빈발 위험

**조치**: protocol-drafting SKILL.md의 16개 섹션 정의를 Appendix B (`ich/e6_r3_full/07_appendix_b_protocol.md`) 명칭과 1:1 정렬.

### M2. RSABE 부정확 [Codex]

`replicate_crossover_be.py`가 `theta_scaled = regulatory_constant × σ_w` 단순 근사. FDA RSABE 공식 판정식(linearized criterion + upper 95% bound) 미구현. HVD(highly variable drug) 시험에 사용 시 규제 부적합.

### M3. Phase 2 병렬 호출의 소프트 데드락 [Claude]

`translational-scientist`는 `regulatory-expert`의 라벨 PG 섹션 추출 결과에 의존하나, Phase 2에서 두 에이전트가 동시 실행됨 → TS 실행 시점에 라벨 파일 미완성. 운 좋게 동작하는 경우가 많지만 race condition 잠재.

**조치**: trial-doc-orchestrator/SKILL.md Phase 2에 dependency edge를 명시 (regulatory-expert 완료 → TS 시작) 또는 TS가 라벨 PG 영역도 독립 수집하도록 정책 정리.

### M4. Reference 의무화 가드레일 부재 [Claude]

CLAUDE.md는 "모든 조사 자료에 reference 필수" 명시. 그러나 4개 에이전트(`clinician`, `biostatistician`, `protocol-writer`, `icf-writer`)의 정의 파일에 reference 정책 명시 없음. CP/TS/REG에는 있음.

**영향**: 안전성·통계·작성 산출물의 인용 누락 가능. QA가 잡지 못하면 통과.

### M5. Williams 6×3 joint power 미산출 [Codex]

양방향 DDI 시험에서 IUT α 조정 불필요는 맞으나, joint power(둘 다 BE 입증) ≈ power_AB × power_BA. 코드는 단방향 80%만 보고 → 사용자가 양방향 결론을 가설로 채택했다면 실제 joint power 64% 수준.

### M6. Synopsis Hard Gate sentinel 부재 [Claude]

Phase 7 Hard Gate가 자연어 응답("승인")에만 의존. 명시적 sentinel 파일(`.synopsis_approved`)이나 metadata 없음 → 부분 재실행 시 하류(`protocol`, `review`, `icf`) 산출물의 stale 상태 검출 불가.

### M7. `sync_plugin.sh` 수동 의존 + 경로 치환 누락 위험 [Gemini]

`.claude/` (개발) → `plugin/.../` (배포)의 sync가 수동 스크립트. 개발자가 동기화 누락 시 plugin zip이 stale. v2.0.0 marketplace로 배포된 zip이 최신 fix를 반영하지 못할 위험.

**조치**: pre-commit hook 또는 GitHub Actions에서 `sync_plugin.sh` 자동 실행 + diff 검사.

---

## 3. Minor / 정책 권고

| # | 영역 | 발견 | 출처 |
|---|------|------|------|
| m1 | 재현성 | `pyproject.toml`/lockfile 부재, scipy 강결합 | Codex |
| m2 | 회귀 방지 | `tests/` 디렉토리 부재 | Codex |
| m3 | 견고성 | FIH 스크립트 입력 양수 검증 부재 | Codex |
| m4 | 온보딩 | README 674줄, 5분 요약 부족 | Gemini |
| m5 | 컴플라이언스 | IRB/AI-generated content Disclaimer 최상단 강조 부족 | Gemini |
| m6 | 사용성 | Quickstart 입력 템플릿 부재 (TRIAL_INFO_INPUT.md 노출 권장) | Gemini |
| m7 | 정책 | TODO §2 — TS의 BE/FE 옵트인 (NTI 약물) | TODO/Gemini |
| m8 | 책임 경계 | QTc 시험의 ECG 통합 책임자 회색지대 (CP↔TS) | Claude |
| m9 | 명명 | `regulatory-review` 스킬명이 실제 범위(통계·임상·중개) 과소 표현 | TODO §6 |

---

## 4. 권고 액션 플랜 (우선순위 + 추정 공수)

### Phase A: Critical 패치 (이번 주, ~4시간)

1. **C1**: `crossover_2x2_be.py` + `crossover_2x2_ddi.py` 표본수 공식 수정 → 회귀 fixture로 PowerTOST 결과 ±2 이내 확인
2. **C2**: `clinical-research/SKILL.md:596`의 clinician 불참 문구 삭제
3. v1 BE statistical_design.md의 잘못된 공식 인용 정정 또는 ERRATUM 첨부
4. `sync_plugin.sh` 실행 → plugin zip 재빌드 (zip 안의 코드도 동일 결함 보유 확인 필요)

### Phase B: Major 처리 (2주 내, ~2-3일)

5. **M1**: protocol-drafting/SKILL.md 16개 섹션을 Appendix B 명칭과 1:1 매핑
6. **M2**: RSABE FDA 판정식 재구현 (PowerTOST source 참조)
7. **M3**: Phase 2 dependency edge 명시 (regulatory-expert → translational-scientist)
8. **M4**: 4개 에이전트(clinician, biostat, protocol-writer, icf-writer)에 reference 정책 추가
9. **M5**: Williams 6×3 joint power 출력
10. **M6**: `.workspace/.synopsis_approved` sentinel 파일 정책 + 부분 재실행 시 stale 검사
11. **M7**: pre-commit hook으로 `sync_plugin.sh` 자동화

### Phase C: 인프라·UX (한 달 내)

12. `tests/` + pytest CI (Codex 회귀 fixture 포함)
13. `pyproject.toml` + lockfile
14. README 상단 "5분 요약 + Quickstart" 박스
15. IRB/AI Disclaimer 강조 박스
16. TODO §2 (TS BE/FE 옵트인) 정책 결정 — NTI 약물 리스트 기반 또는 사용자 명시 트리거

---

## 5. 협력 모델 간 일치도

| 영역 | Claude | Codex | Gemini |
|------|--------|-------|--------|
| 통계 코드 결함 | (범위 외) | **C1, M2, M5 발견** | (범위 외) |
| 에이전트 정합성 | **C2, M1, M3, M4, M6** | (범위 외) | 보조 확인 |
| 외부 UX·문서 | 보조 확인 | (범위 외) | **m4-m7** |
| TODO §2 (TS) | 보조 확인 | (범위 외) | 보조 확인 (TOP 5에 포함) |
| sync_plugin.sh | (언급 안 함) | (범위 외) | **M7** |

세 모델의 영역이 거의 겹치지 않으며 보완적 — 한 모델로는 Critical 2개 중 어느 하나도 발견 못 했을 가능성. 협력 패턴이 효과적이었음.

---

## 보고서 파일

- `claude_harness_report.md` (Claude Opus, 265 lines, 27 KB)
- `codex_report.md` (Codex GPT-5, 본 문서에서 재구성)
- `gemini_report.md` (Gemini 0.43, 44 lines)
- `SYNTHESIS.md` (본 파일, 통합)

원본 trace:
- Codex stdout: `/tmp/codex_run.log` (3527 lines)
- Gemini stdout: `/tmp/gemini_run.log` (18 lines, tool 호출 실패 흔적 포함)
