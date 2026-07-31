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
| clinical-pharmacologist | **opus** | PK 자료(반감기, 변동성), 대사 경로 정성, 약물상호작용 기전, 용량 근거, FIH 초기 용량 | 항상 |
| translational-scientist | **opus** | PD 바이오마커, PK-PD 모델링, 약물유전체학(PG), 대사체학, 수용체 점유율 | **조건부** (BE/FE 불참, 그 외 시험에 우선순위 차등 참여) |
| regulatory-expert | **opus** | MFDS/FDA/EMA 가이드라인, 승인현황, 약물 라벨(PG 섹션 포함), ICD-10 | 항상 |
| clinician | **opus** | 선정/제외 기준, 안전성 프로파일 조사, 임상 절차, 이상반응 관리 | **항상** |
| biostatistician | **opus** | 연구설계, sample size (Python), 무작위화, 통계분석 | 항상 |
| protocol-writer | opus | Synopsis + 자료 기반 Full Protocol 작성 | Phase 8 |
| icf-writer | opus | 계획서 기반 동의문서 작성 (PG/오믹스 별도 동의 포함) | Phase 10 (별도 지시) |
| qa-reviewer | opus | 다중 리뷰 취합, Critical/Major/Minor 분류, 수정 조율 (v3: actor-critic critic) | Phase 9 |

