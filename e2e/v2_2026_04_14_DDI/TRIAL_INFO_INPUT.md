# 시험 정보 — Clopidogrel + Omeprazole DDI (E2E v2)

> 본 문서의 내용을 새 세션에서 `_workspace/00_input/trial_info.md`로 복사하거나, Claude에게 "이 파일을 참조해서 시험 정보를 입력해줘"라고 지시.

---

## 기본 정보

- **시험약(Victim/Probe)**: Clopidogrel bisulfate 75 mg 정제
- **병용약(Perpetrator/Inhibitor)**: Omeprazole 80 mg 캡슐
- **시험 유형**: DDI (Drug-Drug Interaction)
- **적응증 (Clopidogrel)**: 급성관상동맥증후군, 관상동맥질환에서의 죽상경화증 사건 예방
- **ICD-10**: I25.10 (만성 허혈성 심장질환), I20.0 (불안정 협심증)
- **시험 단계**: Phase 1
- **대상 집단**: 건강한 성인 남성 지원자 (만 19-45세)
- **의뢰자명**: [E2E 테스트용 — 실제 의뢰자 아님]
- **투여 경로/제형**: 경구 / 정제·캡슐

## 시험 목적

Clopidogrel의 활성 대사체 형성이 CYP2C19 의존적이며, Omeprazole(CYP2C19 억제제)와의 병용이 활성 대사체 노출과 항혈소판 효과에 미치는 영향을 정량적으로 평가한다.

### 1차 목적
- Omeprazole 병용 시 vs 단독 투여 시 Clopidogrel **활성 대사체(H4)의 AUC₀₋ₜ, Cmax 기하평균비(GMR)** 평가
- GMR 90% CI가 80-125% 범위를 벗어나는지 확인

