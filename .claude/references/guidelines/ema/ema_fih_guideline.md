# Guideline on Strategies to Identify and Mitigate Risks for First-in-Human and Early Clinical Trials with Investigational Medicinal Products

## 메타 정보

| 항목 | 내용 |
|------|------|
| 발행 기관 | EMA CHMP (Safety Working Party, SWP) |
| 문서명 | Guideline on Strategies to Identify and Mitigate Risks for First-in-Human and Early Clinical Trials with Investigational Medicinal Products |
| 문서 번호 | EMEA/CHMP/SWP/28367/07 Rev. 1 |
| 발행일 | 2017-07-25 |
| 발효일 | 2018-02-01 |
| 원문 URL | https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-strategies-identify-and-mitigate-risks-first-human-and-early-clinical-trials-investigational-medicinal-products-revision-1_en.pdf |
| 마지막 검증일 | 2026-04-13 |
| 협력 기관 | EU Clinical Trials Facilitation Group (CTFG, 현 CTCG) |
| 비고 | 2007년 초판 → 2017년 대폭 개정 (TGN1412, BIA 10-2474 사례 반영) |

## 적용 범위

- 인체 최초 투여(FIH) 이전 비임상 및 임상 고려사항
- 초기 임상시험(Phase I/IIa) 전 과정: SAD, MAD, 통합 프로토콜
- 신약(NCE) 및 바이오의약품(biologics) 모두 포함
- 건강인 자원자 및 환자 집단 대상 시험
- 단계적 용량 증량(dose escalation) 시험 및 복합(integrated) 프로토콜

---

## 1. 위험 식별 (Risk Identification)

### 1.1 약리학적 위험 평가 요소

| 평가 요소 | 핵심 고려사항 |
|-----------|---------------|
| 작용 기전(MoA) | 1차 표적 활성화/억제의 예상 생리적 결과; 수용체 하위 유형 선택성 |
| 표적 특성 | 수용체/효소/채널의 발현 부위, 생리적 역할, 밀도 |
| 2차 약리 | 원치 않는 off-target 결합 및 예상 결과 |
| 안전 약리 | CVS (hERG, QT), CNS, 호흡기 계통 영향 |
| 종간 차이 | 동물 모델의 인체 예측성 (수용체 상동성, 발현 패턴) |
| 표적 선택성 | 선택성 마진; 표적 포화(saturation) 농도 |

### 1.2 PK/PD 특성 위험 요인

- **지속성 효과**: 표적 회전율(turnover) 낮아 혈중 소실 후에도 약리 효과 지속
  - 사례: BIA 10-2474의 FAAH 억제 — 혈중 완전 소실 후 24시간 이상 억제 지속
- **비선형 PK**: 용량-노출 비례성 이탈 구간 (포화, 자기 억제 등)
- **느린 표적 해리**: 수용체와 의약품 간 결합·해리 동역학

### 1.3 면역원성/바이오마커 위험

- 사이토카인 폭풍 가능성 (T cell, NK cell 활성화 유발 약물)
- 면역계 자극 정도의 동물 예측성 한계
- TGN1412 교훈: 동물에서 표적 발현 없음 → 인체 초면역 반응 예측 불가

### 1.4 제형 위험

- 비임상 시험 제형과 임상 제형의 차이가 PK에 미치는 영향
- 용해도, 안정성, 용기 흡착 등
- 용량 유연성을 위한 희석 위험

---

## 2. 시작 용량 산출 방법 (Starting Dose Calculation)

### 2.1 방법 선택 원칙

> 불확실성 수준과 인체 관련성에 따라 적절한 방법 선택:
> - 표준 소분자: NOAEL 기반 HED + 안전계수
> - 고도 표적 선택적 약물: MABEL 우선
> - 불확실성 높은 생물의약품: MABEL + PAD 병용

**핵심 원칙**: 여러 방법으로 계산한 시작 용량이 다를 경우, **가장 낮은 값** 사용 (과학적 정당화 없이 더 높은 값 선택 불가)

