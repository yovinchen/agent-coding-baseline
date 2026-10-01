# agent-coding-baseline

Agent 编程（Claude Code / Codex）的个人基准仓库：统一个人偏好、commit 规范、项目模板和常用第三方 skill，让每个新项目从同一套规范起步。

## 收录内容

| 内容 | 来源 | 安装位置 |
| --- | --- | --- |
| 个人偏好 | `user/claude/CLAUDE.md`、`user/codex/AGENTS.md` | `~/.claude/`、`~/.codex/` |
| commit 规范（`/commit`） | `user/claude/commands/commit.md` | `~/.claude/commands/` |
| better-* 等 11 个 skill | [jakubkrehel/skills](https://github.com/jakubkrehel/skills)（MIT） | 用户级 `~/.claude/skills/` |
| web-design-guidelines | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)（MIT） | 用户级 `~/.claude/skills/` |
| impeccable skill + agents + hook | [pbakaus/impeccable](https://github.com/pbakaus/impeccable)（Apache 2.0） | 项目级 `<项目>/.claude/` |

## 结构

```text
agent-coding-baseline/
├── user/                    # 个人级配置（自己维护）
├── project/                 # 新项目模板：AGENTS.md、CLAUDE.md、.claude/、docs/、编辑器与 git 配置
├── vendor/                  # 上游 skill 原样同步，不手改
├── skills.json              # 上游清单：仓库、许可证、同步路径、安装范围
├── skills.lock.json         # 当前同步到的上游提交
├── .github/workflows/
│   ├── sync-upstream.yml    # 每周一 01:00 UTC 拉上游，有变化直接提交到本仓库；可手动触发
│   └── check.yml            # push / PR 时跑 scripts/check.sh
└── scripts/
    ├── sync-upstream.py     # 同步 vendor/；--check 只看有无更新
    ├── install-skills.py    # user：装到 ~/.claude/skills；project <目录>：装 skill/agents 并合并 hooks
    ├── new-project.sh       # 拷模板到目标目录（不覆盖已有文件）；--skills 顺带装项目级 skill
    ├── sync-user.sh         # user/ ↔ 本机：默认看差异，--apply 写入（自动 .bak），--pull 拉回
    └── check.sh             # 语法、JSON、vendor 与清单一致性、本机配置漂移
```

## 常用操作

新项目套用模板并安装项目级 skill：

```bash
scripts/new-project.sh ~/Projects/xxx/my-app --skills
```

把最新的用户级 skill 装到本机：

```bash
scripts/install-skills.py user
```

本机改了 `/commit` 或个人偏好后拉回仓库：

```bash
scripts/sync-user.sh --pull
```

手动检查上游是否有更新：

```bash
scripts/sync-upstream.py --check
```

## 约定

- 个人语言、工作偏好、模型参数只放 `user/`；`project/` 只放能随项目共享的约定。
- `vendor/` 只由同步脚本写入；新增上游时同时更新 `skills.json` 和 `THIRD_PARTY_NOTICES.md`。
- 项目里的 `.claude/skills/`、`.claude/agents/` 不入库（模板 `.gitignore` 已忽略），需要时从本仓库重装。
- 提交前跑 `scripts/check.sh`。
