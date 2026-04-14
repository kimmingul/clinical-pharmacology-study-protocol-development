# EMA Guideline on the Investigation of Drug Interactions (2012)

## 출처
- 문서명: Guideline on the Investigation of Drug Interactions
- 문서 번호: CPMP/EWP/560/95/Rev. 1 Corr. 2
- 발행 기관: EMA CHMP (Committee for Medicinal Products for Human Use)
- 발행일: 2012-06 (채택), 2015-06 (마지막 수정)
- 원문 URL: https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-investigation-drug-interactions-revision-1_en.pdf
- 마지막 검증일: 2026-04-14
- 비고: Rev. 2 개정 진행 중 (2017년 Concept paper 발행). ICH M12 (2024 Step 4) 참조 권고.

---

## 핵심 요건 요약

### 1. In Vitro 평가 체계

#### CYP 억제 트리거 (가역적)

| 기준 | 수식 | 임상 시험 조건 |
|------|------|--------------|
| Basic Model (R₁) | R₁ = 1 + (I / Ki,u) | ≥ 1.02 → 임상 DDI 또는 추가 평가 |
| 장 기여 (R₁,gut) | 복잡 공식 (Ka, Vgut 기반) | ≥ 11 → 장 CYP3A 억제 임상 고려 |
| TDI/MBI (R₂) | R₂ = 1/(1+kinact×[I]/(KI+[I])/kdeg) | ≥ 1.25 → TDI 임상 필요 |

- I: 최고 **비결합형** 혈장 농도 (Cmax,u) — EMA는 비결합 농도 기반 명시
- 유도 판정: R₃ = 1/(1+d×Emax×C/(EC₅₀+C)) ≤ 0.8 → 임상 유도 평가 필요

#### 평가 대상 CYP 효소

| 구분 | 효소 종류 |
|------|----------|
| 가역적 억제 필수 | CYP1A2, 2B6, 2C8, 2C9, 2C19, 2D6, 3A4 (7종) |
| 유도 평가 | CYP1A2, 2B6, 2C9, 2C19, 3A4 (5종) — **FDA보다 광범위** |
| UGT | UGT1A1, UGT2B7 억제 시험 권고 (기질 체계 없음) |

#### 수송체 필수 평가 (BSEP 포함)

| 수송체 | 임계 조건 |
|--------|----------|
| P-gp, BCRP | 모든 신약 |
| OATP1B1, OATP1B3 | 간 배설 ≥25% |
| OCT2, OAT1, OAT3 | 신장 분비 ≥25% |
| **BSEP** | **필수 평가 (EMA 전용; 간독성 목적)** |

- P-gp/BCRP 억제 기준: 50×Cmax,u 농도에서 R ≥ 1.25
- OATP1B1/3 억제: 25×Cmax,u 기준

#### 대사체 DDI — 이중 기준 (FDA보다 엄격)

| 기준 | EMA | FDA |
|------|-----|-----|
| 대사체 평가 역치 | 모약물 AUC의 ≥25% **또는** 총 순환 ≥10% (이중) | 모약물 AUC의 ≥25% (단일) |

### 2. 임상 DDI 시험 설계

#### 기본 원칙

| 항목 | EMA 요건 |
|------|----------|
| 시험 대상자 | 건강 성인 자원자 원칙 |
| 기본 설계 | 교차 설계 우선; 개방 또는 맹검 모두 허용 |
| Washout 기간 | 억제제: t½의 5배 이상; 유도제: 유도 효과 소실 시까지 |
| 유도제 3-arm 설계 | **권고** (단독/유도제+기질/유도제 중단 후) |

#### CYP2C19 Index Substrates

| CYP | 권고 기질 |
|-----|----------|
| CYP2C19 | Omeprazole, Lansoprazole |

#### 혼합 억제/유도 효과

- EMA: PBPK 만으로 불충분 → **in vivo 임상 시험 필수** (FDA와의 핵심 차이점)

### 3. No-Effect Boundary 및 GMR 해석

| 상호작용 크기 | 권고 라벨 내용 |
|--------------|-------------|
| AUC > 5배 증가 | 병용 금기 (contraindicated) |
| AUC 2~5배 증가 | 병용 주의, 용량 조정 권고 |
| AUC 1.25~2배 증가 | 병용 주의, 모니터링 권고 |
| AUC < 1.25배 변화 | 일반적으로 임상적으로 무의미 |
| GMR 0.5~2.0 | 임상적으로 유의한 상호작용 경계 |

### 4. CYP 다형성 고려사항

- CYP2C9, CYP2C19, CYP2D6: 유전형/표현형 검사 권고
- 다형성 효소 주 대사 약물: 표현형 집단별 분리 보고 권고
- UGT1A1, OATP1B1 (SLCO1B1) 수송체 다형성 고려

### 5. SmPC 반영 기준

- 섹션 4.5: 다른 약물과의 상호작용 (정량적 데이터 포함)
- 섹션 4.4: 특별 경고 (중증 상호작용)
- 섹션 5.2: PK 정보 (in vitro 데이터 포함)

---

## 본 시험(Clopidogrel-Omeprazole DDI)에 적용되는 항목

| 항목 | 적용 내용 |
|------|----------|
| Victim/Perpetrator 역할 | Clopidogrel = victim (기질), Omeprazole = perpetrator (CYP2C19 저해제) |
| 시험 설계 | 교차 설계 (fixed-sequence): Omeprazole 정상상태 → Clopidogrel 투여 |
| Washout 기간 | Omeprazole t½ (~1 hr) × 5 = ~5 hr; 혈소판 수명 고려 ≥14일 필요 |
| CYP2C19 다형성 | EMA 권고에 따라 CYP2C19 표현형(EM/IM/PM) 분층 분석 실시 |
| 활성 대사체 평가 | Clopidogrel 활성 대사체(H4)가 pharmacologically active → 대사체 AUC/Cmax 측정 필수 |
| PD 평가 | VerifyNow P2Y12 활성 검사(PRU)를 PK와 병행 — EMA DDI 가이드라인상 PD-DDI 평가 포함 |
| 라벨 반영 | 결과에 따라 SmPC 섹션 4.5에 정량적 데이터 기재 |
| BSEP | 다국가 허가 시 BSEP 억제 데이터 추가 고려 |

---

## 다른 가이드라인과의 차이점

| 항목 | EMA (본 가이드) | FDA | MFDS |
|------|--------------|-----|------|
| 혼합 억제/유도 | **In vivo 필수** | PBPK 허용 | PBPK 보조 활용 |
| BSEP 평가 | **필수** | 불필요 | 언급 없음 |
| CYP 유도 평가 효소 | 5종 (CYP2C9, 2C19 포함) | 3종 | 3종 |
| No-effect boundary | 0.5~2배 (서술적) | 80~125% (명시적) | 80~125% (명시적) |
| 대사체 DDI | 이중 기준 (≥25% 또는 ≥10%) | 단일 기준 (≥25%) | 명시 없음 |
| PBPK 역할 | 지지적 도구 | 주된 도구 인정 | 제한적 |
| 유도 mRNA 기준 | Rifampin 대비 CYP3A4 > 40% | ≥2배 또는 양성 대조 20% | 동일 |
| 농도 지표 | **비결합 농도 명시** | 비결합 권장 | 불명확 |

---

## 참고 문헌

- EMA. Guideline on the Investigation of Drug Interactions (CPMP/EWP/560/95/Rev. 1 Corr. 2). European Medicines Agency; 2012.
- [Guideline on the Investigation of Drug Interactions, EMA CHMP, 2012-06]
