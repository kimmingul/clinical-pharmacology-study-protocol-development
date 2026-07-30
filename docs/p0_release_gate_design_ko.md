# P0 Fail-Closed Release Gate — 설계 문서

- 작성일: 2026-07-30
- 상태: 설계 승인 대기 → 구현 계획(writing-plans) 이관 예정
- 대상 버전: v4.2.0 이후
- 관련 산출물: `.xllm/artifacts/xllm/council-*.md`, `.xllm/artifacts/ask/{codex,grok}-cwd-*.md`

---

## 1. 배경

4-모델 협의체(xllm council) 검토에서 codex(GPT-5.6)는 `reject`(확신 0.98), grok(4.5)은
`mixed`(확신 0.86) 판정을 냈다. gemini-cli와 antigravity는 환경 문제로 기권했으므로,
실질은 **독립 2-모델 합의**이며 상호 반박에서 어느 주장도 기각되지 않았다(8 survived / 0 killed).

두 모델이 첫 번째로 꼽은 개선 항목이 동일했다.

> `/finalize`를 자연어 command가 아닌 독립된 fail-closed release executable로 교체하고,
> 모든 검사 결과·서명·artifact hash를 하나의 release evidence package로 묶는 것. (codex)

> `finalize.md` 절차를 **단일 CLI**로 고정(`finalize_run.py`). 에이전트 해석 제거. (grok)

### 1.1 실측 확인된 결함 4건

아래는 모델 주장을 그대로 옮긴 것이 아니라, **본 저장소에서 명령을 직접 실행해 재확인**한 결과다.

**① 결정적 채점이 규제 적합성을 보증하지 않는다**

```
$ python3 .claude/scripts/qa/doc_lint.py \
    e2e/v2_2026_04_14_DDI/_workspace/03_protocol_draft.md --score
{"doc_type": "protocol", "score": 100, "critical": [], "major": [], "minor": [], "passed": true}
```

같은 파일에 대한 5인 전문가 리뷰 결과(`e2e/v2_2026_04_14_DDI/_workspace/review/qa_review_report.md:14`):

```
- **통합 후 최종 분류**: **Critical: 0건 | Major: 8건 | Minor: 16건**
```

→ `score≥90`은 구조 위생 지표이며 제출 적합성 지표가 아니다.

**② `citation_verify`는 실패해도 차단할 수 없다**

```
$ grep -n "sys.exit" .claude/scripts/qa/citation_verify.py
(출력 없음)
```

`main()`에 종료코드 설정이 없어 `format_fail`/`not_found`가 있어도 항상 exit 0.

**③ `goal_spec` 필드 다수가 소비되지 않는다**

```
$ grep -rn "must_cite_types\|target_power\|acceptable_ci_bounds\|icf_readability_target" \
    .claude/scripts/
(출력 없음)
```

스키마에 "성공 명세"로 정의되어 있으나 어떤 스크립트도 읽지 않는다.

**④ `/finalize`가 검사 결과를 release 조건으로 강제하지 않는다**

`.claude/commands/finalize.md` 실측:

| 줄 | 내용 | 문제 |
|----|------|------|
| 32 | `doc_lint --strict ...; LINT=$?` | 종료코드 저장 O |
| 35 | `doc_lint --score` | 주석이 "(b) 채점 (참고용)" |
| 38 | `citation_verify.py audit ...` | **종료코드 미저장** |
| 55 | `| score | ≥ 90 권장 | 90 미만이면 경고 + 사용자 확인 |` | 차단 아님 |

→ ①~③은 모두 ④에서 파생된다. "검사기를 호출했다"와 "검사 결과가 release를 막는다"가
분리되어 있고, 그 경계가 자연어 command와 에이전트 준수에 의존한다.

---

## 2. 목표 / 비목표

### 2.1 목표

1. release 판정을 **단일 실행 파일**로 이전하여 에이전트 해석을 제거한다.
2. 검사 누락·검사기 크래시가 "통과"로 집계되지 않게 한다(fail-closed).
3. "작성 중 점검"과 "제출 직전 판정"을 **프로파일로 분리**하여, 초안 단계의 정상 상태를
   결함으로 오탐하지 않으면서 제출 직전에는 타협하지 않는다.
4. 판정 근거를 기계 판독 가능한 단일 리포트로 남긴다.

