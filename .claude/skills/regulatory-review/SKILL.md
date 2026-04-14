---
name: regulatory-review
description: "임상시험 문서의 다중 에이전트 리뷰를 지원하는 스킬. 4-5명의 전문가(clinical-pharmacologist, translational-scientist(조건부), clinician, regulatory-expert, biostatistician)가 병렬로 계획서를 검토하고, qa-reviewer가 취합하여 통합 보고서를 작성한다. 문서 검토, 문서 리뷰, QA, 품질 검토, 일관성 검토, 규제 검토, 계획서 리뷰 요청 시 사용."
---

# Regulatory Review — 다중 에이전트 리뷰

4-5명의 전문가가 병렬로 계획서를 검토하고, qa-reviewer가 이를 취합하여 통합 리뷰 보고서를 작성한다. **translational-scientist는 BE/FE 외 시험에서만 참여**한다 (PD/PG/오믹스가 시험 목적과 관련 있는 경우).

## 개별 리뷰어 절차

> 각 리뷰어 에이전트는 이 섹션을 따른다. 자신의 검토 초점에 해당하는 항목만 검토한다.

### Step 1: 문서 로드

다음 파일을 Read로 읽는다:
- `_workspace/03_protocol_draft.md` (리뷰 대상)
- `_workspace/01_research_report.md` (근거 자료 대조)
- `_workspace/02_synopsis.md` (설계 결정 대조)

### Step 2: 초점 영역 검토

#### clinical-pharmacologist 검토 항목

| 항목 | 검토 내용 |
|------|----------|
| PK 설계 | 채혈 시점이 예상 반감기를 고려했는지, 시점 수 적절성 |
| 약물상호작용 평가 | DDI 시험의 상호작용 메커니즘 반영, CYP/수송체 고려 |
| 용량 근거 | 비임상/임상 데이터 기반 용량 설정 타당성, 출처 인용 |
| Washout 기간 | 5×t½ 이상인지, 교차 설계에서의 잔류 효과 |
| 용량 증량 | 증량 비율, 센티넬 도징, SRC 기준 (FIH 시) |

#### clinician 검토 항목 (항상 참여)

| 항목 | 검토 내용 |
|------|----------|
| 선정/제외 기준 | 임상적 타당성, 안전성 관점의 제외 기준 |
| 안전성 모니터링 | 활력징후, ECG, 실험실 검사 빈도 적절성 |
| 이상반응 관리 | 이상반응별 대처 절차, 중증도 평가 기준 |
| 중지 기준 | 개인 수준 + 시험 수준 stopping rules |
| 동의서 내용 | 위험 정보가 충분히 기술되었는지 |

#### translational-scientist 검토 항목 (BE/FE 외 시험)

| 항목 | 검토 내용 |
|------|----------|
| PD 평가 섹션 | 바이오마커 선정 근거(작용 기전 기반), 측정 시점·분석 방법 적절성, 검증 상태 |
| PK-PD 모델링 | 모델 선정(Emax, sigmoid Emax, indirect response 등)의 과학적 타당성, 파라미터 근거 |
| 약물유전체(PG) 분석 | 대상 유전자(CYP·표적)의 시험약 관련성, 한국인 빈도 반영, 표현형별 해석 기준 |
| 대사체 분석 | MIST 준수(ADME), 내인성 바이오마커 측정법(DDI), 시료·시점 적절성 |
| **계획서-ICF 정합성** | 계획서에 명시된 PG/대사체 분석 항목이 ICF Part 4에 빠짐없이 반영되었는가 (생명윤리법 준수) |

#### regulatory-expert 검토 항목

| 항목 | 검토 내용 |
|------|----------|
| ICH E6(R3) Annex 1 | 아래 체크리스트의 13개 필수 항목 충족 여부 |
| MFDS 요건 | KGCP 준수 명시, 국내 IRB 절차, 보험/보상 규정 |
| PIPA | 개인정보 수집·이용·제공 동의 6개 항목 |
| 생명윤리법 | 인체유래물 연구 해당 시 5개 항목 |
| 규제 용어 | 식약처 가이드라인 용어 사용, 영문 병기 |

**ICH E6(R3) Appendix B 체크리스트 (16개 공식 섹션):**

> **원문 근거**: `.claude/references/guidelines/ich/e6_r3_full/07_appendix_b_protocol.md` (ICH E6(R3) 2025-01-06 최종본 Appendix B 전문)

