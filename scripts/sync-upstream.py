#!/usr/bin/env python3
"""按 skills.json 拉取上游默认分支，把指定路径同步到 vendor/<id>/，并更新 skills.lock.json。

用法: scripts/sync-upstream.py [--check]
  --check  只报告上游是否有新提交，不改文件；有更新时退出码为 1。
"""
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "skills.json"
LOCK = ROOT / "skills.lock.json"
VENDOR = ROOT / "vendor"


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def main():
    check_only = "--check" in sys.argv[1:]
    manifest = json.loads(MANIFEST.read_text())
    lock = json.loads(LOCK.read_text()) if LOCK.exists() else {"upstreams": {}}
    changed = []

    with tempfile.TemporaryDirectory() as tmp:
        for up in manifest["upstreams"]:
            uid, repo = up["id"], up["repository"]
            head = git("ls-remote", repo, "HEAD").split()[0]
            prev = lock["upstreams"].get(uid, {}).get("commit")
            if head == prev and (VENDOR / uid).exists():
                print(f"{uid}: 已是最新 {head[:7]}")
                continue
            print(f"{uid}: {prev[:7] if prev else '无'} -> {head[:7]}")
            changed.append(uid)
            if check_only:
                continue

            src = Path(tmp) / uid
            git("clone", "--quiet", "--depth", "1", repo, str(src))
            dest = VENDOR / uid
            if dest.exists():
                shutil.rmtree(dest)
            dest.mkdir(parents=True)
            for target, source in up["paths"].items():
                s = src / source
                if not s.exists():
                    sys.exit(f"{uid}: 上游缺少 {source}，请更新 skills.json 的 paths")
                (dest / target).parent.mkdir(parents=True, exist_ok=True)
                if s.is_dir():
                    shutil.copytree(s, dest / target, ignore=shutil.ignore_patterns(".git", ".DS_Store"))
                else:
                    shutil.copy2(s, dest / target)
            for name in up.get("skills", []):
                if not (dest / "skills" / name / "SKILL.md").exists():
                    sys.exit(f"{uid}: 上游已没有 skill {name}，请更新 skills.json")
            lock["upstreams"][uid] = {
                "repository": repo,
                "commit": head,
                "committedAt": git("log", "-1", "--format=%cI", cwd=src),
                "syncedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }

    if not check_only and changed:
        LOCK.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n")
    print("有更新: " + ", ".join(changed) if changed else "全部最新")
    sys.exit(1 if check_only and changed else 0)


if __name__ == "__main__":
    main()
