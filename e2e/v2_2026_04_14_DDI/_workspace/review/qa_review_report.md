# QA 통합 리뷰 보고서 — CLO-OME-DDI-001 Protocol v1.0

## 검토 요약

- **검토 일시**: 2026-04-14
- **대상 문서**: `_workspace/03_protocol_draft.md` (Clopidogrel-Omeprazole DDI, Phase 1)
- **참여 리뷰어 (5명, DDI 시험 — TS 참여 필수)**:
  - clinical-pharmacologist (CP)
  - regulatory-expert (REG)
  - biostatistician (BS)
  - clinician (CLIN)
  - translational-scientist (TS) — DDI 시험에서 필수 참여로 정상 통합됨
- **총 발견 사항 원본**: CP 9건 (M 3 + m 6 + info 1) / REG 7건 (M 3 + m 4) / BS 8건 (M 3 + m 5) / CLIN 11건 (M 4 + m 7) / TS 8건 (M 3 + m 5)
- **통합 후 최종 분류**: **Critical: 0건 | Major: 8건 | Minor: 16건**

---

## 분류 원칙

| 등급 | 정의 | 본 보고서 적용 |
|------|------|---------------|
| **Critical** | 규제 요건 미충족으로 IND 불합격, 대상자 안전 위험, 중대한 과학적 결함 | **0건** — ICH E6(R3) Appendix B 16개 섹션 모두 구비, 헬싱키·KGCP·PIPA·생명윤리법 모두 인용, 심각한 설계 결함 없음 |
| **Major** | 설계 정합성 이슈, 규제 가이드라인과 불일치, 분석 로직 모호, 주요 정보 누락으로 IND 심사관이 지적할 가능성이 높은 항목 | 8건 |
| **Minor** | 표현 개선, 문서 간 일관성 사소한 불일치, SAP 위임 가능 항목 | 16건 |

**★ 용어 정책 검증 (적용 결과)**:
- B.8 "Assessment of Efficacy" 사용에 대한 지적은 CP-info-01 (정보 등급), REG-Minor-1 (주석 간결화 권고)만 존재. 이들은 **Critical 등급 지적이 아니므로 하향 조정 대상이 없음**. CP-info-01은 정책 적합성 확인에 해당, REG-Minor-1은 문체 간결화 제안으로 Minor 유지.
- TS 리뷰는 DDI 시험 필수 참여자로 정상 통합되었으며, PG/PD 해석 한계·ICF Part 4 정합성 등 TS 고유 관점이 반영됨.

---

## Critical 사항

**없음.** 본 계획서는 IND 신청 구조 요건(ICH E6(R3) Appendix B 16개 섹션, 헬싱키/KGCP/PIPA/생명윤리법 인용, SAE 보고 기한, 피험자 보험 등)을 모두 충족하였다.

---

## Major 사항

### [M-1] CYP2C19 유전형 미검사 결정의 과학적·안전성·결과 해석 일관성 부재 (통합 이슈)

- **발견자**: CP-M-01, CLIN-Major-1, TS-Major-1, TS-Major-3
- **위치**: §B.2.4 (한계 §1), §B.5.3 (커스터마이징 결정), §B.8.2 (PD 평가), §B.9.1 (안전성 모니터링), §B.10.1 (CV% 75%), §B.10.5 (탐색적 분석)
- **내용 (4개 리뷰 통합)**:
  1. **[CP-M-01 — PK 통계적 모순]**: §B.2.4 한계에서 "EM/IM/PM 혼합 코호트"를 인정하면서 §B.10.1에서 CV%=75% (EM 문헌값 50–60%와 혼합 코호트 85–90%의 중간값)를 사용하는 것은 어느 가정에도 기반하지 않는 임의값이다. 예상 GMR=0.55도 EM 기반(Angiolillo 2011)에서 차용했다.
  2. **[CLIN-Major-1 — 안전성 모니터링 공백]**: PM 피험자 혼입(한국인 ~13–15%) 시 기저 PRU 매우 높아도 추가 모니터링 규정 없음. FDA Plavix 블랙박스 경고가 언급만 되고 실행 조치가 없다.
  3. **[TS-Major-1 — PD 결과 해석 방향성]**: 혼합 코호트에서 PRU 변화량이 NM 대비 과소 추정될 수 있으나 B.8.2 또는 B.10.5에 이 방향성이 명시 안 됨.
  4. **[TS-Major-3 — CPIC Level A 충돌 서술]**: CPIC Level A (임상 치료 권고) ≠ 본 시험(PK DDI 특성화 연구)의 구분이 IRB 심의를 위해 명확히 기술되지 않음.
- **근거**: Angiolillo 2011 (PMID 20844485); Lee 2022 (PMID 35034351) CPIC Level A; Simon 2015 (PMID 26071277) γ=7.04의 비선형 관계; FDA Plavix Black Box; ICH E6(R3) B.2 (설계 근거 명확화 요구)
- **권고 (통합)**:
  1. §B.10.1 CV% 설정 근거를 재정렬: 혼합 코호트 가정 유지 시 CV% 85%로 상향 및 n 재산출, 또는 "건강인 EM 기준 50–60% + 불확실성 완충 15%포인트 = 75%"와 같이 근거를 명시. 이상적으로는 Pre-IND 단계에서 MFDS와 합의.
  2. §B.2.4 한계 §1에 다음 한계 추가: "PM 피험자 포함 시 기저 H4 노출이 낮아 Omeprazole 추가 억제의 절대적 효과가 NM과 다르게 나타날 수 있으며, GMR 추정치가 혼합 코호트 평균값으로 해석되어야 함"
  3. §B.9.1에 "기저 PRU > 230 (HPR 기준 이상)인 피험자에 대해 PI는 CYP2C19 유전형 확인 여부를 검토한다" 유연 조항 추가 (CLIN-Major-1)
  4. §B.5.3 또는 §B.2.4 한계 §1에 CPIC 범위·본 시험 범위 구분 명시: "CPIC Level A 및 FDA Black Box는 임상 치료 환경 권고이며, 건강한 지원자 대상 DDI 크기 특성화 연구에는 직접 적용되지 않음"
  5. §B.10.5 탐색적 분석에 "사후 genotype-stratified 분석은 잔여 검체 미보관으로 불가함"을 명시 (TS-Minor-8과 통합)

