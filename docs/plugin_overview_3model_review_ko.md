# 플러그인 종합 설명 — 작동원리·프로세스·자료조사·에이전트·출처 (3-모델 리뷰)

> ⚠️ **[HISTORICAL — v2.1.0 기준]** 이 문서는 v2.1.0 시점의 구조를 설명한다. 본문의 에이전트 모델 표(조사=sonnet)·Phase 9 설명은 **v2.1.0 설정**이며, **v3.0.0에서는 전 에이전트 opus + actor-critic 수렴 루프 + zero-trust 검증 + 3-tier 가드레일**로 변경되었다. 현재 구조는 [`docs/plugin_v3_advancement_proposal_ko.md`](plugin_v3_advancement_proposal_ko.md)·[`CLAUDE.md`](../CLAUDE.md)·[`CHANGELOG.md`](../CHANGELOG.md) 참조.

| 항목 | 내용 |
|------|------|
| 대상 | `clinical-pharmacology-study-protocol-development` **v2.1.0** |
| 작성일 | 2026-06-14 |
| 리뷰어 | **Gemini 0.46**(신선) · **Codex 0.139**(신선) · **Claude**(저, 코드 직접 정독) |
| 교차 대조 | 기존 3-모델 리뷰(`.omc/research/team_review_2026_05_22/`) + 저자 교과서 원고(`docs/manuscript_..._ko.md`) |
| 결론(합의) | 단순 문서 자동화를 넘어선 **임상시험 설계 의사결정 보조 시스템(DSS)**. 한국적 규제 특수성(MFDS·PIPA·생명윤리법)을 기술로 구현 |

> **리뷰 방법**: 세 모델로 v2.1.0 현재 상태를 각각 독립 리뷰하고, 저자가 이미 수행한 2026-05-22 3-모델 리뷰 및 직접 쓴 AI 교과서 원고와 대조했다. 세 모델의 결론은 일치했다.

---

## 핵심 한 줄

이것은 **"AI에게 계획서를 써달라고 시키는 도구"가 아니라**, 교과서 원고의 표현대로 **임상약리 전문가의 판단·검토 프로세스 자체를 구조(harness)로 재현해, AI가 그 규범 안에서 일하도록 만든 시스템**이다. 계획서(protocol)는 "판단의 집합체"이므로, 그 판단들을 **단계로 분해 → 전공별 전문가에게 분담 → 사람 검토 게이트로 통제**한다. 신입에게 곧바로 "계획서 써와" 하지 않고 템플릿·기준·검토문화를 함께 가르치는 것과 같다.

---

## 1. 작동원리 — 왜 "한 명의 똑똑한 AI"가 아닌가

LLM 하나에 맡기면 ① 목적-설계 논리가 끊기고 ② 규제 필수항목이 빠지고 ③ 근거 문헌을 날조하고 ④ 계산 가정이 드러나지 않는다(교과서 원고 §1.3의 진단). 이 플러그인은 그 빈틈을 **4가지 구조 장치**로 막는다.

| 장치 | 역할 | 인간 프로세스 대응 |
|------|------|------------------|
| **다중 에이전트** | 8명의 전공 페르소나가 영역을 나눠 담당 | 임상개발팀(PK·통계·규제·안전성·작성·QA) |
| **자료 불러오기(RAG)** | 모든 주장에 PMID/NCT/URL 출처 의무화 | 문헌·승인사례·라벨·가이드라인 검색 |
| **계산 코드** | 표본수·초기용량을 Python으로 *실행* | 통계 도구로 직접 계산(말로 하지 않음) |
| **검토 게이트** | 사람이 2곳에서 명시 승인해야 진행 | 상급자 검토·승인 문화 |

---

## 2. 프로세스 — 사람의 작성 절차를 그대로 옮긴 10단계

```
Phase 1  입력          약물명 + 시험유형 (FIH는 IB 첨부)
   │
Phase 2  병렬 자료조사   CP · 규제 · 임상의 · (중개의학)   ← 동시 조사
   │
Phase 3  ★게이트1★      핵심발견 요약 → 사용자 검토·승인   (자료 검토)
   │
Phase 4  설계 협의       선정/제외 → 연구설계 → 채혈/평가변수 (대화형)
Phase 5  통계 설계       biostatistician가 Python으로 표본수 산출
   │
Phase 6  Synopsis        1~3p 설계 요약 작성
   │
Phase 7  ★게이트2★      Synopsis 승인 (Hard Gate — 건너뛸 수 없음)
   │
Phase 8  Protocol        ICH E6(R3) Appendix B 16섹션 Full Protocol
Phase 9  다중 리뷰        4~5명 병렬 검토 → QA 취합(Critical/Major/Minor)
   │
Phase 10 ICF             동의설명서/동의서/개인정보 동의서 (별도 /icf)
```

