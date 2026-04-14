# 시험 정보

## 기본 정보
- **시험약 (Victim/Probe)**: Clopidogrel bisulfate 75 mg 정제
- **병용약 (Perpetrator/Inhibitor)**: Omeprazole 80 mg 캡슐
- **시험 유형**: DDI (Drug-Drug Interaction)
- **적응증 (Clopidogrel)**: 급성관상동맥증후군(acute coronary syndrome), 관상동맥질환에서의 죽상경화성 사건 예방
- **ICD-10**: I25.10 (만성 허혈성 심장질환), I20.0 (불안정 협심증)
- **시험 단계**: Phase 1
- **대상 집단**: 건강한 성인 남성 지원자 (만 19-45세)
- **의뢰자명**: [E2E 테스트용 — 실제 의뢰자 아님]
- **투여 경로/제형**: 경구(oral) / 정제·캡슐

## 시험 목적
Clopidogrel의 활성 대사체 형성이 CYP2C19 의존적이며, Omeprazole(CYP2C19 억제제)와의 병용이 활성 대사체 노출과 항혈소판 효과에 미치는 영향을 정량적으로 평가한다.

### 1차 목적
Omeprazole 병용 시 vs 단독 투여 시 Clopidogrel **활성 대사체(H4)의 AUC₀₋ₜ, Cmax 기하평균비(GMR)** 평가. GMR 90% CI가 80–125% 범위를 벗어나는지 확인.

### 2차 목적
- 약력학(PD) 평가: VerifyNow P2Y12 활성 검사(PRU), LTA 혈소판 응집 억제율
- Clopidogrel parent drug 및 주요 대사체 PK
- Omeprazole의 PK 영향 (간접)
- 안전성 및 내약성

## 추가 정보
- **IB 제공 여부**: 불필요 (두 약물 모두 오랜 허가 약물)

## 약물 정보

### Clopidogrel (시험약 / Probe)
- **계열**: Thienopyridine P2Y12 수용체 억제제 (항혈소판제)
- **작용 기전**: **CYP2C19를 통해 활성 대사체(H4)로 전환** → P2Y12 수용체 비가역적 차단 → ADP 유도 혈소판 응집 억제
- **핵심 PK**:
  - Prodrug → 활성 대사체 형성률 ~15% (나머지는 불활성 카르복실산 대사체)
  - CYP2C19가 활성 대사체 형성의 주 경로 (CYP2C19 PM에서 항혈소판 효과 크게 감소)
  - t½ (활성 대사체) ≈ 0.5–1 hr, Tmax ≈ 0.5–2 hr
- **FDA 블랙박스 경고**: CYP2C19 PM에서 효과 감소 — 유전형 검사 권고
- **CPIC Level A**: CYP2C19–Clopidogrel
- **NDA**: 020839 (Plavix)

### Omeprazole (병용약 / Inhibitor)
- **계열**: Proton Pump Inhibitor (PPI)
- **작용 기전**: 위벽세포 H+/K+ ATPase 비가역적 억제
- **DDI 기전**: **CYP2C19 저해제** (+ CYP3A4 약한 저해)
- **핵심 PK**: t½ ≈ 0.5–1 hr, CYP2C19·CYP3A4 경유 대사
- **라벨 경고**: Clopidogrel과의 병용 회피 권장 (FDA 라벨)

## 설계 제안 (Phase 4에서 협의 확정)
- **설계 유형 (초안)**: Two-period, fixed-sequence, open-label, single-center crossover
- **Sample size 초안**: CYP2C19 EM 대상자 중심, 탈락률 고려 ~24명
- **Washout 초안**: ≥14일 (혈소판 수명 고려)

## 규제 고려사항
- **FDA**: Clinical Drug Interaction Studies Guidance (2020)
- **EMA**: Guideline on the Investigation of Drug Interactions (2012)
- **ICH M12**: Drug Interaction Studies (2024, Step 4)
- **MFDS**: 약물상호작용 평가 가이드라인 (2015)

## 배경 요약
Clopidogrel의 항혈소판 효과는 CYP2C19 의존적 활성 대사체에 의한다. Omeprazole은 CYP2C19 저해제로서 활성 대사체 형성을 감소시킬 수 있다. 이 상호작용은 FDA·EMA·MFDS 라벨에 경고되어 있으며, 한국인 CYP2C19 PM 비율이 서양인보다 높아 (~15% vs 2–3%) 국내 임상적 의미가 크다.

---

**입력 참조**: `e2e/v2_2026_04_14_DDI/TRIAL_INFO_INPUT.md`
