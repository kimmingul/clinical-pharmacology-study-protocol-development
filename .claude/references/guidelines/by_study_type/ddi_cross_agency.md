# 약물상호작용(DDI) 시험 — MFDS vs FDA vs EMA 규제 비교

> MFDS가 기준(baseline)이며, FDA/EMA와의 차이점을 중심으로 비교한다.

---

## 핵심 차이 요약 (상위 5개)

| # | 항목 | MFDS (기준) | FDA | EMA | 실무 영향 |
|---|------|-----------|-----|-----|---------|
| 1 | PBPK 수용도 | 보조 근거로 제한적 수용; 단독 대체 불가 | 임상 시험 대체 또는 설계 최적화에 적극 활용; 사전 협의 권장 | 지지적 도구; 단독 의사결정 수단으로 제한적 | FDA에서는 PBPK로 임상 DDI 면제 가능; MFDS/EMA는 추가 임상 데이터 선호 |
| 2 | 혼합 억제/유도 효과 처리 | 개별 평가 또는 통합 PBPK (보조) | PBPK 모델 수용 (in vivo 시험 대체 가능) | **In vivo 임상 시험 필수** (PBPK 불충분) | EMA는 혼합 DDI에 더 보수적; MFDS는 중간 입장 |
| 3 | CYP R-value 트리거 기준 | R-value >1.02 (가역적 억제) | R1 = 1 + Imax,u/Ki,u ≥ 1.02 | R₁ = 1 + I/Ki,u ≥ 1.02 (동일하나 EMA는 비결합 농도 명시) | 수치상 동일하나 농도 지표(총 vs 비결합) 차이로 실제 판정이 달라질 수 있음 |
| 4 | BSEP 평가 | 별도 언급 없음 | 별도 요건 없음 | **BSEP 억제 평가 필수** (간독성 안전성 목적, EMA 전용) | EMA 허가 시 BSEP 데이터 추가 필요 |
| 5 | 대사체 DDI 평가 기준 | 명시 없음 | 순환 대사체 ≥ 모약물 25%이면 평가 | 모약물 AUC의 ≥25% **및** 총 순환 ≥10% (이중 기준) | EMA는 더 낮은 역치의 이중 기준 적용으로 추가 시험 필요 가능 |

---

## 상세 비교

### In Vitro 기준 — CYP 억제 (R-value 및 트리거)

| 항목 | MFDS (기준) | FDA | EMA |
|------|-----------|-----|-----|
| 평가 효소 (가역적 억제) | CYP1A2, 2B6, 2C8, 2C9, 2C19, 2D6, 3A4 (7종 필수) | 동일 7종 | 동일 7종 |
| 가역적 억제 트리거 | R-value >1.02 (= 1 + [I]/Ki >1.02) | R1 = 1 + Imax,u/Ki,u ≥ 1.02 | R₁ = 1 + I/Ki,u ≥ 1.02 |
| 장내 억제 트리거 | 별도 기준 준용 | R2 = 1 + Igut/Ki ≥ 11 (Igut = dose/250 mL) | R₁,gut = 1 + (Fabs×Dose/Ka×Vgut×Ki,u) ≥ 11 |
| TDI/MBI 트리거 | TDI 평가 필수; KI/kinact 기반 기준 초과 | AUCR 예측 ≥1.25 시 임상 권고 | R₂ = 1/(1+kinact,max×[I]/(KI+[I])/kdeg) ≥ 1.25 |
| 농도 지표 | 명시 없음 (총 농도 관행) | Imax,u (비결합형 권장) | **비결합 농도(Cmax,u) 기반 명시** |
| 시간의존적 억제(TDI) | 7종에 대해 TDI 평가 필수 | KI, kinact 측정 | kinact,max, KI 측정 |

### In Vitro 기준 — CYP 유도

| 항목 | MFDS (기준) | FDA | EMA |
|------|-----------|-----|-----|
| 평가 효소 | CYP1A2, 2B6, 3A4 (3종 필수) | CYP1A2, 2B6, 3A (주요) | CYP1A2, 2B6, 2C9, 2C19, 3A4 |
| 판정 방법 | AhR/PXR/CAR 활성화 여부 | mRNA 증가 ≥2배 또는 양성 대조 20% 이상 | mRNA 발현 증가 (선호); R₃ = 1/(1+d×Emax×C/(EC₅₀+C)) ≤ 0.8 |
| 트리거 기준 | 양성 → 임상 고려 | mRNA ≥2배 증가 또는 양성 대조 20% 이상 | R₃ ≤ 0.8 → 임상 필요 |
| 양성 대조약 | 관행적 사용 | CYP3A→Rifampin, CYP1A2→Omeprazole, CYP2B6→Phenobarbital | Rifampin (CYP3A4, 2C9, 2C19) |

