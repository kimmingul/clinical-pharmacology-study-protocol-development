# FDA Clinical Drug Interaction Studies Guidance (2020)

## 출처
- 문서명 (In Vitro): In Vitro Drug Interaction Studies — Cytochrome P450 Enzyme- and Transporter-Mediated Drug Interactions
- 문서명 (Clinical): Clinical Drug Interaction Studies — Cytochrome P450 Enzyme- and Transporter-Mediated Drug Interactions
- 발행 기관: FDA CDER
- 발행일: 2020-01 (Final)
- 원문 URL (In Vitro): https://www.fda.gov/media/135587/download
- 원문 URL (Clinical): https://www.fda.gov/media/135588/download
- 마지막 검증일: 2026-04-14
- 비고: ICH M12 (2024 Step 4) 발행으로 향후 본 가이드라인을 보완/대체할 예정

---

## 핵심 요건 요약

### 1. In Vitro 스크리닝 기준

#### CYP 억제 트리거

| 기준 | 수식 | 임상 시험 권고 조건 |
|------|------|-------------------|
| 가역적 억제 (R1) | R1 = 1 + (Imax,u / Ki,u) | ≥ 1.02 |
| 장관 억제 (R2) | R2 = 1 + (Igut / Ki) | ≥ 11 |
| 시간의존적 억제 (TDI) | AUCR 예측 | ≥ 1.25 |

- Imax,u: 최고 비결합형 혈장 농도
- Igut = dose / 250 mL (장내 추정 농도)
- 비결합형(unbound) 농도 사용 권장

#### 수송체 억제 트리거

| 수송체 | 트리거 기준 |
|--------|-----------|
| P-gp / BCRP (경구) | Igut / IC₅₀ ≥ 10 |
| P-gp / BCRP (정맥/대사체) | I₁ / IC₅₀ ≥ 0.1 |
| OATP1B1 / OATP1B3 | R = 1 + (Imax,u / IC₅₀) > 1.1 |
| OAT1, OAT3, OCT2, MATE1, MATE2-K | Imax,u / IC₅₀ ≥ 0.1 |

**2020년 주요 변경**: MATE 트리거 기준 0.02 → 0.1로 상향 조정

#### CYP 유도 판정 기준

| 기준 | 조건 |
|------|------|
| mRNA 증가 | ≥ 2배 농도 의존적 증가 |
| 양성 대조 대비 | ≥ 20% 증가 (2배 미만이라도) |

- 평가 효소: CYP1A2, CYP2B6, CYP3A (주요 3종)
- 양성 대조: CYP1A2 → Omeprazole; CYP2B6 → Phenobarbital; CYP3A → Rifampin

### 2. 임상 DDI 시험 설계

#### 설계 유형

| 설계 | 적용 조건 |
|------|----------|
| One-sequence (fixed-sequence) | 반감기 긴 기질; 강력 억제제/유도제 사용 시 일반적 |
| Two-period crossover | 기질 PK 예측 가능; 충분한 washout 가능 |
| Parallel | 장기 반감기 기질; crossover 비현실적 |

- Washout: 최소 5 반감기 (억제제 및 기질 모두)
- 억제제 정상상태 도달 후 기질 투여 원칙

#### No-Effect Boundary

| 기준 | 수치 |
|------|------|
| 표준 기준 | GMR 90% CI: **0.80 ~ 1.25** |
| NTI 기질 | 더 좁은 범위 (**0.90 ~ 1.11**) 고려 |

#### GMR 해석 기준 (억제)

| GMR 범위 | 분류 | 라벨 조치 |
|----------|------|----------|
| ≤ 1.25배 | 임상적으로 무의미 | 라벨 기재 불필요 |
| 1.25 ~ 2배 | 약한(weak) 억제 | 경고 또는 용량 조정 고려 |
| 2 ~ 5배 | 중등도(moderate) 억제 | 용량 조정 / 모니터링 라벨 기재 |
| > 5배 | 강한(strong) 억제 | 병용 금기 또는 대폭 감량 |
| > 80% 감소 | 강한 유도 | 병용 금기 또는 용량 증가 |

#### CYP2C19 Index Substrates

| CYP | Sensitive Substrate | Strong Inhibitor |
|-----|---------------------|-----------------|
| CYP2C19 | Omeprazole, Lansoprazole | Fluvoxamine, Fluconazole |

### 3. PBPK 모델링

- 임상 DDI 시험 대체 허용 (사전 FDA 협의 권장)
- 특수 집단 외삽, 혼합 DDI 예측에 활용 가능
- 검증 기준: 관찰 PK 대비 AUC / Cmax 2배 이내 예측 정확도

---

## 본 시험(Clopidogrel-Omeprazole DDI)에 적용되는 항목

| 항목 | 적용 내용 |
|------|----------|
| 시험 설계 | Fixed-sequence (one-sequence) crossover 설계 권장 — Omeprazole이 CYP2C19 저해제(perpetrator)이므로 정상상태 후 Clopidogrel 투여 |
| 억제제 전투여 | Omeprazole 정상상태 도달을 위해 5~7일 전투여 필수 |
| 평가변수 1차 | AUC₀₋∞ (또는 AUC₀₋ₜ) GMR 및 90% CI |
| 평가변수 2차 | Cmax GMR 및 90% CI |
| No-effect boundary | 90% CI **80~125%** 벗어나면 임상적으로 유의한 DDI로 판정 |
| 활성 대사체 | 활성 대사체(H4) AUC/Cmax 반드시 측정 (모약물 + 대사체 모두) |
| 통계 | ln 변환 후 ANOVA 또는 paired t-test, GMR 및 90% CI 보고 |
| CYP2C19 분층 | 표현형(EM/IM/PM) 분층 분석 권장 |
| PBPK 활용 | 기존 임상 데이터가 충분하므로 PBPK는 보조 목적으로 제한 |

---

## 다른 가이드라인과의 차이점

| 항목 | FDA (본 가이드) | MFDS | EMA |
|------|--------------|------|-----|
| PBPK 수용도 | 임상 시험 대체 허용 (사전 협의) | 보조 근거만 허용 | 지지적 도구, 혼합 DDI에 in vivo 필수 |
| 농도 지표 | Imax,u (비결합형 권장) | 명시 없음 (총 농도 관행) | 비결합 농도(Cmax,u) 명시 |
| 유도 평가 효소 | CYP1A2, 2B6, 3A (3종) | 동일 | CYP1A2, 2B6, 2C9, 2C19, 3A4 (5종) |
| BSEP 평가 | 별도 요건 없음 | 별도 언급 없음 | **필수 평가** |
| MATE 트리거 | 0.1 (2020년 상향) | 동일 | 선택적 평가 |
| No-effect boundary | 80~125% | 80~125% | 0.5~2.0배 (서술적) |

---

## 참고 문헌

- FDA. (2020). *Clinical Drug Interaction Studies — Cytochrome P450 Enzyme- and Transporter-Mediated Drug Interactions*. CDER.
- FDA. (2020). *In Vitro Drug Interaction Studies — Cytochrome P450 Enzyme- and Transporter-Mediated Drug Interactions*. CDER.
- [FDA DDI Guidance, FDA CDER, 2020-01]