---

### [M-2] MFDS 기록 보존 기간 오류 — 3년 vs KGCP 15년

- **발견자**: REG-Major-2
- **위치**: §B.14.2 기록 보관 (line 1050)
- **내용**: 계획서는 "시험 종료 후 최소 3년 (KGCP 제9조)"으로 기재하고 있으나, KGCP (의약품등의 안전에 관한 규칙 별표 4, MFDS 2019-12-06)는 Essential Documents (동의서·CRF·원자료·프로토콜)의 보존 기간을 **시험 완료 또는 조기 중단 후 최소 15년**으로 규정한다. 이는 IND 심사관이 즉시 지적 가능한 명백한 규정 불일치이다. 또한 "제9조"라는 조항 번호도 KGCP의 "별표 4" 구조와 일치하지 않을 가능성이 있다.
- **근거**: KGCP `.claude/references/guidelines/regulations/korea_kgcp.md` §7.1 "시험 완료 또는 조기 중단 후 최소 **15년**" [의약품등의 안전에 관한 규칙 별표 4, MFDS, 2019-12-06]
- **권고**: §B.14.2를 다음 구조로 수정:
  - Essential Documents: 시험 완료 또는 조기 중단 후 **최소 15년** (KGCP)
  - 의료기관 의무기록: 의료법에 따라 10년 (별도 법률)
  - 인용 형식: "KGCP 제9조" → "[의약품등의 안전에 관한 규칙 별표 4]"

---

### [M-3] MFDS DDI 가이드라인 1차 평가변수 불일치 — AUC₀₋₂₄ vs AUC₀₋∞

- **발견자**: REG-Major-3 (CP-m-03과 부분 연계)
- **위치**: §B.8.1, §B.10.1, §B.3.1
- **내용**: 계획서는 1차 평가변수를 **AUC₀₋₂₄**로 지정하였으나, MFDS DDI 가이드라인(2015), FDA DDI Guidance(2020), ICH M12(2024)는 **AUC₀₋∞**를 1차로 명시한다. §B.8.1에서 "H4 t½ ≪ 24 hr이므로 AUC₀₋₂₄ ≈ AUC₀₋∞로 근사"라는 과학적 근거가 기술되어 있으나(CP-m-03에서도 H4에 대해 이 근거는 타당하다고 확인), SR26334 t½ 7.2–7.6 hr에 대한 24hr AUC 커버리지 명시(CP-m-03)나 가이드라인과의 공식적 정합성 확인이 불완전하다.
- **근거**: MFDS DDI 가이드라인 §4; FDA Clinical DDI Guidance 2020; ICH M12 2024; DDI Cross-Agency 비교표
- **권고 (두 옵션)**:
  1. **(권장)** 1차 평가변수를 AUC₀₋∞로 변경하고, AUC₀₋₂₄는 2차 파라미터로 이동. 24 hr 채혈로도 λz 추정 가능하므로 AUC₀₋∞ = AUC₀₋ₜ + Cₜ/λz로 산출.
  2. **(대안)** AUC₀₋₂₄ 유지 시 Pre-IND 미팅에서 MFDS와 합의하고 §B.8.1에 "SR26334 t½ 7.2–7.6 hr에 대해 24 hr은 3×t½로 AUC₀₋₂₄ / AUC₀₋∞ ≥ 87.5% 커버리지" (CP-m-03 권고 통합) 및 합의 근거를 명시.

---

### [M-4] H4 AUC₀₋₂₄ 및 Cmax 공동 1차 평가변수의 위계·다중성 처리 미기술

- **발견자**: BS-Major-2
- **위치**: §B.8.1, §B.10.3 (line 771)
- **내용**: §B.8.1과 §B.10.3에서 H4 AUC₀₋₂₄와 Cmax를 모두 1차 평가변수로 지정하고 각각 독립 분석을 수행한다고 명시한다. 그러나 다음이 누락되어 있다:
  - **판정 로직**: 두 지표 모두 경계를 벗어나야 DDI 판정(conjunctive)인지, 어느 하나만 벗어나면 DDI 판정(disjunctive)인지 미명시
  - **다중성 처리**: α=0.10 양측 두 검정 수행 시 FWER 증가 처리 방안 부재
  - **Sample size 근거**: n=20 계산은 AUC₀₋₂₄ 단일 지표 기반으로 수행되었으나, Cmax에도 동일 검정력이 확보되는지 확인 없음
- **근거**: ICH E9 §5.5; FDA DDI Guidance 2020; MFDS DDI 가이드라인 §4; ICH E6(R3) Appendix B.10
- **권고**:
  1. AUC₀₋₂₄를 주된 1차, Cmax를 공동 1차(co-primary) 또는 2차로 위계 부여
  2. 판정 로직을 사전 명시: 예 "AUC₀₋₂₄ CI가 경계를 벗어나면 1차 결론, Cmax는 지지 증거" 또는 "두 지표 모두 벗어날 때 DDI 양성"
  3. Sample size 계산이 AUC₀₋₂₄ 기반임을 명시

