# 배경 조사 통합 보고서 — Clopidogrel + Omeprazole DDI

**시험 유형**: Phase 1, DDI (Drug-Drug Interaction)
**시험약**: Clopidogrel bisulfate 75 mg (victim/probe)
**병용약**: Omeprazole 80 mg (perpetrator/CYP2C19 inhibitor)
**조사 일자**: 2026-04-14
**참여 에이전트**: clinical-pharmacologist (CP), translational-scientist (TS), regulatory-expert (REG), clinician (CLIN)

> 개별 보고서:
> - `01_research_cp.md` (PK·DDI 기전·유사 시험·용량)
> - `01_research_reg.md` (규제 가이드라인·라벨·MFDS)
> - `01_research_clin.md` (안전성·선정/제외·모니터링)
> - `01_research_ts.md` (PD 바이오마커·PG·대사체·ICF 권고)

---

## 1. 적응증 개요

- **시험약 적응증**: 급성관상동맥증후군(ACS)·관상동맥질환에서의 죽상경화성 사건 예방
- **ICD-10**: **I25.10** (협심증 없는 관상동맥 죽상경화성 심장질환), **I20.0** (불안정 협심증)
- **시험 집단**: 건강한 성인 남성 지원자 (Phase 1). 시험 목적상 실제 적응증 환자는 대상 아님.
- **임상적 의미**: Clopidogrel-Omeprazole 상호작용은 FDA·EMA·MFDS 라벨에 명시된 확정된 DDI. 한국인 CYP2C19 PM 비율 ~13–15% (서양인 2–3%) → 국내 임상 적용 시 중요도 매우 큼.

→ 상세: `[01_references/guidelines/ICD10_I25_I20.md 개념]`, `01_research_reg.md §1`

---

## 2. 시험 개요

