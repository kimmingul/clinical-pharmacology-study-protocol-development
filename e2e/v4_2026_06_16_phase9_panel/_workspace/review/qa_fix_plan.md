# QA 수정 계획 (자동 생성 — review_synthesis.json 기반)

## Critical (5)
1. [google:regulatory_cross_check] §B.7 Treatment and Interventions: Omeprazole 투여 요법(투여 기간 및 빈도) 명시 누락 → 권고: Omeprazole의 구체적인 투여 스케줄(예: Day 1-5, 80mg QD)과 Clopidogrel 투여와의 시간 간격을 명확히 기술할 것.
2. [xai:biostat_adversarial] §B.10: 표본수 산출이 완전 공백이다. n, 개체내 CV%, 기대 GMR, 목표 검정력, α, 탈락률, 스크리닝 실패율, 계산 코드·근거 문헌이 전무하다. → 권고: crossover_2x2_ddi.py 등 검증 코드로 CV·GMR·power를 문헌(PMID 19915222, NCT00352877) 기반 산출하고, 스크리닝·탈락을 반영한 최종 n·sequence별 인원·계산 코드 전문을 B.10에 포함하라.
3. [xai:biostat_adversarial] §B.3/B.10: 1차 목적('상호작용 변화 평가')과 통계 성공 기준('no-effect 동등성')이 모순된다. 배경은 병용 시 활성대사체 노출 감소를 전제하는데, 성공은 GMR 90% CI가 80–125%에 완전 포함일 때로 정의된다. → 권고: 목적을 (a) 상호작용 크기 추정+CI 보고 또는 (b) no-effect 입증 중 하나로 명확히 하라. (b)라면 문헌 기대 GMR로 TOST 검정력을 재산출하고, (a)라면 성공 기준을 'CI가 경계 내'가 아닌 'GMR·CI 정밀 추정'으로 바꾸고 필요 n을 정밀도 기반으로 산출하라.
4. [xai:biostat_adversarial] §B.10: 기대 GMR=1.0 또는 no-effect 가정으로 표본수를 잡으면, 실제 효과가 문헌 수준(예: GMR≈0.55)일 때 동등성 입증 검정력은 사실상 0에 가깝다. → 권고: 기대 GMR을 문헌 point estimate(및 보수적 worst-case)로 명시하고, noncentral-t/시뮬레이션 기반 검정력 곡선을 제시하라. no-effect 입증이 목표가 아니면 equivalence power 대신 CI 폭·탐지 가능한 최소 GMR 차이를 기준으로 n을 정하라.
5. [xai:biostat_adversarial] §B.10: 결측치·탈락·intercurrent event 처리가 전혀 없다. Estimand(B.3)와 통계분석이 연결되지 않는다. → 권고: PK evaluable set 정의, period/subject exclusion 규칙, primary=PP 또는 hybrid estimand, dropout imputation(없음/complete-case), tipping-point·worst-case sensitivity를 B.10에 추가하고 표본수에 dropout inflation(통상 10–20%)을 반영하라.

