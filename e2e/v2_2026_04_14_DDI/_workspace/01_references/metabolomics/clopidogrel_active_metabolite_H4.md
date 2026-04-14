# Clopidogrel 활성 대사체 H4 (Clopidogrel Active Metabolite, CLOP-AM)

## 기본 정보

| 항목 | 내용 |
|------|------|
| IUPAC명 | (Z)-Methyl 2-(2-chlorophenyl)-2-(6,7-dihydrothieno[3,2-c]pyridin-5(4H)-yl)-2-(hydroxy)-acetate |
| 별칭 | H4, CLOP-AM, CAM (Clopidogrel Active Metabolite), thiol metabolite |
| 분자량 | ~355.8 Da (thiol form), ~518 Da (BMAP-유도체화 후) |
| 특성 | 반응성 thiol 기 포함 → 생체 내 빠른 불활성화 |
| 측정 방법 | LC-MS/MS (유도체화 필수) |
| 역할 | P2Y12 수용체와 disulfide 결합 → 비가역적 차단 |

## 대사체 H4의 형성 경로

```
Clopidogrel (prodrug)
    ↓ CYP1A2 (소량), 에스테라제 (주요 — 불활성 경로)
2-oxo-clopidogrel (중간체)
    ↓ CYP2C19 (주요), CYP3A4 (보조), PON1 (혈장)
H4 (활성 thiol 대사체, ~15% 생성률)
    ↓ P2Y12 수용체 cysteine에 공유결합
비가역적 수용체 차단 → ADP 유도 혈소판 응집 억제
```

CYP2C19가 2-oxo-clopidogrel → H4 전환의 주 효소 (rate-limiting step). Omeprazole은 이 단계를 억제.

## 불안정성 및 유도체화 필요성

H4는 thiol 기를 가진 반응성 대사체로:
- 생체 내: 혈장 단백질·글루타티온과 결합 → 빠른 불활성화 (t½ < 30분)
- 시료 채취 후: 혈장 내 빠른 분해 (채혈 후 즉시 처리 필요)
- 4°C에서도 수 시간 내 분해 가능

**해결책: 2-bromo-3'-methoxyacetophenone (BMAP) 유도체화**
- BMAP가 thiol 기와 반응 → 안정한 thioether 결합 형성 (CAM-D, 유도체화 활성 대사체)
- 안정성: -80°C에서 4개월 (PMID: 18829199), 실온에서 1주 (PMID: 22169056)

## LC-MS/MS 측정법 (PMID: 18829199 기반)

### 시료 처리 프로토콜
1. 채혈: K2EDTA 진공관 (얼음 위 보관)
2. **즉시** BMAP 용액 (in acetonitrile) 첨가 — 채혈 후 5분 이내
3. 원심분리 (4°C, 2,000 g, 10분) → 상층액 취득
4. Protein precipitation (아세토니트릴 3배 부피 첨가)
5. -80°C 보관 (분석 전까지)

### 분석 조건 (Takahashi 2008, PMID: 18829199)
- **컬럼**: C18 역상 컬럼 (50 × 2.1 mm, 1.7 μm 입자)
- **이동상**: 0.1% formic acid in water / acetonitrile gradient
- **이온화**: ESI 양이온 모드
- **MRM transition (BMAP-유도체화 H4)**: m/z 520→271 (정량), m/z 520→157 (확인)
- **실행 시간**: ~1.5–5분

### 검증 파라미터 (PMID: 18829199)
| 파라미터 | 결과 |
|---------|------|
| LLOQ | 0.5 ng/mL |
| ULOQ | 250 ng/mL |
| 직선성 (r²) | ≥ 0.99 |
| 정확도 | 상대오차 ≤ 12% |
| 정밀도 (CV) | ≤ 6% |
| 회수율 | 85–105% |
| 안정성 (-80°C) | 4개월 |

### 검증 파라미터 (추가 참조: PMID: 22169056)
- 교정 범위: 0.01–50 ng/mL (parent clopidogrel), 0.1–150 ng/mL (CAMD)
- 실행 시간: 1.5분 (고속 분석)
- H4 외 동시 측정 가능: Clopidogrel parent, 2-oxo-clopidogrel, clopidogrel carboxylic acid (H1-H3)

## 시료 채취·보관 요건 (시험 설계 적용)

- **채혈 용기**: K2EDTA 또는 heparin (citrate 튜브는 BMAP 반응 방해 가능)
- **BMAP 첨가**: 채혈 후 **5분 이내** (현장 처리 프로토콜 필수)
- **처리 온도**: 얼음 위 (4°C 이하)
- **보관**: 유도체화 후 -80°C (분석 전)
- **운반**: 드라이아이스 (-80°C)

**임상시험 특별 고려사항**: BMAP 유도체화 시약과 처리 키트를 채혈 현장에 준비. 전담 인력의 즉각적 처리 프로토콜 SOP 수립 필수.

## DDI 시험에서의 대사체학적 의의

### 1차 PK 지표 (clinical-pharmacologist 담당)
- H4 AUC₀₋ₜ, Cmax: Omeprazole DDI의 1차 PK 목적 (GMR 평가)

### TS 담당 (대사체학 측면)
- **H4 측정법 검증**: BMAP 유도체화 LC-MS/MS 분석법의 기술적 상세 제공
- **시료 안정성 근거**: 유도체화 필요성, 현장 처리 SOP 근거
- **H4 vs. PRU 상관관계 (PK-PD 연계)**: H4 AUC ↓ → PRU ↑ (항혈소판 효과 감소)
  - Simon et al. (2015): sigmoid Emax 모델, Emax 56%, EC50 15.9 h·μg/L (PMID: 26071277)

### 내인성 바이오마커 (CYP2C19 표현형 확인 보조 — 해당 시)
- **Omeprazole 자체 PK**: Omeprazole은 CYP2C19 기질이기도 함 → CYP2C19 기능적 표현형의 간접 지표
- **[주의]**: 본 시험의 DDI 방향은 Omeprazole → Clopidogrel (Clopidogrel이 victim)

## 내인성 DDI 바이오마커 (CYP2C19 외)

본 시험의 DDI 기전은 CYP2C19 억제이므로 일반적인 CYP3A/OATP 내인성 바이오마커는 해당 없음. 단, 아래 마커는 적용 불가:
- 4β-hydroxycholesterol: CYP3A4 활성 지표 — 본 시험 불해당
- Coproporphyrin I: OATP1B 활성 지표 — 본 시험 불해당
- 6β-hydroxycortisol: CYP3A 유도 지표 — 본 시험 불해당

**본 시험 적용 대사체**: Clopidogrel H4 (BMAP 유도체화) 자체가 핵심 대사체이자 PD 연계 지표

## 출처

- PMID: 18829199 — Takahashi M et al. J Pharm Biomed Anal. 2008. (LC-MS/MS validation, BMAP derivatization)
- PMID: 22169056 — Ferreiro JL et al. J Chromatogr B. 2012. (fast UHPLC-MS/MS)
- PMID: 26071277 — Simon N et al. Eur J Clin Pharmacol. 2015. (PK-PD modeling, sigmoid Emax)
- PMC: 9002156 — 2022 (simultaneous determination of clopidogrel and metabolites)
- Advion: https://www.advion.com/advion-developing-h4-method-for-clopidogrel-and-the-inactive-metabolites/
