# Omeprazole — openFDA 메타데이터

## 출처
- 약물명: Omeprazole (Prilosec 및 제네릭)
- API: openFDA drug/drugsfda + drug/label
- 조회 URL: https://api.fda.gov/drug/drugsfda.json?search=openfda.brand_name:PRILOSEC&limit=5
- 보완 URL: https://api.fda.gov/drug/label.json?search=openfda.generic_name:omeprazole&limit=1
- 조회일: 2026-04-14

---

## 허가 정보 (drugsfda)

### Prilosec 브랜드 관련 허가

| Application | 신청사 | 브랜드 | ORIG-1 승인일 |
|------------|--------|--------|-------------|
| NDA021229 | ASTRAZENECA | Prilosec OTC/관련 | 2003-06-20 |
| NDA022056 | AZURITY | 관련 제품 | 2008-03-20 |
| ANDA206582 | P AND L | 제네릭 | 2020-06-01 |

**비고**: AstraZeneca의 원개발 Prilosec(omeprazole) NDA019810은 별도 조회 필요. 2026-04-14 기준 검색에서 직접 확인되지 않음. [원개발 NDA 번호 확인 필요]

### 제네릭 omeprazole ANDA (대표 목록)

| Application | 신청사 | ORIG-1 승인일 |
|------------|--------|-------------|
| ANDA078490 | DR REDDYS LABS LTD | 2009-04-17 |
| ANDA217784 | DR REDDYS | 2024-05-09 |
| ANDA205545 | AJANTA PHARMA LTD | 2016-07-27 |
| ANDA207476 | SCIIGEN PHARMS | 2016-12-06 |

---

## 라벨 핵심 정보 (openFDA label)

**조회 결과**: openFDA 검색에서 반환된 라벨은 OTC(일반의약품) omeprazole 기반으로, 처방약 상세 정보(Drug Interactions, Clinical Pharmacology 섹션)가 부족함. DailyMed setid: ded0df8b-1813-4595-ac2b-5499704bfd48에서 처방약 라벨 수집 완료 (omeprazole_DailyMed.md 참조).

### 핵심 확인 사항

| 항목 | 내용 |
|------|------|
| Clopidogrel 병용 경고 | **"Concomitant use of omeprazole 80 mg results in reduced plasma concentrations of the active metabolite of clopidogrel and a reduction in platelet inhibition"** |
| 권고 | **"Avoid concomitant use with omeprazole. Consider use of alternative anti-platelet therapy."** |
| CYP2C19 TDI | Omeprazole은 CYP2C19의 time-dependent inhibitor → autoinhibition → 비선형 PK |
| 자가 억제 | 반복 투여 시 40 mg: Cmax 118% 증가, AUC 175% 증가 |

### CYP2C19 관련 추가 DDI

| 병용약 | 상호작용 기전 | 결과 |
|--------|-----------|------|
| Citalopram | CYP2C19 억제 → 노출 증가 | QT 연장 위험, 최대 20 mg/일 제한 |
| Cilostazol | CYP2C19 억제 | 50 mg bid 감량 |
| Phenytoin | CYP2C19 억제 | 농도 증가, 모니터링 |
| Diazepam | CYP2C19 억제 | AUC 증가 |

### CYP3A4 관련 DDI

| 약물 | 기전 | 결과 |
|------|------|------|
| Rilpivirine | pH 상승 + CYP3A4 | 흡수 감소 → 금기 |
| Atazanavir | pH 상승 | 노출 감소 → 병용 금지 |
| Voriconazole | CYP2C19/3A4 상호 억제 | 노출 현저 증가 → 용량 감소 고려 |
| St. John's Wort | CYP2C19/3A4 유도 | Omeprazole 노출 감소 |

---

## Pharmacogenomics 섹션

**openFDA label 조회 결과**: `pharmacogenomics` 필드 없음.

CYP2C19 관련 정보는 `clinical_pharmacology` 섹션에 포함:

> "Omeprazole is extensively metabolized by the cytochrome P450 (CYP) enzyme system. **The major pathway is through CYP2C19**, which forms hydroxyomeprazole. A secondary pathway is through CYP3A4, which forms omeprazole sulfone."
>
> "In patients who are **CYP2C19 poor metabolizers** (PM), the primary metabolic pathway is altered... **Systemic exposure is significantly higher** in PM compared to extensive metabolizers."

**PM 관련 임상 함의**:
- PM에서 omeprazole 노출 크게 증가 → CYP2C19 억제 효과도 더 강함
- 본 시험에서 PM 대상자가 포함되면 DDI 크기가 EM보다 더 클 가능성
- **→ CYP2C19 표현형 분층 분석 필수적 이유**

**[translational-scientist 인계 사항]**: Omeprazole의 CYP2C19 TDI 특성이 표현형에 따라 달라지는 기전, 한국인 PM에서의 약동학 특성, CPIC에서의 omeprazole-CYP2C19 상호작용 권고 확인

---

## FAERS 이상반응 (참고)

openFDA FAERS 데이터 직접 조회 미수행 (DailyMed 라벨 이상반응 섹션으로 대체).

DailyMed 라벨(omeprazole_DailyMed.md) 기반 주요 이상반응:
- 두통, 복통, 설사, 오심, 구토
- 저마그네슘혈증 (장기 투여 시)
- CDAD (C. difficile 연관 설사)

---

## 본 시험 설계에의 시사점

| 항목 | 내용 |
|------|------|
| 시험 용량 선택 근거 | Omeprazole 80 mg/일 — 라벨에서 이 용량으로 활성 대사체 현저 감소 확인. Worst-case DDI 평가를 위한 최적 용량 |
| 정상상태 전투여 | TDI autoinhibition 특성 → 5~7일 전투여로 정상상태 도달 후 clopidogrel 투여 |
| CYP2C19 표현형 | PM에서 omeprazole 자체 농도 상승 → DDI 크기 더 커질 가능성 → EM 대상자 선별 또는 층화 분석 필수 |
| Trough 측정 | 투여 전 omeprazole trough 농도 측정으로 정상상태 확인 |

---

## 참고 문헌

- openFDA. Drug/Drugsfda — Omeprazole (Prilosec). https://api.fda.gov/drug/drugsfda.json?search=openfda.brand_name:PRILOSEC
- openFDA. Drug/Label — Omeprazole. https://api.fda.gov/drug/label.json?search=openfda.generic_name:omeprazole&limit=1
- [Omeprazole (Prilosec) FDA Prescribing Information, AstraZeneca, NDA019810 — 원본 NDA 확인 필요]