---

### [M-5] GMR=0.60 시나리오에서 검정력 0.72 — 사전 대응 계획 부재

- **발견자**: BS-Major-1
- **위치**: §B.10.1 민감도 분석 결과 표 및 하단 주의 문구
- **내용**: Angiolillo 2011 (PMID 20844485) 보고 GMR 범위 0.53–0.60에서 상한값 0.60은 문헌적으로 현실적인 시나리오이다. 이 경우 n=20 설계의 검정력은 0.72로 표준 0.80에 미달한다. 계획서가 이 위험을 인지하고 있으나 대응 계획(중간 검정력 재추정, 추가 등록, pre-specified 하한 합의)이 없다. ICH E8(R1) §3.1은 "연구 목적에 적절한 검정력 보유"를 요구한다.
- **근거**: Angiolillo 2011 (PMID 20844485); ICH E8(R1) §3.1; FDA/MFDS 표준 검정력 0.80
- **권고 (택1)**:
  1. §B.10.1 및 §B.2.4 한계에 "GMR=0.60 시나리오에서 검정력 0.72는 본 시험의 수용 가능 하한으로 사전 합의" 명시
  2. 등록 목표를 n=22 (검정력 0.80 충족)로 상향 조정, n=20은 최소 평가 가능 수로 재정의

---

### [M-6] Fixed-sequence ANOVA 모형의 SAS 구문 오류 및 1차 분석법 위계 모호

- **발견자**: BS-Major-3
- **위치**: §B.10.3 line 753–761
- **내용**: 계획서에 기술된 "MODEL ln(AUC) = PERIOD / SOLUTION; RANDOM SUBJECT;"는 SAS PROC MIXED 문법 오류이다. 또한 "Paired t-test 또는 등가 ANOVA"에서 어느 것이 1차 분석법인지 위계가 불분명하다. Fixed-sequence에서 sequence 항 제거 근거도 §B.10.3에 부재하다.
- **근거**: ICH E6(R3) B.10 (분석 방법의 명확한 기술); ICH E9 §5.1
- **권고**:
  1. SAS 코드를 올바른 문법으로 수정:
     ```
     PROC MIXED DATA=pkdata;
       CLASS SUBJECT PERIOD;
       MODEL LN_AUC = PERIOD / SOLUTION DDFM=SATTERTHWAITE;
       RANDOM SUBJECT;
       ESTIMATE 'Period 2 vs Period 1' PERIOD -1 1 / CL ALPHA=0.10;
     RUN;
     ```
  2. Paired t-test를 1차로 지정하고 ANOVA를 지지 확인용으로 명시 (또는 그 반대 결정 후 근거 기재)
  3. "Fixed-sequence에서 sequence 항은 단일 sequence 존재로 제거"를 §B.10.3에 명시

---

### [M-7] Omeprazole 정상상태 확인 및 정상상태 PK 조건 서술 불완전

- **발견자**: CP-M-02, CP-M-03
- **위치**: §B.4.4 (line 265–), §B.8.1
- **내용 (2개 발견사항 통합)**:
  - **[CP-M-02]**: §B.4.4는 "7일 이내 정상상태 최대 저해 도달 (Ogilvie 2011)"로만 기술하나, (1) pre-treatment 후 실제 최대 저해 도달 확인 방법 미명시, (2) D31 시점은 Omeprazole D20–D31 = 12일차 투여 상태임이 본문에 명시되지 않음, (3) EM 개인차로 일부는 10일 이상 필요 가능성.
  - **[CP-M-03]**: §B.8.1에서 "Period 1 D5 vs Period 2 D31" 비교가 모두 정상상태 PK 조건임이 명시적으로 기술되지 않음.
- **근거**: Ogilvie 2011 (PMID 21795468); FDA DDI Guidance 2020 (perpetrator 정상상태 요건); ICH M12 2024
- **권고**:
  1. §B.4.4에 "Omeprazole D20–D31까지 총 12일 투여, D27 Clopidogrel 로딩 전 7일 단독 pre-treatment는 Ogilvie 2011 기반 CYP2C19 MDI 최대화에 이론적으로 충분. D26 또는 D27 pre-dose 시점의 Omeprazole trough 농도로 정상상태 간접 확인 가능" 추가
  2. §B.8.1에 "D5 = Clopidogrel 300 mg 로딩 + D2–5(4일 유지)의 정상상태 평가, D31 = 동일 조건 + Omeprazole D12차 투여 시점으로 두 Period가 대칭적 정상상태 PK 조건" 명시

---

### [M-8] TTP 모니터링 불완전 — LDH 선제 측정·말초혈구도말·Haptoglobin 누락 및 임계값 불일치

- **발견자**: CLIN-Major-2, CLIN-Major-3, CLIN-Major-4
- **위치**: §B.6.1 (중지 기준), §B.9.1 (모니터링 표)
- **내용 (3개 발견사항 통합)**:
  - **LDH 선제 측정 부재**: Bennett 2000에 따르면 TTP는 투여 2주 이내 발병(11례 중 10례 14일 이내). LDH는 혈소판감소 선행 지표이므로 "이상 시 즉시"만으로는 조기 발견 불가. D1/D5/D27에 정기 측정 필요.
  - **LDH 임계값 불일치**: §B.6.1에는 "LDH >3× ULN + 혈소판감소"이나 참조 파일 SAE_cases_clopidogrel.md는 ">2× ULN"으로 기재되어 있어 문서 간 불일치.
  - **말초혈구도말·Haptoglobin 미기재**: TTP 진단 확정에 필수인 schistocyte 확인과 용혈 마커 haptoglobin이 B.9.1 모니터링 표와 CMP 목록에서 누락. B.6.1 중지 기준 진단 절차에만 schistocyte 언급.
