# TODO — 중기 검토 및 개선 과제

하네스 정합성·타당성 리뷰(2026-04-14) 결과 중 **중기 검토**로 분류된 항목. 즉시 수정이 필요한 Critical/Major 항목은 모두 커밋 완료되었으며, 본 목록은 구조·정책 수준의 재설계가 필요한 사항이다.

---

## 0. E2E v2 DDI 실행 중 발견된 Web API 결함 (2026-04-14, 미해결)

v2 DDI E2E(Clopidogrel+Omeprazole) 실행 중 사용자 지시로 수정 보류된 항목. 하네스 파이프라인에는 영향이 제한적이나 레시피 개정이 필요.

### 0-1. ~~MFDS `searchClinic` WebFetch 파싱 실패~~ ✅ **해결 완료 (2026-04-14 재조사)**

- **최종 진단**: JavaScript 동적 렌더링 추정은 **오진**. 실제는 **순수 서버 렌더링 HTML**이며 엔드포인트 정상 작동.
- **진짜 원인 2가지** (기존 레시피 결함):
  1. `searchType` 코드 매핑 오류 — `ST1=제품명` 등으로 잘못 기재됨. 실제는 `ST1=의뢰자, ST2=제품명, ST3=시험제목, ST4=실시기관` (HTML `<select><option>` 실측)
  2. hidden 파라미터 `approvalStart`/`approvalEnd` 누락 — UI date picker(`approvalDtStart`/`End`)와 **별도로** DB 쿼리에 사용되는 hidden input이 존재. 둘 다 전송해야 함
- **검증 결과** (실측, 3년 범위):
  - ST2 제품명 "클로피도그렐" → 7건 ✓
  - ST3 시험제목 "클로피도그렐" → 8건 ✓
  - ST1 의뢰자 "한미약품" → 17건 (페이지당 10건, 페이지네이션 확인)
  - ST4 실시기관 "서울대학교병원" → 1,142건 ✓
- **적용된 수정**:
  1. `.claude/references/api_reference/mfds.md` 전면 재작성 (올바른 매핑 + hidden 파라미터 + 3년 제한 반복 검색 전략)
  2. `.claude/agents/regulatory-expert.md` Step D 업데이트
  3. E2E v2 DDI 결과(0건)는 당시 잘못된 파라미터로 인한 것. 재실행 시 정확한 결과 수신 가능
- **남은 이슈**: 
  - 장기 조사 시 3년 구간 반복 호출은 여전히 WebFetch 호출 수 증가 → data.go.kr OpenAPI 전환(§5)이 여전히 중기 가치 있음
  - UI 개편 대응은 §5 또는 HTML 구조 변경 시점에 재검증
  - **상세 페이지(Nexacro SPA) 본문 크롤링 미지원** — 0-3 항목 참조

### 0-3. ~~MFDS 상세 페이지 본문 크롤링~~ ✅ **해결 완료 (2026-04-14 추가 분석)**

- **최종 진단**: Nexacro SPA이지만 SOAP transaction endpoint를 **HTTP POST로 직접 호출하여 XML 응답 수신 가능**. 헤드리스 브라우저 불필요.
- **검증된 호출 형식**:
  - Method: POST
  - Base: `https://nedrug.mfds.go.kr/`
  - Content-Type: `text/xml; charset=UTF-8`
  - Body: `<Root xmlns="http://www.nexacroplatform.com/platform/dataset"><Parameters>...</Parameters></Root>`
  - 응답: 동일 namespace의 XML, `<Dataset>` 노드들에 데이터
  - 인증 불필요
- **검증 결과 (2026-04-14, 시험 clinicExamSeq=202600092, clinicExamNo=103126)**:
  - `clinicExamPlanReport` (Tab 1) → 32 KB, 8개 dataset (선정·제외 기준, 시험약, 임상연구, 자료, 위변조, 메타) 정상 수신 ✓
  - `clinicExamPlanReport` + `mode=RESULT_INFO` (Tab 2) → 23 KB, 결과 본문 정상 수신 ✓
  - `clinicExamOpenChk` → 662 B, 공개 여부 ✓
  - `clinicExamOpenItem` → 2.2 KB, 공개 항목 메타 ✓
