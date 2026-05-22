# Codex 분석 보고서 — Python 스크립트 품질 (재구성)

> Codex가 read-only sandbox 제약으로 `/tmp/codex_report.md`를 직접 저장하지 못해, stdout 출력 + 통합자(Claude Opus) 검증 후 본 파일로 재구성. 원본 trace: `/tmp/codex_run.log` (3527 lines).

---

## 1. Sample size 스크립트

### 1.1 강점

- 모든 스크립트가 `print_result()` 공용 출력 포맷을 사용해 산출물 인용 시 trace 정보가 충분
- `utils/power_analysis.py`의 `normal_quantile`/`t_quantile`/`adjust_for_dropout`가 단일 출처로 추출되어 중복 최소화
- 각 스크립트 docstring이 가이드라인 출처(Chow, Patterson, FDA)를 언급

### 1.2 결함 / 위험

#### Critical

- **`crossover_2x2_be.py:104-110`** — 2×2 crossover BE 공식 명명 오류
  - 표준 공식 (Chow & Liu 2008, Patterson & Jones 2017): `N_total = ⌈(z_α + z_β)² · 2 · σ_w² / margin²⌉`
  - 코드: 동일 식의 결과를 `n_per_seq`로 명명한 뒤 `n_total = 2 × n_per_seq`로 재산출 → **실제 표본 대비 2배 과대**
  - 검증: CV=25%, GMR=0.95, power=0.80, α=0.05 → 정답 N=26, 코드 출력 n_total=52
  - **오염 범위**: `e2e/v1_2026_04_06_BE/_workspace/00_input/statistical_design.md:40-42`에 잘못된 공식이 그대로 인용되어 commit됨. 산출된 protocol draft는 별도 수동 보정(36명) 적용. 향후 BE 시험에서 자동 산출 시 100% 재발

- **`crossover_2x2_ddi.py:52`이하** — `crossover_2x2_be.py`와 동일 구조이므로 동일 결함 보유 추정. 검증 권장

#### Major

- **`replicate_crossover_be.py` RSABE 구현** — `theta_scaled = regulatory_constant × σ_w` 단순 근사. FDA RSABE 공식 판정식(linearized criterion: `(Y_T − Y_R)² − θ_s · σ_WR² ≤ 0`, upper 95% bound)과 다름. 규제 제출 문서에 인용 시 부적합

- **`williams_6x3_ddi.py` 통계 추론 오류** — Codex 발견:
  - IUT(Intersection-Union Test)에서 α 조정 불필요한 것은 type I error 측면
  - 그러나 **두 방향 동시 성공 확률(joint power)**은 곱셈 효과로 감소
  - 각 방향 power=0.80이고 두 endpoint가 독립이라면 둘 다 성공할 확률 ≈ 0.64
  - 현 코드는 큰 n을 채택해 단방향 power만 80%로 보장 → joint power는 보고되지 않음
  - 사용자가 "양방향 모두 BE 입증" 가설을 채택했다면 joint power 산출이 필요

- **`one_sequence_ddi.py`** — `n_periods` 파라미터가 출력에는 포함되지만 분산 추정·검정력 식에 반영되지 않음. 사용자에게 혼란 유발

#### Minor

- **scipy 강결합** — `utils/power_analysis.py:15` `from scipy.stats import norm, t`. dependency 파일(`requirements.txt`, `pyproject.toml`) 부재. README에는 `pip install scipy` 안내가 있으나 `python_requires`/lock 부재로 재현성 약함

- **FIH 스크립트 입력 검증 부재** — `fih/starting_dose_calculation.py`, `fih/dose_escalation.py`의 `NOAEL`, `HED`, `safety_factor`, `body_weight`, `EC50`, `start_dose` 인자가 양수 제약 없음. 0/음수 입력 시 zero division 또는 임상적으로 무의미한 결과

- **테스트 부재** — `tests/`, `pytest.ini`, `conftest.py` 모두 없음. 회귀 검증이 e2e 산출물 비교에만 의존

### 1.3 개선 제안

