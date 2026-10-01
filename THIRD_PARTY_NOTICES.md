# Third-party notices

`vendor/` 下的内容由 `scripts/sync-upstream.py` 从上游原样同步，未做修改；对应提交记录在 `skills.lock.json`。各目录保留上游的 LICENSE（及 NOTICE），并继续受其许可证约束。

## jakubkrehel/skills → `vendor/jakubkrehel-skills/`

- 作者：Jakub Krehel，Copyright (c) 2026 Jakub Krehel
- 来源：https://github.com/jakubkrehel/skills（https://jakub.kr/skills）
- 许可证：MIT，全文见 `vendor/jakubkrehel-skills/LICENSE`
- 用途：UI、可访问性、配色、布局、排版、文案的评审与打磨指引，安装为用户级 skill。

## pbakaus/impeccable → `vendor/impeccable/`

- 来源：https://github.com/pbakaus/impeccable（https://impeccable.style），同步其 `plugin/` 下的 skills、agents、hooks
- 许可证：Apache License 2.0，全文见 `vendor/impeccable/LICENSE`；上游第三方声明见 `vendor/impeccable/NOTICE.md`
- 用途：前端设计与评审 skill、配套子代理，以及 UI 变更检测 hook，安装为项目级 skill。
- 说明：`scripts/install-skills.py` 安装时会把 hooks 中的 `${CLAUDE_PLUGIN_ROOT}` 改写为 `${CLAUDE_PROJECT_DIR}/.claude`，写入目标项目的 settings，`vendor/` 中的文件本身不改动。

## vercel-labs/agent-skills → `vendor/vercel-agent-skills/`

- 作者：Vercel
- 来源：https://github.com/vercel-labs/agent-skills，仅同步 `skills/web-design-guidelines`
- 许可证：MIT。上游仓库没有单独的 LICENSE 文件，许可证声明见其 README 的 License 小节，同步保存在 `vendor/vercel-agent-skills/README.md`
- 用途：按 Vercel Web Interface Guidelines 评审 UI 代码，安装为用户级 skill。该 skill 运行时会从 https://github.com/vercel-labs/web-interface-guidelines （MIT）拉取最新规则，规则本身不入库。
