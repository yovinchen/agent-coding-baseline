#!/usr/bin/env python3
"""把 vendor/ 中的 skill、agent 安装到目标位置。

用法:
  scripts/install-skills.py project <项目目录>   安装 scope=project 的上游（impeccable）：
      skills/agents 拷到 <项目>/.claude/，上游 hooks 改写为项目路径后合并进 .claude/settings.json
  scripts/install-skills.py user [--dry-run]       安装 scope=user 的上游（jakubkrehel/skills）到 ~/.claude/skills
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "skills.json").read_text())


def copy_dir(src: Path, dst: Path, dry: bool):
    print(f"{'将安装' if dry else '安装'}: {dst}")
    if dry:
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def install(up, base: Path, dry: bool):
    vendor = ROOT / "vendor" / up["id"]
    for name in up["skills"]:
        copy_dir(vendor / "skills" / name, base / "skills" / name, dry)
    agents = vendor / "agents"
    if agents.exists():
        for f in sorted(agents.glob("*.md")):
            print(f"{'将安装' if dry else '安装'}: {base / 'agents' / f.name}")
            if not dry:
                (base / "agents").mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, base / "agents" / f.name)


def merge_hooks(up, claude_dir: Path):
    hooks_file = ROOT / "vendor" / up["id"] / "hooks" / "hooks.json"
    if not hooks_file.exists():
        return
    text = hooks_file.read_text().replace("${CLAUDE_PLUGIN_ROOT}", "${CLAUDE_PROJECT_DIR}/.claude")
    upstream = json.loads(text)["hooks"]
    settings_path = claude_dir / "settings.json"
    settings = json.loads(settings_path.read_text()) if settings_path.exists() else {}
    hooks = settings.setdefault("hooks", {})
    marker = f"/skills/{up['skills'][0]}/"
    for event, groups in upstream.items():
        kept = [g for g in hooks.get(event, []) if not any(marker in h.get("command", "") for h in g.get("hooks", []))]
        hooks[event] = kept + groups
    settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n")
    print(f"合并 hooks: {settings_path}")


def main():
    args = sys.argv[1:]
    if not args or args[0] not in ("project", "user"):
        sys.exit(__doc__)
    scope = args[0]
    dry = "--dry-run" in args
    if scope == "project":
        if len(args) < 2:
            sys.exit(__doc__)
        base = Path(args[1]).expanduser().resolve() / ".claude"
    else:
        base = Path.home() / ".claude"
    for up in MANIFEST["upstreams"]:
        if up["scope"] != scope:
            continue
        install(up, base, dry)
        if scope == "project" and not dry:
            merge_hooks(up, base)


if __name__ == "__main__":
    main()
