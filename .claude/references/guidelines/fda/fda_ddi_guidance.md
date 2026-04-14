# In Vitro Drug Interaction Studies & Clinical Drug Interaction Studies (2020)

## 메타 정보

| 항목 | 내용 |
|------|------|
| 발행 기관 | FDA CDER |
| 문서명 (In Vitro) | In Vitro Drug Interaction Studies — Cytochrome P450 Enzyme- and Transporter-Mediated Drug Interactions |
| 문서명 (Clinical) | Clinical Drug Interaction Studies — Cytochrome P450 Enzyme- and Transporter-Mediated Drug Interactions |
| 발행일 | 2020-01 (Final) |
| 원문 URL (In Vitro) | https://www.fda.gov/media/135587/download |
| 원문 URL (Clinical) | https://www.fda.gov/media/135588/download |
| 연방관보 공지 | https://www.federalregister.gov/documents/2020/01/23/2020-01064 |
| 마지막 검증일 | 2026-04-13 |

> **주의:** 원문 PDF 직접 접근 제한으로 공개된 FDA 자료 및 관련 학술 문헌을 통해 재구성하였음. 정확한 수치는 원문 확인 요망.

---

## 적용 범위

- **In Vitro 가이드:** CYP 효소 및 수송체 매개 약물상호작용 가능성의 체외 평가 방법 및 임상 시험 필요 여부 판단
- **Clinical 가이드:** 임상 DDI 시험의 시기, 설계, 결과 해석, 라벨 기재 권고
- 신약(NDA), 생물의약품(BLA), 보완 신청에 적용
- CYP 억제/유도 및 수송체(P-gp, BCRP, OATP, OCT, OAT, MATE) 기반 DDI 평가

---

## Part 1: In Vitro 스크리닝 기준

### 1.1 CYP 억제 평가

#### 가역적 억제 (Reversible Inhibition)
- **평가 효소:** CYP1A2, CYP2B6, CYP2C8, CYP2C9, CYP2C19, CYP2D6, CYP3A (장 및 간)
- **실험 방법:** 인간 간 마이크로솜(HLM) 또는 재조합 CYP 효소 사용
- **Ki 대신 IC50/2 사용 허용:** 탐색 기질(probe substrate) 농도 = 효소의 Km 값인 경우
- **유리형(unbound) 값 사용:** Ki,u 및 KI,u 사용 권장

#### 임상 시험 트리거 기준 (가역적 억제)
| 기준 | 수식 | 임상 시험 권고 |
|------|------|----------------|
| Basic R1 | R1 = 1 + (Imax,u / Ki,u) ≥ 1.02 | 임상 DDI 시험 수행 |
| R2 (장관) | R2 = 1 + (Igut / Ki) ≥ 11 | 장내 CYP3A 억제 고려 |

여기서:
- Imax,u: 최고 비결합형 혈장 농도
- Ki,u: 비결합형 억제 상수
- Igut: 장내 추정 농도 = dose / 250 mL

#### 시간 의존적 억제 (TDI, Time-Dependent Inhibition / Mechanism-Based Inhibition)
- **평가 방법:** Pre-incubation 후 활성 측정 (희석법)
- **트리거 기준:**
  - KI (비활성화 상수) 및 kinact (최대 비활성화 속도상수) 측정
  - AUCR 예측 ≥ 1.25 시 임상 시험 권고
- **우선 대상:** 아민 함유 화합물, 알킬아민, 메틸렌디옥시 그룹 포함 화합물

---

### 1.2 CYP 유도 평가

#### 유도 판단 기준
- **실험 방법:** 인간 원발성 간세포(fresh 또는 cryopreserved hepatocytes) 사용
- **평가 효소:** CYP1A2, CYP2B6, CYP3A (주요 유도 대상)

#### 유도 판정 기준
| 기준 | 조건 | 판정 |
|------|------|------|
| mRNA 증가 | ≥ 2배 농도 의존적 증가 | 유도제 가능성 있음 |
| 양성 대조 대비 | 양성 대조의 ≥ 20% 증가 (2배 미만이라도) | 유도 배제 불가 |
| 간 농도 추정 | 평균 비결합형 정상 상태 혈장 최고 농도의 30배 사용 | 간 유도 평가 |

- 양성 대조: CYP1A2 → Omeprazole; CYP2B6 → Phenobarbital; CYP3A → Rifampin

---

### 1.3 수송체 평가

#### 평가 대상 수송체

| 수송체 | 주요 위치 | 기능 |
|--------|-----------|------|
| P-glycoprotein (P-gp, MDR1) | 장, 간, 신장, BBB | 유출 |
| BCRP (Breast Cancer Resistance Protein) | 장, 간, 신장 | 유출 |
| OATP1B1 | 간 | 유입 |
| OATP1B3 | 간 | 유입 |
| OCT1 | 간 | 유입 |
| OCT2 | 신장 | 유입 |
| OAT1 | 신장 | 유입 |
| OAT3 | 신장 | 유입 |
| MATE1 | 신장, 간 | 유출 |
| MATE2-K | 신장 | 유출 |

