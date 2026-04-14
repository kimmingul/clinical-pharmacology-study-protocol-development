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

## 외부 데이터 소스

### MCP Tools
- **Clinical Trials**: ClinicalTrials.gov API v2 — 유사 시험 검색, 프로토콜 설계 참고, 엔드포인트 분석
- **ICD-10 Codes**: ICD-10-CM/PCS 코드 조회 — 적응증 코딩, 선정/제외 기준 작성 시 활용
- **PubMed**: 문헌 검색 — 배경 근거, 용량 설정 근거, 안전성 정보 확인

### Web API (WebFetch 기반)
MCP 서버 없이 WebFetch로 직접 공개 API를 호출. 쿼리 레시피는 `.claude/references/api_reference/` 참조:

**규제·라벨 (regulatory-expert 담당)**
- **DailyMed** (`dailymed.nlm.nih.gov/dailymed/services/v2/`): 미국 FDA 승인 약물 SPL 라벨 전문 — 약물 라벨 1차 수집
- **openFDA** (`api.fda.gov/drug/`): 허가 정보(NDA 번호·승인일), NDC, FAERS 이상반응, 보조 라벨
- **MFDS 의약품안전나라** (`nedrug.mfds.go.kr/searchClinic` + `/ext/CCAAK02F010/*`): 국내 임상시험 승인현황 리스트(HTML) + 시험별 상세 본문(Nexacro SOAP XML). 인증 불필요. 검색은 최대 3년 구간, 상세는 `clinicExamSeq`+`clinicExamNo`로 POST 호출. 레시피: `.claude/references/api_reference/mfds.md`

**약물유전체 (translational-scientist 담당)**
- **PharmGKB / ClinPGx** (`api.pharmgkb.org/v1/`): 약물-유전자 임상 annotation, 라벨 PGx, 변이 annotation — 무인증, 2 req/sec, CC BY-SA 4.0
- **CPIC** (`api.cpicpgx.org/v1/`): 표현형별 용량 조절 권고, 권고 등급(A/B/C/D), Diplotype→Phenotype 매핑 — 무인증, CC0 Public Domain, PostgREST

## Language Conventions

- 문서 본문: 한국어 (Korean) 기본, 영문 병기 필요 시 괄호 표기
- 의학/약학 전문 용어: 대한의학회 의학용어집 기준, 영문 원어 병기
- 규제 용어: 식품의약품안전처(MFDS) 가이드라인 용어 사용
- 코드/설정 파일: 영어

## Regulatory References

문서 작성 시 준수해야 할 주요 규정:
- **ICH E6(R3)**: GCP 가이드라인 — 2025-01-06 Step 4 최종본 전문이 `.claude/references/guidelines/ich/e6_r3_full/`에 MD로 수록됨. **Appendix B**(`07_appendix_b_protocol.md`)가 프로토콜 16개 필수 섹션(B.1-B.16)을 공식 정의. R2와 구조가 다르므로 주의
- **ICH E8(R1)**: 임상시험의 일반적 고려사항
- **ICH E14**: QTc 시험 가이드라인 (QTc 시험 해당 시)
- **약사법 및 의약품등의 안전에 관한 규칙**: 제30조~34조 (임상시험 관련)
- **임상시험 관리기준(KGCP)**: 식약처 고시
- **개인정보 보호법(PIPA)**: 개인정보 수집·이용·제3자 제공 동의 요건
- **생명윤리 및 안전에 관한 법률**: 인체유래물 연구, 약물유전체(PG) 분석, 대사체 분석, 잔여 검체 보관 시 적용. design 단계에서 PG/대사체 분석 계획이 결정되면 ICF Part 4(선택 동의)에 반드시 반영하고, IRB 외에 기관생명윤리위원회 추가 심의 필요 여부 확인
- **헬싱키 선언**: 윤리적 원칙

## 하네스: 임상시험 문서 개발

**목표:** 임상약리 임상시험의 배경 조사, Synopsis, 계획서, 동의설명서를 체계적으로 생성하고 검토한다.

