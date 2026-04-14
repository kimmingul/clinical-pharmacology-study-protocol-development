# E2E 실행 가이드 — Clopidogrel + Omeprazole DDI (v2, 2026-04-14)

> **목적**: 2026-04-14 대규모 재구성 후의 하네스가 실제로 작동하는지 전체 파이프라인으로 검증.
>
> **비교 대상 (v1)**: `e2e/v1_2026_04_06_BE/` (Amlodipine BE, 구 4-에이전트 구조)
>
> **실행 방식**: Phased E2E (Phase 3/7/9 Gate에서 품질 확인)
>
> **예상 소요 시간**: 1.5-2시간

---

## 1. 시험 선정 배경

### 왜 Clopidogrel + Omeprazole DDI인가?

| 기준 | 설명 |
|------|------|
| **TS 필수 참여** | CYP2C19 기질(Clopidogrel)–저해제(Omeprazole) 시험 → translational-scientist의 조건부 참여 로직 검증에 이상적 |
| **Web API 5종 활용** | DailyMed(두 약물 라벨), openFDA(FAERS, NDA), MFDS(국내 유사 시험), PharmGKB(Clopidogrel-CYP2C19 clinical annotation), CPIC(Level A dosing guideline) |
| **실무 가치** | 한국인 CYP2C19 PM 비율 ~15% → PG 분석이 실제 규제·임상적으로 의미 있음 |
| **CPIC Level A** | Clopidogrel-CYP2C19는 CPIC 권고 최고 등급 → CPIC API 검증에 최적 |
| **FDA 블랙박스 경고** | Clopidogrel 라벨에 PG 경고 존재 → DailyMed PG 섹션 추출 검증 |
| **실제 임상 이슈** | PPI 병용 환자에서 clopidogrel 효과 감소가 문헌·라벨에서 반복 논의 |

### 검증 대상 기능 (2026-04-14 변경분)

- ✅ translational-scientist 에이전트 (신설, DDI에서 필수 참여)
- ✅ Phase 4 협의 재구성 (선정/제외 → 유효성/PD → 유전체/대사체)
- ✅ 5명 리뷰 (TS 포함, Phase 9)
- ✅ ICF Part 4 PG 동의 자동 추가
- ✅ Web API 5종 (DailyMed, openFDA, MFDS searchClinic, PharmGKB, CPIC)
- ✅ ICH E6(R3) Appendix B 16개 섹션 체크리스트
- ✅ Phase 1 용어 정책 완화 (DDI → "유효성 평가" 공식 사용)
- ✅ 선정/제외기준 표준 템플릿 활용

---

## 2. 시험 정보 (Trial Info)

새 세션에서 `_workspace/00_input/trial_info.md`로 저장할 내용. 상세는 `TRIAL_INFO_INPUT.md` 참조.

| 항목 | 값 |
|------|---|
| 시험약 | Clopidogrel bisulfate 75 mg 정제 (Plavix 등) |
| 병용약 | Omeprazole 80 mg 캡슐 (CYP2C19 저해제) |
| 시험 유형 | DDI (Drug-Drug Interaction) |
| 적응증 | 급성관상동맥증후군·관상동맥질환(Clopidogrel 적응증) |
| 시험 단계 | Phase 1 |
| 대상 집단 | 건강한 성인 남성 (만 19-45세, CYP2C19 NM/IM/EM; PM 제외) |
| 설계 (제안) | Two-period, fixed-sequence, open-label crossover |
| 의뢰자 | [E2E 테스트용] |

---

## 3. 사전 준비

### 3-1. Web API 작동 확인 (선택)

새 세션 시작 전 Web API가 접근 가능한지 빠르게 확인:

```
WebFetch(url="https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=clopidogrel&pagesize=3", prompt="setid 3개 추출")
WebFetch(url="https://api.pharmgkb.org/v1/data/clinicalAnnotation?view=mostRecent&chemical.name=clopidogrel&gene.symbol=CYP2C19", prompt="level 추출")
WebFetch(url="https://api.cpicpgx.org/v1/pair_view?drugname=eq.clopidogrel&genesymbol=eq.CYP2C19", prompt="cpiclevel 추출")
WebFetch(url="https://nedrug.mfds.go.kr/searchClinic?searchYn=true&page=1&searchType=ST1&searchKeyword=clopidogrel&approvalDtStart=2020-01-01&approvalDtEnd=2024-12-31", prompt="총 건수 추출")
WebFetch(url="https://api.fda.gov/drug/label.json?search=openfda.generic_name:clopidogrel&limit=1", prompt="pharmacogenomics 필드 유무")
```