| # | 섹션 | 필수 내용 |
|---|------|----------|
| B.1 | General Information | 프로토콜 제목, 고유 식별 번호, 날짜, 개정 번호/날짜, 의뢰자 이름·주소, 서명 권한자 |
| B.2 | Background Information | 시험약 이름·설명, 비임상/임상 주요 소견, 알려진·잠재 위험과 이익, 투여 경로·용량·치료 기간의 정당성, GCP 준수 선언, 대상 집단 설명, 관련 문헌 참조 |
| B.3 | Trial Objectives and Purpose | 과학적 목적·목적의 명확 기술, Estimand 정보 (정의된 경우, ICH E9(R1) 참조) |
| B.4 | Trial Design | 1차/2차 평가변수, 시험 유형·설계, 편향 최소화 조치(무작위화·맹검), 시험약 설명·투여법, 스케줄, 중지 규칙·용량 조정, 대상자 참여 기간·순서, 설명책임 절차, 무작위화 코드 유지·해제 절차, 원본 자료 식별 |
| B.5 | Selection of Participants | 선정 기준, 제외 기준 |
| B.6 | Discontinuation of Trial Intervention and Participant Withdrawal from Trial | 시험 중단·탈락 기준, 추적관찰 절차, 동의 철회 후 자료 처리 |
| B.7 | Treatment and Interventions for Participants | 허용·금지 병용요법·약물, 환자 순응도 모니터링 절차 |
| B.8 | **Assessment of Efficacy** | 유효성 평가 변수 명세, 평가 방법·일정·기록 방법. ★ **ICH E6(R3) 공식 섹션명이 "Assessment of Efficacy"**임 — Phase 1 시험에서도 PD/약효가 1차 평가변수인 경우(DDI의 GMR, BE의 동등성, FE의 식이 영향, QTc의 ddQTcF) "유효성 평가" 표현이 공식 용어로 사용됨. 시험 목적이 PK·안전성·내약성 확립인 FIH/MAD/ADME/Special Pop는 "약동학/약력학 평가"로 기술 (Phase 1 용어 가이드는 `.claude/skills/protocol-drafting/SKILL.md` 참조) |
| B.9 | Assessment of Safety | 안전성 평가 변수, AE/SAE 기록·보고 방법, 안전성 추적관찰 계획 |
| B.10 | Statistical Considerations | 통계 분석 방법·중간 분석 계획, sample size 산출 근거, 유의수준, 분석 집단 정의, 결측치 처리 |
| B.11 | Direct Access to Source Records | 의뢰자·규제 당국의 원본 자료 접근 권한, 모니터링·감사·IRB 심의·규제 검토 허용 |
| B.12 | Quality Control and Quality Assurance | QC·QA 절차, 모니터링 계획 |
| B.13 | Ethics | 윤리적 고려사항 (Declaration of Helsinki, IRB/IEC 승인, 참여자 보호) |
| B.14 | Data Handling and Record Keeping | 자료 관리·기록 보존 방법, 전자 시스템 사용, 감사 추적 |
| B.15 | Financing and Insurance | 재정 및 보험 — 별도 문서로 다루어질 수 있음 |
| B.16 | Publication Policy | 결과 공표 정책 — 별도 문서로 다루어질 수 있음 |

**PIPA 체크리스트:**

| # | 필수 항목 |
|---|----------|
| 1 | 개인정보 수집 항목 명시 |
| 2 | 수집·이용 목적 명시 |
| 3 | 제3자 제공 대상 및 목적 |
| 4 | 보유 기간 |
| 5 | 동의 거부 권리 및 불이익 |
| 6 | 별도 동의서 존재 |

**생명윤리법 체크리스트 (해당 시):**

| # | 필수 항목 |
|---|----------|
| 1 | 인체유래물 종류 및 수집 목적 |
| 2 | 보관 기간 및 장소 |
| 3 | 폐기 절차 |
| 4 | 2차 활용 별도 동의 |
| 5 | 동의 철회 시 검체 폐기 |

#### biostatistician 검토 항목

| 항목 | 검토 내용 |
|------|----------|
| 통계 섹션 완결성 | 분석 집단 정의, 1차/2차 분석 방법, 중간 분석 계획 |
| Sample size 정당성 | 가정 파라미터 타당성, 계산 결과 재현 가능성 |
| 무작위화 | 배정 방법, 블록 크기, 층화 변수 |
| 분석 방법 | 1차 변수 분석 모델, 동등성/우월성 기준 |
| 결측치 처리 | 결측 처리 방법, 민감도 분석 |

### Step 3: 개별 리뷰 산출물 작성

각 리뷰어는 아래 형식으로 `_workspace/review/review_{agent_name}.md`에 Write한다:

```markdown
# {에이전트명} 리뷰

## 검토 요약
- 검토 일시: {날짜}
- 대상 문서: {문서명}
- 검토 초점: {초점 영역}

## 발견 사항

### [심각도-번호] {제목}
- **심각도**: Critical / Major / Minor
- **위치**: 섹션 {번호}, 페이지/줄
- **내용**: {구체적 문제}
- **근거**: {규정/가이드라인/과학적 근거}
- **권고**: {수정 방향}

(반복)

## 종합 의견
```

## QA 취합 절차

> qa-reviewer 에이전트가 이 섹션을 따른다.

### Step 1: 개별 리뷰 로드

