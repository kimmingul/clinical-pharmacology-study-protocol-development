# Bioanalytical Method Validation Guidance for Industry (2018)

## 메타 정보

| 항목 | 내용 |
|------|------|
| 발행 기관 | FDA CDER |
| 문서명 | Bioanalytical Method Validation Guidance for Industry |
| 발행일 | 2018-05-22 (Final) |
| 원문 URL | https://www.fda.gov/files/drugs/published/Bioanalytical-Method-Validation-Guidance-for-Industry.pdf |
| 연방관보 공지 | https://www.federalregister.gov/documents/2018/05/22/2018-10926 |
| 이전 버전 | 2001년 가이드, 2013년 Draft 개정 |
| 마지막 검증일 | 2026-04-13 |

> **참고:** ICH M10 "Bioanalytical Method Validation and Study Sample Analysis" (2023 Final)이 발행되어 일부 국제 조화 요건이 변경됨. 미국 FDA 규제 제출 시 FDA 2018 가이드 우선 적용하되 ICH M10도 참조.

---

## 적용 범위

이 가이드라인은 다음을 목적으로 하는 생체시료 분석법 밸리데이션에 적용된다:
- **비임상(nonclinical):** GLP 독성 시험의 毒性 동태학(TK) 분석
- **임상(clinical):** 약동학(PK), 생물학적 동등성(BE), 생체이용률(BA) 시험
- **생체시료:** 혈액, 혈청, 혈장, 소변, 조직 등

**분석법 유형:**
1. **크로마토그래피 분석법** (Chromatographic Assays): LC-MS/MS, HPLC, GC 등
2. **리간드 결합 분석법** (Ligand Binding Assays, LBA): ELISA, electrochemiluminescence (ECL), radioimmunoassay (RIA) 등

---

## 핵심 밸리데이션 파라미터

### 1. 선택성 / 특이성 (Selectivity)

#### 크로마토그래피 분석법
- **정의:** 기질(매트릭스) 성분의 방해 없이 목표 분석물 측정 능력
- **요건:**
  - 최소 6개의 개별 공백(blank) 시료 분석
  - 각 공백 시료에서 LLOQ 반응의 < 20% 간섭 허용
  - IS(내부 표준물질) 반응의 < 5% 간섭 허용
- **특수 시료:** 용혈 혈장, 지방혈(lipemic) 혈장에서도 선택성 평가 권장

#### 리간드 결합 분석법
- **요건:**
  - 비특이적 결합(NSB) 및 기질 효과(matrix effect) 평가
  - Hook effect(고농도 역반응) 평가
  - 유사 분석물(관련 단백질, 내인성 분석물)의 교차 반응성 확인

---

### 2. 정밀도 (Precision)

#### 정의
같은 방법으로 반복 분석 시 결과의 일치성 (CV% 형태로 표현)

#### 허용 기준

| 분석법 유형 | QC 농도 수준 | 허용 CV (%) |
|-------------|-------------|------------|
| 크로마토그래피 | LLOQ 제외 모든 QC | ≤ 15% |
| 크로마토그래피 | LLOQ | ≤ 20% |
| 리간드 결합 분석법 | LLOQ 제외 모든 QC | ≤ 20% (또는 ≤ 25%) |
| 리간드 결합 분석법 | LLOQ | ≤ 25% (또는 ≤ 30%) |

**주:** LBA의 경우 크로마토그래피보다 허용 오차 범위 넓음.

#### 분석 내 정밀도 (Intra-run / Within-run)
- 동일 분석 배치 내에서 최소 5회 반복 측정

#### 분석 간 정밀도 (Inter-run / Between-run)
- 최소 3개 배치에서 각각 최소 5개 QC 분석

---

### 3. 정확도 (Accuracy)

#### 정의
측정값이 참값(true value)에 얼마나 가까운가 (% 편차로 표현)

#### 허용 기준

| 분석법 유형 | QC 농도 수준 | 허용 편차 (%) |
|-------------|-------------|--------------|
| 크로마토그래피 | LLOQ 제외 모든 QC | ±15% 이내 |
| 크로마토그래피 | LLOQ | ±20% 이내 |
| 리간드 결합 분석법 | LLOQ 제외 모든 QC | ±20% 이내 |
| 리간드 결합 분석법 | LLOQ | ±25% 이내 |

**계산식:** Accuracy (%) = (Mean measured / Nominal concentration) × 100

---

### 4. 검량 표준물질 및 QC 시료 (Calibration Standards and QC Samples)