5개 모두 응답하면 준비 완료. 실패하면 해당 소스 장애 → 대체 방안 (WebSearch 폴백)

### 3-2. 세션 환경
- Claude Code 세션 시작
- 작업 디렉토리 확인: `cd /Users/min/Projects/clinical-trial-protocol_2`
- trial-doc-orchestrator 스킬이 로드되는지 확인

---

## 4. 실행 순서 (Phased)

### Phase 1: 입력
```
사용자 → Claude에게 요청:
"Clopidogrel + Omeprazole DDI 임상시험 문서를 작성해줘. 자세한 시험 정보는
e2e/v2_2026_04_14_DDI/TRIAL_INFO_INPUT.md를 참조해."
```

Claude가 `_workspace/00_input/trial_info.md`를 생성해야 함.

**검증 Checkpoint 1:**
- [ ] `_workspace/00_input/trial_info.md` 생성됨
- [ ] 시험 유형 "DDI" 명시
- [ ] 약물 계열/MOA/CYP 대사 정보 포함
- [ ] **"유전체/인체유래물 포함 여부" 항목이 없음** (Phase 1 입력에서 제거된 정책 반영 확인)

---

### Phase 2-3: `/research`
```
/research
```

**예상 행동**: 4개 에이전트 병렬 호출 (CP + REG + CLIN + **TS**)

**검증 Checkpoint 2 (Phase 3 Gate):**
- [ ] **5개 에이전트 중 TS가 호출됨** (BE/FE가 아닌 DDI이므로)
- [ ] `_workspace/01_research_ts.md` 생성됨
- [ ] `_workspace/01_references/pharmacogenomics/CYP2C19.md` 생성됨
- [ ] `_workspace/01_references/labels/clopidogrel_DailyMed.md` 생성됨
- [ ] `_workspace/01_references/labels/clopidogrel_openFDA.md` 생성됨
- [ ] `_workspace/01_references/mfds_clinical_trials/` 하위에 국내 시험 목록
- [ ] `_workspace/01_references/pd_biomarkers/` 디렉토리 존재
- [ ] **Reference 날조 없음**: PMID/NCT/setid 가 실제 존재하는지 스팟 체크 (3-5개)
- [ ] 통합 보고서(`01_research_report.md`)에 4대 섹션: PK, **PD/약력학**, 규제, **PG**, 안전성

**사용자 승인 게이트**: "자료 조사 승인" 응답 후 Phase 4로

---

### Phase 4-5: `/design`

**예상 행동**: 메인 에이전트가 사용자와 대화로 설계 확정

**검증 Checkpoint 3:**
- [ ] **Step 1 선정/제외기준 협의**: `.claude/references/templates/inclusion_exclusion_criteria.md` 기반 항목별 협의
  - 특히 "CYP2C19 PM 제외" 또는 "표현형별 stratification" 논의 유도
- [ ] **Step 2 연구설계**: fixed-sequence crossover 선택 (DDI 전형)
- [ ] **Step 3 세부 요소**:
  - [ ] PK 채혈 시점 (Clopidogrel 활성 대사체 + parent 모두 측정)
  - [ ] 1차 평가변수: Clopidogrel 활성 대사체의 **AUC/Cmax GMR** (Omeprazole 병용 vs 단독)
  - [ ] **유효성/약력학(PD) 평가 항목**: VerifyNow (P2Y12 활성), 혈소판 응집 억제율
  - [ ] 안전성 평가
  - [ ] **유전체/대사체 분석 계획**:
    - PG: CYP2C19 *2, *3, *17 (분석 필수, 별도 동의)
    - 대사체: Clopidogrel 활성 대사체 (H4)
    - 잔여 검체 보관 여부
  - [ ] Washout (예상 ≥7일)
  - [ ] 투여 조건 (공복)
- [ ] `_workspace/00_input/design_decisions.md`에 모든 결정 기록
- [ ] Sample size 계산 (biostatistician) — DDI GMR 기준, `crossover_2x2_ddi.py`

