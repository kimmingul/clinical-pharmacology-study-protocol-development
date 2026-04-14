# E2E 검증 체크리스트 — v2 DDI

> 각 Phase 실행 후 해당 Checkpoint를 확인하고 Pass/Fail/Partial 기록.
> Fail/Partial 시 `E2E_TEST_REPORT.md`에 결함 상세 기록.

---

## Checkpoint 1 — Phase 1 입력 확인

| 항목 | 예상 | 결과 |
|------|------|------|
| `_workspace/00_input/trial_info.md` 생성 | 존재 | ☐ |
| 시험 유형 "DDI" 기록 | 포함 | ☐ |
| 약물 계열·CYP 대사 경로 포함 | 포함 | ☐ |
| "유전체/인체유래물 포함 여부" 항목 **없음** | 제거됨 (Phase 4로 이관) | ☐ |
| IB 파일 미제공 상태 (DDI이므로 정상) | 정상 | ☐ |

---

## Checkpoint 2 — Phase 3 Gate (자료 조사 승인)

### 2-1. 에이전트 호출

| 에이전트 | 예상 | 결과 |
|---------|------|------|
| clinical-pharmacologist | 호출 | ☐ |
| **translational-scientist** | **호출 (DDI → 필수 참여)** | ☐ |
| regulatory-expert | 호출 | ☐ |
| clinician | 호출 (항상 참여) | ☐ |

### 2-2. 산출물 파일

| 파일 | 존재 여부 |
|------|----------|
| `01_research_cp.md` | ☐ |
| `01_research_ts.md` ★ | ☐ |
| `01_research_reg.md` | ☐ |
| `01_research_clin.md` | ☐ |
| `01_research_report.md` (통합) | ☐ |

### 2-3. Reference 디렉토리

| 디렉토리 | 예상 내용 |
|---------|----------|
| `01_references/trials/` | NCT*.md 파일 (clopidogrel/omeprazole 관련) ☐ |
| `01_references/literature/` | PMID_*.md 파일 다수 ☐ |
| `01_references/guidelines/` | FDA DDI, EMA, MFDS, ICH M12 관련 ☐ |
| `01_references/labels/` | clopidogrel_DailyMed.md, clopidogrel_openFDA.md, omeprazole_*.md ☐ |
| `01_references/safety/` | AE_profile, SAE_cases, class_effect 등 ☐ |
| `01_references/pd_biomarkers/` ★ | VerifyNow PRU, LTA 등 ☐ |
| `01_references/pharmacogenomics/` ★ | CYP2C19.md (한국인 빈도 포함) ☐ |
| `01_references/metabolomics/` (해당 시) | Clopidogrel 활성 대사체 H4 ☐ |
| `01_references/mfds_clinical_trials/` ★ | searchClinic HTML 파싱 결과 ☐ |

### 2-4. Web API 실호출 흔적

