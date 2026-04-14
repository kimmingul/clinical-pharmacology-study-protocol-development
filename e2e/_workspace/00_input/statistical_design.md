# 통계 설계 보고서
## Amlodipine Besylate 5mg 정제 생물학적동등성(BE) 시험

**작성일**: 2026-04-13
**작성자**: Biostatistician (자동 생성)
**기반 문서**: `design_decisions.md`, `01_research_report.md`
**계산 스크립트**: `.claude/scripts/sample_size/crossover_2x2_be.py`

---

## 1. 시험 설계 개요

| 항목 | 내용 |
|------|------|
| 설계 유형 | 무작위배정, 공개, 단회 투여, 2-sequence, 2-period crossover |
| 시험약(T) | Amlodipine besylate 5mg 정제 (제네릭) |
| 대조약(R) | Norvasc® 5mg 정제 (Pfizer) |
| Sequence | TR (시험약 → 대조약), RT (대조약 → 시험약) |
| Washout | 21일 (t½ ~40시간 × 5 = ~200시간 기반) |
| 1차 평가변수 | AUC₀₋ₜ, Cmax (ln 변환 후 TOST) |
| 동등성 한계 | 90% CI: 80.00–125.00% |

---

## 2. Sample Size 계산

### 2.1 계산 방법론

**설계**: 2-sequence, 2-period crossover 생물학적동등성 시험  
**검정 방법**: Two One-Sided Tests (TOST)  
**변환**: 자연로그(ln) 변환 후 분석

**핵심 공식** (Chow & Liu, 2009; MFDS 생동성 가이드라인):

```
sigma_w² = ln(1 + CV_w²)           ← 로그 척도 개체내 분산
delta     = |ln(GMR)|              ← 예상 편차
theta     = ln(1.25)               ← 상한 동등성 한계 (로그 척도)

n_per_seq = ⌈(z_α + z_β)² × 2 × sigma_w² / (theta − delta)²⌉
n_total   = 2 × n_per_seq
n_total_adjusted = ⌈n_total / (1 − dropout_rate)⌉
```

**참조 문헌**:
- Chow S-C, Liu J-P. *Design and Analysis of Bioavailability and Bioequivalence Studies*, 3rd ed. CRC Press, 2009, Chapter 5.
- 식품의약품안전처. 생물학적동등성시험 기준 (고시).

### 2.2 공통 파라미터

| 파라미터 | 값 | 근거 |
|----------|-----|------|
| Intra-subject CV (Cmax) | 18% | Wang et al., 2020 (PMID: 32034814); 복수 문헌 보수적 상한 |
| Intra-subject CV (AUC) | 7.5–11.6% → 12% 사용 | Wang et al., 2020 (PMID: 32034814) |
| 동등성 한계 | 80.00–125.00% | MFDS/FDA/EMA 표준 |
| Alpha (one-sided) | 0.05 (90% CI 기준) | TOST 표준 |
| 탈락률 (dropout) | 20% | 2×2 crossover 보수적 적용 |

> **주의**: Intra-subject CV (개체내 CV, within-subject CV)를 사용한다. Crossover 설계에서 개체간 CV (inter-subject CV)가 아닌 개체내 CV를 적용하여야 한다. Amlodipine Cmax 개체내 CV = 12.4–18% (고변동약물 기준 30% 미만 → 표준 BE 적용).

### 2.3 시나리오별 계산 결과

#### 시나리오 1: 기본 (Cmax 보수적 기준, GMR=0.95, Power=80%)

**이 시나리오가 권고 기준임.**

| 파라미터 | 값 |
|----------|-----|
| Intra-subject CV | 18.0% |
| sigma_w (log scale) | 0.1786 |
| GMR | 0.95 |
| delta \|ln(GMR)\| | 0.0513 |
| theta ln(1.25) | 0.2231 |
| Power | 80% |
| Alpha (one-sided) | 0.05 |
| z_alpha | 1.6449 |
| z_beta | 0.8416 |
| Dropout rate | 20% |
| **n per sequence (순수)** | **14명** |
| **n total (순수)** | **28명** |
| **n per sequence (보정)** | **18명** |
| **n TOTAL (보정, 최종)** | **36명** |

---

#### 시나리오 2: 이상적 (GMR=1.00, Power=80%, CV=18%)