- **근거**: Bennett 2000 (PMID 10852999); SAE_cases_clopidogrel.md §1 TTP 중지 기준; safety_monitoring_rationale.md §1-5
- **권고**:
  1. B.9.1 LDH 측정 시점에 D1, D5, D27 정기 측정 추가 (Bennett 2000 위험 기간 선제 포착)
  2. B.6.1 LDH 임계값을 "LDH >2× ULN + 혈소판감소" 또는 ">3× ULN"으로 SAE 참조 파일과 일치시키기
  3. B.9.1에 "혈소판 <100×10⁹/L 또는 기저치 대비 >25% 감소 + Hgb 감소 시 즉시 말초혈구도말(schistocyte) + haptoglobin + LDH" 조건부 조항 추가

---

## Minor 사항

### [m-1] 채혈 시점 설계 원칙 기술 보완 — 소실기 구간 설명

- **발견자**: CP-m-01
- **위치**: §B.8.4 채혈 시점 설계 원칙
- **권고**: "4 hr 이후 시점(6, 8, 12, 24 hr)은 H4 정량에는 기여하지 않으나 SR26334 소실기(t½ 7.2–7.6 hr) 및 Clopidogrel 모체 측정을 위해 유지" 문구 추가

### [m-2] Washout 14일 근거 표의 Omeprazole 계산식 오기

- **발견자**: CP-m-02
- **위치**: §B.4.4 Washout 14일 근거 표 (line 215)
- **권고**: "2^(-336/1) ≈ 0%"를 "EM t½ ~0.5–1 hr → 14일 = 약 336–672 반감기 경과 → 잔류율 ≈ 0%"로 교정하고 Washout 핵심 인자를 "CYP2C19 효소 재합성(3–7일) + 혈소판 수명(10일)"로 하단 주석

### [m-3] SR26334 AUC₀₋₂₄ 커버리지 명시

- **발견자**: CP-m-03
- **위치**: §B.8.1 (절단 AUC 섹션) 또는 §B.8.2
- **권고**: "SR26334 t½ 7.2–7.6 hr에 대해 24 hr은 3×t½ → AUC₀₋₂₄ / AUC₀₋∞ ≥ ~87.5%" 추가. M-3 해결 시 연계 반영.

### [m-4] BMV/ISR 비율 및 BMAP SOP 거부 기준 명시

- **발견자**: CP-m-04
- **위치**: §B.8.5, §B.12.1
- **권고**:
  - "BMV는 FSI 이전 완료"
  - "ISR: 총 incurred sample의 5–10%, 차이 ±20% 이내 (FDA/MFDS BMV 기준)"
  - "BMAP 첨가 5분 초과 시 시료 reject"

### [m-5] 총 채혈량 표 일관성

- **발견자**: CP-m-05
- **위치**: §B.8.4 vs 부록 B.4
- **권고**: 두 섹션의 항목 분류 및 채혈량 산출 통일 (스크리닝 ~50 mL + 안전성 검사 ~105 mL 방식으로)

### [m-6] Omeprazole 채혈 목적 명시

- **발견자**: CP-m-06
- **위치**: §B.8.4
- **권고**: Omeprazole 채혈 소제목에 "(보조 측정, 2차 목적 §3)" 표기

### [CP-info-01] B.8 "Assessment of Efficacy" 용어 정책 적합성 (**지적 없음**)

- **발견자**: CP-info-01 (정보)
- **위치**: §B.8
- **내용**: Phase 1 DDI 시험에서 H4 GMR이 약리학적 효과 크기 측정치이므로 ICH E6(R3) Appendix B.8 공식 섹션명 "Assessment of Efficacy" 사용은 용어 가이드에 부합함. 수정 불필요. REG-Minor-1과 연계 (주석 간결화 선택 사항).

### [m-7] B.8 "Assessment of Efficacy" 주석 간결화

- **발견자**: REG-Minor-1
- **위치**: §B.8 도입부 주석 박스
- **권고**: 주석을 한 문장으로 압축: "본 섹션은 ICH E6(R3) Appendix B.8 공식 명칭을 따르며, 본 DDI 시험에서 H4 AUC/Cmax GMR이 약리학적 상호작용 크기의 직접 측정치이므로 이 카테고리에 해당한다"

### [m-8] MFDS DDI 가이드라인 발행일 확인

- **발견자**: REG-Major-1 → **Minor로 하향** (실제로는 인용 정확성 개선 항목이며 IND 승인 자체를 저해하지 않음)
- **위치**: 표지 "규제 준거", §B.4.4
- **권고**: MFDS 홈페이지(`mfds.go.kr/brd/m_218`)에서 최신 DDI 가이드라인 발행일 확인 후 "[식약처 고시 제2015-xx호, 연월일]" 형식으로 정확히 기재. 개정판 존재 시 교체.
- **QA 판단**: IND 심사관이 이를 근거로 반려하는 경우는 드물며, Minor로 하향함. 원 REG-Major-1의 우려(최신판 누락 위험)는 유효하므로 수정 권고는 유지.

### [m-9] 생명윤리법 비대상 근거 — 폐기 절차 구체화

- **발견자**: REG-Minor-2
- **위치**: §B.13.6
- **권고**: "분석 완료 후 즉시(최대 30일) 기관 SOP 따라 폐기. 폐기 일자·방법·수량 기록. Trial Master File 보관" 추가

