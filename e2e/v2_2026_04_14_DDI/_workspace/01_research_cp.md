# 임상약리학 조사 보고서 — Clopidogrel + Omeprazole DDI 시험

**작성자**: Clinical Pharmacologist Agent  
**작성일**: 2026-04-14  
**시험 유형**: Phase 1, DDI (Drug-Drug Interaction)  
**시험약**: Clopidogrel 75 mg (victim/probe drug)  
**병용약**: Omeprazole 80 mg (perpetrator/inhibitor)

---

## 1. Clopidogrel PK 개요

### 1.1 약물 특성 요약

| 항목 | 내용 |
|------|------|
| 계열 | Thienopyridine P2Y12 수용체 억제제 (항혈소판제) |
| 구조적 특성 | Prodrug (전구약물) — 활성화 필수 |
| 생체내 활성화 경로 | CYP 효소계를 통한 2단계 산화: Clopidogrel → 2-oxo-clopidogrel → 활성 대사체(H4) |
| 활성 대사체 | H4 이성체 (clopi-H4) — 4개 티올 이성체 중 유일한 활성형 |
| 비활성 대사 경로 | CES1(carboxylesterase 1)에 의한 가수분해 → 비활성 카르복실산 대사체(SR26334) |
| 전환율 | 흡수된 약물의 ~15%만 활성 대사체로 전환; ~85%는 비활성 경로로 |

### 1.2 Clopidogrel 활성 대사체(H4) PK 파라미터

| 파라미터 | 값 | 출처 |
|---------|---|------|
| **Tmax (H4)** | 0.5–1 시간 (로딩 후), 정상 상태 1–2시간 | Caplain 1999 (PMID 10440419), Angiolillo 2011 (PMID 20844485) |
| **t½ (H4)** | **~0.5–1시간** (매우 짧음) | Karazniewicz-Lada 2014 (PMID 24127209), 문헌 공통 |
| **Cmax (H4)** | 7.13 ± 6.32 ng/mL (75 mg 유지, 심혈관 환자) | Karazniewicz-Lada 2014 (PMID 24127209) |
| **AUCt (H4)** | 11.30 ± 9.58 ng·h/mL (75 mg 유지, 환자) | Karazniewicz-Lada 2014 (PMID 24127209) |
| **CV% (Cmax, H4)** | **~89%** (고변동성) | 계산: 6.32/7.13 × 100, PMID 24127209 |
| **CV% (AUC, H4)** | **~85%** (고변동성) | 계산: 9.58/11.30 × 100, PMID 24127209 |
| **AUC 비선형성** | 75 mg → 600 mg: AUC ~4배 증가 (비례 이상) | PMC5677184 (Jiang 2015 review) |

*주: 심혈관 환자 값. 건강인에서는 노출 더 높을 것으로 예상. PMC5677184에서는 건강인 기준 CV% (Cmax 60%, AUC 50%)로 보고.*

### 1.3 Clopidogrel 모체 및 비활성 대사체(SR26334) PK

| 파라미터 | Clopidogrel 모체 | SR26334 (비활성) |
|---------|---------------|--------------|
| Tmax | 0.5–1시간 | 0.8–1.0시간 |
| t½ | 6–8시간 (모체 추정) | **7.2–7.6시간** |
| 혈장 검출 | 거의 불가 (광범위 초회 통과 효과) | 주요 검출 형태 |
| 용량 비례성 | 선형 (50–150 mg) | 확인됨 |
| 정상 상태 | 75 mg QD 투여 시 5–7일 | 동일 |

출처: Caplain et al. 1999 (PMID 10440419)

### 1.4 CYP 효소 기여도 (활성 대사체 형성)

| CYP 효소 | 2-oxo-clopidogrel 형성 (1단계) | H4 활성 대사체 형성 (2단계) |
|---------|---------------------------|------------------------|
| **CYP2C19** | **44.9%** | **20.6%** (단, 임상 기여도 논쟁) |
| CYP3A4 | — | 39.8% |
| CYP2B6 | 19.4% | 32.9% |
| CYP1A2 | 35.8% | — |
| CYP2C9 | — | 6.79% |

출처: PMC5677184 (Jiang et al. 2015 review)