### 2.2 비목표 (이번 범위에서 제외)

| 제외 항목 | 해당 로드맵 |
|----------|-----------|
| 서명 이벤트 스토어 / RBAC 승인 워크플로 | P0-5 |
| claim–evidence graph | P0-3 |
| typed `TrialSpec` | P0-4 |
| 시험유형별 과학 룰팩(`science_lint`) | P1-1 |
| `doc_lint`·`citation_verify`·`dose_safety_guard` 내부 로직 수정 | — |
| Phase 3/7 사람 게이트 흐름 변경 | P0-5 |
| `goal_spec` 미사용 필드 구현 | P1 |

---

## 3. 설계 결정 (5건)

### D1. 검사기는 subprocess가 아니라 라이브러리로 호출한다

`finalize_run.py`가 검사기를 `import`하여 함수를 직접 호출한다.

**근거**
- `.claude/hooks/draft_advisory_hook.py:73-96`이 이미 동일 패턴을 사용한다
  (`import doc_lint; doc_lint.lint_file(file_path)`).
- 검사기 3종이 이미 라이브러리 API를 노출한다:
  `doc_lint.lint_file()` / `doc_lint.score_file()` / `citation_verify.audit_files()` /
  `dose_safety_guard.check_file()`.
- `citation_verify`의 CLI 계약을 변경하지 않으므로 기존 호출자 파손 위험이 없다
  (CLI 호출자는 `finalize.md` 1곳뿐임을 확인).

**트레이드오프**: 검사기가 무한 대기하면 게이트도 멈춘다. 현재 유일한 네트워크 I/O
경로(`citation_verify.verify_online`)에 `timeout=8`이 이미 설정되어 있어 실질 위험은 낮다.

### D2. `doc_lint score`는 게이트에서 제거한다

score는 통과/차단 판정에 사용하지 않고 참고 수치로만 출력한다.

**근거**: §1.1 ①. score=100과 전문가 Major 8건이 공존한다. score를 게이트에 남기면
"몇 점이면 제출 가능한가"라는 잘못된 질문이 계속 생기고, 점수 상승만을 노린 최적화
유인이 남는다(Goodhart). 두 모델 모두 이를 "버려야 할 것"으로 지목했다.

### D3. 심각도 정책은 게이트가 소유한다

검사기는 사실(finding)만 보고하고, "이 발견이 차단인가"는 게이트가 프로파일에 따라 판정한다.

**근거**: 같은 발견의 심각도가 시점에 따라 다르다. `[시험기관명]` 같은 placeholder는
작성 중에는 정상이고 제출 직전에는 차단 사유다. 심각도를 검사기에 두면 작성 중 훅이
정상 초안을 error로 보고하게 된다(`finalize.md:71`이 같은 취지를 이미 기술).

**구현 방식**: 게이트가 `doc_lint.PLACEHOLDER_PATTERNS`(`doc_lint.py:38`)와
`doc_lint.UNVERIFIED_MARKERS`(`doc_lint.py:48`)를 **모듈 상수로 import**한다. warning
문자열 파싱도, 패턴 중복도, 검사기 수정도 발생하지 않는다.

### D4. 프로파일을 둘로 나눈다 — `draft` / `submission`

**근거**: `citation_verify.audit_files(..., online=False)`가 기본값이며, offline에서는
형식만 검사하므로 `not_found`가 항상 0이다. 즉 offline에서 `not_found=0` 기준은 자동으로
참이 되어 아무것도 막지 못한다. 반대로 online을 항상 강제하면 제약사 내부망·오프라인
환경·CI에서 게이트를 돌릴 수 없어 현장에서 우회하게 된다(지킬 수 없는 게이트는 지산직).

### D5. 차원 [4]는 `advisory`이며 `doc_lint` warning **전체**를 대상으로 한다

**근거**: `doc_lint.lint_icf()`에서 PIPA 누락(`doc_lint.py:149`)과 PG 선택동의 누락
(`doc_lint.py:156`)은 error가 아니라 **warning**이다. 차원 [4]를 placeholder로만
한정하면 이 두 항목이 차원 [1](errors=0)에도 [4]에도 걸리지 않아 통과한다.