**에이전트 팀 (8개):**

| 에이전트 | model | 역할 | 참여 |
|---------|-------|------|------|
| clinical-pharmacologist | sonnet | PK 자료(반감기, 변동성), 대사 경로 정성, 약물상호작용 기전, 용량 근거, FIH 초기 용량 | 항상 |
| translational-scientist | sonnet | PD 바이오마커, PK-PD 모델링, 약물유전체학(PG), 대사체학, 수용체 점유율 | **조건부** (BE/FE 불참, 그 외 시험에 우선순위 차등 참여) |
| regulatory-expert | sonnet | MFDS/FDA/EMA 가이드라인, 승인현황, 약물 라벨(PG 섹션 포함), ICD-10 | 항상 |
| clinician | sonnet | 선정/제외 기준, 안전성 프로파일 조사, 임상 절차, 이상반응 관리 | **항상** |
| biostatistician | sonnet | 연구설계, sample size (Python), 무작위화, 통계분석 | 항상 |
| protocol-writer | opus | Synopsis + 자료 기반 Full Protocol 작성 | Phase 8 |
| icf-writer | opus | 계획서 기반 동의문서 작성 (PG/오믹스 별도 동의 포함) | Phase 10 (별도 지시) |
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
- 조사 에이전트(clinical-pharmacologist, translational-scientist, regulatory-expert, clinician, biostatistician)는 sonnet, 작성/검토 에이전트(protocol-writer, icf-writer, qa-reviewer)는 opus 사용
- translational-scientist 참여 조건은 `.claude/skills/clinical-research/SKILL.md`의 "시험 유형별 오믹스/PD 우선순위" 표를 따른다 (BE/FE 불참, 그 외 참여)
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
| 2026-04-14 | **translational-scientist 신규 에이전트**: PD 바이오마커, PK-PD 모델링, 약물유전체학, 대사체학, 수용체 점유율 자료 수집 전담. clinical-pharmacologist는 PK 측면에 집중하도록 영역 재정의 | Phase 4 PD/유효성 평가 협의에 필요한 사전 자료 수집 빈틈 보완. PK ↔ PD 영역 명확 분리 |
| 2026-04-14 | **Phase 4에 유전체/대사체 분석 계획 협의 추가** + **ICF Part 4(선택 동의) PG/오믹스 섹션 강화** + **regulatory-expert 라벨 PG 섹션 추출 책임 추가** | 자료수집·설계협의·동의문서 전 단계에 PG/오믹스가 일관되게 흐르도록 구성. 생명윤리법(인체유래물 연구) 준수 보장 |
| 2026-04-14 | **Web API 5종 통합**: DailyMed + openFDA + MFDS 의약품안전나라(searchClinic 리버스엔지니어링) + PharmGKB/ClinPGx + CPIC. `.claude/references/api_reference/` 하위 5개 레시피 파일, WebFetch 기반 즉시 사용 가능 | MCP 서버 구축 없이 공개 API·크롤링 가능 페이지로 외부 데이터 소스 확장 |
| 2026-04-14 | **ICH E6(R3) 원문 전문 MD 수록 + 체크리스트 재구성**: `ich/e6_r3_full/` 10개 파일, regulatory-review/SKILL.md의 13개 추정 체크리스트를 **Appendix B 공식 16개 섹션(B.1~B.16)**으로 교체. B.8 "Assessment of Efficacy" 공식 명칭 확인으로 Phase 1 용량 정책 정당성 확보 | 사용자가 ICH PDF 제공 → `pdftotext`로 원문 추출 → QA 기준의 근본 신뢰성 확보 |
| 2026-04-14 | **MFDS 크롤링 전면 재검증 + Nexacro SOAP 상세 크롤링 신설**: 기존 레시피의 searchType 매핑 오류(ST1/2/3/4 전체 혼선) + hidden 날짜 파라미터(`approvalStart`/`approvalEnd`) 누락으로 모든 검색이 0건 반환되던 문제 해결. 상세 페이지는 Nexacro SPA이나 `/ext/CCAAK02F010/*` SOAP endpoint 4종(clinicExamPlanReport PLAN/RESULT, clinicExamOpenChk, clinicExamOpenItem)을 HTTP POST + 표준 XML body로 직접 호출하여 **선정·제외 기준·시험약·결과 본문까지 XML dataset 수신 실증**. 검색 리스트 → 상세 자동 follow 전략 도입 (N×4 호출 제한 N≤30) | 사용자 지적으로 실사용 불가 상태가 드러남 + 상세 본문 자동 수집 요구 → 2단계 크롤링(리스트 + Nexacro SOAP) 완성. 헤드리스 브라우저·유료 API 키 불필요 |
| 2026-04-14 | **v2 DDI E2E 실행 후 하네스 강화**: (1) protocol-writer/regulatory-expert에 **규제 상수 표** 추가 — KGCP 기록 보존 **15년** (3년 오기 방지), SAE 7/15일, 종료 90일, 90% CI 80–125% 기본값. (2) clinician에 **약물 계열별 안전성 체크리스트** 추가 — Thienopyridine TTP 4종 세트(혈소판·LDH 정기·Haptoglobin·말초혈구도말). (3) biostatistician에 **SAS PROC MIXED 표준 문법 3종** + **Co-primary IUT 판정 로직**. (4) protocol-template §10.1에 **AUC 시간 범위 선택 표** (AUC₀₋∞/AUC₀₋ₜ/AUC₀₋₇₂ₕ/AUC₀₋τ 가이드라인 정합성). (5) `/synopsis`에 design_decisions.md **강제 반영 Step A/B/C**. (6) `/research`에 **TS 참여 매트릭스 + 자가 검증 절차**. A군 Web API 결함(MFDS JS 렌더링, PharmGKB HTTP 400)은 `TODO.md §0`에 이관 | E2E v2 DDI(`e2e/v2_2026_04_14_DDI/`) 5명 리뷰 중 Major 8건 분석 → 재발 방지용 상수·체크리스트·검증 단계를 에이전트·템플릿·커맨드에 주입 |
| 2026-04-14 | **양방향 DDI 지원 신설**: (1) clinical-pharmacologist에 "DDI 방향성 평가 매트릭스" (기질/저해/유도 역할 표 + 양방향 가능성 체크리스트). (2) `/design` Step 2에 방향성 결정 절차. (3) `/synopsis` §3·§6.1에 role·방향성·co-primary 표기. (4) **Williams 6×3 crossover 신설** (3 treatments: A 단독, B 단독, A+B, 6 sequences=3!, carry-over 균형) + `.claude/scripts/sample_size/williams_6x3_ddi.py` (IUT 기반 양방향 n 계산). (5) biostatistician에 양방향 분석 로직 (PROC MIXED ESTIMATE 2개, IUT 원리 — α 조정 불필요) | 두 약물 모두 CYP 기질일 때 한쪽 방향만 평가하는 결함 방지. FDA DDI(2020) + ICH M12(2024) 권고 정합 |
| 2026-04-15 | **Claude Code plugin 배포 구조 v2.0.0**: `.claude/` 기반 개발 하네스는 그대로 유지하고, 별도 `plugin/clinical-pharmacology-study-protocol-development/` 하위에 배포용 복사본 신설(경로 `.claude/` → `${CLAUDE_PLUGIN_ROOT}/` 치환, 109곳). 루트 `.claude-plugin/marketplace.json` 신설(name=`clinical-pharmacology-marketplace`, owner·metadata·plugins[1] 구조, 단일 plugin 배포). `plugin.json`·marketplace.json 버전 **2.0.0**. 루트 `sync_plugin.sh`로 `.claude/` → `plugin/<이름>/` rsync 자동 동기화 + 경로 치환. MIT 라이선스 명시 | Claude Code marketplace/로컬 플러그인 배포 지원. 개발 continuation과 배포 아티팩트 동시 보존 |
