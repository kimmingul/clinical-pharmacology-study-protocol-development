# Biostatistician 리뷰

## 검토 요약

- **검토 일시**: 2026-04-14
- **대상 문서**: 계획서 CLO-OME-DDI-001 v1.0 (`_workspace/03_protocol_draft.md`)
- **참조 문서**: `_workspace/00_input/statistical_design.md`
- **검토 초점**: B.10 Statistical Considerations (통계적 고려사항) 전체

---

## 발견 사항

### [Major-1] GMR=0.60 시나리오에서 검정력 0.72 — 임계 한계에 대한 대응 계획 부재

- **심각도**: Major
- **위치**: §B.10.1, 민감도 분석 결과 표 및 하단 주의 문구
- **내용**: 계획서는 "실제 GMR이 0.60으로 나타나면 현재 설계(n=20)에서 검정력은 약 0.72로 감소한다"고 명시하고 있다. 그런데 Angiolillo 2011 (PMID 20844485)에서 보고한 GMR 범위는 0.53–0.60으로, 0.60은 문헌에서 충분히 발생 가능한 상한값이다. 검정력 0.72는 일반적으로 수용 가능한 기준(0.80)에 미달한다. 계획서와 statistical_design.md 모두 이 위험을 인지하고 있으나, 이에 대한 **구체적인 대응 방안**(예: 중간 검정력 재추정 후 피험자 수 증가, adaptive design 조항, 또는 수용 불가 시 추가 등록 계획)이 제시되지 않았다.
- **근거**: 규제 기관(FDA, MFDS)은 80% 검정력이 표준이며, 이보다 낮은 검정력으로 설계된 시험은 부정적 결과가 나왔을 때 해석의 불확실성이 증가한다. ICH E8(R1) §3.1은 "연구 목적에 적절한 검정력을 보유해야 한다"고 요구한다.
- **권고**: 
  1. GMR=0.60 시나리오에서의 검정력 감소를 한계로 인정할 경우, 계획서 §B.10.1에 "검정력 0.72는 본 시험에서 수용 가능한 하한으로 사전 합의하며, 이를 §B.2.4 설계 한계에 명시한다"고 사전 합의(pre-specification) 문구를 추가한다.
  2. 또는 n=22 (문헌 상한 GMR=0.60, 검정력 0.80 충족)를 등록 목표로 상향 조정하고, n=20을 최소 평가 가능 대상자 수로 재정의한다.

---

### [Major-2] H4 Cmax를 별도 1차 평가변수로 포함할 때 다중성 보정 미기술

- **심각도**: Major
- **위치**: §B.10.3 판정 기준 — "H4 AUC₀₋₂₄ 및 H4 Cmax 각각 독립 분석"
- **내용**: 계획서 §B.8.1과 §B.10.3 모두 H4 AUC₀₋₂₄와 H4 Cmax를 **1차 평가변수**로 지정하고, 각각에 대해 독립적으로 90% CI를 산출하여 80–125% 경계와 비교하도록 명시하고 있다. 그러나 두 지표에 대해 동시에 귀무가설 기각을 요구하는지(conjunctive criterion), 또는 어느 하나라도 경계를 벗어나면 DDI 결론을 내리는지(disjunctive criterion)에 대한 **판정 로직**이 기술되지 않았다. 또한 두 개의 독립 검정을 수행할 때 전체 유형 I 오류율 제어 방법이 명시되지 않았다. 이 경우 α=0.10 양측 두 검정을 수행하면 family-wise error rate(FWER)가 증가한다.
- **근거**: FDA DDI Guidance(2020) 및 ICH M12(2024)는 GMR과 90% CI를 AUC와 Cmax 각각에 대해 보고하도록 요구하나, 두 지표를 모두 1차 평가변수로 동등하게 취급할 경우 다중 비교 고려를 요구한다. MFDS 의약품상호작용시험 가이드라인(2015)도 복수 평가변수에 대한 분석 계획의 사전 명시를 요구한다.
- **권고**: 
  1. H4 AUC₀₋₂₄를 **주된(co-primary 중 우선순위)** 1차 변수로, Cmax를 **공동 1차(co-primary)** 또는 **2차** 변수로 명확히 위계(hierarchy)를 부여한다.
  2. 판정 로직을 명시한다: "AUC₀₋₂₄와 Cmax 모두 90% CI가 80–125% 범위를 벗어날 경우 DDI 양성으로 판정(conjunctive)"하거나, "AUC₀₋₂₄의 결과를 기준으로 1차 결론을 내리고 Cmax는 지지적 증거로 제시"하는 방식 중 하나를 사전에 지정한다.
  3. Sample size 계산이 AUC₀₋₂₄만을 기반으로 수행되었음을 명시하고, Cmax에 별도 검정력 계산을 추가하거나 2차 변수로 격하한다.