> **임상 DDI 관점**: CYP2C19는 2단계(최종 활성화) 기여도가 20.6%로 낮아 보이지만, Boulenc et al. 2012 (PMID 22004687)에서 임상 조건의 CYP2C19 기여도는 **58–72%**로 훨씬 높음. 시험관 분획 실험과 임상 결과의 차이는 기질 특이성, 효소 분획 조건 차이에 기인.

### 1.5 식이 영향 (Food Effect)

| 파라미터 | 공복 | 식후 | 임상 의의 |
|---------|------|------|---------|
| 모체 AUC | 기준 | 3.32배 증가 | 모체 노출 크게 증가 |
| H4 AUC | 기준 | ~12% 감소 | **임상적으로 유의하지 않음** |
| 혈소판 응집 억제 | 54.0% | 49.7% | 유의한 차이 없음 |
| **결론** | | **공복 또는 식후 모두 가능** | |

출처: Hurbin et al. 2012 (PMID 22128201)

**DDI 시험 설계**: 공복 투여 표준화로 변동 요인 제거 → NCT01129375, NCT01129414 모두 공복 투여 적용

---

## 2. Omeprazole PK 개요

### 2.1 약물 특성 요약

| 항목 | 내용 |
|------|------|
| 계열 | Proton Pump Inhibitor (PPI) |
| 작용 기전 | 위벽세포 H⁺/K⁺ ATPase 비가역적 억제 |
| DDI 기전 | **CYP2C19 시간 의존적 억제제(TDI)** (주요); CYP3A4 약한 억제 (부) |

### 2.2 Omeprazole PK 파라미터 (CYP2C19 유전형별)

| 파라미터 | EM (wild-type) | IM | PM |
|---------|--------------|----|----|
| AUC₀₋₁₂ₕ (단회, μg·h/L) | **713 ± 556** | 973 ± 603 | **3,652 ± 878** |
| AUC₀₋₁₂ₕ (Day 8, μg·h/L) | **1,715 ± 1,199** | 2,087 ± 1,046 | **3,669 ± 929** |
| Tmax | 1–3.5시간 | | 지연될 수 있음 |
| **t½ (EM)** | **~0.5–1시간** | 1–2시간 | >3시간 |
| 생체이용률 | 30–40% | 증가 | 크게 증가 |
| PM 배수 (단회) | 1× (기준) | 1.36× | **5.12×** |

출처: Park et al. 2017 (PMID 28378544), 한국인 건강인 기준

> **80 mg 용량 근거**: DDI 시험 표준 용량 80 mg/day. EM에서도 자기 저해(autoinhibition)를 통해 CYP2C19 포화 → worst-case DDI 달성.

### 2.3 CYP2C19 유전형에 따른 Omeprazole PK 변동성

- **PM: AUC 5배 이상 증가** (단회 투여)
- 자기 저해 효과로 반복 투여 시 EM/IM에서 노출 증가, PM 비율 감소
- **한국인 PM 빈도**: ~12–15% (서양인 2–3% 대비 약 5배 높음)

출처: Park et al. 2017 (PMID 28378544)

---

## 3. CYP2C19 기반 DDI 기전 평가

### 3.1 Omeprazole의 CYP2C19 억제 기전

| 기전 | 분류 | 근거 |
|------|------|------|
| **가역적 억제** | 경쟁적 | Ki 8.2 ± 3.6 μM (Shirasaka 2013) |
| **시간 의존적 억제 (TDI)** | **Mechanism-Based Inhibition (비가역적)** | IC₅₀ shift 4.2~10배, kinact 존재 (Ogilvie 2011, Shirasaka 2013) |
| 대사체 기여 | 가역적 + TDI | 전체 DDI의 20–50% 기여 (Shirasaka 2013) |

### 3.2 정량적 억제 파라미터 요약

