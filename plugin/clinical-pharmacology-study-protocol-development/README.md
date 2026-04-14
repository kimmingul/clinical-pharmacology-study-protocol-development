# clinical-pharmacology-study-protocol-development

> 한국 MFDS 환경 기준 임상약리 임상시험의 배경 조사·Synopsis·계획서(Protocol)·동의설명서(ICF)를 8개 전문 에이전트와 10단계 파이프라인으로 개발하는 Claude Code 플러그인.

## 개요

FIH, SAD/MAD, DDI(단방향·양방향), BA/BE, FE, QTc, ADME 등 임상약리 Phase 1 시험 유형을 지원한다. ICH E6(R3) Appendix B의 16개 공식 섹션 구조, MFDS·FDA·EMA 규제 가이드라인 사전 라이브러리, MFDS 의약품안전나라 2단계 크롤링(검색 리스트 HTML + Nexacro SOAP 상세 본문), Williams 6×3 양방향 DDI 설계를 모두 내장.

## 에이전트 (8)

| 에이전트 | model | 역할 | 참여 |
|---|---|---|---|
| clinical-pharmacologist | sonnet | PK·대사·DDI 기전·용량 근거·FIH 초기 용량·**DDI 방향성 평가 매트릭스** | 항상 |
| translational-scientist | sonnet | PD 바이오마커·PK-PD·약물유전체·대사체·수용체 점유율 | BE/FE 외 |
| regulatory-expert | sonnet | MFDS/FDA/EMA 가이드라인·약물 라벨·MFDS 승인현황(Nexacro SOAP)·ICD-10 | 항상 |
| clinician | sonnet | 선정/제외·안전성 프로파일·모니터링·중지 기준 (Thienopyridine TTP 4종 세트 등 계열별 체크리스트) | 항상 |
| biostatistician | sonnet | 연구설계·sample size(Python)·무작위화·SAS PROC MIXED·**Williams 6×3 양방향 IUT** | 항상 |
| protocol-writer | opus | Synopsis·자료 기반 Full Protocol (ICH E6(R3) Appendix B 16 섹션) | Phase 8 |
| icf-writer | opus | 계획서 기반 동의문서 (Part 1–3 + Part 4 PG/대사체/보관/결과통보) | Phase 10 |
| qa-reviewer | opus | 다중 리뷰 통합·Critical/Major/Minor 분류·수정 조율 | Phase 9 |

## Commands (7)

| Command | Phase | 기능 |
|---|---|---|
| `/research` | 2–3 | 병렬 자료 수집 + 사용자 검토 게이트 |
| `/design` | 4–5 | 대화형 설계 협의 + 통계 설계 (DDI 방향성 결정 포함) |
| `/synopsis` | 6 | Synopsis 생성. 설계 변형을 인자로 지정(`/synopsis crossover 6x3` 등) |
| `/compare` | 6 | 여러 Synopsis를 비교표로 제시 |
| `/protocol` | 8 | Full Protocol 작성 (Synopsis 승인 필수) |
| `/review` | 9 | 4–5명 병렬 리뷰 + QA 취합 |
| `/icf` | 10 | 동의문서 작성 (Protocol 필수) |

## Skills (5)

| Skill | 용도 |
|---|---|
| `trial-doc-orchestrator` | 전체 10단계 파이프라인 조율, 사용자 게이트 관리 |
| `clinical-research` | 배경 조사 4-agent 분업 + MFDS 2단계 크롤링 절차 |
| `protocol-drafting` | ICH E6(R3) Appendix B 16 섹션 템플릿·Phase 1 용어 가이드·AUC 시간 범위 선택 |
| `regulatory-review` | 다중 리뷰 체크리스트·상충 해결·문서 간 일관성 |
| `icf-drafting` | 쉬운 한국어 변환·PIPA·생명윤리법 Part 4 자동 반영 |

## 로컬 설치

```bash
# Plugin 루트 디렉토리(본 README가 위치한 디렉토리)를
# Claude Code plugin 디렉토리로 심볼릭 링크 또는 복사
ln -s "$(pwd)" ~/.claude/plugins/clinical-pharmacology-study-protocol-development

# 재시작 후 활성화 확인
claude plugin list
```

또는 zip 업로드가 요구되는 UI의 경우, 본 디렉토리를 그대로 zip으로 압축하여 업로드.

