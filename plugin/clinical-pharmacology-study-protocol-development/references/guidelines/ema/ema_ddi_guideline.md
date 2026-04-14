# Guideline on the Investigation of Drug Interactions

## 메타 정보

| 항목 | 내용 |
|------|------|
| 발행 기관 | EMA CHMP (Committee for Medicinal Products for Human Use) |
| 문서명 | Guideline on the Investigation of Drug Interactions |
| 문서 번호 | CPMP/EWP/560/95/Rev. 1 Corr. 2 |
| 발행일 | 2012-06 (채택), 2015-06 (마지막 수정) |
| 원문 URL | https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-investigation-drug-interactions-revision-1_en.pdf |
| 마지막 검증일 | 2026-04-13 |
| 비고 | 현재 Rev. 2 개정 진행 중 (2017년 Concept paper 발행). ICH M12 (2024 Step 5) 참조 권고. |

## 적용 범위

- 신약 및 의약품의 잠재적 약물-음식 및 약물-약물 상호작용(DDI) 평가
- 허브 의약품 포함
- 대사 효소(CYP, UGT) 및 수송체 매개 상호작용
- In vitro → in vivo 외삽 및 라벨링 권고 기준
- PBPK 모델링 활용 원칙

---

## 1. In Vitro DDI 평가 체계

### 1.1 평가 시기

- 원칙: Phase II 진입 전에 주요 in vitro 시험 완료 권고
- 목적: 임상 DDI 시험 필요성 조기 결정 및 임상 시험 설계 지원

### 1.2 평가 약물

| 역할 | 정의 |
|------|------|
| Victim (피해약) | 다른 약물에 의해 PK가 변화되는 약물 (피해를 받는 기질) |
| Perpetrator (가해약) | 다른 약물의 PK를 변화시키는 약물 (억제제, 유도제) |

---

## 2. CYP 효소 평가

### 2.1 평가 대상 CYP 효소

| 효소 | 주요 역할 | 평가 방향 |
|------|-----------|-----------|
| CYP1A2 | 카페인, 클로자핀 등 | Substrate / Inhibitor / Inducer |
| CYP2B6 | 부프로피온, 에파비렌즈 등 | Substrate / Inhibitor / Inducer |
| CYP2C8 | 파클리탁셀, 레파글리니드 등 | Substrate / Inhibitor |
| CYP2C9 | 와파린, 셀레콕시브 등 | Substrate / Inhibitor / Inducer |
| CYP2C19 | 오메프라졸, 클로피도그렐 등 | Substrate / Inhibitor / Inducer |
| CYP2D6 | 데시프라민, 메토프롤롤 등 | Substrate / Inhibitor |
| CYP3A4/5 | 미다졸람, 시클로스포린 등 | Substrate / Inhibitor / Inducer |

### 2.2 기질 평가 — Victim 가능성

- 각 CYP에서 미다졸람, 덱스트로메토르판 등 선택적 기질과 경쟁 실험
- 특정 CYP에 의한 대사 분율(fm) 추정
- **fm ≥25%**: 해당 CYP의 억제제/유도제와 임상 DDI 시험 고려

### 2.3 억제제 평가 — Perpetrator 가능성 (가역적 억제)

**Basic Model (기본 모형):**
- 공식: R₁ = 1 + (I/Ki,u)
  - I: 억제제의 최고 계획 혈장 내 비결합 농도 (Cmax,u)
  - Ki,u: 비결합 억제 상수
- **판정 기준**: R₁ ≥ 1.02 → 임상 DDI 시험 또는 추가 평가 필요

**장 기여 고려 (R₁,gut):**
- 공식: R₁,gut = 1 + (Fabs × Dose / Ka × Vgut × Ki,u)
  - Ka: 흡수 속도 상수 (~0.1 min⁻¹)
  - Vgut: 장 유체 부피 (~650 mL)
- **판정 기준**: R₁,gut ≥ 11 → 장 CYP3A 억제 임상 시험 고려