| 파라미터 | 값 | 출처 |
|---------|---|------|
| IC₅₀ (CYP2C19, 직접) | **8.4 ± 0.6 μM** | Shirasaka 2013 (PMID 23620487) |
| Ki (가역적) | **8.2 ± 3.6 μM** | Shirasaka 2013 |
| KI (TDI 비활성화 반감기) | **1.7–9.1 μM** | Ogilvie 2011 (PMID 21795468) |
| kinact (최대 비활성화 속도) | **0.029–0.046 min⁻¹** | Shirasaka 2013, Ogilvie 2011 |
| IC₅₀ shift (MDI 확인) | **4.2~10배** (>2배: MDI 기준) | Ogilvie 2011, Shirasaka 2013 |
| KI (mechanism-based, Boulenc) | **8.56 μM** | Boulenc 2012 (PMID 22004687) |
| kinact (Boulenc) | **0.156 min⁻¹** | Boulenc 2012 |

*kinact 값 불일치 (0.029 vs 0.156 min⁻¹): 실험 기질, 효소 출처, 배양 조건 차이에 기인. 두 출처 모두 mechanism-based inhibition 결론은 일치.*

### 3.3 FDA 가이드라인 기준 저해 강도 분류

| 기준 | Omeprazole 값 | 판정 |
|------|-------------|-----|
| TDI 여부 (IC₅₀ shift >2배) | **4.2–10배** | **TDI 확인** |
| CYP2C19 기여도 | **58–72%** (임상) | 주요 경로 |
| 임상 DDI 관찰 | H4 AUC 40–47% 감소 | **Strong ~ Moderate** |
| FDA 기준 강한 저해제 | CYP2C19 AUC ≥5배 증가 | CYP2C19 기질 노출에 따라 분류 |

**결론**: Omeprazole은 CYP2C19에 대한 **Moderate~Strong Mechanism-Based Inhibitor** (임상 DDI 크기: H4 AUC 40–47% 감소)

### 3.4 PPI 간 CYP2C19 저해 차이 비교

| PPI | 저해 기전 | IC₅₀ | TDI | 임상 DDI (H4 AUC 감소) |
|-----|---------|------|-----|---------------------|
| **Omeprazole** | 가역 + **MDI** | ~8 μM | **있음** (4.2~10배) | **40–47%** |
| Esomeprazole | 가역 + MDI | 유사 | 있음 | 38–41% |
| Lansoprazole | 가역 | 1.2 μM | 없음 (<1.5배) | 낮음 |
| **Pantoprazole** | 가역 | 93 μM | **없음** | **14%** (유의 않음) |
| Dexlansoprazole | 가역 | — | 없음 | 최소 |

출처: Ogilvie 2011 (PMID 21795468), Angiolillo 2011 (PMID 20844485), Frelinger 2012 (PMID 22464259)

---

## 4. 유사 DDI 시험 분석 (ClinicalTrials.gov)

### 4.1 확인된 유사 시험 목록

| NCT | 시험명 요약 | 상태 | n | 설계 | Clopidogrel 용량 | PPI |
|-----|-----------|------|---|------|----------------|-----|
| **NCT01129375** | Clopidogrel 300/75 mg + Omeprazole 80 mg | Completed | 72 | Crossover, 4-arm | 300 mg LD + 75 mg MD | Omeprazole 80 mg |
| **NCT01129414** | Clopidogrel 600/150 mg + Omeprazole 80 mg | Completed | 72 | Crossover, 4-arm | 600 mg LD + 150 mg MD | Omeprazole 80 mg |
| **NCT01896557** | Omeprazole vs Ranitidine (Clopidogrel 병용) | Completed | 92 | Parallel, Phase 4 | 75 mg QD | Omeprazole 20 mg BID |
| **NCT00557921** | COGENT-1: Clopidogrel + Omeprazole 복합제 | Terminated | ~5,000 계획 | Parallel, Phase 3 | 75 mg QD | Omeprazole 20 mg |
| **NCT01094275** | CYP2C19 유전형과 Clopidogrel-Omeprazole DDI | Completed | 32 | Observational crossover | 75 mg QD | Omeprazole 20 mg |

상세: [_workspace/01_references/trials/NCT01129375.md]  
상세: [_workspace/01_references/trials/NCT01129414.md]  
상세: [_workspace/01_references/trials/NCT01896557.md]  
상세: [_workspace/01_references/trials/NCT00557921.md]  
상세: [_workspace/01_references/trials/NCT01094275.md]

### 4.2 기존 시험의 설계 특징 요약