| 파라미터 | 값 |
|----------|-----|
| Intra-subject CV | 18.0% |
| GMR | 1.00 |
| Power | 80% |
| **n per sequence (순수)** | **8명** |
| **n total (순수)** | **16명** |
| **n per sequence (보정)** | **10명** |
| **n TOTAL (보정, 최종)** | **20명** |

> GMR=1.00(완전 동등) 가정 시 최소 대상자 수. 실제 시험에서 GMR=1.00 보장 불가 → 보수적 시나리오(GMR=0.95) 채택.

---

#### 시나리오 3: 고검정력 (Power=90%, GMR=0.95, CV=18%)

| 파라미터 | 값 |
|----------|-----|
| Intra-subject CV | 18.0% |
| GMR | 0.95 |
| Power | 90% |
| z_beta | 1.2816 |
| **n per sequence (순수)** | **19명** |
| **n total (순수)** | **38명** |
| **n per sequence (보정)** | **24명** |
| **n TOTAL (보정, 최종)** | **48명** |

> Power=90% 요구 시 대상자 수가 36명 → 48명으로 증가. 규제 최소 요건(80%)을 초과하며 대상자 부담 및 비용 증가. 탐색적 시나리오로 제시.

---

#### 시나리오 4: AUC 기준 (CV=12%, GMR=0.95, Power=80%)

| 파라미터 | 값 |
|----------|-----|
| Intra-subject CV | 12.0% |
| sigma_w (log scale) | 0.1196 |
| GMR | 0.95 |
| Power | 80% |
| **n per sequence (순수)** | **6명** |
| **n total (순수)** | **12명** |
| **n per sequence (보정)** | **8명** |
| **n TOTAL (보정, 최종)** | **16명** |

> AUC₀₋ₜ는 CV가 낮아(7.5–12%) 별도 계산 시 최소 16명 충분. 그러나 시험은 Cmax 기준으로 대상자 수를 결정하므로 36명이 양쪽 평가변수를 모두 충족한다.

---

### 2.4 시나리오 비교 요약

| 시나리오 | CV(%) | GMR | Power | n(순수) | n(보정) | 비고 |
|---------|-------|-----|-------|---------|---------|------|
| 1. 기본 (Cmax, GMR=0.95) | 18 | 0.95 | 80% | 28 | **36** | **권고** |
| 2. 이상적 (GMR=1.00) | 18 | 1.00 | 80% | 16 | 20 | 하한 참고값 |
| 3. 고검정력 (Power=90%) | 18 | 0.95 | 90% | 38 | 48 | 탐색적 |
| 4. AUC 기준 (CV=12%) | 12 | 0.95 | 80% | 12 | 16 | AUC 단독 하한 |

---

### 2.5 실행 코드

아래 코드를 `/Users/min/Projects/clinical-trial-protocol_2/.claude/scripts/sample_size/` 디렉토리에서 pyenv Python으로 실행:

```python
import math, sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'resources', 'sample_size'))
from crossover_2x2_be import calculate_sample_size

# 시나리오 1 (권고 기준)
result = calculate_sample_size(
    intra_cv=18.0,
    equivalence_limits=(0.80, 1.25),
    power=0.80,
    alpha=0.05,
    gmr=0.95,
    dropout_rate=0.20,
)

# 시나리오 2: gmr=1.00
result2 = calculate_sample_size(intra_cv=18.0, gmr=1.00, power=0.80, alpha=0.05,
                                dropout_rate=0.20, equivalence_limits=(0.80, 1.25))

# 시나리오 3: power=0.90
result3 = calculate_sample_size(intra_cv=18.0, gmr=0.95, power=0.90, alpha=0.05,
                                dropout_rate=0.20, equivalence_limits=(0.80, 1.25))

# 시나리오 4: intra_cv=12% (AUC)
result4 = calculate_sample_size(intra_cv=12.0, gmr=0.95, power=0.80, alpha=0.05,
                                dropout_rate=0.20, equivalence_limits=(0.80, 1.25))
```

**실행 명령어**:
```bash
/Users/min/.pyenv/versions/3.12.8/bin/python3 -c "..."
# 또는 (pyenv 활성화 후)
python3 .claude/scripts/sample_size/crossover_2x2_be.py
```