---

### Phase 6-7: `/synopsis` + 승인
```
/synopsis
```

**검증 Checkpoint 4 (Phase 7 Gate — Hard):**
- [ ] Synopsis 13개 섹션 모두 존재:
  - 1.시험 제목 / 2.목적 / 3.설계 / 4.대상자 (선정·제외 full list)
  - 5.시험약 / 6.평가변수 (6.3 **PD 평가**, 6.4 절단 AUC 해당 안 됨)
  - 7.PK 채혈 / 8.Washout / 9.안전성
  - **10.유전체/대사체 분석 계획** ★
  - 11.통계 / 12.방문 / 13.시험 기간
- [ ] 10.1 PG 분석: CYP2C19 대상 유전자 명시
- [ ] 6.1에 "유효성 평가" 용어 사용 (Phase 1 용어 가이드 반영)

**사용자 승인 게이트**: "Synopsis 승인" 명시 응답

---

### Phase 8: `/protocol`
```
/protocol
```

**검증 Checkpoint 5:**
- [ ] **ICH E6(R3) Appendix B 16개 섹션 모두 존재**:
  - B.1 General Information, B.2 Background, B.3 Objectives, B.4 Design
  - B.5 Selection, B.6 **Discontinuation** ★(기존 누락이었던 항목)
  - B.7 Treatment, **B.8 Assessment of Efficacy** ★(공식 섹션명)
  - B.9 Safety, B.10 Statistics
  - B.11 **Direct Access** ★, B.12 QC/QA, B.13 Ethics, B.14 Data Handling
  - B.15 **Financing/Insurance** ★, B.16 **Publication Policy** ★
- [ ] B.8에 Clopidogrel 활성 대사체 AUC/Cmax GMR를 "유효성 평가변수"로 기술
- [ ] PG/오믹스 분석 계획 포함 (Synopsis 10.1~10.3과 일관)
- [ ] 선정/제외 기준이 Synopsis 4.2~4.3과 완전 일치

---

### Phase 9: `/review`
```
/review
```

**예상 행동**: 5명 병렬 리뷰 (DDI → TS 포함)

**검증 Checkpoint 6:**
- [ ] 리뷰 파일 **5개** 생성: CP, TS, CLIN, REG, BIOSTAT
- [ ] `review_translational_scientist.md` 내용: PD 평가·PG 분석·ICF 정합성 검토
- [ ] `qa_review_report.md`에 5명 취합 명시
- [ ] Phase 1 용어 정책 반영 (B.8 "Assessment of Efficacy" 사용을 Critical로 지적하지 않음)
- [ ] ICH E6(R3) 체크리스트 16개 섹션 기준으로 검토 (Appendix B 근거 인용)

---

### Phase 10: `/icf`
```
/icf
```

**예상 행동**: icf-writer 호출, design_decisions.md 기반 Part 4 자동 추가

**검증 Checkpoint 7:**
- [ ] `_workspace/04_icf_draft.md` 생성
- [ ] **Part 4 자동 포함** (DDI 시험 + PG 분석 → 생명윤리법 적용):
  - 5.1 약물유전체(PG) 분석 동의 — CYP2C19 명시
  - 5.2 대사체 분석 동의 (활성 대사체 측정)
  - 5.3 잔여 검체 보관 동의
  - 5.4 연구 결과 통보 동의 (PG 임상적 중요 소견)
- [ ] design_decisions.md의 분석 계획과 ICF Part 4가 정합
- [ ] Part 1-3 (설명서·서명·개인정보)가 시험 절차와 일치

---

## 5. 결함 기록 방법

각 Checkpoint에서 실패 발견 시 `E2E_TEST_REPORT.md`(새 세션에서 생성)에 기록:

```markdown
### 결함 #N — [Phase X Checkpoint Y]
- **예상 동작**: ...
- **실제 동작**: ...
- **영향 범위**: Critical / Major / Minor
- **재현 방법**: ...
- **원인 추정**: (에이전트 정의 오류 / 스킬 문서 불명확 / API 응답 형식 변경 등)
- **수정 제안**: ...
```

E2E 완료 후 결함을 **일괄 수정**(본 세션에서는 실행하지 않고 기록만). 다음 세션에서 수정 진행.

