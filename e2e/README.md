# E2E (End-to-End) 테스트 세션

하네스의 실제 동작을 검증한 E2E 세션 기록. 버전별로 분리하여 구/신 구조를 비교 가능하게 보존.

## 디렉토리 구조

```
e2e/
├── README.md                       # (본 파일)
├── v1_2026_04_06_BE/               # 초기 4-에이전트 구조, Amlodipine BE
│   ├── E2E_TEST_REPORT.md
│   └── _workspace/                 # 실행 산출물 (보존)
└── v2_2026_04_14_DDI/              # 8-에이전트 + TS + Web API 5종, Clopidogrel+Omeprazole DDI
    ├── E2E_EXECUTION_GUIDE.md      # 실행 가이드
    ├── TRIAL_INFO_INPUT.md         # 시험 정보 입력 템플릿
    ├── CHECKLIST.md                # Phase별 검증 체크리스트
    ├── E2E_TEST_REPORT_TEMPLATE.md # 실행 리포트 템플릿
    └── _workspace/                 # (신규 세션에서 생성)
```

## 버전별 요약

### v1 (2026-04-06): Amlodipine BE
- **구조**: 4 에이전트 (clinical-pharmacologist, regulatory-expert, clinician, biostatistician) + protocol-writer + icf-writer + qa-reviewer
- **Web API 통합**: 없음 (PubMed, ClinicalTrials.gov, ICD-10 MCP만)
- **ICH 체크리스트**: 13개 추정 항목
- **상태**: 완료 (`v1_2026_04_06_BE/E2E_TEST_REPORT.md` 참조)

### v2 (2026-04-14 예정): Clopidogrel + Omeprazole DDI
- **구조**: 8 에이전트 (v1 + **translational-scientist** 신설)
- **Web API 통합**: DailyMed, openFDA, MFDS 의약품안전나라, PharmGKB, CPIC (WebFetch)
- **ICH 체크리스트**: **16개 공식 섹션** (ICH E6(R3) Appendix B 원문 기반)
- **Phase 4 재구성**: 선정/제외기준 → 유효성/PD → 유전체/대사체 협의 순서
- **ICF Part 4**: PG/대사체/잔여 검체/결과 통보 자동 포함
- **상태**: 계획 수립 완료, 실행 대기 (새 세션에서 `E2E_EXECUTION_GUIDE.md` 따라 실행)

## 실행 순서

1. v2 가이드 검토: `v2_2026_04_14_DDI/E2E_EXECUTION_GUIDE.md`
2. 새 Claude Code 세션 시작
3. 체크리스트와 함께 파이프라인 실행
4. 완료 후 `E2E_TEST_REPORT.md` 작성 (템플릿 기반)
5. 결함 일괄 수정 (후속 세션)
