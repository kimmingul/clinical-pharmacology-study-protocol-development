# Claude 하네스 아키텍처 분석

분석 대상: `/Users/min/Projects/clinical-pharmacology-study-protocol-development` v2.0.0
분석 일자: 2026-05-22
분석자 범위: 에이전트 정의 정합성, 스킬·커맨드 매핑, 게이트/재실행 정책, ICH E6(R3) Appendix B 체크리스트 정합성, Reference 의무화 정책

---

## 1. 에이전트 역할 경계 분석

### 1.1 PK vs PD 경계 (clinical-pharmacologist ↔ translational-scientist)

**전반적으로 잘 분리됨**. 양쪽 에이전트 정의 파일에서 영역 경계를 명시적으로 선언한다.

- `.claude/agents/clinical-pharmacologist.md:10` — "PD 측면(약리학적 효과, 바이오마커, 수용체 점유)과 개인차(약물유전체학, 대사체학)는 translational-scientist 담당"
- `.claude/agents/translational-scientist.md:10` — "clinical-pharmacologist는 PK 측면(혈중 농도, 반감기, 대사 경로)을 담당. translational-scientist는 PD 측면(약리학적 효과, 바이오마커)과 개인차(PG/대사체)를 담당"
- `.claude/agents/translational-scientist.md:244` — "clinical-pharmacologist 영역 침범 금지: PK 파라미터(Cmax, AUC, t½), CYP 대사 경로의 정성적 기여(이건 CP), 약물상호작용 정량 결과(이건 CP) — 본 에이전트 영역 아님"

**잠재 회색 지대 1 — QTc 시험의 hERG/PK-QTc 모델링**:
- `clinical-pharmacologist.md:19` — "QTc(hERG는 안전성 약리, PD는 translational-scientist)"
- `translational-scientist.md:121` — "QTc | ★★ ddQTcF, C-QTc 모델 | ★★ KCNH2/SCN5A"
- `clinical-research/SKILL.md:82` — "QTc | hERG 데이터(안전성 약리), 기존 QTc 연구의 PK 측면 (PK-QTc 정량 모델은 translational-scientist) | ICH E14, FDA QT/QTc 가이드라인"

세 곳의 표현이 모두 일관된다(hERG는 CP, C-QTc/PK-QTc 모델은 TS). 하지만 **clinician.md의 QTc 섹션(81–82행)**은 별도 안전성 모니터링 관점에서 다루고 있어, "어느 에이전트가 QTc Holter/12-lead ECG 평가 시점의 과학적 근거를 작성하는가"가 명문화되어 있지 않다. (clinician은 "심전도 모니터링 항목·시점", CP는 "PK 측면", TS는 "C-QTc 모델"로 3분할되지만, 채혈/ECG 동기화 스케줄의 책임자가 모호함)

**잠재 회색 지대 2 — CYP 다형성 정량 변화**:
- `clinical-pharmacologist.md:18` — "DDI 기전 평가: 정성적 기여 및 기전 위주 (**PG 다형성에 따른 정량 변화는 translational-scientist 담당**)"
- `translational-scientist.md:244` — "약물상호작용 정량 결과(이건 CP) — 본 에이전트 영역 아님"

⚠️ **상호 모순 가능성**: CP는 "PG에 따른 정량 변화는 TS 담당"이라 하고, TS는 "약물상호작용 정량 결과는 CP 담당"이라 한다. CYP2C19 PM에서의 AUC 4배 증가 같은 데이터는 어느 쪽이 작성하는지 불확실. **PG 효과 ↔ 일반 DDI 정량 결과의 구분**이 명문화되어 있지 않다.

### 1.2 안전성 vs 규제 경계 (clinician ↔ regulatory-expert)

**경계는 비교적 명확**. 그러나 **약물 라벨 이상반응 데이터의 처리에 책임 충돌 위험**이 있다.

