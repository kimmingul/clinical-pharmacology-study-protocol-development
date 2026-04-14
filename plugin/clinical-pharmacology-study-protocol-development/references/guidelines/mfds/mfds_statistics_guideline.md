# MFDS 임상약리시험 통계 가이드라인

## 메타 정보

| 항목 | 내용 |
|------|------|
| 발행 기관 | 식품의약품안전처 (MFDS) |
| 문서명 | 생물학적동등성시험 통계분석 가이드라인; 임상시험 통계 관련 가이드라인 (식약처) |
| 관련 ICH 가이드라인 | ICH E9(R1): Statistical Principles for Clinical Trials; ICH E9 Addendum (Estimands) |
| 발행일 / 최신 개정 | [전문 미수집 — 사용자 PDF 제공 필요] |
| 원문 URL | https://www.mfds.go.kr/brd/m_218/list.do |
| 마지막 검증일 | 2026-04-14 |

---

## 1. 표본크기 계산 원칙 (Sample Size Determination)

### 1.1 일반 원칙

| 항목 | 요건 |
|------|------|
| **근거 의무** | 모든 임상시험은 통계적 근거에 기반한 대상자 수 산출 필수 |
| **명시 사항** | 가정(assumptions), 검정력(power), 유의수준(α), 효과 크기(effect size), 변동성(variability), 예상 탈락률 |
| **탈락률 보정** | 예상 탈락률을 반영한 보정 대상자 수 산출 필수 |
| **참고 문헌** | 변동성 추정의 근거 (문헌, 예비 시험 결과, 공개된 데이터베이스) 명시 |
| **단측/양측 검정** | 원칙적으로 양측 검정; 단측 사용 시 과학적 정당성 제시 |

### 1.2 시험 유형별 표본크기 요건

