# Clinical Pharmacology Study Protocol Development — Plugin Design

프로젝트 레벨 하네스를 Claude Code 플러그인으로 전환하는 설계 문서.

## 결정 사항

| 항목 | 결정 |
|------|------|
| 범위 | 임상약리(Phase 1) 전용 |
| 사용자 | 사내 소규모 팀 |
| 접근 방식 | Approach C — 플러그인 + 기존 MCP + WebFetch 확장 |
| 데이터 소스 확장 | OpenFDA, DailyMed, MFDS를 WebFetch로 시작, 향후 MCP 전환 |

## 1. 플러그인 구조

```
clinical-pharmacology-study-protocol-development/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── researcher.md
│   ├── protocol-writer.md
│   ├── icf-writer.md
│   └── qa-reviewer.md
├── skills/
│   ├── trial-doc-orchestrator/
│   │   └── SKILL.md
│   ├── clinical-research/
│   │   └── SKILL.md
│   ├── protocol-drafting/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── protocol-template.md
│   ├── icf-drafting/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── icf-template.md
│   └── regulatory-review/
│       └── SKILL.md
├── .mcp.json
└── scripts/
```

## 2. plugin.json

```json
{
  "name": "clinical-pharmacology-study-protocol-development",
  "version": "1.0.0",
  "description": "임상약리(Phase 1) 임상시험 문서 개발 플러그인. 계획서, 동의설명서, 동의서를 자동 생성하고 QA 검토한다.",
  "author": { "name": "Min-Gul Kim" },
  "repository": "https://github.com/kimmingul/clinical-pharmacology-study-protocol-development",
  "keywords": ["clinical-trial", "protocol", "icf", "phase1", "clinical-pharmacology"]
}
```

## 3. .mcp.json

```json
{
  "mcpServers": {
    "Clinical Trials": {
      "type": "url",
      "url": "https://mcp.anthropic.com/Clinical_Trials"
    },
    "PubMed": {
      "type": "url",
      "url": "https://mcp.anthropic.com/PubMed"
    },
    "ICD-10 Codes": {
      "type": "url",
      "url": "https://mcp.anthropic.com/ICD-10_Codes"
    }
  }
}
```

향후 커스텀 MCP 서버(OpenFDA, DailyMed, MFDS)는 `scripts/mcp-servers/`에 구현 후 여기에 추가.

## 4. 에이전트 구성

| 에이전트 | model | 역할 |
|---------|-------|------|
| researcher | sonnet | IB 분석 + MCP + WebFetch(FDA/DailyMed/MFDS) 배경 조사 |
| protocol-writer | opus | ICH E6(R3) Annex 1 기반 계획서 작성 |
| icf-writer | opus | 동의설명서/동의서/개인정보 동의서 작성 (PIPA, 생명윤리법) |
| qa-reviewer | opus | 규제 준수, 문서 간 일관성, 과학적 타당성 검토 |

모든 에이전트는 `general-purpose` 타입으로 호출. 에이전트 정의와 스킬은 서브 에이전트가 `${CLAUDE_PLUGIN_ROOT}/` 경로에서 Read로 로드.

## 5. 경로 체계

| 구분 | 경로 참조 |
|------|----------|
| 플러그인 코드 (에이전트, 스킬, 템플릿) | `${CLAUDE_PLUGIN_ROOT}/agents/...`, `${CLAUDE_PLUGIN_ROOT}/skills/...` |
| 프로젝트 산출물 (_workspace) | `_workspace/...` (프로젝트 루트 기준 상대 경로) |

## 6. 데이터 소스 확장

### 현재 (MCP)
- ClinicalTrials.gov — 유사 시험 검색, 엔드포인트 분석
- PubMed — 문헌 조사, PK/PD 데이터
- ICD-10 — 적응증 코딩

### 추가 (WebFetch 기반, 향후 MCP 전환)
- **OpenFDA** (`api.fda.gov/drug/label.json`) — 승인약 라벨에서 PK/안전성 추출
- **DailyMed** (`dailymed.nlm.nih.gov/dailymed/services`) — 상세 약물 라벨링, DDI
- **MFDS 의약품안전나라** (`nedrug.mfds.go.kr`) — 국내 허가 약물 정보

clinical-research 스킬에 Step 5(승인 약물 라벨 조사)로 추가. WebFetch로 각 API를 직접 호출.

### MCP 전환 경로
1. `scripts/mcp-servers/openfda-server.mjs` 구현
2. `.mcp.json`에 등록
3. 스킬에서 WebFetch → MCP 도구 호출로 교체
4. 에이전트 프롬프트 변경 불필요 (스킬이 추상화)

## 7. 오케스트레이터 워크플로우

변경 없음. E2E 테스트를 통과한 파이프라인 유지:

```
[메인 에이전트: 정보 수집]
  → [researcher/sonnet] → 배경 조사
  → [protocol-writer/opus] → 계획서
  → [icf-writer/opus] → 동의설명서
  → [qa-reviewer/opus] → QA 검토
  → (Critical 시) 자동 1회 수정
```

## 8. 프로젝트별 커스터마이징

팀에서 반복 사용 시, 프로젝트의 `CLAUDE.md`에 기본값을 설정:

```markdown
## 기본 설정
- 의뢰자: 테스트제약 주식회사
- 시험기관: OO대학교병원 임상약리학과
- 시험책임자: OOO
- IB 위치: docs/ib/
```

## 9. 설치 및 사용

```bash
# 설치
claude plugin add github:kimmingul/clinical-pharmacology-study-protocol-development

# 사용 (어떤 프로젝트에서든)
> "XYZ-0042의 Phase 1 SAD 시험 문서를 작성해줘.
   적응증: 제2형 당뇨병, DPP-4 억제제, 경구 정제."

# 업데이트
claude plugin update clinical-pharmacology-study-protocol-development
```

## 10. 구현 작업 목록

1. 플러그인 디렉토리 생성 + `plugin.json`, `.mcp.json`
2. 기존 하네스 파일 복사 + 경로 `${CLAUDE_PLUGIN_ROOT}` 전환
3. clinical-research 스킬에 FDA/DailyMed/MFDS WebFetch 조사 Step 추가
4. researcher 에이전트에 WebFetch 데이터 소스 활용 지시 추가
5. Git 저장소 초기화 + GitHub 푸시
6. E2E 테스트 (플러그인 설치 → 문서 생성 → QA 검토)
