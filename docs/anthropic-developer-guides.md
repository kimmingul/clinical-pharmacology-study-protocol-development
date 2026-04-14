# Anthropic 공식 개발자 가이드 종합 정리

> Claude Code 최적 환경 설정을 위한 Anthropic 공식 리소스 맵
> 작성일: 2026-04-05 | 마지막 검증: 2026-04-05

---

## 개요

이 문서는 Anthropic 개발자/엔지니어가 직접 작성한 **실전 가이드, 엔지니어링 블로그, 공식 문서**를 주제별로 정리한 것입니다. 단순 제품 발표가 아닌, **"어떻게 만들어야 잘 작동하는가"** 에 대한 실천적 지식을 담은 글들을 우선 수집했습니다.

---

## 1. Skills (Agent Skills)

### 1.1 핵심 리소스

| # | 제목 | 저자/출처 | 유형 | URL |
|---|------|----------|------|-----|
| 1 | **Lessons from Building Claude Code: How We Use Skills** | Thariq Shihipar (Anthropic) | LinkedIn Article / X Thread | [LinkedIn](https://www.linkedin.com/pulse/lessons-from-building-claude-code-how-we-use-skills-thariq-shihipar-iclmc) / [X Thread](https://x.com/trq212/status/2033949937936085378) |
| 2 | **Equipping Agents for the Real World with Agent Skills** | Anthropic Engineering | Engineering Blog | [anthropic.com](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) |
| 3 | **Introducing Agent Skills** | Anthropic News | Product Blog | [anthropic.com](https://www.anthropic.com/news/skills) |
| 4 | **Improving skill-creator: Test, Measure, and Refine Agent Skills** | Anthropic News | Product Blog | [anthropic.com/news](https://www.anthropic.com/news) (블로그 목록에서 검색) |
| 5 | **Skills Repository (소스 코드)** | Anthropic | GitHub | [github.com/anthropics/skills](https://github.com/anthropics/skills) |
| 6 | **Agent Skills Skilljar Course** | Anthropic Academy | 온라인 코스 | Anthropic Academy 내 (Thariq가 추천) |

### 1.2 핵심 교훈 (Thariq Shihipar 글 요약)

**Skills은 "마크다운 파일"이 아니라 "폴더"다:**
- 스크립트, 에셋, 데이터, 설정 옵션(동적 hooks 등록 포함)을 포함할 수 있음
- 파일 시스템 자체가 context engineering과 progressive disclosure의 한 형태

**9가지 Skill 카테고리:**

1. **Library & API Reference** — 라이브러리, CLI, SDK 사용법 + gotchas
2. **Product Verification** — Playwright, tmux 등과 연동한 테스트/검증 (가장 투자할 가치 있음)
3. **Data & Monitoring** — 데이터/모니터링 스택 연동
4. **Workflow Automation** — 반복 작업 자동화
5. **Scaffolding & Boilerplate** — 프레임워크 보일러플레이트 생성
6. **Code Quality & Review** — 코드 품질 + 리뷰 (hooks/GitHub Actions로 자동 실행 가능)
7. **Code Deployment** — 코드 fetch, push, deploy
8. **Investigation & Triage** — Slack 스레드, 알림, 에러 시그니처 → 구조화된 리포트
9. **Operational & Maintenance** — 루틴 유지보수 및 운영 절차

**9가지 Best Practices:**

1. **Claude가 이미 아는 것과 차별화** — 기본 동작에서 벗어나는 지식에 집중
2. **Gotchas 섹션이 가장 가치 높음** — 실패 사례를 지속적으로 축적
3. **Progressive Disclosure 활용** — SKILL.md에서 다른 파일을 참조, Claude가 필요시 읽도록
4. **너무 구체적이지 않게** — Claude에게 적응할 유연성 제공
5. **폴더 구조 활용** — references/, assets/, scripts/ 등으로 맥락 분배
6. **Verification Skills에 엔지니어 1주일 투자 가치** — 비디오 녹화, 프로그래밍적 assertion 기법
7. **로그 파일로 이전 실행 결과 저장** — 일관성과 반성 기회 제공
8. **hooks와 결합** — SessionStart hook로 자동 주입, GitHub Actions로 자동 실행
9. **Skill Creator로 스킬 생성을 가속** — Claude Code 자체를 활용하여 제작

---

## 2. Plugins

### 2.1 핵심 리소스

| # | 제목 | 유형 | URL |
|---|------|------|-----|
| 1 | **Create Plugins (공식 문서)** | Developer Docs | [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins) |
| 2 | **Plugins Reference (스펙)** | Developer Docs | code.claude.com 내 Plugins reference 페이지 |
| 3 | **Customize Claude Code with Plugins** | Product Blog (2025.11) | [anthropic.com/news/claude-code-plugins](https://www.anthropic.com/news/claude-code-plugins) |
| 4 | **claude-plugins-official** | GitHub | [github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) |
| 5 | **claude-code/plugins (커뮤니티 + 공식)** | GitHub | [github.com/anthropics/claude-code/blob/main/plugins/README.md](https://github.com/anthropics/claude-code/blob/main/plugins/README.md) |

### 2.2 Plugin 구조

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json        # 메타데이터 (필수, 이 디렉토리 안에만)
├── commands/               # Slash commands (선택)
├── agents/                 # Agent 정의 (선택)
├── skills/                 # Skill 정의 (선택)
├── hooks/                  # Hook 정의 (선택)
├── .mcp.json              # MCP 서버 설정 (선택)
├── .lsp.json              # LSP 서버 설정 (선택)
├── settings.json          # 기본 설정 (선택)
└── README.md
```

**흔한 실수:** commands/, agents/, skills/, hooks/ 를 `.claude-plugin/` 디렉토리 안에 넣지 말 것. `plugin.json`만 `.claude-plugin/` 안에 위치.

---

## 3. Hooks

### 3.1 핵심 리소스

Hooks에 대한 독립 블로그 포스트는 없으나, 아래 문서들에서 상세히 다룸:

| # | 출처 | 참고 내용 |
|---|------|----------|
| 1 | **Plugins 공식 문서** | `.claude/settings.json`에 hooks 구성, `/reload-plugins`로 재로드 |
| 2 | **Plugins Reference** | PreToolUse, PostToolUse, SessionStart, Stop 등 lifecycle 이벤트 스펙 |
| 3 | **Thariq - How We Use Skills** | Skills과 hooks 결합 패턴, 동적 hooks 등록 |
| 4 | **2026.04 릴리즈 노트** | PreToolUse hooks에 "defer" 결정 추가 등 최신 기능 |

### 3.2 Hooks 핵심 개념

- **Deterministic scripts**: 모델이 아닌 결정론적 코드가 lifecycle 이벤트에서 실행
- **주요 이벤트**: PreToolUse, PostToolUse, SessionStart, Stop
- **용도 예시**:
  - 파일 편집 후 자동 포매팅
  - 커밋 전 lint 실행
  - 세션 시작 시 컨텍스트 자동 주입
  - 위험한 행동 감지/차단 (hookify 플러그인 참조)

---

## 4. Harness (Agent Harness)

### 4.1 핵심 리소스

| # | 제목 | 날짜 | URL |
|---|------|------|-----|
| 1 | **Harnessing Claude's Intelligence** | 2026.04.02 | [claude.com/blog/harnessing-claudes-intelligence](https://claude.com/blog/harnessing-claudes-intelligence) |
| 2 | **Harness Design for Long-Running Application Development** | 2026.03 | [anthropic.com/engineering/harness-design-long-running-apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) |
| 3 | **Effective Harnesses for Long-Running Agents** | 2025.11 | [anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| 4 | **Building Agents with the Claude Agent SDK** | 2026.01 | [anthropic.com/engineering/building-agents-with-the-claude-agent-sdk](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) |
| 5 | **Effective Context Engineering for AI Agents** | 2025.09 | [anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) |
| 6 | **Writing Effective Tools for AI Agents—Using Agents** | 2025-2026 | [anthropic.com/engineering/writing-tools-for-agents](https://www.anthropic.com/engineering/writing-tools-for-agents) |

### 4.2 핵심 교훈

**"Harnessing Claude's Intelligence" (2026.04.02) — 3가지 패턴:**

1. **Use what it already knows** — Claude가 이미 잘 이해하는 도구를 사용하여 구축
2. **Ask what you can stop doing** — 모델이 발전하면서 불필요해진 harness 코드 제거
3. **Carefully set boundaries with the agent harness** — harness가 인코딩하는 가정이 낡아지므로 주기적으로 재검토

> "agent harness는 Claude가 스스로 할 수 없는 것에 대한 가정을 인코딩한다. Claude가 더 유능해지면 그 가정을 테스트해야 한다."

**"Effective Harnesses" (2025.11) — 2-Agent 아키텍처:**

- **Initializer Agent**: 첫 세션에서 환경 설정 (feature list JSON, init.sh, claude-progress.txt, git 초기화)
- **Coding Agent**: 이후 세션에서 한 번에 하나의 feature를 구현, 커밋, 진행 상황 기록
- 핵심: `claude-progress.txt` + git history로 세션 간 상태 유지

**"Harness Design for Long-Running Apps" (2026.03) — 3-Agent 아키텍처:**

- **Planner**: 스펙 분해 및 작업 계획
- **Generator/Builder**: 기능 구현
- **Evaluator**: 별도 에이전트가 결과물을 평가 (자기 평가 편향 방지)
- 핵심 통찰: "생성과 평가를 분리하면 자기 평가 편향을 해결하는 강력한 레버가 된다"

**"Context Engineering" (2025.09) — 4가지 전략:**

1. **Just-in-Time Context**: 필요할 때만 데이터 로드 (경로, 쿼리만 유지)
2. **Compaction**: 이전 메시지 요약/압축
3. **Tool Result Clearing**: 사용된 도구 결과 제거
4. **Structured Note-taking**: NOTES.md, todo list 등으로 context window 바깥에 상태 유지

---

## 5. Agent Teams / Multi-Agent

### 5.1 핵심 리소스

Agent Teams에 대한 독립적인 "How to Build" 가이드는 아직 공식 발행되지 않음. 관련 정보는 아래 분산되어 있음:

| # | 출처 | 관련 내용 |
|---|------|----------|
| 1 | **Claude Agent SDK 블로그** | subagent 기반 병렬 작업 패턴 |
| 2 | **Harness Design 블로그** | Planner-Generator-Evaluator 3-agent 패턴 |
| 3 | **Claude Code Overview 문서** | "여러 Claude Code 에이전트가 동시에 다른 부분 작업. Lead agent가 조정" |
| 4 | **Opus 4.6 발표** | Agent Teams feature 언급 |
| 5 | **claude-code/plugins/README.md** | code-review 플러그인: 5개 병렬 Sonnet agent 예시 |

### 5.2 현재 알려진 패턴

- **Subagent 패턴**: lead agent가 subagent 생성, 각 subagent가 독립적 컨텍스트에서 작업
- **병렬 실행**: 읽기 전용 작업(검색, 분석)은 높은 병렬성, 쓰기 작업(빌드, 테스트)은 제한
- **Handoff Artifact**: 세션 간 상태 전달을 위한 구조화된 파일 (claude-progress.txt 등)
- **Context Reset vs Compaction**: compaction은 연속성 유지하지만 context anxiety 유발 가능. Reset은 깨끗한 시작이지만 handoff 비용 발생

---

## 6. Prompt Caching & Tool Design

### 6.1 핵심 리소스

| # | 제목 | 저자 | URL |
|---|------|------|-----|
| 1 | **Lessons from Building Claude Code: Prompt Caching Is Everything** | Thariq Shihipar | [X Thread](https://x.com/trq212/status/2024574133011673516) |
| 2 | **Lessons from Building Claude Code: Seeing Like an Agent** | Thariq Shihipar | [X Thread](https://x.com/trq212/status/2027463795355095314) |
| 3 | **Writing Effective Tools for AI Agents—Using Agents** | Anthropic Engineering | [anthropic.com](https://www.anthropic.com/engineering/writing-tools-for-agents) |

### 6.2 Prompt Caching 핵심 교훈 (Thariq)

- **정적 콘텐츠를 먼저, 동적 콘텐츠를 나중에** — 캐시 히트 극대화
- **도구 세트를 중간에 바꾸지 말 것** — 도구가 캐시된 prefix의 일부이므로, 추가/제거 시 전체 캐시 무효화
- **모델 전환 시 subagent 사용** — Opus가 Haiku에게 작업 위임하는 패턴
- **Plan Mode는 캐싱 제약 기반 설계** — 읽기 전용 도구로 교체하면 캐시 깨짐. 대신 EnterPlanMode/ExitPlanMode를 도구로 유지
- **system-reminder 태그로 업데이트** — 프롬프트를 수정하는 대신 다음 턴의 사용자 메시지에 업데이트 정보 추가

### 6.3 Tool Design 핵심 교훈 (Seeing Like an Agent)

- **Progressive Disclosure**: 에이전트가 필요시 재귀적으로 파일을 탐색하여 컨텍스트 구축
- **도구 없이 기능 추가**: "도구를 추가하지 않고도 progressive disclosure로 새 기능 추가 가능"
- **Ask User Question Tool**: 사용자와의 양방향 소통 대역폭 증가
- **Todo → Tasks 진화**: 의존성, 멀티에이전트 워크플로우, 세션 간 지속성 지원

---

## 7. 종합 참고 리소스

### Anthropic 공식

| 리소스 | URL |
|--------|-----|
| Engineering Blog 전체 목록 | [anthropic.com/engineering](https://www.anthropic.com/engineering) |
| Claude Code 공식 문서 | [code.claude.com/docs](https://code.claude.com/docs) |
| Agent SDK Overview | code.claude.com 내 Agent SDK 섹션 |
| Skills GitHub Repo | [github.com/anthropics/skills](https://github.com/anthropics/skills) |
| Plugins GitHub Repo | [github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) |
| Claude Code GitHub | [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code) |

### Thariq Shihipar 시리즈 (Anthropic Technical Staff)

| 주제 | 플랫폼 |
|------|--------|
| How We Use Skills | LinkedIn / X |
| Prompt Caching Is Everything | X Thread |
| Seeing Like an Agent (Tool Design) | X Thread |
| Building Claude Code at Anthropic (Vibe Code Camp) | [Distilled Transcript](https://davidguttman.github.io/every-vibe-code-camp-distilled/14_thariq_shihipar.html) |
| Figma MCP + Skills Livestream | Figma 공식 (Brett McMillin 공동) |
| Pinned Thread (전체 글 목록) | [x.com/trq212](https://x.com/trq212) |

### 커뮤니티 정리본

| 리소스 | URL |
|--------|-----|
| awesome-claude-code (종합 목록) | [github.com/hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) |
| claude-code-best-practice (Thariq 팁 포함) | [github.com/shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) |
| Harness Engineering Best Practices (Anthropic + OpenAI 통합) | [GitHub Gist](https://gist.github.com/celesteanders/21edad2367c8ede2ff092bd87e56a26f) |
| Context Engineering from Claude (AWS re:Invent 정리) | [01.me](https://01.me/en/2025/12/context-engineering-from-claude/) |
| Paradime Guide (Skills & Harness) | [paradime.io](https://www.paradime.io/guides/claude-code-skills-plugins-rules-guide) |

---

## 8. 최적 환경 설정 체크리스트

위 리소스에서 추출한 핵심 실천 항목:

### CLAUDE.md 설정
- [ ] 프로젝트 코딩 표준, 아키텍처 결정, 선호 라이브러리 명시
- [ ] 리뷰 체크리스트 포함
- [ ] `.claude/CLAUDE.md`를 버전 관리에 포함

### Skills 설정
- [ ] 9가지 카테고리 중 조직에 필요한 skill 식별
- [ ] Verification Skills에 최우선 투자 (1주일 가치)
- [ ] Gotchas 섹션을 실패 사례로 지속 업데이트
- [ ] Progressive Disclosure 패턴 활용 (SKILL.md → 하위 파일 참조)

### Hooks 설정
- [ ] 파일 편집 후 자동 포매팅 hook
- [ ] 커밋 전 lint/type-check hook
- [ ] SessionStart hook으로 필요 컨텍스트 자동 주입

### Plugins 설정
- [ ] 공식 marketplace에서 필요한 plugin 설치 (`/plugin marketplace add`)
- [ ] 프로젝트 스코프로 설치 (`--scope project`)하여 `.claude/settings.json`으로 팀 공유
- [ ] `/reload-plugins`로 변경사항 즉시 반영

### Prompt Caching 최적화
- [ ] 정적 콘텐츠 먼저, 동적 콘텐츠 나중에
- [ ] 도구 세트 변경 최소화
- [ ] system-reminder 패턴으로 프롬프트 업데이트

### Long-Running Tasks
- [ ] Initializer → Coding Agent 2-agent 패턴 또는 Planner → Generator → Evaluator 3-agent 패턴
- [ ] claude-progress.txt로 세션 간 상태 유지
- [ ] 각 성공적 작업 후 커밋
- [ ] 생성과 평가를 분리

---

*이 문서는 2026년 4월 5일 기준으로 작성되었습니다. Anthropic의 Claude Code 에코시스템은 빠르게 진화 중이므로, 정기적으로 [anthropic.com/engineering](https://www.anthropic.com/engineering)과 [Thariq의 X](https://x.com/trq212)를 확인하시기 바랍니다.*