### 2차 목적
- **약력학(PD) 평가**: VerifyNow P2Y12 활성 검사(PRU), LTA(Light Transmittance Aggregometry) 혈소판 응집 억제율
- **약물유전체(PG) 평가**: CYP2C19 표현형(*1/*1, *1/*2 등) 별 DDI 영향 정도
- Clopidogrel parent drug 및 주요 대사체 PK
- Omeprazole의 PK 영향 (간접)
- 안전성·내약성

## 약물 정보

### Clopidogrel (시험약 / Probe)
- **계열**: Thienopyridine P2Y12 수용체 억제제 (항혈소판제)
- **작용 기전**: CYP2C19를 거쳐 활성 대사체(R-130964 / H4)로 전환 → P2Y12 수용체 비가역적 차단 → ADP 유도 혈소판 응집 억제
- **핵심 PK 특성**:
  - Prodrug → 활성 대사체 형성률 ~15% (나머지는 불활성 카르복실산 대사체)
  - **CYP2C19가 활성 대사체 형성의 주 경로** (CYP2C19 PM에서 항혈소판 효과 크게 감소)
  - t½ (활성 대사체) ≈ 0.5-1 hr
  - Tmax (활성 대사체) ≈ 0.5-2 hr
- **FDA 블랙박스 경고**: CYP2C19 PM에서 효과 감소 — 유전형 검사 권고
- **CPIC Level A**: CYP2C19-Clopidogrel (대체 항혈소판제 권고: Prasugrel, Ticagrelor)
- **NDA**: 020839 (Plavix, Bristol-Myers Squibb/Sanofi)

### Omeprazole (병용약 / Inhibitor)
- **계열**: Proton Pump Inhibitor (PPI)
- **작용 기전**: 위벽세포 H+/K+ ATPase 비가역적 억제
- **DDI 기전**: **CYP2C19 저해제** (또한 CYP3A4 약한 저해)
- **핵심 PK**:
  - t½ ≈ 0.5-1 hr
  - CYP2C19·CYP3A4 경유 대사
- **라벨 경고**: Clopidogrel과의 병용 **회피 권장** (FDA 라벨)

### 왜 이 조합이 DDI 시험 E2E에 이상적인가
1. **CYP2C19 중심 DDI**로 PharmGKB/CPIC 활용 필수
2. **활성 대사체 측정**이 1차 평가변수 → translational-scientist의 대사체 분석 설계 검증
3. **PD 평가(P2Y12, LTA)** 포함 → "유효성 평가(Assessment of Efficacy)" 공식 용어 적용 검증
4. **PG 분석(CYP2C19 표현형)** 필수 → ICF Part 4 자동 포함 검증
5. **한국인 CYP2C19 PM ~15%** → 선정/제외 기준 협의에 실제 임상 이슈 반영

## 설계 제안 (Phase 4에서 협의 확정)

- **설계 유형**: Two-period, **fixed-sequence**, open-label, single-center
  - Period 1: Clopidogrel 300 mg 로딩 → 75 mg QD × 7일 (단독)
  - Washout: ≥14일 (혈소판 수명 고려)
  - Period 2: Omeprazole 80 mg QD × 5일 (pre-treatment) → Omeprazole + Clopidogrel 75 mg QD × 7일
- **Sample size**: CYP2C19 EM 대상자 중심, 탈락률 고려 ~24명
- **채혈 시점**: Day 7 (steady state) 기준 0, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12, 24 hr
- **PD 평가**: VerifyNow (PRU) 및 LTA — 각 Period의 Day 7 0h, 4h, 24h
- **PG 분석**: 스크리닝 시 CYP2C19 유전형 검사 (*1, *2, *3, *17) — **별도 동의**

## 추가 정보

- **IB 제공**: 불필요 (두 약물 모두 오랜 허가 약물)
- **약물유전체 시험 여부**: **포함** (CYP2C19 필수 + 별도 동의) → ICF Part 4 자동 추가 대상
- **대사체 분석 여부**: **포함** (Clopidogrel 활성 대사체 측정) → ICF Part 4 자동 추가 대상
- **잔여 검체 보관**: 협의 결정 (default: 5년 보관 동의 옵션 제공)
- **작용 기전 요약 (Background)**: Clopidogrel의 항혈소판 효과는 CYP2C19 의존적 활성 대사체에 의한다. Omeprazole은 CYP2C19 저해제로 활성 대사체 형성을 감소시킬 수 있다. 이 상호작용은 FDA·EMA·MFDS 라벨에 경고되어 있으며, 한국인 CYP2C19 PM 비율이 서양인보다 높아 (~15% vs 2-3%) 국내 임상적 의미가 크다.

## 참고 문헌 (배경 자료용, Phase 2 조사에서 검증)

- Gurbel PA et al. "Clopidogrel with or without omeprazole in coronary artery disease." NEJM. 2010
- FDA Drug Safety Communication on clopidogrel-omeprazole interaction (2009, 2010)
- CPIC Guideline for CYP2C19 and Clopidogrel Therapy (Scott SA et al., 2013; 2023 update)
- FDA Plavix Label (NDA 020839) — 블랙박스 경고

## 규제 고려사항

- **FDA**: DDI 시험 — FDA Clinical Drug Interaction Studies Guidance (2020)
- **EMA**: Guideline on the Investigation of Drug Interactions (2012)
- **ICH M12**: Drug Interaction Studies (2024, Step 4)
- **MFDS**: 약물상호작용 평가 가이드라인 (2015)

## Phase 4 협의 시 중점 사항 (체크리스트)

Design 단계에서 다음 질문에 대한 사용자 결정이 필요:

1. **대상자 CYP2C19 표현형 포함 범위**:
   - 옵션 A: NM/IM만 (PM·UM 제외) — 대사 변동성 최소화
   - 옵션 B: NM/IM/EM 모두 포함, PM·UM 제외 — 실무적 균형
   - 옵션 C: 모든 표현형 층화(stratification) — 이상적이나 sample size 증가
2. **PD 평가 도구**: VerifyNow 단독 / LTA 단독 / 둘 다
3. **Washout 기간**: 14일 / 21일 / 표준 5×t½ 기반
4. **잔여 검체 보관 기간**: 5년 / 10년 / 영구
5. **CPIC 권고 적용 여부**: 결과 해석에 CPIC 가이드라인 인용할 것인지
