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

> **협의 순서 원칙**: 대상자 선정/제외기준 → 연구설계 → PK 채혈/평가변수 → 안전성/투여조건. 대상자 정의가 모든 후속 결정(설계, sample size, 안전성 모니터링)의 전제이므로 가장 먼저 협의한다.

### Step 1: 선정/제외기준 협의 (최우선)

`.claude/references/templates/inclusion_exclusion_criteria.md`를 Read하여 표준 템플릿을 사용자에게 제시한다.

**진행 절차:**
1. 템플릿의 1.1 선정기준, 1.2 제외기준 전문을 사용자에게 그대로 제시
2. 템플릿의 "시험별 커스터마이징 가이드"(A~F)를 순서대로 협의:
   - **A. 대상자 성별**: 남성만 vs 남녀 모두 (여성 포함 시 임신검사·피임 요건 추가)
   - **B. 연령 범위**: 통상 19~55세, 고령자 코호트 별도 가능
   - **C. BMI 기준**: 표준(18.5~25.0) vs 관대한 범위(17.5~30.5)
   - **D. IRB 명칭**: `[시험기관명]` placeholder를 실제 기관명으로 치환
   - **E. 시험 유형별 추가 항목**: 템플릿 가이드 표 참조 (DDI/BE/FE/QTc/FIH 등)
   - **F. 약물 특이 항목**: `_workspace/01_research_report.md`의 약물 정보를 바탕으로 추가 (알레르기, contraindication, 약물 대사 다형성 등)
3. 확정된 기준을 `_workspace/00_input/design_decisions.md`의 "선정/제외기준" 섹션에 번호와 함께 기록

> **주의**: 선정/제외기준은 IRB 심사·MFDS IND 승인의 핵심 검토 대상이다. 사용자의 명시적 확정 없이 다음 단계로 진행하지 않는다.

### Step 2: 연구설계 옵션 제시

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

### Step 3: 세부 설계 요소 협의
사용자와 순차적으로 확정:
1. **연구설계 확정**: parallel vs crossover → crossover라면 어떤 유형?
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
4. **1차 평가변수**: AUC (전체 또는 절단), Cmax, GMR, ddQTcF 등 — 시험 목적의 핵심 변수
5. **2차 평가변수**: 추가 PK 파라미터(Tmax, t½, CL/F 등), 보조 PD/유효성 변수
6. **유효성/약력학(PD) 평가 항목**: 시험 목적에 부합하는 약효·약리학적 효과 측정. 시험 유형별 권장 항목:

   | 시험 유형 | 유효성/PD 평가 요소 |
   |----------|-------------------|
   | **DDI** | Probe 약물의 PK 변화율(GMR 90% CI), 대사효소 활성 마커(예: 4β-hydroxycholesterol/cholesterol ratio for CYP3A4), 수송체 활성 변화 |
   | **BE** | 동등성 판정 (90% CI 80~125% 또는 NTI/HVD 기준), AUC 및 Cmax 차이의 임상적 의의 |
   | **FE** | 공복 vs 식후 AUC/Cmax 비, Tmax 변화, 흡수 속도/범위 영향 |
   | **QTc** | ddQTcF (ΔΔQTcF), C-QTc 관계 모델, ECG 형태 변화, 양성 대조군 assay sensitivity |
   | **FIH/SAD** | 약리학적 활성 마커(있을 시), 수용체 점유율, 표적 결합 |
   | **MAD** | 정상상태 PD 마커, 누적 효과, 내성(tolerance) 지표 |
   | **ADME** | 대사체 프로파일, 인체 특이 대사체 식별, 물질 수지(mass balance) |
   | **Special Pop** | 정상군 대비 PK 차이의 임상적 의의(용량 조절 권고 근거) |

   **협의 사항:**
   - PD 바이오마커: 어떤 마커를 측정할 것인가? (시험약 작용 기전 기반)
   - 측정 시점: PK 채혈과 동시 또는 별도 일정?
   - 분석 방법: assay 검증 상태, 분석 기관
   - PK-PD 모델링 계획: Emax, sigmoid Emax, 직접/간접 효과 모델 등
7. **안전성 평가 항목**: 이상반응, 활력징후, ECG, 실험실검사
8. **유전체/대사체 분석 계획** (translational-scientist 보고서 기반, BE/FE 시험 외):

   `_workspace/01_research_ts.md`의 권장 사항을 참조하여 협의:

   **약물유전체(PG) 분석:**
   - 분석 여부 (필수 / 선택 / 미수행)
   - 분석 대상 유전자 (예: CYP2C19, CYP2D6, KCNH2 등)
   - 분석 시점 (스크리닝 / 투여 전 / 사후)
   - **별도 동의 필수** (생명윤리법 인체유래물 연구 적용)
   - 검체 보관 기간 및 폐기 절차

   **대사체 분석:**
   - 분석 여부 (해당 시)
   - 측정 방법 (LC-MS/MS 등) 및 대상 마커 (예: 4β-OH-cholesterol/cholesterol for CYP3A4)
   - 채혈 시점 정렬 (PK 채혈과 동시 vs 별도)
   - 분석 기관 (자체 vs 외부 위탁)

   **인체유래물 보관 정책:**
   - 향후 분석을 위한 잔여 검체 보관 여부
   - 보관 기간, 보관 장소, 2차 활용 동의 (별도 동의서 항목)
   - 동의 철회 시 검체 폐기 절차

   > **생명윤리법 적용 검토**: PG 분석 또는 잔여 검체 보관이 포함되면 IRB 외에 기관생명윤리위원회 추가 심의 필요 여부 확인. ICF에 별도 동의 섹션 추가 필요 (icf-writer가 자동 반영)

9. **휴약기(Washout)**: PK 파라미터 기반 산출
   - 공식: ≥ 10×t½(max) → 실용적 단위로 올림
   - 잔류 농도 추정: Period 2 투약 시 Cmax의 < 0.1% 보장
   - 규제 요건(MFDS: ≥ 5×t½)과 비교
10. **투여 조건**: 공복/식후, 수분 제한 등

### Step 4: 설계 결정 기록
확정된 설계 전체(선정/제외기준 + 연구설계 + 세부 요소 + 유전체/대사체 분석 계획)를 `_workspace/00_input/design_decisions.md`에 Write한다.

> **PG/오믹스 결정 사항이 포함된 경우** ICF에 별도 동의 섹션이 자동 추가되도록 design_decisions.md에 명시적으로 기록 (icf-writer가 Read하여 반영).

## Phase 5: 통계 설계

### Step 5: Biostatistician 에이전트 호출
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

### Step 6: 통계 결과 검토
통계 설계 결과를 사용자에게 제시:
- Sample size (탈락률 반영 전/후)
- 검정력
- 주요 파라미터 (CV%, 동등성 한계, 유의수준)
- 사용자가 파라미터 변경을 원하면 biostatistician 재호출

## 산출물
- `_workspace/00_input/design_decisions.md` — 확정된 설계
- `_workspace/00_input/statistical_design.md` — 통계 설계 (Python 코드 포함)
