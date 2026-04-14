# regulatory-expert 리뷰

## 검토 요약
- 검토 일시: 2026-04-14
- 대상 문서: `_workspace/03_protocol_draft.md` (CLO-OME-DDI-001 v1.0)
- 시험 유형: Phase 1 DDI (Clopidogrel-Omeprazole)
- 검토 초점: ICH E6(R3) Appendix B 16개 섹션 충족 여부, MFDS IND 요건, DDI 가이드라인 인용, 윤리 법령 인용, 생명윤리법 적용 명시, 1차 평가변수 정합성
- 근거 문서:
  - ICH E6(R3) 2025-01-06 Step 4 Final — Appendix B (`.claude/references/guidelines/ich/e6_r3_full/07_appendix_b_protocol.md`)
  - KGCP (`.claude/references/guidelines/regulations/korea_kgcp.md`)
  - 약사법 제34조 (`.claude/references/guidelines/regulations/korea_pharmaceutical_act.md`)
  - MFDS DDI 가이드라인 (`.claude/references/guidelines/mfds/mfds_ddi_guideline.md`)
  - DDI Cross-Agency 비교표 (`.claude/references/guidelines/by_study_type/ddi_cross_agency.md`)

---

## ICH E6(R3) Appendix B 16개 섹션 충족 체크리스트

> 근거: ICH E6(R3) Appendix B, Final version, 2025-01-06

| 섹션 | 공식 명칭 | 충족 여부 | 비고 |
|------|----------|:--------:|------|
| B.1 | General Information | **충족** | 프로토콜 번호·버전·날짜·의뢰자·서명권한자 포함 (placeholder 있으나 IND 제출 전 확정 예정) |
| B.2 | Background Information | **충족** | 시험약·병용약 설명, 비임상/임상 소견, 위험·이익 평가, 투여 근거, GCP 준수 선언, 인구집단 설명, 참고 문헌 포함 |
| B.3 | Trial Objectives and Purpose | **충족** | 1차·2차·탐색적 목적 명시. Estimand 미정의는 DDI 시험 특성상 수용 가능 (ICH E9(R1) 적용 불필요) |
| B.4 | Trial Design | **충족** | 설계 개략도, 평가변수, 무작위화·맹검 방침 명시, 투여법·일정·중지 기준, 약물관리 절차 포함 |
| B.5 | Selection of Participants | **충족** | 선정 6항목, 제외 18항목 (표준 15 + 약물 특이 3) |
| B.6 | Discontinuation of Trial Intervention and Participant Withdrawal from Trial | **충족** | 개인·시험 수준 중단 기준, 추적관찰, 대체 방침, 철회 후 데이터 처리 명시 |
| B.7 | Treatment and Interventions for Participants | **충족** | 시험약·병용약 정보, 투여 절차, 약물관리, 금지·허용 병용약 포함 |
| B.8 | **Assessment of Efficacy** | **충족** | ICH E6(R3) 공식 섹션명 "Assessment of Efficacy" 사용. DDI 시험의 1차 평가변수(H4 GMR)를 "유효성 평가"로 기술한 것이 Phase 1 용어 가이드에 부합하며 사유를 §B.8 주석에 명시 |
| B.9 | Assessment of Safety | **충족** | 안전성 파라미터, AE/SAE 기록·보고, 중지 기준, 추적관찰 계획 포함 |
| B.10 | Statistical Considerations | **충족** | 통계 방법, 중간 분석 방침, sample size 근거, 유의수준, 분석집단 정의, 결측치 처리 포함 |
| B.11 | Direct Access to Source Records | **충족** | 의뢰자·MFDS·IRB·외국 규제기관 접근 권한 명시 |
| B.12 | Quality Control and Quality Assurance | **충족** | QC·QA 절차, 모니터링 계획, 감사, 규제 실사 대응, SOP 목록 포함 |
| B.13 | Ethics | **충족** | 헬싱키 선언, ICH E6(R3), KGCP, 약사법 제34조, PIPA, 생명윤리법 인용. IRB·MFDS IND 절차, 동의 취득, 보험 명시 |
| B.14 | Data Handling and Record Keeping | **충족** | 자료 수집 방법, 원자료 식별, 기록 보존 기간 명시 |
| B.15 | Financing and Insurance | **충족** | 재정 및 보험 섹션 별도 존재, 피험자 보험 기준(약사법 시행규칙 제24조) 인용 |
| B.16 | Publication Policy | **충족** | 공표 정책 별도 섹션 존재, ICMJE·CRIS 등록 포함 |