- `regulatory-expert.md:16` — 약물 라벨 정보 수집(허가사항, 약물상호작용, 금기, **이상반응 포함**)
- `clinician.md:110` — "라벨 이상반응 vs 문헌 이상반응: 약물 라벨(regulatory-expert 담당)에 있는 이상반응 목록을 단순 복사하지 말 것. 문헌에서 빈도, 중증도, 시간 경과를 추가로 수집"
- `clinician.md:32` — "PK 파라미터 수집(CP 담당)이나 규제 가이드라인(REG 담당)과 겹치지 않도록 한다"

라벨에서 추출된 이상반응 목록이 어느 산출물에 들어가는지(`labels/{drug}_DailyMed.md` vs `safety/AE_profile_{drug}.md`)는 명시되어 있으나, 이를 **통합 보고서에서 어떻게 합치는지**는 trial-doc-orchestrator/SKILL.md Phase 3에서 다루지 않는다. 중복 가능성.

### 1.3 잠재적 중복/누락 영역

| 영역 | 현재 상태 | 위험 |
|------|---------|------|
| **QTc ECG 모니터링 시점 결정** | CP(PK 시점), TS(C-QTc), clinician(안전성 ECG)에 분산. 명시적 통합 책임자 없음 | 중복 또는 누락 |
| **CYP PG 정량 변화** | CP가 "TS 담당"이라 하나 TS는 "정량 결과 = CP"라 함 | 상호 책임 회피 |
| **약물 라벨 이상반응** | regulatory-expert가 라벨 추출, clinician이 보강 — 명문화는 됐으나 통합 규칙 부재 | 중복 |
| **소아 채혈량 제한** | `clinician.md:113`만 다룸 — Special Pop 전반은 다른 에이전트가 다루는가? | 누락 가능 |
| **양방향 DDI 방향성 평가 매트릭스** | CP만 작성(`clinical-pharmacologist.md:93–158`). TS는 PG 측면에서 동일 매트릭스 작성 의무 없음 | TS와 CP가 방향성을 다르게 판단할 가능성 |
| **PK 채혈 시점 + PD 마커 시점 동기화** | CP와 TS가 별도 reference 파일 생성 — 동기화 책임은 메인 에이전트 또는 protocol-writer | Phase 4 협의에서 협의되긴 하나 책임자 불명확 |

### 1.4 입출력 명세 명확성

- 입력/출력 경로는 모든 에이전트에서 `_workspace/01_research_*.md` 형식으로 표준화됨.
- 단, **biostatistician**(`biostatistician.md:75–76`)는 입력으로 `_workspace/00_input/design_decisions.md` + `_workspace/01_research_report.md`를 명시하나, 일부 시험 유형은 `01_research_ts.md`의 PD 변동성을 받아야 함(`translational-scientist.md:264` — "biostatistician에게 PD 변동성 자료 제공 → PK-PD 분석 또는 sample size 보정에 활용"). 이 데이터 흐름이 명시적으로 biostatistician 입력에 포함되지 않음. **누락**.

### 1.5 에이전트 호출 deadlock·순환 의존

조사 단계(Phase 2)에서 4-5명이 **병렬 호출** + 산출물이 서로 다른 파일에 작성 → 순환 의존 없음. 검토 단계(Phase 9)도 동일 패턴. **deadlock 위험 낮음**.

다만 `translational-scientist.md:263` — "regulatory-expert가 추출한 약물 라벨의 PG 섹션을 본 에이전트가 재해석"이라는 데이터 흐름은 **병렬 호출에서 순서 의존성**을 만든다. regulatory-expert가 라벨 추출을 완료하기 전에 TS가 재해석할 수 없으므로, **TS의 라벨 PG 해석 작업은 실질적으로 Phase 2 단일 라운드에서 불가능**(병렬 호출이라 라벨 파일이 완성되지 않은 시점에 TS가 실행됨). 현재 trial-doc-orchestrator는 Phase 2의 라운드 분할 또는 Phase 3 후 TS 재호출을 명시하지 않음. → **소프트 데드락**.

---

## 2. 스킬·커맨드·에이전트 3계층 매핑 정합성

### 2.1 Command ↔ Phase ↔ Skill ↔ Agents 매핑