### [m-10] 90% CI 판정 기준 방향성 명시

- **발견자**: BS-Minor-1
- **위치**: §B.10.3
- **권고**: "CI 상한 < 80% 또는 하한 > 125%이면 DDI 양성. 본 시험 목적상 전자(H4 노출 감소)가 임상적으로 유의" 명시

### [m-11] ITT 정의의 Crossover 맥락 재검토

- **발견자**: BS-Minor-2
- **위치**: §B.10.2
- **권고**: "ITT = 두 period 모두 최소 1회 투여받은 피험자 (paired comparison 가능)"로 수정

### [m-12] Tmax Wilcoxon 결과에 Hodges-Lehmann 추정량 추가

- **발견자**: BS-Minor-3
- **위치**: §B.10.4
- **권고**: "Tmax: Wilcoxon signed-rank p-value + Hodges-Lehmann median difference + 95% CI 보고"

### [m-13] 공변량 ANCOVA 및 Outlier 처리의 SAP 위임 문구 추가

- **발견자**: BS-Minor-4, BS-Minor-5
- **위치**: §B.10.5
- **권고**: "공변량 목록·적용 outcome·선택 기준은 SAP에서 사전 명세. Outlier 기본 방법은 Grubbs test (α=0.05), ROUT는 보조"

### [m-14] Fixed-sequence 무작위화 항목 B.10 요약

- **발견자**: BS 일관성 점검표
- **위치**: §B.10
- **권고**: "본 시험은 Fixed-sequence로 무작위 배정 미수행. 모든 피험자 동일 sequence (Period 1 단독 → Period 2 병용)" 한 줄 추가

### [m-15] 임상 세부 사항 개선

- **발견자**: CLIN-Minor-1~7 (통합)
- **위치**: §B.5.2 (16, 17, 18번), §B.7.6, §B.9.1, 부록 A
- **권고 (항목별)**:
  - 제외 기준 16: "자발성 출혈, 외상·수술에 비례하지 않는 출혈 지속, 두개내·GI·안구내·관절강 출혈 병력 또는 혈소판 기능 이상 진단 과거력" (CLIN-Minor-1)
  - 제외 기준 17: 상한 >450×10⁹/L 근거로 "혈전 위험 증가 및 기저 염증성 질환 반영 가능" 추가 (CLIN-Minor-2)
  - 제외 기준 18: PPI 14일 기간을 "CYP2C19 MDI 회복(3–7일)의 안전 여유" 근거로 보완 (CLIN-Minor-3)
  - §B.9.1 활력징후: "투여 후 1, 2, 4, 8 hr (또는 PK 채혈 시점과 동기화)" 구체화 (CLIN-Minor-4)
  - §B.7.6 아나필락시스: "에피네프린 0.3–0.5 mg 근육 주사 (허벅지 전외측) + 응급실 이송" 명시 (CLIN-Minor-5)
  - 출혈 문진 도구: WHO Bleeding Scale로 단일화 + 추가 체크리스트 (CLIN-Minor-6)
  - D-1 입원 + D20–D26 자택 복용기 연락 절차: 부록 A와 §B.9에 명시 (CLIN-Minor-7)

### [m-16] TS 세부 사항 개선

- **발견자**: TS-Minor-4~8 (통합)
- **위치**: §B.8.2, §B.8.3, §B.8.5, §B.13.4, §B.13.6
- **권고 (항목별)**:
  - LTA SOP 요건: "채혈 후 2시간 이내 PRP 제조 (150g × 10분), 37°C, ADP 10 μmol/L" §B.8.5에 명시 (TS-Minor-4)
  - Sigmoid Emax 독립변수: "H4 AUC₀₋₂₄ 기본, Cmax 탐색적 대안" 명확화, Simon 2015 파라미터가 AUC 기반임을 명시 (TS-Minor-5)
  - PK tube 유형: 부록 B 채혈표에 "EDTA / sodium citrate" tube 명시 (TS-Minor-6)
  - ICF Part 4 근거: "H4 대사체 분석 동의는 생명윤리법이 아닌 ICH E6(R3)/KGCP 원칙 기반" 명시 (TS-Minor-7)
  - §B.10.5 또는 §B.13.6: "사후 유전형 분석은 잔여 검체 미보관으로 불가. 필요 시 별도 연구 필요" 명시 (TS-Minor-8) — M-1 권고 §5와 통합

### [m-17] PRU 기저값 정의 및 D14 Washout 시점 PRU 측정 고려

- **발견자**: TS-Major-2 → **Minor로 하향 조정**
- **위치**: §B.8.2, 부록 A
- **내용**: D1 pre-dose PRU가 "Clopidogrel 최초 투여 직전 진정 기저"임이 명시되지 않음. Washout 완료 시점(D14) 또는 Period 2 시작 시점(D26)의 PRU 측정이 선택적으로 추가되면 두 period의 baseline 동등성 확인이 강화됨.
- **QA 판단**: 진정 기저값의 명시는 필수 수정(원 Major)이나, D14/D26 PRU 측정 추가는 선택 제안이므로 전체를 Minor로 통합.
- **권고**: §B.8.2에 "D1 pre-dose = Clopidogrel 최초 투여 직전 진정 기저" 명시. D14 PRU 측정은 탐색적 옵션으로 제안 (SAP 또는 v2.0 개정 고려).

### [m-18] B.6.3 MFDS 시험 수준 중단 48시간 보고 근거 인용