| 설계 요소 | NCT01129375 (표준 용량) | 본 시험 방향 |
|---------|----------------------|-----------|
| 설계 | 2-period crossover, DB, PBO-controlled | 동일 방향 적용 |
| 용량 | Clopidogrel 300/75 mg + Omeprazole 80 mg | 동일 |
| 투여 조건 | 공복 | 동일 |
| 1차 평가변수 | H4 AUC₀₋₂₄ GMR | 동일 권장 |
| 채혈 | Day 5 정상 상태, 0–24시간 | 참고 |
| 대상자 수 | 72명 (4-arm) | ~24명 (2-arm) 로 단순화 가능 |
| 대상 | 건강인, CYP2C19 EM | 동일 |
| 휴약기 | ~14일 이상 | 계산 필요 |

---

## 5. PK 파라미터 기반 시험 설계 산출

### 5.1 채혈 시점 설계 (H4 활성 대사체 기준)

| 설계 요소 | 산출 방법 | 적용값 |
|---------|---------|--------|
| Tmax (H4) | 0.5–1시간 | 0.5시간 |
| Tmax × 1.5 (흡수기 상한) | 0.5h × 1.5 = 0.75h | 약 1시간 |
| 흡수기 밀집 구간 | 0–Tmax×1.5 에 집중 | **0–1시간에 포인트 집중** |
| Tmax ± 50% 핵심 구간 | 0.25–0.75시간 | 15분, 30분, 45분, 1시간 |
| 소실기 (t½=0.5–1h 기준) | 반감기 2–4배 → 1–4시간에 점진 확대 | 1.5, 2, 3, 4, 6시간 |
| 후기 포인트 | 8, 12, 24시간 (비활성 대사체/모체 병행 측정) | 8, 12, 24시간 |

**권고 채혈 시점 (H4 평가 최적화)**:
- 전혈(0h), 투여 후: **0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12, 24시간**
- 총 13 포인트 (저용량 로딩일 Day 1), 정상상태일 Day 5 동일 적용
- **0.25시간 (15분) 포인트 중요**: H4 Tmax가 매우 짧아 흡수 초기 놓치지 않도록

출처: Karazniewicz-Lada 2014 (PMID 24127209), Angiolillo 2011 (PMID 20844485)

### 5.2 절단 AUC 적용 여부

| 약물 | t½ | 절단 AUC 검토 | 결론 |
|------|----|-----------|----|
| 활성 대사체 H4 | **~0.5–1시간** | **해당 없음** (t½ << 24시간) | AUC₀₋ₜ 적용 (AUC₀₋₂₄로 충분) |
| Clopidogrel 모체 | ~6–8시간 | 해당 없음 | AUC₀₋ₜ |
| SR26334 (비활성 대사체) | ~7.6시간 | 해당 없음 | AUC₀₋ₜ |
| Omeprazole | ~0.5–1시간 (EM) | 해당 없음 | AUC₀₋ₜ |

**결론**: H4 t½ << 24시간 → **절단 AUC 적용 불필요**. AUC₀₋₂₄ = AUC₀₋∞에 충분히 근접. 1차 평가변수: **AUC₀₋₂₄** (또는 AUC₀₋ₜ, t=최후 정량 가능 시점)

### 5.3 휴약기(Washout) 산출

#### 약물별 t½ 기준 계산

| 약물 | t½ (최대값) | 이론적 최소 (10×t½) | 규제 최소 (5×t½ 또는 1주 중 긴 것) |
|-----|-----------|------------------|--------------------------------|
| Clopidogrel H4 (활성 대사체) | 1시간 | 10시간 | 7일 (1주 기준이 더 긴 경우) |
| Clopidogrel SR26334 (비활성) | 7.6시간 | 76시간 (3.2일) | 7일 |
| Omeprazole (EM) | 1시간 | 10시간 | 7일 |
| **혈소판 수명** | **~10일** | — | **혈소판 교체 기간 고려** |

#### 휴약기 산출 근거 표

