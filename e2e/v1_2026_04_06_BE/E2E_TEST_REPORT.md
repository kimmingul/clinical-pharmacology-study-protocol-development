# E2E 테스트 보고서

**시험 시나리오**: Amlodipine Besylate 5mg 정제 생물학적동등성(BE) 시험
**실행일**: 2026-04-14
**목적**: 재구성된 7-에이전트 하네스의 전체 파이프라인 검증

---

## 실행 결과 요약

| Phase | 기능 | 에이전트 | 모델 | 결과 |
|-------|------|---------|------|------|
| 1 | 입력 수집 | 메인 | — | trial_info.md 생성 |
| 2 | 병렬 자료 수집 | CP + REG | sonnet × 2 | 병렬 실행 성공, 검색 영역 분리 확인 |
| 3 | 자료 종합 + 사용자 검토 게이트 | 메인 | — | 통합 보고서 생성, 사용자 승인 |
| 4 | 대화형 설계 협의 | 메인 | — | 2×2 crossover, 공복, 72h 절단 AUC |
| 5 | 통계 설계 | STAT | sonnet | Sample size 4개 시나리오 계산 (Python 코드 실행) |
| 6 | Synopsis 생성 | 메인 | — | v1.1 (채혈 최적화, 절단 AUC 반영) |
| 7 | Synopsis 승인 (Hard Gate) | 사용자 | — | 승인 |
| 8 | Full Protocol | protocol-writer | opus | 1,011줄, 16개 섹션, ICH E6(R3) 구조 |
| 9 | 다중 에이전트 리뷰 | CP+REG+STAT → QA | sonnet×3 → opus | C:3, M:10, m:13 |

---

## 검증된 하네스 기능

### 정상 작동 확인
- [x] 시험 유형별 분기 (BE → 허가 약물 → IB 불필요)
- [x] 에이전트 병렬 실행 (Phase 2: CP+REG, Phase 9: 3명 리뷰어)
- [x] 검색 영역 분리 (CP: PK/PD/유사시험, REG: 가이드라인/라벨/ICD-10)
- [x] 사용자 검토 게이트 (Phase 3: 자료 조사 후, Phase 7: Synopsis 승인)
- [x] Synopsis Hard Gate (승인 없이 Protocol 진행 불가)
- [x] Sample size Python 코드 실행 (crossover_2x2_be.py)
- [x] 대화형 설계 협의 (사용자 피드백으로 채혈/절단 AUC 수정)
- [x] 다중 에이전트 리뷰 + QA 취합 (중복 제거, 심각도 조정, 상충 해결)
- [x] Clinician 조건부 불참 (건강인 대상 BE → 불참)

### E2E 중 발견된 개선 사항 → 하네스에 반영 완료
- [x] 채혈 시점을 Tmax/t½ 기반으로 정량적 산출 → clinical-pharmacologist, design command 업데이트
- [x] t½ > 24h 시 절단 AUC₀₋₇₂ₕ 검토 → clinical-pharmacologist, biostatistician, synopsis, protocol-drafting 업데이트
- [x] 휴약기를 ≥10×t½(max) 공식으로 산출 → clinical-pharmacologist, design command 업데이트

---

## QA 리뷰에서 발견된 계획서 주요 이슈

### Critical 3건
1. 절단 AUC MFDS 사전 협의를 "의무"로 격상 + 컨틴전시 계획 필요
2. 72시간 채혈이 MFDS 3×t½ 기준과 상충 → 절단 AUC 논리로 해결 필요
3. MFDS IND 승인 절차(약사법 제34조) 계획서 미기술

### 하네스 개선 시사점
- 규제 전문가가 IND 절차를 자동 포함하도록 protocol-drafting 스킬에 체크리스트 추가 필요
- 절단 AUC 적용 시 MFDS 채혈 기간 요건과의 조화 로직을 design command에 반영 필요

---

## 산출물 목록

```
e2e/_workspace/
├── 00_input/
│   ├── trial_info.md                 (523 bytes)
│   ├── design_decisions.md           (1.8 KB)
│   └── statistical_design.md         (5.2 KB)
├── 01_research_cp.md                 (11 KB)
├── 01_research_reg.md                (15 KB)
├── 01_research_report.md             (7.5 KB)
├── 02_synopsis.md                    (6.8 KB)
├── 03_protocol_draft.md              (~40 KB, 1011줄)
└── review/
    ├── review_clinical_pharmacologist.md
    ├── review_regulatory_expert.md
    ├── review_biostatistician.md
    └── qa_review_report.md
```