warning 전체를 submission 차단 대상으로 두면 (a) 어떤 warning이 차단인지 분류할 필요가
없고, (b) 검사기를 수정하지 않으며, (c) placeholder·미확인 인용·PIPA 누락·PG 선택동의
누락·CI 경계(80.00/125.00) 표기 누락이 자동으로 커버된다.

**기존 CI 영향 없음(확인)**: CI가 `--strict`로 검사하는 golden fixture
(`e2e/v2_2026_04_14_DDI/_workspace/03_protocol_draft.md`)는 warning이 0건이다.

---

## 4. 아키텍처

```
                    ┌───────────────────────────────┐
  대상 문서 ──────▶│      finalize_run.py           │
  --profile         │  (release를 결정하는 유일한 곳)  │
                    └───────────────────────────────┘
                         │ import (subprocess 아님, D1)
        ┌────────────────┼────────────────┬──────────────────┐
        ▼                ▼                ▼                  ▼
   doc_lint.        citation_verify.  dose_safety_guard.  doc_lint.
   lint_file()      audit_files()     check_file()        PLACEHOLDER_PATTERNS
   score_file()                                          UNVERIFIED_MARKERS
        │                │                │                  │
        └────────────────┴────────────────┴──────────────────┘
                         │  Finding 목록 (사실만, 심각도 없음)
                         ▼
              ┌──────────────────────────┐
              │  심각도 정책 (게이트 소유, D3) │
              └──────────────────────────┘
                         ▼
   _workspace/verification/release_gate.json  +  터미널 요약  +  종료코드
```

### 4.1 구성요소

| 구성요소 | 책임 | 분리 이유 |
|---------|------|----------|
| `Status` | 상태 어휘(§5) | "검사 안 함"과 "통과"를 구조적으로 구분 |
| `Dimension` | 차원 하나(id, 이름, 실행 함수) | 차원 추가가 표 한 줄로 끝남 |
| `Profile` | 프로파일별 차단 규칙 | 정책이 한 곳에 모임 |
| `run_gate()` | 차원 실행 → 집계 → 종료코드 | 판정 로직 단일 함수 |

경로는 모두 `__file__` 기준 상대경로로 해석한다(`draft_advisory_hook.py` 패턴).
`plugin/` 미러의 `.py`는 `.claude/` 문자열 치환 대상이 아니므로
(`sync_plugin.sh:44`는 `*.md`만 치환) 런타임 경로를 하드코딩하지 않는 것이 필수다.

---

## 5. 상태 어휘

| 상태 | 의미 | draft 집계 | submission 집계 |
|------|------|-----------|----------------|
| `PASS` | 검사 실행됨, 차단 사유 없음 | 통과 | 통과 |
| `FAIL` | 검사 실행됨, 차단 사유 있음 | 차단 | 차단 |
| `SKIPPED` | 해당 없음(예: 비-FIH의 용량 검사) | 통과 | 통과 |
| `FORMAT_ONLY` | 부분만 검증됨(offline 인용) | 통과(표시) | 차단 |
| `NOT_IMPLEMENTED` | 기반 미구현(승인 차원) | 집계 제외 + 경고 | 집계 제외 + 경고 |
| `ERROR` | 검사기 예외/크래시 | 차단 (exit 2) | 차단 (exit 2) |

`FAIL`은 exit 1, `ERROR`는 exit 2로 서로 다른 종료코드에 대응한다(§7).

`NOT_IMPLEMENTED`를 별도 상태로 두는 이유: 미구현 통제를 조용히 빠뜨리는 대신 매 실행마다
출력에 노출시킨다. 현재 문제의 본질이 "검사가 있는 척"이었으므로 같은 공백을 만들지 않는다.

---

## 6. 차원 정의

| # | id | 사용하는 것 | draft 기준 | submission 기준 |
|---|-----|-----------|-----------|----------------|
| 1 | `structure` | `doc_lint.lint_file()` errors | errors = 0 | errors = 0 |
| 2 | `citation` | `citation_verify.audit_files()` | offline → `FORMAT_ONLY` | online 필수. `format_fail=0` AND `not_found=0` AND `unverified_network=0`. 네트워크 불가 → `FAIL` |
| 3 | `dose` | `dose_safety_guard.check_file()` + `goal_spec.trial_type` | violation = 0. mrsd 없으면 `SKIPPED` | FIH 계열이면 `mrsd.json` 필수 — 없으면 `FAIL` |
| 4 | `advisory` | `doc_lint.lint_file()` warnings 전체 (D5) | 발견돼도 `PASS`(표시) | warning ≥ 1 → `FAIL` |
| 5 | `approval` | — | `NOT_IMPLEMENTED` | `NOT_IMPLEMENTED` |