**시간 의존성 억제(TDI/MBI) — Mechanism-Based Inhibition:**
- R₂ = 1 / (1 + kinact,max × [I] / (KI + [I]) / kdeg)
  - kinact,max: 최대 불활성화 속도 상수
  - KI: 불활성화 반감 농도
  - kdeg: CYP 자연 분해 속도 상수
- **판정 기준**: R₂ ≥ 1.25 → 임상 TDI 평가 필요

### 2.4 유도제 평가 — Inducer 가능성

**In vitro 지표:**
- mRNA 발현 증가 (선호 지표)
- 효소 활성 증가 (보완 지표)
- 양성 대조: 리팜피신 (CYP3A4, CYP2C9, CYP2C19 등)

**판정 기준 (R₃, indirect response model):**
- 공식: R₃ = 1 / (1 + d × Emax × C / (EC₅₀ + C))
  - d: 인체와 in vitro 시스템 간 보정 계수 (약 1)
- **R₃ ≤ 0.8** → 임상 유도 평가 필요

**주요 CYP 유도인자 mRNA 기준:**
- 리팜피신 대비 CYP3A4 mRNA 증가 >40% → 임상적으로 유의한 유도 가능성

### 2.5 UGT 평가

- UGT1A1, UGT2B7: 억제제 시험 권고 (FDA와 달리 기질 의사결정 체계 없음)
- **EMA 특이**: BSEP (담즙 유출 펌프) 억제 평가 권고 — 간 독성 안전성 목적

---

## 3. 수송체(Transporter) DDI 평가

### 3.1 필수 평가 수송체 (Mandatory)

| 수송체 | 위치 | 방향 | 임계 조건 |
|--------|------|------|-----------|
| P-glycoprotein (P-gp, ABCB1) | 장, 뇌, 신장 | 유출(efflux) | 모든 신약 |
| BCRP (ABCG2) | 장, 간, 뇌 | 유출 | 모든 신약 |
| OATP1B1 (SLCO1B1) | 간 | 흡수(uptake) | 간 배설 ≥25% |
| OATP1B3 (SLCO1B3) | 간 | 흡수 | 간 배설 ≥25% |
| OCT2 (SLC22A2) | 신장 | 흡수 | 신장 분비 ≥25% |
| OAT1 (SLC22A6) | 신장 | 흡수 | 신장 분비 ≥25% |
| OAT3 (SLC22A8) | 신장 | 흡수 | 신장 분비 ≥25% |

### 3.2 선택적 평가 수송체 (Optional, 임상적 관련성 있는 경우)

| 수송체 | 위치 | 방향 |
|--------|------|------|
| OCT1 (SLC22A1) | 간 | 흡수 |
| MATE1 (SLC47A1) | 신장, 간 | 유출 |
| MATE2-K (SLC47A2) | 신장 | 유출 |
| BSEP (ABCB11) | 간 | 유출 (EMA 추가) |

### 3.3 In Vitro 기질 판정 기준

- Efflux ratio (ER) ≥2 (bidirectional permeability assay): P-gp 또는 BCRP 기질 가능성
- Net ER >2: 능동 수송 존재 시사

### 3.4 In Vitro 억제 기준

**P-gp / BCRP 억제 평가:**
- 기준 농도: 50 × Cmax,u (비결합 형태 최고 농도 기준)
- R 값: R = 1 + (I/IC₅₀) 계산

**OATP1B1/1B3 억제 평가 (간 유입):**
- 기준 농도: 25 × Cmax,u (비결합 형태)
- 경구 약물의 경우 간문맥 최고 농도 고려 필요

**판정:**
- IC₅₀ 또는 Ki 계산으로 임상 관련성 예측
- R ≥ 1.25: 임상 DDI 시험 또는 PBPK 분석 고려

---

## 4. 임상 DDI 시험 설계

### 4.1 기본 설계 원칙

- **우선**: 건강 성인 자원자 대상, 교차 설계
- 충분한 세척 기간 (억제제: t½의 5배 이상, 유도제: 유도 효과 소실 시까지)
- 개방 또는 맹검 설계 (상호작용 크기 예측이 목적이므로 개방도 허용)