- **적용**:
  1. `.claude/references/api_reference/mfds.md` §"상세 페이지 크롤링 — Nexacro SOAP 직접 호출" 신설 — 완전한 curl + Python 파싱 예시
  2. `.claude/agents/regulatory-expert.md` Step D-8/D-9 갱신 — 상세 본문까지 자동 수집 정책
- **운영 주의**:
  - 검색 N건 × 최대 4 endpoint = SOAP 호출량. N≤30 권장. 초과 시 `data.go.kr` OpenAPI(§5) 사용
  - HTML entity(`&#32;`=공백, `&#10;`=줄바꿈) unescape 필수
  - xfdl 구조 변경 시 `/NEXACRO/Work/Ext/Apr/ccaak02/CCAAK02F010_PLAN.xfdl.js`에서 `var sUrl = "..."` 패턴 재추출

### 0-2. PharmGKB `clinicalAnnotation` API HTTP 400 (Minor)

- **증상**: `https://api.pharmgkb.org/v1/data/clinicalAnnotation?view=mostRecent&chemical.name=clopidogrel&gene.symbol=CYP2C19` → HTTP 400 Bad Request
- **원인**: URL/파라미터 형식이 현행 API 스펙과 불일치 추정 (PharmGKB → ClinPGx 전환 영향 가능)
- **완화**: CPIC API(`api.cpicpgx.org`)가 동등한 Level A 정보를 정상 제공 → 실질 영향 낮음
- **권고 수정**:
  1. `pharmgkb.md` 레시피에 현행 엔드포인트 재검증 (`api.pharmgkb.org` vs `api.clinpgx.org` 전환 확인)
  2. 쿼리 파라미터 형식 재검증 (`chemical.name` vs `chemical.symbol`)
  3. 실패 시 CPIC 단독 사용을 공식 폴백으로 레시피에 명시
- **증빙**: `e2e/v2_2026_04_14_DDI/E2E_TEST_REPORT.md §3 결함 #2`

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

## 4. Web API 전체의 Custom MCP 서버 전환 (Major, 인프라)

### 현황
2026-04-14 기준 5개 Web API(DailyMed, openFDA, MFDS, PharmGKB, CPIC)가 **WebFetch 기반**으로 통합됨. 쿼리 레시피는 `.claude/references/api_reference/`에 수록.

### 전환 트리거
다음 조건이 충족되면 Custom MCP 서버로 전환:
- **일관성 이슈 실측**: WebFetch 기반 추출이 에이전트마다 다른 필드를 놓치거나 동일 쿼리에 다른 결과를 내는 사례가 축적
- **Rate limit 초과**: openFDA 무키 1,000 req/day 또는 PharmGKB 2 req/sec 초과
- **Plugin 배포**: `clinical-pharmacology-study-protocol-development` Claude Code plugin 전환 시 — 이때 MCP로 전환하면 다른 사용자가 API 쿼리 패턴 재학습 불필요

### 구현 스케치
1. `.claude/scripts/mcp-servers/dailymed.mjs` (~200줄)
   - `get_spl_by_drug_name(name) → setid[]`
   - `get_spl_label(setid) → {sections}`
   - `extract_pg_section(setid) → text`
2. `.claude/scripts/mcp-servers/openfda.mjs` (~300줄)
   - `get_drugsfda(generic_name)`, `get_label(generic_name)`, `count_faers_reactions(drug_name)`
3. `.claude/scripts/mcp-servers/mfds.mjs` (~150줄)
   - `search_clinical_trials({drug_name, sponsor, date_range, page})` → HTML 파싱 + 구조화
4. `.claude/scripts/mcp-servers/pharmgkb.mjs` (~200줄)
   - `get_clinical_annotation(drug, gene)`, `get_guideline(drug, source)`, `get_label_pgx(source, drug)`
