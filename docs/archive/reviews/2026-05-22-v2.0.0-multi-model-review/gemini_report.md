# Gemini 분석 보고서 — 문서·UX·플러그인 배포

## 1. 온보딩 & README
### 강점
- **체계적인 워크플로우 가시화**: `README.md`에 10단계(Phase 1-10) 파이프라인과 2개의 '사용자 검토 게이트'를 명확히 정의하여 신뢰성을 높임.
- **역할 기반 에이전트 설계**: 8개 에이전트의 역할과 모델(Sonnet/Opus)을 표 형태로 정리하여 사용자가 어떤 전문가와 협업하는지 직관적으로 인지 가능.
- **시험 유형별 특화**: FIH(신약)와 DDI/BE/FE(허가 약물)의 경로 분기를 명확히 하여 입력 데이터의 차이(IB 필수 여부 등)를 쉽게 이해하도록 돕고 있음.
- **국제화 및 전문 용어 병기**: 한국어 기본이나 의학/약학 전문 용어 및 규제 용어의 영문 병기가 일관성 있게 이루어져 전문성을 확보함.

### 개선점 (severity 표기)
- **Quickstart 예제 부족 (Minor)**: `README.md` 하단에 command 예시가 있으나, 실제 첫 실행 시 사용자가 마주할 'Trial Info' 입력 예시나 템플릿 파일에 대한 직접 링크가 더 강조되면 좋음.
- **문서 방대함으로 인한 초기 피로도 (Minor)**: `README.md`가 600줄이 넘어 핵심 가치를 빠르게 파악하기 어려울 수 있음. '5분 요약' 또는 '핵심 명령 일람' 섹션을 최상단에 배치 권장.

## 2. 플러그인 배포 구조
### 위험: sync drift
- **동기화 수동 의존**: `.claude/` (개발용)와 `plugin/` (배포용) 디렉토리가 분리되어 있으며 `sync_plugin.sh`를 통해 수동으로 동기화함. 개발자가 동기화 스크립트 실행을 누락할 경우 배포용 플러그인에 최신 기능이나 버그 수정이 반영되지 않을 위험이 있음. (CI/CD 자동화 필요)
- **경로 치환 누락 가능성**: `sync_plugin.sh`에서 `.claude/` → `${CLAUDE_PLUGIN_ROOT}/` 치환을 수행하나, 새로운 파일 확장자나 패턴이 추가될 경우 정규표현식에 의한 치환이 완벽하지 않을 수 있음.

### marketplace 등록 명확성
- **v2.0.0 스펙 준수**: `marketplace.json`과 `plugin.json`이 최신 Claude Code 플러그인 규격을 따르고 있으며, `keywords`와 `license` 등이 상세히 정의되어 있어 배포 준비 상태가 양호함.
- **버전 관리 일관성**: 루트 `CLAUDE.md`, `README.md`, `plugin.json`의 버전 정보가 2.0.0으로 동기화되어 있음.

## 3. 용어·개념 일관성
| 개념 | 일관성 상태 | 혼재/모순 사례 |
|------|-----------|--------------|
| **Phase** | 매우 높음 | 1-10 단계가 모든 에이전트 정의와 스킬에서 일관되게 인용됨. |
| **Agent** | 매우 높음 | 8개 에이전트의 명칭과 역할 정의가 명확히 분리됨 (특히 PK vs PD 영역). |
| **Command** | 높음 | `/research`, `/design` 등 7개 명령어가 Phase와 일대일 매칭됨. |
| **Gate** | 높음 | Phase 3, Phase 7의 '사용자 승인 게이트'가 모든 워크플로우 문서에 강조됨. |

## 4. 컴플라이언스 가시성 (IRB/PIPA/생명윤리법)
- **강점**: 
  - `icf-writer`가 PIPA(개인정보 보호법) 요건을 갖춘 별도의 개인정보 동의서를 생성함.
  - 약물유전체(PG) 및 대사체 분석 시 **생명윤리법**에 따른 별도 동의(Part 4)를 자동 포함하는 로직이 설계되어 있어 국내 규제 준수성이 매우 높음.
  - `regulatory-expert`가 MFDS(의약품안전나라)의 국내 임상시험 승인현황을 2단계(리스트 + Nexacro SOAP 상세)로 조사하여 국내 특화 데이터를 제공함.
- **주의**: 외부 사용자가 이 도구를 사용하더라도 최종 책임은 연구자에게 있음을 알리는 'Disclaimer'가 `README.md` 최상단에 더 명시적으로 보강될 필요가 있음.

## 5. TOP 5 즉시 개선안 (impact × effort)
1. **Disclaimer 강화 (High Impact / Low Effort)**: IRB 승인 전 사용 불가 및 AI 생성물의 최종 검토 책임이 사용자에게 있음을 명시하는 경고문구 최상단 배치.
2. **Phase 4 간소화 (High Impact / High Effort)**: `TODO.md`에도 언급된 20여 개의 의사결정 프로세스를 묶음(Bundle) 형태로 제시하여 사용자 피로도 감소 (Option A/B 채택).
3. **Quickstart 템플릿 제공 (Medium Impact / Low Effort)**: `e2e/v2`에서 사용된 `TRIAL_INFO_INPUT.md`와 같은 표준 입력 템플릿을 루트에 배치하여 즉시 복사-붙여넣기 가능하게 함.
4. **sync_plugin.sh 자동화 (Medium Impact / Medium Effort)**: pre-commit hook 또는 GitHub Actions를 통해 동기화 누락 방지.
5. **TS 참여 로직 완화 (Medium Impact / Medium Effort)**: NTI 약물이나 특정 규제 권고가 있는 경우 BE/FE 시험에서도 `translational-scientist`가 참여할 수 있도록 옵션화 (`TODO.md` #2 반영).