- **발견자**: REG-Minor-4
- **위치**: §B.6.3
- **권고**: 48시간 보고 요건의 약사법 시행규칙 조항 확인 후 인용. 조항 확인 불가 시 "[발행일 확인 필요]" 임시 표기

### [m-19] B.14.2 KGCP 조항 번호 인용 정정

- **발견자**: REG-Minor-3
- **위치**: §B.14.2
- **권고**: "KGCP 제9조" → "[의약품등의 안전에 관한 규칙 별표 4]"로 수정 (M-2와 연동 반영)

### [m-20] B.16.2 CRIS 등록의 IRB 연관성 명시

- **발견자**: REG-Minor-5
- **위치**: §B.16.2
- **권고**: "CRIS 등록은 FSI 이전을 목표로 하며, 시험기관 IRB 요건에 따라 등록증을 IRB 심의 자료로 제출할 수 있다" 추가

---

## 상충 의견 (Conflicting Opinions)

### [상충-1] M-3 (1차 평가변수: AUC₀₋₂₄ vs AUC₀₋∞)

- **REG-Major-3**: MFDS/FDA/ICH M12 가이드라인은 AUC₀₋∞를 1차로 요구 → **AUC₀₋∞로 변경 권장**
- **CP-m-03**: H4 t½ ≪ 24 hr이므로 AUC₀₋₂₄ ≈ AUC₀₋∞ 근사 타당, SR26334 24hr 커버리지 87.5%도 충분 → **AUC₀₋₂₄ 유지 시 근거 강화면 수용 가능**
- **QA 판단**: 양쪽 근거 모두 유효. 과학적으로는 CP 의견이 타당하나, 규제 심사 관례상 REG 권장이 안전. **사용자 판단 필요** — Pre-IND 미팅 여부에 따라 결정 권장. Pre-IND를 실시하면 AUC₀₋₂₄ 유지 + 과학적 근거 강화(옵션 2), 실시하지 않으면 AUC₀₋∞로 변경(옵션 1)이 안전.

### [상충-2] M-1 CV% 설정 (75% 유지 vs 재설정)

- **CP-M-01**: 현행 75%는 EM 50–60%와 혼합 85–90% 중간의 임의값 → **EM 기준 n=13 또는 혼합 기준 n=30+ 중 선택**
- **설계 현실**: 등록 부담 고려 시 혼합 가정으로 n 대폭 증가가 비현실적이며, 현행 설계(n=20)는 실용적 타협안
- **QA 판단**: 설계 변경보다 **근거 서술 강화**가 현실적. 권고 통합안: "건강인 EM 문헌값(50–60%)에 PM/IM 혼합으로 인한 불확실성 완충 15%포인트 상향 = 75% 보수적 설정"으로 §B.10.1에 명시.

### [상충-3] 기타 리뷰 간 상충 없음

---

## Synopsis–Protocol 일관성 점검표

| 비교 항목 | Synopsis (v1.0) | Protocol (v1.0) | 일치 여부 |
|----------|-----------------|------------------|---------|
| 시험명 | Clopidogrel-Omeprazole DDI (Fixed-sequence 2-period crossover) | 동일 | **일치** |
| 시험 유형 | Phase 1 DDI | 동일 | **일치** |
| 1차 평가변수 | H4 AUC₀₋₂₄, Cmax GMR + 90% CI | 동일 (AUC₀₋₂₄) | **일치** (M-3 공통 이슈) |
| 비교 판정 기준 | 90% CI 80–125% 범위 이탈 | 동일 | **일치** |
| 시험 설계 | Fixed-sequence 2-period crossover, open-label | 동일 | **일치** |
| Washout | 14일 | 14일 | **일치** |
| Omeprazole pre-treatment | D20–D26 (7일) | D20–D26 (7일) | **일치** |
| Clopidogrel 투여 | 300 mg 로딩 + 75 mg × 4일 유지 (D1, D27) | 동일 | **일치** |
| Period 1 PK 평가일 | D5 | D5 | **일치** |
| Period 2 PK 평가일 | D31 | D31 | **일치** |
| 대상자 수 (등록) | 20명 | 20명 | **일치** |
| 대상자 수 (완료 목표) | 17명 | 17명 | **일치** |
| CV% 가정 | 75% | 75% | **일치** (M-1 공통 이슈) |
| 예상 GMR | 0.55 | 0.55 | **일치** |
| 탈락률 | 15% | 15% | **일치** |
| α / 검정력 | 0.10 양측 / 0.80 | 동일 | **일치** |
| 통계 프레임워크 | DDI detection (TOST 미적용) | 동일 | **일치** |
| 1차 분석 방법 | Paired t-test (또는 등가 ANOVA) | 동일 (M-6 모호성 공통) | **일치** |
| PP 1차, ITT sensitivity | 명시 | 명시 | **일치** |
| PD 1순위 | VerifyNow PRU | VerifyNow PRU | **일치** |
| PD 2순위 | LTA %IPA (ADP 10 μmol/L) | 동일 | **일치** |
| PK 채혈 시점 (D5/D31) | 13 포인트 (0–24 hr) | 동일 | **일치** |
| Omeprazole 채혈 (D31) | 11 포인트 | 동일 | **일치** |
| 총 채혈량 | ≤ 400 mL | ≤ 400 mL | **일치** (m-5 항목 분류 불일치) |
| CYP2C19 유전형 검사 | 미시행 | 미시행 | **일치** |
| 잔여 검체 보관 | 없음 | 없음 | **일치** |
| 생명윤리법 적용 | 비대상 | 비대상 | **일치** |
| 시험 기간 | 약 12–18개월 | 동일 | **일치** |