| 항목 | 계산 과정 | 값 |
|------|---------|---|
| 약물 세척 기준 (t½ 기반) | 10 × 7.6h (SR26334 최장) = 76시간 → 7일로 올림 | **7일** |
| CYP2C19 효소 재합성 기간 | MDI (mechanism-based): 새 효소 합성까지 3–7일 필요 | **7–14일** |
| 혈소판 수명 기반 | 비가역적 P2Y12 차단 → 새 혈소판 교체 ~10일 필요 | **10–14일** |
| 최종 권고 휴약기 | 가장 긴 요소: 혈소판 수명 + 여유 | **≥14일 (2주)** |

#### 잔류 농도 추정 (14일 후)

| 약물 | 14일 후 잔류 분율 | 절대값 추정 |
|------|--------------|----------|
| SR26334 (t½=7.6h) | 2^(-336/7.6) ≈ 0% | 무시 가능 |
| Omeprazole (t½=1h) | 2^(-336/1) ≈ 0% | 0 |
| CYP2C19 효소 활성 | ~7–14일 후 기저 회복 | 정상화 |

**최종 권고**: 휴약기 **≥14일** (혈소판 수명 10일 + 4일 여유) — 기존 유사 시험 (NCT01129375, NCT01129414) 동일 적용

> **중요**: 본 시험에서 휴약기는 단순 약물 t½ 기반(7일)으로는 부족함. CYP2C19 MDI 회복(효소 재합성 3–7일)과 혈소판 수명(~10일)이 결정 인자. 14일이 실용적 하한.

출처: Ogilvie 2011 (PMID 21795468), Angiolillo 2011 (PMID 20844485)

---

## 6. 용량 근거 정리 (DDI 시험 용량)

### 6.1 Clopidogrel 용량 — 허가 용량 기반

| 용량 | 근거 | 임상 용도 |
|------|------|---------|
| **로딩 300 mg** | FDA 허가 용량 (Plavix NDA 020839); ACS 적응증 | 정상 상태 신속 달성 |
| **유지 75 mg QD** | FDA 허가 유지 용량; 만성 항혈소판 치료 표준 | 정상 상태 유지 |

**DDI 시험 투여 일정**: Day 1: 300 mg 로딩, Day 2–5: 75 mg QD  
- 5일간 투여 시 정상 상태(5–7일 기준) 도달 가능  
- Day 5가 PK 평가 적정 시점 (NCT01129375, NCT01129414 동일)

참고: NCT01129375, Angiolillo 2011 (PMID 20844485)

### 6.2 Omeprazole 용량 — DDI 최대화(worst-case) 근거

| 용량 | 근거 |
|------|------|
| **80 mg/day** | DDI 시험 표준 용량; 최대 CYP2C19 억제 달성 (worst-case DDI 조건) |
| 임상 용량 (20 mg) | 일반 치료 용량; 본 시험 목적에 insufficient |

**80 mg 근거**:
1. 기존 유사 시험(NCT01129375, NCT01129414) 동일 용량 적용
2. Angiolillo 2011에서 80 mg으로 H4 AUC 40–47% 감소 입증
3. 자기 저해로 EM에서도 CYP2C19 포화 달성 → 유전형 무관한 최대 억제 조건
4. FDA 임상 약물상호작용 가이드라인(2020): DDI 시험에서 maximal inhibitor dose 사용 권고

---

## 7. 핵심 문헌 요약

