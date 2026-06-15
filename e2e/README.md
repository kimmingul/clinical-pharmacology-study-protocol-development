# E2E (End-to-End) 테스트 세션

하네스의 실제 동작을 검증한 E2E 세션 기록. 버전별로 분리하여 구/신 구조를 비교 가능하게 보존.

## 디렉토리 구조

```
e2e/
├── README.md                       # (본 파일)
├── v1_2026_04_06_BE/               # 초기 4-에이전트 구조, Amlodipine BE
│   ├── E2E_TEST_REPORT.md
│   └── _workspace/                 # 실행 산출물 (보존)
├── v2_2026_04_14_DDI/              # 8-에이전트 + TS + Web API 5종, Clopidogrel+Omeprazole DDI
│   ├── E2E_EXECUTION_GUIDE.md      # 실행 가이드
│   ├── TRIAL_INFO_INPUT.md         # 시험 정보 입력 템플릿
│   ├── CHECKLIST.md                # Phase별 검증 체크리스트
│   ├── E2E_TEST_REPORT_TEMPLATE.md # 실행 리포트 템플릿
│   └── _workspace/                 # 실행 산출물 (보존)
└── v3_2026_06_15_DDI_clopidogrel_omeprazole/  # v3 actor-critic 수렴 루프 + 가드레일 실증
    ├── E2E_REPORT.md               # 결과 리포트 (score 10→100, T0 차단→통과)
    └── _workspace/                 # goal_spec·초안·citation_audit·manifest
```

## 버전별 요약

### v1 (2026-04-06): Amlodipine BE
- **구조**: 4 에이전트 (clinical-pharmacologist, regulatory-expert, clinician, biostatistician) + protocol-writer + icf-writer + qa-reviewer
- **Web API 통합**: 없음 (PubMed, ClinicalTrials.gov, ICD-10 MCP만)
- **ICH 체크리스트**: 13개 추정 항목
- **상태**: 완료 (`v1_2026_04_06_BE/E2E_TEST_REPORT.md` 참조)

### v2 (2026-04-14): Clopidogrel + Omeprazole DDI
- **구조**: 8 에이전트 (v1 + **translational-scientist** 신설)
- **Web API 통합**: DailyMed, openFDA, MFDS 의약품안전나라, PharmGKB, CPIC (WebFetch)
- **ICH 체크리스트**: **16개 공식 섹션** (ICH E6(R3) Appendix B 원문 기반)
- **Phase 4 재구성**: 선정/제외기준 → 유효성/PD → 유전체/대사체 협의 순서
- **ICF Part 4**: PG/대사체/잔여 검체/결과 통보 자동 포함
- **상태**: 완료. 5명 리뷰 Major 8건 → 하네스 강화 반영 (가이드·템플릿·`_workspace/` 보존)

### v3 (2026-06-15): Clopidogrel + Omeprazole DDI — v3 제어 계층 실증
- **목적**: actor-critic 수렴 루프 · 3-tier 가드레일 · zero-trust 인용 검증 실증
- **actor**: 실제 opus `protocol-writer` / **critic**: 결정적 `doc_lint.py`
- **결과**: score **10 → 100**, Critical **4 → 0** (1회 반복 수렴), T0 hook **차단→통과**, dose guard `skipped`(DDI), 인용 검증에서 PMID verified / NCT not-found 포착
- **상태**: 완료 (`v3_2026_06_15_DDI_clopidogrel_omeprazole/E2E_REPORT.md`)

## 비고

- v1·v2는 **pre-v3 산출물**(구버전 동작 기준)이며 회귀·역사 비교용으로 보존한다.
- v3 이후 신규 검증은 `/finalize`(T0 게이트) + Phase 9 수렴 루프를 따른다.