**결론: 16개 섹션 모두 존재하며 구조적으로 충족.**

---

## 발견 사항

### [Major-1] MFDS DDI 가이드라인 발행일 불명확 — 2015년 표기 오류 가능성

- **심각도**: Major
- **위치**: 표지 "규제 준거", B.4.4 설계 선택 근거
- **내용**: 계획서 표지 및 §B.4.4에 "MFDS 의약품 상호작용시험 가이드라인(2015)"로 기재되어 있다. 그러나 본 레퍼런스 파일(`mfds_ddi_guideline.md`)에는 발행일이 "[전문 미수집 — 사용자 PDF 제공 필요]"로 표시되어 있어 2015년이 정확한지 확인되지 않는다. MFDS는 2022년 이후 일부 DDI 가이드라인을 개정하였으며, 최신 버전을 인용하지 않으면 규제 심사 시 지적받을 수 있다.
- **근거**: `mfds_ddi_guideline.md` 메타 정보 "발행일 / 최신 개정: [전문 미수집]"; MFDS 고시는 정기 개정됨
- **권고**: MFDS 홈페이지(`mfds.go.kr/brd/m_218`)에서 최신 DDI 가이드라인 발행일을 확인하여 정확한 발행연도를 기재. 만약 2015년이 최신이면 "[식약처 고시 제2015-xx호, 2015-xx-xx]" 형식으로 명시. 개정판 존재 시 개정판 인용으로 교체.

---

### [Major-2] MFDS 기록 보존 기간 불일치 — 계획서 "3년" vs KGCP "15년"

- **심각도**: Major
- **위치**: B.14.2 기록 보관
- **내용**: §B.14.2에 "시험 종료 후 최소 3년 (KGCP 제9조)"으로 기재되어 있다. 그러나 KGCP(`korea_kgcp.md`, 섹션 7.1)는 Essential Documents(동의서, CRF, 원자료 등)의 보존 기간을 "시험 완료 또는 조기 중단 후 최소 **15년**"으로 규정한다. "3년" 기재는 KGCP 실제 요건과 상충하는 중대한 오류이다. (단, 이 "3년"이 구 KGCP 기준이거나 특정 문서에 한정된 표현일 수 있으나, 오해를 유발할 수 있다.)
- **근거**: KGCP (`korea_kgcp.md`) §7.1 "Essential Documents: 시험 완료 또는 조기 중단 후 최소 **15년**" [의약품등의 안전에 관한 규칙 별표 4, MFDS, 2019-12-06]
- **권고**: §B.14.2를 다음과 같이 수정:
  - Essential Documents(동의서, CRF, 원자료, 프로토콜): **최소 15년** (KGCP)
  - 임상시험용 의약품 기록: 허가 만료 또는 시험 완료 후 최소 2년
  - 의료기관 의무기록: 의료법에 따라 10년 (별도 법률 적용)
  - "KGCP 제9조" 조항 번호도 원문 대조 후 정확히 기재 필요

---

### [Major-3] MFDS 1차 평가변수: AUC₀₋₂₄ vs AUC₀₋∞ 불일치