### 4.2 Probe Substrate 선택

| CYP/수송체 | 권고 기질 (임상 probe) |
|------------|------------------------|
| CYP3A4 (장+간) | 미다졸람(midazolam) i.v. + p.o. (두 경로 구분) |
| CYP3A4 | 부세나파이드(buspirone), 펠로디핀(felodipine) |
| CYP2C9 | 와파린(warfarin), 톨부타미드(tolbutamide) |
| CYP2C19 | 오메프라졸(omeprazole), 란소프라졸(lansoprazole) |
| CYP2D6 | 데시프라민(desipramine), 메토프롤롤(metoprolol) |
| CYP1A2 | 카페인(caffeine), 테오필린(theophylline) |
| CYP2B6 | 에파비렌즈(efavirenz), 부프로피온(bupropion) |
| OATP1B1/1B3 | 로수바스타틴(rosuvastatin), 프라바스타틴(pravastatin) |
| P-gp | 디곡신(digoxin), 다비가트란 에텍실레이트 |
| BCRP | 로수바스타틴(rosuvastatin) |
| OCT2/MATE | 메트포르민(metformin) |

### 4.3 특수 설계

**유도제 3-arm 설계:**
- Arm 1: 기질 단독
- Arm 2: 유도제 + 기질 (정상 상태)
- Arm 3: 유도제 중단 후 기질 (회복 평가)
- 목적: 유도 효과 발현 및 소실에 필요한 시간 파악

**혼합 억제/유도 효과:**
- EMA: 기계론적 모델만으로 부족 → in vivo 임상 시험 필요
- FDA와의 주요 차이점

### 4.4 평가 지표 (PK Endpoints)

| 지표 | 해석 |
|------|------|
| AUC ratio (± 상호작용) | 전신 노출 변화 크기 |
| Cmax ratio | 최고 농도 변화 |
| 90% CI for GMR | 상호작용의 통계적 불확실성 |
| Half-life, oral clearance | 기전 이해 보완 |

**임상적 유의성 판단:**
- 통상적으로 GMR 50–200% (0.5–2배): 임상적으로 유의한 상호작용
- NTI 약물: 더 엄격한 기준 적용

---

## 5. PBPK 모델링 활용

### 5.1 EMA 입장

- PBPK는 지지적 도구로 허용; **1차 의사결정 수단으로는 제한적**
- EMA는 FDA보다 덜 처방적 접근: 개략적 framework 제공
- 혼합 억제/유도 효과 예측에 in vivo 데이터 선호

### 5.2 PBPK 활용 가능 분야

| 활용 분야 | 세부 내용 |
|-----------|-----------|
| 임상 시험 면제 근거 | in vitro 데이터 + PBPK로 임상 DDI 불필요 증명 |
| 특수 집단 외삽 | 노인, 신기능장애, 간기능장애 환자 |
| 시간 의존성 억제 | TDI 효과의 시간적 변화 모델링 |
| 다중 DDI 예측 | 여러 상호작용 동시 평가 |
| 복용 시간 최적화 | 투여 간격 조정 시뮬레이션 |

### 5.3 PBPK 보고 요건

- 모델 구조 및 가정 명시
- 입력 파라미터 및 출처
- 모델 검증 데이터 (임상 PK 데이터 대비)
- 예측 신뢰도 평가

---

## 6. 대사체(Metabolite) DDI 평가

### 6.1 EMA 기준

- 모약물 AUC의 **≥25%**에 달하는 대사체: 가해약(perpetrator) 및 피해약(victim) 평가 필요
- EMA 추가 조건: 총 순환 대사체 부담의 **≥10%** → 평가 고려
- 약리적 또는 독성학적으로 활성인 대사체는 더 낮은 역치에서도 평가

---

## 7. CYP 다형성(Polymorphism) 고려

