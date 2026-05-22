# .githooks — 프로젝트 전용 git hooks

이 디렉토리는 본 저장소 전용 git hooks 를 포함합니다. **사용자가 한 번 설정해야 활성화**됩니다 (git 정책상 hook 은 저장소에 commit 되지만 자동 활성화되지 않음).

## 설치 (한 번만)

저장소 루트에서:

```bash
git config core.hooksPath .githooks
```

이렇게 하면 `.git/hooks/` 대신 `.githooks/` 가 사용됩니다.

확인:
```bash
git config core.hooksPath
# 출력: .githooks
```

## 비활성화

- **이번 커밋만 우회**: `git commit --no-verify`
- **영구 비활성화**: `git config --unset core.hooksPath`

## 등록된 Hooks

### `pre-commit` — `.claude/` ↔ `plugin/` drift 자동 방지 (M7)

배경: 개발 하네스(`.claude/`) 와 배포 카피(`plugin/clinical-pharmacology-study-protocol-development/`) 가 분리되어 있어 수동 sync 누락 시 plugin zip 이 stale 상태로 배포될 위험이 있었음 (2026-05-22 다중 모델 리뷰 M7).

동작:
1. staged 변경에 `.claude/` 파일이 포함되어 있는지 확인
2. 포함 시 `./sync_plugin.sh` 자동 실행 → 경로 치환(`.claude/` → `${CLAUDE_PLUGIN_ROOT}/`) 포함
3. 동기화된 `plugin/` 변경분을 동일 커밋의 staged 영역에 자동 추가
4. zip 파일 갱신이 필요한 경우 안내 메시지 출력 (zip 재빌드는 수동 — 변경 폭에 따라 사용자 판단)

zip 수동 재빌드:
```bash
cd plugin
rm -f clinical-pharmacology-study-protocol-development.zip
zip -rq clinical-pharmacology-study-protocol-development.zip \
    clinical-pharmacology-study-protocol-development \
    -x '*.DS_Store' -x '*__pycache__*' -x '*.pyc'
```

## CI 환경

CI 에서는 `git config core.hooksPath` 가 적용되지 않으므로 워크플로우 yaml 에 별도 step 으로 sync 검증 추가 권장:

```yaml
- name: Verify plugin sync
  run: |
    ./sync_plugin.sh
    git diff --exit-code plugin/clinical-pharmacology-study-protocol-development/ \
      || (echo "::error::plugin/ 가 .claude/ 와 동기화되지 않음" && exit 1)
```