- **심각도**: Major
- **위치**: B.8.1, B.10.1, B.3.1
- **내용**: 계획서의 1차 평가변수는 **AUC₀₋₂₄**로 설정되어 있다. 그러나 MFDS DDI 가이드라인(`mfds_ddi_guideline.md` §4)은 1차 평가변수를 **"AUC₀₋∞"**으로 명시하고 있으며, AUC₀₋ₜ는 AUC₀₋∞ 산출 불가 시 사용하는 보조 지표이다. FDA DDI Guidance(2020) 및 ICH M12(2024)도 AUC₀₋∞를 1차로 요구한다. §B.8.1에 "절단 AUC 적용하지 않음" 및 "AUC₀₋₂₄ ≈ AUC₀₋∞ 수준으로 근사"라는 과학적 근거가 기술되어 있으나, 이는 가이드라인과의 공식적 정합성 문제를 완전히 해소하지는 못한다.
- **근거**: MFDS DDI 가이드라인 §4 "AUC₀₋∞: 1차 평가변수"; FDA Clinical DDI Guidance 2020; DDI Cross-Agency 비교표 "1차 평가변수: AUC₀₋∞"
- **권고**: 두 가지 옵션 중 선택:
  1. **(권장)** 1차 평가변수를 AUC₀₋∞로 변경하고, AUC₀₋₂₄는 보조 파라미터로 전환. 채혈 일정상 24시간 채혈로도 AUC₀₋∞ 추정이 가능 (H4 t½ ≪ 24 hr이므로 λz 추정 가능). Phoenix WinNonlin NCA에서 AUC₀₋∞ = AUC₀₋ₜ + Cₜ/λz로 산출.
  2. **(대안)** AUC₀₋₂₄를 유지하되, MFDS 사전 협의(Pre-IND 미팅)에서 H4 PK 특성(t½ ~0.5–1 hr)을 근거로 AUC₀₋₂₄가 AUC₀₋∞의 유효한 근사임을 확인받고 계획서에 해당 근거를 더 명확히 기술.

---

### [Minor-1] B.8 섹션명 "Assessment of Efficacy" — 주석의 용어 설명 과잉, 간결화 권고

- **심각도**: Minor
- **위치**: B.8 도입부 주석 박스
- **내용**: §B.8 도입부에 ICH E6(R3) 공식 섹션명 사용 이유를 상세히 설명하는 주석이 있다. 해당 설명 자체는 정확하며 IND 심사관이 오해할 소지를 차단하는 유익한 서술이다. 다만 박스 형식이 과도하게 눈에 띄어 공식 계획서 문체와 다소 이질적이다.
- **근거**: ICH E6(R3) Appendix B.8 "Assessment of Efficacy" [ICH, 2025-01-06]
- **권고**: 주석 박스는 유지하되 한 문장으로 압축: "본 섹션은 ICH E6(R3) Appendix B.8 공식 명칭("Assessment of Efficacy")을 따르며, 본 DDI 시험에서는 Clopidogrel 활성 대사체 H4의 노출(AUC, Cmax) GMR이 약리학적 상호작용 크기의 직접 측정치이므로 이 카테고리에 해당한다."

---

### [Minor-2] 생명윤리법 적용 제외 근거 — 잔여 검체 폐기 절차 미명시

- **심각도**: Minor
- **위치**: B.13.6
- **내용**: §B.13.6에서 생명윤리법 비대상 근거로 "잔여 검체를 보관하지 않는다"고 명시하였으나, **실제 폐기 절차(시점, 방법, 책임자)** 가 기술되지 않았다. IRB 심의 시 "검체를 보관하지 않는다"는 단순 선언보다 "분석 완료 후 N일 이내 XX방법으로 폐기하며 책임자 서명 기록"과 같은 절차적 근거가 더 설득력 있다.
- **근거**: 생명윤리 및 안전에 관한 법률 적용 비대상 판단의 IRB 설득력 강화 목적; `korea_bioethics_act.md` 체크리스트 3항 "폐기 절차" [생명윤리 및 안전에 관한 법률, 국회, 현행]
- **권고**: §B.13.6에 다음 문구 추가: "분석 완료 후 즉시(최대 30일 이내) 기관 SOP에 따라 혈장 시료를 폐기하며, 폐기 일자·방법·수량을 시험기관 약제부 또는 분석기관이 서명·기록한다. 이 폐기 기록은 Trial Master File에 보관한다."

---

### [Minor-3] B.14.2 KGCP 조항 번호 오기 가능성

- **심각도**: Minor
- **위치**: B.14.2 기록 보관
- **내용**: "시험 종료 후 최소 3년 (KGCP 제9조)"에서 "제9조"라는 조항 번호가 실제 KGCP 조문과 일치하는지 불확실하다. KGCP는 별표 4 형식으로 조항 구조가 다르며, "제9조"로 특정된 조문이 없을 수 있다.
- **근거**: KGCP (`korea_kgcp.md`) 원문은 "의약품등의 안전에 관한 규칙 [별표 4]" 형식으로 인용; 조항 번호 체계 불일치 가능
- **권고**: "KGCP 제9조" → "KGCP [의약품등의 안전에 관한 규칙 별표 4]"로 인용 형식 수정. 동시에 위 [Major-2]에 따라 보존 기간을 15년으로 정정.