`score`는 차원이 아니다. 출력에 `score N/100 (참고, 판정 미사용)`으로만 표기한다.

### 6.1 차원 3의 시험유형 판별

`goal_spec.json`의 `trial_type`을 읽는다. 이 필드는 스키마상 **required**이다
(`.claude/references/schemas/trial_goal_spec.schema.json`, `required: [schema, drug,
trial_type, primary_objective]`).

| goal_spec 상태 | draft | submission |
|---------------|-------|-----------|
| 있음 + `trial_type` ∈ {FIH, SAD, MAD} | mrsd 있으면 검사, 없으면 `SKIPPED` | mrsd 없으면 `FAIL` |
| 있음 + 그 외 유형 | `SKIPPED` | `SKIPPED` |
| 없음 | `SKIPPED` | `FAIL` — 시험유형 확인 불가 시 제출 판정 불가 |

`trial_type` 매칭은 대소문자 무시 + **단어 경계** 정규식으로 한다
(`\b(FIH|SAD|MAD)\b`, `re.IGNORECASE`). 스키마가 `type: string` 자유 서술을 허용하므로
`"FIH (SAD/MAD 포함)"` 같은 값이 올 수 있어 부분 일치가 필요하지만, 단어 경계 없이
부분 문자열로 매칭하면 다른 단어 안의 `SAD`/`MAD`를 오탐할 수 있다.

---

## 7. 오류 처리 및 종료코드

| 상황 | 처리 | 종료코드 |
|------|------|---------|
| 대상 파일 없음 | 즉시 중단, 차원 실행 안 함 | 2 |
| `--profile` 인자 오류 | 즉시 중단 | 2 |
| 검사기 예외 발생 | 해당 차원 `ERROR`, 나머지 차원은 계속 실행 | 2 |
| 리포트 쓰기 실패 | 중단 — 증거를 남기지 못하면 통과를 주장하지 않는다 | 2 |
| 차원 ≥ 1개 `FAIL` | 전 차원 실행 후 집계 | 1 |
| 전부 통과 | | 0 |

종료코드 의미:

- `0` = 통과
- `1` = **판정했고 불합격** → 문서를 수정해야 함
- `2` = **판정 불가** → 게이트 또는 입력을 수정해야 함

**우선순위**: `ERROR`와 `FAIL`이 동시에 존재하면 **exit 2가 우선**한다. 검사기 하나가
깨진 상태에서는 나머지 차원의 `FAIL`이 완전한 목록이라고 주장할 수 없으므로, "불합격
항목은 이것뿐"이라는 잘못된 신호를 주지 않기 위해 "판정 불가"로 보고한다.

검사기 크래시를 `2`로 두는 이유: 검사기가 깨진 상태는 "문서가 나쁘다"가 아니라
"판단할 수 없다"이다. 둘을 같은 코드로 합치면 엉뚱한 문서 수정을 유발한다.

---

## 8. 산출물 — `_workspace/verification/release_gate.json`

```json
{
  "schema": "release_gate/v1",
  "generated_utc": "2026-07-30T01:23:45Z",
  "target": "_workspace/03_protocol_draft.md",
  "doc_type": "protocol",
  "profile": "submission",
  "trial_type": "DDI",
  "result": "FAIL",
  "exit_code": 1,
  "score_informational": 88,
  "dimensions": [
    {
      "id": "structure",
      "status": "PASS",
      "findings": []
    },
    {
      "id": "citation",
      "status": "FAIL",
      "findings": ["PMID 99999999: not_found"],
      "detail": {"format_fail": 0, "not_found": 1, "unverified_network": 0}
    },
    {
      "id": "dose",
      "status": "SKIPPED",
      "findings": [],
      "reason": "trial_type=DDI (non-FIH)"
    },
    {
      "id": "advisory",
      "status": "FAIL",
      "findings": ["unresolved placeholder marker: 'TODO'"]
    },
    {
      "id": "approval",
      "status": "NOT_IMPLEMENTED",
      "findings": [],
      "reason": "서명 이벤트 스토어 미구현 (P0-5)"
    }
  ],
  "warnings": [
    "approval 차원 미구현 — 이 결과는 '제출 가능'을 의미하지 않음"
  ]
}
```