- CYP2C9, CYP2C19, CYP2D6: 유전형/표현형 검사 권고
- UGT1A1, OATP1B1 (SLCO1B1): 수송체 다형성 고려
- 임상 시험에서 분층화(stratification) 또는 별도 분석
- 다형성 효소에 의해 주로 대사되는 약물: 표현형 집단별 분리 보고

---

## 8. DDI 시험 면제 조건

### 8.1 In Vitro 기반 면제

| 상황 | 면제 조건 |
|------|-----------|
| CYP 비가역적 억제 없음 | R₁ < 1.02 및 R₁,gut < 11 |
| TDI 없음 | R₂ < 1.25 |
| 유도 없음 | R₃ > 0.8 (mRNA 기준 유의미한 유도 없음) |
| 수송체 억제 낮음 | IC₅₀ >> 임상 농도 |

### 8.2 임상 시험 면제 (PBPK 기반)

- 충분히 검증된 PBPK 모델로 AUC ratio <0.8 또는 >1.25 배제 가능
- EMA는 지지 자료로 수용하나 단독 근거로는 더 엄격한 검토

---

## 9. 약물 라벨(SmPC) 반영 기준

### 9.1 임상적 유의성에 따른 라벨링

| 상호작용 크기 | 권고 라벨 내용 |
|---------------|----------------|
| AUC >5배 증가 | 병용 금기(contraindicated) |
| AUC 2–5배 증가 | 병용 주의, 용량 조정 권고 |
| AUC 1.25–2배 증가 | 병용 주의, 모니터링 권고 |
| AUC <1.25배 변화 | 일반적으로 임상적으로 무의미 |
| AUC >50% 감소 (유도) | 병용 주의 또는 금기, 용량 증량 고려 |

### 9.2 SmPC 섹션별 DDI 정보 기술

- 섹션 4.5: 다른 약물과의 상호작용 (정량적 데이터 포함)
- 섹션 4.4: 특별 경고 (중증 상호작용의 경우)
- 섹션 5.2: PK 정보 (in vitro 데이터 포함)

---

## 10. EMA vs. FDA 주요 차이점

| 항목 | EMA (2012) | FDA |
|------|------------|-----|
| **농도 지표** | **비결합 농도(fu) 기반** | 총 Cmax 기반 (일선) |
| **혼합 억제/유도** | **In vivo 시험 필요** | PBPK 모델 수용 |
| **평가 시기** | Phase II 전 권고 | 덜 명시적 |
| **UGT** | 억제 시험만 (기질 체계 없음) | 기질 의사결정 체계 있음 |
| **BSEP** | **필수 평가 (EMA 전용)** | 해당 없음 |
| **접근 방식** | 개념적/일반적 framework | 처방적 (12개 의사결정 트리) |
| **PBPK 역할** | 지지적 도구 | 더 주된 역할 인정 |
| **대사체 기준** | ≥25% 또는 ≥10% (이중 기준) | ≥25% 단일 기준 |

---

## 11. 관련 가이드라인 연계

| 가이드라인 | 관계 |
|-----------|------|
| ICH M12 Drug Interaction Studies (2024) | 최신 국제 조화 기준; EMA 현행 가이드라인 보완/대체 예정 |
| EMA PBPK 보고 가이드라인 | PBPK 모델링 보고 요건 상세 기술 |
| ICH E7 (노인 대상 임상시험) | 특수 집단 DDI 평가 연계 |
| ICH M3(R2) | 비임상 안전성 시험과 DDI 평가 시점 연계 |

---

## 참고 문헌

- EMA. Guideline on the Investigation of Drug Interactions (CPMP/EWP/560/95/Rev. 1 Corr. 2). European Medicines Agency; 2012.
- EMA. ICH M12 Guideline on Drug Interaction Studies. 2024.
- Benet LZ, et al. Drug–Drug Interaction Studies: Regulatory Guidance and An Industry Perspective. AAPS J. 2014;16(6):1295-1309. PMC3691435.
- EMA. Guideline on Reporting of Physiologically Based Pharmacokinetic (PBPK) Modelling and Simulation. 2018.
