# Bioequivalence Studies with Pharmacokinetic Endpoints for Drugs Submitted Under an ANDA

## 메타 정보

| 항목 | 내용 |
|------|------|
| 발행 기관 | FDA CDER |
| 문서명 | Bioequivalence Studies with Pharmacokinetic Endpoints for Drugs Submitted Under an Abbreviated New Drug Application |
| 발행일 | 2021-08 (Draft revised); 2022-02 (Posted) |
| 원문 URL | https://www.fda.gov/media/164681/download |
| 참조 URL | https://www.fda.gov/drugs/news-events-human-drugs/bioequivalence-studies-pharmacokinetic-endpoints-drugs-submitted-under-anda-02242022 |
| 마지막 검증일 | 2026-04-13 |

> **주의:** 원문 PDF 전문 접근 제한으로 일부 내용은 공개된 FDA 자료 및 관련 문헌을 통해 재구성하였음. 원문 확인 권장.

---

## 적용 범위

이 가이드라인은 ANDA(Abbreviated New Drug Application) 및 ANDA 보완(supplement)에 포함되는 생물학적 동등성(BE) 정보를 계획하는 신청자를 대상으로 한다. 주로 경구 투여 제제에 적용되며, 시스템 노출(PK 엔드포인트)에 의존하는 비경구 투여 제제(경피 흡수제, 일부 직장 및 비강 제제)에도 적용된다.

**FD&C Act** 및 FDA 규정에 따른 BE 요건을 충족하는 방법을 기술한다.

---

## 핵심 요건

### 1. 시험 설계 요건

#### 기본 원칙
- **표준 설계:** 단회 투여(single-dose), 무작위 배정, 2-way crossover, 공복(fasting) 조건
- **식후(fed) 시험:** 식이가 흡수에 영향을 미치는 경우 또는 라벨에 음식과 함께 복용 지시가 있는 경우 필수 수행

#### Crossover 설계 적용 조건
| 설계 유형 | 적용 조건 |
|-----------|-----------|
| 2-period, 2-sequence crossover | 대부분의 즉방형(IR) 제제 — 기본 설계 |
| 4-period, fully replicate crossover | 고변동 약물(HVD) RSABE 적용 시; NTI 약물 |
| Parallel 설계 | 반감기 > 24시간으로 crossover 비현실적인 경우; 윤리적 이유로 반복 투여 불가한 경우 |

#### Parallel 설계 요건
- 충분한 통계적 검정력 확보를 위해 더 많은 피험자 수 필요
- 최소한 동일한 피험자가 시험약과 대조약을 모두 복용하는 crossover 설계만큼의 검정력 유지

#### Washout period
- 최소 5개 반감기(t½) 이상
- 단, 배경 수치로 돌아오기까지 충분한 기간 확보

---

### 2. 공복/식후 시험 요건

#### 공복 시험
- 투약 전 최소 10시간 공복
- 투약 후 최소 4시간 금식
- 240 mL 물과 함께 투약

#### 식후 시험
- 투약 전 최소 10시간 공복 후 고지방/고칼로리 식사 제공
- **표준 고지방식:** 800~1,000 kcal, 지방 50% (약 500~600 kcal from fat)
  - 예시: 계란 2개(버터에 프라이), 베이컨 2줄, 버터 바른 토스트 2조각, 해시브라운 감자 4 oz, 전유 8 oz
- 식사 시작 후 30분 이내에 투약
- 식사는 30분 내에 완료

---

### 3. BE 판정 기준 (표준 약물)

#### 핵심 PK 파라미터
| 파라미터 | 정의 |
|----------|------|
| AUC₀₋ₜ | 투약부터 마지막 측정 가능한 농도까지 AUC (선형/로그-선형 사다리꼴법) |
| AUC₀₋∞ | 외삽 AUC (단, 외삽이 전체 AUC의 20% 미만이어야 함) |
| Cmax | 최고 혈중 농도 |

#### 표준 BE 허용 기준
- **90% CI of GMR (Test/Reference):** 80.00% ~ 125.00%
- 적용 파라미터: AUC₀₋ₜ, AUC₀₋∞, Cmax 모두 80.00~125.00% 이내
- log 변환 후 평균 차이의 90% CI가 기준 범위 내에 있어야 함

---

### 4. 고변동 약물(HVD) — RSABE

