# Clopidogrel × CYP2C19 — CPIC 권고 가이드라인

## 출처

| 항목 | 내용 |
|------|------|
| CPIC pair API | https://api.cpicpgx.org/v1/pair_view?drugname=eq.clopidogrel&genesymbol=eq.CYP2C19 |
| Guideline URL | https://www.clinpgx.org/guideline/PA166251443 |
| CPIC Level | **A** (최고 등급, 근거 강함) |
| ClinPGx Level | 1A |
| Pair ID | 110091 |
| Actionable PGx | Yes |
| Provisional | No |
| 조회일 | 2026-04-14 |
| 라이선스 | CC0 1.0 Public Domain |

## 가이드라인 원문 (발행 이력)

| 연도 | 저자 | 저널 | PMID | 주요 변경사항 |
|-----|------|------|------|------------|
| 2013 | Scott SA et al. | Clin Pharmacol Ther. 2013;94(3):317-23 | 23698643 | 최초 CPIC 가이드라인 발행; PM/IM에서 대체 항혈소판제 권고 |
| 2022 | Lee CR et al. | Clin Pharmacol Ther. 2022;112(5):959-67 | 35034351 | IM 권고 강도 강화; 비ACS/PCI 적응증 확대 (뇌졸중, NVI); RM 표현형 추가 |

## CPIC Level

**Level A**: CPIC이 가이드라인을 발행하였으며, 이 약물-유전자 쌍에 대한 충분한 근거가 존재하여 임상적 실행이 권고됨. 계획서에서 인용 가능한 최고 수준의 PGx 가이드라인.

## 표현형별 권고 (CPIC 2022, CPIC recommendation_view 확인)

| 표현형 | 임상 상황 | 권고 내용 | 권고 강도 |
|-------|---------|---------|---------|
| **PM** (Poor Metabolizer) | ACS/PCI | Avoid clopidogrel. Use prasugrel or ticagrelor if no contraindication | **Strong** |
| **PM** | Non-ACS/PCI (NVI 등) | Avoid clopidogrel if possible | Moderate |
| **IM** (Intermediate Metabolizer) | ACS/PCI | Avoid standard-dose clopidogrel. Use prasugrel or ticagrelor | **Strong** |
| **IM** | Non-ACS/PCI | No recommendation (근거 불충분) | No Rec. |
| **IM** | NVI (비판막성 심방세동 등) | Avoid standard-dose clopidogrel if possible | Moderate |
| **NM** (Normal Metabolizer) | 모든 적응증 | Use standard-dose clopidogrel (75 mg/일) | **Strong** |
| **RM** (Rapid Metabolizer) | ACS/PCI, NVI | Use standard-dose clopidogrel | Strong |
| **RM** | Non-ACS/PCI | No recommendation | No Rec. |
| **UM** (Ultrarapid Metabolizer) | ACS/PCI | Use standard-dose clopidogrel | Strong |
| **UM** | Non-ACS/PCI, NVI | No recommendation | No Rec. |
| **Indeterminate** | 모든 | No recommendation | No Rec. |

*NVI: Non-valvular atrial fibrillation and/or venous thromboembolism indication (CPIC 2022 추가)*

## Diplotype → Phenotype 매핑 (CPIC diplotype endpoint 확인)

| Diplotype | Phenotype | Activity | Priority |
|-----------|----------|----------|---------|
| *17/*17 | Ultrarapid Metabolizer (UM) | Increased | High Risk |
| *1/*17 | Rapid Metabolizer (RM) | Normal-Increased | High Risk |
| *1/*1 | Normal Metabolizer (NM) | Normal | Low Risk |
| *1/*2 | Intermediate Metabolizer (IM) | Normal-Decreased | High Risk |
| *1/*3 | Intermediate Metabolizer (IM) | Normal-Decreased | High Risk |
| *2/*17 | Intermediate Metabolizer (IM) | Decreased | High Risk |
| *2/*2 | Poor Metabolizer (PM) | None/Minimal | High Risk |
| *2/*3 | Poor Metabolizer (PM) | None/Minimal | High Risk |
| *3/*3 | Poor Metabolizer (PM) | None/Minimal | High Risk |

*한국인 주요 PM diplotype: *2/*2, *2/*3 (합산 ~5–7%), *3/*3 (~0.5%)*

## 본 시험 설계 적용

### 1. 선정 기준
```
포함 기준: CYP2C19 Normal Metabolizer (*1/*1) — 사전 유전형 검사로 확인
제외 기준: CYP2C19 Poor Metabolizer (*2/*2, *2/*3, *3/*3) 또는 
           Intermediate Metabolizer (*1/*2, *1/*3)
           (이유: PM/IM에서 clopidogrel 기저 PD 효과 이미 감소 → DDI 평가 혼란)
```

**CPIC 인용 근거**: "CPIC Level A 가이드라인(Lee CR et al., Clin Pharmacol Ther. 2022)에 따르면 CYP2C19 PM 및 IM에서 clopidogrel 항혈소판 효과가 유의미하게 감소한다. 본 시험에서는 CYP2C19 유전형이 DDI 평가의 교란 변수로 작용하지 않도록 NM 대상자만 선정한다."

### 2. 계획서 배경 인용
"한국인 CYP2C19 PM 비율은 ~15%로 백인(~2–3%)의 약 5–7배에 달하여, clopidogrel + omeprazole DDI의 임상적 의의가 한국 환자에서 특히 크다."

### 3. ICF Part 4 설명 문구 (PG 분석 동의)
"본 시험에서는 시험 등록 전 귀하의 혈액에서 CYP2C19 유전형 검사를 실시합니다. CYP2C19는 clopidogrel을 활성화하는 효소로, 국제 가이드라인(CPIC Level A, 2022)에 따르면 이 효소의 유전적 변이에 따라 clopidogrel 효과가 크게 달라질 수 있습니다. 유전형 검사 결과는 귀하의 시험 참여 적합성 판단에만 사용되며, 결과는 귀하에게 통보됩니다."

## 참고 문헌

- PMID: 35034351 — Lee CR et al. Clin Pharmacol Ther. 2022;112(5):959-967. (CPIC 2022 update)
- PMID: 23698643 — Scott SA et al. Clin Pharmacol Ther. 2013;94(3):317-323. (CPIC 2013 원본)
- CPIC Web: https://cpicpgx.org/guidelines/guideline-for-clopidogrel-and-cyp2c19/
- API 호출 결과 (2026-04-14):
  - pair_view: Level A, ClinPGx 1A, Pair ID 110091 — 성공
  - recommendation_view: 표현형별 권고 확인 — 성공
  - diplotype endpoint: *1/*1~*3/*3 매핑 확인 — 성공
  - PharmGKB clinicalAnnotation: [API 호출 실패 — HTTP 400, 공개 논문 기반 보완]