### 2.2 NOAEL → HED (Human Equivalent Dose) 방법

**적용 대상**: 표준 소분자 신약, 동물 모델의 인체 예측성이 합리적인 경우

**계산 절차:**

1. **NOAEL 결정**: 주요 독성 동물 시험(일반독성, 안전 약리)에서 무독성량 확인
2. **HED 변환**: 체표면적(BSA) 기반 종간 스케일링

| 동물 종 | Km 계수 | HED 변환 공식 |
|---------|---------|---------------|
| 마우스 | 3 | HED = NOAEL(mg/kg) × (3/37) |
| 랫트 | 6 | HED = NOAEL(mg/kg) × (6/37) |
| 토끼 | 12 | HED = NOAEL(mg/kg) × (12/37) |
| 비글견 | 20 | HED = NOAEL(mg/kg) × (20/37) |
| 원숭이 | 12 | HED = NOAEL(mg/kg) × (12/37) |
| 인간 | 37 | — |

3. **안전계수 적용**: 최소 10분의 1 (HED의 1/10)
   - 안전계수 조정 근거: 약리작용 특성, 종간 차이, 독성 심각도/가역성, 노출 마진

**한계점**: 표적이 동물에 없거나 발현 패턴이 다른 경우 예측성 불충분

### 2.3 MABEL (Minimum Anticipated Biological Effect Level) 방법

**정의**: 인체에서 최소한의 생물학적 효과를 야기할 것으로 예상되는 용량 수준

**적용 대상**:
- 표적 선택성이 매우 높고 사이토카인 폭풍 등 면역 반응 위험이 있는 약물
- 작용 기전상 T세포, NK세포 등 면역계 직접 자극 약물
- TGN1412 같은 agonistic 항체 등 바이오의약품
- 동물 모델의 인체 예측성이 낮은 경우

**MABEL 계산 데이터 소스 (모든 이용 가능한 정보 통합):**
- In vitro 수용체 결합 친화도(Kd, IC₅₀, EC₅₀)
- In vitro 세포 기반 검사에서의 활성 농도
- In vivo 동물 PK/PD 데이터
- 수용체 점유율(receptor occupancy)–효과 관계

**계산 원칙:**
- 모든 관련 in vitro, in vivo 데이터의 통합적 해석
- 가장 민감한 검사(most sensitive assay)에서의 최소 활성 농도 사용
- 비결합 농도(free concentration) 기준 적용 권고

### 2.4 PAD (Pharmacologically Active Dose) 방법

**정의**: 인체에서 측정 가능한 약리적 효과를 유발할 것으로 예상되는 용량

**관계**: MABEL < PAD < 치료 용량(anticipated therapeutic dose)

**적용**: MABEL 계산이 어렵거나 MABEL과 PAD를 함께 고려하여 시작 용량 결정

### 2.5 ATD (Anticipated Therapeutic Dose) — 신개념

**정의**: 임상적으로 의미 있는 치료 효과를 예상하는 용량

- 시작 용량은 ATD를 초과하지 않아야 함
- PAD를 통해 ATD 추정 가능

---

## 3. 용량 증량 전략 (Dose Escalation Strategy)

### 3.1 초기 용량 단계

**권고 최대 증량 규모**: 일반적으로 단계당 최대 100% (2배) 증량
- 낮은 용량 범위: 더 큰 폭 증량 가능 (비선형 구간 이전)
- 표적 포화 접근 시: 더 작은 폭 (최대 50% 이하)
- 비선형 PK 관찰 시: 더 작은 폭

**증량 결정 근거 (종합 평가):**
- 예측 vs. 실측 노출(AUC, Cmax, Cmin) 비교
- 용량-노출 비례성 (선형성 여부)
- 노출-효과 관계 (PD 바이오마커)
- 안전성 데이터 (AE 발생 및 중증도)

