# E14/S7B Q&As 및 ICH E14 Implementation (FDA 관점)

## 메타 정보

| 항목 | 내용 |
|------|------|
| 발행 기관 | FDA CDER / ICH (International Council for Harmonisation) |
| 문서명 (주요) | E14 and S7B Clinical and Nonclinical Evaluation of QT/QTc Interval Prolongation and Proarrhythmic Potential — Questions and Answers |
| 발행일 | 2022-06 (E14/S7B Q&As, R3) |
| 원문 URL | https://www.fda.gov/media/161198/download |
| 원문 URL (E14 원본) | https://www.fda.gov/media/71379/download |
| 관련 FDA 자료 | https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/interdisciplinary-review-team-cardiac-safety-studies-formerly-qt-irt |
| 참고 문헌 | FDA's insights: implementing new strategies for evaluating drug-induced QTc prolongation (PMC12198268) |
| 마지막 검증일 | 2026-04-13 |

---

## 적용 범위

- 인간 심장 안전성 평가: 약물이 QT/QTc 간격을 연장시킬 가능성(torsades de pointes 유발 위험) 평가
- **ICH E14:** 임상 QT/QTc 평가 (TQT 시험, C-QTc 분석)
- **ICH S7B:** 비임상 QT/QTc 평가 (hERG assay, in vivo QT study)
- **통합 위험 평가:** E14와 S7B를 함께 적용하여 약물의 심장 위험성 종합 평가
- FDA Interdisciplinary Review Team for Cardiac Safety Studies (IRT-CS, 구 QT-IRT)가 검토 수행

---

## 핵심 요건

### 1. 전통적 TQT (Thorough QT/QTc) 시험 요건

#### 기본 설계
- **설계:** 무작위 배정, 위약 대조, 양성 대조 포함, crossover 또는 parallel
- **용량:** 치료 용량(therapeutic dose) 및 고용량(supratherapeutic dose) 포함
  - 고용량: 최고 임상 예상 용량의 2배 이상 (또는 독성 한계 내 최고 용량)
- **평가 집단:** 일반적으로 건강한 성인 자원자

#### 필수 구성 요소
| 구성 요소 | 세부 요건 |
|-----------|-----------|
| 양성 대조약 | 모시플록사신(Moxifloxacin) 400 mg 단회 경구 투여 (일반적) |
| 위약 대조 | 자연적 QTc 변동 통제 |
| 고용량 투여 | 최고 임상 용량의 ≥ 2배 (치료 용량 + 수퍼치료 용량) |
| ECG 기록 | 다중 시점 기록: 투약 전 (baseline), 투약 후 연속 시간대 |
| ECG 판독 | 중앙 집중 판독 (central ECG laboratory) 권장 |
| QTc 보정법 | Fridericia (QTcF) 또는 Bazett (QTcB), 개별 보정(QTcI) |

#### 1차 평가변수
- **ΔΔQTcF (ddQTcF):** 기저치 보정 + 위약 보정 QTcF 간격 변화
  - ΔQTc = QTc (after drug) - QTc (baseline, time-matched)
  - ΔΔQTc = ΔQTc (drug) - ΔQTc (placebo)

---

### 2. ddQTcF 판정 기준 (10ms 임계값)

#### 판정 기준
| 결과 | 해석 | 규제 조치 |
|------|------|-----------|
| ddQTcF 95% CI 상한 < 10 ms | 음성 (Negative TQT 시험) | QTc 우려 없음 |
| ddQTcF 95% CI 상한 ≥ 10 ms | 양성 (Positive) 또는 불확정 | 추가 평가, 라벨 경고 |
| ddQTcF > 20 ms | 상당한 QTc 연장 | 개발 중단 고려 또는 엄격한 규제 조건 |

**10 ms 임계값의 의미:**
- 10 ms 이하의 평균 QTc 연장은 일반적으로 torsades de pointes와 연관된 임상적 위험을 나타내지 않음
- 10 ms 초과: 잠재적 우려이나, 기저 심장 위험 인자 보유 환자에서 추가 위험 가능

#### 시점별 분석
- 예측 최고 약물 농도 시점(Tmax)에서의 최고 효과 평가
- 모든 측정 시점에서 ddQTcF 90% CI 산출 및 보고
- "At any time point" 판정: 어느 시점에서도 90% CI 상한 < 10 ms

---

### 3. 양성 대조약 요건 (Moxifloxacin)

#### 모시플록사신 사용 근거
- hERG 채널 차단 기전으로 QTc 연장 유발 (기대 효과: 약 8~12 ms)
- 광범위하게 연구되어 예측 가능한 QTc 연장 효과 확인
- TQT 시험의 **검정력(assay sensitivity)** 확인에 사용