---

## 3. 권고 대상자 수 (최종)

| 구분 | 대상자 수 | 근거 |
|------|---------|------|
| 통계적 최소 필요 수 (평가 가능) | 28명 | Cmax CV=18%, GMR=0.95, Power=80%, α=0.05 |
| 탈락 보정 후 등록 수 | 36명 | 탈락률 20% 보정: ⌈28 / 0.80⌉ = 35 → 짝수 조정 36명 |
| MFDS 최소 완료 요건 | 12명 | 규제 하한 (통계 근거에 의한 산출값이 우선) |

> **최종 권고**: 총 **36명 등록**, 각 sequence (TR/RT)에 **18명씩 배정**.  
> 탈락 후 최소 **28명 이상 평가 완료**를 목표로 한다.  
> MFDS 생동성시험 기준 최소 12명 완료 요건을 충족하며, 유사 시험(NCT02974439) 24명보다 보수적이다.

---

## 4. 무작위화 방법

### 4.1 무작위화 설계

- **방법**: 블록 무작위배정 (Permuted Block Randomization)
- **블록 크기**: 4 (가변 블록: 4, 8 혼용 — 배정 예측 방지)
- **배정 비율**: 1:1 (TR sequence : RT sequence)
- **층화**: 단일 기관 시험이므로 층화 무작위화 불필요

### 4.2 무작위화 절차

1. 독립적 생물통계사가 사전에 무작위배정 목록 생성 (SAS PROC PLAN 또는 R `blockrand` 패키지)
2. 봉인 봉투 또는 웹 기반 무작위화 시스템(IVRS/IWRS)으로 배정 정보 관리
3. 임상시험책임자 및 담당자는 투여 당일까지 배정 순서 비공개 유지 (공개 설계이므로 시험대상자·투여자에게는 투여 직전 공개)
4. 긴급 해제(Emergency Unblinding) 절차는 공개 설계이므로 해당 없음

### 4.3 Sequence 배정

| Sequence | Period 1 | Period 2 |
|----------|---------|---------|
| TR (홀수 번호) | 시험약(T) | 대조약(R) |
| RT (짝수 번호) | 대조약(R) | 시험약(T) |

> 2×2 Crossover에서 Period 효과, Sequence 효과, Carry-over 효과 평가 가능. Washout 21일(≥5×t½)로 carry-over 효과 최소화.

---

## 5. 통계 분석 방법

### 5.1 분석 집단

| 집단 | 정의 |
|------|------|
| Safety Population | 시험약 또는 대조약을 1회 이상 투여받은 모든 대상자 |
| PK (Full Analysis) Set | 적어도 1개 period의 유효 PK 파라미터를 가진 대상자 |
| **Per-Protocol (PP) Set** | PK Set 중 중대한 프로토콜 위반이 없는 대상자 — **생동성 1차 분석 집단** |

> 생동성 판정은 PP Set 기준. PK Set는 민감도 분석으로 활용.

### 5.2 1차 분석 — 생물학적동등성 판정

**평가변수**: AUC₀₋ₜ, Cmax (동시 충족 필요)

**분석 모형 (혼합효과 ANOVA)**:

```
ln(Y_ijk) = μ + S_i + P_j + F_k + ε_ijk
```

| 효과 | 설명 |
|------|------|
| μ | 전체 평균 (intercept) |
| S_i | Sequence 효과 (고정: TR, RT) |
| Subject(Sequence) | 대상자 효과 (무작위: 개체내 반복 구조) |
| P_j | Period 효과 (고정: Period 1, 2) |
| F_k | 제형(Formulation) 효과 (고정: T, R) — 관심 효과 |
| ε_ijk | 잔차 (개체내 오차) |

**소프트웨어**: SAS PROC MIXED 또는 R `lme4`/`nlme`

**추정량**:
- GMR = exp(μ_T − μ_R) — 기하평균비
- 90% 신뢰구간 (CI) = exp(추정치 ± t₀.₀₅, df × SE)

**판정 기준**:
- AUC₀₋ₜ 90% CI **AND** Cmax 90% CI **모두** 80.00–125.00% 이내 → 생물학적 동등

**유의수준**: 각 one-sided test α = 0.05 (전체적으로 90% CI 방식 = TOST)

### 5.3 2차 분석

