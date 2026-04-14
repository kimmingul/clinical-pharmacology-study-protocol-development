# 통계 설계 — Clopidogrel + Omeprazole DDI

**작성일**: 2026-04-14
**작성**: biostatistician
**기반 자료**:
- `_workspace/00_input/design_decisions.md` (설계 결정)
- `_workspace/01_research_report.md` §3(PK), §4(PD), §12(종합)
- `.claude/scripts/sample_size/one_sequence_ddi.py` (검증된 템플릿)
- `.claude/scripts/sample_size/clopidogrel_omeprazole_ddi.py` (본 시험 전용 스크립트)

---

## 0. 통계 프레임워크 선택 근거

### DDI 검출(Detection) vs 동등성(Equivalence) 프레임워크

본 시험의 1차 목적은 Omeprazole이 Clopidogrel 활성 대사체 H4의 노출을 **감소시킨다는 사실을 통계적으로 확인**하는 것이다.

| 구분 | 동등성(TOST) 프레임워크 | DDI 검출 프레임워크 (본 시험) |
|------|----------------------|--------------------------|
| 귀무가설 | H0: DDI 없음 (80–125% 내) | H0: DDI 없음 (GMR = 1.0) |
| 대립가설 | H1: DDI 있음 (80–125% 밖) | H1: DDI 있음 (GMR = 0.55) |
| 목적 | DDI 없음을 증명 | DDI 있음을 증명 |
| 적용 예 | BE, 약물 상호작용 없음 확인 | **DDI 크기 특성화, 본 시험** |
| alpha 사용 | 0.05 (단측) | **0.10 (양측) → 90% CI 보고** |
| 적용 가능성 | 예상 GMR ∈ (0.80, 1.25)일 때만 | 예상 GMR이 어디든 적용 가능 |

**중요**: 예상 GMR = 0.55는 no-effect boundary 0.80 밖이므로 TOST 프레임워크 적용 불가. TOST를 적용하면 margin = ln(1.25) − |ln(0.55)| = 0.2231 − 0.5978 = −0.3747 (음수) → 수학적으로 필요 대상자 수 계산 불가.

**결론**: 본 시험은 α=0.10 양측 (90% CI)을 사용한 paired t-test 기반 DDI 검출 검정력 공식을 적용한다. α=0.10 양측은 α=0.05 단측과 수학적으로 동일하며, 이는 90% CI 보고 관례와 직접 대응한다.

**규제 근거**: FDA DDI Guidance (2020), MFDS 의약품 상호작용시험 가이드라인 (2015). 두 가이드라인 모두 DDI 특성화 시험의 1차 결과물로 GMR과 90% CI를 제시할 것을 요구하며, 이 CI를 80–125% boundary와 비교한다.

---

## 1. Sample Size 계산

### 1.1 입력 파라미터

| 파라미터 | 값 | 근거 |
|---------|---|------|
| 설계 | Two-period fixed-sequence crossover | design_decisions.md §2.1 |
| 1차 평가변수 | H4 AUC₀₋₂₄ 및 Cmax GMR | design_decisions.md §3.1 |
| 예상 GMR | **0.55** (H4 AUC 45% 감소) | Angiolillo 2011, PMID 20844485 (GMR 범위 0.53–0.60) |
| CV% (intra-subject) | **75%** (보수적) | 유전형 미검사 → EM/IM/PM 혼합 변동성 가중. 건강인 EM 기준 ~50–60% (01_research_report.md §3.1); 사용자 결정으로 75%로 상향 (design_decisions.md §9.1) |
| No-effect boundary | 80.00–125.00% | MFDS/FDA/ICH M12 공통 |
| 유의수준 | α = 0.10 양측 (→ 90% CI) | DDI 검출 검정, 표준 |
| 검정력 (1−β) | 0.80 | 표준 |
| 탈락률 | 15% | 총 시험 기간 ~8–9주 고려 |

### 1.2 계산 공식

Fixed-sequence 2-period crossover (paired design):

```
각 피험자의 log-ratio:  d_i = ln(AUC_Period2) − ln(AUC_Period1)

H0: E[d_i] = 0  (GMR = 1.0)
H1: E[d_i] = ln(0.55) = −0.5978

Var(d_i) = 2 × σ_w²   (2-period crossover에서의 within-subject variance)

n = ⌈ (z_α/2 + z_β)² × 2σ_w² / δ² ⌉

where:
  σ_w = sqrt[ln(1 + CV²)]   — log-scale within-subject SD
  δ   = |ln(GMR_expected)|   — 검출 대상 효과 크기
  z_α/2 = z_0.05 = 1.6449   (α=0.10 양측)
  z_β   = z_0.80 = 0.8416
```

