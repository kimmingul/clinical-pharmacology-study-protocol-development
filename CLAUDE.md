# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

임상약리 임상시험의 문서 개발 프로젝트. 주요 산출물:
- **계획서 (Protocol)**: 임상시험 계획서 (Clinical Trial Protocol)
- **동의설명서/동의서 (ICF)**: 시험대상자 동의설명서 + 동의서 서명 페이지 (하나의 문서 세트)
- **개인정보 동의서**: 개인정보 수집·이용·제3자 제공 동의서 (PIPA 요건)

### 시험 유형별 입력 요건

| 시험 유형 | 필요 입력 | 근거 |
|----------|----------|------|
| FIH, SAD/MAD (신약) | IB 필수 | 신약이므로 공개 정보 없음. IB가 유일한 1차 자료 |
| DDI, BE, FE, QTc, ADME 등 | 약물명만으로 충분 | 이미 허가된 약물 대상. 기존 문헌·공개 DB에서 정보 수집 가능 |

## MCP Tools Available

이 프로젝트에서는 다음 MCP 도구를 활용할 수 있음:
- **Clinical Trials**: ClinicalTrials.gov API v2 — 유사 시험 검색, 프로토콜 설계 참고, 엔드포인트 분석
- **ICD-10 Codes**: ICD-10-CM/PCS 코드 조회 — 적응증 코딩, 선정/제외 기준 작성 시 활용
- **PubMed**: 문헌 검색 — 배경 근거, 용량 설정 근거, 안전성 정보 확인

## Language Conventions

- 문서 본문: 한국어 (Korean) 기본, 영문 병기 필요 시 괄호 표기
- 의학/약학 전문 용어: 대한의학회 의학용어집 기준, 영문 원어 병기
- 규제 용어: 식품의약품안전처(MFDS) 가이드라인 용어 사용
- 코드/설정 파일: 영어

## Regulatory References

문서 작성 시 준수해야 할 주요 규정:
- **ICH E6(R3)**: GCP 가이드라인 — Annex 1(비기술적 원칙)에 프로토콜 필수 요소 정의. R2와 구조가 다르므로 주의
- **ICH E8(R1)**: 임상시험의 일반적 고려사항
- **ICH E14**: QTc 시험 가이드라인 (QTc 시험 해당 시)
- **약사법 및 의약품등의 안전에 관한 규칙**: 제30조~34조 (임상시험 관련)
- **임상시험 관리기준(KGCP)**: 식약처 고시
- **개인정보 보호법(PIPA)**: 개인정보 수집·이용·제3자 제공 동의 요건
- **생명윤리 및 안전에 관한 법률**: 인체유래물 연구, 유전체 분석 시 적용
- **헬싱키 선언**: 윤리적 원칙

## 하네스: 임상시험 문서 개발

**목표:** 임상약리 임상시험의 배경 조사, Synopsis, 계획서, 동의설명서를 체계적으로 생성하고 검토한다.

**에이전트 팀 (7개):**

| 에이전트 | model | 역할 | 참여 |
|---------|-------|------|------|
| clinical-pharmacologist | sonnet | PK/PD 자료, 대사 경로, 약물상호작용, 용량 근거, FIH 초기 용량 | 항상 |
| regulatory-expert | sonnet | MFDS/FDA/EMA 가이드라인, 승인현황, 약물 라벨, ICD-10 | 항상 |
| clinician | sonnet | 선정/제외 기준, 안전성 프로파일 조사, 임상 절차, 이상반응 관리 | **항상 참여** |
| biostatistician | sonnet | 연구설계, sample size (Python), 무작위화, 통계분석 | 항상 |
| protocol-writer | opus | Synopsis + 자료 기반 Full Protocol 작성 | Phase 8 |
| icf-writer | opus | 계획서 기반 동의문서 작성 | Phase 10 (별도 지시) |
| qa-reviewer | opus | 다중 리뷰 취합, Critical/Major/Minor 분류, 수정 조율 | Phase 9 |

**Commands:**