#### 모시플록사신 양성 대조 기준
- **기대 ddQTcF:** 약 5~15 ms (최소 5 ms 이상 검출되어야 함)
- **허용 기준:** 모시플록사신군의 90% CI 하한 > 5 ms → assay sensitivity 확인
- **맹검 여부:** 2015년 Q&A(R3) 이후 맹검 불필요; 그러나 개방표지(open-label)는 ECG 판독에 편향 최소화 조치 필요

#### 모시플록사신 필요 여부
- E14 Q&A 5.1 접근 방식(C-QTc 분석 대안) 채택 시: 양성 대조 불필요
- E14 Q&A 6.1 접근 방식(통합 비임상 위험 평가): 양성 대조 불필요

---

### 4. Concentration-QTc (C-QTc) 분석 대안

#### 배경
2015년 ICH E14 Q&A(R3)에서 공식 인정된 대안적 접근법.
별도의 전통적 TQT 시험 없이 임상 개발 과정에서 수집된 농도-ECG 데이터를 활용.

#### C-QTc 분석 방법
| 단계 | 내용 |
|------|------|
| 데이터 수집 | Phase 1 또는 Phase 2 시험에서 PK 채혈 및 ECG 동시 기록 |
| 농도 측정 | 각 ECG 시점에서의 혈장 약물 농도 측정 |
| 기저치 보정 | 시간 대응 기저치(time-matched baseline) 또는 투약 전 기저치 사용 |
| 모델 적합 | 선형 혼합효과 모형: ΔΔQTc = β₀ + β₁ × Concentration + (random effects) |
| 예측 | 최고 임상 농도(Cmax)에서의 ΔΔQTcF 추정 및 90% CI 산출 |

#### C-QTc 판정 기준
- **Negative C-QTc:** 최고 임상 농도에서 예측된 ΔΔQTcF의 90% CI 상한 < 10 ms
- **Positive/Inconclusive:** CI 상한 ≥ 10 ms

#### C-QTc 대안의 장점
- 별도 TQT 시험 없이 기존 임상 시험에서 QTc 데이터 수집
- 샘플 크기 대폭 감소:
  - Parallel 설계: 67% 감소
  - Nested crossover: 42% 감소
  - Crossover: 35% 감소
- 환자 집단에서 실제 임상 노출 수준 반영

#### C-QTc 적용 조건 (E14 Q&A 5.1)
1. 충분한 농도 범위 달성: 최고 임상 용량의 ≥ 2배 노출 (또는 독성 한계 내 최고 노출)
2. 고품질 ECG 데이터: 삼중복(triplicate) ECG 또는 동등한 품질
3. PK-ECG 동시 기록: 각 ECG와 농도 측정 시점의 일치
4. 위약 대조: 위약군 포함 (기저치 보정에 사용)
5. 사전 통계 계획: 시험 시작 전 분석 계획 확정

---

### 5. 비임상 QT 평가 (S7B) 연계

#### S7B 요건
- **hERG assay:** 약물의 hERG 채널(IKr) 억제 능력 평가
- **In vivo QT study:** 개(dog) 또는 비인간 영장류에서 QT 간격 측정

#### "Double-negative" 비임상 판단
통합 위험 평가에서 낮은 QT 위험성 판단 기준:
1. **hERG 안전 마진:** 알려진 torsadogenic 약물보다 높은 IC₅₀ (≥ 30배 이상 안전 마진)
2. **In vivo QT:** 임상 최고 노출량에서 QT 연장 없음 (모약 및 주요 인간 대사체 포함)

#### 통합 위험 평가 (E14 Q&A 6.1)
위약 대조, 양성 대조 없이 통합 비임상 근거로 QT 평가 가능한 경우:
- 항암제(oncology) 또는 위약 대조 불가능한 중증 질환 약물
- 안전성/윤리적 이유로 건강인에서의 수퍼치료 용량 투여 불가
- 비임상 "double-negative" 결과 + 임상에서 제한적 농도-QTc 데이터

---

### 6. TQT 시험 면제 조건

#### TQT 시험 면제(waiver) 가능 경우
1. **C-QTc 분석 대안(Q&A 5.1):** Phase 1 임상에서 충분한 노출 범위 달성하여 C-QTc 분석 수행 가능한 경우
2. **비임상 통합 평가(Q&A 6.1):** Double-negative 비임상 결과 + 임상에서의 제한적 QTc 데이터
3. **국소 작용 약물:** 전신 노출이 극히 낮은 국소 적용 약물
4. **방사성 치료약:** 방사선 치료 관련 약물 (매우 짧은 노출 기간)

---

### 7. ECG 측정 및 QTc 보정

