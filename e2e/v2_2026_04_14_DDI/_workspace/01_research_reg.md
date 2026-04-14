# 규제 자료 조사 보고서 — Clopidogrel + Omeprazole DDI 시험

**작성일**: 2026-04-14
**작성자**: regulatory-expert
**시험 유형**: DDI (Drug-Drug Interaction), Phase 1
**시험약**: Clopidogrel bisulfate 75 mg (victim/probe) + Omeprazole 80 mg (perpetrator)

---

## 1. 적응증 코딩 (ICD-10)

| ICD-10 코드 | 영문 명칭 | 한글 명칭 | 비고 |
|-----------|----------|---------|------|
| **I25.10** | Atherosclerotic heart disease of native coronary artery without angina pectoris | 협심증 없는 원발성 관상동맥의 죽상경화성 심장질환 | Clopidogrel 주 적응증 |
| **I20.0** | Unstable angina | 불안정 협심증 | ACS(급성관상동맥증후군) 포함 |

**확인 방법**: NLM ICD-10-CM API (clinicaltables.nlm.nih.gov) — 두 코드 모두 유효 확인.

**코딩 근거**: trial_info.md 기재 적응증(급성관상동맥증후군, 관상동맥질환 죽상경화성 사건 예방)에 대응하는 공식 ICD-10 코드. 실제 시험은 건강인 대상이므로 적응증 코드는 계획서 배경 섹션 기술 목적으로만 사용.

---

## 2. 규제 가이드라인 요약

→ 상세: 개별 파일 `_workspace/01_references/guidelines/`

### 2.1 MFDS 가이드라인

**문서**: 의약품의 약물상호작용 평가 가이드라인 (2015, [발행일 확인 필요])
→ 상세: `[01_references/guidelines/MFDS_DDI_2015.md]`

| 핵심 요건 | 내용 |
|---------|------|
| 시험 설계 | Fixed-sequence (고정순서) 교차설계 — 억제제 정상상태(5~7일 전투여) 후 기질 단회 투여 |
| 1차 평가변수 | AUC₀₋∞ GMR 및 90% CI |
| No-effect boundary | **90% CI 80.00%~125.00%** |
| 통계 분석 | ANOVA (ln 변환), GMR 및 90% CI |
| 대상자 | 건강한 성인 자원자 원칙 |
| PBPK | 보조 근거만; 임상 시험 단독 대체 불가 |
| Washout | 기질 및 억제제 각각 5 반감기 이상 |

**MFDS vs FDA 핵심 차이**: PBPK 수용도 차이 — FDA는 임상 면제 허용, MFDS는 보조만.

### 2.2 FDA 가이드라인

**문서**: Clinical Drug Interaction Studies Guidance (2020-01)
→ 상세: `[01_references/guidelines/FDA_DDI_2020.md]`

| 핵심 요건 | 내용 |
|---------|------|
| In vitro CYP 가역적 억제 트리거 | R1 = 1 + (Imax,u/Ki,u) ≥ 1.02 |
| In vitro TDI 트리거 | AUCR 예측 ≥ 1.25 |
| 임상 설계 | One-sequence (fixed-sequence) — 강력 억제제 perpetrator 시 표준 |
| No-effect boundary | 90% CI **80~125%** |
| NTI 기질 | 더 좁은 기준 (90~111%) 고려 |
| 억제제 분류 | Strong: AUC ≥5배; Moderate: 2~5배; Weak: 1.25~2배 |
| PBPK | 임상 시험 대체 허용 (사전 FDA 협의 권장) |

**2020년 주요 변경**: MATE 수송체 트리거 기준 0.02 → 0.1 상향; 비결합형 농도(Imax,u) 사용 명시

### 2.3 EMA 가이드라인

**문서**: Guideline on the Investigation of Drug Interactions (CPMP/EWP/560/95/Rev. 1, 2012)
→ 상세: `[01_references/guidelines/EMA_DDI_2012.md]`

| 핵심 요건 | 내용 |
|---------|------|
| 농도 기준 | 비결합 농도(Cmax,u) 기반 명시 |
| BSEP 평가 | **EMA 전용 필수** — 간독성 목적 |
| 혼합 억제/유도 | **In vivo 임상 시험 필수** (PBPK 불충분) |
| CYP 유도 평가 | 5종 (FDA/MFDS 3종보다 광범위) |
| 대사체 DDI | 이중 기준: ≥25% 또는 ≥10% |
| No-effect boundary | 0.5~2.0배 (서술적 접근) |
| CYP 다형성 | CYP2C19 유전형/표현형 분층 권고 명시 |