### 3.2 특수 상황 증량 기준

| 상황 | 권고 증량 폭 |
|------|-------------|
| 표적 포화 접근 | ≤50% 또는 그 이하 |
| 비선형 PK 전환점 | ≤50% |
| 최대 계획 노출 근접 | 세밀한 단계 증량 |
| 1차 중지 기준에 근접 | 단계 보류 또는 소규모 증량 |

### 3.3 최대 노출 한계

- 프로토콜에 사전 정의된 최대 노출(Cmax, AUC) 초과 시: 중대한 개정(substantial amendment) 및 규제 정당화 필요
- 수퍼치료 용량(supra-therapeutic dose): 안전성 마진이 충분하고 PK 선형성이 입증된 경우 탐색 가능

---

## 4. 센티넬 도징 (Sentinel Dosing)

### 4.1 정의 및 목적

- 동일 코호트 내에서 전체 대상자에게 동시 투여하기 전, 1–2명의 선도(sentinel) 대상자에게 먼저 투약
- 목적: 초기 안전성 신호 포착 → 나머지 대상자 보호

### 4.2 권고 적용 시점

| 상황 | 센티넬 도징 권고 |
|------|-----------------|
| 표적 포화 접근 시 | 강력 권고 |
| 최대 계획 노출 도달 시 | 강력 권고 |
| 비선형 PK 전환점 도달 시 | 강력 권고 |
| 모든 코호트 진입 시 | 권고 (정당화 없으면 필수) |

### 4.3 센티넬 도징 면제 조건

- 충분한 약물의 약리학적 안전성 프로파일 사전 지식
- 면제 기준은 프로토콜(또는 개정본)에 명시하고 규제 심사의 일부로 승인 필요

### 4.4 실제 구현

- 센티넬 1–2명 투약 후 관찰 기간 (통상 24–48시간, 약물 특성에 따라 조정)
- 선도 대상자 안전성 확인 후 나머지 코호트 투약 진행
- MAD(다회 투약) 시험에서도 첫 회 또는 증량 시점에 적용 가능

---

## 5. 안전성 검토위원회 (Safety Review Committee, SRC / DSMB)

### 5.1 위원회 구성 요건

- 의뢰자(sponsor)로부터 독립적인 전문가 구성 필수
- 프로토콜에 구성의 적절성 문서화 및 정당화 필요
- **권고 구성원:**
  - 임상 약리학자
  - 관련 전문과목 임상의
  - 통계학자 (맹검 해제 담당)
  - 필요 시: 약리독성학자, 면역학자 등

### 5.2 역할 및 의사결정

- 각 코호트 완료 후 누적 안전성 데이터 검토
- 용량 증량 승인/보류/중단 결정
- 의사결정 근거 문서화 (GCP 실사 대비 기록 유지)
- **의사결정 기록**: "다음 용량으로의 진행 근거를 기록하여 향후 GCP 실사에서 열람 가능하도록"

### 5.3 데이터 검토 요건

- 진행 전 전체 안전성 데이터 검토 필수
- 부분적 PK 데이터 및 PD 데이터도 충분한 정당화 하에 허용
- **"Totality of safety data"**: 안전성 데이터 전체의 종합 검토

---

## 6. 안전성 모니터링 요건

### 6.1 노출 기반 모니터링

- 투여 용량이 아닌 **실측 노출(AUC, Cmax)** 기준 안전성 모니터링
- 프로토콜에 최대 노출 한계 사전 정의 필수
- 노출-반응 관계에서의 PD 바이오마커 통합

### 6.2 모니터링 지속 기간 및 장소

- 약물의 예상 위험 프로파일에 따라 정당화된 기간 설정
- 약리 활성이 지속되는 경우 (예: 지속적 수용체 결합) 더 긴 관찰 기간 필요
- 시설 적절성: 응급 처치 장비 및 의료 지원 인프라 문서화

### 6.3 PD 바이오마커 통합