- **설계 제안(초안)**: Two-period, fixed-sequence, open-label crossover (Phase 4에서 확정)
- **대상자**: 건강한 성인 남성, 19–45세, **CYP2C19 EM (*1/*1)**
- **Washout 권장**: ≥14일 (혈소판 수명 + MDI 효소 회복)
- **1차 평가변수 권장**: 활성 대사체 H4의 AUC₀₋₂₄ 및 Cmax GMR (90% CI 80–125% 기준)

---

## 3. PK 자료 (CP)

### 3.1 Clopidogrel PK 핵심
- Prodrug → 활성 대사체 **H4** (thiol 형태). 흡수 약물의 ~15%만 활성형으로 전환
- **H4 Tmax 0.5–1 hr, t½ ~0.5–1 hr** (매우 짧음, 초기 밀집 채혈 필수)
- **H4 CV% ~50–60% (건강인 EM 기준)**, ~85–89% (환자) — biostatistician 입력값: **보수적 60%**
- 모체 및 비활성 대사체 SR26334 (t½ ~7.2–7.6 hr) — 보조 측정
- **식이 영향**: H4는 ~12% 감소 (임상적으로 유의하지 않음) → 공복 투여 표준화 권고

### 3.2 Omeprazole PK
- CYP2C19 TDI(**mechanism-based inhibitor**), IC₅₀ 8.4 μM, KI 1.7–9.1 μM, kinact 0.029–0.156 min⁻¹
- EM t½ ~0.5–1 hr, **PM에서 AUC 5.12×** (한국인 EM vs PM, PMID 28378544)
- **DDI 시험 용량 80 mg**: 자기 저해로 EM에서도 CYP2C19 포화 → worst-case DDI 조건

### 3.3 DDI 기전 및 예상 크기
- Omeprazole 80 mg 동시 투여 시 **H4 AUC 40–47% 감소 (GMR 0.53–0.60)**, 혈소판 억제 ~47% 감소
- 투여 시간 분리(12시간 간격)도 DDI 해결 **불가** (MDI + autoinhibition, PMID 20844485)
- Pantoprazole은 CYP2C19 DDI 미미 (H4 AUC 14% 감소) → 대조 권고

### 3.4 채혈 시점 권고
**Day 1 + Day 5 (정상 상태) 각각**: 0, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12, 24 hr (총 13 포인트)
- 0.25 hr 포인트 필수 (H4 Tmax 매우 짧음)
- 24시간으로 AUC₀₋∞ 근사 충분 (t½ ≪ 24 hr) → **절단 AUC 불필요**

→ 상세: `01_research_cp.md`, `[01_references/trials/NCT01129375.md]`, `[PMID_20844485.md]`

---

## 4. PD/약력학 자료 (TS)

### 4.1 PD 바이오마커 권고
| 순위 | 지표 | 방법 | 비고 |
|-----|-----|------|-----|
| 1순위 | **VerifyNow PRU** | Point-of-care (~5분) | FDA 510(k) 허가, CV<8%, HPR>208 / LPR<95 |
| 2순위 | **LTA % IPA (ADP 10 μmol/L)** | PRP 응집계 | Gold standard 참조 방법 |
| 탐색 | P2Y12 수용체 점유율 | LC-MS/MS | 연구용, 선택 |

**측정 시점**: 기저(D1 pre-dose), Period 1 정상상태 (D5–7 투여 후 2–4 hr), Period 2 정상상태 (D12–14 투여 후 2–4 hr)

### 4.2 PK-PD 모델 (Simon 2015, PMID 26071277)
- Sigmoid Emax 모델: Emax 56%, EC50 15.9 h·μg/L, **γ = 7.04** (매우 가파른 S형)
- 예상 PRU 변화: 단독 ~196 → 병용 ~217 (+21 PRU, ~11% 증가; PMID 23630016)
- HPR (>208 PRU) 비율: 48% (omeprazole) vs 33% (baseline)

→ 상세: `01_research_ts.md §2`, `[01_references/pd_biomarkers/VerifyNow_PRU.md]`, `[01_references/pd_biomarkers/LTA_platelet_aggregation.md]`

---

## 5. 유사 시험 분석

5건 주요 DDI 시험 확인 (clinical-pharmacologist 수집):

| NCT | 설계 | n | Clopidogrel | Omeprazole |
|-----|------|---|-------------|-----------|
| **NCT01129375** | 4-arm crossover | 72 | 300/75 mg | 80 mg |
| **NCT01129414** | 4-arm crossover | 72 | 600/150 mg | 80 mg |
| NCT01896557 | Parallel Ph4 | 92 | 75 mg QD | 20 mg BID |
| NCT00557921 | COGENT-1 Ph3 | ~5,000 (중단) | 75 mg | 20 mg |
| NCT01094275 | CYP2C19 × DDI | 32 | 75 mg | 20 mg |

**본 시험 방향**: NCT01129375 설계(2-arm crossover, 80 mg) 기반, sample size는 ~24명으로 단순화.

→ 상세: `[01_references/trials/NCT*.md]` 5개 파일

---

## 6. 규제 가이드라인 (REG)

### 6.1 적용 규제 우선순위 (국내 IND)
**MFDS (1순위) → FDA (2순위) → EMA (3순위) → ICH M12 (조화 기준)**

### 6.2 4대 기관 비교 (본 시험 관련)

| 항목 | MFDS 2015 | FDA 2020 | EMA 2012 | ICH M12 2024 |
|------|-----------|----------|----------|---------------|
| 설계 | Fixed-sequence | Fixed-sequence (Strong) | Fixed-sequence | Fixed-sequence |
| 1차 평가변수 | AUC₀₋∞ | AUC₀₋∞ | AUC₀₋∞ | AUC₀₋∞ |
| No-effect boundary | **80–125%** | **80–125%** | 0.5–2배 (서술) | 80–125% |
| PBPK 활용 | 보조만 | **임상 대체 허용** | 지지적 | 통합 활용 |
| CYP2C19 분층 | 권장 | 권장 | **명시적 권고** | **명시적 권고 (PM 별도)** |
| 특이 요건 | — | — | BSEP 필수 | OCT1 신규 명시 |

**결론**: 본 시험의 설계(fixed-sequence, EM 대상, H4 AUC GMR 90% CI 80–125%)는 4대 기관 모두 충족. 국내 IND 기준 MFDS 요건 우선 적용.

### 6.3 기타 규제
- **ICH E6(R3)** 2025-01-06 Step 4 최종본 — Appendix B (B.1~B.16) 16개 섹션 준수 필수
- **KGCP** (의약품등의 안전에 관한 규칙 별표 4)
- **생명윤리법** — CYP2C19 유전형 검사 → IRB + 기관생명윤리위원회 심의 확인 필요
- **PIPA** — 유전정보 민감정보, 별도 동의 필요

→ 상세: `01_research_reg.md §2`, `[01_references/guidelines/{MFDS_DDI_2015, FDA_DDI_2020, EMA_DDI_2012, ICH_M12}.md]`

---

## 7. 약물 라벨 정보 (PG 섹션 포함)

### 7.1 Clopidogrel 라벨 (Plavix, NDA 020839)
- **DailyMed setid**: `e51d4bcc-01df-409d-9179-45e6536ac25b` (Published 2026-04-02)
- **블랙박스 경고**: CYP2C19 PM에서 항혈소판 효과 감소 → 대체 P2Y12 억제제 고려
- **약물상호작용 섹션**:
  - **Omeprazole/Esomeprazole**: **병용 금지 (Avoid)** — 활성 대사체 ~45% 감소, 혈소판 억제 ~47% 감소, 12시간 간격도 불충분
  - Pantoprazole/Dexlansoprazole/Lansoprazole: 상대적으로 영향 적음
  - Rifampin: 병용 금지 (CYP2C19 유도)
- **인종별 PM 비율 (라벨)**: White 2%, Black 4%, **Chinese 14%**

### 7.2 Omeprazole 라벨
- **DailyMed setid**: `ded0df8b-1813-4595-ac2b-5499704bfd48` (Published 2026-04-08)
- **Section 5.7**: "Avoid concomitant use of omeprazole with clopidogrel" (양방향 경고)
- CYP2C19 TDI 특성 + autoinhibition 명시

→ 상세: `[01_references/labels/{clopidogrel, omeprazole}_{DailyMed, openFDA}.md]`

---

## 8. MFDS 임상시험 승인현황

**상태: 미수집 (결함 후보)**

- MFDS 의약품안전나라 `searchClinic` WebFetch 조회 결과 **0건 반환**
- 한글·영문 키워드 다수 시도 모두 파싱 실패 (JavaScript 동적 렌더링 추정)
- **권고**: (1) MFDS 의약품안전나라 오프라인 직접 조회, (2) data.go.kr OpenAPI(serviceKey 발급) 활용, (3) ClinicalTrials.gov `country=Korea + intervention=clopidogrel` 교차 확인

→ 상세: `[01_references/mfds_clinical_trials/clopidogrel_approved_trials.md]`, `01_research_reg.md §4`

---

## 9. 임상적 고려사항·안전성 (CLIN)

### 9.1 Clopidogrel 안전성 (건강인 단기)
- 한국인 건강인 30명 연구 (Shim 2010, PMID 20974324): 이상반응 없음
- CAPRIE 주요 AE: 발진 6.0%, 설사 4.46%, GI 출혈 1.99%, 두개내 출혈 0.33%
- **TTP**: 매우 드물지만(~1/200,000) 치명적, 투여 2주 이내 발병 → 집중 모니터링

### 9.2 Omeprazole 안전성 (단기)
- 주요 AE: 두통 ~4.7%, 설사 ~3.2% (경미, 일과성)
- 80 mg 고용량 단기 사용 — GI 증상 빈도 증가 가능, 장기 합병증(저Mg² 등) 무관

### 9.3 병용 안전성
- 항혈소판 효과 감소는 시험 목적 자체 (의도된 현상)
- GI 출혈: PPI 병용으로 오히려 **보호 효과** (RR 0.13, meta-analysis)
- 건강인 단기 시험에서 심각한 안전성 우려 없음

### 9.4 핵심 선정/제외 기준 (안전성 근거)
- **CYP2C19 PM 제외** (DDI 평가 타당성 + 안전성 측면은 양호)
- 출혈 병력, TTP 과거력, 혈소판 질환, 혈소판 <150×10⁹/L 제외
- 항혈전제·NSAIDs·항응고제 병용자 제외
- 활동성 GI 질환, 수술 예정자 제외
- PPI 기저 투여자 제외 (DDI 설계 타당성)

### 9.5 모니터링·중지 기준 핵심
- **혈소판 수 모니터링**: Screening, D1, D5–7, D14 (TTP 조기 발견)
- **중지 기준 (개인)**: 혈소판 <100×10⁹/L 또는 기저치 대비 >25% 감소 / TIMI Major 출혈 / 아나필락시스 / AST·ALT >5× ULN
- **중지 기준 (시험)**: TTP 1건, TIMI Major 출혈 1건, 인과관계 있는 SAE ≥2건

→ 상세: `01_research_clin.md`, `[01_references/safety/{AE_profile_*, SAE_cases_clopidogrel, safety_monitoring_rationale, stopping_rules_rationale}.md]`

---

## 10. 약물유전체학(PG) 자료 (TS) ★

### 10.1 CYP2C19 한국인 빈도 (매우 중요)
| 대립유전자/표현형 | 한국인 | 백인 |
|---|---|---|
| *2 (LoF) | ~26–28% | ~15% |
| *3 (LoF) | ~10–11% | <1% |
| *17 (GoF) | ~3–5% | ~18–22% |
| **PM 빈도** | **~13–15%** | **~2–3%** (5–7×) |
| NM 빈도 | ~40–45% | ~40% |
| IM 빈도 | ~35–40% | ~25% |

### 10.2 CPIC Level A — Clopidogrel-CYP2C19
- **CPIC `pair_view` API 직접 확인** (2026-04-14): Level A, Pair ID 110091, ClinPGx 1A
- **표현형별 권고 (CPIC 2022 Update, PMID 35034351)**:
  - PM/IM: **Clopidogrel 회피 → prasugrel/ticagrelor** (Strong)
  - NM/RM/UM: 표준 용량 (Strong)

### 10.3 FDA Black Box Warning
- CYP2C19 PM에서 항혈소판 효과 감소, 대체 약물 고려 명시
- Clopidogrel은 FDA Table of Pharmacogenomic Biomarkers에 "Affects Response" 등재

### 10.4 본 시험 PG 설계 권고
1. **CYP2C19 NM (*1/*1)만 선정** (CPIC Strong + FDA Black Box 이중 근거)
2. 스크리닝 유전형 검사: *2 (rs4244285), *3 (rs4986893), *17 (rs12248560) — TaqMan/PCR-RFLP
3. **스크리닝 수 보강**: NM 비율 ~40–45% → 24명 등록 위해 40–50명 스크리닝 예상
4. 탐색적 잔여 변동성 × 유전형 연관 분석 (선택)

### 10.5 ICF Part 4 권고 (생명윤리법 적용)
- **Part 4.1 CYP2C19 유전형 검사 동의** (선정 + 탐색적)
- **Part 4.2 잔여 검체 보관 동의** (선택)
- 유전정보 보호 문구, 결과 통보 조항 포함
- **기관생명윤리위원회 추가 심의 필요 여부 사전 확인**

→ 상세: `01_research_ts.md §3, §5.4`, `[01_references/pharmacogenomics/{CYP2C19, CPIC_clopidogrel_guideline}.md]`

---

## 11. 대사체 자료

### 11.1 Clopidogrel 활성 대사체 H4 (1차 평가변수)
- **BMAP 유도체화 LC-MS/MS 필수** (2-bromo-3'-methoxyacetophenone) — 반응성 thiol 기 안정화
- **채혈 후 5분 이내 BMAP 첨가 현장 SOP 필수**
- LLOQ 0.5 ng/mL (Takahashi 2008, PMID 18829199)
- -80°C 보관, 드라이아이스 운반
- 분석법 검증 (BMV) 필수

### 11.2 내인성 DDI 바이오마커
- 4β-hydroxycholesterol (CYP3A4 마커), Coproporphyrin I (OATP1B), 6β-hydroxycortisol (CYP3A 유도) — 모두 **본 시험에 해당 없음** (CYP2C19 DDI)
- H4 자체가 CYP2C19 활성의 기능적 지표 역할

→ 상세: `[01_references/metabolomics/clopidogrel_active_metabolite_H4.md]`

---

## 12. 종합 고려사항 (Phase 4 설계 협의 입력)

### 12.1 설계 확정 권고
| 항목 | 권고 | 근거 |
|-----|------|------|
| 시험 설계 | Two-period fixed-sequence, open-label crossover | MFDS/FDA/ICH M12 공통 |
| Period 1 | Clopidogrel 300 mg 로딩 D1 → 75 mg QD D2–5 | NCT01129375 |
| Washout | **≥14일** | 혈소판 수명 + MDI 효소 회복 |
| Period 2 | Omeprazole 80 mg × 7일 pre-treatment + Clopidogrel 300/75 mg 중첩 | Autoinhibition 정상상태 |
| 1차 평가변수 | **H4 AUC₀₋₂₄ 및 Cmax GMR** (90% CI 80–125%) | FDA DDI 2020, MFDS 2015 |
| PD 2차 | VerifyNow PRU (1순위), LTA %IPA (2순위) | FDA 510(k), gold standard |
| 대상자 | 건강한 성인 남성, 19–45세, **CYP2C19 *1/*1 EM only** | CPIC Strong, FDA Black Box |
| Sample size | n ~24 (CV% 60%, GMR 0.55, 90% CI 80–125%) | biostatistician 재계산 |
| 투여 조건 | **공복** | 식이 영향 없으나 표준화 |
| 채혈 | D1·D5 각 13 포인트 (0–24h) | H4 Tmax 짧음 |

### 12.2 Sample Size 계산 입력값 (biostatistician 인계)
- CV% (AUC, H4, 건강인 EM): **~60%** (보수적)
- 예상 GMR: 0.53–0.60 (DDI 40–47%)
- 동등성 경계: 90% CI 80–125%
- α = 0.05, 1-β = 0.80 (표준)
- 탈락률 10–15% 고려
- **초기 추정**: 완료 20명 → 등록 24명

### 12.3 유전체/대사체 분석 계획 확정 필요 항목
1. CYP2C19 유전형 범위 (*2, *3, *17 → 확정)
2. 검사 시점 (스크리닝 → 확정)
3. PM/IM 포함/제외 (제외 권고)
4. 탐색적 유전형 × 변동성 분석 여부
5. H4 대사체 분석법 (BMAP 유도체화 LC-MS/MS)
6. 잔여 검체 보관 기간 (5/10년/영구)
7. 유전자 결과 통보 여부

### 12.4 ICF 구성 항목 (phase 10)
- Part 1–3 (설명서, 서명, PIPA)
- **Part 4.1 CYP2C19 PG 동의** (필수)
- **Part 4.2 활성 대사체 대사체 분석 동의** (필수)
- **Part 4.3 잔여 검체 보관 동의** (선택)
- **Part 4.4 결과 통보 동의** (PG 임상적 중요 소견)

---

## 13. 참고 문헌 (통합)

### ClinicalTrials.gov (5건)
NCT01129375, NCT01129414, NCT01896557, NCT00557921, NCT01094275

### PubMed (28건, 핵심)
- **PK/DDI (CP)**: 20844485 Angiolillo 2011, 21795468 Ogilvie 2011, 23620487 Shirasaka 2013, 22004687 Boulenc 2012, 19106084 Mega 2009 NEJM, 22128201 Hurbin 2012, 24127209 Karazniewicz-Lada 2014, 29060457 Tangamornsuksan 2017, 28378544 Park 2017, 26071277 Simon 2015, 10440419 Caplain 1999
- **PD/PG/대사체 (TS)**: 16845449 Malinin 2006, 22464259 Frelinger 2012, 23630016 Arbel 2013, 20858862 2010, 18829199 Takahashi 2008, 35034351 Lee 2022 CPIC, 23074110 Shin 2012, 40041905 Li 2024
- **안전성 (CLIN)**: 10852999 Bennett 2000 TTP NEJM, 18774008 Price & Teirstein 2008, 24281379 Kubitza 2012, 20974324 Shim 2010, 25949846 Bouziana 2015, 10514023 Harker 1999 CAPRIE, 30738497 Fahmy 2019 FAERS, 1397750 Joelson 1992

### 가이드라인
- **ICH E6(R3)** 2025-01-06 Step 4 Final (Appendix B 16 sections)
- **ICH M12** 2024 Drug Interaction Studies (Step 4)
- **FDA** Clinical Drug Interaction Studies Guidance (2020-01)
- **EMA** Guideline on Investigation of Drug Interactions (CPMP/EWP/560/95/Rev.1, 2012)
- **MFDS** 약물상호작용 평가 가이드라인 (2015)

### 약물 라벨 (4건)
- Clopidogrel DailyMed (setid e51d4bcc-…) / openFDA NDA020839
- Omeprazole DailyMed (setid ded0df8b-…) / openFDA

### Pharmacogenomic API
- CPIC `pair_view`: https://api.cpicpgx.org/v1/pair_view?drugname=eq.clopidogrel&genesymbol=eq.CYP2C19 (Level A)
- CPIC `recommendation_view`: ibid., PM/IM/NM/RM/UM 권고
- PharmGKB `clinicalAnnotation`: [API HTTP 400 — 공개 논문 보완]
- CPIC Guideline URL: https://www.clinpgx.org/guideline/PA166251443

---

## 14. API 호출 상태 및 한계

| API | 상태 | 비고 |
|-----|------|------|
| DailyMed `spls.json` | ✅ 성공 | setid 실제 UUID 확보 |
| openFDA `drug/label.json` | ✅ 성공 | NDA020839 확인 |
| MFDS `searchClinic` | ❌ 실패 | JavaScript 동적 렌더링, 0건 반환 → **결함 후보 #1** |
| PharmGKB `clinicalAnnotation` | ❌ 실패 | HTTP 400 → 공개 논문 기반 보완, **결함 후보 #2** |
| CPIC `pair_view`/`recommendation_view`/`diplotype` | ✅ 성공 | Level A 확인 |
| ClinicalTrials.gov v2 | ✅ 성공 | 5건 NCT 수집 |
| PubMed | ✅ 성공 (WebSearch/WebFetch) | 28건 PMID 수집 |

---

## 15. 다음 단계 (Phase 4 설계 협의 입력 정리)

1. **선정/제외**: CYP2C19 PM/IM 제외 여부 확정
2. **연구설계**: Two-period fixed-sequence (확정적)
3. **PK 채혈**: 13 포인트 / Day 1 + Day 5 (확정적)
4. **PD 평가**: VerifyNow PRU 1순위 / LTA 2순위 (확정적)
5. **유전체/대사체 분석 계획**: CYP2C19 + H4 (필수), 잔여 검체 보관 (협의), 결과 통보 (협의)
6. **Washout**: 14일 (확정적)
7. **투여 조건**: 공복 (확정적)
8. **Sample size**: ~24명 (biostatistician 재계산 필요, CV% 60%)

---

*보고서 작성: 2026-04-14 | 참여: CP+TS+REG+CLIN 4-agent parallel research*