**개정 현황**: Rev. 2 개정 진행 중 (2017년 Concept paper); ICH M12(2024) 참조 권고.

### 2.4 ICH M12

**문서**: ICH M12 Drug Interaction Studies (2024, Step 4)
→ 상세: `[01_references/guidelines/ICH_M12.md]`

| 핵심 요건 | 내용 |
|---------|------|
| 성격 | FDA 2020 + EMA 2012를 국제 조화한 통합 가이드라인 |
| OCT1 평가 | 새로 명시적 권고 추가 |
| UGT 기질 | 의사결정 체계 도입 |
| 국제 공동 제출 | 단일 분석으로 복수 기관 제출 가능 |
| CYP2C19 분층 | PM 집단 별도 분석 권고 |
| 발행 시기 | 2024 (가장 최신) |

### 2.5 가이드라인 간 차이점 요약 (본 시험 관련)

| 항목 | MFDS | FDA | EMA | ICH M12 |
|------|------|-----|-----|---------|
| PBPK 활용 | 보조만 | 대체 허용 | 지지적 | 통합 활용 |
| No-effect boundary | 80~125% | 80~125% | 0.5~2배 | 80~125% |
| CYP2C19 분층 | 권장 | 권장 | **명시적 권고** | 명시적 권고 |
| BSEP | 없음 | 없음 | **필수** | [확인 필요] |
| 발행 최신성 | 2015 | 2020 | 2012 | **2024** |

**우선순위 적용**: MFDS(1순위) → FDA(2순위) → EMA(3순위) → ICH M12 (조화 기준)

---

## 3. 약물 라벨 핵심 정보

### 3.1 Clopidogrel (Plavix, NDA020839)

→ 상세: `[01_references/labels/clopidogrel_DailyMed.md]`, `[01_references/labels/clopidogrel_openFDA.md]`

**라벨 조회 정보**:
- DailyMed setid: e51d4bcc-01df-409d-9179-45e6536ac25b (Published: 2026-04-02)
- NDA020839, Sanofi Aventis US, 최초 승인: 1997-11-17

#### 블랙박스 경고 (FDA)

> **"DIMINISHED ANTIPLATELET EFFECT IN PATIENTS WITH TWO LOSS-OF-FUNCTION ALLELES OF THE CYP2C19 GENE"**
>
> CYP2C19 poor metabolizer(PM)로 확인된 환자에게 다른 P2Y12 억제제 사용 고려.

#### 약물상호작용 섹션 핵심

| 병용약 | 상호작용 | FDA 라벨 권고 |
|--------|---------|-------------|
| **Omeprazole/Esomeprazole** | CYP2C19 억제 → 활성 대사체 ~45% 감소, 혈소판 억제 ~47% 감소 | **병용 금지 (Avoid)** |
| Dexlansoprazole/Lansoprazole/Pantoprazole | 영향 적음 | 상대적으로 덜 우려 |
| Rifampin | CYP2C19 강력 유도 → 출혈 위험 | 병용 금지 |
| Repaglinide | CYP2C8 억제 (활성 대사체) → 3.9~5.1배 노출 증가 | 용량 감소 필요 |

#### 중요 PK 정보

| 파라미터 | 값 |
|---------|---|
| 성격 | Prodrug → 활성 대사체(H4) |
| Tmax (활성 대사체) | ~0.5~2 hr |
| t½ (활성 대사체) | ~0.5~1 hr |
| 활성 대사체 분율 | ~15% (나머지 85%는 불활성 카르복실산) |
| 대사 경로 | CYP2C19 (활성화); CYP3A4/2B6/1A2 (불활성화) |

#### CYP2C19 PM 비율 (라벨 기재)

| 인종 | PM 비율 |
|------|--------|
| White (서양인) | ~2% |
| Black | ~4% |
| Chinese | ~14% |

**임상 시사점**: 한국인 PM 비율 ~15% (서양인 2-3% 대비 현저히 높음) → 국내 임상 적용 시 CYP2C19 분층 분석의 임상적 중요성 크다.

### 3.2 Omeprazole (Prilosec/제네릭)

→ 상세: `[01_references/labels/omeprazole_DailyMed.md]`, `[01_references/labels/omeprazole_openFDA.md]`

**라벨 조회 정보**:
- DailyMed setid: ded0df8b-1813-4595-ac2b-5499704bfd48 (Published: 2026-04-08)
- NDA021229 (AstraZeneca, 2003-06-20); 원개발 Prilosec NDA019810 [확인 필요]