**가이드라인이 권장하는 PD 바이오마커 역할:**
- 동물 시험에서의 가정 검증
- 1차 약리 효과 모니터링
- 임상적으로 의미 있는 2차 효과 조기 감지
- 용량 조정을 위한 실시간 정보 제공

---

## 7. 중지 규칙 (Stopping Rules)

### 7.1 중지 수준

| 수준 | 내용 |
|------|------|
| **개인 중지** | 개별 대상자의 사전 정의된 AE 임계값 도달 시 해당 대상자 투약 중단 |
| **코호트 중지** | 동일 코호트 내 추가 대상자 투약 중단 |
| **시험 중지** | 전체 시험 또는 다음 단계 진행 중단 |

### 7.2 중지 기준 정의 원칙

- **DLT(Dose-Limiting Toxicity)**: 표준화된 등급 체계(예: NCI CTCAE v5.0) 기반 정의
- **중증도 임계값**: AE 심각도(Grade 2 이상 등), 빈도, 지속 기간 포함
- 예시: 중등도(moderate) 이상 AE 발생 시 코호트 중지 고려
- **약리학적 기전 연계 AE**: 1차 또는 2차 약리 표적 관련 독성은 특히 중지 기준으로 적극 고려

### 7.3 통신 계획 (Communication Plan)

**BIA 10-2474 사건 교훈 반영:**
- 연구자-의뢰자-CRO-윤리위원회-규제당국 간 정보 흐름 명확히 정의
- 긴급 상황 시 에스컬레이션 절차 명시
- 투명성 실패가 TGN1412, BIA 10-2474에서 심각한 결과 초래

---

## 8. 바이오의약품 특이 요건

### 8.1 바이오의약품 위험 프로파일 특성

| 특성 | 고려사항 |
|------|----------|
| 면역원성 | ADA(항약물항체) 발생으로 PK/PD 변화; 아나필락시스 위험 |
| 사이토카인 방출 | T세포/NK세포 활성화 약물에서 사이토카인 폭풍 위험 |
| 표적 발현 차이 | 동물-인체 표적 발현 및 분포 차이 → 인체 예측성 제한 |
| 지속성 억제 | 지속 반감기 약물 또는 내재화(internalization) 후 효과 지속 |

### 8.2 바이오의약품 시작 용량

- **MABEL 방법 우선** 적용 (NOAEL 방법 단독 사용 불충분)
- 수용체 점유율(Receptor Occupancy, RO) 기반 MABEL 계산
- 목표 RO < 10% (안전 마진 확보)
- 인체 조직(post-mortem 등)에서의 수용체 발현 데이터 활용

### 8.3 센티넬 도징 및 코호트 내 간격

- 바이오의약품, 특히 면역 자극성 생물의약품에서 센티넬 도징 **강력 권고**
- 코호트 내 투약 간격: 면역 반응의 초기 징후 관찰 시간 충분히 확보
- 면역 조절제(immunomodulator): 더 엄격한 관찰 기간 요구

### 8.4 모노클로날 항체(mAb) 특이 사항

- Fc 기능에 따른 효과기 세포(effector cell) 활성화 위험 평가
- 동물에서 표적이 없는 경우 인체 cross-reactive 연구 필요 (예: 비인간 영장류)
- 사이토카인 프로파일 모니터링: IFN-γ, IL-2, IL-6, TNF-α 등

---

## 9. 통합 프로토콜 (Integrated/Complex Protocols)

### 9.1 정의

- 여러 "study part"를 단일 마스터 프로토콜 아래 수행
- SAD → MAD, 또는 Phase I → IIa를 단일 프로토콜로 통합
- 목적: 개발 효율화, 신속한 PoC(Proof of Concept) 확보

### 9.2 필수 요건

- 각 단계 간 진행 기준(progression criteria) 사전 정의
- 충분한 지식 축적 전 다음 단계 진행 금지
- 의사결정 기준: PK(노출 한계, 선형성), PD(표적 관여, 효과 진행), 안전성
- 추가 인구집단(환자 포함) 포함 시 추가 위험 평가