`schema` 필드를 둔 이유는 기존 `citation_audit/v1`,
`pipeline_manifest` 스키마 관례와 일치시키기 위함이다.

---

## 9. `finalize.md` 축소

`.claude/commands/finalize.md`는 판정 로직을 보유하지 않고, 실행 파일을 호출하고 결과를
사용자에게 보고하는 얇은 래퍼로 축소한다.

- 유지: 대상 결정 규칙(인자에 `icf` 포함 여부), 사용자 보고 형식, Gotchas
- 제거: Step 2의 개별 검사기 bash 호출, Step 3의 판정 표(→ 실행 파일로 이전)
- 추가: `--profile` 사용 안내 (작성 중=draft, 제출 직전=submission)

에이전트가 "통과했다"고 보고한 텍스트는 판정 입력으로 사용하지 않는다. 판정은 종료코드와
`release_gate.json`만으로 이루어진다.

---

## 10. 테스트 계획

위치: `.claude/scripts/tests/test_finalize_run.py`
fixture: `.claude/scripts/tests/fixtures/gate/`

기존 `conftest.py`가 `.claude/scripts/qa/`를 `sys.path`에 추가하므로
`import finalize_run`이 바로 가능하다.

**네트워크 금지**: 기존 `test_citation_verify.py`의 규약("NO test performs network I/O")을
따른다. submission 프로파일 테스트는 `citation_verify.verify_online`을 monkeypatch한다.

| # | fixture | 잡는 차원 | draft | submission |
|---|---------|----------|-------|-----------|
| 1 | 존재하지 않는 PMID (`verify_online` mock → `not_found=1`) | 2 | `FORMAT_ONLY` → exit 0 | exit 1 |
| 2 | `[출처 미확인]` 잔존 | 4 | 표시 → exit 0 | exit 1 |
| 3 | PIPA 내용 없는 ICF | 4 | 표시 → exit 0 | exit 1 |
| 4 | PG 언급 + Part 4 없는 ICF | 4 | 표시 → exit 0 | exit 1 |
| 5 | `trial_type=FIH` + `mrsd.json` 없음 | 3 | `SKIPPED` → exit 0 | exit 1 |
| 6 | B.7 섹션 누락 | 1 | exit 1 | exit 1 |
| ＋ | v2 golden fixture (양성 대조) | 전부 | exit 0 | exit 0 (online mock=verified) |
| ＋ | 검사기 예외 주입 (음성 대조) | — | exit 2 | exit 2 |

### 10.1 fixture 구성 제약 — 단일 결함 원칙

각 fixture는 **의도한 차원 하나만** 위반해야 한다. 다른 차원까지 동시에 위반하면
§11의 수용 기준 2(draft에서 6번만 exit ≠ 0)가 성립하지 않아, 프로파일 분리가
검증되지 않는다.

구체적으로 fixture 1~5는 다음을 모두 만족해야 한다.

- B.1~B.16 섹션이 모두 존재 (차원 1을 건드리지 않기 위해)
- 보존기간을 `3년`으로 쓰지 않음 — `_retention_errors`는 `보존/보유/보관 기간` 줄에
  `3년`이 있고 `15년`이 없을 때만 error를 내므로, 해당 문장을 아예 생략하거나 `15년`으로
  쓰면 된다 (`doc_lint.py` `_retention_errors` 확인)
- 의도한 결함 외의 placeholder·미확인 인용 마커가 없음 (차원 4 오염 방지)
- **fixture의 설명용 제목·주석이 그 결함의 검사 정규식에 걸리지 않음** — 결함을 설명하려고
  쓴 단어가 검사식에 매칭되면 fixture가 스스로 검사를 통과시킨다(자기 무력화).

fixture 6(B.7 누락)만 예외로 차원 1을 의도적으로 위반하며, 그 외 차원은 깨끗해야 한다.

#### 자기 무력화 함정 (실측 사례)

`icf_pg_without_part4.md`의 초안 제목을 `— PG 언급, 선택동의 없음`으로 썼더니 의도한
경고가 **0건** 나왔다. `lint_icf`의 검사식이