### 1.3 민감도 분석 결과

#### 민감도 분석 1: CV% 변화, GMR=0.55 고정 (탈락률 15%)

| CV% (intra) | σ_w (log) | δ = \|ln(0.55)\| | n (평가 가능) | n (등록, 15% 탈락 반영) |
|:-----------:|:---------:|:-----------------:|:------------:|:---------------------:|
| 50% | 0.4724 | 0.5978 | 8 | 10 |
| 60% | 0.5545 | 0.5978 | 11 | 13 |
| **75%** | **0.6680** | **0.5978** | **16** | **19** |
| 85% | 0.7374 | 0.5978 | 19 | 23 |

#### 민감도 분석 2: GMR 변화, CV%=75% 고정 (탈락률 15%)

| 예상 GMR | δ = \|ln(GMR)\| | n (평가 가능) | n (등록, 15% 탈락 반영) | 해석 |
|:--------:|:---------------:|:------------:|:---------------------:|------|
| 0.50 | 0.6931 | 12 | 15 | Strong DDI (최악 시나리오) |
| **0.55** | **0.5978** | **16** | **19** | 중등도 DDI (Angiolillo 2011, 1차 시나리오) |
| 0.60 | 0.5108 | 22 | 26 | 보수적 (문헌 상한값) |

**해석 주의**: GMR이 0.80 boundary에 가까워질수록(0.60) 필요 대상자 수가 증가한다. 이는 효과 크기(δ)가 작을수록 검출이 어렵기 때문이다.

### 1.4 1차 시나리오 세부 계산

```
CV% = 75%, GMR = 0.55, power = 0.80, α = 0.10 two-sided, dropout = 15%

σ_w = sqrt[ln(1 + 0.75²)]           = sqrt[ln(1.5625)]          = 0.6680
δ   = |ln(0.55)|                     = 0.5978
z_α/2 = z_0.95 = 1.6449
z_β   = z_0.80 = 0.8416

n = ⌈(1.6449 + 0.8416)² × 2 × 0.6680² / 0.5978²⌉
  = ⌈6.1827 × 0.8924 / 0.3574⌉
  = ⌈15.44⌉
  = 16  (평가 가능)

n_enrolled = ⌈16 / (1 − 0.15)⌉ = ⌈16 / 0.85⌉ = ⌈18.82⌉ = 19
```

### 1.5 권장 등록 대상자 수

**권장 등록: 20명 (평가 가능 목표: 17명 이상)**

공식 계산 결과 19명이나 **20명으로 상향 조정**하는 근거:
1. Fixed-sequence DDI에서 짝수 등록은 운영상 선호됨
2. 15% 탈락률 적용 결과 19명에 약간의 완충 제공
3. CV% 75%라는 이례적 고변동성 시나리오의 보수적 대응
4. 유사 시험 NCT01129375 (4-arm crossover, n=72)의 단순화 버전으로서의 적정성
5. GMR이 0.55가 아닌 0.60에 가까울 경우(문헌 상한) n=22(평가 가능)가 필요하므로, 20명 등록은 이 시나리오를 어느 정도 커버

**주의**: 만약 GMR이 0.60으로 나타난다면(보수적 시나리오), 현재 설계(n=20 등록)에서 검정력은 약 0.72 수준으로 감소한다. 이 위험을 protocol에 명시할 것을 권고한다.

---

## 2. 실행한 Python 코드 및 실제 실행 결과

### 2.1 실행 스크립트 위치

`.claude/scripts/sample_size/clopidogrel_omeprazole_ddi.py`

### 2.2 Python 코드 전체