**핵심은 게이트 2개다.** ① 자료가 부실하면 설계로 넘어가지 못하고, ② Synopsis(설계 합의)를 사람이 승인하기 전에는 본문을 쓰지 않는다 — 잘못된 전제로 수십 페이지를 쓰는 낭비를 원천 차단한다. Codex·Gemini 모두 이 "단계적 제어"를 최대 강점으로 꼽았다.

각 단계는 `/research` `/design` `/synopsis` `/protocol` `/review` `/icf` 커맨드로 개별 실행할 수도 있고, 산출물은 `_workspace/`에 단계별 파일(`01_research_report.md` → `02_synopsis.md` → `03_protocol_draft.md` → `04_icf_draft.md`)로 누적된다.

---

## 3. 에이전트별 페르소나 — 가상 임상시험팀

| 에이전트 | 모델 | 실제 팀 역할 | 참여 |
|---------|------|------------|------|
| **clinical-pharmacologist** | sonnet | PK(반감기·변동성)·대사경로·DDI 기전·FIH 초기용량 | 항상 |
| **translational-scientist** | sonnet | PD 바이오마커·PK-PD 모델·약물유전체(PG)·대사체 | 조건부(BE/FE 제외) |
| **regulatory-expert** | sonnet | MFDS/FDA/EMA 가이드라인·약물라벨·ICD-10 | 항상 |
| **clinician** | sonnet | 선정/제외 기준·안전성 프로파일·중지규칙 | **항상** |
| **biostatistician** | sonnet | 연구설계·표본수(Python)·무작위화·분석 | 항상 |
| **protocol-writer** | opus | Synopsis+자료 기반 Full Protocol 작성 | Phase 8 |
| **icf-writer** | opus | 계획서 기반 동의문서(생명윤리법 Part 4 포함) | Phase 10 |
| **qa-reviewer** | opus | 다중 리뷰 취합·우선순위 분류·수정 조율 | Phase 9 |

**설계의 묘**(Gemini·Codex 공통 호평):
- **PK(CP) ↔ PD/PG(TS) 분리** — 최신 중개의학·FIH 트렌드 반영
- **작성(opus) ↔ 검토(병렬) 분리** — 자기 글을 자기가 통과시키지 않는 cross-check
- **clinician 항상 참여** — 건강인 시험도 안전성 전담자 필수
- **모델 차등** — 조사는 sonnet(빠르고 충분), 작성·검토는 opus(깊은 추론)

> **정직한 빈틈**(Codex 지적): 실제 팀에 있는 **bioanalytical(분석법)·임상운영(CRC)·데이터관리(EDC)·약물감시(PV)** 전담 역할은 별도 에이전트로 없다. 현재는 계획서·동의서 작성에 집중한 범위라 합리적 선택이나, 확장 여지다.

---

## 4. 자료조사 방법과 출처 — "환각 방지"가 설계 목표

모든 주장에 **검증 가능한 출처(PMID·NCT·URL·가이드라인 인용)를 의무화**하고, 확인되지 않은 것은 `[출처 미확인]`으로 표시한다(날조 금지).

**(A) MCP 도구** — PubMed(문헌) · ClinicalTrials.gov(유사시험 설계·엔드포인트) · ICD-10(적응증 코딩)

**(B) Web API(WebFetch)** — 5종, 무인증 즉시 사용:
- **MFDS 의약품안전나라**: 국내 임상시험 승인현황(searchClinic) + 상세본문(Nexacro SOAP 직접 호출) — *한국 특수성을 기술로 구현* (Gemini 호평)
- **DailyMed / openFDA**: FDA 라벨 전문 · 허가정보(NDA) · FAERS 이상반응
- **PharmGKB / CPIC**: 약물-유전자 임상 annotation · 표현형별 용량권고

**(C) 사전수록 가이드라인 라이브러리** — 매번 웹검색 대신 신뢰 사본을 내장(재현성↑): ICH E6(R3) 전문·E8(R1)·E14·M13A, FDA·EMA·MFDS 가이드라인, 시험유형별 cross-agency 비교표.

> **3-모델 공통 한계 지적**: PubMed 전문은 OA 중심(초록 의존) · MFDS는 HTML 구조 변경에 취약 · FAERS는 인과성/빈도 해석 제한 · PharmGKB는 한국인 빈도 미제공(PubMed 보완) · 일부 가이드라인 원문 미수집(`needs_user_input.md`).
>
> **Codex의 1순위 개선**: 이 외부수집 계층을 WebFetch 레시피 → **MCP 서버 / 공식 `data.go.kr` API**로 고정하고, 매 호출을 manifest에 해시·조회일·URL로 남길 것. 임상약리 근거 완결성과 소프트웨어 재현성 리스크를 동시에 줄인다.

---

## 5. 규제·GCP 출처 — 무엇을 근거로 쓰는가