1. **즉시 패치**: `crossover_2x2_be.py`/`crossover_2x2_ddi.py`에서 `n_per_seq = math.ceil(n_total / 2)`로 변경, 변수명도 `n_total` 우선
2. **회귀 fixture**: `tests/test_sample_size.py`에서 표준 케이스(CV=25/30/40%, GMR=0.95/1.00, power=0.80/0.90)에 대해 PASS Sample Size 4.0 또는 R `PowerTOST::sampleN.TOST` 결과와 ±2 이내 비교
3. **RSABE 재구현**: FDA RSABE linearized criterion 식 그대로 구현, scaled limit은 `θ_s = (ln(1.25)/0.25)² = 0.7972` 등 명시 상수 사용
4. **Joint power 출력**: Williams 6×3에서 `joint_power = power_AB × power_BA` 추가 보고

---

## 2. FIH 스크립트

### 2.1 강점

- NOAEL → HED → MRSD/MABEL 흐름이 FDA 2005 guidance 구조와 일치

### 2.2 결함

- 입력 양수 검증 부재 (§1.2 Minor)
- `dose_escalation.py`의 3+3·mTPI·BOIN 구현 다양성은 확보되어 있으나 mTPI/BOIN 설계 파라미터(`eps1`, `eps2`, target toxicity probability) 문서화가 약함

### 2.3 개선 제안

1. 모든 인자에 `if value <= 0: raise ValueError(...)` 가드
2. mTPI/BOIN의 단위 테스트로 알려진 표(논문 Table) 재현 확인
3. PK-driven 초기 용량(`AUC_target`) 옵션 추가 검토

---

## 3. 공통 권고 (테스트, 패키징, 재현성)

| 항목 | 현황 | 권고 |
|------|------|------|
| Dependency 고정 | `pip install scipy` 안내만 존재 | `pyproject.toml` + `requirements.txt` 추가, `python_requires=">=3.10"` |
| Lockfile | 없음 | `uv.lock` 또는 `requirements.lock` |
| 테스트 | 없음 | `pytest` + GitHub Actions CI |
| 재현성 fixture | e2e 산출물에서 추론 | `tests/golden/` 표준 케이스 보관 |
| Random seed | 결정적 (랜덤 미사용) | 변경 시 seed 고정 정책 명시 |
| 로깅 | print만 | `logging` 모듈 + 산출물에 `git rev-parse HEAD` 기록 |

---

## 4. 우선순위 TOP 5 개선안

| # | severity | 항목 | 영향 | 난이도 |
|---|----------|------|------|--------|
| 1 | **Critical** | `crossover_2x2_be.py` / `crossover_2x2_ddi.py` N 2배 과대 산출 수정 | BE/DDI 시험 자동 산출 신뢰성 — 규제 제출 직결 | Low (4줄 수정 + 회귀 테스트) |
| 2 | **Major** | RSABE 공식을 FDA 판정식으로 재구현 | HVD(highly variable drug) 시험 신뢰성 | Medium (참고: PowerTOST source) |
| 3 | **Major** | Williams 6×3 joint power 산출 추가 | 양방향 DDI 시험 검정력 보고 정확성 | Low |
| 4 | **Major** | `tests/` 디렉토리 + sample size 회귀 fixture | 향후 회귀 방지 | Medium |
| 5 | **Minor** | `pyproject.toml` + lockfile + FIH 입력 검증 | 재현성·견고성 | Low |

---

## 외부 출처

- FDA MRSD Guidance (2005): https://www.fda.gov/regulatory-information/search-fda-guidance-documents/estimating-maximum-safe-starting-dose-initial-clinical-trials-therapeutics-adult-healthy-volunteers
- FDA Clinical DDI Guidance (2020): https://www.fda.gov/media/135586/
- FDA BE PK Endpoints Draft Guidance: https://www.fda.gov/files/drugs/published/GUI_Rev_Draft_Bioequivalence%20Studies%20With%20Pharmacokinetic%20Endpoints%20for%20Drugs%20Submitted%20Under%20an%20ANDA%20%281%29.pdf
- Chow, Wang & Shao (2008) *Sample Size Calculations in Clinical Research*
- Patterson & Jones (2017) *Bioequivalence and Statistics in Clinical Pharmacology*