| 시험 유형 | 핵심 파라미터 | 최소 요건 |
|----------|-------------|----------|
| **BE (2×2 교차)** | Intra-subject CV, 예상 GMR, 동등성 한계, 검정력(1-β) | 평가 가능 최소 **12명** |
| **BE (replicate 교차)** | Intra-subject CV (>30%), 설계 유형 | 설계별 산출 |
| **DDI (교차)** | Intra-subject CV, 예상 GMR, no-effect boundary | 통계적 산출 |
| **DDI (고정순서)** | Intra-subject CV, 예상 fold change | 통계적 산출 |
| **병렬 (연속형)** | 표준편차(SD), 평균 차이, 효과크기(Cohen's d) | 통계적 산출 |
| **FIH (SAD/MAD)** | 코호트당 관행: 활성약 **6~8명** + 위약 **1~2명** | 관행 기반 (검정력 산출 필수 아님) |

### 1.3 BE 시험 표본크기 공식

```
일반 교차설계 BE:
n = 2 × σ²_intra × (z_{α/2} + z_β)² / (ln(θ_U) - |ln(GMR)|)²

여기서:
  σ²_intra = 개체 내 분산 (= (ln(1 + CV²_intra)))
  θ_U = 상단 동등성 한계 (= ln(1.25))
  GMR = 예상 기하평균비 (통상 1.00 또는 0.95 가정)
  z_{0.05} = 1.6449 (단측 α=0.05)
  z_{0.20} = 0.8416 (β=0.20 → 검정력 80%)
  z_{0.10} = 1.2816 (β=0.10 → 검정력 90%)
```

### 1.4 BE 표본크기 참고 테이블 (80% 검정력, α=0.05, GMR=1.00)

| Intra-subject CV (%) | 필요 대상자 수 (양측 80-125%) |
|---------------------|---------------------------|
| 10 | 12 (최소) |
| 15 | 12 (최소) |
| 20 | 16 |
| 25 | 24 |
| 30 | 34 |
| 35 | 46 |
| 40 | 60 |
| 45 | 76 |
| 50 | 94 |

> 탈락률 10~20% 보정 필요 → 실제 등록 대상자 수 = 위 수치 ÷ (1 - 탈락률)

### 1.5 표본크기 산출 소프트웨어

| 도구 | 특징 |
|------|------|
| **PASS (NCSS)** | 상용; BE·DDI·병렬 등 다양한 설계 지원 |
| **nQuery** | 상용; adaptive design 지원 |
| **SAS (PROC POWER)** | 상용; 대부분의 설계 유형 지원 |
| **R (pwr, PowerTOST)** | 오픈소스; BE 표본크기 전문 패키지 |
| **Python (scipy.stats, pingouin)** | 오픈소스 |

---

## 2. BE 시험 통계 분석 (BE Statistical Analysis)

### 2.1 분산분석 모형 (ANOVA Model)

#### 2×2 교차설계

| 요인 | 유형 | 수준 |
|------|------|------|
| 순서 (Sequence) | 고정 효과 | RT, TR (2수준) |
| 대상자 (Subject within Sequence) | 변량 효과 | 개체간 변동 반영 |
| 기간 (Period) | 고정 효과 | 1기, 2기 (2수준) |
| 제형 (Formulation/Treatment) | 고정 효과 | T(시험약), R(대조약) |

**SAS 코드 예시:**
```sas
PROC MIXED DATA=bedata;
  CLASS seq subj period trt;
  MODEL lnAUC = seq period trt / DDFM=SATTERTH;
  RANDOM subj(seq);
  LSMEANS trt / DIFF CL ALPHA=0.10;
  ODS OUTPUT DIFFS=estimates;
RUN;
```

#### Replicate 교차설계 (2×3 또는 2×4)

| 요인 | 유형 | 비고 |
|------|------|------|
| 순서 (Sequence) | 고정 효과 | 2수준 이상 |
| 대상자 (Subject within Sequence) | 변량 효과 | |
| 기간 (Period) | 고정 효과 | |
| 제형 (Formulation) | 고정 효과 | |
| 개체×제형 (Subject×Formulation) | 변량 효과 | 개체 내 분산 추정용 |

### 2.2 분석 절차 (Step-by-Step)

1. AUC₀₋ₜ 및 Cmax를 자연로그(ln) 변환
2. 혼합효과 ANOVA 실행 (SAS PROC MIXED 또는 R lme4/nlme)
3. 제형(T vs R) 효과의 최소제곱평균(LSM) 차이 및 90% 신뢰구간 산출
4. 역변환(exp): GMR 및 90% CI(%) 계산
5. 90% CI가 **80.00%~125.00%** 이내이면 동등 판정

### 2.3 분석 보고 양식

| 보고 항목 | 내용 |
|---------|------|
| **기하평균 (GM)** | 시험약(T) 및 대조약(R) 각각의 GM (AUC, Cmax) |
| **기하평균비 (GMR)** | T/R GMR (%) |
| **90% 신뢰구간 (90% CI)** | 하한 ~ 상한 (%) |
| **판정** | BE 충족 여부 |
| **ANOVA 테이블** | 순서, 기간, 제형 효과의 F값, p값 |
| **분산 성분** | 개체간 분산, 개체 내 분산, 잔차 분산 |
| **개별 대상자 데이터** | 각 대상자의 AUC, Cmax, T/R 비율 |

---

## 3. DDI 시험 통계 분석 (DDI Statistical Analysis)

### 3.1 교차설계 DDI

| 항목 | 방법 |
|------|------|
| **주 분석** | BE 분석과 동일한 ANOVA 모형 |
| **1차 평가변수** | AUC₀₋∞ (또는 AUC₀₋ₜ) |
| **2차 평가변수** | Cmax |
| **보고** | GMR 및 90% CI |
| **판정 기준** | 90% CI 80~125% 이내 = 임상적으로 유의한 DDI 없음 |

### 3.2 고정순서(One-Sequence) DDI

| 항목 | 방법 |
|------|------|
| **주 분석** | Paired t-test (ln-변환) 또는 ANOVA (기간 효과) |
| **보고** | GMR 및 90% CI |
| **추가 분석** | 개별 대상자 fold-change scatter plot |
| **캐리오버 평가** | 고정순서 설계에서는 캐리오버 평가 불가; 설계로 최소화 |

### 3.3 DDI 결과 시각화

| 그래프 | 내용 |
|--------|------|
| **농도-시간 곡선** | 병용 전(기질 단독) vs 병용 후 평균 곡선 중첩 (linear + semi-log) |
| **개별 fold-change** | 각 대상자의 AUC 비율(병용/단독) 점도표 |
| **GMR + 90% CI 플롯** | Forest plot 형식의 GMR 요약 |

---

## 4. FIH 시험 통계 (FIH Statistical Analysis)

| 항목 | 방법 |
|------|------|
| **PK 기술통계** | 코호트별: 기하평균(GM), CV%, 중앙값, 범위 (n이 적으므로 비모수 요약 병행) |
| **용량 비례성** | Power model: ln(AUC) = ln(a) + b × ln(Dose); b의 90% CI |
| **비례성 판단 기준** | b의 90% CI가 [0.70, 1.43] 이내이면 비례성 있다고 판단 |
| **안전성** | 이상반응 빈도표 (CTCAE 등급별); 활력징후·검사치 기술통계 |
| **PD 분석** | PK-PD 관계 산점도 및 상관분석 |
| **표본크기 근거** | 관행 기반 (코호트당 6+2); 통계적 검정력 산출은 일반적으로 요구하지 않음 |

---

## 5. 결측치 처리 (Missing Data Handling)

| 상황 | 처리 방법 |
|------|----------|
| **PK 채혈 누락 (시점 결측)** | 해당 시점 결측 처리; NCA에서 일반적으로 보간하지 않음; 경우에 따라 제외 |
| **교차설계 기간 전체 결측** | 해당 대상자 평가 불가 → 탈락으로 처리; 평가 가능 집단에서 제외 |
| **이상치 (outlier)** | 사전 정의 기준(예: Cook's distance, Grubbs test) 적용; 포함/제외 모두 분석 (sensitivity analysis) |
| **BE 시험 탈락** | 탈락 대상자 제외 후 evaluable population 분석 (PP 분석 중심) |
| **사전 정의 필수** | 모든 결측치·이상치 처리 규칙은 프로토콜 또는 SAP에 사전 정의 |

---

## 6. 분석 소프트웨어 및 코드 검증

| 항목 | 요건 |
|------|------|
| **승인 소프트웨어** | SAS, R, Phoenix WinNonlin, NONMEM 등 |
| **소프트웨어 검증** | 소프트웨어 검증(validation) 기록 유지; 버전 관리 |
| **코드 제출** | 식약처 제출 시 SAS/R 코드 및 출력물 포함 |
| **재현성** | 동일 코드로 동일 결과 재현 가능성 확보; 코드 주석 포함 |
| **QC 절차** | 이중 프로그래밍(dual programming) 권장; 상호 검증 |

---

## 7. 보고 양식 (Reporting Format)

### 7.1 필수 포함 표

| 표 번호 | 내용 |
|--------|------|
| 인구통계학적 특성 | 연령(평균±SD), 성별(n, %), 체중, BMI; 군별 균형 확인 |
| PK 파라미터 요약 | 기하평균, CV%(기하), 중앙값, Min~Max; 시험별 각 코호트 |
| ANOVA 결과 | 각 효과(순서, 기간, 제형)의 F값, p값; Mean Square; 분산 성분 |
| GMR 및 90% CI | 제형 비교 결과; 동등성 판정 |
| 개별 대상자 PK | 각 대상자의 AUC₀₋ₜ, Cmax, Tmax 등 및 T/R 비율 |
| 이상반응 요약 | 계통기관분류(SOC)/선호 용어(PT)별 빈도; 중증도별 |
| 임상검사 변화 | 투여 전 대비 투여 후 변화량; 정상범위 이탈 사례 |

### 7.2 필수 포함 그래프

| 그래프 | 내용 |
|--------|------|
| 평균 농도-시간 곡선 | Linear scale + semi-log scale; 오차막대(±SD 또는 95% CI) |
| 개별 농도-시간 곡선 | 대상자별 중첩 (spaghetti plot) |
| 개별 T/R 비율 산점도 | BE: 각 대상자의 AUC₀₋ₜ 및 Cmax 비율; 기준선(80-125%) 표시 |
| GMR Forest plot | DDI 또는 BE 여러 파라미터의 GMR + 90% CI 한눈에 비교 |
| 용량 비례성 그래프 | FIH: Dose vs AUC/Cmax (power model 적합 곡선 포함) |
| QTc 플롯 | QTc 연장 시험: 농도 vs ΔQTcF scatter plot + 회귀선 |

---

## 8. Estimand Framework (ICH E9(R1) 적용)

MFDS는 ICH E9(R1) estimand framework를 참조하며, 임상약리시험에서의 적용:

| Estimand 구성 요소 | 임상약리시험에서의 적용 예 |
|------------------|----------------------|
| **Population** | 건강한 성인 자원자 (BE); 안정적 CYP3A4 대사 환자 (DDI) |
| **Variable (Endpoint)** | AUC₀₋ₜ, Cmax |
| **Intercurrent events** | 조기 탈락, 구토, 음식 섭취 위반 |
| **Population-level summary** | GMR 및 90% CI |
| **Sensitivity analysis** | 이상치 포함/제외; 다른 결측치 처리 방법 |

---

## 9. 통계적 가설 검정 (Statistical Hypothesis Testing)

### 9.1 동등성 검정 (Equivalence Test)

```
귀무가설 (H₀): θ ≤ θ_L 또는 θ ≥ θ_U (동등하지 않음)
대립가설 (H₁): θ_L < θ < θ_U (동등함)

여기서:
  θ = T/R GMR (로그 척도)
  θ_L = ln(0.80) = -0.2231
  θ_U = ln(1.25) = +0.2231
  α = 0.05 (단측); 양측 합산 신뢰구간 = 90% CI
```

### 9.2 Non-inferiority 검정 (해당 시)

일부 DDI 시험에서 상호작용 없음(non-inferiority to 병용 없음 상황)을 입증하기 위해:
- 단측 90% CI 하한이 no-effect 하한(예: 80%) 이상이어야 함

---

## 10. 주요 참조 규정 및 가이드라인

| 규정/가이드라인 | 내용 | 적용 시험 |
|---------------|------|---------|
| MFDS 의약품동등성시험기준 | BE 특화 통계 요건 | BE 시험 |
| ICH E9(R1) | 통계적 원칙, estimand framework | 모든 임상시험 |
| ICH E6(R3) | GCP, 통계 섹션 요건 (SAP 사전 정의 등) | 모든 임상시험 |
| FDA BE Guidance (2021) | RSABE 포함 통계 방법; 비교 참고 | BE 시험 (비교용) |
| EMA BE Guideline (2010, 개정판) | EU 기준 비교 | BE 시험 (비교용) |
| MFDS 다중 평가변수 가이드라인 | 다중 평가변수 사용 임상시험 | 다중 endpoint 시험 |

---

## 참고 문헌 및 원문 URL

- MFDS 가이드라인 목록: https://www.mfds.go.kr/brd/m_218/list.do
- 의약품동등성시험기준 (법령): https://www.law.go.kr/행정규칙/의약품동등성시험기준
- 다중 평가변수 가이드라인 (민원인 안내서): https://www.mfds.go.kr/brd/m_1060/
- ICH E9(R1) 통계 원칙: https://www.ich.org/page/efficacy-guidelines
- R PowerTOST 패키지: https://cran.r-project.org/package=PowerTOST