계획서의 "규제 적합성"은 다음 골격 위에서 만들어진다:
- **ICH**: E6(R3) GCP — **Appendix B의 16개 필수섹션(B.1~B.16)을 1:1 준수**(작성자↔리뷰어 체크리스트 정렬), E8(R1) 일반고려, E14(QTc), M13A(BE)
- **국내 법령**: 약사법 · KGCP · 개인정보보호법(PIPA) · 생명윤리법(인체유래물/PG 분석 시 ICF Part 4 별도동의)
- **재발 오류 방지 상수 내장**(Gemini가 강점으로 지목): KGCP 기록보존 **15년**, SAE 보고 7일+8일, 시험종료 90일, BE/DDI 동등성 **90% CI 80.00–125.00%** — 사람이 자주 틀리는 수치를 에이전트에 사전 주입

---

## 6. 품질·신뢰 장치 (v2.1.0 강화)

- **통계는 코드로 검증**: 2×2 BE/DDI를 **exact TOST(noncentral-t)**로 계산하고 PowerTOST·몬테카를로 대조 테스트(73개) 통과 — "말로 표본수"가 아니라 재현 가능한 계산
- **출력 자동 검증(doc_lint)**: 16섹션 누락·보존기간 3년 오기·CI 경계·미해결 placeholder를 기계적으로 점검(CI 게이트 + 작성 직후 advisory 경고)
- **재현성 매니페스트**: 단계별로 어느 모델·버전이 어떤 입력으로 무엇을 만들었는지 SHA-256·타임스탬프로 기록
- **CI/CD · `claude plugin validate`**: PR마다 통계·정합성·보안 자동 검사

---

## 7. 3-모델 리뷰 종합 — 합의된 평가

**공통 호평**: 도메인 특수성을 깊이 반영한 정교한 멀티에이전트 설계 · 명확한 역할 경계(중복·누락↓) · 단계적 게이트와 추적성을 **아키텍처 수준에서 보장** · 통계를 코드로 처리 · 한국 규제(MFDS·PIPA·생명윤리법)를 기술로 구현.

**공통 리스크(전문가 최종검증 필수)**:
1. **IB 보안**(Gemini) — 신약 FIH의 비공개 IB를 클라우드 LLM에 올릴 때 유출 관리 필요
2. **용량근거 환각**(Gemini) — Dose Justification의 PK 수치 오독은 *자원자 안전에 직결* → 사람 검증 필수
3. **복잡설계 한계**(Gemini·Codex) — 양방향 DDI의 IUT/joint power 등은 전문가 최종 확인 필요
4. **외부수집 취약성**(Codex) — MFDS 크롤링 등은 구조 변경에 약함 → MCP/공식 API 전환이 다음 과제

**이번 리뷰가 찾아 즉시 고친 것**: Codex가 `icf-writer.md`의 계획서 입력 경로 오기(`02` → `03_protocol_draft.md`)를 발견 → 검증 후 수정·배포(commit `550aa1a`).

> **참고 — 직전 v2.0.0 리뷰와의 관계**: 2026-05-22 3-모델 리뷰가 찾았던 Critical/Major(2×2 표본수 2배 과대, RSABE 부정확, Williams joint power, clinician 정책 모순, Appendix B 매핑, Phase 2 의존성, sync 자동화, 테스트 부재 등)은 **v2.1.0에서 대부분 해결**되었다. 본 문서의 리뷰는 그 수정 이후 상태를 평가한 것이다.

---

## 맺음말

세 모델과 저자 교과서 원고가 같은 결론에 모인다 — 이것은 **AI가 사람을 대체하는 도구가 아니라, 사람의 판단·검토 규범을 구조로 만들어 AI가 그 안에서 안전하게 일하게 한 "실행 환경(harness)"**이다. 최종 책임과 과학적·규제적 판단은 여전히 임상약리 전문가에게 있고, 시스템은 그 판단을 *구조화·가속·검증*한다. 교과서 원고의 핵심 메시지("AI가 잘 쓰게 하려면 먼저 무엇을 생각해야 하는지 알려주어야 한다")가 코드로 구현된 사례로 정리할 수 있다.

---

## 부록 — 리뷰 출처

- 신선 리뷰: Gemini 0.46 / Codex 0.139 (본 v2.1.0 상태 대상, 2026-06-14)
- 기존 3-모델 리뷰: `.omc/research/team_review_2026_05_22/` (Claude·Codex·Gemini, v2.0.0)
- 저자 교과서 원고: `docs/manuscript_designing_clinical_pharmacology_studies_using_ai_textbook_ko.md`
- 1차 코드 정독: `.claude/`(agents·skills·commands·references·scripts) + `CLAUDE.md` + `README.md`
- 변경 이력: `CHANGELOG.md` (v2.1.0)