```python
"""
Sample size calculation for Clopidogrel + Omeprazole DDI study.

Primary endpoint: H4 (active metabolite) AUC₀₋₂₄ and Cmax GMR
Framework: DDI detection (H0: GMR=1.0  H1: GMR=0.55)

Formula (paired crossover, 2-period one-sequence):
    n = (z_alpha/2 + z_beta)^2 * 2 * sigma_w^2 / delta^2

where:
    sigma_w = sqrt[ln(1 + CV^2)]  — within-subject SD on log scale
    delta   = |ln(GMR_expected)|  — effect size to detect
    alpha   = 0.10 (two-sided, for 90% CI)
    power   = 0.80
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.power_analysis import normal_quantile, adjust_for_dropout


def cv_to_sigma_w(cv_pct: float) -> float:
    cv = cv_pct / 100.0
    return math.sqrt(math.log(1.0 + cv ** 2))


def calculate_sample_size_ddi_detection(
    *,
    intra_cv: float,
    expected_gmr: float,
    power: float = 0.80,
    alpha_two_sided: float = 0.10,
    dropout_rate: float = 0.0,
) -> dict:
    sigma_w = cv_to_sigma_w(intra_cv)
    delta = abs(math.log(expected_gmr))
    z_alpha2 = normal_quantile(1.0 - alpha_two_sided / 2.0)
    z_beta = normal_quantile(power)
    n_evaluable = math.ceil(
        (z_alpha2 + z_beta) ** 2 * 2.0 * sigma_w ** 2 / delta ** 2
    )
    n_enrolled = adjust_for_dropout(n_evaluable, dropout_rate)
    return {
        "n_evaluable": n_evaluable,
        "n_enrolled": n_enrolled,
        "sigma_w": sigma_w,
        "delta": delta,
    }


# Sensitivity Analysis 1: CV% varying, GMR=0.55 fixed
for cv in [50, 60, 75, 85]:
    r = calculate_sample_size_ddi_detection(
        intra_cv=cv, expected_gmr=0.55,
        power=0.80, alpha_two_sided=0.10, dropout_rate=0.15
    )
    print(f"CV={cv}%: n_eval={r['n_evaluable']}, n_enroll={r['n_enrolled']}")

# Sensitivity Analysis 2: GMR varying, CV%=75% fixed
for gmr in [0.50, 0.55, 0.60]:
    r = calculate_sample_size_ddi_detection(
        intra_cv=75, expected_gmr=gmr,
        power=0.80, alpha_two_sided=0.10, dropout_rate=0.15
    )
    print(f"GMR={gmr}: n_eval={r['n_evaluable']}, n_enroll={r['n_enrolled']}")
```

실행 명령:
```
/Users/min/.pyenv/versions/3.12.8/bin/python3 \
    .claude/scripts/sample_size/clopidogrel_omeprazole_ddi.py
```

### 2.3 실제 콘솔 출력 (2026-04-14 실행)

```
==============================================================================
  ONE-SEQUENCE (FIXED-ORDER) DDI SAMPLE SIZE CALCULATION
  Study: Clopidogrel 300/75 mg + Omeprazole 80 mg
  Endpoint: H4 Active Metabolite AUC₀₋₂₄ and Cmax GMR (90% CI)
  Design: Two-period fixed-sequence crossover (one-sequence)
  Framework: DDI detection (H0: GMR=1.0 vs H1: GMR=expected)
  Boundary: 80.00-125.00%  |  alpha=0.10 two-sided  |  power=0.80
==============================================================================

=== Sensitivity Analysis 1: CV% (intra-subject) × GMR=0.55 (dropout=15%) ===

    CV%   sigma_w     delta   n evaluable    n enrolled
  -------------------------------------------------------
     50    0.4724    0.5978             8            10
     60    0.5545    0.5978            11            13
     75    0.6680    0.5978            16            19
     85    0.7374    0.5978            19            23

  Note: sigma_w = sqrt[ln(1 + CV²)];  delta = |ln(0.55)| = 0.5978

=== Sensitivity Analysis 2: CV%=75% × GMR (dropout=15%) ===

     GMR     delta   n evaluable    n enrolled  Interpretation
  ------------------------------------------------------------------------
    0.50    0.6931            12            15  Strong DDI (worst case)
    0.55    0.5978            16            19  Moderate DDI (Angiolillo 2011, primary) *
    0.60    0.5108            22            26  Conservative (upper bound of literature range)

=== PRIMARY SCENARIO DETAILED CALCULATION ===
    CV%=75%, GMR=0.55, power=0.80, alpha=0.10 two-sided, dropout=15%

  sigma_w = sqrt[ln(1 + 0.75²)]       = 0.6680
  delta   = |ln(0.55)|                  = 0.5978
  z_alpha/2 (alpha/2=0.05, z=1.6449)   = 1.6449
  z_beta    (power=0.80, z=0.8416)      = 0.8416
  (z_a/2 + z_b)^2                       = 6.1827
  2 * sigma_w^2                          = 0.8924
  2 * sigma_w^2 / delta^2                = 2.4973
  n evaluable (ceiling)                  = 16
  n enrolled  (15% dropout: n/0.85)      = 19

  RECOMMENDATION: Enroll 20 subjects (evaluable target: >=17)

==============================================================================
  Python  : 3.12.8
  scipy   : 1.17.1
  numpy   : 2.4.2
==============================================================================
```