---

### [Minor-4] B.6.3 MFDS 시험 수준 중단 보고 기한 — "48시간" 근거 미인용

- **심각도**: Minor
- **위치**: B.6.3
- **내용**: §B.6.3에 "의뢰자·규제기관·IRB 보고 (시험 수준 중단 시 MFDS 48시간 내 보고)"로 기재되어 있으나, MFDS 48시간 보고 요건의 근거 조항(약사법 시행규칙 또는 KGCP 조항)이 인용되지 않았다. 또한 KGCP/약사법에서 시험 수준 "일시 중지"에 대한 48시간 보고 의무 조항을 확인할 필요가 있다 — SAE/SUSAR와 달리 시험 일시 중지에 대한 구체적 시한은 별도 조항에 있을 수 있다.
- **근거**: 약사법 시행규칙 관련 조항 인용 불명; KGCP `korea_kgcp.md` §6.1에는 SAE 보고 기간만 명시 (7일/15일/24시간)
- **권고**: 48시간 보고 요건의 법령 조항을 확인하여 "[약사법 시행규칙 제XXX조, MFDS, 202X]" 형식으로 인용. 확인 불가 시 "[발행일 확인 필요]" 표시 후 담당 부처 사전 확인 권고.

---

### [Minor-5] B.16.2 임상시험 등록 — FSI 이전 등록이 ICMJE 권고지만 국내 의무 여부 미명시

- **심각도**: Minor
- **위치**: B.16.2
- **내용**: §B.16.2에 "FSI 이전 (ICMJE 권고)"으로 기재하였으나, CRIS(임상연구정보서비스) 등록이 국내 IRB 심의의 필수 조건인지 여부가 명시되지 않았다. 일부 IRB는 CRIS 등록증을 심의 서류로 요구하므로, 이를 명시하면 계획서 완성도가 높아진다.
- **근거**: 식품의약품안전처 고시(시험 등록 요건); 일부 기관 IRB 자체 규정
- **권고**: "CRIS 등록은 FSI 이전을 목표로 하며, 시험기관 IRB 요건에 따라 등록증을 IRB 심의 자료로 제출할 수 있다"는 문구 추가 검토.

---

## 종합 의견

**전반적 평가**: 본 계획서는 ICH E6(R3) Appendix B 16개 공식 섹션을 **모두 구비**하였으며 구조적 완성도가 높다. B.8 "Assessment of Efficacy" 섹션명도 ICH E6(R3) 공식 용어를 정확히 사용하였다. Declaration of Helsinki, KGCP, PIPA, 생명윤리법이 B.13에 명시적으로 인용되어 있다. DDI 가이드라인(FDA 2020, ICH M12 2024, MFDS 2015)이 표지와 설계 근거에 인용되어 있다. SAE 7일/15일 보고, 시험 종료 90일 보고, 피험자 보험 등 MFDS IND 요건의 핵심 항목도 기술되어 있다.

**주요 수정 필요 사항 (2건 — Major)**:
1. [Major-2] 기록 보존 기간: KGCP 규정대로 "15년"으로 정정 — IND 심사관이 즉시 지적할 수 있는 오류
2. [Major-3] 1차 평가변수: AUC₀₋₂₄를 AUC₀₋∞로 변경하거나 MFDS 사전 협의를 통해 근거 강화 — 가이드라인 정합성 문제

**추가 권고 사항 (1건 — Major)**:
- [Major-1] MFDS DDI 가이드라인 발행일 확인 및 정확한 인용

**Minor 사항(4건)**은 문서 품질 개선이며 규제 승인 자체를 저해하지 않는다.

**생명윤리법**: §B.13.6에서 CYP2C19 유전형 미검사·잔여 검체 미보관·2차 활용 없음을 근거로 생명윤리법 인체유래물 연구 비대상임을 명시하였다. 이 판단은 적절하다. 다만 IRB 심의 시 폐기 절차의 구체성을 보완(→ [Minor-2])하면 심의 설득력이 강화된다.

**ICH M12 인용**: ICH M12(2024)는 DDI 가이드라인 최신 국제 기준으로 표지와 §B.4.4에 인용되어 있다. 이는 현시점에서 적절하다 [ICH M12 Drug Interaction Studies, ICH, 2024].