### 9.3 중대한 개정 요건

- 계획된 최대 노출 초과 시 반드시 규제기관 승인 후 진행
- 예상치 못한 독성 또는 PK 변화 시 개정 및 재승인

---

## 10. 특수 집단 고려사항

### 10.1 건강인 대 환자

| 집단 | 고려사항 |
|------|----------|
| 건강인 자원자 | 기본; 약물 안전성 프로파일 불명확 시 위험 고려 |
| 환자 집단 | 질환에 따른 PK/PD 차이; SAD 후 MAD 보수적 설계 |
| 취약 집단 | 질환 중증도, 동반 약물, 신기능/간기능 장애 고려 |

### 10.2 선정/제외 기준

- 생리적 파라미터: 인구 기반 참고 범위 사용 (질환 진단 범위 아닌)
- 취약성 평가: 질환 상호작용 및 집단 특이적 불확실성 반영

---

## 11. 2007년 초판 대비 2017년 주요 변경사항

| 항목 | 2007년 초판 | 2017년 개정판 |
|------|------------|---------------|
| 적용 범위 | FIH 중심 (주로 비임상) | FIH + 초기 임상 전 과정 (통합 프로토콜 포함) |
| MABEL | 비임상 시작 용량에 한정 | 모든 단계의 용량 결정에 통합 |
| 노출 기반 접근 | 용량 중심 | **노출(AUC, Cmax) 중심**으로 전환 |
| 적응적 설계 | 언급 없음 | 통합 프로토콜 명시적 허용 |
| 통신 계획 | 없음 | **필수 (BIA 10-2474 교훈 반영)** |
| 센티넬 도징 | 개략 언급 | 구체적 요건 명시 |
| 바이오의약품 | 일부 언급 | 더 상세한 요건 제공 |
| SRC/DSMB | 권고 | 구성 적절성 프로토콜 문서화 필수 |

---

## 12. 주요 사례에서의 교훈

### 12.1 TGN1412 (2006년)

- 항-CD28 superagonist mAb
- 원숭이에서 표적(CD28)이 T 조절 세포에 발현 없음 → 인체 초면역 반응 예측 불가
- **교훈**: 동물 모델 예측성 한계 인식 → MABEL 도입의 직접적 계기

### 12.2 BIA 10-2474 (2016년)

- FAAH(지방산 아마이드 가수분해효소) 억제제
- 혈중 소실 후에도 뇌 내 효소 억제 지속 (지속성 표적 결합)
- 5명 심각 신경 독성, 1명 사망
- **교훈**: 혈장 PK와 PD 해리 → 노출 기반 모니터링의 한계 및 조직 분포 중요성; 통신 계획 필요성

---

## 참고 문헌

- EMA. Guideline on Strategies to Identify and Mitigate Risks for First-in-Human and Early Clinical Trials with Investigational Medicinal Products (EMEA/CHMP/SWP/28367/07 Rev. 1). European Medicines Agency; 2017.
- Suntharalingam G, et al. Cytokine storm in a phase 1 trial of the anti-CD28 monoclonal antibody TGN1412. N Engl J Med. 2006;355(10):1018-28.
- Kenter MJH, Cohen AF. Commentary on the EMA Guideline on strategies to identify and mitigate risks for first-in-human and early clinical trials with investigational medicinal products. Br J Clin Pharmacol. 2018;84(9):1909-1916. PMC6005602.
- Muñoz-Sánchez A, et al. The New First-in-Human EMA Guideline: Disruptive or Constructive? Outcomes From the First EUFEMED Discussion Forum. Front Med. 2019;6:39. PMC6491518.
- EMA News. Revised guideline on first-in-human clinical trials. 2017. https://www.ema.europa.eu/en/news/revised-guideline-first-human-clinical-trials