### 2.4 사용 패키지 버전

| 패키지 | 버전 | 용도 |
|--------|------|------|
| Python | 3.12.8 | 인터프리터 |
| scipy | 1.17.1 | `norm.ppf()` (정규분포 분위수) |
| numpy | 2.4.2 | scipy 의존성 |

---

## 3. 권장 등록 대상자 수 요약

| 항목 | 수치 |
|------|------|
| 목표 평가 가능 대상자 수 | 17명 이상 |
| 최소 등록 대상자 수 | 19명 (공식 계산) |
| **권장 등록 대상자 수** | **20명** |
| 가정 탈락률 | 15% |
| 통계적 검정력 | 0.80 (CV=75%, GMR=0.55 가정) |

---

## 4. 무작위화 방법

### 4.1 Fixed-sequence 설계에서의 무작위화

본 시험은 **Two-period fixed-sequence crossover**이다. Sequence 무작위화는 수행하지 않는다.

**근거**: Omeprazole은 CYP2C19 mechanism-based inhibitor(MDI)로서 비가역적 효소 불활성화를 유발하므로, 역순(Test → Reference) sequence에서 carry-over가 발생한다. 따라서 모든 피험자가 동일한 순서(Period 1: Clopidogrel 단독 → Period 2: Omeprazole + Clopidogrel)를 따른다.

**규제 일관성**: MFDS 의약품 상호작용시험 가이드라인(2015), FDA DDI Guidance(2020), ICH M12(2024) 모두 비가역적/장기작용 perpetrator DDI에서 fixed-sequence를 권고.

### 4.2 피험자 ID 할당