참여한 모든 개별 리뷰 파일을 Read한다:
- `_workspace/review/review_clinical_pharmacologist.md`
- `_workspace/review/review_regulatory_expert.md`
- `_workspace/review/review_biostatistician.md`
- `_workspace/review/review_clinician.md`
- `_workspace/review/review_translational_scientist.md` (존재하면 — BE/FE 외 시험)
- `_workspace/03_protocol_draft.md` (원문 대조)

### Step 2: 분류 및 우선순위 지정

4-5개 리뷰의 발견 사항을 통합하여 심각도별로 재분류한다:

| 등급 | 정의 | 처리 |
|------|------|------|
| **Critical** | 규제 요건 미충족, 대상자 안전 위험, 과학적 결함 | 자동 수정 후 재리뷰 |
| **Major** | 설계 적절성 문제, 주요 정보 누락 | 사용자에게 수정 권고 |
| **Minor** | 표현 개선, 일관성 사소한 불일치 | 수정 제안 (선택적) |

### Step 3: 상충 의견 해결

리뷰어 간 상충 의견이 있으면:
1. 양쪽 근거를 비교한다
2. 명확히 한쪽이 우세하면 해당 근거를 채택한다
3. 판단이 어려우면 **양쪽 의견을 모두 기재**하고 사용자에게 판단을 요청한다

### Step 4: 문서 간 일관성 검토

Protocol과 Synopsis 간 일관성을 확인한다:

| 비교 항목 | Synopsis | Protocol | 일치 여부 |
|----------|----------|----------|----------|
| 시험 설계 | | | |
| 1차 평가변수 | | | |
| 대상자 수 | | | |
| 통계 분석 방법 | | | |
| 용량/투여법 | | | |
| 선정/제외 기준 | | | |

### Step 5: 통합 보고서 작성

`_workspace/review/qa_review_report.md`에 아래 형식으로 Write한다:

```markdown
# QA 통합 리뷰 보고서

## 검토 요약
- 검토 일시: {날짜}
- 대상 문서: Protocol v{X}
- 리뷰어: clinical-pharmacologist, regulatory-expert, biostatistician, clinician{, translational-scientist (BE/FE 외)}
- **Critical: N건 | Major: N건 | Minor: N건**

## Critical 사항
### [C-1] {제목}
- **발견자**: {에이전트명}
- **위치**: 섹션 {번호}
- **내용**: {구체적 문제}
- **근거**: {규정/가이드라인 참조}
- **권고**: {수정 방향}

## Major 사항
### [M-1] {제목}
(동일 형식)

## Minor 사항
### [m-1] {제목}
(동일 형식)

## 상충 의견 (해당 시)
### {주제}
- **{에이전트A}**: {의견 + 근거}
- **{에이전트B}**: {의견 + 근거}
- **QA 판단**: {채택 의견 또는 "사용자 판단 요청"}

## Synopsis-Protocol 일관성 점검표
(교차 비교 매트릭스)

## 규제 체크리스트 결과
### ICH E6(R3) Annex 1
(13개 항목 충족 여부)
### MFDS 요건
### PIPA
### 생명윤리법 (해당 시)

## 종합 의견
```

## Gotchas

- **리뷰어 범위 침범**: 각 리뷰어는 자기 초점 영역만 검토해야 한다. biostatistician이 규제 용어를, regulatory-expert가 통계 방법론을 검토하면 전문성 밖의 부정확한 피드백이 된다
- **Synopsis-Protocol 불일치**: Synopsis에서 결정된 사항(설계, 대상자 수, 분석 방법)이 Protocol에서 변경되지 않았는지 반드시 확인
- **Critical 남발**: Critical은 "규제 불합격 또는 대상자 안전 위험"에만 사용. 표현 개선이나 사소한 누락은 Minor
- **상충 의견 무시 금지**: 리뷰어 간 의견이 다르면 반드시 양쪽을 기재하고 근거를 비교해야 한다
- **translational-scientist 리뷰 누락 (BE/FE 외 시험)**: BE/FE 외 시험에서 TS가 빠지면 PD 평가·PG/오믹스 분석 섹션과 ICF Part 4 정합성을 검증할 리뷰어가 없어진다. 시험 유형을 확인하여 호출
- **translational-scientist 리뷰 요구 금지 (BE/FE)**: BE/FE에서는 TS가 불참이다. 누락으로 보고하지 말 것
- **ICH E6 R3 vs R2 혼동**: R3는 Annex 1/Annex 2 구조. R2의 섹션 번호와 다르므로 주의
- **Phase 1 용어 정책**: "유효성 평가" 일률 금지 아님. 시험 목적별 차등 적용 — PD/약효 측정이 1차 평가변수인 시험(DDI의 GMR, BE의 동등성, FE의 식이 영향, QTc의 ddQTcF)은 "유효성 평가" 표현 사용 가능. FIH/MAD/ADME/Special Pop은 "약동학/약력학 평가" 유지. 상세는 `.claude/skills/protocol-drafting/SKILL.md`의 "Phase 1 용어 가이드" 표

## References

규제 체크리스트 상세 내용 및 시험 유형별 리뷰 포인트는 `references/` 디렉토리를 참조한다.