#### 수송체 억제 — 임상 트리거 기준

**P-gp / BCRP 억제 (경구 투여):**
- 기준: [I_gut] / IC₅₀ ≥ 10 → 임상 DDI 시험 고려
- I_gut = dose / 250 mL

**P-gp / BCRP 억제 (정맥 투여 또는 순환 대사체):**
- 기준: I₁ / IC₅₀ ≥ 0.1 → 임상 DDI 시험 고려
- I₁ = 총 최고 혈장 농도 (Cmax)

**OATP1B1 / OATP1B3 억제:**
- 기준: R = 1 + (Imax,u / IC₅₀) > 1.1 → 임상 DDI 시험 고려

**OAT1, OAT3, OCT2, MATE1, MATE2-K 억제:**
- 기준: Imax,u / IC₅₀ ≥ 0.1 → 임상 DDI 시험 고려
- (2020년 가이드에서 MATE 기준이 0.02 → 0.1로 상향 조정)

**OCT1 억제:**
- 기준: Imax / IC₅₀ ≥ 0.1 (총 Imax 사용)

---

## Part 2: Clinical DDI Study 설계

### 2.1 시험 설계 선택

| 설계 유형 | 적용 조건 |
|-----------|-----------|
| One-sequence (비교적 간단) | 반감기 긴 기질(substrate) 사용 시; 기질이 임상 용량에서 안전한 경우 |
| Two-period crossover | 기질의 약동학 예측 가능; 충분한 washout 가능한 경우 |
| Fixed-sequence (순차적) | 시험약이 기질 역할도 할 경우; 안전성 고려 필요 시 |
| Parallel | 장기 반감기 기질; crossover 비현실적인 경우 |

#### 권고 사항
- 강력한 억제제/유도제를 perpetrator로 사용하는 경우 one-sequence 설계가 일반적
- Crossover는 개체 내 변동성 통제에 유리
- Washout: 최소 5 반감기 (억제제 및 기질 모두)

---

### 2.2 DDI Study 필요 판단 기준

임상 DDI 시험을 수행해야 하는 경우:
1. In vitro 스크리닝에서 임상 트리거 기준 충족
2. 높은 간 추출률 약물 (first-pass 효과 큰 경우)
3. 좁은 치료 지수(NTI) 약물이 기질 또는 perpetrator인 경우
4. 주요 CYP 경로에 의해 대사되는 주요 약물 (AUC에서 ≥25% 기여)

PBPK 모델로 임상 시험을 대체하거나 시험 설계 최적화할 수 있음 (사전 FDA 협의 권장).

---

### 2.3 기질/억제제/유도제 선택

#### Index Substrates (탐색 기질)

| CYP/수송체 | Sensitive Index Substrate | Strong Inhibitor (perpetrator) |
|------------|--------------------------|-------------------------------|
| CYP1A2 | Caffeine, Tizanidine | Fluvoxamine |
| CYP2B6 | Bupropion | Ticlopidine |
| CYP2C8 | Repaglinide, Rosiglitazone | Gemfibrozil |
| CYP2C9 | Warfarin (S-), Tolbutamide | Fluconazole |
| CYP2C19 | Omeprazole, Lansoprazole | Fluvoxamine, Fluconazole |
| CYP2D6 | Desipramine, Dextromethorphan | Paroxetine, Bupropion |
| CYP3A | Midazolam, Buspirone | Itraconazole, Clarithromycin |
| P-gp | Digoxin, Dabigatran etexilate | Quinidine |
| OATP1B1/3 | Rosuvastatin, Atorvastatin | Rifampin (single dose) |
| OAT1/3 | Furosemide, Methotrexate | Probenecid |
| OCT2/MATE | Metformin | Cimetidine, Pyrimethamine |

**Sensitive substrate 정의:** 강력한 index inhibitor 존재 시 AUC ≥ 5배 증가하는 기질
**Moderate sensitive:** AUC 2~5배 증가
**Weak:** AUC < 2배 증가

#### Strong/Moderate/Weak Inhibitor 분류
| 분류 | 기준 (sensitive substrate AUC 변화) |
|------|-------------------------------------|
| Strong inhibitor | ≥ 5배 증가 |
| Moderate inhibitor | 2~5배 미만 증가 |
| Weak inhibitor | 1.25~2배 미만 증가 |

#### Strong/Moderate/Weak Inducer 분류
| 분류 | 기준 (sensitive substrate AUC 변화) |
|------|-------------------------------------|
| Strong inducer | ≥ 80% 감소 |
| Moderate inducer | 50~80% 감소 |
| Weak inducer | 20~50% 감소 |

---

### 2.4 No-Effect Boundary