| Phase | Command | Skill | 호출 Agents (참여 조건) | 상태 |
|-------|---------|-------|---------------------|------|
| 0 | (없음, 메인) | — | — | OK |
| 1 | (없음, 대화) | — | — | OK |
| 2 | `/research` Step 2 | clinical-research | CP(항상) + REG(항상) + CLIN(항상) + TS(BE/FE 외) | OK |
| 3 | `/research` Step 4 | clinical-research | 메인(게이트) | OK |
| 4 | `/design` Step 1-4 | (없음, 대화) | — | OK |
| 5 | `/design` Step 5 | (없음) | biostatistician | OK |
| 6 | `/synopsis`, `/compare` | (없음) | 메인 | OK |
| 7 | (사용자 승인) | — | — | OK (Hard Gate) |
| 8 | `/protocol` | protocol-drafting | protocol-writer | OK |
| 9 | `/review` | regulatory-review | CP+CLIN+REG+BS(항상) + TS(BE/FE 외) + qa-reviewer | OK |
| 10 | `/icf` | icf-drafting | icf-writer | OK |

**Phase ↔ Command 매핑은 trial-doc-orchestrator/SKILL.md:14–22에서 명시적**으로 1:1 대응됨. 정합성 우수.

### 2.2 스킬 description의 trigger keyword 충돌

- `protocol-drafting`(`SKILL.md:2`): "계획서 작성, 프로토콜 작성, 시험 설계, 계획서 수정, 프로토콜 수정 요청 시 사용"
- `trial-doc-orchestrator`(`SKILL.md:3`): "임상시험 문서 작성, 계획서 개발, 프로토콜 개발, 동의설명서 개발, 시험 문서 생성 요청 시 사용. 후속 작업: **문서 수정, 계획서 수정**, 동의설명서 수정, 프로토콜 업데이트, 문서 보완, 다시 실행, 재실행"

⚠️ **"계획서 수정", "프로토콜 수정" trigger가 양쪽 스킬에 동시 정의됨**. 사용자가 "계획서 수정"이라 요청하면 두 스킬이 모두 트리거 후보가 된다. 우선순위 규칙이 명문화되지 않음.

- `clinical-research`(`SKILL.md:3`): "임상시험 조사, 문헌 검색, 배경 연구, 유사 시험 분석, 규제 자료 조사, 가이드라인 검색, 약물 라벨 조회 요청 시 사용"
- `regulatory-review`(`SKILL.md:3`): "문서 검토, 문서 리뷰, QA, 품질 검토, 일관성 검토, **규제 검토**, 계획서 리뷰 요청 시 사용"

`regulatory-review`의 "규제 검토"와 `clinical-research`의 "규제 자료 조사"는 의미가 다르지만(전자는 작성된 문서 리뷰, 후자는 사전 자료 수집), **"규제"** 키워드로 모두 매칭될 가능성. (Minor)

### 2.3 clinical-research skill의 TS 참여 매트릭스 vs README/CLAUDE.md 일관성

| 출처 | BE | FE | DDI | QTc | FIH | ADME |
|------|----|----|-----|-----|-----|------|
| `clinical-research/SKILL.md:39–43` | 불참 | 불참 | 참여 | 참여 | 참여 | 참여 |
| `commands/research.md:42–52` | 불참 | 불참 | 참여 | 참여 | 참여 | 참여 |
| `commands/review.md:14–20` | 불참 | 불참 | 참여 | 참여 | 참여 | 참여 |
| `trial-doc-orchestrator/SKILL.md:33` | 불참 | 불참 | 참여 | 참여 | 참여 | 참여 |
| `README.md:34` | 불참 | 불참 | 참여 | 참여 | 참여 | 참여 |
| `CLAUDE.md` 5번째 표 | 불참 | 불참 | 참여 | 참여 | 참여 | 참여 |

**일관성 우수**.

### 2.4 ★ CRITICAL — clinician 참여 조건 모순

**4곳에서 명시적으로 모순됨**:

| 출처 | clinician 참여 |
|------|--------------|
| `.claude/agents/clinician.md:3` (description) | "**모든 시험에서 참여**" |
| `.claude/agents/clinician.md:10` | "건강인 대상(DDI, BE, FE)이든 환자 대상이든 관계없이 **항상** 참여" |
| `trial-doc-orchestrator/SKILL.md:35` | "clinician | sonnet | ... | **항상**" |
| `trial-doc-orchestrator/SKILL.md:451` | "**clinician은 항상 참여**: 건강한 성인 시험에서도 안전성 프로파일 체계적 수집은 필수" |
| `commands/research.md` | clinician을 무조건 호출(조건문 없음) |
| `commands/review.md:88` | "항상 참여 (모든 시험)" |
| `.claude/skills/clinical-research/SKILL.md:596` | "⚠️ **clinician 호출 조건**: 건강한 성인 대상(DDI, BE, FE)에서는 clinician이 불참. 환자 대상 시험에서만 참여" |

⚠️ `.claude/skills/clinical-research/SKILL.md:596`의 Gotcha 항목은 **다른 모든 정의(에이전트 정의, 오케스트레이터, 두 commands, 자기 SKILL의 28-29줄)와 정면 충돌**. 이 SKILL.md를 Read한 서브에이전트가 잘못된 행동을 할 수 있음. **즉시 수정 필요**.

---

## 3. 게이트·재실행 정책

### 3.1 Hard Gate 무결성 (Phase 7)

- `commands/protocol.md:8–14` — "전제 조건 (Hard Gate): 1. `_workspace/02_synopsis.md`가 존재해야 함, 2. Synopsis가 사용자에 의해 **명시적으로 승인**되어야 함. 미충족 시: ... 'Synopsis를 검토하시고 승인해주세요. 승인 후 /protocol을 다시 실행합니다'"
- `trial-doc-orchestrator/SKILL.md:287–291` — "이 게이트는 건너뛸 수 없다"

⚠️ **약점**: 승인의 검증 방법은 **사용자의 자연어 응답에만 의존**. `.claude/skills/protocol-drafting/SKILL.md:9` — "Synopsis 승인(Phase 7) 후에만 이 스킬이 실행된다"고 명시하나, 코드 수준의 차단(예: `_workspace/02_synopsis.md.approved` 같은 sentinel 파일)이 없음. 사용자가 "OK"라고만 답해도 protocol-writer가 호출됨. **메인 에이전트의 판단에 게이트 무결성이 의존**.

권고: `_workspace/00_input/synopsis_approved.md` 같은 명시적 승인 마커 파일을 둬서 `commands/protocol.md`가 ls로 확인하게 하면 우회 위험 감소.

### 3.2 QA Critical 자동 수정 루프 방지

- `trial-doc-orchestrator/SKILL.md:379–399` — "Step 3: Critical 자동 수정 (조건부) ... **최대 1회만**. 재검토 후에도 Critical이 있으면 사용자에게 보고한다"
- `commands/review.md:159–168` — "**최대 1회만 수행.** 재검토 후에도 Critical이 있으면 사용자에게 보고"
- `CLAUDE.md` — "QA에서 Critical 발견 시 자동 1회 수정 후 재검토"

**무한루프 방지 정책 명확**. 단 카운터 메커니즘은 메인 에이전트의 자기 추적에 의존(파일 기반 카운터 없음). 메인 에이전트가 컨텍스트 초기화 후 재호출되면 카운터가 리셋될 위험 → 실무적 발생 가능성은 낮으나 이론적 결함.

### 3.3 부분 재실행 시 하류 의존성 전파

`trial-doc-orchestrator/SKILL.md:72–79`에서 의존성 규칙 명시:
- "자료 조사 보완" → Phase 2-3부터 하류 전체 재실행
- "설계 변경" → Phase 4부터
- "synopsis 수정" → Phase 6부터
- "계획서 수정" → Phase 8 → Phase 9
- "동의설명서 수정" → Phase 10만
- "리뷰 다시" → Phase 9만

**정책은 명확하나 강제 메커니즘은 없음**. 사용자가 "synopsis 수정"을 요청하면 메인 에이전트가 Phase 6부터 재시작하지만, **Phase 8/9/10 이전 산출물이 자동 무효화되지 않는다**. `_workspace/03_protocol_draft.md`가 그대로 남아있으면 다음 `/protocol`이 부분 수정으로 동작할 수도 있고 전체 재작성을 할 수도 있는데 이 분기가 명문화되어 있지 않음.

