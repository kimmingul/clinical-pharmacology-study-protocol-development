# ICH M12 Drug Interaction Studies (2024)

## 출처
- 문서명: ICH M12 Guideline on Drug Interaction Studies
- 발행 기관: ICH (International Council for Harmonisation of Technical Requirements for Pharmaceuticals for Human Use)
- 발행일: 2024 (Step 4 최종, 구체적 날짜 확인 필요)
- 원문 URL: https://www.ich.org/page/multidisciplinary-guidelines (M12 섹션)
- 마지막 검증일: 2026-04-14
- 비고: FDA 2020 가이드라인 및 EMA 2012 가이드라인을 국제 조화 관점에서 통합/대체하는 방향. trial_info.md에는 "2024, Step 4"로 기재됨. [발행일 세부 확인 필요]

---

## 핵심 요건 요약

ICH M12는 in vitro 및 임상 DDI 평가를 하나의 통합 가이드라인으로 제공하는 국제 조화 문서이다. FDA(2020)와 EMA(2012)의 핵심 요건을 단일 프레임워크로 조화시켰으며, 새로운 약물상호작용 평가 방법론을 반영하였다.

### 1. 통합 프레임워크 주요 특징

| 항목 | ICH M12 접근 |
|------|------------|
| 문서 구조 | In vitro + 임상 DDI를 단일 문서로 통합 (FDA 2020은 별도 분리) |
| 국제 조화 | FDA/EMA/PMDA/MFDS 공동 가이드라인 — 허가 기관 간 중복 시험 최소화 |
| PBPK | 통합적 활용 지침 제공; 임상 시험 대체/보완 근거로 사용 가능 |
| 새 수송체 | OCT1 평가 권고 명시 (FDA 2020 대비 강화) |
| UGT | 기질 의사결정 체계 도입 (EMA는 억제만 있었음) |

### 2. In Vitro 기준 (조화된 기준)

#### CYP 억제

| 기준 | 수식 | 임상 시험 조건 |
|------|------|-------------|
| 가역적 억제 | R₁ = 1 + (Imax,u / Ki,u) | ≥ 1.02 |
| 장관 억제 | R₂ = 1 + (Igut / Ki) | ≥ 11 |
| TDI | AUCR 예측 | ≥ 1.25 |

#### 평가 대상 효소

- CYP1A2, CYP2B6, CYP2C8, CYP2C9, CYP2C19, CYP2D6, CYP3A4/5 (7종 기본)
- 유도: CYP1A2, CYP2B6, CYP3A4 (주요), CYP2C9/2C19 (추가 권고)

#### 수송체

| 수송체 | 평가 기준 |
|--------|---------|
| P-gp, BCRP | 모든 신약 필수 |
| OATP1B1, OATP1B3 | 간 배설 관련 |
| OCT1 | **새로 추가** — 간 흡수에서 역할 명확화 |
| OCT2, OAT1, OAT3 | 신장 분비 관련 |
| MATE1, MATE2-K | Imax,u/IC₅₀ ≥ 0.1 |

### 3. 임상 DDI 설계 국제 조화 원칙

| 항목 | ICH M12 원칙 |
|------|------------|
| 설계 선택 | Perpetrator 특성에 따른 risk-based 접근 |
| Fixed-sequence | 강력 억제제/유도제 perpetrator 시 표준 |
| No-effect boundary | 90% CI **0.80~1.25** (표준) |
| NTI 기질 | 더 엄격한 기준 (예: 0.90~1.11) |
| Washout | 억제제/기질 최소 5 반감기 |
| 억제제 전투여 | 정상상태 도달 후 기질 투여 |

### 4. 대사체 DDI 평가 기준 (ICH M12 조화 입장)

| 기준 | ICH M12 | FDA | EMA |
|------|---------|-----|-----|
| 주요 순환 대사체 | ≥25% (FDA와 조화) | ≥25% | ≥25% 또는 ≥10% |

### 5. PBPK 활용

- 임상 DDI 시험 설계 최적화 및 특수 집단 외삽에 활용
- 적절히 검증된 PBPK 모델은 임상 시험 면제 근거로 활용 가능 (규제 기관 사전 협의 권장)
- 국제 공동 허가 시 단일 PBPK 분석으로 복수 기관 제출 가능

### 6. CYP 다형성 및 유전체 고려사항

- CYP2C19, CYP2D6, CYP2C9: 주요 다형성 효소
- 연구 대상자 선정 시 표현형 분층 권고
- PM(poor metabolizer) 집단 별도 분석 권고

---

## 본 시험(Clopidogrel-Omeprazole DDI)에 적용되는 항목

| 항목 | 적용 내용 |
|------|----------|
| 국제 제출 기반 | ICH M12 준수 시 FDA/EMA/MFDS 공동 제출 용이 |
| Fixed-sequence 설계 | ICH M12 원칙에 부합 — Omeprazole 정상상태 후 Clopidogrel 단회 투여 |
| 활성 대사체 평가 | H4 대사체 ≥25% 기준 충족 → 별도 평가 대상 |
| No-effect boundary | 90% CI 80~125% (표준) 적용 |
| CYP2C19 분층 | ICH M12 권고에 따라 EM/IM/PM 표현형별 분석 실시 |
| PBPK 보완 | 기존 임상 데이터 검증 목적으로 PBPK 보조 활용 가능 |
| 수송체 평가 | CYP2C19 기반 DDI이므로 추가 수송체 영향 최소화 예상 (확인 필요) |

---

## 다른 가이드라인과의 차이점

| 항목 | ICH M12 | FDA 2020 | EMA 2012 |
|------|---------|----------|----------|
| 문서 구조 | 통합 (in vitro + 임상) | 분리 (별도 2개 문서) | 통합 |
| OCT1 평가 | 명시적 권고 | 언급 있음 | 선택적 |
| UGT 기질 | 체계 도입 | 체계 있음 | 억제만 |
| BSEP | 언급 필요 [확인 필요] | 없음 | 필수 |
| 국제 조화 | 최고 수준 | FDA 단독 | EMA 단독 |
| 발행 시기 | 2024 (최신) | 2020 | 2012 |

---

## 참고 문헌

- ICH. ICH M12 Guideline on Drug Interaction Studies. International Council for Harmonisation; 2024.
- [ICH M12 Drug Interaction Studies, ICH, 2024]
- 비고: 원문 전문 미수집. 가이드라인 핵심 내용은 공개 ICH 문서 및 관련 학술 자료를 통해 재구성. 정확한 조항은 원문 확인 필요.
