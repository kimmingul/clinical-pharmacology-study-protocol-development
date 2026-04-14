# Estimating the Maximum Safe Starting Dose in Initial Clinical Trials for Therapeutics in Adult Healthy Volunteers (2005)

## 메타 정보

| 항목 | 내용 |
|------|------|
| 발행 기관 | FDA CDER |
| 문서명 | Guidance for Industry: Estimating the Maximum Safe Starting Dose in Initial Clinical Trials for Therapeutics in Adult Healthy Volunteers |
| 발행일 | 2005-07 |
| 원문 URL | https://www.fda.gov/downloads/Drugs/GuidanceComplianceRegulatoryInformation/Guidances/ucm078932.pdf |
| 연방관보 공지 | https://www.federalregister.gov/documents/2005/07/22/05-14456 |
| 마지막 검증일 | 2026-04-13 |

---

## 적용 범위

- 소분자 화합물(small molecule therapeutics)의 최초 임상시험(First-in-Human, FIH) 단회 상승 용량 시험 시 성인 건강한 자원자에 대한 **최대 안전 시작 용량(Maximum Recommended Starting Dose, MRSD)** 추정
- 적용 제외: 세포독성 항암제(별도 지침 적용), 생물의약품(biologics, 일부 원칙 공유)
- 목적: 동물 독성 자료(NOAEL)를 인간 등가 용량(HED)으로 환산하고, 안전 계수(safety factor)를 적용하여 MRSD 도출

---

## 핵심 요건

### 1. MRSD 산출 5단계 절차

| 단계 | 내용 |
|------|------|
| 1 | 각 동물 종의 NOAEL 결정 |
| 2 | 각 NOAEL을 HED(Human Equivalent Dose)로 환산 |
| 3 | 가장 적절한 동물 종 선택 |
| 4 | 안전 계수(safety factor) 적용 |
| 5 | 약리학적 고려사항 적용(해당 시) |

---

### 2. NOAEL 결정

**NOAEL (No Observed Adverse Effect Level):**
- 동물 독성시험에서 대조군 대비 유의한 유해 효과의 증가가 관찰되지 않는 최고 용량
- 가역적 또는 비가역적 유해 효과, 임상적으로 유의한 기능 변화 없음
- 단위: mg/kg/day (경구 또는 해당 투여 경로)

**적용 시험 자료:**
- 최소한 두 종(설치류 및 비설치류) 반복 투여 독성 시험 요구
- 계획된 임상 시험 기간 이상의 독성 시험 완료 후 MRSD 확정

---

### 3. HED 환산 — 체표면적(BSA) 방법

#### 기본 원칙
체표면적(Body Surface Area) 정규화를 통해 종간 용량 환산:

**HED 계산식:**

$$\text{HED (mg/kg)} = \text{Animal NOAEL (mg/kg)} \times \frac{K_m^{animal}}{K_m^{human}}$$

또는:

$$\text{HED (mg)} = \text{Animal NOAEL (mg/kg)} \times \text{Animal weight (kg)} \times \frac{K_m^{animal}}{K_m^{human}}$$

#### Km 인자 (체중/체표면적 비율)

| 동물 종 | 표준 체중 (kg) | 체표면적 (m²) | Km 인자 |
|---------|--------------|--------------|---------|
| 인간 (성인) | 60 | 1.62 | 37 |
| 마우스 (Mouse) | 0.02 | 0.007 | 3 |
| 랫트 (Rat) | 0.15 | 0.025 | 6 |
| 햄스터 (Hamster) | 0.08 | 0.016 | 5 |
| 기니피그 (Guinea Pig) | 0.40 | 0.05 | 8 |
| 토끼 (Rabbit) | 1.8 | 0.15 | 12 |
| 개 (Dog) | 10 | 0.50 | 20 |
| 원숭이 (Rhesus Monkey) | 3 | 0.25 | 12 |
| 마모셋 (Marmoset) | 0.35 | 0.06 | 6 |
| 미니피그 (Minipig) | 40 | 1.14 | 27 |

**주:** Km = 체중(kg) / 체표면적(m²)

#### HED 계산 예시

**예시:** 랫트 NOAEL = 100 mg/kg/day

$$\text{HED} = 100 \text{ mg/kg} \times \frac{6}{37} = 16.2 \text{ mg/kg}$$

**개 NOAEL = 50 mg/kg/day:**

$$\text{HED} = 50 \text{ mg/kg} \times \frac{20}{37} = 27.0 \text{ mg/kg}$$

---

### 4. 가장 적절한 동물 종 선택

#### 선택 원칙
1. **독성학적으로 가장 관련성 높은 종(most relevant species)** 우선 선택
2. 독성 기전이 인간과 유사한 종
3. 동일 표적 기관(target organ) 독성 확인 종
4. 독성 기전 불명확한 경우: **가장 민감한 종(most sensitive species)** 선택 → 가장 낮은 HED 적용

#### 선택 시 고려 사항
- 인간과 유사한 대사 경로
- 동일 약리학적 기전으로 인한 독성
- 수용체/효소 발현 유사성
- 종 특이적 독성 배제(예: 랫트의 α2u-globulin 신장병증)

---

### 5. 안전 계수 (Safety Factor) 적용

#### 기본 안전 계수
$$\text{MRSD} = \frac{\text{HED}}{Safety Factor}$$

**기본 안전 계수: 10**
- 동물-인간 간 생리적 차이 보정
- 임상 시험 집단의 이질성 고려

#### 안전 계수 조정 조건

**더 큰 안전 계수 적용 (> 10):**