#### 검량선 (Calibration Curve)
- **최소 6개** 비영(non-zero) 농도 수준
- **포함 범위:** LLOQ부터 ULOQ까지
- **허용 기준:**
  - 각 검량 표준의 역산 농도가 명목 농도의 ±15% 이내
  - LLOQ에서는 ±20% 이내
  - 전체 표준 중 2/3 이상 허용 기준 충족, LLOQ 및 ULOQ 반드시 포함
- **모형:** 일반적으로 1/x 또는 1/x² 가중 선형 회귀; 또는 이차 방정식 적합

#### QC 시료
| QC 유형 | 권고 농도 범위 |
|---------|--------------|
| LLOQ QC | LLOQ ± 20% |
| Low QC | LLOQ의 3배 이내 |
| Medium QC | 검량선 중앙값 근처 |
| High QC | ULOQ의 75% 이상 |

**QC 수:** 각 배치에서 각 수준별 최소 3개

---

### 5. LLOQ / ULOQ (정량 한계)

#### LLOQ (Lower Limit of Quantification)
- 허용 기준: 정밀도 ≤ 20%, 정확도 ±20% 이내
- 최소 5회 반복 분석으로 검증
- Signal/Noise: 최소 5 이상 권장

#### ULOQ (Upper Limit of Quantification)
- 검량선의 최고 표준 농도
- 이 이상의 시료는 희석 후 재분석

---

### 6. 안정성 (Stability)

#### 평가 조건 및 허용 기준

| 안정성 조건 | 세부 사항 | 허용 기준 |
|-------------|-----------|-----------|
| 동결-해동 안정성 (Freeze-Thaw) | ≥ 3회 동결-해동 사이클 | ±15% |
| 단기 실온 안정성 (Bench-top) | 예상 가공 시간 (≥ 4~24시간) | ±15% |
| 장기 동결 안정성 (Long-term) | 예상 보관 기간 이상 | ±15% |
| 처리 후 안정성 (Processed sample) | 예상 대기 시간 | ±15% |
| 스톡 용액 안정성 | 장기 보관 조건 | ±10% |
| 희석 안정성 (Dilution integrity) | 최고 임상 농도의 희석 검증 | ±15% |

**평가 방법:**
- 신선 조제 QC 시료를 참조로 하여 보관 후 QC 시료 비교
- 저농도(Low QC) 및 고농도(High QC)에서 평가
- % 편차 계산: [(Stored - Fresh) / Fresh] × 100

---

### 7. 기질 효과 / 매트릭스 효과 (Matrix Effect)

#### 크로마토그래피 분석법
- **이온 억제/증폭(Ion Suppression/Enhancement):** 매트릭스 성분이 MS 신호에 미치는 영향
- **평가 방법:** Post-column infusion 또는 post-extraction spike
- **허용 기준:** IS-정규화 매트릭스 인자의 CV ≤ 15%
- **최소 6개** 개별 공여자의 매트릭스에서 평가

#### 리간드 결합 분석법
- 비특이적 결합(NSB) 및 매트릭스 간섭 평가
- 최소 10개 개별 공여자 매트릭스에서 확인 권장

---

### 8. Incurred Sample Reanalysis (ISR)

#### 정의
실제 연구에서 수집된 임상/비임상 시료를 재분석하여 원래 결과의 재현성 확인

#### ISR 수행 요건

| 항목 | 기준 |
|------|------|
| 시험 대상 | 모든 임상 PK 및 BE 시험 (생체시료 분석 포함) |
| 재분석 시료 수 | 전체 시료의 최소 5~10% (또는 최소 20개) |
| 선택 기준 | Cmax 부근 및 소실 상 시료 포함 |
| 허용 기준 | 원래 값과 재분석 값의 차이 ≤ ±20% (at least 2/3 이상) |
| 비교 기준 | [(ISR - Original) / Mean(ISR, Original)] × 100 ≤ ±20% |

#### ISR 수행 시기
- 기법 전이(method transfer) 후 첫 번째 시험
- 새로운 매트릭스 적용 첫 번째 시험
- 장기간 연구 (시료 수 > 1,000개인 경우)

---

### 9. 시험 시료 분석 (Study Sample Analysis)

#### 허용 기준
- 각 배치(analytical run)에서 QC 허용 기준 충족 필요:
  - 최소 4개 QC (LLOQ, Low, Medium, High 각 수준)
  - 각 수준에서 ≥ 2/3가 ±15% 이내
  - 전체 QC에서 ≥ 50%가 ±15% 이내

