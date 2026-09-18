# Chef's Pick OSS Starter — 开发工作区 / Development workspace

这是 [chefs-pick-oss-starter](https://github.com/anyingiit/chefs-pick-oss-starter) 模板仓库的**开发与维护工作区**：规格、选型调研、校验工具都在这里，模板仓库只承载 `template/` 的内容。

This is the development and maintenance workspace for the
[chefs-pick-oss-starter](https://github.com/anyingiit/chefs-pick-oss-starter)
template repository. The specification, selection research and validation tooling live
here; the template repository carries only the contents of `template/`.

## 目录结构 / Layout

| 路径 | 说明 / What it is | 是否发布 / Published |
|---|---|---|
| `template/` | 模板仓库默认分支的全部内容（26 个文件） / everything on the template repo's default branch | 是 / yes |
| `specs/001-chefs-pick-starter/` | 规格、计划、任务、调研、契约 / spec, plan, tasks, research, contracts | 否 / no |
| `tools/` | 校验与数据刷新脚本及其测试 / validation and data-refresh scripts, with tests | 否 / no |
| `.specify/`、`.claude/` | Spec Kit 与 AI 助手配置 / Spec Kit and AI assistant config | 否 / no |

**只有 `template/` 会被发布。** 校验项 C02 会拦截任何进入 `template/` 的开发文件。

## 常用命令 / Common commands

```bash
python3 tools/check_template.py              # 24 项结构校验 / 24 structural checks
python3 tools/check_template.py --release    # 发布门禁（核实日期收紧到 30 天）
python3 -m unittest discover -s tools/tests  # 单元测试 / unit tests
python3 tools/verify_sources.py              # 只读复核认可度数据 / dry-run refresh
python3 tools/verify_sources.py --write      # 写入刷新结果 / write refreshed data
```

数据刷新需要已登录的 `gh` CLI。复核周期、触发条件和发布门禁见
`template/.github/chefs-pick/MAINTAINING.md`。

Refreshing adoption data requires an authenticated `gh` CLI. The review cadence,
re-evaluation triggers and release gates are documented in
`template/.github/chefs-pick/MAINTAINING.md`.

## 发布 / Publishing

完整步骤见 [quickstart.md](specs/001-chefs-pick-starter/quickstart.md) 的 B、C、D 三部分。
把 `template/` 推送到模板仓库：

The full procedure is in parts B, C and D of
[quickstart.md](specs/001-chefs-pick-starter/quickstart.md). To push `template/` to the
template repository:

```bash
git subtree split --prefix=template -b publish
git push <模板仓库远程名 / template remote> publish:main
```

不要把本工作区的其他目录推送到模板仓库，也不要在模板仓库上直接合并 Dependabot 的合并请求
（原因见 MAINTAINING 的"动作版本更新"一节）。

Never push this workspace's other directories to the template repository, and never merge
Dependabot pull requests on the template repository directly — see the "Action updates"
section of MAINTAINING for why.

## 许可证 / License

MIT，与模板仓库一致。模板自身的许可证与署名说明见
`template/.github/chefs-pick/LICENSE`。

MIT, same as the template repository. The template's own license and attribution notes are
in `template/.github/chefs-pick/LICENSE`.