| 조건 | 권고 안전 계수 |
|------|---------------|
| 가파른 용량-반응 곡선 | > 10 |
| 심각하고 비가역적인 독성 (심독성, 신독성) | > 10 |
| 독성 발현이 노출 초기에 나타남 | > 10 |
| NOAEL 불확실성 (용량 간격 넓음) | > 10 |
| 종 간 독성 데이터 일치하지 않음 | > 10 |
| 작용 기전 불명확 | > 10 |

**더 작은 안전 계수 허용 (< 10):**

| 조건 | 권고 안전 계수 |
|------|---------------|
| 독성 기전 완전히 규명됨 | 5~10 |
| 여러 종에서 독성 반응 일관 | 5~10 |
| 독성이 가역적이고 경미함 | 5~10 |
| 적절한 약리학적 모니터링 가능 | 5~10 |
| 독성 발현에 충분한 선행 지표 존재 | 5 |

---

### 6. 최소 예상 생물학적 효과 수준(MABEL) 접근

전통적 NOAEL/HED 방법의 대안 또는 보완:
- **MABEL (Minimum Anticipated Biological Effect Level):** 최소 약리학적 효과가 예상되는 용량
- 주로 면역 조절 약물, 단클론 항체 등 생물의약품에 적용
- FIH 시작 용량은 MABEL과 MRSD(NOAEL 기반) 중 낮은 값 선택

---

### 7. 약리학적 고려사항

#### 약리학적 활성 용량과의 비교
- **PAD (Pharmacologically Active Dose):** 동물에서 원하는 약리 효과를 나타내는 용량
- MRSD > PAD인 경우: 시험 시작 시 이미 치료 용량 범위일 수 있으므로 주의
- MRSD ≪ PAD인 경우: 안전성 확보된 낮은 용량에서 시작 가능

#### 종 특이적 약리 반응
- 동물 모델에서 약리 효과가 매우 크거나 특이적인 경우 MRSD를 낮게 조정 가능

---

### 8. 용량 증량 방법

#### 기본 원칙
- FIH 시험은 일반적으로 **단회 상승 용량(SAD)** 시험으로 시작
- **인트라파티엔트(intra-patient) 용량 증량:** 동일 피험자 내에서 순차적 증량

#### 권고 용량 증량 간격
| 단계 | 용량 증가 폭 |
|------|-------------|
| 저용량 단계 | 최대 2배 (100% 증가) |
| 중등 용량 단계 | 최대 60~75% 증가 |
| 고용량 단계 | 최대 25~33% 증가 (또는 PK/PD 데이터 기반) |

- Modified Fibonacci 증량법: 100%, 67%, 50%, 40%, 33%, ...
- 각 코호트 투여 후 안전성 데이터 검토 후 다음 용량 결정 (Dose Escalation Review Committee, DERC)

---

### 9. 안전성 고려사항

#### 중단 기준 (Stopping Rules)
- 미리 정의된 용량 제한 독성(DLT, Dose-Limiting Toxicity) 발생 시 증량 중단
- 피험자당 최대 용량 한계 설정 (안전 계수 기반)

#### 특수 독성 고려
- **심독성:** hERG 채널 억제, QTc 연장 → 심전도 모니터링
- **신독성:** Creatinine, BUN 모니터링
- **간독성:** LFT 모니터링
- **중추신경 독성:** 신경 기능 평가

---

## MRSD 산출 예시 (종합)

**시나리오:**
- 랫트 NOAEL: 100 mg/kg/day → HED = 100 × (6/37) = 16.2 mg/kg
- 개 NOAEL: 30 mg/kg/day → HED = 30 × (20/37) = 16.2 mg/kg
- 가장 민감한 종: 랫트와 개 동일한 HED
- 독성: 간 효소 상승 (가역적)

**안전 계수 적용:**
- 가역적 독성, 독성 지표 모니터링 가능 → 안전 계수 = 10 (기본)
- MRSD = 16.2 / 10 = **1.62 mg/kg** (≈ 97 mg, 60 kg 기준)

---

## 주의 사항

1. **이 가이드는 소분자 화합물에 특화:** 단클론 항체, 세포/유전자 치료제는 별도 가이드 (예: EMEA/CHMP/SWP/28367/07 등) 참조.
2. **세포독성 항암제:** 별도 FDA 가이드라인 "Guidance for Industry: Estimating the Maximum Safe Starting Dose for Oncology Phase I Trials" 적용.
3. **체중 기반 용량:** 이 가이드는 mg/kg 단위 기준; flat dose 또는 BSA 기반 용량(mg/m²)은 별도 환산 필요.
4. **인간 대사 차이:** 인간에서 독성 대사체가 생성될 가능성이 있는 경우 별도 고려 필요.
5. **TK(Toxicokinetics) 데이터:** 동물 독성 시험에서 독성 동태학 데이터가 있으면 HED 환산의 정확도 향상.
6. **2005년 이후 업데이트:** 이 가이드는 2005년 이후 개정되지 않았으나, ICH S9, ICH M3(R2) 등 최신 가이드라인과 함께 적용.

---

## 참고 문헌

- FDA. (2005). *Guidance for Industry: Estimating the Maximum Safe Starting Dose in Initial Clinical Trials for Therapeutics in Adult Healthy Volunteers*. CDER.
- Reagan-Shaw, S., Nihal, M., & Ahmad, N. (2008). Dose translation from animal to human studies revisited. *FASEB J*, 22(3), 659–661.
- FDA. (2021). *M3(R2) Nonclinical Safety Studies for the Conduct of Human Clinical Trials and Marketing Authorization for Pharmaceuticals*. (ICH)