| API | 검증 방법 |
|-----|---------|
| DailyMed | clopidogrel_DailyMed.md에 setid (UUID) 기재 ☐ |
| openFDA | clopidogrel_openFDA.md에 NDA 번호(020839) 기재 ☐ |
| MFDS searchClinic | mfds_clinical_trials/*.md에 "총 N건" + 실제 의뢰자명 ☐ |
| PharmGKB | pharmacogenomics/CYP2C19.md에 `/v1/data/` URL 인용 ☐ |
| CPIC | CYP2C19.md에 CPIC Level A 등급 + `/v1/pair_view` URL ☐ |

### 2-5. Reference 품질 (스팟 체크 3-5건)

- [ ] PubMed PMID 무작위 3개 선택 → 실제 존재 확인 (WebFetch로 검증)
- [ ] NCT 번호 무작위 2개 선택 → ClinicalTrials.gov에서 확인
- [ ] DailyMed setid → 실제 라벨 페이지 로드 가능 확인

### 2-6. 통합 보고서 섹션

`01_research_report.md`에 다음 섹션 모두 존재:

- [ ] 1. 적응증 개요
- [ ] 3. PK 자료 (CP)
- [ ] 4. **PD/약력학 자료 (TS)** ★
- [ ] 5. 유사 시험 분석
- [ ] 6. 규제 가이드라인
- [ ] 7. 약물 라벨 정보 (PG 섹션 포함)
- [ ] 8. MFDS 임상시험 승인현황
- [ ] 9. 임상적 고려사항·안전성
- [ ] **10. 약물유전체학(PG) 자료 (TS)** ★
- [ ] 11. 대사체 자료 (해당 시)
- [ ] 12. 종합 고려사항
- [ ] 13. 참고 문헌 (통합)

---

## Checkpoint 3 — Phase 4 설계 협의

### 3-1. Step 1: 선정/제외 기준

- [ ] `.claude/references/templates/inclusion_exclusion_criteria.md` 템플릿 인용/제시
- [ ] 표준 선정 6항목 + 제외 15항목 기반 협의
- [ ] **CYP2C19 PM 제외** 또는 **층화** 논의 발생 (약물 특이 추가 항목)
- [ ] 한국인 PM 빈도 ~15% 반영된 논의
- [ ] 최종 선정/제외 기준 `design_decisions.md`에 번호와 함께 기록

### 3-2. Step 2: 연구설계

- [ ] 시험 유형별 설계 옵션 제시 (DDI → One-sequence / Crossover / Parallel)
- [ ] Fixed-sequence crossover 선택 (비가역적 억제 고려)

### 3-3. Step 3: 세부 요소

- [ ] PK 채혈 시점 (Clopidogrel 활성 대사체 고려한 밀집 구간)
- [ ] 1차 평가변수: **활성 대사체 AUC/Cmax GMR** (90% CI 80-125%)
- [ ] 2차 평가변수
- [ ] **유효성/PD 평가 항목** (VerifyNow PRU, LTA 등) ★
- [ ] 안전성 평가
- [ ] **유전체/대사체 분석 계획** ★
  - [ ] PG: CYP2C19 *2, *3, *17 분석 / 스크리닝 시점
  - [ ] 대사체: Clopidogrel 활성 대사체 H4 측정
  - [ ] 잔여 검체 보관 여부·기간
- [ ] Washout 기간 (혈소판 수명 고려 ≥14일)
- [ ] 투여 조건 (공복, 수분 제한 등)

### 3-4. Step 4: 기록

- [ ] `design_decisions.md`에 모든 결정 포함
- [ ] "유전체/대사체 분석 계획" 섹션이 명시적으로 존재 (ICF와 연계 명시)

### 3-5. Step 5-6: 통계 (biostatistician)

- [ ] biostatistician Agent 호출
- [ ] `crossover_2x2_ddi.py` 또는 유사 스크립트 사용
- [ ] Sample size 계산 결과 + Python 코드 전체 포함
- [ ] `statistical_design.md` 생성
- [ ] 탈락률 반영된 최종 대상자 수

---

## Checkpoint 4 — Phase 7 Gate (Synopsis 승인, Hard)

`02_synopsis.md` 구조 확인 (13개 섹션):

| 섹션 | 존재 |
|------|------|
| 1. 시험 제목 | ☐ |
| 2. 시험 목적 (1차/2차) | ☐ |
| 3. 시험 설계 | ☐ |
| 4. 대상자 (선정·제외 **전체 항목**) | ☐ |
| 5. 시험약 및 투여 | ☐ |
| 6.1 1차 평가변수 (**"유효성 평가" 표현 사용**) ★ | ☐ |
| 6.2 2차 평가변수 | ☐ |
| **6.3 유효성/약력학(PD) 평가 항목** ★ | ☐ |
| 6.4 절단 AUC (DDI는 해당 없음 → 섹션 생략 가능) | ☐ |
| 7. PK 채혈 시점 및 근거 | ☐ |
| 8. Washout 근거 | ☐ |
| 9. 안전성 평가 | ☐ |
| **10. 유전체/대사체 분석 계획** ★ | ☐ |
| 10.1 PG 분석 (CYP2C19 명시) | ☐ |
| 10.2 대사체 분석 (해당 시) | ☐ |
| 10.3 인체유래물 보관 정책 | ☐ |
| 11. 통계 분석 | ☐ |
| 12. 방문 일정 요약 | ☐ |
| 13. 시험 기간 | ☐ |

**Gate 통과 조건**: 사용자가 명시적으로 "Synopsis 승인" 응답

---

## Checkpoint 5 — Phase 8 Protocol

`03_protocol_draft.md`가 **ICH E6(R3) Appendix B 16개 섹션** 모두 포함:

| # | 섹션 | 존재 | 내용 적절성 |
|---|------|------|-----------|
| B.1 | General Information | ☐ | 프로토콜 번호, 버전(v1.0), 날짜 명시 ☐ |
| B.2 | Background Information | ☐ | IB 없으므로 문헌 기반, FDA 블랙박스 경고 인용 ☐ |
| B.3 | Trial Objectives and Purpose | ☐ | 1차/2차 목적 + Estimand (선택) ☐ |
| B.4 | Trial Design | ☐ | Fixed-sequence crossover, 평가변수, 중지 규칙 ☐ |
| B.5 | Selection of Participants | ☐ | Synopsis 4와 완전 일치 ☐ |
| **B.6** | **Discontinuation of Trial Intervention** ★ | ☐ | 기존 누락 섹션 ☐ |
| B.7 | Treatment and Interventions | ☐ | 허용·금지 병용약 (CYP2C19 영향 약물 제한) ☐ |
| **B.8** | **Assessment of Efficacy** ★ | ☐ | 활성 대사체 GMR를 "유효성 평가변수"로 기술 ☐ |
| B.9 | Assessment of Safety | ☐ | AE/SAE 보고, 혈소판 수치 모니터링 등 ☐ |
| B.10 | Statistical Considerations | ☐ | Sample size, 90% CI 80-125% 기준 ☐ |
| **B.11** | **Direct Access to Source Records** ★ | ☐ | 기존 누락 섹션 ☐ |
| B.12 | Quality Control and Quality Assurance | ☐ | ☐ |
| B.13 | Ethics | ☐ | IRB, Declaration of Helsinki, **생명윤리법**(PG 분석) ☐ |
| B.14 | Data Handling and Record Keeping | ☐ | ☐ |
| **B.15** | **Financing and Insurance** ★ | ☐ | 기존 누락 섹션 (간략 기술 허용) ☐ |
| **B.16** | **Publication Policy** ★ | ☐ | 기존 누락 섹션 (간략 기술 허용) ☐ |

### MFDS IND 필수 요소 체크 (Protocol-drafting SKILL 기준)

- [ ] 약사법 제34조 IND 승인 절차
- [ ] IND 승인 후 시험 개시 명시
- [ ] IRB/IEC 승인 절차
- [ ] 시험대상자 보험 가입
- [ ] MFDS 변경 승인/보고 절차
- [ ] SAE/SUSAR 보고 절차 (MFDS + IRB)
- [ ] 시험 종료/조기 중단 시 MFDS 보고

### Synopsis-Protocol 일관성

| 비교 항목 | 일치 여부 |
|----------|----------|
| 시험 설계 | ☐ |
| 1차 평가변수 | ☐ |
| 대상자 수 | ☐ |
| 선정/제외 기준 (전체) | ☐ |
| 유전체/대사체 분석 계획 | ☐ |

---

## Checkpoint 6 — Phase 9 Review (5명)

### 6-1. 리뷰 파일

| 파일 | 생성 여부 | 품질 |
|------|----------|------|
| `review_clinical_pharmacologist.md` | ☐ | PK 초점 유지 ☐ |
| `review_translational_scientist.md` ★ | ☐ | PD·PG·ICF 정합성 초점 ☐ |
| `review_clinician.md` | ☐ | 안전성·선정/제외 초점 ☐ |
| `review_regulatory_expert.md` | ☐ | ICH B.1-B.16 체크 ☐ |
| `review_biostatistician.md` | ☐ | 통계 초점 ☐ |

### 6-2. QA 취합 보고서

`review/qa_review_report.md`:

- [ ] 5명 취합 명시
- [ ] Critical/Major/Minor 분류
- [ ] 리뷰어 간 상충 의견 기록 (있는 경우)
- [ ] Synopsis-Protocol 일관성 점검표
- [ ] 규제 체크리스트 결과 (ICH E6 R3 16개 섹션 기준)

### 6-3. 용어 정책 검증

- [ ] B.8 "Assessment of Efficacy" / "유효성 평가" 사용을 **Critical로 지적하지 않음** (정책 완화 반영)
- [ ] TS 리뷰가 누락된 경우 Critical로 지적 (DDI 이므로 참여 필수)

### 6-4. Critical 자동 수정 (해당 시)

- [ ] Critical 발견 시 protocol-writer 재호출
- [ ] 수정 후 1회 재리뷰
- [ ] 최대 1회 시도 후 잔여 Critical은 사용자 보고

---

## Checkpoint 7 — Phase 10 ICF

`04_icf_draft.md` 구조:

### 7-1. 기본 구조

- [ ] Part 1: 동의설명서 (14개 섹션)
- [ ] Part 2: 동의서 서명 페이지
- [ ] Part 3: 개인정보 수집·이용·제3자 제공 동의서 (PIPA)
- [ ] **Part 4: 선택 동의** ★ (PG + 대사체 분석 있으므로 필수 포함)

### 7-2. Part 4 세부 (생명윤리법)

- [ ] **5.1 약물유전체(PG) 분석 동의** — CYP2C19 *2, *3, *17 명시
- [ ] **5.2 대사체 분석 동의** — Clopidogrel 활성 대사체 H4 측정
- [ ] **5.3 잔여 검체 보관 동의**
- [ ] **5.4 연구 결과 통보 동의** (PG 임상적 중요 소견)

### 7-3. design_decisions.md와의 정합성

| 항목 | 일치 |
|------|------|
| PG 분석 대상 유전자 | ☐ |
| 대사체 분석 대상 마커 | ☐ |
| 잔여 검체 보관 기간 | ☐ |
| 연구 결과 통보 정책 | ☐ |

### 7-4. 계획서와의 정합성

- [ ] 채혈 횟수·총 채혈량 일치
- [ ] 방문 일정 일치
- [ ] 금지 사항 (CYP2C19 영향 약물) 일치
- [ ] 위험 정보 (PPI-Clopidogrel 상호작용 포함) 일치

### 7-5. 쉬운 언어

- [ ] 전문 용어에 괄호 설명
- [ ] Phase 1 임상시험의 직접적 치료 이익 과장 없음
- [ ] 유전형 검사 의미를 시험대상자 수준에서 설명

---

## 종합 평가

### 정량

| 항목 | 목표 | 실제 | 평가 |
|------|------|------|------|
| Checkpoint 1-7 통과율 | ≥ 80% | | ☐ |
| Critical 결함 | ≤ 2건 | | ☐ |
| Major 결함 | ≤ 5건 | | ☐ |
| 파이프라인 완주 | Yes | | ☐ |

### 정성

- 가장 잘 작동한 부분:
- 가장 큰 문제점:
- 다음 E2E (BE, QTc 등)에 필요한 개선:

---

## v1 (BE) vs v2 (DDI) 구조 비교

| 비교 축 | v1 (BE) | v2 (DDI) |
|--------|---------|----------|
| `01_references/` 디렉토리 수 | | |
| 조사 에이전트 수 | | |
| Research 보고서 섹션 수 | | |
| Protocol Appendix B 섹션 수 | | |
| Review 파일 수 | | |
| ICF Part 4 포함 여부 | | |
| Reference 소스 종류 | | |
