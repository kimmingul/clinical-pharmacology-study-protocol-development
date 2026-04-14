---
name: compare
description: "여러 Synopsis를 비교표로 제시한다. 설계 유형, sample size, 기간, 장단점을 나란히 비교하여 최적의 설계를 선택할 수 있게 한다. /compare 또는 시놉시스 비교 요청 시 사용."
---

# /compare — Synopsis 비교 (Phase 6)

## 전제 조건
- `_workspace/` 내에 `02_synopsis*.md` 파일이 2개 이상 존재해야 함
- 미존재 시: "/synopsis로 2개 이상의 변형을 먼저 생성해주세요" 안내

## 워크플로우

### Step 1: Synopsis 파일 수집
`_workspace/` 내 `02_synopsis*.md` 패턴의 모든 파일을 Glob으로 찾고 Read한다.

### Step 2: 비교표 생성

| 항목 | Synopsis A | Synopsis B | Synopsis C |
|------|-----------|-----------|-----------|
| 설계 유형 | | | |
| Sequence/Period | | | |
| 대상자 수 | | | |
| 시험 기간 | | | |
| Washout 기간 | | | |
| 검정력 | | | |
| 복잡도 | | | |
| 규제 선례 | | | |
| 장점 | | | |
| 단점 | | | |
| 비용 영향 | | | |

### Step 3: 권고 의견
- 각 설계의 trade-off를 분석하여 권고 의견 제시
- 유사 시험의 설계 선택 사례 인용
- 규제 기관 선호도 반영

### Step 4: 사용자 선택
사용자가 선택한 synopsis를 `_workspace/02_synopsis.md`로 복사 (승인용 최종 버전).
기존 변형 파일은 보존한다.