---

## 6. 산출물 저장 위치

새 세션에서 생성될 파일들:
```
e2e/v2_2026_04_14_DDI/
├── E2E_EXECUTION_GUIDE.md    # (이 파일)
├── CHECKLIST.md              # 검증 체크리스트 (별도)
├── TRIAL_INFO_INPUT.md       # 시험 정보 입력
├── E2E_TEST_REPORT.md        # (신규 세션에서 작성) — 결함 로그 + 종합 평가
└── _workspace/               # (신규 세션에서 생성)
    ├── 00_input/
    ├── 01_references/
    ├── 01_research_*.md
    ├── 01_research_report.md
    ├── 02_synopsis.md
    ├── 03_protocol_draft.md
    ├── 04_icf_draft.md
    └── review/
```

**주의**: 루트 `_workspace/`는 `.gitignore`에 의해 무시되나, **`e2e/*/` 하위 `_workspace/`는 추적됨** (v1 디렉토리가 증거). E2E 결과를 git 이력에 남기기 위함.

---

## 7. 구 버전(v1 BE)과의 비교 포인트

v2 실행 완료 후 v1과 구조적 비교 (품질 평가용):

| 비교 축 | v1 (BE, 4-agent) | v2 (DDI, 8-agent) 예상 |
|--------|-----------------|----------------------|
| `01_references/` 하위 디렉토리 수 | 4개 (trials, literature, guidelines, labels) | 7개+ (pd_biomarkers, pharmacogenomics, metabolomics 추가) |
| `01_research_*.md` 에이전트별 파일 수 | 3개 (cp, reg, clin) | 4개 (+ts) |
| Protocol Appendix B 섹션 수 | 일부 누락 가능 | 16개 완전 |
| Review 파일 수 | 3-4개 | 5개 (TS 포함) |
| ICF Part 4 | 없음/간략 | PG+대사체+잔여 검체+결과 통보 |
| Reference 소스 다양성 | PubMed, ICD-10, MFDS guidelines | + DailyMed, openFDA, MFDS searchClinic, PharmGKB, CPIC |

→ 단순히 "더 많다"가 아닌, **실제 임상약리학자에게 유용한 정보인가** 기준으로 평가.

---

## 8. 실행 시 주의사항

- **모든 Reference는 실제 존재해야 함**. MCP/WebFetch 결과에서 확인된 것만 인용. 날조 의심 시 즉시 중단하고 기록
- **Phase 7 Gate는 건너뛸 수 없음**. Synopsis 명시적 승인 후 Protocol 진행
- **Web API 응답 시간**: PharmGKB 2 req/sec 제한, MFDS는 명시 없으나 느릴 수 있음
- **토큰 소비**: 전체 파이프라인에서 상당한 토큰 사용. 중간에 세션 종료 시 재개 가능한지 확인
- **결함 발견 ≠ 실패**: 결함은 개선 기회. 기록하고 계속 진행

---

## 9. 성공 기준

E2E가 "성공"이라 판단할 기준:
1. **파이프라인 완주**: Phase 1 → 10 모두 에러 없이 완료
2. **Checkpoint 1-7 통과율 ≥ 80%**: 일부 결함은 허용, 파이프라인 무결성 중심
3. **Critical 결함 ≤ 2건**: 파이프라인 중단 유발 결함 최소화
4. **데이터 흐름 일관성**: design_decisions → synopsis → protocol → ICF 간 주요 결정 사항 불일치 없음

---

## 10. 시작하기

**새 세션에서 다음 명령으로 시작**:

```
/research

(또는 orchestrator 사용 시)
Clopidogrel + Omeprazole DDI 임상시험 문서를 작성해줘.
시험 정보는 e2e/v2_2026_04_14_DDI/TRIAL_INFO_INPUT.md 참조.
검증 체크리스트는 e2e/v2_2026_04_14_DDI/CHECKLIST.md 참조.
```

**참고 파일**:
- 시험 정보 상세: `TRIAL_INFO_INPUT.md`
- 체크리스트 (Phase별): `CHECKLIST.md`
- 본 가이드: `E2E_EXECUTION_GUIDE.md`

완료 후 `E2E_TEST_REPORT.md`를 작성하여 결과와 발견 결함을 요약한다.
