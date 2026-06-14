# 확장 가이드 (Extension Guide)

이 하네스를 확장할 때 **여러 파일을 손으로 동기화**해야 하는 지점을 한곳에 정리한다.
누락 시 Phase 9 리뷰나 CI(`.github/workflows/ci.yml`)에서 정합성 오류로 드러난다.
작업 후 반드시 마지막 **검증 체크리스트**를 실행한다.

---

## A. 새 시험 유형 추가 (예: "Pediatric PK", "Hepatic Impairment")

새 시험 유형 `X`를 추가하려면 다음 파일의 표/목록을 함께 갱신한다.

| # | 파일 | 갱신 내용 |
|---|------|----------|
| 1 | `.claude/skills/clinical-research/SKILL.md` | "시험 유형별 오믹스/PD 우선순위" 표에 `X` 행 추가 (translational-scientist 참여/우선순위) |
| 2 | `.claude/commands/research.md` | TS 참여 매트릭스(39~51줄 표)에 `X` 행 추가 |
| 3 | `.claude/commands/design.md` | "연구설계 옵션(시험 유형별)" 표 + "유효성/PD 평가 항목" 표에 `X` 행 추가 |
| 4 | `.claude/commands/synopsis.md` | 시험유형별 섹션 적용표에 `X` 행 추가 |
| 5 | `.claude/agents/regulatory-expert.md` | "시험 유형별 조사 초점" 표에 `X` 행 (MFDS/FDA·EMA 가이드라인, 라벨 초점) |
| 6 | `.claude/agents/clinician.md` | 시험 유형별 안전성 고려가 다르면 반영 (clinician은 항상 참여) |
| 7 | `.claude/agents/clinical-pharmacologist.md`, `.claude/agents/translational-scientist.md` | 해당 PK/PD·오믹스 초점 추가 |
| 8 | `.claude/references/guidelines/index.md` + `by_study_type/` | 해당 cross-agency 비교표가 있으면 추가/링크 |
| 9 | `CLAUDE.md`, `README.md` | "시험 유형" 목록 + (진화 로그/CHANGELOG) 갱신 |

> **clinician은 항상 참여**, **translational-scientist는 BE/FE만 불참**이라는 기존 정책과
> 모순되지 않게 작성한다(이 두 규칙이 여러 파일에 반복되므로 일관성 유지가 핵심).

---

## B. 새 표본수/설계 스크립트 추가

1. `.claude/scripts/sample_size/<design>.py` 작성 — 기존 패턴을 따른다:
   - `from utils.power_analysis import ...` (공용 헬퍼: `normal_quantile`, `t_quantile`,
     `adjust_for_dropout`, `tost_power_2x2`, `solve_n_2x2_tost`, `print_result`)
   - `calculate_sample_size(...) -> dict` + `if __name__ == "__main__":` 예시
   - docstring에 **방법론 출처**(가이드라인/논문)와, 검증 전이면 "**규제 제출용 아님**" 경고
2. `.claude/scripts/tests/test_<design>.py` 추가 — 결과를 **독립 참조값**(PowerTOST,
   FDA 가이던스 예제, 또는 문서화된 시뮬레이션)과 대조하는 테스트를 반드시 포함
3. `.claude/commands/design.md`의 설계 옵션 표 + `.claude/agents/biostatistician.md`에 등록
4. 새 의존성이 있으면 `.claude/scripts/requirements.txt`에 추가
5. `python -m pytest tests/ -q` 통과 확인

> 규제 계산 코드는 **테스트 없이 추가 금지**. 회귀를 막는 참조값 테스트가 단일 안전장치다.

---

## C. 새 에이전트 추가

1. `.claude/agents/<name>.md` — frontmatter(`name`, `description`) + 역할·원칙·입출력 프로토콜
2. `.claude/skills/trial-doc-orchestrator/SKILL.md` — 에이전트 구성 표 + 해당 Phase 호출 블록
3. `CLAUDE.md`의 에이전트 팀 표 + `README.md`의 에이전트 표/개수
4. 호출하는 command(`.claude/commands/*.md`)에 Agent 호출 추가
5. `general-purpose` 타입으로 호출(커스텀 subagent_type 미지원) — 에이전트 정의를 Read로 로드

---

## D. 새 Web API 레시피 추가

1. `.claude/references/api_reference/<name>.md` — 기본정보(Base/인증/Rate Limit/**라이선스**) +
   엔드포인트 + WebFetch 레시피 + Gotchas + **실패 처리/폴백**
2. 소유 에이전트(`.claude/agents/regulatory-expert.md` 또는
   `.claude/agents/translational-scientist.md`)의 "Web API" 절차에 연결
3. 비밀 키가 필요하면 `.env.example`에 추가하고 `SECURITY.md` 정책을 따른다(절대 커밋 금지)

---

## 검증 체크리스트 (확장 후 필수)

```bash
# 1) 통계/도구 테스트
cd .claude/scripts && python -m pytest tests/ -q && cd -

# 2) 하네스 정합성 — 내부 참조·매니페스트
python3 .github/scripts/check_internal_refs.py        # 하네스 내부 .md/.py 참조가 실존하는지
python3 .github/scripts/validate_manifests.py         # 매니페스트 + sync 불변식

# 3) 출력 품질 린터(골든 픽스처)
python3 .claude/scripts/qa/doc_lint.py e2e/v2_2026_04_14_DDI/_workspace/03_protocol_draft.md --strict

# 4) 배포본 동기화 + 검증
./sync_plugin.sh
claude plugin validate plugin/clinical-pharmacology-study-protocol-development
claude plugin validate .
```

CI가 동일 검사를 PR마다 자동 수행한다. 로컬에서 위가 모두 green이면 PR을 연다.
재현성을 위해 파이프라인 실행 시 `.claude/scripts/qa/pipeline_manifest.py`로 단계별 provenance를 기록한다.