#### Clopidogrel 병용 경고 (Section 5.7)

> **"Avoid concomitant use of omeprazole with clopidogrel."**
>
> Omeprazole은 CYP2C19 활성을 억제하여 clopidogrel의 활성 대사체 형성을 장애시킨다. 80 mg 병용 시 활성 대사체 노출 현저 감소. **12시간 간격 투여도 동일 효과** → 투여 시간 분리로 회피 불가.

#### Omeprazole의 CYP2C19 TDI 특성

| 특성 | 내용 |
|------|------|
| 억제 유형 | **Time-Dependent Inhibitor (TDI)** + autoinhibition |
| 비선형 PK | 반복 투여 시 농도 비례 이상 증가 (40 mg: Cmax 118%↑, AUC 175%↑) |
| 대사 경로 | CYP2C19 (주) → hydroxyomeprazole; CYP3A4 (부) → omeprazole sulfone |
| PM에서 노출 | PM에서 Omeprazole 자체 농도 현저 증가 → DDI 크기도 더 커짐 |

---

## 4. MFDS 국내 임상시험 승인현황

→ 상세: `[01_references/mfds_clinical_trials/clopidogrel_approved_trials.md]`

**[MFDS 승인현황 미수집 — 오프라인 확인 권장]**

- MFDS 의약품안전나라 searchClinic WebFetch 조회 결과: **0건 반환** (파싱 실패 추정)
- 영문("clopidogrel"), 한글("클로피도그렐", "항혈소판", "혈소판") 다수 키워드 시도 모두 0건
- 원인: 서버 렌더링 HTML + JavaScript 동적 테이블 파싱 한계

**권고 사항**:
1. MFDS 의약품안전나라 직접 접속하여 오프라인 조회
2. data.go.kr MFDS 임상시험 OpenAPI (serviceKey 발급 후) 활용 검토
3. ClinicalTrials.gov `country=South Korea` + `intervention=clopidogrel` 검색 (clinical-pharmacologist 담당)

---

## 5. 규제 전략 권고

### 5.1 시험 설계 관련 규제 요건

| 항목 | 규제 요건 | 권고 |
|------|---------|------|
| 시험 설계 | Fixed-sequence crossover (MFDS/FDA/ICH M12 모두 지지) | Two-period fixed-sequence, open-label |
| Omeprazole 전투여 기간 | 5~7일 (정상상태 도달) | TDI autoinhibition 특성 고려하여 7일 권장 |
| 기질 투여 | 단회투여 (MFDS 원칙) | Clopidogrel 75 mg 단회 투여 |
| Washout | ≥5 반감기 (MFDS/FDA) | 혈소판 수명(~10일) 고려 ≥14일 |
| 1차 평가변수 | AUC₀₋∞ GMR 90% CI (MFDS/FDA) | 활성 대사체(H4) AUC₀₋ₜ 및 Cmax GMR |
| No-effect boundary | 80~125% (MFDS/FDA) | 90% CI 80~125% 범위 이탈 시 임상적 유의 DDI |
| 통계 | ANOVA, ln 변환 (MFDS) | Paired t-test 또는 ANOVA |
| CYP2C19 분층 | 권장 (모든 기관) | EM 대상자 선별; 표현형별 층화 분석 |

### 5.2 CYP2C19 유전형 검사 필요성