#### 정의
- 생체 내 within-subject CV (coefficient of variation) ≥ 30% (σ_wR ≥ 0.294)

#### RSABE (Reference-Scaled Average Bioequivalence) 적용 조건
- within-subject 변동성이 높은 약물에 대해 BE 허용 범위를 대조약의 변동성에 맞게 확장
- **Regulatory constant (θ):** 0.760 (log-scale)
  - 이 값은 σ_wR = 0.25에서의 80~125% 한계에 해당
- **RSABE 기준식:** 
  - (μ_T - μ_R)² ≤ θ × σ²_wR
  - 여기서 θ = (ln 1.25)² / 0.0625 = 0.892 (또는 FDA 적용 값 0.760)

#### HVD RSABE 적용 절차
1. Fully replicate crossover (4-period) 설계로 σ_wR 추정
2. σ_wR ≥ 0.294 이면 RSABE 적용 가능
3. 확장된 BE 한계: 80~125%의 상한이 σ_wR에 비례하여 확장
4. **최대 확장 한계 (cap):** 69.84% ~ 143.19% (σ_wR ≥ 0.5인 경우)
5. Cmax에 적용; AUC에는 표준 80~125% 기준 유지 권장 (제품별 가이드 참조)

#### 통계 분석 (RSABE)
- SAS PROC MIXED 또는 동등한 소프트웨어로 분산 성분 추정
- Point estimate (GMR)가 80.00~125.00% 이내여야 함 (RSABE 외에 추가 조건)

---

### 5. Truncated AUC 허용 조건

- **적용:** t½ > 24시간인 약물 (장기 반감기)
- AUC₀₋₇₂h (또는 AUC₀₋₄₈h) 사용 가능
- Cmax는 항상 평가
- **조건:** 72시간(또는 48시간) 채혈 시점까지 충분한 PK 프로파일 확보
- 통계 기준은 동일 (90% CI 80.00~125.00%)

---

### 6. NTI (Narrow Therapeutic Index) 약물 요건

#### NTI 약물 목록 예시
- Warfarin, Phenytoin, Digoxin, Lithium, Cyclosporine, Tacrolimus, Theophylline 등

#### 추가 요건
- **Fully replicate crossover 설계** 필수 (4-period)
- 대조약의 within-subject 변동성(σ_wR)을 추정하여 BE 한계 설정
- **RSABE와 반대 방향:** σ_wR이 작을수록 BE 한계가 좁아짐
- **표준 기준:** AUC 및 Cmax 모두 90% CI 80.00~125.00% (일부 PSG에서 더 엄격)
- 시험약의 within-subject 변동성(σ_wT)이 대조약(σ_wR)보다 크지 않아야 함 (비열등성 조건)

---

### 7. Fed Bioequivalence Study 요건

- 라벨에 음식과 함께 복용 지시가 있는 경우 필수
- 변형 방출(MR) 제제의 경우 일반적으로 공복 + 식후 두 가지 시험 모두 수행
- 즉방형(IR) 제제도 음식 섭취 지시가 있는 경우 식후 시험 필수
- 설계: 표준 고지방식 crossover 시험 (공복 시험과 동일한 원칙 적용)

---

### 8. Biowaiver 조건 (BCS 기반)

#### BCS 분류 시스템
| Class | 용해도 | 투과도 |
|-------|--------|--------|
| I | High | High |
| II | Low | High |
| III | High | Low |
| IV | Low | Low |

#### Biowaiver 허용 조건 (BCS Class I 기반)
1. **약물:** BCS Class I (고용해도, 고투과도)
2. **제제:** 즉방형(IR), 고용해도 제제
3. **용해도 기준:** pH 1.2, 4.5, 6.8 모두에서 37°C, 900 mL 이하 용매에서 최고 투여 용량이 완전 용해
4. **용해 시험 기준:** 참조약과 시험약 모두 900 mL pH 6.8 완충액에서 30분 내 85% 이상 용해 (paddle 50 rpm 또는 basket 100 rpm)
5. **추가 조건:** 음식이 흡수에 유의하게 영향을 미치지 않을 것 (AUC 변화 < 20%)

#### BCS Class III Biowaiver (경우에 따라)
- 고용해도, 저투과도 약물
- 매우 빠른 용해 기준: 15분 내 85% 이상
- 보조제가 동일하거나 유사할 것
- 흡수에 영향을 미치는 보조제 없을 것

---

