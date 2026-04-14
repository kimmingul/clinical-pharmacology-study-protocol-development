# Plugin Conversion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 프로젝트 레벨 하네스를 `clinical-pharmacology-study-protocol-development` Claude Code 플러그인으로 전환하고, FDA/DailyMed/MFDS WebFetch 데이터 소스를 추가한다.

**Architecture:** 기존 `.claude/` 하위 파일(agents 4개, skills 5개, references 2개)을 플러그인 디렉토리로 이동. 모든 `.claude/` 경로를 `${CLAUDE_PLUGIN_ROOT}/`로 전환. clinical-research 스킬에 WebFetch 기반 Step 5 추가.

**Tech Stack:** Claude Code Plugin System, MCP (claude.ai remote), WebFetch (OpenFDA, DailyMed, MFDS API)

**Spec:** `docs/superpowers/specs/2026-04-06-plugin-conversion-design.md`

---

### Task 1: 플러그인 디렉토리 스캐폴딩

**Files:**
- Create: `clinical-pharmacology-study-protocol-development/.claude-plugin/plugin.json`
- Create: `clinical-pharmacology-study-protocol-development/.mcp.json`
- Create: `clinical-pharmacology-study-protocol-development/scripts/.gitkeep`

- [ ] **Step 1: 플러그인 루트 디렉토리 및 하위 구조 생성**

```bash
mkdir -p clinical-pharmacology-study-protocol-development/.claude-plugin
mkdir -p clinical-pharmacology-study-protocol-development/agents
mkdir -p clinical-pharmacology-study-protocol-development/skills
mkdir -p clinical-pharmacology-study-protocol-development/scripts
```

- [ ] **Step 2: plugin.json 작성**

`clinical-pharmacology-study-protocol-development/.claude-plugin/plugin.json`:
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

- [ ] **Step 3: .mcp.json 작성**

`clinical-pharmacology-study-protocol-development/.mcp.json`:
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

- [ ] **Step 4: scripts/.gitkeep 생성**

```bash
touch clinical-pharmacology-study-protocol-development/scripts/.gitkeep
```

- [ ] **Step 5: 구조 확인**

```bash
find clinical-pharmacology-study-protocol-development -type f | sort
```

Expected:
```
clinical-pharmacology-study-protocol-development/.claude-plugin/plugin.json
clinical-pharmacology-study-protocol-development/.mcp.json
clinical-pharmacology-study-protocol-development/scripts/.gitkeep
```

- [ ] **Step 6: Commit**

```bash
cd clinical-pharmacology-study-protocol-development
git init
git add -A
git commit -m "chore: scaffold plugin directory structure"
```

---

### Task 2: 에이전트 정의 마이그레이션 (경로 전환)

**Files:**
- Create: `clinical-pharmacology-study-protocol-development/agents/researcher.md`
- Create: `clinical-pharmacology-study-protocol-development/agents/protocol-writer.md`
- Create: `clinical-pharmacology-study-protocol-development/agents/icf-writer.md`
- Create: `clinical-pharmacology-study-protocol-development/agents/qa-reviewer.md`
- Source: `.claude/agents/*.md` (현재 프로젝트)

각 파일을 복사하되, `.claude/` 경로를 `${CLAUDE_PLUGIN_ROOT}/`로 치환한다.

- [ ] **Step 1: researcher.md 복사 및 경로 전환**

`.claude/agents/researcher.md`를 복사. 18행의 경로를 변경:

변경 전: `.claude/skills/clinical-research/SKILL.md`를 Read로 읽어
변경 후: `${CLAUDE_PLUGIN_ROOT}/skills/clinical-research/SKILL.md`를 Read로 읽어

- [ ] **Step 2: protocol-writer.md 복사 및 경로 전환**

`.claude/agents/protocol-writer.md`를 복사. 17행의 경로 2개를 변경:

변경 전: `.claude/skills/protocol-drafting/SKILL.md`
변경 후: `${CLAUDE_PLUGIN_ROOT}/skills/protocol-drafting/SKILL.md`

변경 전: `.claude/skills/protocol-drafting/references/protocol-template.md`
변경 후: `${CLAUDE_PLUGIN_ROOT}/skills/protocol-drafting/references/protocol-template.md`

- [ ] **Step 3: icf-writer.md 복사 및 경로 전환**

