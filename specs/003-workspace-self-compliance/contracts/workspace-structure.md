# 契约：工作区门面文档的结构

逐字契约。凡本文件写成代码块或行内代码的内容，实现时必须一字不差地照抄。

## 1. 语言入口（FR-005、FR-008）

各放在文件首个一级标题之后、空行分隔，逐字为：

| 文件 | 该行内容 |
|---|---|
| `README.md` | `**English** · [简体中文](README.zh-CN.md)` |
| `README.zh-CN.md` | `[English](README.md) · **简体中文**` |

分隔符是 U+00B7 中点，左右各一个半角空格。写法与模板引导层完全一致（002 契约 language-structure §1），只是链接目标换成工作区自己的文件。

## 2. 章节锚点序列（FR-013）

每个标题之前一行放 `<!-- anchor: <id> -->`，渲染后不可见。两种语言版本的锚点序列必须**逐字相同、顺序相同**：

```
chefs-pick-oss-starter-workspace
layout
common-commands
publishing
license
```

共 5 项，对应 1 个一级标题与 4 个二级标题。

## 3. 规范性声明（FR-006）

只出现在 `README.zh-CN.md`，位于语言入口之后，逐字为：

```
> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。
```

`README.md` 中不得出现任何关于本文语言的说明。

## 4. 来源标记（FR-014）

只出现在 `README.zh-CN.md`，全文**恰好一处**，逐字形如：

```
<!-- translation-of: README.md sha256:<16 位十六进制> -->
```

摘要是 `README.md` 文件字节的 SHA-256 前 16 位十六进制。摘要值由 `python3 tools/check_template.py --update-digests` 写入，**不得手算、不得手改**。

## 5. 语言纯度（FR-005、FR-006、FR-009）

