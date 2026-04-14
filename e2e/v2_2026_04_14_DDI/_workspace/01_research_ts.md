# PD/오믹스 자료 조사 보고서 — Translational Scientist

## 시험 정보
- **시험약**: Clopidogrel bisulfate 75 mg + Omeprazole 80 mg (병용약)
- **시험 유형**: DDI (Drug-Drug Interaction)
- **조사일**: 2026-04-14

---

## 1. 조사 범위 및 우선순위

| 영역 | 우선순위 | 조사 결과 |
|-----|---------|---------|
| PD 바이오마커 (VerifyNow PRU, LTA) | ★★ 권장 | 완료 |
| 약물유전체학 CYP2C19 (한국인 PM ~15%) | ★★★ 필수 | 완료 |
| 대사체학 (H4 측정법, BMAP 유도체화) | ★★ 권장 | 완료 |
| 수용체 점유율 (P2Y12 비가역 차단) | ★★ 권장 | 탐색 완료 |

**근거**: DDI 시험 — PG ★★★ 필수 (CYP PM/EM 분류), PD ★★ 권장 (probe 약물 PD), 대사체 ★★ 권장 (DDI 관련 대사체) — clinical-research/SKILL.md 우선순위 표 기준

### Web API 호출 결과
- CPIC `pair_view` (clopidogrel/CYP2C19): **성공** — Level A, ClinPGx 1A, Pair ID 110091
- CPIC `recommendation_view` (clopidogrel): **성공** — PM/IM/NM/RM/UM별 표현형 권고 확인
- CPIC `diplotype` (CYP2C19): **성공** — *1/*1~*3/*3 Phenotype 매핑 확인
- PharmGKB `clinicalAnnotation` (clopidogrel/CYP2C19): **[API 호출 실패 — HTTP 400, 공개 논문 기반 보완]**

---

## 2. PD/약력학 자료

### 2.1 작용 기전(MOA) 요약

Clopidogrel은 **prodrug**으로 경구 투여 후 간에서 CYP2C19 (주요 경로), CYP3A4 (보조)를 통해 **활성 대사체(H4, thiol 대사체)**로 전환된다. H4는 혈소판 P2Y12 수용체의 Cys97, Cys175 잔기와 **disulfide 결합(비가역적)**을 형성하여 ADP 매개 혈소판 활성화와 응집을 억제한다.

Omeprazole은 CYP2C19를 경쟁적으로 억제하여 2-oxo-clopidogrel → H4 전환을 감소시키며, 결과적으로 H4 AUC 및 항혈소판 효과를 유의미하게 감소시킨다.

### 2.2 PD 바이오마커 후보

| 바이오마커 | 측정 시료 | 분석 방법 | 검증 상태 | 권장 우선순위 | 출처 |
|----------|---------|---------|---------|------------|------|
| **VerifyNow PRU** (P2Y12 Reaction Units) | 전혈 (citrate) | Point-of-care turbidimetry | FDA 510(k) 허가, 완전 검증 | 1순위 (2차 PD 지표) | PMID 16845449 |
| **LTA % IPA** (ADP 10 μmol/L) | PRP | 광투과율 응집계 | 참조 방법 (gold standard) | 2순위 (보완 PD 지표) | PMID 21192314 |
| **P2Y12 수용체 점유율** | 전혈 (EDTA) | LC-MS/MS (중수소 표지 H4) | 연구용 검증, 임상 미표준화 | 탐색적 (선택) | PMID 40041905 |

→ 상세: `01_references/pd_biomarkers/VerifyNow_PRU.md`, `01_references/pd_biomarkers/LTA_platelet_aggregation.md`

### 2.3 측정 방법 상세

#### VerifyNow PRU (권장 1순위)
- **채혈**: 3.2% sodium citrate 진공관 2.7 mL
- **측정 시간**: ~5분 (point-of-care)
- **컷오프**: HPR > 208 PRU, LPR < 95 PRU, 치료 목표 95–208 PRU
- **CV**: < 8% (within-run)
- **간섭 물질**: GP IIb/IIIa 억제제 주의; Hct 이상치 영향
- **시점**: 기저(Day 1 pre-dose), Period 1 정상상태 (Day 5–7 투여 후 2–4 hr), Period 2 정상상태 (Day 12–14 투여 후 2–4 hr)

#### LTA % IPA (보완 2순위)
- **채혈**: 3.2% sodium citrate, PRP 제조 (원심분리 150 g, 10분)
- **자극 물질**: ADP 10 μmol/L 권장
- **측정 시간**: 30–60분
- **측정 변수**: 최대 혈소판 응집률 (% PA), IPA (%) = 100 − % PA
- **주의**: 채혈 후 2시간 이내 검사, 37°C 유지

### 2.4 PK-PD 모델링 문헌

#### Sigmoid Emax 모델 (Simon et al., 2015, PMID: 26071277)

| 파라미터 | 값 | 의미 |
|---------|---|-----|
| Emax | **56 ± 5%** | 최대 혈소판 응집 억제율 (IPA) |
| EC50 (EAUC50) | **15.9 ± 0.8 h·μg/L** | 반최대 효과에서의 H4 AUC |
| Gamma (γ) | **7.04 ± 2.26** | Hill exponent (매우 가파른 S형 관계) |

**임상 시사점**:
- γ = 7의 가파른 관계 → 작은 H4 AUC 감소도 큰 IPA/PRU 변화 유발
- Omeprazole DDI에 의한 H4 AUC 46% 감소 → IPA 상당폭 감소 예측 가능
- PRU 변화량 예측: Omeprazole 병용 시 PRU ~196 → ~217 (+21 PRU, +11%; PMID: 23630016)

→ 상세: `01_references/literature/PMID_26071277.md`

#### Population PK-PD 모델 (Jung et al., 2024)
- Clin Pharmacol Ther. 2024
- CYP2C19 표현형별 용량 최적화 시뮬레이션
- PM의 경우 NM 대비 3–4배 고용량 필요 시뮬레이션 (계획서 PG 근거 보완)

### 2.5 수용체 점유율

P2Y12 수용체 점유율은 H4의 **비가역적 공유결합**으로 생긴 억제를 직접 반영한다.

- **측정 방법**: LC-MS/MS (Li et al., 2024/2025, PMID: 40041905) — 중수소 표지 H4로 미점유 수용체 정량
- **P2Y12 점유율 vs IPA 상관관계**: y = 0.839x + 12.55, r² = 0.883 (강한 선형 관계)
- **Omeprazole DDI 효과**: 수용체 점유율 54.8% 감소
- **현황**: 연구용 방법, 임상 일상화 미달성

**본 시험 적용 권고**: 탐색적 부가 평가로 고려 가능하나, 비용 및 복잡성 고려 시 주요 PD 지표로는 PRU/LTA IPA 사용. 설계 협의에서 추가 여부 결정.

→ 상세: `01_references/literature/PMID_40041905.md`

---

## 3. 약물유전체학 자료

### 3.1 CYP2C19 다형성 (주요 관여 효소 — Major)

| 효소 | 시험약 기여도 | 주요 대립유전자 | 한국인 빈도 | PM 빈도 |
|------|-----------|-------------|----------|--------|
| **CYP2C19** | **Major** (rate-limiting step) | *1(정상), *2(기능상실), *3(기능상실), *17(기능증가) | *2 ~27%, *3 ~10.5% | **~13–15%** |

**한국인 vs 백인 비교**:

| 대립유전자 | 한국인 | 백인 | 임상 의의 |
|----------|-------|------|---------|
| *2 | ~26–28% | ~15% | 한국인에서 2배 높음 |
| *3 | ~10–11% | <1% | 한국인에서 매우 높음 |
| *17 | ~3–5% | ~18–22% | 한국인에서 훨씬 낮음 |
| PM 빈도 | **~13–15%** | ~2–3% | 한국인에서 5–7배 높음 |

→ 상세: `01_references/pharmacogenomics/CYP2C19.md`

### 3.2 표현형 분류 (CPIC 기준)

| 표현형 | 한국인 빈도 | Clopidogrel 효과 |
|-------|-----------|----------------|
| NM (*1/*1) | ~40–45% | 정상 항혈소판 효과 |
| IM (*1/*2, *1/*3) | ~35–40% | 중간 정도 효과 감소 |
| PM (*2/*2, *2/*3, *3/*3) | **~13–15%** | 항혈소판 효과 크게 감소 |
| RM (*1/*17) | ~3–5% | 정상–약간 증가 |
| UM (*17/*17) | ~0.1–0.5% | 약간 증가 (출혈 위험 불명확) |

### 3.3 FDA 라벨 PG 권고사항 (Plavix NDA 020839)

**Black Box Warning (블랙박스 경고)**:
"Diminished antiplatelet effect in patients with two loss-of-function alleles of the CYP2C19 gene. Consider use of another platelet P2Y12 inhibitor."

**Clopidogrel + Omeprazole 상호작용 경고**:
"Avoid concomitant use of omeprazole or esomeprazole with clopidogrel bisulfate. Separate administration by 12 hours does not appear to mitigate the interaction."

**PK/PD 데이터 (FDA 라벨)**:
- CYP2C19 PM: 활성 대사체 AUC ~30% 낮음, 최대 혈소판 억제 ~32% (NM ~51%)
- Omeprazole 80 mg 동시 투여: 활성 대사체 AUC 46% 감소, 최대 혈소판 응집 억제율 47% 감소

### 3.4 CPIC 가이드라인 (Level A)

**CPIC Pair View API 확인** (2026-04-14):
- Level: **A** (최고 등급)
- ClinPGx Level: **1A**
- Guideline URL: https://www.clinpgx.org/guideline/PA166251443

**핵심 표현형별 권고 (2022 Update, PMID: 35034351)**:

| 표현형 | ACS/PCI 권고 | 강도 |
|-------|------------|-----|
| PM | clopidogrel 회피 → prasugrel/ticagrelor | **Strong** |
| IM | clopidogrel 회피 → prasugrel/ticagrelor | **Strong** |
| NM | 표준 용량 (75 mg/일) | **Strong** |
| RM/UM | 표준 용량 | Strong |

→ 상세: `01_references/pharmacogenomics/CPIC_clopidogrel_guideline.md`

---

## 4. 대사체 자료

### 4.1 Clopidogrel 활성 대사체 H4 — 본 시험 핵심 대사체

H4는 본 시험의 **1차 PK 목적 지표**이면서, PD와 연계되는 **핵심 대사체**이다.

| 항목 | 내용 |
|------|------|
| 화학 특성 | 반응성 thiol 기 보유 → 생체 내 빠른 불활성화 |
| 분석 방법 | LC-MS/MS (BMAP 유도체화 필수) |
| LLOQ | 0.5 ng/mL (Takahashi 2008, PMID: 18829199) |
| 안정성 | -80°C 4개월 (유도체화 후) |
| 채혈 특이사항 | 채혈 후 5분 이내 BMAP 첨가 필수 |

**유도체화 원리**: BMAP + H4 thiol → 안정한 thioether (CAM-D) → 생체분석 가능

→ 상세: `01_references/metabolomics/clopidogrel_active_metabolite_H4.md`

### 4.2 내인성 DDI 바이오마커 검토

본 시험의 DDI 기전은 **CYP2C19 억제** (Omeprazole → Clopidogrel 활성화 감소). 일반적인 DDI 내인성 바이오마커는 아래와 같이 적용성을 검토하였다:

| 내인성 마커 | 적용 DDI 기전 | 본 시험 적용 여부 |
|-----------|------------|----------------|
| 4β-hydroxycholesterol/cholesterol | CYP3A4 활성 | 해당 없음 (CYP2C19 DDI) |
| Coproporphyrin I | OATP1B 활성 | 해당 없음 |
| 6β-hydroxycortisol | CYP3A 유도 | 해당 없음 |

**결론**: 본 시험에는 별도의 내인성 바이오마커 측정이 필요 없음. H4 자체가 CYP2C19 활성의 기능적 지표 역할을 함.

---

## 5. 본 시험 설계에의 시사점

### 5.1 권장 PD 평가 항목 (Phase 4 설계 협의 입력)

**2차 목적 PD 평가 권장 구성**:

| 순위 | 지표 | 방법 | 시점 | 비고 |
|-----|-----|------|-----|-----|
| 1순위 | VerifyNow PRU | Point-of-care | Day 1 pre-dose, Period 1/2 Day 5 투여 후 2–4 hr | 표준화된 검증 방법 |
| 2순위 | LTA % IPA (ADP 10 μmol/L) | 전통적 응집계 | 동일 시점 | 참조 방법 보완 |
| 탐색 | P2Y12 수용체 점유율 | LC-MS/MS | 선택적 | 연구용, 비용 고려 |

**권장 PD 측정 시점 (PRU 기준)**:
- T1: Day 1, Pre-dose (기저값, Clopidogrel 투여 전)
- T2: Period 1 Day 5–7, Clopidogrel 투여 후 2–4 hr (Clopidogrel 단독 정상상태)
- T3: Period 2 Day 12–14, 병용 투여 후 2–4 hr (Omeprazole 병용 정상상태)

**예상 PRU 변화 (문헌 기반)**:
- Clopidogrel 단독: ~196 PRU (기저 ~270 PRU에서 감소)
- Omeprazole 병용: ~217 PRU (+21 PRU, ~11% 증가; PMID: 23630016)
- HPR (>208 PRU) 비율: ~48% (omeprazole) vs ~33% (baseline; PMID: 23630016)

### 5.2 PG 분석 권장 여부 및 항목

**권장**: 강력히 권장 (CPIC Level A, FDA Black Box Warning)

| 항목 | 내용 |
|-----|-----|
| 검사 유전자 | CYP2C19 |
| 검출 대립유전자 | *2 (rs4244285), *3 (rs4986893), *17 (rs12248560) |
| 시점 | 스크리닝 방문 시 (등록 전) |
| 시료 | 전혈 (EDTA 4 mL), 또는 Buccal swab |
| 방법 | TaqMan 실시간 PCR 또는 PCR-RFLP |
| 목적 1 | 선정 기준 적용 (NM *1/*1만 등록, PM/IM 제외) |
| 목적 2 | 탐색적 분석 — 잔여 변동성과 유전형 연관성 분석 (선택) |

**한국인 특이 사항**:
- PM (~15%) 및 IM (~35–40%) 비율이 높아 스크리닝 탈락률 고려 필요
- 전체 스크리닝 대상 24명의 NM 등록을 위해 ~35–45명 스크리닝 예상 (PM ~15% + IM ~35–40% 제외 고려)
- 이를 시험 계획서 스크리닝 실패 허용 범위에 반영 권장

### 5.3 대사체 분석 권장 여부 및 항목

**H4 측정** (clinical-pharmacologist 주도, TS 분석 기술 지원):
- BMAP 유도체화 LC-MS/MS: 반드시 적용
- 현장 즉시 처리 SOP 수립: 채혈 후 5분 이내 BMAP 첨가
- 분석 검증 (bioanalytical method validation): BMAP-유도체화 H4 분석법을 미리 검증 후 적용

### 5.4 추가 동의 필요 여부 (생명윤리법 적용 검토)

**생명윤리 및 안전에 관한 법률 적용**:

| 항목 | 해당 여부 | 내용 |
|-----|---------|-----|
| CYP2C19 유전형 검사 (선정 목적) | **해당** | 인체유래물(혈액) + 유전정보 수집 → 생명윤리법 적용 |
| CYP2C19 유전형 검사 (탐색적 연구) | **해당** | 별도 선택 동의 필요 (ICF Part 4.1) |
| H4 활성 대사체 측정 | 해당 없음 | 약물 분석, 유전정보 아님 |
| PRU/LTA 측정 | 해당 없음 | 기능 검사 |

**ICF 구성 권고**:

```
ICF Part 4 (선택 동의) — 약물유전체 분석
4.1 CYP2C19 유전형 검사 동의
    - 목적: 시험 적합성 확인 (선정 기준) 및 탐색적 PGx 분석
    - 검사 내용: *2, *3, *17 대립유전자 검출
    - 결과 통보: 유전형 검사 결과를 귀하에게 알려드립니다 (동의 시)
    - 자료 보관: 익명화 후 연구 목적으로 최대 15년 보관
    - 생명윤리법 제42조에 따른 유전정보보호 조항 포함
    
4.2 잔여 생물학적 검체 보관 동의 (해당 시)
    - 검체: 혈액 (CYP2C19 유전형 검사 후 잔여)
    - 향후 PGx 관련 연구 목적 보관 여부
```

**기관생명윤리위원회(IRB) 별도 검토**:
- CYP2C19 유전형 검사 + 유전정보 수집이 연구 목적으로 포함되는 경우
- IRB 승인과 별도로 **기관생명윤리위원회 추가 심의** 필요 여부 확인 권장

---

## 6. 한계 및 추가 자료 필요

### MCP/API 도구 한계

| 도구 | 상태 | 내용 |
|-----|-----|-----|
| CPIC pair_view API | **성공** | Level A, Pair ID 110091 확인 |
| CPIC recommendation_view API | **성공** | PM/IM/NM/RM/UM 권고 확인 |
| CPIC diplotype API | **성공** | 주요 diplotype 매핑 확인 |
| PharmGKB clinicalAnnotation API | **[실패 — HTTP 400]** | 공개 논문(PMID 35034351 등) 기반 보완 |
| PubMed MCP | **미사용** (MCP 미로드) | WebSearch + WebFetch로 대체 |
| HMDB | 미사용 | H4 상세 대사 정보는 공개 논문으로 충분 |

### 추가 자료 권장

1. **FDA Plavix 전문 라벨 (DailyMed)**: regulatory-expert가 DailyMed WebFetch로 PGx 섹션 전문 추출 후 교차 확인
2. **MFDS Plavix 국내 라벨**: 국내 라벨의 omeprazole 병용 경고 문구 확인 (한국어 계획서 인용)
3. **CPIC 가이드라인 전문 PDF**: https://files.cpicpgx.org/data/guideline/publication/clopidogrel/2022/35034351.pdf

---

## 7. 핵심 권고 목록 (Phase 4 설계 협의 입력용)

다음 항목들이 시험 설계 협의 (Phase 4) 시 반드시 반영되어야 할 TS 관점 핵심 권고이다.

### 선정/제외 기준
1. **CYP2C19 NM (*1/*1)만 선정** — CPIC Level A, FDA Black Box Warning 근거
2. **사전 스크리닝에서 CYP2C19 유전형 검사 포함** (*2, *3, *17)
3. **PM/IM 제외 기준 명시** — *2/*2, *2/*3, *3/*3 (PM); *1/*2, *1/*3 (IM)
4. **스크리닝 수 보강**: NM 비율 ~40–45% → 목표 등록수 확보 위해 1.8–2.5배 스크리닝 예상

### PD 평가 설계
5. **VerifyNow PRU 2차 PD 지표로 필수 포함** — FDA 510(k) 허가된 검증 방법
6. **LTA % IPA (ADP 10 μmol/L) 보완 지표** — 참조 방법으로 추가
7. **PRU 측정 시점**: 기저(D1), Period 1 정상상태(D5–7), Period 2 정상상태(D12–14), 투여 후 2–4 hr
8. **HPR (>208 PRU) 발생률 비교** — 2차 탐색적 지표

### 생체분석 계획
9. **H4 분석에 BMAP 유도체화 LC-MS/MS 사용** — PMID: 18829199 검증 방법
10. **채혈 후 5분 이내 BMAP 첨가 현장 SOP 필수** — 안정성 확보
11. **-80°C 보관, 드라이아이스 운반** 조건 명시

### ICF 구성
12. **ICF Part 4.1 (선택 동의): CYP2C19 유전형 검사 동의 항목 추가**
13. **생명윤리법에 따른 유전정보 보호 문구** 및 결과 통보 여부 명시
14. **잔여 검체 보관 동의 (Part 4.2)** 여부 의뢰자와 협의

### 통계 분석 계획
15. **Biostatistician에 제공**: PRU 기저값 ~196 (단독), ~217 (omeprazole 병용), ΔPR ~21 PRU, HPR 비율 48% vs 33%
16. **CYP2C19 유전형 층화 분석** (NM만 선정하더라도 *1/*1이 등록된 전체에서 동질성 확인)

---

## 8. 참고 문헌

| PMID | 저자 (연도) | 내용 요약 |
|------|-----------|---------|
| **16845449** | Malinin et al. (2006) | VerifyNow P2Y12 validation, CV < 8%, LTA 일치도 확인 |
| **22464259** | Frelinger et al. (2012) | PPI 4종 vs clopidogrel PD, 건강한 지원자 160명 crossover, PRU 측정 |
| **23630016** | Arbel et al. (2013) | Omeprazole vs pantoprazole vs famotidine PRU 비교, HPR 48% vs 33% |
| **20858862** | — (2010) | 동시 vs 12시간 간격 투여 PRU 비교, 12시간 간격도 DDI 해결 못함 |
| **26071277** | Simon et al. (2015) | PK-PD sigmoid Emax 모델, Emax 56%, EC50 15.9 h·μg/L, γ 7.04 |
| **23333143** | Frelinger et al. (2013) | Clopidogrel PK/PD variability (CYP2C19 NM only), CV 32–53% |
| **18829199** | Takahashi et al. (2008) | H4 LC-MS/MS BMAP 유도체화, LLOQ 0.5 ng/mL, 검증 완료 |
| **35034351** | Lee CR et al. (2022) | CPIC 2022 update, PM/IM → clopidogrel 회피 Strong 권고 |
| **23074110** | Shin DJ et al. (2012) | 한국인 CYP2C19*2 ~27%, *3 ~10.5% |
| **40041905** | Li H et al. (2024/2025) | P2Y12 수용체 점유율 LC-MS/MS, IPA와 r²=0.883, Omeprazole 점유율 54.8% 감소 |
| **24100274** | Kim YH et al. (2014) | 한국인 8,163명 코호트, CYP2C19 PM 14.2% |

**API 출처**:
- CPIC pair_view: https://api.cpicpgx.org/v1/pair_view?drugname=eq.clopidogrel&genesymbol=eq.CYP2C19 (조회: 2026-04-14)
- CPIC recommendation_view: https://api.cpicpgx.org/v1/recommendation_view?drugname=eq.clopidogrel (조회: 2026-04-14)
- Guideline: https://www.clinpgx.org/guideline/PA166251443

**개별 reference 파일 목록**:
- `_workspace/01_references/pd_biomarkers/VerifyNow_PRU.md`
- `_workspace/01_references/pd_biomarkers/LTA_platelet_aggregation.md`
- `_workspace/01_references/pharmacogenomics/CYP2C19.md`
- `_workspace/01_references/pharmacogenomics/CPIC_clopidogrel_guideline.md`
- `_workspace/01_references/metabolomics/clopidogrel_active_metabolite_H4.md`
- `_workspace/01_references/literature/PMID_16845449.md`
- `_workspace/01_references/literature/PMID_22464259.md`
- `_workspace/01_references/literature/PMID_23630016.md`
- `_workspace/01_references/literature/PMID_20858862.md`
- `_workspace/01_references/literature/PMID_26071278.md` (Simon 2015)
- `_workspace/01_references/literature/PMID_18829199.md`
- `_workspace/01_references/literature/PMID_35034351.md`
- `_workspace/01_references/literature/PMID_23074110.md`
- `_workspace/01_references/literature/PMID_40041905.md`