권고: Phase 6 재실행 시 `_workspace/03_protocol_draft.md`, `_workspace/04_icf_draft.md`, `_workspace/review/`에 "stale" 표시 또는 백업 후 삭제하는 자동 정책 추가.

---

## 4. ICH E6(R3) Appendix B 16개 섹션 체크리스트 정합성

원문(`.claude/references/guidelines/ich/e6_r3_full/07_appendix_b_protocol.md`) vs `regulatory-review/SKILL.md:67–84` vs `qa-reviewer.md` vs `protocol-drafting/SKILL.md:39–56` 비교:

| # | 원문 섹션명 (Appendix B) | regulatory-review/SKILL.md 표 | protocol-drafting/SKILL.md 섹션 | qa-reviewer.md | 정합성 |
|---|------------------------|----------------------------|-----------------------------|--------------|------|
| B.1 | General Information | ✅ "프로토콜 제목, 고유 식별 번호, 날짜, 개정 번호/날짜, 의뢰자 이름·주소, 서명 권한자" | §1 표지, §2 개정 이력 | 간접 명시 (Annex 1 필수 항목) | OK |
| B.2 | Background Information | ✅ "비임상/임상 주요 소견, 위험·이익, 투여 경로·용량·치료 기간 정당성, GCP 준수 선언, 대상 집단" | §4 서론 및 배경 | 간접 | OK — 원문의 B.2.5(GCP 준수 선언), B.2.7(문헌 참조) 포함 |
| B.3 | Trial Objectives and Purpose | ✅ "과학적 목적·목적의 명확 기술, Estimand 정보" | §5 시험 목적 | 간접 | OK |
| B.4 | Trial Design | ✅ "1차/2차 평가변수, 시험 유형·설계, 편향 최소화 조치, 시험약 설명·투여법, 스케줄, 중지 규칙·용량 조정, 대상자 참여 기간·순서, 설명책임 절차, 무작위화 코드 유지·해제 절차, 원본 자료 식별" | §6 시험 설계 | 간접 | ⚠️ "원본 자료 식별"이 protocol-drafting의 §6 또는 §15에 명시되어 있지 않음. 원문 B.4와는 다르고 실은 B.14(Data Handling)에 가까움. **`regulatory-review/SKILL.md:72`의 B.4 정의에 "원본 자료 식별" 포함은 원문 B.4 외 항목 (Appendix B 원문에 없음)** |
| B.5 | Selection of Participants | ✅ "선정 기준, 제외 기준" | §7 대상자 선정 | 간접 | OK. 단 원문 B.5.3(pre-screening/screening mechanism)은 누락 |
| B.6 | Discontinuation ... Withdrawal | ✅ "시험 중단·탈락 기준, 추적관찰 절차, 동의 철회 후 자료 처리" | (없음 — protocol-drafting 16개 섹션 목록에 별도 항목 없음. §6 또는 §8에 포함 추정) | 간접 | ⚠️ **`protocol-drafting/SKILL.md:39–56`의 "필수 섹션 16개"에 B.6 Discontinuation이 별도 섹션으로 명시되지 않음**. §6 시험 설계의 "중지 규칙" 또는 §12 안전성 평가에 흡수된 상태. 사용자가 protocol-template을 따를 때 누락 위험 |
| B.7 | Treatment and Interventions | ✅ "허용·금지 병용요법·약물, 환자 순응도 모니터링 절차" | §8 시험 치료 | 간접 | OK |
| B.8 | **Assessment of Efficacy** | ✅ 상세하게 명시 + Phase 1 용어 정책 반영 | §9 약동학/약력학(PK/PD) 평가 | 간접 ("Phase 1 용어 적절성") | OK. Phase 1 용어 가이드(`protocol-drafting/SKILL.md:133–154`)와 정확 일치 |
| B.9 | Assessment of Safety | ✅ "안전성 평가 변수, AE/SAE 기록·보고 방법, 안전성 추적관찰 계획" | §12 안전성 평가 | 간접 | ⚠️ 원문 B.9.4(임신 등 사후 추적관찰 기간)는 protocol-drafting/SKILL.md에 명시되지 않음 |
| B.10 | Statistical Considerations | ✅ "통계 분석 방법·중간 분석 계획, sample size 산출 근거, 유의수준, 분석 집단 정의, 결측치 처리" | §13 통계 분석 | 간접 | OK. 단 원문 B.10.5(SAP 일탈 시 CSR에 기술) 누락 |
| B.11 | Direct Access to Source Records | ✅ "의뢰자·규제 당국의 원본 자료 접근 권한, 모니터링·감사·IRB 심의·규제 검토 허용" | (없음 — 별도 섹션 없음) | 간접 | ⚠️ **`protocol-drafting/SKILL.md:39–56` 16개 섹션 목록에 B.11이 누락**. §14 윤리적 고려사항 또는 §15 자료 관리에 흡수 추정. **공식 섹션을 별도 항목으로 두지 않음** |
| B.12 | Quality Control and Quality Assurance | ✅ "QC·QA 절차, 모니터링 계획" | §15 자료 관리 및 품질 관리 | 간접 | OK |
| B.13 | Ethics | ✅ "윤리적 고려사항 (Declaration of Helsinki, IRB/IEC 승인, 참여자 보호)" | §14 윤리적 고려사항 | 간접 | OK |
| B.14 | Data Handling and Record Keeping | ✅ "자료 관리·기록 보존 방법, 전자 시스템 사용, 감사 추적" | §15 자료 관리 (B.12와 묶임) | 간접 | ⚠️ B.12와 B.14를 §15에서 합침. 원문은 별도 섹션 |
| B.15 | Financing and Insurance | ✅ "재정 및 보험 — 별도 문서로 다루어질 수 있음" | (없음) | 간접 | ⚠️ **누락**. 16개 섹션 목록에 명시 없음 (§16 부록에 흡수되지 않음) |
| B.16 | Publication Policy | ✅ "결과 공표 정책 — 별도 문서로 다루어질 수 있음" | (없음) | 간접 | ⚠️ **누락** |