- **표준 기준:** GMR (Test/Reference) 90% CI가 **0.80 ~ 1.25** 범위 이내
- 이 범위 내에 있으면 clinically meaningful DDI 없음으로 판정
- NTI 기질의 경우: 더 좁은 범위 (0.90 ~ 1.11) 고려

---

### 2.5 GMR 해석 기준

| GMR 변화 | 해석 | 라벨 권고 |
|----------|------|-----------|
| ≤ 1.25배 증가 또는 감소 | 임상적으로 무의미 | 라벨 기재 불필요 (또는 간단 언급) |
| 1.25~2배 증가 | 약한 억제 | 경고 또는 용량 조정 고려 라벨 기재 |
| 2~5배 증가 | 중등도 억제 | 병용 주의/용량 조정/모니터링 라벨 기재 |
| > 5배 증가 | 강한 억제 | 병용 금기 또는 엄격한 용량 조정 |
| > 80% 감소 | 강한 유도 | 병용 금기 또는 용량 증가 |

---

## Part 3: 약물 라벨 기재 권고

### 라벨 포함 정보
- 시험된 perpetrator 및 기질 약물
- GMR 및 90% CI (AUC, Cmax)
- 임상적 권고사항 (용량 조정, 병용 금기, 모니터링)
- In vitro 데이터만 있는 경우 → 임상 상호작용 가능성 기술
- PBPK 모델 결과 → 실제 임상 시험을 대체하거나 라벨 문구 지원 가능

### 라벨 기재 문구 예시
- "Coadministration with strong CYP3A inhibitors increased [drug] exposure by X-fold"
- "Avoid coadministration with strong CYP3A inducers"
- "[Drug] is an inhibitor of [transporter]; monitor for adverse effects of [substrate]"

---

## Part 4: PBPK 모델링 활용

- 임상 시험 설계 최적화 (용량 선택, 투여 간격)
- 임상 시험을 수행하기 어려운 집단(소아, 임산부)에서의 DDI 예측
- 기존 임상 DDI 데이터를 활용한 다른 병용약에 대한 외삽
- **FDA PBPK 활용 가이드:** "Physiologically Based Pharmacokinetic Analyses — Format and Content" (2018)
- PBPK 모델 검증: 관찰된 PK 데이터와 비교, AUC 및 Cmax 2배 이내 예측 정확도

---

## 주요 기준 요약 테이블

| 항목 | 기준 |
|------|------|
| CYP 가역적 억제 트리거 (R1) | ≥ 1.02 |
| CYP 장내 억제 트리거 (R2) | ≥ 11 |
| CYP 유도 트리거 (mRNA) | ≥ 2배 또는 양성 대조 20% 이상 |
| P-gp/BCRP 억제 트리거 (경구) | I_gut/IC₅₀ ≥ 10 |
| P-gp/BCRP 억제 트리거 (정맥/대사체) | I₁/IC₅₀ ≥ 0.1 |
| OATP1B1/3 억제 트리거 | R > 1.1 |
| OAT/OCT2/MATE 억제 트리거 | Imax,u/IC₅₀ ≥ 0.1 |
| No-effect boundary | GMR 90% CI 0.80~1.25 |
| Strong inhibitor 정의 | sensitive substrate AUC ≥ 5배 증가 |
| Strong inducer 정의 | sensitive substrate AUC ≥ 80% 감소 |

---

## 주의 사항

1. **2020년 개정 주요 변경:** MATE 트리거 기준 상향(0.02→0.1), OATP pre-incubation 시간 단축(30→15분), Ki,u/IC₅₀,u 비결합형 값 사용 명시.
2. **ICH M12:** 2022년 발행된 ICH M12는 국제 조화 가이드라인으로, 이 FDA 2020 가이드를 대체/보완하는 방향으로 진화 중. 최신 요건은 ICH M12 확인 필요.
3. **Metabolite DDI:** 주요 인간 대사체(순환 농도 ≥ 모약의 25%)도 별도 평가 필요.
4. **복합 기전:** 동일 약물이 여러 경로로 DDI를 일으킬 경우 모든 경로 평가.
5. **특수 집단:** 신장/간 기능 장애 환자에서 수송체 역할 변화 가능; 집단 PK 분석 보완 권고.

---

## 참고 문헌

- FDA. (2020). *In Vitro Drug Interaction Studies — Cytochrome P450 Enzyme- and Transporter-Mediated Drug Interactions*. CDER.
- FDA. (2020). *Clinical Drug Interaction Studies — Cytochrome P450 Enzyme- and Transporter-Mediated Drug Interactions*. CDER.
- FDA Drug Interactions Table: https://www.fda.gov/drugs/drug-interactions-labeling/drug-development-and-drug-interactions-table-substrates-inhibitors-and-inducers
- ICH M12 Drug Interaction Studies (2022): https://database.ich.org/sites/default/files/M12_Step1_draft_Guideline_2022_0524.pdf
