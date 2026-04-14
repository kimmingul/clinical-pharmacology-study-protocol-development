# `.claude/scripts/` — 실행 가능한 Python 스크립트

에이전트가 실행 시 활용하는 Python 코드 템플릿 모음 (sample size 계산, FIH 용량 산출).

규제 가이드라인 참조 파일은 별도 디렉토리 `.claude/references/guidelines/` 참조.

---

## 디렉토리 구조

| 경로 | 설명 |
|------|------|
| `sample_size/` | Sample size 계산 Python 스크립트 (BE, DDI, parallel, replicate, Williams 등) |
| `fih/` | FIH 시험 전용 산출 코드 (초기 용량, 용량 증량 스킴) |

---

## Sample Size 스크립트 (`sample_size/`)

| 파일 | 적용 설계 |
|------|---------|
| `parallel_continuous.py` | 병렬 설계, 연속형 엔드포인트 |
| `parallel_binary.py` | 병렬 설계, 이분형 엔드포인트 |
| `crossover_2x2_be.py` | 2×2 crossover BE (AUC/Cmax) |
| `crossover_2x2_ddi.py` | 2×2 crossover DDI (GMR) |
| `replicate_crossover_be.py` | Replicate crossover BE (RSABE 포함) |
| `one_sequence_ddi.py` | 단일 순서 DDI 시험 |
| `williams_4x4.py` | 4-sequence × 4-period Williams 설계 |
| `utils/power_analysis.py` | 공통 검정력/유효 표본 수 유틸리티 |

---

## FIH 산출 스크립트 (`fih/`)

| 파일 | 용도 |
|------|------|
| `starting_dose_calculation.py` | NOAEL → HED → MRSD/MABEL 산출 |
| `dose_escalation.py` | 용량 증량 스킴 생성 (3+3, mTPI, BOIN 등) |

---

## 사용 원칙

- 에이전트는 스크립트를 `Read`로 읽어 파라미터를 채운 후 `Bash`로 실행한다
- **코드 투명성**: sample size 계산에 사용한 Python 코드 전체를 산출물에 포함하여, 사용자가 파라미터를 변경하여 재실행할 수 있도록 한다
- 신규 스크립트 추가 시 이 README도 업데이트한다
