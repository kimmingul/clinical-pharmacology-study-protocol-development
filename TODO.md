# TODO — 중기 검토 및 개선 과제

하네스 정합성·타당성 리뷰(2026-04-14) 결과 중 **중기 검토**로 분류된 항목. 즉시 수정이 필요한 Critical/Major 항목은 모두 커밋 완료되었으며, 본 목록은 구조·정책 수준의 재설계가 필요한 사항이다.

---

## 1. Phase 4 협의 프로세스 간소화 (Major, UX)

### 현황
Phase 4는 사용자와 약 20개 의사결정을 순차 대화로 확정하도록 구성:
- Step 1: 선정/제외기준 (커스터마이징 가이드 A~F)
- Step 2: 연구설계
- Step 3: 세부 요소 8개 (연구설계 확정, PK 채혈, 절단 AUC, 1차·2차 평가변수, 유효성/PD, 안전성, 유전체/대사체, washout, 투여)

### 문제
실제 임상시험 컨설팅에서 수 주에 걸쳐 이뤄지는 결정을 단일 세션 대화로 처리 → **사용자 피로도 급증 + 결정 품질 저하 우려**.

### 검토 옵션
- **Option A**: 관련 항목을 묶어 일괄 제시 → 일괄 확정 (예: 평가변수 3개 묶음)
- **Option B**: 메인 에이전트가 research 보고서 기반 초안을 자동 제시, 사용자는 수정 항목만 논의 (opt-out 방식)
- **Option C**: 단계별 체크포인트 도입 (Step 1-2 → 소게이트 → Step 3)

### 결정 필요
어느 옵션을 채택할지 사용자·실무자 피드백 기반 결정. 현재 하네스는 Option A 방향으로 미세 조정되었으나 본격 개편 미적용.

---

## 2. translational-scientist의 BE/FE 선택적 참여 허용 (Major, 정책)

### 현황
BE/FE 시험에서 translational-scientist는 **완전 불참**으로 설정 (research/design/review 전 단계).

### 문제
일부 BE/FE 시험에서 PG 고려가 임상적으로 의미 있음:
- **NTI 약물** BE (warfarin, tacrolimus 등) — CYP 다형성 고려
- **한국인 CYP2C19 PM 비율 높은 약물** — PM 제외 여부가 규제 이슈
- FDA는 일부 BE 시험에 "CYP2C19 PM 제외" 라벨 권고

현재 정책으로는 이런 경우에도 TS 조사·검토가 불가능.

### 검토 방향
"BE/FE 기본 불참, 단 약물 특이 사유 시 사용자가 명시적으로 요청하면 참여"로 완화. 구체적 트리거 기준 정의 필요:
- NTI 약물 목록 매칭?
- 약물명 입력 시 MEDLINE/FDA PG Table 자동 조회?
- 사용자 수동 지정?

### 영향 범위
- `clinical-research/SKILL.md` 시험 유형별 우선순위 표
- `commands/research.md`, `commands/review.md` TS 참여 조건
- `trial-doc-orchestrator/SKILL.md` Phase 2, Phase 9

---

## 3. biostatistician / clinician 모델 재검토 (Minor, 성능)

### 현황
조사 에이전트는 모두 sonnet 사용.

### 검토 대상
- **biostatistician** (sonnet): 연구설계 옵션 제시 + Python 코드 실행 + 통계 분석 설계. 복잡도 높음 → opus 고려 가능
- **clinician** (sonnet): 안전성 전담 + 개별 reference 5개 파일(AE_profile, SAE_cases, class_effect, safety_monitoring_rationale, stopping_rules_rationale) 생성. 부담 높음

### 결정 기준
실제 운영 중 결과 품질 모니터링 후 결정. 현재까지 명백한 품질 저하 사례 관측 없음.

---

## 4. `regulatory-review` 스킬명 변경 검토 (Minor, 네이밍)

### 현황
스킬 이름 `regulatory-review`지만 실제로는 임상약리/통계/임상의학/중개의학 리뷰까지 모두 포함.

### 검토 옵션
- `multi-agent-review`
- `protocol-review`
- `document-review`

### 영향 범위
- 디렉토리명 변경 (`.claude/skills/regulatory-review/` → 신규명)
- 이를 참조하는 모든 파일 경로 갱신:
  - `commands/review.md`
  - `trial-doc-orchestrator/SKILL.md`
  - 5개 조사 에이전트 (`.claude/agents/*.md`)
  - CLAUDE.md, README.md
- 약 10-15개 파일 변경 예상

### 우선순위 낮음 사유
동작에는 영향 없음. 주석/용어 일치 수준의 개선.

---

## 5. ICH E6(R3) Annex 1 "13개 필수 항목" 체크리스트 원문 검증 (Major, 규제)

### 현황
`.claude/skills/regulatory-review/SKILL.md` Line 55-69의 13개 항목은 에이전트가 외우는 기준이나, 실제 ICH E6(R3) Annex 1 Appendix B의 항목 목록과 1:1 대조 검증 미완.

### 근거
`.claude/references/guidelines/needs_user_input.md`에 "ICH E6(R3) Step 4 최종본 Appendix B 전체 조항 원문 확인 필요"가 명시되어 있어, 현재 체크리스트는 추정치 가능성.

### 해결 경로
- 사용자가 ICH E6(R3) PDF 제공 → 원문 대조
- 또는 ICH 공식 다운로드 URL(`.claude/references/guidelines/needs_user_input.md` 하단 링크)에서 수동 다운로드

### 영향 범위
체크리스트 자체가 틀리지는 않을 가능성이 높으나, **규제 제출용 문서의 QA 기준**이므로 원문 검증 없이는 "Critical"로 지적받을 위험.

---

## 완료된 항목 (본 리뷰 커밋에 반영됨)

✅ **Critical (3건)** — `1306f8e` 커밋
- C1: regulatory-review/SKILL.md 전면 개정 (TS 리뷰 통합)
- C2: protocol-writer.md Phase 1 용어 + 4→5명 갱신
- C3: ICF 경로 수정 (trial_info → design_decisions)

✅ **Major (5건)** — `6409cb2` 커밋
- M1: biostatistician parallel_binary.py 추가
- M2: qa-reviewer description 조건부 5명 표현
- M3: synopsis.md 구조 확장 (PD 평가, 유전체/대사체 섹션)
- M4: Phase 1 입력에서 "유전체/인체유래물" 제거
- M5: compare.md 비교 항목 확장

✅ **Minor (3건)** — 현 커밋
- m3: clinical-research 시험 유형별 특화 조사 표 경계 명확화
- m4: /synopsis 인자-스크립트 매핑 표 명시화
- m5: settings.local.json 불필요 권한 정리