`.claude/agents/icf-writer.md`를 복사. 18행의 경로 2개를 변경:

변경 전: `.claude/skills/icf-drafting/SKILL.md`
변경 후: `${CLAUDE_PLUGIN_ROOT}/skills/icf-drafting/SKILL.md`

변경 전: `.claude/skills/icf-drafting/references/icf-template.md`
변경 후: `${CLAUDE_PLUGIN_ROOT}/skills/icf-drafting/references/icf-template.md`

- [ ] **Step 4: qa-reviewer.md 복사 및 경로 전환**

`.claude/agents/qa-reviewer.md`를 복사. 17행의 경로를 변경:

변경 전: `.claude/skills/regulatory-review/SKILL.md`
변경 후: `${CLAUDE_PLUGIN_ROOT}/skills/regulatory-review/SKILL.md`

- [ ] **Step 5: 경로 전환 검증**

```bash
grep -rn "\.claude/" clinical-pharmacology-study-protocol-development/agents/
```

Expected: 0 matches (모든 `.claude/` 경로가 `${CLAUDE_PLUGIN_ROOT}/`로 전환됨)

- [ ] **Step 6: Commit**

```bash
cd clinical-pharmacology-study-protocol-development
git add agents/
git commit -m "feat: migrate agent definitions with plugin path references"
```

---

### Task 3: 스킬 마이그레이션 (경로 전환)

**Files:**
- Create: `clinical-pharmacology-study-protocol-development/skills/clinical-research/SKILL.md`
- Create: `clinical-pharmacology-study-protocol-development/skills/protocol-drafting/SKILL.md`
- Create: `clinical-pharmacology-study-protocol-development/skills/protocol-drafting/references/protocol-template.md`
- Create: `clinical-pharmacology-study-protocol-development/skills/icf-drafting/SKILL.md`
- Create: `clinical-pharmacology-study-protocol-development/skills/icf-drafting/references/icf-template.md`
- Create: `clinical-pharmacology-study-protocol-development/skills/regulatory-review/SKILL.md`
- Source: `.claude/skills/` (현재 프로젝트)

- [ ] **Step 1: clinical-research 스킬 복사**

`.claude/skills/clinical-research/SKILL.md`를 복사. 이 파일에는 `.claude/` 경로 참조가 없으므로 변경 불필요.

- [ ] **Step 2: protocol-drafting 스킬 복사 및 경로 전환**

`.claude/skills/protocol-drafting/SKILL.md`를 복사. 32행의 경로를 변경:

변경 전: `.claude/skills/protocol-drafting/references/protocol-template.md`
변경 후: `${CLAUDE_PLUGIN_ROOT}/skills/protocol-drafting/references/protocol-template.md`

`.claude/skills/protocol-drafting/references/protocol-template.md`를 그대로 복사 (변경 없음).

- [ ] **Step 3: icf-drafting 스킬 복사 및 경로 전환**

`.claude/skills/icf-drafting/SKILL.md`를 복사. 22행의 경로를 변경:

변경 전: `.claude/skills/icf-drafting/references/icf-template.md`
변경 후: `${CLAUDE_PLUGIN_ROOT}/skills/icf-drafting/references/icf-template.md`

`.claude/skills/icf-drafting/references/icf-template.md`를 그대로 복사 (변경 없음).

- [ ] **Step 4: regulatory-review 스킬 복사**

`.claude/skills/regulatory-review/SKILL.md`를 복사. `.claude/` 경로 참조 없으므로 변경 불필요.

- [ ] **Step 5: 경로 전환 검증**

```bash
grep -rn "\.claude/" clinical-pharmacology-study-protocol-development/skills/
```

Expected: 0 matches

- [ ] **Step 6: Commit**

```bash
cd clinical-pharmacology-study-protocol-development
git add skills/
git commit -m "feat: migrate skills with plugin path references"
```

---

### Task 4: 오케스트레이터 마이그레이션 (경로 전환)

**Files:**
- Create: `clinical-pharmacology-study-protocol-development/skills/trial-doc-orchestrator/SKILL.md`
- Source: `.claude/skills/trial-doc-orchestrator/SKILL.md`

오케스트레이터는 가장 많은 경로 참조(16개)를 포함. 모든 `.claude/` → `${CLAUDE_PLUGIN_ROOT}/`로 전환.