**핵심 발견**:

1. `regulatory-review/SKILL.md:67–84`는 ICH E6(R3) 원문과 **체크리스트 수준에서 정확한 정합성** 확보 (TODO #7 완료 작업 결과)
2. `protocol-drafting/SKILL.md:39–56`의 "필수 섹션 16개"는 **번호로는 16개**이지만 **B.6, B.11, B.15, B.16과 1:1 매핑되지 않음**. 일부 섹션은 다른 섹션에 흡수되거나 누락됨. → **리뷰어가 16개 체크리스트로 점검할 때, protocol-writer가 작성한 문서의 섹션 번호와 정합하지 않을 위험**. Reviewer는 B.11을 찾는데 작성자는 §14·§15에 분산 작성.
3. `qa-reviewer.md:33`의 ICH E6(R3) Annex 1 언급은 일반적 — Appendix B의 16개 섹션을 명시적으로 나열하지 않고 `regulatory-review/SKILL.md`를 참조하도록 위임. **위임 자체는 OK**.

권고: protocol-drafting/SKILL.md의 "필수 섹션" 목록을 ICH E6(R3) Appendix B의 16개 섹션과 1:1 정확 매핑하여, B.6/B.11/B.15/B.16에 대응하는 protocol-template 섹션을 명시. 또는 protocol-template.md에 16개 섹션 헤더를 의무화.

---

## 5. Reference 의무화 정책 일관성

### 5.1 각 에이전트별 Reference 의무 정책

| 에이전트 | Reference 필수 명시 | Reference 날조 금지 명시 | 위치 |
|---------|------------------|-------------------|------|
| clinical-pharmacologist | ✅ Yes | ✅ Yes | `.md:28, 166` |
| translational-scientist | (간접 — "MCP 도구 한계 은폐 금지", "한국인 빈도 우선") | ✅ Yes | `.md:241, 246` |
| regulatory-expert | ✅ Yes | ✅ Yes | `.md:29, 137` |
| clinician | (간접 — "라벨 이상반응 vs 문헌 이상반응") | ❌ **명시 없음** | `.md:109` |
| biostatistician | (간접 — "계산 결과에 근거가 되는 문헌 인용") | ❌ **명시 없음** | `.md:21` |
| protocol-writer | (간접 — "용량 설정, 엔드포인트 선택 등 핵심 결정에는 문헌/IB 근거를 인용") | ❌ **명시 없음** | `.md:22` |
| icf-writer | ❌ **언급 없음** | ❌ **명시 없음** | — |
| qa-reviewer | (간접 — 리뷰에서 근거 인용을 요구함) | ❌ **명시 없음** | — |

⚠️ **clinician.md는 안전성 문헌 인용을 한 곳에서만 다루고 "Reference 날조 금지" 가드레일이 없음**. 안전성 데이터는 PMID/사례보고 인용이 핵심인데 가드레일 부재. 다른 조사 에이전트(CP, REG, TS)와 정책 불일치.

⚠️ **biostatistician.md**는 sample size CV%·GMR 출처를 요구하나 "MCP 결과에 없는 값을 추측하지 말라"는 가드레일이 없음. 시뮬레이션 시 추측 값을 사용할 위험.

⚠️ **protocol-writer.md**는 작성 에이전트로서 다른 에이전트 산출물의 reference를 인용해야 하나, "조사 보고서에 없는 reference를 만들어내지 말라"는 명시 없음.

⚠️ **icf-writer.md**는 리스크/이익을 기술할 때 안전성 데이터 출처 인용 요구가 없음. ICF는 시험대상자용이라 PMID 표기는 안 하지만, 기술된 위험 정보의 출처 추적이 불가하다.

### 5.2 QA 단계의 Reference 누락 검출

`qa-reviewer.md` 또는 `regulatory-review/SKILL.md` 어느 곳에도 **"Reference 누락 검출"이 체크리스트에 명시되어 있지 않다**. QA가 Critical/Major로 지적하는 항목 중 "PMID 미인용" 또는 "[출처 미확인]" 표시가 있는 항목을 자동 검출하는 절차 없음.

권고: `regulatory-review/SKILL.md`의 검토 항목에 "Reference 인용 완결성" 추가 (Major 등급), `qa-reviewer.md`에 "출처 미확인 항목 카운트" 의무화.

### 5.3 사용자 출력 시 Reference 차단 메커니즘

⚠️ **현재 차단 메커니즘 없음**. 메인 에이전트가 Phase 3 검토 게이트(`commands/research.md:161–172`)에서 사용자에게 "수집된 reference 파일 목록"을 제시하지만, **목록만 보여줄 뿐 결측 검증은 없음**. 통합 보고서(`01_research_report.md`)에 "[출처 미확인]"이나 빈 인용이 남아있어도 그대로 진행될 수 있다.

권고: Phase 3 게이트에 자동 자가 검증 — "통합 보고서에서 인용된 PMID/NCT/가이드라인 문서명을 모두 추출하여, 개별 reference 파일(`_workspace/01_references/`)에 실제 존재하는지 확인" 절차 추가.

---

## 6. 우선순위 권고 TOP 5

| # | severity | 영역 | 권고 | 영향도 |
|---|---------|------|------|-------|
| 1 | **Critical** | clinical-research/SKILL.md:596 Gotcha 항목과 다른 7곳 정의가 **clinician 참여 조건에서 정면 모순** | `clinical-research/SKILL.md:596` 줄을 즉시 삭제 또는 "건강인 시험에서도 항상 참여"로 정정. 서브에이전트가 이 SKILL.md를 Read하면 잘못된 행동(건강인 DDI/BE/FE 시험에서 clinician 불참)을 할 위험 | 운영 중단 수준의 결함. 즉시 수정 필요 |
| 2 | **Major** | `protocol-drafting/SKILL.md:39–56`의 16개 필수 섹션이 ICH E6(R3) Appendix B와 1:1 정확 매핑이 아님 (B.6/B.11/B.15/B.16 별도 섹션 없음) | 16개 섹션을 Appendix B와 1:1 매핑되도록 재구성하거나, `protocol-template.md`에 명시적 매핑 표 추가. 현재 리뷰어(`regulatory-review/SKILL.md:67–84`)는 16개 정확 체크하나 작성자는 다른 구조로 작성 → Critical 지적 빈발 위험 | QA 마찰 증가, 재작성 비용 |
| 3 | **Major** | translational-scientist의 라벨 PG 재해석은 regulatory-expert의 라벨 추출 산출물에 의존하나, Phase 2가 **병렬 호출**이라 TS 실행 시점에 라벨 PG 섹션이 아직 작성 안 됨 | (a) Phase 2를 라운드 분할(R1: REG 라벨 추출 → R2: TS 재해석) 하거나, (b) Phase 3 후 TS만 보충 호출하는 단계 명시 | TS의 PG 재해석 산출물이 빈약해질 위험. DDI/QTc 시험에서 PG 깊이 부족 |
| 4 | **Major** | 4개 에이전트(clinician, biostatistician, protocol-writer, icf-writer)에 "Reference 날조 금지" 가드레일 부재 | 각 에이전트 파일의 "Gotchas" 또는 "작업 원칙" 섹션에 "MCP/조사 보고서에 없는 PMID/근거를 추측으로 인용 금지" 추가. QA 체크리스트에 "출처 미확인 항목 카운트" 의무화 | 환각 인용 위험. 규제 제출 시 신뢰성 훼손 |
| 5 | **Major** | Synopsis 승인(Phase 7) Hard Gate가 자연어 응답 의존 — 명시적 sentinel 파일 없음. 부분 재실행 시 하류 산출물 자동 무효화 정책 부재 | (a) `_workspace/00_input/synopsis_approved.md` sentinel 파일 도입, (b) Phase 6 재실행 시 하류 산출물 백업/삭제 자동화 | 부분 수정 시 stale 산출물 잔존 → 사용자 혼란. 게이트 우회 가능성 |

---

## 부록: 추가 발견 (Minor)

1. **PG 정량 효과 책임 불명**: CP("PG는 TS 담당") ↔ TS("DDI 정량 결과는 CP 담당") 상호 책임 회피. CYP2C19 PM에서 AUC 변화 같은 정량 데이터의 작성 책임자 미정의.
2. **biostatistician 입력에 `01_research_ts.md` 누락**: TS가 PD 변동성 자료를 biostat에게 전달한다고 했으나 biostatistician.md:75–76 입력 명세에 미포함.
3. **QTc ECG 모니터링 시점**: CP/TS/clinician 3분할 중 통합 책임자 불명.
4. **protocol-writer "Reference 날조 금지" 부재**: 작성 단계에서 환각 인용 위험.
5. **icf-writer Part 4 작성 조건 검증**: design_decisions.md만 의존 — Synopsis §10이 작성 조건과 불일치할 가능성 미차단.
6. **trigger keyword 충돌**: `protocol-drafting`의 "계획서 수정" vs `trial-doc-orchestrator`의 "계획서 수정" 동시 매칭 가능. 우선순위 규칙 부재.
7. **QA Critical 자동 수정 카운터**: 파일 기반이 아닌 메인 에이전트 메모리 — 컨텍스트 초기화 시 리셋 위험.

---

## 분석 메서드

- 읽은 에이전트 파일 8개: `.claude/agents/{clinical-pharmacologist,translational-scientist,clinician,regulatory-expert,biostatistician,protocol-writer,icf-writer,qa-reviewer}.md`
- 읽은 스킬 파일 5개: `.claude/skills/{trial-doc-orchestrator,clinical-research,regulatory-review,protocol-drafting,icf-drafting}/SKILL.md`
- 읽은 커맨드 파일 7개: `.claude/commands/{research,design,synopsis,compare,protocol,review,icf}.md`
- 읽은 ICH 원문: `.claude/references/guidelines/ich/e6_r3_full/07_appendix_b_protocol.md`
- TODO.md, CLAUDE.md, README.md grep 검증
- 모순/누락 검출은 키워드 cross-grep으로 보강
