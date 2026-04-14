---
name: synopsis
description: "임상시험 Synopsis 생성. 설계 협의 결과를 1-3페이지 요약 문서로 작성한다. 인자로 설계 변형을 지정할 수 있다 (예: /synopsis crossover 2x2). /synopsis 또는 시놉시스 요청 시 사용."
---

# /synopsis — Synopsis 생성 (Phase 6)

## 전제 조건
- `_workspace/00_input/design_decisions.md` 존재 (설계 협의 완료)
- `_workspace/00_input/statistical_design.md` 존재 (통계 설계 완료)
- 미존재 시: "먼저 /design으로 설계 협의를 완료해주세요" 안내

## 인자 처리
- `/synopsis` → 기본 설계로 synopsis 생성
- `/synopsis crossover 2x2` → 2×2 crossover 변형
- `/synopsis parallel` → parallel design 변형
- `/synopsis replicate 2x4` → 2×4 replicate crossover 변형
- 변형 지정 시 해당 설계에 맞게 sample size와 통계 방법을 조정

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
### 4.2 주요 선정 기준
### 4.3 주요 제외 기준
### 4.4 대상자 수: N명 (근거: CV=X%, 검정력=X%)
## 5. 시험약 및 투여
## 6. 평가 변수
### 6.1 1차 평가변수
(절단 AUC 적용 시: AUC₀₋₇₂ₕ + Cmax, 근거 명시)
(미적용 시: AUC₀₋ₜ + Cmax)
### 6.2 2차 평가변수
### 6.3 절단 AUC 적용 근거 (해당 시)
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
## 10. 통계 분석
### 10.1 Sample size 근거
### 10.2 1차 분석 방법
### 10.3 2차 분석 방법
## 11. 방문 일정 요약
## 12. 시험 기간
```

## 작성 원칙
- 1-3 페이지로 간결하게 (전체 계획서의 핵심 요약)
- 모든 설계 결정에 근거 명시 (연구 보고서 reference)
- Sample size 근거에 Python 코드 결과 인용
- 변형 synopsis 작성 시: 변형 사유와 기본 설계와의 차이점을 명시
