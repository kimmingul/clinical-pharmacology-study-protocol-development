# Trial Info — 입력 템플릿

본 템플릿을 프로젝트 루트에 복사한 후 (`TRIAL_INFO.md`) 항목을 채워 LLM에 전달하세요.

---

## 기본 정보 (모든 시험 공통)

- **약물명** (generic name): 
- **시험 유형** [FIH | SAD | MAD | DDI | BE | FE | QTc | ADME | PK Special Pop]: 
- **시험 단계**: Phase 1
- **대상자 집단**: 건강한 성인 남성 / 환자 / 특수 집단(고령/소아/신장애/간장애)
- **목표 등록 인원** (있을 시): 
- **임상시험 실시기관**: 

## 약물 특성 (허가 약물인 경우)

- **MFDS 품목허가번호**: 
- **FDA NDA / EMA EMEA 번호**: 
- **약효군** (예: 항혈전제, PPI): 
- **주요 대사 효소** (이미 알려진 경우): 
- **CYP 기질/저해/유도 역할**: 
- **BCS Class** (BE의 경우):
- **NTI 약물 여부** (warfarin, tacrolimus 등): 

## FIH 시험 추가 입력

- **IB 첨부 경로**: ./IB/investigator_brochure.pdf
- **NOAEL** (mg/kg/day): 
- **종(가장 민감한 종)**: 
- **HED 환산 인자**: 
- **목표 PD 효과 시점 EC50 추정** (있을 시):

## DDI 시험 추가 입력

- **Object drug**: 
- **Precipitant drug**: 
- **양방향 평가 여부**: [Yes | No — 한 방향만]
- **예상 GMR 범위**: 
- **임상적으로 의미 있는 변화 기준**: AUC ±25% / Cmax ±20%

## BE 시험 추가 입력

- **시험약(T) / 대조약(R)**: 
- **제형**: 
- **예상 intra-subject CV**: 
- **사전 BE 결과 (있을 시)**:

## FE 시험 추가 입력

- **공복 / 식후 비교 유형**: high-fat / low-fat / 일반식
- **식이 조성** (FDA / EMA / MFDS 기준):

## 안전성 사전 정보

- **알려진 SAE / 주요 AE**: 
- **약물 상호작용 주의 약물**: 
- **임상시험 중 금기 약물·식품**: 

## 규제 / 인허가 정보

- **승인기관(목표)**: MFDS / FDA / EMA / 기타
- **IND 번호** (있을 시): 
- **IRB 심의 일정** (있을 시):
- **이전 동일 약물 임상시험 NCT ID**:

## 사용자 선호 (선택)

- **선호 연구설계**: parallel / 2×2 crossover / Williams 4×4 / Williams 6×3 / one sequence
- **선호 sample size 정책**: ICH 기본 (90% CI 80-125%) / 사용자 정의
- **유전체 분석 포함 여부**: Yes (별도 동의 ICF Part 4) / No
- **대사체 분석 포함 여부**: Yes / No

---

> **주의**: 본 정보는 LLM이 background research, synopsis, protocol 작성 시 활용합니다. 부정확한 입력은 부정확한 산출로 직결됩니다. 가능하면 출처(PMID, NCT, 라벨 URL)도 함께 명시하세요.