#### QTc 보정 방법

| 방법 | 수식 | 특징 |
|------|------|------|
| Fridericia (QTcF) | QTc = QT / RR^(1/3) | FDA 선호; 심박수 보정 우수 |
| Bazett (QTcB) | QTc = QT / √RR | 빈맥/서맥에서 부정확 |
| Individual (QTcI) | 개인별 보정식 | 정확하나 대규모 데이터 필요 |

**FDA 권장:** QTcF (Fridericia)를 1차 보정법으로 사용

#### ECG 기록 프로토콜
- **삼중복(Triplicate) ECG:** 각 시점에서 최소 3개 연속 ECG 기록, 평균 사용
- **중앙 집중 판독:** 맹검 처리된 중앙 실험실(central ECG lab) 판독 권장
- **전자 ECG:** 디지털 ECG 시스템 사용, 수작업 측정 최소화

#### 기저치(Baseline) 정의
- **시간 대응 기저치(Time-matched baseline):** 투약 전 동일 시간대 ECG
- **투약 전 기저치(Pre-dose baseline):** 투약 당일 투약 직전 ECG
- TQT 시험: 일반적으로 투약 전날 또는 투약 당일 여러 시점에서 기저치 측정

---

### 8. FDA 구현 현황 (2016~2024 데이터)

| 연도 | TQT 비율 | C-QTc 비율 |
|------|---------|------------|
| 2016 | 75% | 6% |
| 2019 | ~65% | ~20% |
| 2023 | 41% | 39% |

**전체 변화:** TQT 시험 비율 34% 감소, C-QTc 분석 대폭 증가

FDA 심장 안전성 평가 자료 분석 (424개 QT 시험):
- C-QTc 분석이 QTc 연장 약물의 약 60%에서 primary analysis로 활용
- C-QTc의 높은 예측 정확도 확인

---

## 요약 테이블

| 항목 | 기준/요건 |
|------|-----------|
| 전통 TQT 설계 | 무작위, 위약 대조, 양성 대조(모시플록사신), crossover/parallel |
| 고용량 | 최고 임상 용량의 ≥ 2배 수퍼치료 용량 포함 |
| 양성 대조약 | 모시플록사신 400 mg 단회 경구 (기대 효과: 5~15 ms) |
| 1차 평가변수 | ΔΔQTcF (ddQTcF): 기저치 및 위약 보정 QTcF |
| 음성 판정 기준 | ΔΔQTcF 95% CI 상한 < 10 ms (최고 임상 노출 시점) |
| 양성 대조 assay sensitivity | 모시플록사신 90% CI 하한 > 5 ms |
| C-QTc 대안 (Q&A 5.1) | Phase 1에서 ≥ 2배 임상 노출 달성, 위약 포함, 고품질 ECG |
| 통합 비임상 (Q&A 6.1) | Double-negative (hERG + in vivo QT) + 제한적 임상 데이터 |
| QTc 보정법 (FDA 선호) | QTcF (Fridericia) |
| ECG 기록 | 삼중복, 중앙 집중 판독 |

---

## 주의 사항

1. **E14/S7B 통합 접근:** 최신 2022 Q&A에서는 비임상(S7B)과 임상(E14) 데이터를 통합하여 위험 평가하도록 권고.
2. **특수 집단:** 환자 집단(신장/간 기능 장애, 선천성 long QT 증후군 등)에서 QTc 위험 증가 가능; 라벨에 별도 경고 필요.
3. **TQT 시험 시기:** 대규모 Phase 3 시험 전 수행이 원칙이나, C-QTc 대안으로 개발 초기 임상 시험에서 수집 가능.
4. **라벨 기재:** QTc 연장 가능성이 있는 약물은 "Prolongation of the QT Interval" 관련 라벨 경고 기재 (contraindication, warning, precaution, drug interaction).
5. **IRT-CS:** FDA의 심장 안전성 전문가 팀이 TQT 시험 계획 및 결과 검토에 관여; IND 단계에서 사전 상담(pre-IND meeting) 권장.

---

## 참고 문헌

- ICH. (2022). *E14 and S7B Clinical and Nonclinical Evaluation of QT/QTc Interval Prolongation and Proarrhythmic Potential — Questions and Answers*. FDA CDER. https://www.fda.gov/media/161198/download
- ICH E14. (2005). *Clinical Evaluation of QT/QTc Interval Prolongation and Proarrhythmic Potential for Non-Antiarrhythmic Drugs*.
- FDA. (2024). *FDA's insights: implementing new strategies for evaluating drug-induced QTc prolongation*. PMC12198268.
- FDA IRT-CS: https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/interdisciplinary-review-team-cardiac-safety-studies-formerly-qt-irt