#### 재분석(Repeat Analysis)
- 예외적 경우만 허용 (기기 고장, 처리 오류 등)
- 사전 정의된 절차 필요
- 재분석 이유 및 결과 모두 문서화

---

### 10. 분석법 전이 (Method Transfer)

- 원래 개발 실험실에서 수행 실험실로 분석법 전이 시 적합성 확인
- **이전 기준:** 정밀도 및 정확도 기준 재확인
- ANDA 시험의 경우 특히 중요 (참조약/시험약 분석의 동일성 보장)

---

## 크로마토그래피 vs 리간드 결합 분석법 비교

| 항목 | 크로마토그래피 (LC-MS/MS 등) | 리간드 결합 분석법 (ELISA 등) |
|------|---------------------------|------------------------------|
| 정밀도 허용 기준 | ≤ 15% (LLOQ: ≤ 20%) | ≤ 20% (LLOQ: ≤ 25%) |
| 정확도 허용 기준 | ±15% (LLOQ: ±20%) | ±20% (LLOQ: ±25%) |
| 검량선 모형 | 선형 또는 이차 회귀 | 4PL, 5PL 로지스틱 등 |
| 내부 표준물질 | 동위원소 표지 또는 구조 유사체 | 참조 표준 (외부 또는 내부) |
| 선택성 평가 | 기질 효과, 이온 억제 | NSB, hook effect, 교차 반응 |
| 검출 한계 | 일반적으로 낮음 (pg/mL) | 분자에 따라 다양 |

---

## 요약 허용 기준 테이블

| 파라미터 | 크로마토그래피 | 리간드 결합 |
|----------|--------------|------------|
| Intra-run 정밀도 (CV%) | ≤ 15% (LLOQ: ≤ 20%) | ≤ 20% (LLOQ: ≤ 25%) |
| Inter-run 정밀도 (CV%) | ≤ 15% (LLOQ: ≤ 20%) | ≤ 20% (LLOQ: ≤ 25%) |
| 정확도 (% 편차) | ±15% (LLOQ: ±20%) | ±20% (LLOQ: ±25%) |
| 안정성 (% 편차) | ±15% | ±15% |
| 스톡 용액 안정성 | ±10% | ±10% |
| 매트릭스 효과 CV% | ≤ 15% | N/A (별도 NSB 평가) |
| ISR 허용 기준 | ≥ 2/3가 ±20% 이내 | ≥ 2/3가 ±20% 이내 |
| 검량선 표준 기준 | ±15% (LLOQ: ±20%) | ±20% (LLOQ: ±25%) |
| 배치 허용 QC 기준 | ≥ 2/3가 ±15% 이내, 각 수준 ≥ 1/2 | 동일 |

---

## 주의 사항

1. **ICH M10과의 관계:** ICH M10 (2023 Final)은 국제 조화 목적으로 발행되었으나, 미국 FDA 제출 시 FDA 2018 가이드가 주요 기준. 둘을 비교하여 더 엄격한 기준 적용 권장.
2. **희귀 매트릭스:** 표준 혈장 대신 DBS(건조 혈반), 조직, 뇌척수액 등 사용 시 추가 밸리데이션 필요.
3. **내인성 분석물:** 체내 존재하는 분석물(호르몬, 바이오마커) 측정 시 대리 매트릭스(surrogate matrix) 또는 표준 추가(standard addition) 방법 사용.
4. **재현성 문제:** ISR 실패 시 시료 불안정성, 기기 편차, 기질 효과 등 원인 조사 및 문서화 필요.
5. **방법 개선:** 기존 방법 개선 또는 변경 시 부분 재밸리데이션(partial re-validation) 수행; 변경 범위에 따라 파라미터 선택.

---

## 참고 문헌

- FDA. (2018). *Bioanalytical Method Validation Guidance for Industry*. CDER. https://www.fda.gov/files/drugs/published/Bioanalytical-Method-Validation-Guidance-for-Industry.pdf
- ICH. (2023). *M10 Bioanalytical Method Validation and Study Sample Analysis*. https://www.fda.gov/media/179296/download
- FDA. (2019). *Regulatory Education for Industry (REdI): How should I measure this? An FDA perspective on the Bioanalytical Method Validation (BMV)*. https://www.fda.gov/drugs/cder-small-business-industry-assistance-sbia/regulatory-education-industry-redi-how-should-i-measure-fda-perspective-bioanalytical-method