### 9. Sample Size 권고

#### 결정 인자
- Intra-subject CV (%)
- 목표 검정력 (통상 80% 이상)
- 유의수준 α = 0.05
- 예상 GMR (점 추정치)

#### 일반 지침
| CV (%) | 최소 피험자 수 (crossover, 80% power) |
|--------|---------------------------------------|
| 15 | ~12 |
| 20 | ~18~24 |
| 25 | ~24~30 |
| 30 | ~36~48 |
| 40 | ~60~80 |

- 탈락률(dropout rate) 고려하여 20% 추가 등록 권장
- 최소 12명 완료 필요 (일부 PSG는 더 많은 수 요구)

---

### 10. 통계 분석

#### 기본 모형 (ANOVA)
- **모형:** ln(PK parameter) = sequence + subject(sequence) + period + treatment + ε
- **Log 변환:** 모든 PK 파라미터 자연로그 변환 후 분석
- **90% CI:** 역변환(antilog)하여 원래 척도의 GMR 90% CI 계산
- **소프트웨어:** SAS PROC MIXED (또는 GLM) 권장

#### Fixed Effects
- Sequence (순서)
- Period (투여기)
- Treatment (시험약 vs 대조약)

#### Random Effects
- Subject within sequence (개체)

#### 검정 통계
- Schuirmann's two one-sided tests (TOST)
- 유의수준: 각 one-sided test α = 0.05

#### 결과 보고
- GMR (Geometric Mean Ratio)
- 90% CI (하한, 상한)
- 피험자별 AUC, Cmax 원시 데이터 및 로그 변환값
- ANOVA 표

---

### 11. Product-Specific Guidance (PSG) 참조

- FDA는 특정 기 허가 약물에 대한 **Product-Specific Guidance (PSG)** 발행
- PSG는 이 일반 가이드라인에 우선하여 적용
- 접근: https://www.accessdata.fda.gov/scripts/cder/psg/
- PSG에 명시된 경우: 권장 시험 설계, 특수 BE 기준, 추가 요건 등 포함

---

## 주요 참고 기준 정리

| 항목 | 기준 |
|------|------|
| 표준 BE 90% CI | 80.00 ~ 125.00% |
| HVD RSABE 정의 기준 CV | ≥ 30% (σ_wR ≥ 0.294) |
| RSABE regulatory constant θ | 0.760 (FDA 적용) |
| HVD RSABE cap (최대 허용 범위) | 69.84 ~ 143.19% |
| NTI 약물 설계 | Fully replicate 4-period crossover |
| 장기 반감기 약물 truncated AUC | t½ > 24시간; AUC₀₋₇₂h 허용 |
| 공복 조건 | 투약 전 10시간 이상 금식 |
| 식후 시험 고지방식 | 800~1,000 kcal, 지방 약 50% |
| ANOVA 모형 고정 효과 | Sequence, Period, Treatment |
| 로그 변환 | 자연로그(ln) |

---

## 주의 사항

1. **PSG 우선 적용:** 해당 약물의 PSG가 존재하는 경우, PSG 요건이 이 일반 가이드에 우선함.
2. **HVD RSABE:** Cmax에만 일반적으로 허용; AUC에 적용 시 별도 과학적 근거 필요.
3. **통계 소프트웨어:** SAS의 경우 PROC MIXED 사용; R의 경우 `lme4` 등 동등한 혼합효과 모형.
4. **생물학적 제제:** 이 가이드는 소분자 화합물(small molecule)에 주로 적용되며, 생물의약품(biologics)은 별도 가이드 적용.
5. **추가 강도(additional strength):** 일부 경우 lowest strength 시험 후 약동학적 선형성(linearity) 입증으로 상위 강도 biowaiver 가능.
6. **2022년 버전:** 2013년 초판 대비 개정 주요 사항 — 성별 및 연령 관련 시험 집단 요건 명확화, 변형 방출 추가 강도에 대한 BE 평가 명확화.

---

## 참고 문헌

- FDA. (2022). *Bioequivalence Studies with Pharmacokinetic Endpoints for Drugs Submitted Under an ANDA*. CDER. https://www.fda.gov/media/164681/download
- FDA. (2003). *Bioavailability and Bioequivalence Studies for Orally Administered Drug Products — General Considerations*. CDER.
- FDA PSG Database: https://www.accessdata.fda.gov/scripts/cder/psg/