- [ ] **Step 1: 오케스트레이터 복사 및 경로 전환**

`.claude/skills/trial-doc-orchestrator/SKILL.md`를 복사. 다음 경로들을 모두 전환:

| 행 | 변경 전 | 변경 후 |
|----|---------|---------|
| 37 | `.claude/agents/*.md` | `${CLAUDE_PLUGIN_ROOT}/agents/*.md` |
| 88 | `.claude/agents/researcher.md` | `${CLAUDE_PLUGIN_ROOT}/agents/researcher.md` |
| 89 | `.claude/skills/clinical-research/SKILL.md` | `${CLAUDE_PLUGIN_ROOT}/skills/clinical-research/SKILL.md` |
| 114 | `.claude/agents/protocol-writer.md` | `${CLAUDE_PLUGIN_ROOT}/agents/protocol-writer.md` |
| 115 | `.claude/skills/protocol-drafting/SKILL.md` | `${CLAUDE_PLUGIN_ROOT}/skills/protocol-drafting/SKILL.md` |
| 116 | `.claude/skills/protocol-drafting/references/protocol-template.md` | `${CLAUDE_PLUGIN_ROOT}/skills/protocol-drafting/references/protocol-template.md` |
| 142 | `.claude/agents/icf-writer.md` | `${CLAUDE_PLUGIN_ROOT}/agents/icf-writer.md` |
| 143 | `.claude/skills/icf-drafting/SKILL.md` | `${CLAUDE_PLUGIN_ROOT}/skills/icf-drafting/SKILL.md` |
| 144 | `.claude/skills/icf-drafting/references/icf-template.md` | `${CLAUDE_PLUGIN_ROOT}/skills/icf-drafting/references/icf-template.md` |
| 163 | `.claude/agents/qa-reviewer.md` | `${CLAUDE_PLUGIN_ROOT}/agents/qa-reviewer.md` |
| 164 | `.claude/skills/regulatory-review/SKILL.md` | `${CLAUDE_PLUGIN_ROOT}/skills/regulatory-review/SKILL.md` |

- [ ] **Step 2: 산출물 경로 확인 (변경 없음)**

`_workspace/` 경로는 프로젝트 루트 기준 상대 경로이므로 변경하지 않는다. 확인:

```bash
grep "_workspace/" clinical-pharmacology-study-protocol-development/skills/trial-doc-orchestrator/SKILL.md | head -5
```

Expected: `_workspace/` 경로 유지 (변환 없음)

- [ ] **Step 3: 전체 경로 전환 최종 검증**

```bash
grep -rn "\.claude/" clinical-pharmacology-study-protocol-development/
```

Expected: 0 matches (플러그인 전체에서 `.claude/` 경로 없음)

- [ ] **Step 4: Commit**

```bash
cd clinical-pharmacology-study-protocol-development
git add skills/trial-doc-orchestrator/
git commit -m "feat: migrate orchestrator with plugin path references"
```

---

### Task 5: clinical-research 스킬에 WebFetch 데이터 소스 추가

**Files:**
- Modify: `clinical-pharmacology-study-protocol-development/skills/clinical-research/SKILL.md`
- Modify: `clinical-pharmacology-study-protocol-development/agents/researcher.md`

기존 Step 0~4 뒤에 **Step 5: 승인 약물 라벨 조사 (WebFetch)**를 추가한다.

- [ ] **Step 1: clinical-research SKILL.md에 Step 5 추가**

`SKILL.md`의 `## 품질 기준` 섹션 앞에 다음을 삽입:

```markdown
### Step 5: 승인 약물 라벨 조사 (WebFetch)

동일 계열 승인 약물의 라벨에서 PK/안전성 정보를 추출한다. WebFetch 도구로 공개 API를 직접 호출한다.

#### 5-1. OpenFDA — 약물 라벨 검색

```
WebFetch(url="https://api.fda.gov/drug/label.json?search=indications_and_usage:{적응증}+AND+active_ingredient:{약물 계열 대표 약물}&limit=5")
```

추출 항목:
- `clinical_pharmacology` 섹션: PK 파라미터 (Cmax, AUC, t½, 대사 경로)
- `adverse_reactions` 섹션: 이상반응 빈도
- `drug_interactions` 섹션: CYP 상호작용 정보
- `dosage_and_administration` 섹션: 승인 용량 범위

#### 5-2. DailyMed — 상세 약물 라벨링

```
WebFetch(url="https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={약물명}&pagesize=5")
```

SPL ID를 획득한 뒤 상세 라벨 조회:
```
WebFetch(url="https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{SPL_ID}.json")
```

추출 항목:
- 약물 상호작용 상세 (CYP 기질/억제/유도 여부)
- 특수 집단 PK (간/신기능 장애, 고령자)
- 금기 사항

#### 5-3. MFDS 의약품안전나라 — 국내 허가 정보

```
WebFetch(url="https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?openDataInfoSeq={품목코드}")
```

또는 품목명으로 검색:
```
WebFetch(url="https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemList?typeName=품목명&searchKey={약물명}")
```

추출 항목:
- 국내 허가 여부 및 적응증
- 국내 첨부문서의 용법/용량
- 국내 특이 주의사항

> API 호출 실패 시 해당 소스를 "[미수집]"으로 표시하고 나머지로 진행한다. 이 데이터 소스들은 보충 자료이며, MCP 도구(ClinicalTrials.gov, PubMed, ICD-10)가 핵심이다.
```

- [ ] **Step 2: 산출물 구조에 FDA/DailyMed/MFDS 섹션 추가**

같은 파일의 산출물 구조(`## 산출물 구조`)에서 `## 5. 규제 고려사항` 앞에 추가:

```markdown
## 5. 승인 약물 라벨 분석 (WebFetch)
### 5.1 OpenFDA — 계열 약물 PK/안전성 요약
### 5.2 DailyMed — 약물 상호작용, 특수 집단 PK
### 5.3 MFDS — 국내 허가 현황
```

기존 `## 5. 규제 고려사항`을 `## 6.`으로, `## 6. 참고 문헌`을 `## 7.`로 번호 조정.

- [ ] **Step 3: researcher.md에 WebFetch 활용 지시 추가**

`researcher.md`의 `## 핵심 역할` 섹션에 항목 추가:

```markdown
6. WebFetch로 OpenFDA, DailyMed, MFDS API를 호출하여 승인 약물의 라벨 정보 수집
```

`## MCP 도구 활용 전략` 섹션 뒤에 추가:

```markdown
## WebFetch 데이터 소스 (보충 자료)

MCP 도구로 수집한 데이터를 보충하기 위해 WebFetch로 공개 API를 호출한다.
상세 절차는 스킬 파일의 Step 5를 참조한다.

- **OpenFDA**: 동일 계열 승인약 라벨에서 PK/안전성 추출
- **DailyMed**: 상세 약물 라벨링, DDI, 특수 집단 PK
- **MFDS 의약품안전나라**: 국내 허가 약물 정보, 첨부문서
```

- [ ] **Step 4: 검증**

```bash
grep -c "WebFetch" clinical-pharmacology-study-protocol-development/skills/clinical-research/SKILL.md
grep -c "WebFetch" clinical-pharmacology-study-protocol-development/agents/researcher.md
```

Expected: SKILL.md에 6건 이상, researcher.md에 1건 이상

- [ ] **Step 5: Commit**

```bash
cd clinical-pharmacology-study-protocol-development
git add skills/clinical-research/ agents/researcher.md
git commit -m "feat: add FDA/DailyMed/MFDS WebFetch data sources to clinical-research"
```

---

### Task 6: Git 저장소 정리 및 README

**Files:**
- Create: `clinical-pharmacology-study-protocol-development/README.md`

- [ ] **Step 1: README.md 작성**

```markdown
# Clinical Pharmacology Study Protocol Development

임상약리(Phase 1) 임상시험 문서 개발 플러그인 for Claude Code.

## 기능

- **배경 조사**: ClinicalTrials.gov, PubMed, ICD-10, OpenFDA, DailyMed, MFDS 데이터 수집
- **계획서 작성**: ICH E6(R3) Annex 1 준수 임상시험 계획서 자동 생성
- **동의설명서 작성**: 시험대상자용 동의설명서/동의서/개인정보 동의서 작성
- **QA 검토**: 규제 준수, 문서 간 일관성, 과학적 타당성 자동 검토

## 설치

```bash
claude plugin add github:kimmingul/clinical-pharmacology-study-protocol-development
```

## 사용

```
임상시험 문서를 작성해줘.
- 약물: XYZ-0042
- 적응증: 제2형 당뇨병
- 시험 유형: Phase 1 SAD
- 약물 계열: DPP-4 억제제
- 제형: 경구 정제
```

## 프로젝트별 설정

`CLAUDE.md`에 기본값을 지정하면 매번 입력할 필요가 없습니다:

```markdown
## 기본 설정
- 의뢰자: OO제약 주식회사
- 시험기관: OO대학교병원 임상약리학과
- IB 위치: docs/ib/
```

## 라이선스

MIT
```