**결론**: Synopsis와 Protocol 간 주요 설계 결정은 전부 정합. 공통 이슈(M-1 CV%, M-3 AUC 정의, M-6 분석법)는 Synopsis 수준의 결정이 Protocol로 전파된 것으로, 두 문서 모두 함께 수정해야 일관성 유지 가능.

---

## 규제 체크리스트 결과

### ICH E6(R3) Appendix B 16개 섹션 체크리스트

> 근거: `.claude/references/guidelines/ich/e6_r3_full/07_appendix_b_protocol.md` (ICH E6(R3) 2025-01-06 Step 4 Final)

| # | 섹션 (공식 명칭) | 존재 | 충실도 | 비고 |
|---|-------|:---:|:---:|------|
| B.1 | General Information | ✓ | ★★★ | 프로토콜 번호·버전·날짜·의뢰자·서명권한자 (IND 제출 전 placeholder 확정 필요) |
| B.2 | Background Information | ✓ | ★★★ | 시험약·병용약 설명, 비임상/임상 소견, 위험·이익 평가, 투여 근거, GCP 준수 선언 |
| B.3 | Trial Objectives and Purpose | ✓ | ★★★ | 1차·2차·탐색적 목적 명시. Estimand 미정의는 DDI 시험 특성상 수용 가능 (ICH E9(R1) 적용 불필요) |
| B.4 | Trial Design | ✓ | ★★☆ | 설계 개략도, 평가변수, 일정 포함. **M-7 (정상상태 확인 절차 보완 필요)** |
| B.5 | Selection of Participants | ✓ | ★★★ | 선정 6 + 제외 18항목 (일부 표현 개선 — m-15) |
| B.6 | Discontinuation of Trial Intervention | ✓ | ★★☆ | 중단 기준·추적관찰·데이터 처리. **M-8 LDH 임계값 불일치, m-18 48시간 보고 조항 근거 보완** |
| B.7 | Treatment and Interventions | ✓ | ★★★ | 투여 절차·약물관리·허용/금지 병용약. **m-15 응급처치 구체화 권고** |
| B.8 | **Assessment of Efficacy** | ✓ | ★★☆ | ICH E6(R3) 공식 섹션명 사용, Phase 1 용어 정책에 부합. **M-3 AUC 정의 정합성, M-4 1차 변수 위계, M-7 정상상태 명시, m-7 주석 간결화** |
| B.9 | Assessment of Safety | ✓ | ★★☆ | AE/SAE 정의·보고·추적관찰. **M-8 TTP 모니터링 보완 필요** |
| B.10 | Statistical Considerations | ✓ | ★★☆ | 분석법·sample size·유의수준·분석집단·결측치 처리. **M-4/M-5/M-6 여러 이슈 존재** |
| B.11 | Direct Access to Source Records | ✓ | ★★★ | 의뢰자·MFDS·IRB 접근 권한 명시 |
| B.12 | Quality Control and Quality Assurance | ✓ | ★★★ | QC/QA, 모니터링, 감사, 규제 실사. **m-4 BMV/ISR 기준 명시 권고** |
| B.13 | Ethics | ✓ | ★★★ | 헬싱키, ICH E6(R3), KGCP, 약사법, PIPA, 생명윤리법 모두 인용. **m-9 폐기 절차 구체화 권고** |
| B.14 | Data Handling and Record Keeping | ✓ | ★★☆ | 자료 관리·원자료 식별. **M-2 기록 보존 15년 정정 필수** |
| B.15 | Financing and Insurance | ✓ | ★★★ | 재정 및 보험 별도 섹션, 피험자 보험(약사법 시행규칙 제24조) 인용 |
| B.16 | Publication Policy | ✓ | ★★★ | 공표 정책, ICMJE·CRIS 등록. **m-20 IRB 연관성 명시 권고** |

**결론**: **16개 섹션 모두 구비. 구조적 완결성은 충족.** 내용적 보완이 필요한 섹션은 B.4, B.6, B.8, B.9, B.10, B.14 등 6개 섹션.

### MFDS 요건

| 항목 | 충족 | 비고 |
|------|:---:|------|
| KGCP 준수 선언 | ✓ | §B.13, 표지 |
| 약사법 제34조 IND 절차 | ✓ | §B.13.2 |
| 피험자 보험 (약사법 시행규칙 제24조) | ✓ | §B.15 |
| SAE 보고 (SUSAR 7일/15일, 시험 종료 90일) | ✓ | §B.9.3 |
| Essential Documents 보존 (15년) | **✗** | **M-2 — 현행 3년 표기, 정정 필요** |
| MFDS 가이드라인 발행일 정확 인용 | △ | m-8 — 2015 표기 확인 필요 |
| 1차 평가변수 MFDS DDI 가이드라인 정합성 | △ | M-3 — AUC₀₋∞ vs AUC₀₋₂₄ |

### PIPA 체크리스트

| # | 항목 | 충족 | 비고 |
|---|------|:---:|------|
| 1 | 개인정보 수집 항목 명시 | ✓ | §B.13 (ICF 별도 동의서 참조) |
| 2 | 수집·이용 목적 명시 | ✓ | §B.13 |
| 3 | 제3자 제공 대상 및 목적 | ✓ | §B.13 (의뢰자·MFDS·IRB) |
| 4 | 보유 기간 | △ | §B.14.2 연동, M-2 해결 시 자동 반영 |
| 5 | 동의 거부 권리 및 불이익 | ✓ | §B.13 |
| 6 | 별도 동의서 존재 | ✓ | ICF Part 2 (개인정보 동의서 별도) |

