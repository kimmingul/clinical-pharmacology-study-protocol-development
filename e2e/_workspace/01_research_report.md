# 임상시험 배경 조사 보고서
## Amlodipine Besylate 5mg 정제 생물학적동등성(BE) 시험

**작성일**: 2026-04-14
**시험 유형**: BA/BE (생물학적동등성)
**약물**: Amlodipine besylate 5mg 정제 (제네릭) vs Norvasc® (대조약)

> 이 보고서는 clinical-pharmacologist와 regulatory-expert의 개별 조사 결과를 통합한 것이다.
> 개별 보고서: `01_research_cp.md`, `01_research_reg.md`

---

## 1. 적응증 개요
*(출처: regulatory-expert)*

| 적응증 | ICD-10 코드 | 설명 |
|--------|-----------|------|
| 고혈압 | **I10** | 본태성(일차성) 고혈압 (Essential hypertension) |
| 협심증 | **I20** | 협심증 (I20.0 불안정형, I20.1 혈관연축성, I20.9 상세불명) |

Amlodipine은 고혈압 및 안정형/혈관연축성 협심증에 허가된 약물. BE 시험에서는 건강한 성인 대상이므로 ICD-10 코드는 시험약의 적응증 코드로 활용.

---

## 2. PK/PD 자료 요약
*(출처: clinical-pharmacologist)*

### 2.1 핵심 PK 파라미터

| 파라미터 | 값 | 출처 |
|----------|-----|------|
| Tmax | 6–12시간 (중앙값 ~8시간) | [Norvasc® Label, FDA, 2013] |
| Cmax (5mg, 공복) | ~3.9–4.0 ng/mL | [Wang et al., 2020, PMID: 32034814] |
| t½ | 30–50시간 (평균 ~40시간) | [Abernethy et al., 1993, PMID: 1534713] |
| 생체이용률 (F) | 64–90% | [Norvasc® Label, FDA, 2013] |
| 단백결합률 | ~93% | [Norvasc® Label, FDA, 2013] |
| Vd | 21 L/kg | [Abernethy et al., 1993, PMID: 1534713] |

### 2.2 대사 경로

- **주요 대사 효소**: CYP3A4 (주), CYP3A5 (부) [Nakamura et al., 2013, PMID: 24301608]
- **활성 대사체**: 없음 — 90%가 비활성 pyridine 유도체(M9)로 전환
- **First-pass 효과**: 없음 (다른 DHP CCB와 구별되는 특징)
- **식이 영향**: 없음

### 2.3 BCS 분류

- **보수적 분류**: BCS Class III (고용해성, 투과성 in vitro 불확실)
- **실질적 특성**: 인체 흡수율 ≥96%로 Class I에 가까움
- **BE 시험 적용**: 표준 2×2 교차 in vivo 시험 실시 (biowaiver 미적용)

### 2.4 PK 변동성 (Sample Size 핵심)

| 파라미터 | Intra-subject CV% | 출처 |
|----------|-------------------|------|
| AUC₀₋ₜ | 7.5–11.6% | [Wang et al., 2020, PMID: 32034814] |
| Cmax | 12.4–18% | 복수 문헌 |

- **고변동약물 해당 여부**: 비해당 (CV% < 30%)
- **Sample size 계산 기준**: Cmax 보수적 CV% = 18% 적용 권장

---

## 3. 유사 시험 분석
*(출처: clinical-pharmacologist)*

### 주요 시험

| NCT 번호 | 설계 | 대상자 수 | Washout | 결과 |
|----------|------|----------|---------|------|
| NCT02974439 | 무작위, 공개, 2×2 crossover | 24명/조건 | 15일 | 공복/식후 모두 BE 확인 |

- 대조약: Norvasc® 5mg
- 분석: LC-MS/MS, 비구획분석(NCA)
- 공복 조건에서 Cmax GMR 90% CI가 80-125% 이내

---

## 4. 규제 가이드라인 요약
*(출처: regulatory-expert)*

### 4.1 MFDS BE 가이드라인 핵심

| 항목 | 요건 |
|------|------|
| 설계 | 2×2 교차설계 (표준) |
| 대상자 | 건강한 성인, 최소 12명 (평가 가능) |
| 투여 조건 | 공복 10시간+, 240mL 물 |
| 평가변수 | AUC₀₋ₜ + Cmax (90% CI: 80–125% 동시 충족) |
| 채혈 기간 | 최소 3×t½ = 최소 96–120시간 |
| Washout | ≥5×t½ → 실용적 21일 이상 |
| 통계 | ln 변환 후 ANOVA, GMR + 90% CI |