```python
if re.search(r"유전체|약물유전|대사체|인체유래물|잔여\s*검체", text):
    if not re.search(r"Part\s*4|선택\s*동의|별도\s*동의", text):
        warnings.append(...)
```

처럼 **문서 전체**를 훑고, `선택\s*동의`가 공백 없는 `선택동의`에도 매칭하기 때문이다.
즉 "선택 동의 절이 없다"를 보여주려는 fixture가 제목에 그 단어를 담아 검사를 통과시켰다.
`Part 4`도 같은 이유로 제목에 쓸 수 없다. 검증된 제목은 `— 약물유전체 언급, 추가 동의 절 부재`다.

**절차적 방어**: fixture를 만든 직후 `doc_lint.py <fixture>`를 실행해 **의도한 findings가
정확히 그 개수만** 나오는지 확인한다. fixture 내용을 눈으로 읽는 것으로는 이 함정을 잡을 수 없다.

추가 테스트:

- 대상 파일 없음 → exit 2
- `--profile bogus` → exit 2
- 리포트 경로 쓰기 불가(읽기 전용 디렉터리) → exit 2
- `release_gate.json`이 `schema: release_gate/v1`을 포함하고 차원 5개를 모두 기록

---

## 11. 수용 기준 (기계적 검증)

1. **fixture 6종이 submission 프로파일에서 전부 exit ≠ 0.**
2. **fixture 중 6번만 draft 프로파일에서 exit ≠ 0** (1~5번은 exit 0).
   이 비대칭 자체가 프로파일 분리의 검증이다 — draft에서 1~5번이 막히면 프로파일 분리가
   고장난 것이고, submission에서 하나라도 통과하면 게이트가 고장난 것이다.
3. **검사기 예외 주입 시 exit 2** (통과로 집계되지 않음).
4. **v2 golden fixture는 draft에서 exit 0** (기존 산출물 회귀 없음).
5. `.github/scripts/validate_manifests.py` exit 0 (plugin 동기화 불변식 유지).
6. 기존 pytest 전량 통과 (검사기 미변경이므로 회귀 없어야 함).
7. `release_gate.json`이 생성되고 차원 5개 + `NOT_IMPLEMENTED` 경고를 포함.

---

## 12. 변경 파일 목록

| 파일 | 변경 |
|------|------|
| `.claude/scripts/qa/finalize_run.py` | 신규 |
| `.claude/scripts/tests/test_finalize_run.py` | 신규 |
| `.claude/scripts/tests/fixtures/gate/*` | 신규 (fixture 6종 + goal_spec 변형) |
| `.claude/commands/finalize.md` | 래퍼로 축소 (§9) |
| `plugin/clinical-pharmacology-study-protocol-development/**` | `./sync_plugin.sh` 실행 결과 |

`doc_lint.py`, `citation_verify.py`, `dose_safety_guard.py`, `draft_advisory_hook.py`,
`.github/workflows/ci.yml`은 **변경하지 않는다**.

---

## 13. 후속 (이 설계가 그릇을 제공하는 항목)

- **P0-3** claim–evidence graph → 차원 추가
- **P0-4** typed `TrialSpec` → 차원 3의 시험유형 판별을 `goal_spec` 대신 `TrialSpec`에서
- **P0-5** 서명 이벤트 스토어 → 차원 5의 `NOT_IMPLEMENTED`를 실제 판정으로 교체
- **P1-1** `science_lint` 룰팩 → 차원 추가
- **P0-6** 제품 상태 머신 → `release_gate.json`의 `result`를 문서 상태로 승격

차원 추가가 표 한 줄로 끝나도록 설계한 이유가 여기에 있다.

---

## 14. 참고

- 협의체 원문: `.xllm/artifacts/ask/codex-cwd-*.md`, `.xllm/artifacts/ask/grok-cwd-*.md`
- 협의체 요약: `.xllm/artifacts/xllm/council-*.md`
- 기존 패턴 근거: `.claude/hooks/draft_advisory_hook.py:73-96`
- 검사기 API: `.claude/scripts/qa/{doc_lint,citation_verify,dose_safety_guard}.py`
- 동기화 규약: `sync_plugin.sh`, `.github/scripts/validate_manifests.py`