### In Vitro 기준 — 수송체 (Cutoff)

| 수송체 | MFDS (기준) | FDA | EMA |
|--------|-----------|-----|-----|
| P-gp | 기질/억제제/유도제 평가 (필수) | 경구: Igut/IC₅₀ ≥10; 정맥: I₁/IC₅₀ ≥0.1 | 50×Cmax,u 농도 기준 R ≥1.25 |
| BCRP | 기질/억제제 평가 (필수) | 동일 P-gp 기준 | 동일 P-gp 기준 |
| OATP1B1 | 기질/억제제 평가 | R = 1 + Imax,u/IC₅₀ >1.1 | 25×Cmax,u 기준 R ≥1.25 |
| OATP1B3 | 기질/억제제 평가 | 동일 OATP1B1 기준 | 동일 |
| OAT1, OAT3 | 평가 권장 | Imax,u/IC₅₀ ≥0.1 | 신장 분비 ≥25%인 경우 필수 |
| OCT2 | 평가 권장 | Imax,u/IC₅₀ ≥0.1 | 신장 분비 ≥25%인 경우 필수 |
| MATE1, MATE2-K | 평가 권장 | Imax,u/IC₅₀ ≥0.1 (2020년 0.02→0.1로 상향) | 선택적 평가 (임상 관련성 있는 경우) |
| BSEP | 별도 언급 없음 | 별도 요건 없음 | **필수 평가 (EMA 전용; 간독성 목적)** |
| UGT | 명시 없음 | 기질 의사결정 체계 있음 | 억제 시험만 (기질 체계 없음) |

### 임상 DDI 설계

| 항목 | MFDS (기준) | FDA | EMA |
|------|-----------|-----|-----|
| 시험 원칙 | 전향적 전용 DDI 시험 원칙 | 전향적 DDI 시험 | 건강 성인 자원자, 교차 설계 우선 |
| 기본 설계 | 교차설계(crossover) 권장 | one-sequence 또는 two-period crossover | 교차 설계 우선; 개방 또는 맹검 모두 허용 |
| 억제제 전투여 기간 | 정상상태 도달 후 기질 투여 (통상 5~7일) | 동일 원칙 | t½의 5배 이상 세척 기간 |
| 유도제 전투여 기간 | 최소 7~14일 전투여 | 동일 원칙 | 유도 효과 소실 시까지 |
| 고정순서 설계 허용 | 반감기 긴 경우 허용 | 강력 억제제/유도제의 perpetrator 시 일반적 | 명시적 허용 |
| 3-arm 유도제 설계 | 명시 없음 | 별도 명시 없음 | **권고** (기질 단독/유도제+기질/유도제 중단 후 기질) |
| 대상자 집단 | 건강한 성인 자원자 원칙 | 동일 | 동일 |
| 환자 대상 | 건강인 불가/비윤리적 경우 허용 | 동일 | 동일 |

### GMR 해석 기준 및 No-Effect Boundary

| 항목 | MFDS (기준) | FDA | EMA |
|------|-----------|-----|-----|
| No-effect boundary | 90% CI **80.00%~125.00%** 이내 = 유의한 DDI 없음 | 90% CI **80.00%~125.00%** = 임상적으로 무의미 | GMR 0.50~2.0배 = 임상적으로 유의한 상호작용 경계 |
| NTI 기질 기준 | 더 좁은 범위 고려 | **90.00%~111.11%** 고려 | 더 엄격한 기준 적용 |
| 약한 억제 | 1.25 < GMR ≤ 2.0 | AUC 1.25~2배 증가 = weak inhibitor | AUC 1.25~2배 = 주의 모니터링 |
| 중등도 억제 | 2.0 < GMR ≤ 5.0 | AUC 2~5배 = moderate inhibitor | AUC 2~5배 = 병용 주의/용량 조정 |
| 강한 억제 | GMR >5.0 | AUC ≥5배 = strong inhibitor | AUC >5배 = 병용 금기 고려 |
| 약한 유도 | 0.50 ≤ GMR <0.80 | AUC 20~50% 감소 = weak inducer | AUC >50% 감소 = 주의 |
| 강한 유도 | GMR <0.20 | AUC ≥80% 감소 = strong inducer | 동일 개념 적용 |

### Index Substrate 선정

