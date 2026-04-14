#!/usr/bin/env bash
# sync_plugin.sh
#
# 개발용 .claude/ 를 배포용 plugin/clinical-pharmacology-study-protocol-development/
# 으로 동기화. 경로 참조(.claude/ → ${CLAUDE_PLUGIN_ROOT}/)를 plugin 카피에만 적용.
#
# 사용법: scripts/sync_plugin.sh [--dry-run]

set -euo pipefail

PLUGIN_DIR="plugin/clinical-pharmacology-study-protocol-development"
SUBDIRS=(agents commands skills scripts references)

DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN="--dry-run"
  echo "[DRY-RUN 모드] 실제 변경 없이 변경 예정만 출력"
fi

if [[ ! -d ".claude" ]]; then
  echo "ERROR: .claude/ 디렉토리가 없습니다. 프로젝트 루트에서 실행하세요." >&2
  exit 1
fi

echo "=== .claude/ → $PLUGIN_DIR/ 동기화 ==="
for sub in "${SUBDIRS[@]}"; do
  if [[ -d ".claude/$sub" ]]; then
    echo "- $sub/"
    rsync -a $DRY_RUN \
      --delete \
      --exclude='__pycache__/' \
      --exclude='.DS_Store' \
      --exclude='*.pyc' \
      ".claude/$sub/" "$PLUGIN_DIR/$sub/"
  fi
done

if [[ -z "$DRY_RUN" ]]; then
  echo ""
  echo "=== plugin/ 내부 경로 참조 치환 (.claude/ → \${CLAUDE_PLUGIN_ROOT}/) ==="
  find "$PLUGIN_DIR" -name "*.md" -exec sed -i '' 's|\.claude/|${CLAUDE_PLUGIN_ROOT}/|g' {} \;

  LEFT=$(grep -rn "\.claude/" "$PLUGIN_DIR" --include="*.md" 2>/dev/null | wc -l | tr -d ' ')
  ROOT_REFS=$(grep -rn "CLAUDE_PLUGIN_ROOT" "$PLUGIN_DIR" --include="*.md" 2>/dev/null | wc -l | tr -d ' ')
  echo "  .claude/ 잔재: $LEFT"
  echo "  \${CLAUDE_PLUGIN_ROOT}/ 참조: $ROOT_REFS"
  if [[ "$LEFT" != "0" ]]; then
    echo "  WARNING: .claude/ 잔재가 남아있습니다. 수동 확인 필요." >&2
  fi
fi

echo ""
echo "동기화 완료."