| 파라미터 | 분석 방법 | 목적 |
|----------|---------|------|
| AUC₀₋∞ | 동일 혼합효과 ANOVA, GMR + 90% CI | 참고용 생동성 지표 |
| Tmax | Wilcoxon Signed-Rank Test (비모수) | 중앙값 비교 |
| t½ | 기술통계 (평균, 표준편차, CV%) | 배경 특성 확인 |
| λz (소실속도상수) | 기술통계 | 배경 특성 확인 |

### 5.4 비구획분석 (Non-Compartmental Analysis, NCA)

- **소프트웨어**: Phoenix® WinNonlin® (Certara) 또는 R `PKNCA` 패키지
- **AUC 계산**: Linear-Log trapezoidal method (흡수기 linear, 소실기 log)
- **AUC₀₋∞**: AUC₀₋ₜ + C_last / λz (외삽 <20% 권장)
- **Cmax**: 실측치 (모델 추정 아님)
- **λz**: 소실기 최소 3개 시점, r² ≥ 0.9

### 5.5 안전성 분석

- **이상반응(AE)**: MedDRA 코딩, 빈도표 (System Organ Class / Preferred Term)
- **활력징후, 임상검사치, ECG**: 기술통계, 기저치 대비 변화량
- 분석 집단: Safety Population

---

## 6. 결측치 처리 방법

### 6.1 결측치 분류 및 처리 원칙

| 유형 | 정의 | 처리 방법 |
|------|------|---------|
| 채혈 시점 누락 (단일) | 1–2개 시점 채혈 실패 | 인접 시점으로 AUC 계산 (사다리꼴법 연속 적용); 누락 시점 보간 없음 |
| Cmax 누락 | Cmax 시점 채혈 실패 | 해당 period PK 분석 제외, 대상자 PP Set에서 제외 고려 |
| 구토·재투여 | 투여 후 2시간 내 구토 | 해당 period 제외, 필요 시 재투여 (프로토콜 명시) |
| Period 전체 누락 | 2nd period 미완료 | 해당 대상자 전체 PK 분석 제외 (crossover 특성상 두 period 모두 필요) |
| 탈락 (dropout) | 철회, AE, 기타 | PP Set 제외; Safety Population 포함 |

### 6.2 민감도 분석 (Sensitivity Analysis)

- PP Set 결과와 PK (Full Analysis) Set 결과를 병렬 제시하여 결측치 영향 평가
- 결측 메커니즘이 MCAR(완전 무작위 결측)이 아닌 것으로 의심될 경우 별도 기술

### 6.3 Carry-over 효과 평가

- Sequence × Period 교호작용 검정 (α=0.10 기준)
- 유의한 carry-over 의심 시 1st period 데이터만으로 추가 분석 (참고용)

---

## 7. 통계 소프트웨어 및 검증

| 소프트웨어 | 용도 |
|----------|------|
| Phoenix® WinNonlin® 또는 R `PKNCA` | NCA (비구획분석) |
| SAS® 9.4 (PROC MIXED) 또는 R `lme4` | 혼합효과 ANOVA, GMR + 90% CI |
| SAS PROC PLAN 또는 R `blockrand` | 무작위배정 목록 생성 |
| Python 3.12 (`scipy`, `crossover_2x2_be.py`) | Sample size 계산 |

---

## 8. 참고 문헌

1. Chow S-C, Liu J-P. *Design and Analysis of Bioavailability and Bioequivalence Studies*, 3rd ed. CRC Press, 2009, Chapter 5.
2. 식품의약품안전처. 생물학적동등성시험 기준. 식약처 고시.
3. EMA. Guideline on the Investigation of Bioequivalence. CPMP/EWP/QWP/1401/98 Rev. 1, 2010.
4. FDA. Guidance for Industry: Bioavailability and Bioequivalence Studies Submitted in NDAs or INDs. 2014.
5. Wang Y et al. Bioequivalence of generic amlodipine 5mg in Chinese healthy volunteers. *Drug Des Devel Ther* 2020; 14:633–640. PMID: 32034814.
6. ClinicalTrials.gov NCT02974439 — Amlodipine 5mg BE study (2×2 crossover, 24명/arm, washout 15일).
7. ICH E6(R3). Good Clinical Practice. 2023.