| Command | Phase | 기능 |
|---------|-------|------|
| `/research` | 2-3 | 병렬 자료 수집 + 사용자 검토 게이트 |
| `/design` | 4-5 | 대화형 설계 협의 + 통계 설계 |
| `/synopsis` | 6 | Synopsis 생성 (인자로 변형 지정) |
| `/compare` | 6 | Synopsis 비교표 |
| `/protocol` | 8 | Full Protocol (Synopsis 승인 필수) |
| `/review` | 9 | 다중 에이전트 병렬 리뷰 |
| `/icf` | 10 | 동의문서 (별도 지시, Protocol 필수) |

**실행 규칙:**
- 임상시험 문서 작성/수정 요청 시 `trial-doc-orchestrator` 스킬 또는 개별 command로 처리
- 단순 질문(규제 용어, 개념 설명 등)은 에이전트 없이 직접 응답해도 무방
- 조사 에이전트(clinical-pharmacologist, regulatory-expert, clinician, biostatistician)는 sonnet, 작성/검토 에이전트(protocol-writer, icf-writer, qa-reviewer)는 opus 사용
- 모든 에이전트는 `general-purpose` 타입으로 호출 (커스텀 subagent_type 미지원)
- 에이전트 정의(`.claude/agents/*.md`)와 스킬은 서브 에이전트가 Read로 직접 로드
- 중간 산출물: `_workspace/` 디렉토리
- **사용자 검토 게이트 2개**: Phase 3 (자료 조사 후), Phase 7 (Synopsis 승인 — Hard Gate)
- 부분 재실행 시 하류 의존성 전파
- QA에서 Critical 발견 시 자동 1회 수정 후 재검토
- ICF는 메인 파이프라인에서 분리. `/icf` 별도 지시로 실행
- 모든 조사 자료에 reference 필수 (PMID, NCT, URL, 가이드라인 인용)
- Sample size 계산은 `.claude/scripts/sample_size/` Python 코드로 수행, 코드와 결과를 모두 산출물에 포함

**진화 로그:**

| 날짜 | 변경 내용 | 사유 |
|------|----------|------|
| 2026-04-05 | 초기 구성 — 4개 에이전트 파이프라인 | 프로젝트 시작 |
| 2026-04-06 | IB 입력, PIPA/생명윤리법, ICH Annex 1, 의존성 전파, QA 자동 수정, sonnet 전환 | 1차 리뷰 |
| 2026-04-06 | 상대 경로, Agent API, Phase 1 인터랙티브, 생명윤리법, 대용량 출력, icf-writer Part 4 | 2차 리뷰 |
| 2026-04-06 | general-purpose 타입, Skill → Read, 에이전트 정의를 프롬프트에서 로드 | E2E 테스트 |
| 2026-04-14 | **대규모 재구성**: 4→7 에이전트 (역할 기반), 10-Phase 워크플로우, Synopsis 단계 도입 (Hard Gate), 7개 commands, 다중 에이전트 병렬 리뷰, ICF 분리, MFDS 가이드라인 조사, Reference 의무화, Sample size Python 코드, FIH 초기 용량 산출 | 도메인 전문가 피드백 + Anthropic best practices |
| 2026-04-14 | **규제 가이드라인 라이브러리 구축**: `.claude/references/guidelines/`에 ICH(E6 R3, E8 R1, E14, M13A) + FDA + EMA + MFDS 가이드라인 + 국내 법령(약사법, KGCP, PIPA, 생명윤리법) + 시험 유형별 cross-agency 비교표 6건(BE, DDI, FIH, QTc, FE, PK 일반) 사전 수록 | 매번 웹 검색하지 않고 신뢰 가능한 사전 자료 우선 활용 |
| 2026-04-14 | **디렉토리 정리**: `resources/` (루트) → `.claude/scripts/`로 이동·개명 (실행 가능한 Python 코드의 본질 명확화); 중복된 MFDS 가이드라인은 `.claude/references/guidelines/mfds/`로 일원화 | 단일 진실 공급원 + 명명 일관성 (`scripts` vs `references`) |