判定前依次剥离：围栏代码块（含 ``` 与 ~~~ 两种）→ HTML 注释 → 行内代码 → Markdown 链接目标 → 裸 URL → 语言入口行。剥离后：

- `README.md`：中文字符数必须为 **0**。
- `README.zh-CN.md`：最长连续英文词串必须**小于 6**。

与模板侧使用同一套函数（`strip_for_purity`、`cjk_count`、`longest_english_run`），不另写实现。

## 6. 可机读事实的承载句式（FR-011、FR-012）

三项事实各用一条固定句式承载，两种语言版本都必须出现且取值一致。

| 事实 | `README.md` 中的句式 | `README.zh-CN.md` 中的句式 |
|---|---|---|
| `template/` 文件数 | `` `template/` holds <N> files. `` | `` `template/` 共 <N> 个文件。 `` |
| 结构校验项数 | `` <N> structural checks `` | `` <N> 项结构校验 `` |
| 规格目录 | 目录结构表中每个 `` `specs/<目录名>/` `` 各占一行 | 同左 |

`<N>` 为十进制整数，不加千分位。规格目录一项的判定是：`specs/` 下**每一个**实际存在的目录名都必须在该文件中以 `` `specs/<目录名>/` `` 的形式出现；允许文件中出现额外说明文字，但不得遗漏任何一个目录。

## 7. 发布流程（FR-001 ~ FR-004）

`README.md` 的 `publishing` 一节必须区分两种情形。后续发布的步骤逐字包含以下命令块（`<template-remote>` 与 `<clone-path>` 是占位说明，允许维护者替换为实际值）：

```bash
git -C <clone-path> fetch origin main
git -C <clone-path> checkout -B main origin/main
git -C <clone-path> rm -rqf .
cp -a template/. <clone-path>/
git -C <clone-path> add -A
diff -r --exclude=.git <clone-path> template
git -C <clone-path> commit -m "docs: sync template content"
git -C <clone-path> push origin main
```

该节还必须以正文散文（不是行内代码）给出三条警告，逐字措辞见 §9（英文）与 §10（中文）：
不得强制推送；推送被拒时停下排查而非强推；`git subtree split` 的历史与模板仓库没有共同祖先、
只适用于向空仓库的首次发布。命令块内的注释各用本文件自己的语言书写。

## 8. 不得改动的范围（FR-017、FR-018）

- `template/` 下的任何文件内容不得改变。
- 不得向模板仓库推送任何内容、创建标签或发布。

## 9. `README.md` 全文（逐字）

实现时整份文件的内容必须与下面的代码块完全一致，包括空行。`<!-- translation-of: -->` 不出现在本文件中。

````markdown
<!-- anchor: chefs-pick-oss-starter-workspace -->
# Chef's Pick OSS Starter — development workspace

**English** · [简体中文](README.zh-CN.md)

This is the development and maintenance workspace for the
[chefs-pick-oss-starter](https://github.com/anyingiit/chefs-pick-oss-starter)
template repository. The specification, selection research and validation tooling live
here; the template repository carries only the contents of `template/`.

<!-- anchor: layout -->
## Layout

| Path | What it is | Published |
|---|---|---|
| `template/` | Everything on the template repository's default branch | Yes |
| `specs/001-chefs-pick-starter/` | The original specification, plan, tasks, research and contracts | No |
| `specs/002-english-first-docs/` | The English-first documentation restructure | No |
| `specs/003-workspace-self-compliance/` | Holding this workspace to the rules it ships | No |
| `tools/` | Validation and data-refresh scripts, with their tests | No |
| `.specify/`, `.claude/` | Spec Kit and AI assistant configuration | No |

`template/` holds 28 files. **Only `template/` is ever published.** Check C02 rejects any
development file that finds its way into it.

<!-- anchor: common-commands -->
## Common commands

```bash
python3 tools/check_template.py              # 27 structural checks
python3 tools/check_template.py --release    # release gate; verification dates tighten to 30 days
python3 tools/check_template.py --update-digests  # refresh translation source markers
python3 -m unittest discover -s tools/tests  # unit tests
python3 tools/verify_sources.py              # dry-run refresh of the adoption data
python3 tools/verify_sources.py --write      # write the refreshed adoption data
```

Refreshing adoption data requires an authenticated `gh` CLI. The review cadence,
re-evaluation triggers and release gates are documented in
`template/.github/chefs-pick/MAINTAINING.md`.

<!-- anchor: publishing -->
## Publishing

Publishing means copying the contents of `template/` onto the default branch of the
template repository. Nothing else in this workspace is ever published. The full context is
in parts B, C and D of [quickstart.md](specs/001-chefs-pick-starter/quickstart.md).

Which steps apply depends on whether the template repository already has content.

**First publish, to a newly created empty repository.** Either copy the contents of
`template/` into a clone of the empty repository and commit, or run:

```bash
git subtree split --prefix=template -b publish
git push <template-remote> publish:main
```

**Every publish after that.** Work in a clone of the template repository and add a commit
on top of what is already there:

```bash
# Subsequent publish: replace the content inside a clone, add one commit
git -C <clone-path> fetch origin main
git -C <clone-path> checkout -B main origin/main
git -C <clone-path> rm -rqf .
cp -a template/. <clone-path>/
git -C <clone-path> add -A
diff -r --exclude=.git <clone-path> template
git -C <clone-path> commit -m "docs: sync template content"
git -C <clone-path> push origin main
```

Two of those steps are easy to leave out and both cause real damage. `checkout -B main origin/main`
resets the clone to the published branch, so a clone that is behind cannot build its commit on
stale history and a clone carrying unrelated local commits cannot push them into the template
repository. `git rm -rqf .` empties the working tree first, so a file deleted from `template/`
actually disappears from the publication instead of lingering, and a path that changed between a
file and a directory does not make the copy fail. The `diff` line is the checkpoint: it must print
nothing before you commit.

Three things to know, because getting them wrong damages the published repository:

- Never force-push to the template repository.
- A rejected push means the template repository has commits this workspace does not; stop and investigate rather than forcing.
- `git subtree split` produces a history with no common ancestor with the template repository, so it can only be pushed with `--force`. Use it for the first publish to an empty repository and never afterwards.

That last point is not hypothetical. The template repository carries a `v1.0.0` tag, and
force-pushing a split history would leave the commit that tag points at unreachable from
any branch.

Never merge a Dependabot pull request on the template repository directly — see the
"Action updates" section of MAINTAINING for why.

<!-- anchor: license -->
## License

MIT, same as the template repository. The template's own license and attribution notes are
in `template/.github/chefs-pick/LICENSE`.
````

## 10. `README.zh-CN.md` 全文（逐字）

整份文件的内容必须与下面的代码块完全一致，唯一例外是来源标记中的 16 位摘要——那一位由 `--update-digests` 写入，实现时先填 16 个 `0`，随后运行该命令刷新。

````markdown
<!-- anchor: chefs-pick-oss-starter-workspace -->
# Chef's Pick OSS Starter — 开发工作区

[English](README.md) · **简体中文**

> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。

<!-- translation-of: README.md sha256:0000000000000000 -->

这是 [chefs-pick-oss-starter](https://github.com/anyingiit/chefs-pick-oss-starter)
模板仓库的开发与维护工作区：规格、选型调研、校验工具都在这里，模板仓库只承载 `template/` 的内容。

<!-- anchor: layout -->
## 目录结构

| 路径 | 说明 | 是否发布 |
|---|---|---|
| `template/` | 模板仓库默认分支的全部内容 | 是 |
| `specs/001-chefs-pick-starter/` | 最初的规格、计划、任务、调研与契约 | 否 |
| `specs/002-english-first-docs/` | 文档改为英文规范版的改造 | 否 |
| `specs/003-workspace-self-compliance/` | 让工作区遵守它自己交付的规矩 | 否 |
| `tools/` | 校验与数据刷新脚本及其测试 | 否 |
| `.specify/`、`.claude/` | Spec Kit 与 AI 助手的配置 | 否 |

`template/` 共 28 个文件。**只有 `template/` 会被发布。** 校验项 C02 会拦截任何混入其中的开发文件。

<!-- anchor: common-commands -->
## 常用命令

```bash
python3 tools/check_template.py              # 27 项结构校验
python3 tools/check_template.py --release    # 发布门禁，核实日期收紧到 30 天
python3 tools/check_template.py --update-digests  # 刷新译本的来源标记
python3 -m unittest discover -s tools/tests  # 单元测试
python3 tools/verify_sources.py              # 只读复核认可度数据
python3 tools/verify_sources.py --write      # 写入刷新后的认可度数据
```

刷新认可度数据需要已登录的 `gh` 命令行工具。复核周期、重新评估的触发条件与发布门禁，见
`template/.github/chefs-pick/MAINTAINING.md`。

<!-- anchor: publishing -->
## 发布

发布指的是把 `template/` 的内容复制到模板仓库的默认分支上。工作区里的其他内容一概不发布。
完整背景见 [quickstart.md](specs/001-chefs-pick-starter/quickstart.md) 的 B、C、D 三部分。

用哪一套步骤，取决于模板仓库里是否已经有内容。

**首次发布，目标是刚建好的空仓库。** 把 `template/` 的内容复制进空仓库的克隆后提交即可，或者运行：

```bash
git subtree split --prefix=template -b publish
git push <模板仓库远程名> publish:main
```

**此后的每一次发布。** 在模板仓库的克隆里操作，在已有内容之上追加一个提交：

```bash
# 后续发布：在模板仓库的克隆里替换内容，追加一个提交
git -C <克隆路径> fetch origin main
git -C <克隆路径> checkout -B main origin/main
git -C <克隆路径> rm -rqf .
cp -a template/. <克隆路径>/
git -C <克隆路径> add -A
diff -r --exclude=.git <克隆路径> template
git -C <克隆路径> commit -m "docs: sync template content"
git -C <克隆路径> push origin main
```

其中两步最容易被省掉，而省掉任何一步都会造成真实的损坏。`checkout -B main origin/main` 把克隆重置到
已发布的分支，这样落后的克隆不会把提交建在陈旧历史上，带着无关本地提交的克隆也不会把它们推进模板仓库。
`git rm -rqf .` 先清空工作树，于是从 `template/` 删掉的文件在发布内容中真的消失，而不是残留下来；
某个路径在文件与目录之间变更时，复制也不会失败。`diff` 那一行是检查点：提交前它必须没有任何输出。

有三件事必须知道，弄错会损坏已发布的仓库：

- 绝不要对模板仓库强制推送。
- 推送被拒，意味着模板仓库上有工作区没有的提交；此时应当停下来排查，而不是强推。
- `git subtree split` 切出的历史与模板仓库没有共同祖先，只能靠 `--force` 推上去。它适用于向空仓库的首次发布，此后一概不用。

最后这一条不是假想。模板仓库上有 `v1.0.0` 标签，强推一套 split 历史会让该标签指向的提交
从任何分支都不再可达。

也不要在模板仓库上直接合并 Dependabot 的合并请求，原因见 MAINTAINING 的「动作版本更新」一节。

<!-- anchor: license -->
## 许可证

MIT，与模板仓库一致。模板自身的许可证与署名说明见
`template/.github/chefs-pick/LICENSE`。
````
