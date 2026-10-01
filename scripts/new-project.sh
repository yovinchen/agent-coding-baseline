#!/usr/bin/env bash
# 把 project/ 模板拷进目标目录，已存在的文件一律跳过，不覆盖。
# 用法: scripts/new-project.sh <目标目录> [--skills]
#   --skills  从 vendor/ 安装项目级 skill（impeccable 及其 agents、hooks）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-}"
[ -n "$TARGET" ] || { echo "用法: $0 <目标目录> [--skills]" >&2; exit 2; }
mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"

cd "$ROOT/project"
find . -type f | sed 's|^\./||' | sort | while read -r rel; do
  if [ -e "$TARGET/$rel" ]; then
    echo "跳过（已存在）: $rel"
  else
    mkdir -p "$TARGET/$(dirname "$rel")"
    cp "$rel" "$TARGET/$rel"
    echo "新增: $rel"
  fi
done

if [ "${2:-}" = "--skills" ]; then
  python3 "$ROOT/scripts/install-skills.py" project "$TARGET"
fi

echo "完成。下一步：填写 $TARGET/AGENTS.md 中的 <占位>，按需调整 .claude/launch.json。"