5. `.claude/scripts/mcp-servers/cpic.mjs` (~200줄)
   - `get_pair(drug, gene) → {level, guideline}`
   - `get_recommendations(drug, gene) → {phenotype: recommendation[]}`
   - `get_diplotype_mapping(gene) → {diplotype: phenotype}`
6. `.mcp.json` 프로젝트 루트에 5개 서버 등록
7. regulatory-expert/translational-scientist의 "Web API" 섹션을 "MCP Tools"로 이동
8. `.claude/references/api_reference/` — 레퍼런스로 유지 (MCP 서버 디버깅 및 폴백용)
9. 기존 커뮤니티 MCP 참고 검토:
   - **OpenPGx** (https://github.com/open-pgx/openpgx) — PharmGKB + CPIC 통합, 초기 단계(star 5)
   - **BioMCP** — CPIC + PharmGKB 통합

### 우선순위 판단
현재 WebFetch로 충분. **Plugin 전환 시점까지 보류** 권장. 단, 커뮤니티 MCP(OpenPGx, BioMCP)가 안정화되면 재검토 가치 있음.

---

## 5. MFDS `data.go.kr` OpenAPI 전환 (Major, 안정성)

### 현황
MFDS 의약품안전나라 임상시험 승인현황은 현재 **searchClinic HTML 스크래핑**으로 운영 중. 공식 OpenAPI(`data.go.kr` ID 15056835 등)는 serviceKey 발급이 필요해 미통합.

### 전환 트리거
- **searchClinic HTML 구조 변경**으로 파싱 실패가 반복 발생
- **대량 조사 필요**: 수백 건 이상 페이지네이션 시 HTML 파싱 부담이 커짐
- **공식 인용 필요**: 계획서/보고서에 "공식 API 기반"이라는 명시가 필요한 경우

### 전환 절차
1. 사용자가 `data.go.kr`에서 무료 회원가입 후 serviceKey 발급
   - API: `15056835` (의약품 임상시험 정보) 기본
   - 개발계정 10,000 req/day, 운영계정은 활용사례 등록 후 증설
2. serviceKey를 **환경변수** `MFDS_SERVICE_KEY`로 저장 (절대 settings.local.json이나 파일로 커밋 금지)
3. `.claude/references/api_reference/mfds.md`에 OpenAPI 섹션 추가 (엔드포인트·파라미터 상세)
   - Swagger UI는 JS 렌더링이라 WebFetch로 파싱 불가 → 사용자가 data.go.kr 로그인 후 명세 확인 필요
4. regulatory-expert.md Step D를 "OpenAPI 우선, searchClinic fallback"으로 변경

### 우선순위 판단
현재 searchClinic으로 충분. HTML 구조 변경이 실제 발생하면 그때 전환. **Plugin 배포 시에는 무조건 OpenAPI 전환 권장** (다른 사용자가 serviceKey 발급만 하면 동작).

---

## 6. `regulatory-review` 스킬명 변경 검토 (Minor, 네이밍)

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

## 7. ~~ICH E6(R3) Annex 1 체크리스트 원문 검증~~ ✅ 완료 (2026-04-14)

사용자가 ICH E6(R3) 2025-01-06 최종본 PDF를 제공하여 전체 원문을 MD로 변환하고 체크리스트를 재구성함.

### 해결 내용
- **원문 수록**: `.claude/references/guidelines/ich/e6_r3_full/` 하위 10개 MD 파일 (Introduction + Principles + Annex 1 × 4 + Appendix A/B/C + Glossary)
- **체크리스트 갱신**: `regulatory-review/SKILL.md`의 "13개 필수 항목"을 **Appendix B 공식 16개 섹션(B.1~B.16)**으로 교체
- **발견한 추정 오류**:
  - 기존: 13개 "필수 항목" → 실제: **16개 공식 섹션**
  - 누락된 섹션: B.6 Discontinuation, B.11 Direct Access, B.15 Financing, B.16 Publication
  - **B.8이 공식적으로 "Assessment of Efficacy"** — 최근 "Phase 1 용어 정책 완화"가 ICH 원문에 부합함이 확인됨
- **요약본 보존**: 기존 `ich_e6_r3.md`는 빠른 참조용 요약으로 유지, 상단에 원문 링크 추가

### 후속 과제 (남은 원문 필요 항목)
`needs_user_input.md`의 항목 2-8 (ICH E8(R1), E14, M13A, E9(R1), E17, M9)도 동일한 방식으로 PDF 제공 시 보강 가능. **Quick Win 후보**.

---

## 8. ICH E6(R3) 요약본 재작성 검토 (Minor, 품질)

### 현황
`ich_e6_r3.md` 요약본은 원문 없이 2차 자료·기억에 기반하여 작성됨. 일부 섹션 번호나 세부 내용이 원문과 미묘한 차이가 있을 수 있음.

### 해결 경로
원문 MD(`e6_r3_full/`)를 참조하여 요약본을 전면 재작성. 또는 요약본 자체를 폐기하고 원문 링크만 유지 (실용 가치 재평가 필요).

### 우선순위 판단
현재는 원문이 확보되어 있으므로 요약본 오류 영향은 제한적. 실사용 중 요약본에서 발견한 구체 오류가 있을 때 교정하는 방식으로 충분.

---

## (구 번호 7: 정책 갱신으로 대체됨)
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

✅ **Minor (3건)** — `ad8e69f` 커밋
- m3: clinical-research 시험 유형별 특화 조사 표 경계 명확화
- m4: /synopsis 인자-스크립트 매핑 표 명시화
- m5: settings.local.json 불필요 권한 정리

✅ **DailyMed/openFDA WebFetch 통합** (2026-04-14)
- `.claude/references/api_reference/dailymed.md` — SPL 2-step 조회, PG 섹션 추출 레시피
- `.claude/references/api_reference/openfda.md` — 5개 엔드포인트, FAERS 이상반응 집계
- regulatory-expert.md + clinical-research/SKILL.md Step 3에 구체 절차 반영
- CLAUDE.md + README.md에 "Web API (WebFetch)" 섹션 신설

✅ **MFDS 의약품안전나라 WebFetch 통합** (2026-04-14)
- `.claude/references/api_reference/mfds.md` — searchClinic 리버스엔지니어링 기반
- 파라미터 전체(searchType/Keyword/approvalDt/clinicStepCode 등) 확인
- regulatory-expert.md + clinical-research/SKILL.md Step 4 갱신
- 공식 `data.go.kr` OpenAPI 전환은 위 5번 항목으로 이관

✅ **PharmGKB/CPIC WebFetch 통합** (2026-04-14)
- `.claude/references/api_reference/pharmgkb.md` — api.pharmgkb.org/v1, CC BY-SA 4.0
- `.claude/references/api_reference/cpic.md` — api.cpicpgx.org/v1, CC0 Public Domain, PostgREST
- translational-scientist.md에 "Web API (WebFetch) — PharmGKB/CPIC" 섹션 + 5단계 조사 절차 추가
- 한국인 빈도는 PubMed 보완 조사 명시 (PharmGKB/CPIC에 구조화 안 됨)
- Custom MCP 서버 전환은 위 4번 항목으로 이관

✅ **ICH E6(R3) 원문 MD 변환 및 체크리스트 재구성** (2026-04-14)
- `ich/e6_r3_full/` 10개 파일: Introduction, Principles (11개), Annex 1 × 4 섹션, Appendix A/B/C, Glossary
- `pdftotext -layout` + Python 스크립트로 86페이지 PDF를 정확히 추출
- `regulatory-review/SKILL.md` 체크리스트: 기존 13개 추정 → **Appendix B 공식 16개(B.1~B.16)**로 전면 교체
- 기존 체크리스트에서 누락되어 있던 B.6/B.11/B.15/B.16 추가
- B.8 "Assessment of Efficacy"가 공식 섹션명임을 확인 → Phase 1 용어 정책 정당성 확보
- `ich_e6_r3.md` 요약본 메타정보에 원문 링크 추가, `needs_user_input.md` 항목 1 완료 표시
- TODO #7 완료
