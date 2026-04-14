---
name: synopsis
description: "임상시험 Synopsis 생성. 설계 협의 결과를 1-3페이지 요약 문서로 작성한다. 인자로 설계 변형을 지정할 수 있다 (예: /synopsis crossover 2x2). /synopsis 또는 시놉시스 요청 시 사용."
---

# /synopsis — Synopsis 생성 (Phase 6)

## 전제 조건
- `_workspace/00_input/design_decisions.md` 존재 (설계 협의 완료)
- `_workspace/00_input/statistical_design.md` 존재 (통계 설계 완료)
- 미존재 시: "먼저 /design으로 설계 협의를 완료해주세요" 안내

## 원칙: Phase 4 협의 결과 전량 반영

Synopsis는 Phase 4에서 확정된 **모든 설계 결정**을 포함해야 한다. design_decisions.md의 섹션 중 하나라도 Synopsis에 누락되면, 해당 결정이 이후 Protocol/ICF 작성에서 참조되지 못하는 위험이 있다. 특히 다음 항목은 반드시 포함한다:
- 선정/제외기준 (확정된 전체 목록)
- 유효성/약력학(PD) 평가 항목 (해당 시)
- 유전체/대사체 분석 계획 (해당 시)

## 인자 처리

변형을 지정하면 해당 설계에 맞게 sample size와 통계 방법을 조정한다. 지원되는 인자는 `.claude/scripts/sample_size/` 디렉토리의 스크립트와 1:1 매핑된다.

| 인자 | 설계 | 매핑 스크립트 |
|------|------|-------------|
| (생략) | 기본 설계 (design_decisions.md 결정 반영) | — |
| `crossover 2x2` | 2×2 crossover (BE/DDI/FE 공통) | `crossover_2x2_be.py` 또는 `crossover_2x2_ddi.py` |
| `crossover 2x3` | 2-sequence × 3-period replicate | `replicate_crossover_be.py` |
| `crossover 2x4` | 2-sequence × 4-period replicate (RSABE) | `replicate_crossover_be.py` |
| `crossover 4x4` | Williams 4×4 | `williams_4x4.py` |
| `one-sequence` | 단일 순서 DDI | `one_sequence_ddi.py` |
| `parallel` | Parallel (연속형 기본) | `parallel_continuous.py` |
| `parallel binary` | Parallel 이분형 | `parallel_binary.py` |

> 미지원 인자 입력 시 위 표를 제시하고 재입력을 요청한다.

## 산출물 파일명
- 기본: `_workspace/02_synopsis.md`
- 변형: `_workspace/02_synopsis_{variant}.md` (예: `02_synopsis_crossover_2x2.md`)

## Synopsis 구조

```markdown
# 임상시험 Synopsis

## 1. 시험 제목
## 2. 시험 목적
### 2.1 1차 목적
### 2.2 2차 목적
## 3. 시험 설계
- 설계 유형, 맹검, 무작위화
- 처리군 구성
## 4. 대상자
### 4.1 대상 집단
### 4.2 선정 기준 (design_decisions.md의 전체 항목 반영)
### 4.3 제외 기준 (design_decisions.md의 전체 항목 반영)
### 4.4 대상자 수: N명 (근거: CV=X%, 검정력=X%)
## 5. 시험약 및 투여
## 6. 평가 변수
### 6.1 1차 평가변수
(시험 유형별 핵심 변수: AUC/Cmax, GMR, ddQTcF 등. 절단 AUC 적용 시 AUC₀₋₇₂ₕ, 미적용 시 AUC₀₋ₜ. 용어는 시험 목적에 따라 "유효성 평가" 또는 "약동학/약력학 평가" 적용 — Phase 1 용어 가이드 참조)
### 6.2 2차 평가변수
### 6.3 유효성/약력학(PD) 평가 항목 (해당 시)
- 시험 유형별 PD 평가 요소:
  - DDI: Probe 약물 PK 변화율(GMR), 대사효소 활성 마커
  - QTc: ddQTcF (ΔΔQTcF), C-QTc 모델
  - FIH/MAD: PD 바이오마커, 수용체 점유율
  - ADME: 대사체 프로파일
- 선정된 바이오마커, 측정 시점, 분석 방법, PK-PD 모델링 계획
### 6.4 절단 AUC 적용 근거 (해당 시, BE/FE 주로 적용)
- t½ > 24시간 여부
- FDA/MFDS 규제 상태
- MFDS 사전 협의 권장 여부
## 7. PK 채혈 시점 및 근거
### 7.1 채혈 시점표
(시점 #, 투여 후 시간, 구간, PK 파라미터 기반 설계 근거)
### 7.2 채혈 시점 설계 원칙
- Tmax 기반 밀집 구간 정의
- t½ 기반 총 채혈 기간 산출
- 총 채혈량
## 8. 휴약기(Washout) 근거
- t½(max) 값 및 출처
- 산출 공식: ≥ 10×t½(max)
- 잔류 농도 추정 (< 0.1% Cmax)
- 규제 요건(MFDS: ≥ 5×t½) 비교
- 최종 설정값
## 9. 안전성 평가
## 10. 유전체/대사체 분석 계획 (해당 시, BE/FE 외)
### 10.1 약물유전체(PG) 분석
- 분석 여부 (필수/선택/미수행)
- 분석 대상 유전자 (예: CYP2C19, CYP2D6)
- 분석 시점, 분석 방법, 분석 기관
- 별도 동의(생명윤리법) 요건
### 10.2 대사체 분석 (해당 시)
- 분석 대상 (인체 특이 대사체 / 내인성 바이오마커)
- 측정 방법 (LC-MS/MS), 채혈 시점
### 10.3 인체유래물 보관 정책
- 잔여 검체 보관 여부, 기간, 장소
- 2차 활용 동의 조항
## 11. 통계 분석
### 11.1 Sample size 근거
### 11.2 1차 분석 방법
### 11.3 2차 분석 방법
## 12. 방문 일정 요약
## 13. 시험 기간
```

### 시험 유형별 특화 섹션 안내

위 구조는 표준이며, 시험 유형에 따라 일부 섹션의 상세도가 달라진다:

| 시험 유형 | 강조되는 섹션 | 간소화 가능 섹션 |
|----------|-------------|--------------|
| BE/FE | 6.4 절단 AUC, 7. PK 채혈, 8. Washout | 6.3 PD 평가, 10. 유전체/대사체 (생략) |
| DDI | 6.1 GMR, 6.3 PD 평가(probe 약물), 10.1 PG(CYP PM/EM) | — |
| QTc | 6.3 PD 평가(ddQTcF, C-QTc) | 6.4 절단 AUC (해당 없음) |
| FIH/SAD/MAD | 5. 용량 증량, 6.3 PD 바이오마커, 9. 안전성 | 6.4 절단 AUC |
| ADME | 10.2 대사체 분석(MIST) | — |
| Special Pop | 4.1 대상 집단(기능 분류), 10.1 PG | — |

## 작성 원칙
- 1-3 페이지로 간결하게 (전체 계획서의 핵심 요약)
- 모든 설계 결정에 근거 명시 (연구 보고서 reference)
- Sample size 근거에 Python 코드 결과 인용
- 변형 synopsis 작성 시: 변형 사유와 기본 설계와의 차이점을 명시