| PMID | 저자 | 연도 | 핵심 기여 | 파일 |
|------|------|------|---------|------|
| **20844485** | Angiolillo et al. | 2011 | **핵심**: Omeprazole 80 mg → H4 AUC 40–47% 감소; 4개 crossover 시험 | [PMID_20844485.md] |
| **21795468** | Ogilvie et al. | 2011 | Omeprazole MDI 기전 (IC₅₀ shift 4.2배, KI 1.7–9.1 μM) | [PMID_21795468.md] |
| **23620487** | Shirasaka et al. | 2013 | IC₅₀ 8.4 μM, Ki 8.2 μM, kinact 0.029 min⁻¹, 대사체 기여 20–50% | [PMID_23620487.md] |
| **22004687** | Boulenc et al. | 2012 | CYP2C19 기여도 58–72%, MDI KI 8.56 μM, 유전형별 예측 | [PMID_22004687.md] |
| **19106084** | Mega et al. (NEJM) | 2009 | CYP2C19 reduced allele → H4 AUC 32.4% 감소; FDA 블랙박스 근거 | [PMID_19106084.md] |
| **22128201** | Hurbin et al. | 2012 | 식이 영향 없음 (H4 12% 감소만); 공복 투여 표준화 근거 | [PMID_22128201.md] |
| **24127209** | Karazniewicz-Lada et al. | 2014 | H4 PK: Cmax 7.13 ng/mL, AUC 11.30 ng·h/mL, CV% ~85–89% | [PMID_24127209.md] |
| **29060457** | Tangamornsuksan et al. | 2017 | CYP2C19 경쟁적 억제 PK-DDI 모델; 6개 임상 데이터셋 검증 | [PMID_29060457.md] |
| **28378544** | Park et al. | 2017 | 한국인 Omeprazole PK; EM t½ ~0.5–1h, PM 5.12배 AUC 증가 | [PMID_28378544.md] |
| **26071277** | Simon et al. | 2015 | PK-PD Sigmoid Emax 모델; Omeprazole + CYP2C19*2 상승 작용 | [PMID_26071277.md] |
| **10440419** | Caplain et al. | 1999 | Clopidogrel 기초 PK; SR26334 t½ 7.2–7.6h, 라벨 근거 | [PMID_10440419.md] |

---

## 8. biostatistician을 위한 PK 파라미터 요약 (Sample Size 계산용)

### 활성 대사체 H4 (1차 평가변수 기준)

| 파라미터 | 값 | 출처 |
|---------|---|------|
| **변동 계수 CV% (AUC)** | **50–89%** | PMID 24127209 (환자), PMC5677184 (건강인: ~50%) |
| **권장 CV% (DDI 시험용)** | **~50–60%** (건강인 CYP2C19 EM 기준) | PMC5677184 |
| **예상 GMR (Omeprazole 80 mg 효과)** | **0.53–0.60** (40–47% 감소) | PMID 20844485 |
| **예상 AUC 감소** | **40–47%** | PMID 20844485 |
| **1차 평가변수** | AUC₀₋₂₄ GMR (H4 활성 대사체) | |
| **동등성 기준 (DDI 판정)** | GMR 90% CI: 80–125% 범위 이탈 여부 확인 | FDA DDI Guidance 2020 |

### 시험 설계 핵심 수치

| 항목 | 권고값 | 근거 |
|------|--------|------|
| 대상자 수 (초안) | ~20–24명 (CYP2C19 EM) | NCT01094275 (32명), Angiolillo 각 시험 (60–72명) 참고 |
| 탈락률 | 10–15% 고려 | 일반 Phase 1 관행 |
| 최종 목표 | **완료 20명** | |
| 채혈 포인트 | Day 1 + Day 5 각각 13 포인트 | H4 t½ ~0.5–1h 고려 |
| 투여 조건 | 공복 | PMID 22128201 |
| 휴약기 | **≥14일** | 혈소판 수명 + MDI 회복 |

---

## 9. 참고 문헌 전체 목록

### 임상시험 (ClinicalTrials.gov)

1. NCT01129375. Interaction Study of Clopidogrel 300/75 mg Given Alone or Concomitantly With Omeprazole 80 mg in Healthy Subjects. Sanofi. 2009. → [상세: 01_references/trials/NCT01129375.md]
2. NCT01129414. Interaction Study of Clopidogrel 600/150 mg Given Alone or Concomitantly With Omeprazole 80 mg in Healthy Subjects. Sanofi. 2009. → [상세: 01_references/trials/NCT01129414.md]
3. NCT01896557. Ranitidin Versus Omeprazole in Patients Taking Clopidogrel. University of Sao Paulo. 2011. → [상세: 01_references/trials/NCT01896557.md]
4. NCT00557921. COGENT-1: Clopidogrel and the Optimization of Gastrointestinal Events. Cogentus Pharmaceuticals. 2007. → [상세: 01_references/trials/NCT00557921.md]
5. NCT01094275. Role of CYP2C19 Polymorphism in the Drug Interaction Between Clopidogrel and Omeprazole. Methodist Hospital Research Institute. 2010. → [상세: 01_references/trials/NCT01094275.md]

### PubMed 문헌

