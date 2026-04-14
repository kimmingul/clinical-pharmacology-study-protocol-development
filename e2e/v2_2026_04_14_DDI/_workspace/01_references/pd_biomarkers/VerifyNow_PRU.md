# VerifyNow P2Y12 Assay — P2Y12 Reaction Units (PRU)

## 기본 정보

| 항목 | 내용 |
|------|------|
| 측정 대상 | P2Y12 수용체 매개 혈소판 응집 억제 |
| 시료 | 전혈 (whole blood), citrate 항응고 |
| 분석 방법 | 점탄성 혈소판 기능 분석 (turbidimetric optical method) |
| 단위 | PRU (P2Y12 Reaction Units) |
| 정상 범위 | 182–335 PRU (P2Y12 억제제 미투여 시) |
| 치료 범위 | 95–208 PRU (Clopidogrel 치료 목표) |
| 검증 상태 | FDA 510(k) 허가 완료 (K051231), 완전 검증 |

## 작동 원리

VerifyNow P2Y12 assay는 ADP와 prostaglandin E1 (PGE1)을 혼합한 시약으로 혈소판을 자극한다.

- **ADP**: P2Y12 수용체를 자극하여 혈소판 응집 유도
- **PGE1**: P2Y1 수용체 하류 신호를 억제 → P2Y12 특이적 측정 가능
- **fibrinogen-coated beads**: 활성화된 GPIIb/IIIa에 결합 → 광학적 응집 신호 생성
- PRU 값: 광투과율 변화 속도 및 정도 기반 산출

이 방식으로 P2Y12 수용체 억제제(clopidogrel, prasugrel, ticagrelor 등)에 대한 **특이적** 혈소판 억제 측정이 가능하다.

## 시험약과의 연관성 (Clopidogrel + Omeprazole DDI)

- Clopidogrel 활성 대사체(H4)가 P2Y12 수용체에 비가역적으로 결합 → PRU 감소
- Omeprazole CYP2C19 억제 → H4 형성 감소 → PRU 증가 (혈소판 억제 약화)
- PRU 변화는 **Omeprazole DDI의 PD 효과를 직접 반영**
- 연구 근거: Omeprazole 병용 시 PRU ~217 (vs. 단독 투여 ~196), HPR (>208 PRU) 유병률 48% vs. 33% (famotidine) (PMID: 23630016)

## 임상 컷오프 기준

| 범주 | PRU 기준 | 임상 의미 |
|------|---------|---------|
| HPR (High Platelet Reactivity) | > 208 PRU | Clopidogrel 저항성; 허혈성 사건 위험 증가 |
| 치료 목표 | 95–208 PRU | 적절한 항혈소판 억제 |
| LPR (Low Platelet Reactivity) | < 95 PRU | 과도한 억제; 출혈 위험 증가 |

- 208 PRU 컷오프: VerifyNow package insert 기준, P2Y12 억제제 효과 감지 민감도·특이도 최적점
- 단, 뇌혈관 질환 등 다른 적응증에서는 최적 컷오프가 다를 수 있음 (190, 235 PRU 제안도 있음)

## 측정 방법 상세

- **채혈 방법**: 3.2% sodium citrate 진공관, 전혈 2.7 mL
- **검사 시점**: Clopidogrel 복용 후 2–4시간 (Tmax 기반) 또는 정상 상태 (steady-state)
- **결과 산출 시간**: ~5분 (point-of-care 가능)
- **간섭 물질**: GP IIb/IIIa 억제제(tirofiban, eptifibatide) — 2일 이내, abciximab — 2주 이내 투여 시 결과 부정확
- **헤마토크릿 영향**: Hct < 20% 또는 > 60% 시 결과 신뢰도 감소 (PMID: 24118870)
- **변동 계수(CV)**: < 8% (within-run precision; PMID: 16845449)

## DDI 평가에서의 활용

- **1차 PD 지표**: PRU (DDI 시험 2차 목적)
- **2차 PD 지표**: %IPA (Percent Inhibition of Platelet Aggregation) = (기저 PRU - 치료 후 PRU) / 기저 PRU × 100
- 측정 시점 권고:
  - 기저 (Pre-dose Day 1, Clopidogrel 투여 전)
  - Clopidogrel 단독 정상 상태 (Day 5–7, 투여 후 2–4 hr)
  - Omeprazole 병용 정상 상태 (Day 12–14, 투여 후 2–4 hr)

## 민감도/특이도

- LTA (ADP 5 μmol/L)와의 상관계수: r = 0.82–0.90 (문헌에 따라 다양)
- 항혈소판 억제 측정 민감도: 93–95% (PMID: 16845449)
- CYP2C19 genotype별 PRU 변화를 반영하는 능력 확인 (PMID: 22464259)

## 한계

- 헤마토크릿에 의한 측정값 편이 존재
- GP IIb/IIIa 억제제 사용 시 결과 부정확
- 컷오프 값의 임상 적응증별 차이
- PRU 208 컷오프가 건강한 지원자가 아닌 ACS/PCI 환자 데이터 기반

## 출처

- PMID: 16845449 — Malinin A et al. Methods Find Exp Clin Pharmacol. 2006;28(5):315-322. (VerifyNow P2Y12 validation)
- PMID: 23630016 — Arbel Y et al. Clin Cardiol. 2013 (Omeprazole vs famotidine vs pantoprazole PRU comparison)
- PMID: 22464259 — Frelinger AL et al. J Am Coll Cardiol. 2012;59(14):1304-11. (PPI comparison, healthy volunteers)
- PMID: 24118870 — Kakouros N et al. J Thromb Haemost. 2013. (Hematocrit interference)
- FDA 510(k): K051231 (VerifyNow P2Y12 cartridge)