### 필수 요구사항

- Claude Code (latest)
- Python 3.10+ with `scipy` (sample size 계산용): `pip install scipy`
- PubMed·ClinicalTrials.gov·DailyMed·openFDA·PharmGKB·CPIC 접근 가능한 네트워크 환경

## 사용 예시

```bash
# 사용자 프로젝트 디렉토리에서:
cd ~/Projects/my-clinical-trial/
claude

# Claude Code 세션에서:
/research   # 병렬 자료 수집 → 사용자 검토
/design     # 대화형 설계 협의 → biostatistician sample size
/synopsis   # Synopsis 생성
# (사용자가 검토·승인)
/protocol   # Full Protocol 작성
/review     # 4–5명 병렬 리뷰 + QA
/icf        # 동의문서 작성
```

산출물은 사용자의 현재 작업 디렉토리의 `_workspace/` 하위에 생성된다.

## 외부 데이터 소스

### 통합된 Web API (WebFetch 기반, 인증 불필요)

| 소스 | 용도 | 레시피 |
|---|---|---|
| **DailyMed** (`dailymed.nlm.nih.gov/dailymed/services/v2/`) | 미국 FDA 승인 약물 SPL 라벨 전문 | `references/api_reference/dailymed.md` |
| **openFDA** (`api.fda.gov/drug/`) | 허가 정보·NDA·FAERS·보조 라벨 | `references/api_reference/openfda.md` |
| **MFDS 의약품안전나라** (`nedrug.mfds.go.kr/searchClinic` + `/ext/CCAAK02F010/*`) | 국내 임상시험 승인현황 리스트 + Nexacro SOAP 상세 본문 | `references/api_reference/mfds.md` |
| **PharmGKB/ClinPGx** (`api.pharmgkb.org/v1/`) | 약물-유전자 임상 annotation (CC BY-SA 4.0) | `references/api_reference/pharmgkb.md` |
| **CPIC** (`api.cpicpgx.org/v1/`) | 표현형별 용량 조절 권고 (CC0) | `references/api_reference/cpic.md` |

### 사전 수록 규제 라이브러리

`references/guidelines/` 에 ICH(E6 R3, E8 R1, E14, M13A) + FDA + EMA + MFDS 가이드라인 + 국내 법령(약사법, KGCP, PIPA, 생명윤리법) + 시험 유형별 cross-agency 비교표 6건(BE, DDI, FIH, QTc, FE, PK 일반)이 사전 수록되어 있다.

## 시험 유형별 지원

| 시험 유형 | 주요 설계 | Sample size 스크립트 |
|---|---|---|
| FIH/SAD | 순차 증량, 센티넬, MRSD | `scripts/fih/starting_dose_calculation.py` |
| MAD | 반복 투여, 정상상태 | `scripts/sample_size/crossover_2x2_ddi.py` (응용) |
| **DDI 단방향** | One-sequence, 2×2 crossover | `one_sequence_ddi.py`, `crossover_2x2_ddi.py` |
| **DDI 양방향** ★ | **Williams 6×3** (A 단독, B 단독, A+B) | **`williams_6x3_ddi.py`** (IUT 기반) |
| BE | 2×2, 2×3/2×4 replicate (RSABE) | `crossover_2x2_be.py`, `replicate_crossover_be.py` |
| FE | 2×2 crossover | `crossover_2x2_be.py` |
| QTc | Williams 4×4 | `williams_4x4.py` |
| Parallel | 연속형/이분형 | `parallel_continuous.py`, `parallel_binary.py` |

## 핵심 설계 원칙

- **사용자 게이트 2개**: Phase 3 자료 조사 승인, Phase 7 Synopsis 승인 (Hard Gate)
- **Reference 의무화**: 모든 조사에 PMID/NCT/URL/가이드라인 인용
- **Synopsis 보존**: Phase 7 승인된 결정은 Protocol에서 변경 불가
- **ICF 분리**: `/icf` 별도 지시로 실행 (Protocol 필수)
- **방향성 매트릭스**: DDI 시험에서 단방향/양방향을 clinical-pharmacologist가 평가·권고
- **부분 재실행**: 수정 요청 시 하류 의존성 자동 전파

## 라이선스

MIT License.

## Author

Min-Gul Kim