---

### [Major-3] Fixed-sequence ANOVA 모형의 PERIOD 항 처리 방식 불명확

- **심각도**: Major
- **위치**: §B.10.3 통계 모형
- **내용**: 계획서는 "Fixed-sequence ANOVA 등가형: `MODEL ln(AUC) = PERIOD / SOLUTION; RANDOM SUBJECT;`"라고 기술하고 있다. 그러나 SAS PROC MIXED에서 `PERIOD / SOLUTION`은 문법 오류이며, 통상적인 표기는 `MODEL ln_AUC = PERIOD;`이다. 또한 fixed-sequence (one-sequence) 설계에서 sequence 항을 제거한다는 기술이 statistical_design.md에는 있으나 계획서 B.10.3에는 누락되어 있다. 더불어, paired t-test와 ANOVA 중 어느 것이 1차 분석법인지 계획서 내 명확한 위계가 없다. "또는(또는 등가 ANOVA)"이라는 표현은 SAP 작성 시 모호성을 야기한다.
- **근거**: ICH E6(R3) Appendix B.10은 "통계 분석 방법의 명확한 기술"을 요구하며, 불명확한 모형 기술은 사후 분석 방법 변경의 빌미를 제공할 수 있다. SAS PROC MIXED 문법 오류는 실제 분석 코드와의 불일치를 초래할 수 있다.
- **권고**: 
  1. SAS PROC MIXED 코드를 올바른 문법으로 수정한다:
     ```
     PROC MIXED DATA=pkdata;
       CLASS SUBJECT PERIOD;
       MODEL LN_AUC = PERIOD / SOLUTION DDFM=SATTERTHWAITE;
       RANDOM SUBJECT;
       ESTIMATE 'Period 2 vs Period 1' PERIOD -1 1 / CL ALPHA=0.10;
     RUN;
     ```
  2. Paired t-test를 1차 분석법으로 지정하고, ANOVA를 보조 확인 방법으로 위치시킨다. 또는 ANOVA를 1차 분석법으로 채택하되 그 이유를 명시한다.
  3. Fixed-sequence에서 sequence 항 제거 근거(단일 sequence 존재)를 B.10.3에 명시한다.

---

### [Minor-1] 90% CI 보고 방식 — 판정 기준 서술의 비대칭성

- **심각도**: Minor
- **위치**: §B.10.3 판정 및 §B.10.1 통계 프레임워크
- **내용**: 계획서는 "90% CI가 80.00–125.00% 범위를 **벗어나면** DDI 양성"으로 기술하고 있다. 이는 통상적인 DDI 검출 맥락에서 올바르나, CI의 **상한값과 하한값 중 어느 것**이 경계를 벗어나야 하는지 (예: CI 상한 > 125%이거나 CI 하한 < 80%) 또는 CI **전체**가 범위 밖에 있어야 하는지에 대한 서술이 없다. 본 시험에서 H4 노출이 감소하므로 실질적으로는 CI 상한 < 80% 또는 점 추정값 < 80%가 판정 기준이 될 것이나, 이를 명시하지 않으면 결과 해석 시 모호성이 발생할 수 있다.
- **근거**: MFDS 의약품상호작용시험 가이드라인(2015)은 GMR과 그 90% CI를 제시하되 판정 기준을 명확히 기술하도록 요구한다.
- **권고**: "90% CI의 상한이 80.00% 미만인 경우(H4 노출 감소 DDI 확인) 또는 하한이 125.00% 초과인 경우(H4 노출 증가 DDI) DDI 양성으로 판정한다. 본 시험의 목적상 전자만이 임상적으로 유의하다"는 방향성 기술을 추가한다.

---

### [Minor-2] ITT 정의의 DDI 맥락 적합성 검토 필요