[생물학적동등성시험 기준, 식품의약품안전처 고시]

### 4.2 FDA PSG (Product-Specific Guidance)

- 10mg 기준 시험 후 5mg biowaiver 허용 [PSG_019787, FDA CDER, October 2024]
- MFDS는 해당 강도(5mg) 직접 시험 요구 가능 → 식약처 요건 우선

### 4.3 MFDS vs FDA 차이점

| 항목 | MFDS | FDA |
|------|------|-----|
| 공복/식후 | 공복 우선, 식후 별도 | 통상 양쪽 권고 |
| 고변동약물 | 확장 한계 방식 | RSABE |
| 최소 대상자 | 12명 하한 | 통계적 근거만 |
| Biowaiver (5mg) | 식약처 별도 확인 | PSG상 허용 |

→ Amlodipine은 식이 영향 없고 CV 낮아, MFDS 기준 공복 단독 시험 충분.

---

## 5. 약물 라벨 정보
*(출처: regulatory-expert)*

- **대조약**: Norvasc® (Pfizer, NDA 019787)
- **용법용량**: 5mg 1일 1회 경구 (성인 표준 시작 용량)
- **허가 적응증**: 고혈압, 만성 안정형 협심증, 혈관연축성 협심증
- **국내**: 암로디핀베실산염 다수 제네릭 허가 (산도스, 동화 등)

---

## 6. MFDS 임상시험 승인현황
*(출처: regulatory-expert)*

- 국내 amlodipine besylate 제네릭 다수 등재 → 과거 BE 시험 다수 수행
- 통상 설계: 건강 남성 15–24명, 2×2 crossover, 공복, washout 21–28일
- 구체적 승인 번호/건수: 의약품안전나라 직접 확인 필요

[MFDS 승인현황 — 의약품안전나라 직접 접속 확인 권장]

---

## 7. 종합 고려사항

| 항목 | 권고 | 근거 |
|------|------|------|
| 설계 | 무작위, 공개, 단회, 2×2 crossover | MFDS 표준, 유사 시험 설계 |
| 투여 조건 | 공복 | 식이 영향 없음, MFDS 공복 우선 |
| Washout | 21일 | t½ ~40시간, 실용적 표준 |
| 채혈 | 0–144시간, 18개 시점 | t½ 기반, 흡수기 밀집 |
| 평가변수 | AUC₀₋ₜ, Cmax (1차); AUC₀₋∞, Tmax, t½ (2차) | MFDS BE 기준 |
| 동등성 한계 | 90% CI: 80.00–125.00% | 표준 BE 기준 |
| 대상자 수 | ~21명 (유효), ~26명 (등록, 20% 탈락) | CV% 18% 보수적 기준 |
| 대조약 | Norvasc® 5mg | 원개발사 오리지널 |
| 분석 | LC-MS/MS, NCA, ln-ANOVA | MFDS/FDA 표준 |

---

## 8. 참고 문헌 (통합)

1. [Abernethy DR et al., 1993, PMID: 1534713] — Amlodipine PK/PD
2. [Abernethy DR et al., 1989, PMID: 2977393] — Amlodipine PK in healthy volunteers
3. [Meredith PA, Elliott HL, 1992, PMID: 1532771] — Clinical pharmacokinetics of amlodipine
4. [Wang Y et al., 2020, PMID: 32034814] — BE study, Chinese volunteers
5. [Nakamura K et al., 2014, PMID: 24301608] — CYP3A4/5 metabolism
6. [Pyo J et al., 2020, PMC: PMC7216797] — CYP450 genotypes, Korean subjects
7. [Kim KA et al., 2007, PMID: 17213004] — S-amlodipine PK, Korean subjects
8. [Choi DH et al., 2009, PMID: 19446150] — 10mg BE, Chinese volunteers
9. [Norvasc® Label, FDA, NDA 019787, 2013]
10. [PSG_019787, FDA CDER, October 2024] — Amlodipine BE guidance
11. [생물학적동등성시험 기준, 식품의약품안전처 고시]
12. [ClinicalTrials.gov NCT02974439]