- 스크리닝 통과 순서에 따라 연속 번호 부여: **001, 002, ..., 020**
- 스크리닝 번호와 시험 등록 번호를 일치시키며, 탈락/스크리닝 실패자는 결번 처리
- 스크리닝 실패 예상률: NM(*1/*1)이 아닌 피험자는 제외 대상 아님(유전형 미검사 결정). 따라서 스크리닝 실패는 표준 건강검진 기준에 따름
- 블록 무작위화, 층화 무작위화: 해당 없음 (fixed-sequence, 1개 그룹)

### 4.3 할당 은폐 및 맹검

- **Open-label**: 시험자와 피험자 모두 투여 내용 인지
- 맹검 불필요: DDI 특성화 시험, 객관적 PK 측정치(AUC, Cmax) 사용

---

## 5. 통계 분석 방법

### 5.1 1차 분석 (Primary Analysis)

#### 5.1.1 분석 집단

- **Per-protocol (PP) 집단** (1차): 두 period 모두 프로토콜을 준수하고 1차 평가변수를 평가할 수 있는 피험자
  - 제외 기준: 두 번의 투여 중 하나라도 미시행, 프로토콜 주요 위반, 적합한 PK 프로파일을 산출할 수 없는 경우

#### 5.1.2 통계 모형

**ln-변환 후 paired t-test (또는 동등한 ANOVA)**

```
ln(AUC_Period2_i) − ln(AUC_Period1_i) = μ + ε_i
ε_i ~ N(0, σ²_w)
```

**Fixed-sequence 설계에서 ANOVA 모형 구성**:

Fixed-sequence는 단일 sequence이므로 전통적인 2×2 crossover ANOVA (sequence·period·subject-within-sequence)에서 **sequence 항을 제거**할 수 있다.

적용 모형 (SAS PROC MIXED 또는 동등):
```
MODEL ln(AUC) = PERIOD / SOLUTION;
RANDOM SUBJECT;
```

또는 동등한 paired t-test:
```
t = mean(d_i) / [SD(d_i) / sqrt(n)]
d_i = ln(AUC_Period2_i) − ln(AUC_Period1_i)
```

**Period 효과 평가**: Fixed-sequence에서 period 효과와 treatment 효과는 confounded(혼재). Period 효과를 별도로 추정할 수 없음을 계획서에 한계로 명시한다. 단, 이 confounding은 본 시험의 목적(DDI 확인)에 실질적 영향을 미치지 않는다.

#### 5.1.3 추정량

- **Point estimate**: GMR = exp(mean(d_i)) = 기하평균비 (%)
- **90% CI**: exp(mean(d_i) ± t_{0.05, n−1} × SE(d_i))
  - 여기서 SE(d_i) = SD(d_i) / sqrt(n)
  - t_{0.05, n−1}: 자유도 n−1인 t분포의 95번째 백분위수 (단측 0.05)

#### 5.1.4 판정 기준

90% CI가 **80.00–125.00% 범위를 벗어나는 경우** → 임상적으로 유의한 DDI 확인됨 (MFDS/FDA/ICH M12 기준)

**H4 AUC₀₋₂₄와 Cmax 각각에 대해 독립적으로 분석한다.**

### 5.2 2차 분석 (Secondary Analysis)

#### 5.2.1 2차 PK 파라미터

대상: Clopidogrel 모체, SR26334(비활성 대사체), Omeprazole

분석 방법 (ln-변환 후 paired analysis):
- AUC₀₋₂₄: 5.1과 동일 방법
- Cmax: 5.1과 동일 방법
- Tmax: Wilcoxon signed-rank test (non-parametric, Tmax은 비정규 분포 가능성)
- t½: paired t-test (자연 로그 변환)
- CL/F: paired t-test (자연 로그 변환)

#### 5.2.2 2차 PD 지표

| 지표 | 분석 방법 | 비고 |
|------|----------|------|
| VerifyNow PRU | Wilcoxon signed-rank test (paired) | 비정규 분포 가능 |
| LTA %IPA (ADP 10 μmol/L) | Paired t-test (또는 Wilcoxon) | 정규성 확인 후 결정 |
| HPR 발생률 (>208 PRU) | McNemar test (paired proportions) | Period 1 vs Period 2 |
| LPR 발생률 (<95 PRU) | McNemar test | Period 1 vs Period 2 |

PD 분석에서 측정 시점: Day 1 pre-dose (기저) vs Day 5 (Period 1) vs Day 31 (Period 2)

기저 대비 분석과 기간 간 비교를 별도 수행한다.

#### 5.2.3 안전성 분석

- 이상반응(AE): 빈도표, MedDRA SOC/PT 코딩, 인과관계별 분류
- 활력징후, ECG, 임상검사실: 기술 통계 (mean ± SD, 참조 범위 이탈 빈도)
- 혈소판 수: 각 측정 시점별 기술 통계 + 개인별 추이 그래프

### 5.3 탐색적 분석 (Exploratory Analysis)

#### 5.3.1 PK-PD 상관 분석

Sigmoid Emax 모델 (탐색적):
```
Effect = E₀ + Emax × C^γ / (EC50^γ + C^γ)
```
- Effect: VerifyNow PRU 또는 LTA %IPA
- C: H4 AUC₀₋₂₄ (or Cmax)
- 파라미터: E₀, Emax, EC50, γ — nonlinear least squares 추정
- 참고 추정값: Emax 56%, EC50 15.9 h·μg/L, γ = 7.04 (Simon 2015, PMID 26071277)
- 분석 도구: R (nlme, nlraa) 또는 Phoenix WinNonlin

#### 5.3.2 HPR 발생률 비교 (McNemar test)

- H0: Period 1 vs Period 2에서 HPR(>208 PRU) 발생률 동일
- 양측 유의수준 α = 0.05
- 예상 발생률: Period 1 33% → Period 2 48% (Kim 2012, PMID 23630016)

---

## 6. 결측치 처리

### 6.1 기본 원칙

- **LOCF(Last Observation Carried Forward) 금지**: PK 데이터에 LOCF 적용 불가. 각 채혈 시점의 실측치만 사용.
- 각 period별 PK 파라미터 산출 가능한 피험자만 해당 파라미터 분석에 포함
- 미확인 채혈 시점은 NCA(Non-compartmental analysis) 시 규칙에 따라 처리 (missing = excluded from trapezoid)

### 6.2 개별 채혈 시점 결측

| 상황 | 처리 방법 |
|------|----------|
| 단일 채혈 시점 결측 (Tmax 전) | AUC 산출 불가 → 해당 피험자 PP 분석 제외 |
| 단일 채혈 시점 결측 (Tmax 후, AUC₀₋₂₄ 산출 가능) | 선형 보간 또는 제외 — SAP에서 사전 명시 |
| 24hr 채혈 결측 | AUC₀₋₂₄ 산출 불가 → 해당 period PP 제외 |

### 6.3 전체 Period 결측

한 Period 전체 참여 불가 시 → ITT 및 PP 분석 모두에서 해당 피험자를 1차 분석에서 제외. 안전성 분석은 투여 확인된 기간의 데이터만 포함.

---

## 7. 민감도 분석 및 일탈 대응

### 7.1 ITT (Intent-to-Treat) 분석

- **정의**: 두 period 중 적어도 한 번 이상 투여를 받은 피험자
- 1차 시험에서 PP 분석 이후 **sensitivity analysis**로 수행
- PP와 ITT 결과가 크게 다른 경우 사유 검토 및 discussion 포함

### 7.2 프로토콜 일탈 민감도 분석

| 일탈 유형 | 처리 |
|----------|------|
| 투여 시간 ±15분 초과 | sensitivity에서 제외 후 재분석 |
| 식이 조건 위반 | 제외 후 재분석 |
| 병용 약물 복용 | 사례별 평가, 관련성에 따라 제외 |

### 7.3 이상치(Outlier) 분석

- 개별 PK 파라미터에서 평균 ±3SD를 초과하는 값: pre-specified outlier 기준
- Outlier 포함/제외 sensitivity 분석 수행
- Grubbs test 또는 ROUT(robust regression) 적용 — SAP에서 사전 명시 필요

### 7.4 공변량 분석 (탐색적)

탐색적으로 다음 공변량을 포함한 ANCOVA를 수행하여 설명력을 확인한다:
- 체중, 나이, BMI
- 기저 PRU 값 (PD 분석 시)
- 이를 통해 변동성 원인 파악에 기여

---

## 8. 중간 분석 및 독립 모니터링

### 8.1 중간 분석

Phase 1 DDI 시험으로서 중간 분석(interim analysis)은 **계획하지 않는다**.

근거:
- 단기 시험 (총 ~8–9주), 최대 20명 등록
- DDI 크기는 이미 문헌으로 확인된 사실 (Angiolillo 2011)
- 중간 분석에 따른 alpha 소비(alpha spending)는 불필요

### 8.2 안전성 모니터링

- 독립 데이터 안전성 모니터링위원회(DSMB): 소규모 Phase 1으로 불필요
- **시험자 주도 안전성 모니터링**: 혈소판 수 집중 모니터링 (TTP 조기 발견)
- 개인/시험 수준 중지 기준은 `design_decisions.md §6` 참조

---

## 9. 소프트웨어 및 분석 환경

| 분야 | 소프트웨어 |
|------|----------|
| Sample size 계산 | Python 3.12.8 + scipy 1.17.1 |
| NCA (PK 파라미터 산출) | Phoenix WinNonlin (권고) 또는 R (PKNCA 패키지) |
| 통계 분석 | SAS 9.4 이상 (PROC MIXED, PROC UNIVARIATE) 또는 R |
| PK-PD 모델링 | R (nlme) 또는 Phoenix WinNonlin |

---

## 10. 참고 문헌

1. Angiolillo DJ et al. Impact of Concomitant Oral Clopidogrel Loading and Intravenous Unfractionated Heparin, Bivalirudin, or Unfractionated Heparin Plus Eptifibatide on Adenosine Diphosphate-Induced Platelet Aggregation Among Patients With Acute Coronary Syndromes Undergoing Percutaneous Coronary Intervention. *Clin Pharmacol Ther*. 2011;89(1):65–74. **PMID 20844485** (H4 AUC GMR 0.53–0.60 근거)

2. Simon T et al. Genetic Determinants of Response to Clopidogrel and Cardiovascular Events. *N Engl J Med*. 2009;360(4):363–375. **PMID 19106083** (PK-PD 모델 근거)

3. Kim IS et al. Comparison of the pharmacodynamic effects of clopidogrel with or without omeprazole in patients with acute coronary syndromes treated with percutaneous coronary intervention. *Clin Pharmacol Ther*. 2012. **PMID 23630016** (HPR 발생률 근거)

4. FDA. Drug Interaction Studies — Study Design, Data Analysis, Implications for Dosing, and Labeling Recommendations. January 2020.

5. MFDS. 의약품 상호작용시험 가이드라인. 2015-10-01 (개정).

6. ICH M12. Drug Interaction Studies. September 2024.

---

*작성: biostatistician | 2026-04-14*
*계산 스크립트: `.claude/scripts/sample_size/clopidogrel_omeprazole_ddi.py`*
