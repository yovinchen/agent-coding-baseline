#!/usr/bin/env bash
# 基准仓库自检：脚本语法、JSON 合法性、vendor/ 与清单一致；本机运行时额外报告 user/ 配置漂移。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
status=0

for f in scripts/*.sh; do
  bash -n "$f" || status=1
done
for f in scripts/*.py; do
  python3 -m py_compile "$f" || status=1
done
find scripts -name '__pycache__' -type d -exec rm -rf {} +

while IFS= read -r f; do
  python3 -m json.tool "$f" >/dev/null || { echo "JSON 无效: $f"; status=1; }
done < <(find . -name '*.json' -not -path './.git/*')

python3 - <<'PY' || status=1
import json, sys
from pathlib import Path
manifest = json.load(open("skills.json"))
lock = json.load(open("skills.lock.json"))["upstreams"]
bad = []
for up in manifest["upstreams"]:
    uid = up["id"]
    if uid not in lock:
        bad.append(f"{uid}: skills.lock.json 缺少记录")
    for name in up["skills"]:
        if not Path(f"vendor/{uid}/skills/{name}/SKILL.md").exists():
            bad.append(f"{uid}: vendor 中缺少 {name}/SKILL.md")
    lic = up.get("licenseFile", "LICENSE")
    if not Path(f"vendor/{uid}/{lic}").exists():
        bad.append(f"{uid}: vendor 中缺少 {lic}")
for b in bad:
    print(b)
sys.exit(1 if bad else 0)
PY

if [ -z "${CI:-}" ] && [ -d "$HOME/.claude" ]; then
  drift=$(scripts/sync-user.sh)
  if [ -n "$drift" ]; then
    echo "user/ 与本机配置不一致（scripts/sync-user.sh 查看，--pull 或 --apply 处理）:"
    echo "$drift" | grep -E '^(==|新增)' || true
  fi
fi

[ $status -eq 0 ] && echo "检查通过"
exit $status
