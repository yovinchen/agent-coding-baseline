#!/usr/bin/env bash
# 把 user/ 下的个人级配置同步到 ~/.claude 与 ~/.codex。
# 默认只显示差异；加 --apply 才写入，写入前把旧文件备份为 *.bak。
# 加 --pull 反向操作：把本机当前配置拉回仓库，便于提交。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="diff"
case "${1:-}" in
  --apply) MODE="apply" ;;
  --pull) MODE="pull" ;;
  "") ;;
  *) echo "用法: $0 [--apply|--pull]" >&2; exit 2 ;;
esac

PAIRS=(
  "user/claude/CLAUDE.md:$HOME/.claude/CLAUDE.md"
  "user/claude/commands/commit.md:$HOME/.claude/commands/commit.md"
  "user/codex/AGENTS.md:$HOME/.codex/AGENTS.md"
)

for pair in "${PAIRS[@]}"; do
  src="$ROOT/${pair%%:*}"
  dst="${pair#*:}"
  case "$MODE" in
    diff)
      if [ ! -f "$dst" ]; then
        echo "新增: $dst"
      elif ! diff -q "$src" "$dst" >/dev/null; then
        echo "== $dst"
        diff -u "$dst" "$src" || true
      fi
      ;;
    apply)
      mkdir -p "$(dirname "$dst")"
      if [ -f "$dst" ] && ! diff -q "$src" "$dst" >/dev/null; then
        cp "$dst" "$dst.bak"
      fi
      cp "$src" "$dst"
      echo "已写入: $dst"
      ;;
    pull)
      [ -f "$dst" ] && cp "$dst" "$src" && echo "已拉回: ${pair%%:*}"
      ;;
  esac
done