> **v3.0.0 모델 정책**: 모든 에이전트는 **opus(최신)**로 작동한다. 환각 위험이 자원자 안전에 직결되는 임상시험 문서 도메인에서 조사·작성·검토 전 단계에 최고 추론 모델을 사용한다.

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
- **모든 에이전트(조사·작성·검토 8종)는 opus(최신) 사용** (v3.0.0). 임상시험 문서의 환각·누락 위험이 자원자 안전·규제 적합성에 직결되므로 전 단계 최고 추론 모델 적용
- translational-scientist 참여 조건은 `.claude/skills/clinical-research/SKILL.md`의 "시험 유형별 오믹스/PD 우선순위" 표를 따른다 (BE/FE 불참, 그 외 참여)
- 모든 에이전트는 `general-purpose` 타입으로 호출 (커스텀 subagent_type 미지원)
- 에이전트 정의(`.claude/agents/*.md`)와 스킬은 서브 에이전트가 Read로 직접 로드
- 중간 산출물: `_workspace/` 디렉토리
- **사용자 검토 게이트 2개**: Phase 3 (자료 조사 후), Phase 7 (Synopsis 승인 — Hard Gate)
- 부분 재실행 시 하류 의존성 전파
- QA(Phase 9)는 **예산형 actor-critic 수렴 루프**(v3.0.0): protocol-writer(actor) ↔ qa-reviewer + `doc_lint` 채점(critic)이 `Critical=0 AND score≥90`까지 반복하되, `max_iterations`/score plateau 시 사람에게 에스컬레이션. synopsis·design_decisions는 불변 입력으로 락
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
| 2026-06-14 | **v3.0.0 — 최신 에이전트 엔지니어링 동향 반영 (loop·goal·zero-trust·guardrail)**: 3-모델 리뷰(Claude·Codex 0.139·Gemini 0.46) 후 3방향 동시 구현. (1) **Goal+Loop**: `trial_goal_spec.schema.json`(+example) 신설 — estimand·CI 경계·검정력·필수 ICH 섹션·보존연한을 기계 판독형 성공명세로 정의. `doc_lint.py`에 결정적 채점(`score_file`) 추가. Phase 9를 `max 1 revision` → **예산형 actor-critic 수렴 루프**(Critical=0 & score≥90 또는 budget·plateau 종료)로 재설계. (2) **Zero-trust**: `citation_verify.py`(PMID/NCT/setid/URL 독립 재조회·offline-graceful·`citation_audit.json`) + `source_snapshot.py`(외부 fetch SHA-256 provenance) 신설. IB least-privilege(섹션 제한 + `ib_manifest.json`). (3) **Guardrail**: advisory hook을 **3-tier**로 승격 — T0 차단(보존<15년, MRSD 초과 용량, ICF PII, 최종화 시 섹션 누락), T1 권고, T2 사람 게이트. `dose_safety_guard.py` + `/finalize` 커맨드(`doc_lint --strict` 실서류 적용). (4) **전 에이전트 opus(최신) 전환** + 8개 페르소나에 v3 역할(goal_spec·zero-trust·loop) 주입 | 사용자(임상약리 교수) 지시: harness를 넘어 loop·goal·zero-trust·guardrail 동향을 반영해 환자안전·규제·재현성을 아키텍처로 강제 |
| 2026-06-16 | **v4.1.0 — 4-모델 리뷰(정확성·적절성·정합성·시의성) 반영**: Opus·Codex·Gemini 교차 검토 후 P0~P2 일괄 수정. (P0) egress 하드코딩 `REGULATORY_PUBLIC` 제거 + `egress_gate` `confidential_context`(ib_manifest) 강제 floor → FIH/IB는 선언 무관 외부 차단. (P1) `ask_model.sh` stdin/`--prompt-file` 디스패치(ARG_MAX 회피); **보존기간 법령 근거화**(`RETENTION_LEGAL_BASIS`=「의약품등의 안전에 관한 규칙」 별표 4·KGCP 15년, protocol·ICF 공통, 템플릿 3년→15년); `/finalize icf` 대상 버그; judge_synth host 역할 명시; `/review` Step 4 수렴 루프 정정; model_profiles 현행화. (P2) egress 단어경계 매칭(오탐 제거), v4 제안서 배지, README 구조 보강, ICH E6(R3) Annex 2 Step 4·M12 Step 4 표기 정정 | 외부 모델 자기 CLI/모델명 오인은 실측 기각. 보존기간은 "해당국 법률 근거" 지시로 별표 4 인용·15년 일원화(goal_spec로 조정 가능) |
| 2026-06-16 | **v4.0.0 — Multi-LLM + Multi-Persona 하이브리드 (벤더 중립)**: 4-모델 자문(Opus·GPT/codex·Gemini·Grok). (1) **벤더 중립 라우팅**: `/llm-health`+`health_check.py`(nonce+산술 live probe로 로그인/키 실검증, 재실행·자동폴딩), `route_select.py`(health×capability_scores 결정적 배정; authoring=host, biostat=**Grok 1순위**, judge≠author; 호스트는 제안만), `ask_model.sh`(단일 게이트). 강점은 `references/llm/*.json` **편집 가능 데이터**(`as_of`). (2) **호스트 무관 egress 게이트**: `egress_gate.py` fail-closed, 분류(PUBLIC~SAFETY_CRITICAL)→허용 provider, **선언 floor + 마커는 상향만**, 벤더명 무하드코딩. 기밀 IB/안전핵심은 호스트 무관 차단. (3) **Phase 9 cross-vendor critic 패널**: `review_panel.py`(build_panel/synthesize **결정적 우선·다수결 ❌**/`_extract_json`/`collect_deterministic`/`fixplan→qa_fix_plan.md`) + `run_review_panel.sh`, `/review` Step 2.5 배선. 라이브 실증서 **Grok이 Gemini가 놓친 5 Critical 포착**, 결정적 도구가 벤더 오판(보존 "3년") 방어. **단일-LLM=v3 동등**(multi_llm=false) | 사용자 지시: 다양한 LLM 보유 환경별로 벤더 중립 조합을 사전 정의하고, 호스트가 최신 데이터×health로 최적 조합을 제안→사용자 선택. OMC cross-vendor 프리미티브(omc ask/team) 차용 + grok 어댑터 신설 |
| 2026-06-29 | **v4.2.0 — 버그픽스: agy 마이그레이션 + 명시 모델 핀**: Multi-LLM 어댑터 가용성·정확성 버그 3건(핀할 4개 모델 id 실측 검증 후 반영, 라우팅·capability 점수 불변). (1) **gemini CLI → agy(antigravity)**: Google 공식 전환(2026-06-18 gemini-cli 서비스 중단). `model_profiles` google `cli:"agy"`, `ask_model.sh` google 분기를 **stdin 입력 + brain 아티팩트 경로 파싱** 어댑터로 재작성, `health_check`에 **per-provider `probe_timeout`**(google=70, agy 시작 지연 대응) 추가. (2) **Anthropic Opus 명시 핀 + Fable 차단**: `ask_model.sh`가 `resolved_model`을 **dispatch 앞에서 읽어 `--model`로 전달** → "기록=실제 호출" 보장(기존엔 provenance에 opus 기록하나 CLI 기본 모델 호출 → Fable이면 거짓 기록+수출통제 위반). `availability_constraint`(Fable 수출통제→Opus 고정, 자동 latest 금지) 명문화. (3) **각 회사 최신 고성능 모델 날짜 스냅샷 핀**: claude-opus-4-8·gpt-5.5·**gemini-3.5-pro-002**(스냅샷)·grok-build, `resolved_model`을 바레 `--model` id로 정리, probe_cmd도 동일 핀. (4) v4.2 불변식 고정 테스트 6건(전체 152 passed) | 사용자(임상약리 교수) 지시: gemini→agy 전환, Anthropic은 Fable 불가→Opus, 각 회사 최신 고성능 모델을 (a)명시 핀(날짜 스냅샷) 방식으로. agy 인터페이스(stdin·`--model`·아티팩트)와 4개 모델 id 모두 실제 CLI 호출로 사전 검증 |
| 2026-07-31 | **v4.3.0 — P0 fail-closed release 게이트**: `/finalize`의 판정 주체를 커맨드 마크다운(에이전트 해석)에서 **결정적 실행 파일** `.claude/scripts/qa/finalize_run.py`로 이전. (1) **5개 차원**(`structure`/`citation`/`dose`/`advisory`/`approval`) + **상태 어휘 6개**(`PASS`/`FAIL`/`SKIPPED`/`FORMAT_ONLY`/`NOT_IMPLEMENTED`/`ERROR`) + **프로파일 2종**(`draft` 기본 / `submission`). (2) **종료코드가 유일한 판정**: `0` 통과 / `1` 판정했고 불합격 / `2` 판정 불가. **`ERROR`가 `FAIL`보다 우선** — 검사기가 깨진 상태에서 FAIL 목록이 완전하다고 주장할 수 없기 때문. (3) **증거 없으면 통과 주장 금지**: `<workspace>/verification/release_gate.json`(`schema: release_gate/v1`)을 임시파일+`os.replace`로 **원자적 기록**, 기록 실패는 exit 2. 판정 불가 실행이 이전 PASS 리포트를 남기지 않도록 최소 `UNDECIDABLE` 리포트로 교체. (4) **미구현 통제를 숨기지 않음**: 사람 승인 차원은 `NOT_IMPLEMENTED`로 매 실행 경고 노출 — 게이트 통과가 '제출 가능'을 뜻하지 않음을 출력이 직접 말한다. (5) **개발 중 fail-open 6건 차단**(전부 실측 재현 후 수정): 손상된 `mrsd.json`에서 FIH 9999mg 문서가 submission 통과 / `trial_type` 불명이 '비-FIH'로 붕괴해 같은 문서가 4가지 입력에서 통과 / 리포트 직렬화 오류가 exit 1(불합격)로 오인 + 손상 JSON 잔존 / 출력 인코딩 오류가 진짜 exit 2를 exit 1로 강등 / online 검증 불가 인용(DailyMed setid·URL)이 submission에서 `PASS` / 상태 어휘 밖 문자열이 비차단 집계. (6) 테스트 152→219 passed, 네트워크 I/O 0 | 사용자(임상약리 교수) 지시: `/finalize`가 "검사가 있는 척"이 되지 않도록 판정을 코드로 강제. Subagent-Driven Development 8-태스크로 구현하고, 구현자·리뷰어 보고를 **전부 재실행으로 검증**. 계획 자체도 파견 전 실측으로 검증해 결함 6건과 낡은 기대치 3건을 사전 정정 |