- **심각도**: Minor
- **위치**: §B.10.2 분석 집단
- **내용**: ITT를 "최소 1회 이상 시험약을 투여받은 모든 피험자"로 정의하고 있다. Crossover DDI 시험에서 ITT는 일반적으로 두 period 중 적어도 한 period에서 투여를 받은 피험자를 의미한다. Period 1만 투여받고 Period 2를 미이수한 피험자는 paired analysis에서 분석 불가능하므로, 이 피험자들을 ITT에 포함할 경우 실질적으로 분석 가능한 집단은 PP와 동일해지거나 매우 작아질 수 있다. ITT의 sensitivity 분석으로서의 실질적 기여가 불분명하다.
- **근거**: 2-period crossover 시험의 특성상, 두 period 모두 참가하지 않으면 paired comparison 자체가 불가하다. PP와 ITT 결과가 사실상 동일하다면 ITT는 형식적인 항목이 된다.
- **권고**: ITT 집단의 정의를 "두 period 모두 최소 1회 이상 투여받은 피험자 (paired comparison 가능)"로 수정하고, PP와의 차이점을 명확히 한다. 또는 ITT를 "proton pump inhibitor washout 전 모든 등록 피험자"로 재정의하여 선택편향 평가에 활용한다.

---

### [Minor-3] Tmax 분석에 Wilcoxon signed-rank test 적용 — Hodges-Lehmann 추정량 보고 여부 미기술

- **심각도**: Minor
- **위치**: §B.10.4 2차 PK 파라미터
- **내용**: Tmax에 Wilcoxon signed-rank test를 적용하는 것은 적절하나, 검정 결과 외에 **Hodges-Lehmann 추정량(중앙값 차이의 중앙값)**과 그 95% CI(또는 90% CI)를 함께 보고할지 여부가 기술되지 않았다. Wilcoxon 검정의 유의성만 보고하면 효과 크기 추정이 누락된다.
- **근거**: 비모수 검정에서도 효과 크기 추정을 함께 보고하는 것이 규제 기관의 권고이다 (FDA Statistical Review, EMA 가이드라인 일반 원칙).
- **권고**: "Tmax 비교에서 Wilcoxon signed-rank test의 p-value와 함께, Hodges-Lehmann 추정량(median difference) 및 95% CI를 보고한다"는 문구를 추가한다.

---

### [Minor-4] 공변량 ANCOVA의 사전 명세 수준이 계획서와 SAP 간 분담 불명확

- **심각도**: Minor
- **위치**: §B.10.5 탐색적 분석
- **내용**: "공변량 ANCOVA: 체중·연령·BMI·기저 PRU 포함"이라고 간략히 기술되어 있으나, 이 분석이 탐색적 분석의 일환으로 명확히 분류되어 있고, 어떤 outcome에 적용하는지(PK 또는 PD 또는 양쪽), 공변량 선택 기준(단순 포함 vs. 단계적 선택), 결과 해석 방식이 기술되지 않았다. 탐색적 분석이라도 pre-specified 수준이 지나치게 낮으면 사후 검토로 오해받을 수 있다.
- **근거**: ICH E9(R1) §3.6은 탐색적 분석도 사전 명세를 통해 confirmatory 분석과 명확히 구분하도록 권고한다.
- **권고**: ANCOVA가 탐색적 분석임을 명시하고, "SAP에서 적용 outcome, 공변량 목록, 해석 범위를 사전 명세한다"는 문구를 추가하여 계획서 수준의 기술이 SAP에 위임됨을 명확히 한다.

---

### [Minor-5] 이상치(Outlier) 처리 — Grubbs test와 ROUT 중 선택 기준 미명시

- **심각도**: Minor
- **위치**: §B.10.5 탐색적 분석, §B.10.6 결측치 처리
- **내용**: "Grubbs test 또는 ROUT, sensitivity 수행"이라고만 기술되어 있다. Grubbs test는 정규분포 가정 하에 단일 이상치를 검출하는 반면, ROUT(robust outlier test)는 비선형 회귀 기반으로 다중 이상치 검출에 사용된다. PK 데이터는 log-transform 후 비교적 정규 분포를 따르므로 Grubbs test가 통상적으로 적합하다. 두 방법을 OR로 나열하면 사후 선택 가능성이 있다.
- **근거**: FDA 가이드라인은 outlier 처리 기준의 사전 명세를 요구한다.
- **권고**: Grubbs test를 기본 방법으로 지정하고 ROUT는 보조 방법 또는 sensitivity로 명시한다. 또는 SAP에서 구체적 방법과 임계값(예: Grubbs α=0.05)을 사전 명세한다는 문구를 추가한다.

---

## statistical_design.md와 계획서 B.10 정합성 검토