- [ ] **Step 2: .gitignore 작성**

```
.DS_Store
_workspace/
node_modules/
```

- [ ] **Step 3: Commit**

```bash
cd clinical-pharmacology-study-protocol-development
git add README.md .gitignore
git commit -m "docs: add README and gitignore"
```

---

### Task 7: 최종 검증

**Files:** 전체 플러그인 디렉토리

- [ ] **Step 1: 파일 구조 확인**

```bash
find clinical-pharmacology-study-protocol-development -type f | grep -v ".git/" | sort
```

Expected:
```
clinical-pharmacology-study-protocol-development/.claude-plugin/plugin.json
clinical-pharmacology-study-protocol-development/.gitignore
clinical-pharmacology-study-protocol-development/.mcp.json
clinical-pharmacology-study-protocol-development/README.md
clinical-pharmacology-study-protocol-development/agents/icf-writer.md
clinical-pharmacology-study-protocol-development/agents/protocol-writer.md
clinical-pharmacology-study-protocol-development/agents/qa-reviewer.md
clinical-pharmacology-study-protocol-development/agents/researcher.md
clinical-pharmacology-study-protocol-development/scripts/.gitkeep
clinical-pharmacology-study-protocol-development/skills/clinical-research/SKILL.md
clinical-pharmacology-study-protocol-development/skills/icf-drafting/SKILL.md
clinical-pharmacology-study-protocol-development/skills/icf-drafting/references/icf-template.md
clinical-pharmacology-study-protocol-development/skills/protocol-drafting/SKILL.md
clinical-pharmacology-study-protocol-development/skills/protocol-drafting/references/protocol-template.md
clinical-pharmacology-study-protocol-development/skills/regulatory-review/SKILL.md
clinical-pharmacology-study-protocol-development/skills/trial-doc-orchestrator/SKILL.md
```

- [ ] **Step 2: 경로 참조 최종 검증**

```bash
# .claude/ 경로 잔존 확인 (0건이어야 함)
grep -rn "\.claude/" clinical-pharmacology-study-protocol-development/ --include="*.md"

# ${CLAUDE_PLUGIN_ROOT} 사용 확인
grep -rn "CLAUDE_PLUGIN_ROOT" clinical-pharmacology-study-protocol-development/ --include="*.md" | wc -l
```

Expected: `.claude/` = 0건, `CLAUDE_PLUGIN_ROOT` = 16건 이상

- [ ] **Step 3: YAML frontmatter 검증**

```bash
for f in clinical-pharmacology-study-protocol-development/agents/*.md clinical-pharmacology-study-protocol-development/skills/*/SKILL.md; do
  echo "--- $(basename $f) ---"
  head -3 "$f" | tail -2
  echo ""
done
```

Expected: 모든 파일에 `name:` + `description:` frontmatter 존재

- [ ] **Step 4: SKILL.md 라인 수 확인 (<500줄)**

```bash
for f in clinical-pharmacology-study-protocol-development/skills/*/SKILL.md; do wc -l "$f"; done
```

Expected: 모든 SKILL.md가 500줄 이내

- [ ] **Step 5: plugin.json 유효성**

```bash
python3 -c "import json; json.load(open('clinical-pharmacology-study-protocol-development/.claude-plugin/plugin.json')); print('VALID')"
python3 -c "import json; json.load(open('clinical-pharmacology-study-protocol-development/.mcp.json')); print('VALID')"
```

Expected: 둘 다 `VALID`

- [ ] **Step 6: 최종 커밋 (필요 시)**

```bash
cd clinical-pharmacology-study-protocol-development
git status
# 변경 사항이 있으면:
git add -A
git commit -m "chore: final verification and cleanup"
```