### 생명윤리법 체크리스트 (비대상 판정)

| # | 항목 | 적용 | 비고 |
|---|------|:---:|------|
| — | 인체유래물 연구 해당 여부 | **비대상** | §B.13.6 — CYP2C19 유전형 미검사, 잔여 검체 미보관, 2차 활용 없음 (판정 적절) |
| — | 폐기 절차 구체화 | △ | m-9 — IRB 설득력 강화 권고 |

---

## 수정 우선순위 권고 (Remediation Priority)

| 우선순위 | 사항 | 처리 방침 |
|---------|------|----------|
| **즉시 수정 (IND 제출 전 필수)** | M-2 기록 보존 15년, M-8 TTP 모니터링·임계값 정정 | Critical은 아니나 IND 심사관이 즉시 지적. **1차 수정 사이클 필수** |
| **1차 수정 사이클 (v1.1)** | M-1, M-3, M-4, M-5, M-6, M-7 | IRB/MFDS 심의 대비. 과학적 근거·분석 로직 강화 |
| **SAP에 위임 가능** | m-10, m-12, m-13, m-14 | SAP 작성 시 반영 |
| **v2.0 또는 다음 개정** | m-1, m-2, m-3, m-4, m-5, m-6, m-7, m-8, m-9, m-11, m-15, m-16, m-17, m-18, m-19, m-20 | 문서 품질 개선, 승인 저해 없음 |

---

## MFDS IND 제출 적합성 종합 평가

### 판정: **"수정 후 제출 가능"** (Acceptable with Revisions)

**근거**:
1. **구조적 완결성**: ICH E6(R3) Appendix B 16개 섹션 모두 구비
2. **규제 준수**: 헬싱키, KGCP, 약사법 제34조, PIPA, 생명윤리법이 모두 명시 인용. 피험자 보험, SAE 보고 체계, 기관 IRB 심의 절차 완비
3. **과학적 타당성**: DDI 설계(Fixed-sequence), Washout(14일), PK 채혈 시점, 용량 근거(라벨 기준)가 공개 문헌·가이드라인 근거와 정합
4. **Critical 결함 없음**: 대상자 안전을 즉각 위협하는 결함, IND 반려 사유에 해당하는 규제 불합격 요소, 설계상 치명적 오류 모두 부재

### 필수 수정 사항 (최우선 8건 — Major)

M-1 (CYP2C19 유전형 결정 일관성), M-2 (기록 보존 15년), M-3 (AUC 정의 정합성), M-4 (1차 변수 위계), M-5 (검정력 0.72 대응 계획), M-6 (ANOVA 구문 오류), M-7 (정상상태 조건 서술), M-8 (TTP 모니터링)

### 예상 수정 기간

- **1차 수정 사이클**: 1–2주 (protocol-writer 자동 수정 후 재리뷰)
- **Pre-IND 미팅 (선택)**: M-3 상충 해결을 위해 2–4주 추가 권장
- **수정 완료 후 IND 제출 가능 시점**: 2–6주 내

### 판정 재확인

- ✗ 즉시 제출 가능 (Ready for Immediate Submission)
- ✓ **수정 후 제출 가능 (Acceptable with Revisions)** ← **본 판정**
- ✗ 전면 재작성 필요 (Requires Major Rework)

---

## 종합 의견

본 계획서 CLO-OME-DDI-001 v1.0은 **Phase 1 DDI 시험으로서 구조적·규제적 완성도가 높으며**, ICH E6(R3) 최신판(2025-01-06) Appendix B 16개 섹션 공식 구조를 완전히 따르고 있다. B.8 "Assessment of Efficacy" 공식 섹션명의 Phase 1 DDI 맥락 사용은 용어 가이드에 부합하며, 해당 주석에서 "치료 효과가 아닌 DDI 크기 특성화" 의미를 명확히 한 점은 IRB·MFDS 심사관 혼동을 선제 차단한다.

**5명 전문가(DDI 시험 필수 구성)** 리뷰를 통합한 결과, Critical 결함은 없으며 Major 8건·Minor 16건이 확인되었다. Major 사항의 대부분은 **서술 보완·분석 로직 명확화·규제 인용 정정**으로 해결 가능하며, 설계의 근본적 변경 없이 1–2주 내 수정 사이클로 IND 제출 가능 수준으로 도달할 수 있다.

**핵심 상충 이슈**는 M-3 (AUC₀₋₂₄ vs AUC₀₋∞)로, 과학적 근거(CP)와 규제 가이드라인 정합성(REG)이 서로 다른 방향을 가리킨다. 이는 Pre-IND 미팅 실시 여부에 따라 결정하는 것이 현실적이며, **사용자(의뢰자) 판단이 필요한 사항**이다.

**자동 수정 필요 여부**: Critical 사항이 없으므로 **자동 수정 트리거 요건 미충족**. protocol-writer의 자동 1차 수정은 규정상 Critical 발견 시 실행되므로, 본 리뷰에서는 **사용자에게 Major 8건 수정 여부를 확인받는 절차가 우선**된다. Major 수정 승인 시 protocol-writer에 위임 가능.

---

*작성: qa-reviewer | 검토일: 2026-04-14*
*기반 리뷰 5건: `_workspace/review/review_{clinical_pharmacologist, regulatory_expert, biostatistician, clinician, translational_scientist}.md`*
*규제 근거: ICH E6(R3) 2025-01-06 Step 4 Final Appendix B, KGCP, 약사법, PIPA, 생명윤리법, FDA DDI Guidance 2020, ICH M12 2024, MFDS DDI 가이드라인(2015)*