| 항목 | statistical_design.md | 계획서 B.10 | 정합성 |
|------|----------------------|------------|--------|
| 통계 프레임워크 | DDI 검출, α=0.10 양측 | 동일 | 일치 |
| Sample size (평가 가능) | 16명 | 16명 | 일치 |
| Sample size (등록, 탈락 15%) | 19명 → 20명 권장 | 20명 | 일치 |
| 평가 가능 목표 | ≥17명 | ≥17명 | 일치 |
| 탈락률 | 15% | 15% | 일치 |
| CV% | 75% (intra-subject) | 75% (intra-subject) | 일치 |
| 예상 GMR | 0.55 | 0.55 | 일치 |
| 검정력 | 0.80 | 0.80 | 일치 |
| 1차 분석 방법 | Paired t-test (또는 등가 ANOVA) | 동일 | 일치 |
| 90% CI 수식 | exp[mean(d) ± t_{0.05,n-1} × SE] | 동일 | 일치 |
| PP 1차 / ITT sensitivity | 명시 | 명시 | 일치 |
| LOCF 금지 | 명시 | 명시 | 일치 |
| Wilcoxon (Tmax, VerifyNow PRU) | 명시 | 명시 | 일치 |
| McNemar (HPR/LPR 발생률) | 명시 | 명시 | 일치 |
| Sigmoid Emax PK-PD | 탐색적 명시 | 탐색적 명시 | 일치 |
| 중간 분석 없음 | 명시 | 명시 | 일치 |
| 무작위화 없음 (fixed-sequence) | 명시 | **계획서 B.10에 무작위화 항목 별도 부재** | 불완전 — 하단 참조 |
| GMR=0.60 시나리오 검정력 0.72 | 명시 (주의 항목으로) | 명시 (주의 항목으로) | 일치하나 대응 계획 부재 (Major-1) |
| H4 AUC vs Cmax 판정 로직 | 독립 분석 명시, 위계 미지정 | 동일 | 양 문서 모두 미비 (Major-2) |

**무작위화 항목**: statistical_design.md §4에는 "Fixed-sequence에서 무작위화 불시행, 피험자 ID 연속 부여" 등이 상세히 기술되어 있으나, 계획서 B.10에는 이에 대한 명시적 언급이 없다. B.4에서 다루어졌을 수 있으나, ICH E6(R3) B.10은 분석 집단 정의와 더불어 배정 방법 요약도 포함하도록 권고한다. B.10에 "본 시험은 Fixed-sequence 설계로 무작위 배정을 수행하지 않으며, 모든 피험자는 동일한 투여 순서(Period 1: Clopidogrel 단독 → Period 2: Clopidogrel + Omeprazole)를 따른다"는 한 줄 요약을 추가하는 것이 바람직하다.

---

## 종합 의견

계획서 §B.10은 전반적으로 statistical_design.md를 충실히 반영하고 있으며, DDI 검출 프레임워크 선택의 수학적 근거(TOST 적용 불가 이유), sample size 계산 공식과 민감도 분석, LOCF 금지 원칙, 결측치 처리 기준이 명확하게 기술되어 있다. Sigmoid Emax PK-PD 탐색 분석과 McNemar test를 통한 HPR/LPR 이분형 PD 평가의 포함은 적절하다.

주요 보완 사항은 두 가지다.

첫째, GMR=0.60 시나리오에서 검정력이 0.72로 감소한다는 사실을 인지하면서도 구체적인 대응 계획을 제시하지 않았다 (Major-1). Angiolillo 2011의 GMR 상한값인 0.60은 현실적인 시나리오이므로, 이 경우에 대한 사전 합의 또는 n 상향 조정이 필요하다.

둘째, H4 AUC₀₋₂₄와 Cmax를 동등한 1차 평가변수로 취급하면서 판정 로직(conjunctive vs. disjunctive)과 다중성 처리 방안이 제시되지 않았다 (Major-2). 이는 분석 계획의 핵심 항목으로, SAP 이전에 계획서 수준에서 위계를 부여해야 한다.

Minor 사항들은 SAP 작성 시 보완 가능한 수준이며, Critical에 해당하는 규제 불합격 또는 대상자 안전 위험 요인은 발견되지 않았다.

**발견 사항 요약**: Critical 0건 | Major 3건 | Minor 5건

---

*작성: biostatistician | 2026-04-14*
*검토 대상: CLO-OME-DDI-001 v1.0 §B.10 Statistical Considerations*