## Major (14)
1. [google:citation_integrity] §B.7 (Treatment and Interventions): 용량 설정 근거와 실제 기술된 용량 간의 불일치 → 권고: B.2의 용량 근거를 'DDI 평가를 위한 최대 저해 효과 유도' 등의 과학적 근거로 수정하거나, 용량을 허가 범위 내로 조정하십시오.
2. [google:citation_integrity] §B.14 (Data Handling and Record Keeping): 법적 문서 보존 기간에 대한 잘못된 인용 및 단정 → 권고: KGCP 규정에 따른 실제 법적 보존 기간(품목허가일로부터 3년 등)으로 수정하거나, 15년이 의뢰자 내부 정책(SOP)임을 명시하십시오.
3. [google:regulatory_cross_check] §B.1 General Information: 시험책임자, 공동연구자 및 임상시험 실시기관 정보 완전 누락 → 권고: 실시기관 정보와 의학적 자문을 제공할 전문의(Medical Monitor) 정보를 추가할 것.
4. [google:regulatory_cross_check] §B.9 Assessment of Safety: 중대한 이상반응(SAE) 즉시 보고 절차 및 타임라인 부재 → 권고: SAE 발생 시 24시간 이내 의뢰자 및 IRB 보고 절차와 보고 양식을 구체화하여 명시할 것.
5. [google:regulatory_cross_check] §B.5 Selection of Participants: 시험대상자 선정/제외 기준의 구체성 결여 (BMI, 피임, 병용약물) → 권고: BMI, 피임법(이중차단), 시험 참여 전 일정 기간 내 약물 복용 금지 등 제외 기준을 정밀화할 것.
6. [google:regulatory_cross_check] §B.10 Statistical Considerations: 구체적인 표본수 산출 근거 및 N수 미제시 → 권고: Clopidogrel 활성대사체의 개체내 변동성(CV) 문헌치를 인용하여 산출된 구체적인 대상자 수(예: N=24)와 탈락률을 제시할 것.
7. [xai:biostat_adversarial] §B.10: AUC·Cmax co-primary에 대한 IUT(교집합-합집합) 판정 논리가 누락되었다. → 권고: 'AUC와 Cmax 각각 90% CI가 80.00–125.00%에 완전 포함되어야 no-effect 성립(IUT, family-wise α=0.05 유지)'을 명시하고, sample size 기준 변수(AUC vs Cmax 중 보수적 CV)를 지정하라.
8. [xai:biostat_adversarial] §B.10: 1차 분석 혼합모형이 'log-변환 혼합효과' 한 줄로만 기술되어 재현 불가능하다. → 권고: SAS PROC MIXED 전체 문법(CLASS/MODEL/RANDOM/LSMEANS/ESTIMATE), GMR=exp(LSM difference), 90% CI 산출, Kenward-Roger, subject(sequence) random effect를 SAP 수준으로 기재하라. 필요 시 period×treatment carry-over 사전검정·민감도 분석을 추가하라.
9. [xai:biostat_adversarial] §B.4: 무작위화 설계가 '순서 효과 균형화' 수준으로만 기술되어 통계적 타당성을 검증할 수 없다. → 권고: computer-generated randomization, fixed block size(예: 4), 1:1 AB/BA, (선택) CYP2C19 metabolizer status 층화, sequence별 evaluable n 균형 모니터링 계획을 B.4/B.10에 명시하라.
10. [xai:biostat_adversarial] §B.4/B.10: 14일 washout이 omeprazole 80 mg의 CYP2C19 저해 잔류 및 clopidogrel 비가역적 PD carry-over를 충분히 제거한다는 근거가 없다. → 권고: 문헌/PK-PD 기반 washout justification(≥14일 근거 수치), 선행 period baseline PK·PD(혈소판 기능), period×treatment interaction 검정, 실패 시 해당 period/subject exclusion 규칙을 추가하거나 one-sequence/parallel 대안을 검토하라.
11. [xai:biostat_adversarial] §B.7/B.4: Clopidogrel 300 mg 부하 후 75 mg regimen이 각 period에 어떻게 적용되는지 불명확해 GMR 해석이 불안정하다. → 권고: 각 period의 정확한 dosing calendar(clopidogrel 부하/유지, omeprazole 80 mg 선행 일수, PK sampling window)를 표로 고정하고, 분석 모형이 steady-state vs single-dose estimand와 일치하는지 확인하라.
12. [xai:biostat_adversarial] §B.4: 1차 변수 AUC0-last 선택이 부적절할 수 있으나 extrapolation·<20% 규칙이 없다. → 권고: 채혈 스케줄(최소 8–12 points, terminal phase), AUC0-inf 계산·%extrapolation 기준, AUC0-last 사용 시 정당화를 B.8/B.10에 추가하라.
13. [xai:biostat_adversarial] §B.5/B.10: CYP2C19 PM 제외만으로 genotype-driven PK 변동을 통제한다고 가정하는 것은 낙관적이다. → 권고: CYP2C19 genotype 사전 확정·EM-only enrollment 또는 genotype 층화 randomization, genotype별 exploratory/subgroup 분석, 보수적 CV%(문헌 상위 quartile)로 n을 재산출하라.
14. [xai:biostat_adversarial] §B.10: α 수준·검정력·탈락 반영이 명시되지 않아 '90% CI'만으로는 TOST 가정이 불완전하다. → 권고: 'two one-sided tests at α=0.05 each (overall 90% CI)', target power≥80%(또는 90%), anticipated dropout 10–15%를 명시하고 adjusted n을 보고하라.

> protocol-writer는 위 Critical→Major 순으로 본문을 수정한다. synopsis·design_decisions의 설계 결정은 불변. 결정적 도구(doc_lint/citation_verify/dose_safety) 항목이 최우선.