- FDA 블랙박스 경고: CYP2C19 PM에서 항혈소판 효과 현저 감소
- 본 시험에서 **CYP2C19 EM 대상자를 선별**하여 표준 DDI 크기를 측정하는 것이 일반적
- 선정 기준에 CYP2C19 genotyping 결과(*1/*1 = EM) 포함 필요
- 탐색적 분석으로 IM 포함 시 별도 분석 계획 수립 권장

### 5.3 활성 대사체(H4) 측정 요건

- FDA DDI Guidance: 주요 활성 대사체(모약물 AUC의 ≥25%) → 별도 DDI 평가 대상
- Clopidogrel 활성 대사체(H4): 전체 순환 노출의 ~15% (수치는 낮으나 약리적 활성 중요)
- **본 시험의 핵심 평가변수**: H4 AUC₀₋ₜ/Cmax GMR (라벨 DDI 데이터 근거)
- 생물분석법(bioanalytical method) 검증 필수 — BMV 가이드라인(FDA/EMA) 준수

### 5.4 다국가 허가 시 추가 고려사항

| 국가/기관 | 추가 요건 |
|---------|---------|
| MFDS (한국) | 본 가이드라인 요건 충족 |
| FDA | PBPK 보완 자료 활용 가능; NDA 제출 시 라벨 업데이트 |
| EMA | BSEP 억제 평가 데이터 추가 필요; CYP2C19 표현형 분층 명시적 권고 |

### 5.5 GCP 준수

- **ICH E6(R3)**: 2025-01-06 Step 4 최종본 — Annex 1(비기술적 원칙) + Annex 2(기술적) 구조
  - 계획서 필수 요소: Appendix B (B.1~B.16) 16개 섹션 준수
- **KGCP**: 의약품 임상시험 관리기준 (의약품등의 안전에 관한 규칙 별표 4)
- **생명윤리 및 안전에 관한 법률**: CYP2C19 유전형 검사(PG 분석) 계획 포함 → IRB 심의 및 기관생명윤리위원회 추가 심의 필요 여부 확인 필수
- **PIPA (개인정보 보호법)**: 유전정보는 민감정보 — 별도 동의 절차 필요

---

## 6. CYP2C19 PG 섹션 — Translational-Scientist 인계

**[translational-scientist 참고 자료]**

FDA 라벨에서 추출한 Clopidogrel CYP2C19 PG 정보:

1. **블랙박스 경고**: CYP2C19 two loss-of-function alleles (PM) → 항혈소판 효과 현저 감소 → 대체 P2Y12 억제제 권고
2. **인종별 PM 비율 (라벨 기재)**: White 2%, Black 4%, Chinese 14%
3. **CYP2C19 표현형 정의**:
   - PM (Poor Metabolizer) = two loss-of-function alleles
   - IM (Intermediate Metabolizer) = one loss-of-function allele
   - EM (Extensive Metabolizer) = no loss-of-function allele
4. **임상 결과**: TRITON-TIMI 38 서브분석에서 PM의 MACE 위험 증가 확인
5. **FDA Table of Pharmacogenomic Biomarkers**: Clopidogrel — CYP2C19 (Affects Response) 등재
6. **CPIC Level A**: CYP2C19–Clopidogrel (trial_info 기재)

**translational-scientist 담당 사항**:
- 한국인 CYP2C19 *2, *3 (loss-of-function) allele 빈도
- 표현형별 용량 조절 근거 (CPIC 가이드라인 세부 내용)
- PharmGKB/CPIC API 통한 최신 권고 확인
- Omeprazole 자체의 CYP2C19 기질 특성이 표현형별 DDI 크기에 미치는 영향 분석

---

## 7. 참고 문헌

| 항목 | 출처 |
|------|------|
| MFDS DDI 가이드라인 | 의약품의 약물상호작용 평가 가이드라인, MFDS, 2015 [발행일 확인 필요] |
| FDA DDI Guidance (Clinical) | Clinical Drug Interaction Studies, FDA CDER, 2020-01 |
| FDA DDI Guidance (In Vitro) | In Vitro Drug Interaction Studies, FDA CDER, 2020-01 |
| EMA DDI Guideline | Guideline on the Investigation of Drug Interactions, EMA CHMP, 2012-06 (CPMP/EWP/560/95/Rev. 1 Corr. 2) |
| ICH M12 | ICH M12 Drug Interaction Studies, ICH, 2024 |
| ICH E6(R3) | Good Clinical Practice, ICH, 2025-01-06 (Step 4 Final) |
| Clopidogrel 라벨 | Plavix (Clopidogrel Bisulfate) Prescribing Information, Sanofi Aventis US, NDA020839, 최초 승인 1997-11-17. DailyMed setid: e51d4bcc-01df-409d-9179-45e6536ac25b (2026-04-02) |
| Omeprazole 라벨 | Omeprazole Delayed-Release Capsules, FDA Prescribing Information. DailyMed setid: ded0df8b-1813-4595-ac2b-5499704bfd48 (2026-04-08) |
| ICD-10-CM 코드 | I25.10, I20.0, NLM ICD-10-CM API (clinicaltables.nlm.nih.gov), 2026-04-14 확인 |
| DDI Cross-Agency 비교 | ddi_cross_agency.md, 본 프로젝트 .claude/references, 2026-04-14 |
| MFDS 승인현황 | nedrug.mfds.go.kr/searchClinic — 2026-04-14 조회, 0건 반환 [오프라인 확인 권장] |
| FDA PG Biomarkers Table | FDA Table of Pharmacogenomic Biomarkers in Drug Labeling, https://www.fda.gov/medical-devices/precision-medicine/table-pharmacogenomic-biomarkers-drug-labeling |