6. Angiolillo DJ et al. Differential effects of omeprazole and pantoprazole on the pharmacodynamics and pharmacokinetics of clopidogrel. Clin Pharmacol Ther. 2011;89(1):65-74. PMID: 20844485. → [상세: 01_references/literature/PMID_20844485.md]
7. Ogilvie BW et al. The proton pump inhibitor, omeprazole, but not lansoprazole or pantoprazole, is a metabolism-dependent inhibitor of CYP2C19. Drug Metab Dispos. 2011;39(11):2020-33. PMID: 21795468. → [상세: 01_references/literature/PMID_21795468.md]
8. Shirasaka Y et al. Inhibition of CYP2C19 and CYP3A4 by omeprazole metabolites and their contribution to drug-drug interactions. Drug Metab Dispos. 2013;41(7):1414-24. PMID: 23620487. → [상세: 01_references/literature/PMID_23620487.md]
9. Boulenc X et al. Effects of omeprazole and genetic polymorphism of CYP2C19 on the clopidogrel active metabolite. Drug Metab Dispos. 2012;40(1):96-104. PMID: 22004687. → [상세: 01_references/literature/PMID_22004687.md]
10. Mega JL et al. Cytochrome P-450 polymorphisms and response to clopidogrel. N Engl J Med. 2009;360(4):354-62. PMID: 19106084. → [상세: 01_references/literature/PMID_19106084.md]
11. Hurbin F et al. Clopidogrel pharmacodynamics and pharmacokinetics in the fed and fasted state. J Clin Pharmacol. 2012;52(2):273-85. PMID: 22128201. → [상세: 01_references/literature/PMID_22128201.md]
12. Karaźniewicz-Łada M et al. Clinical pharmacokinetics of clopidogrel and its metabolites in patients with cardiovascular diseases. Clin Pharmacokinet. 2014;53(2):155-64. PMID: 24127209. → [상세: 01_references/literature/PMID_24127209.md]
13. Tangamornsuksan W et al. A pharmacokinetic model of drug-drug interaction between clopidogrel and omeprazole at CYP2C19. EMBC 2017. PMID: 29060457. → [상세: 01_references/literature/PMID_29060457.md]
14. Park S et al. Effects of CYP2C19 Genetic Polymorphisms on PK/PD Responses of Omeprazole in Korean Healthy Volunteers. J Korean Med Sci. 2017;32(4):729-736. PMID: 28378544. → [상세: 01_references/literature/PMID_28378544.md]
15. Simon N et al. Omeprazole, pantoprazole, and CYP2C19 effects on clopidogrel pharmacokinetic-pharmacodynamic relationships. Eur J Clin Pharmacol. 2015;71(10):1185-91. PMID: 26071277. → [상세: 01_references/literature/PMID_26071277.md]
16. Caplain H et al. Pharmacokinetics of clopidogrel. Semin Thromb Hemost. 1999;25 Suppl 2:25-8. PMID: 10440419. → [상세: 01_references/literature/PMID_10440419.md]

---

## 10. 주요 불확실성 및 한계

| 항목 | 내용 |
|------|------|
| H4 절대값 | 기존 PK 데이터 대부분이 심혈관 환자 기준. 건강인 CYP2C19 EM에서의 절대값은 더 높을 것으로 예상 |
| CV% 불확실성 | 환자 기준 CV% ~85–89% vs 건강인 기준 ~50–60% → biostatistician에게 보수적으로 60% 권고 |
| MDI kinact 불일치 | Boulenc 0.156 vs Shirasaka 0.029 min⁻¹ — 두 출처 모두 MDI 기전 확인, 기전 결론은 일치 |
| CYP 기여도 논쟁 | 분획 실험 (~21%) vs 임상 (~58–72%): 임상 조건에서 CYP2C19 기여도가 훨씬 높음 |
| 한국인 데이터 | Clopidogrel H4 한국인 기준 PK 데이터 부족 — 서양인 데이터 적용 |
| Open Access 한계 | 일부 논문 초록 기반 추출 (전문 미접근) |

---

*보고서 완료: 2026-04-14*  
*작성: Clinical Pharmacologist Agent (claude-sonnet-4-6)*
