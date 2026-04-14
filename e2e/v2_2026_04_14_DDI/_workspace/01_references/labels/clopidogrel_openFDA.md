# Clopidogrel — openFDA 메타데이터

## 출처
- 약물명: Clopidogrel Bisulfate (Plavix)
- API: openFDA drug/drugsfda + drug/label
- 조회 URL (drugsfda): https://api.fda.gov/drug/drugsfda.json?search=openfda.generic_name:clopidogrel&limit=5
- 조회 URL (label): https://api.fda.gov/drug/label.json?search=openfda.application_number:NDA020839&limit=1
- 조회일: 2026-04-14

---

## 허가 정보 (drugsfda)

| 항목 | 내용 |
|------|------|
| NDA 번호 | **NDA020839** |
| 브랜드명 | PLAVIX |
| 신청사 (Sponsor) | SANOFI AVENTIS US |
| 최초 승인일 | 1997-11-17 (ORIG-1 submission_status_date) |
| 현재 상태 | Prescription |

### 제네릭 허가 이력 (ANDA)

| Application | 신청사 | ORIG-1 승인일 |
|------------|--------|-------------|
| ANDA076999 | TEVA | 2012-05-17 |
| ANDA203632 | ALKEM LABS LTD | 2023-12-08 |
| ANDA090494 | SUN PHARM | 2012-05-17 |
| ANDA090844 | TORRENT PHARMS LTD | 2012-05-17 |

**비고**: Clopidogrel 특허 만료 후 2012년부터 다수의 제네릭 허가. 현재 본 시험 약물(Clopidogrel bisulfate 75 mg 정제)은 NDA020839 기반 제품.

---

## 라벨 핵심 정보 (openFDA label, NDA020839)

### Boxed Warning (블랙박스 경고)

**"DIMINISHED ANTIPLATELET EFFECT IN PATIENTS WITH TWO LOSS-OF-FUNCTION ALLELES OF THE CYP2C19 GENE"**

- CYP2C19를 통한 활성 대사체 전환에 효과 의존
- PM 식별을 위한 유전형 검사 이용 가능
- **"CYP2C19 poor metabolizer로 확인된 환자에게 다른 P2Y12 억제제 사용 고려"**

### CYP2C19 인종별 PM 비율 (라벨 기재)

| 인종 | PM 비율 |
|------|--------|
| White | ~2% |
| Black | ~4% |
| Chinese | ~14% |

### Drug Interactions 핵심 (Section 7)

| 병용약 | 상호작용 | 권고 |
|--------|---------|------|
| **Omeprazole / Esomeprazole** | CYP2C19 억제 → 활성 대사체 ~45% 감소, 혈소판 억제 ~47% 감소 | **병용 금지 (Avoid)** |
| Dexlansoprazole, Lansoprazole, Pantoprazole | 영향 적음 | 상대적으로 덜 우려 |
| Rifampin (CYP2C19 유도제) | 활성 대사체 증가 → 출혈 위험 | 강한 CYP2C19 유도제 병용 금지 |
| NSAIDs | 위장관 출혈 위험 증가 | 주의 |
| Repaglinide | CYP2C8 억제 → repaglinide 노출 3.9~5.1배 증가 | 용량 감소 필요 |

### 임상적 DDI 데이터

- Omeprazole 80 mg 병용 시: AUC(활성 대사체) 약 45% 감소
- **12시간 간격 투여도 동일한 효과 감소** — 투여 시간 분리로 회피 불가
- 이 데이터가 본 시험의 양성 대조 또는 기존 알려진 DDI의 재확인 근거

---

## 약물유전체(PG) 섹션 추출 — Translational-Scientist 인계

**[translational-scientist 참고 자료 — PG 섹션]**

openFDA에서 추출된 Clopidogrel의 PG 관련 정보:

1. **블랙박스 경고 전문**: CYP2C19 two loss-of-function alleles (PM) → 항혈소판 효과 현저 감소
2. **섹션 5.1 (Warnings)**: "Clopidogrel is a prodrug. Inhibition of platelet aggregation by clopidogrel is entirely due to an active metabolite. **The metabolism of clopidogrel to its active metabolite can be impaired by genetic variations in CYP2C19.**"
3. **섹션 12.2**: PM 비율 인종별 데이터 (White 2%, Black 4%, Chinese 14%)
4. **CYP2C19 표현형 분류**: PM = two loss-of-function alleles; IM = one; EM = none
5. **CPIC Level A**: CYP2C19–Clopidogrel (별도 CPIC 데이터 참조 필요)
6. **FDA Table of Pharmacogenomic Biomarkers**: Clopidogrel 등재 (CYP2C19 — Affects Response)

**[translational-scientist 담당 사항]**:
- 한국인 CYP2C19 loss-of-function allele (*2, *3) 빈도 분석
- 표현형별(EM/IM/PM) 용량 조절 근거 (CPIC 가이드라인 세부 내용)
- PharmGKB/CPIC API를 통한 최신 권고 확인

---

## FDA Table of Pharmacogenomic Biomarkers in Drug Labeling

| 약물명 | 바이오마커 | 라벨 섹션 | 효과 유형 |
|--------|---------|----------|---------|
| Clopidogrel (Plavix) | CYP2C19 | 블랙박스, 섹션 2, 5.1, 12.2 | Affects Response |

출처: FDA Table of Pharmacogenomic Biomarkers in Drug Labeling (https://www.fda.gov/medical-devices/precision-medicine/table-pharmacogenomic-biomarkers-drug-labeling)

---

## 참고 문헌

- openFDA. Drug/Drugsfda. NDA020839 — Clopidogrel Bisulfate (Plavix). https://api.fda.gov/drug/drugsfda.json?search=openfda.generic_name:clopidogrel
- openFDA. Drug/Label. NDA020839. https://api.fda.gov/drug/label.json?search=openfda.application_number:NDA020839&limit=1
- [Clopidogrel Bisulfate (Plavix) FDA Prescribing Information, Sanofi Aventis US, NDA020839, 최초 승인 1997-11-17]
