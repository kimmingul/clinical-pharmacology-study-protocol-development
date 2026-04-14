---
name: design
description: "대화형 시험 설계 협의 + 통계 설계. 수집된 자료를 바탕으로 연구설계, PK 채혈시점, 평가변수, sample size를 사용자와 협의한다. /design 또는 설계, 디자인, 시험설계 요청 시 사용."
---

# /design — 대화형 설계 협의 + 통계 설계 (Phase 4-5)

## 전제 조건
- `_workspace/01_research_report.md`가 존재해야 함
- 미존재 시: "먼저 /research로 자료 수집을 완료해주세요" 안내

## Phase 4: 대화형 설계 협의

메인 에이전트가 사용자와 직접 대화하여 설계를 확정한다. 서브 에이전트를 호출하지 않는다.

### Step 1: 연구 자료 기반 설계 옵션 제시
`_workspace/01_research_report.md`를 Read하고, 시험 유형에 맞는 설계 옵션을 제시한다.

**연구설계 옵션 (시험 유형별):**

| 시험 유형 | 주요 설계 옵션 |
|----------|--------------|
| DDI | One-sequence, Crossover 2×2, Parallel |
| BE | Crossover 2×2, Replicate 2×3/2×4 (고변동 약물), Parallel (장기 반감기) |
| FE | Crossover 2×2 |
| QTc | Crossover 4×4 (Williams), Parallel |
| FIH/SAD | 순차 증량, 위약 대조, 센티넬 도징 |
| MAD | 반복 투여, 위약 대조, 코호트 기반 |

각 옵션에 대해 제시:
- 장단점
- 유사 시험 사례 (연구 보고서에서 인용)
- 규제 기관 선호도

### Step 2: 세부 설계 요소 협의
사용자와 순차적으로 확정:
1. **연구설계**: parallel vs crossover → crossover라면 어떤 유형?
2. **PK 채혈 시점**: 배경 조사 보고서의 "PK 기반 시험 설계 파라미터" 섹션을 참조하여 제시
   - Tmax 기반 밀집 구간 (Tmax ± 50% 구간에 1–2시간 간격)
   - 소실기: t½ 기반 점진 확대
   - 각 시점의 설계 근거를 명시
3. **절단 AUC 적용 여부 + MFDS 규제 조화**: t½ > 24시간이면 AUC₀₋₇₂ₕ 적용을 제안
   - 적용 시: 채혈 종료 ~72시간, 1차 평가변수 = AUC₀₋₇₂ₕ + Cmax
   - 미적용 시: 채혈 종료 ≥ 3×t½, 1차 평가변수 = AUC₀₋ₜ + Cmax
   - **MFDS 규제 조화 필수 안내**: MFDS "최소 3×t½ 채혈" 요건과 절단 AUC 72시간의 충돌 가능성을 사용자에게 명시적으로 설명
   - **컨틴전시 전략 협의**: MFDS 불수용 시 대체 방안 미리 합의
     - 옵션 A: AUC₀₋ₜ를 공동 1차 평가변수로 추가 (dual primary)
     - 옵션 B: 채혈 기간을 ≥3×t½로 연장하여 AUC₀₋ₜ 전환
   - **MFDS 사전 협의 의무화**: "권장"이 아닌 "IND 신청 전 반드시 완료"로 안내
4. **1차 평가변수**: AUC (전체 또는 절단), Cmax, GMR, ddQTcF 등
5. **2차 평가변수**: 추가 PK 파라미터, PD 마커 등
6. **안전성 평가 항목**: 이상반응, 활력징후, ECG, 실험실검사
7. **휴약기(Washout)**: PK 파라미터 기반 산출
   - 공식: ≥ 10×t½(max) → 실용적 단위로 올림
   - 잔류 농도 추정: Period 2 투약 시 Cmax의 < 0.1% 보장
   - 규제 요건(MFDS: ≥ 5×t½)과 비교
8. **투여 조건**: 공복/식후, 수분 제한 등

### Step 3: 설계 결정 기록
확정된 설계를 `_workspace/00_input/design_decisions.md`에 Write한다.

## Phase 5: 통계 설계

### Step 4: Biostatistician 에이전트 호출
```
Agent(
  description: "통계 설계 및 sample size 계산",
  model: "sonnet",
  name: "biostatistician",
  prompt: "먼저 .claude/agents/biostatistician.md를 Read하여 역할을 숙지하라.
설계 결정: _workspace/00_input/design_decisions.md를 Read하라.
배경 자료: _workspace/01_research_report.md를 Read하라.
.claude/scripts/sample_size/ 내 해당 Python 코드를 Read하여 파라미터를 채워 실행하라.

산출물에 다음을 포함하라:
1. Sample size 계산 결과
2. 실행한 Python 코드 전체
3. 무작위화 방법
4. 통계 분석 방법 (1차/2차)
5. 결측치 처리 방법

산출물을 _workspace/00_input/statistical_design.md에 Write하라."
)
```

### Step 5: 통계 결과 검토
통계 설계 결과를 사용자에게 제시:
- Sample size (탈락률 반영 전/후)
- 검정력
- 주요 파라미터 (CV%, 동등성 한계, 유의수준)
- 사용자가 파라미터 변경을 원하면 biostatistician 재호출

## 산출물
- `_workspace/00_input/design_decisions.md` — 확정된 설계
- `_workspace/00_input/statistical_design.md` — 통계 설계 (Python 코드 포함)