| CYP/수송체 | MFDS (기준) | FDA | EMA |
|-----------|-----------|-----|-----|
| CYP3A | Midazolam (통상) | Midazolam, Buspirone | Midazolam i.v.+p.o. (장/간 분리), Felodipine |
| CYP2C9 | Warfarin, Tolbutamide | Warfarin (S-), Tolbutamide | Warfarin, Tolbutamide |
| CYP2C19 | Omeprazole | Omeprazole, Lansoprazole | Omeprazole, Lansoprazole |
| CYP2D6 | Desipramine, Dextromethorphan | Desipramine, Dextromethorphan | Desipramine, Metoprolol |
| CYP1A2 | Caffeine | Caffeine, Tizanidine | Caffeine, Theophylline |
| CYP2B6 | Bupropion | Bupropion | Efavirenz, Bupropion |
| OATP1B1/3 | Rosuvastatin | Rosuvastatin, Atorvastatin | Rosuvastatin, Pravastatin |
| P-gp | Digoxin | Digoxin, Dabigatran etexilate | Digoxin, Dabigatran |
| OCT2/MATE | Metformin | Metformin | Metformin |

### PBPK 활용 범위

| 항목 | MFDS (기준) | FDA | EMA |
|------|-----------|-----|-----|
| 임상 DDI 면제 근거 | 보조 근거로 제한적 수용; 단독 대체 불가 | **임상 시험 대체 허용** (사전 FDA 협의 권장) | 충분한 검증 시 수용하나 단독 근거로 더 엄격 |
| 혼합 억제/유도 | 통합 PBPK (보조) | PBPK 모델 수용 | **In vivo 시험 필수** |
| 특수 집단 외삽 | 활용 가능 | 활용 가능 | 활용 가능 |
| 보고 요건 | 명시 없음 | "PBPK Format and Content" 가이드 | 모델 구조/가정/검증 데이터 명시 필요 |
| Sensitive substrate AUC 분류 | FDA/EMA 기준 준용 | ≥5배: strong; 2~5배: moderate; 1.25~2배: weak | 동일 개념 |

### 통계 분석

| 항목 | MFDS (기준) | FDA | EMA |
|------|-----------|-----|-----|
| 교차설계 DDI | ANOVA (BE와 동일 모형); ln 변환; GMR 및 90% CI | 동일 | 동일 |
| 고정순서 DDI | Paired t-test (ln 변환) 또는 ANOVA; GMR 및 90% CI | 동일 | 동일 |
| 1차 평가변수 | AUC₀₋∞ (AUC₀₋ₜ 보조) | AUC₀₋∞ | AUC ratio (±상호작용) |
| 2차 평가변수 | Cmax | Cmax | Cmax ratio |
| 시각화 | Forest plot, fold-change scatter plot | 동일 | 동일 |

---

## 프로토콜 작성 시 주의사항

1. **In vitro 수송체 평가 순서**: MFDS는 P-gp, BCRP, OATP1B1/3, OAT1/3, OCT2, MATE1/2-K를 모두 평가 권장하며, EMA는 추가로 **BSEP** 평가를 요구한다. 다국가 허가 시 BSEP 데이터를 처음부터 포함한다.

2. **농도 지표 선택**: FDA와 EMA 모두 비결합(unbound) 농도 기반 트리거를 명시하는 반면, MFDS는 이를 명확히 규정하지 않는다. 다국가 제출 시 총 농도와 비결합 농도 모두 산출하여 제시한다.

3. **혼합 억제/유도 DDI**: EMA는 억제와 유도가 동시에 예상되는 경우 PBPK 만으로 불충분하여 in vivo 임상 시험을 요구한다. FDA는 PBPK 모델로 대체 가능하다. 유럽 허가를 목표로 하면 별도 임상 시험을 계획한다.

4. **No-effect 기준의 차이**: MFDS와 FDA는 90% CI 80~125%를 명시적 no-effect 기준으로 사용하나, EMA는 더 서술적 접근으로 임상적 유의성을 판단한다. NTI 기질(Digoxin, Warfarin 등)은 모든 기관에서 더 좁은 기준을 적용하므로 별도로 명시한다.

5. **PBPK 활용 전략**: MFDS 제출 시 PBPK는 보조 자료로 제출하고, 임상 DDI 시험 면제를 위해서는 FDA의 사전 협의 절차(Pre-IND meeting)를 활용하는 것이 효율적이다.

6. **대사체 DDI**: EMA의 이중 기준(≥25% 또는 ≥10%)으로 인해 FDA 기준(≥25% 단일)보다 더 많은 대사체에 대한 DDI 평가가 요구될 수 있다. 다국가 허가 시 EMA 기준을 기본으로 설계한다.

---

## 참고 가이드라인

| 기관 | 주요 가이드라인 |
|------|--------------|
| MFDS | 의약품의 약물상호작용 평가 가이드라인 (식약처 민원인 안내서) |
| FDA | In Vitro Drug Interaction Studies (2020); Clinical Drug Interaction Studies (2020) |
| EMA | Guideline on the Investigation of Drug Interactions (CPMP/EWP/560/95/Rev. 1, 2012) |
| ICH | M12 Drug Interaction Studies (2024, Step 5) |
