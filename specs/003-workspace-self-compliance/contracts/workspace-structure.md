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
# 后续发布：在模板仓库的克隆里替换内容，追加一个提交
git -C <clone-path> fetch origin main
git -C <clone-path> checkout main
cp -a template/. <clone-path>/
git -C <clone-path> add -A
git -C <clone-path> commit -m "docs: sync template content"
git -C <clone-path> push origin main
```

该节必须逐字包含以下三句警告（英文版为准，中文版为其译文）：

1. `Never force-push to the template repository.`
2. `A rejected push means the template repository has commits this workspace does not; stop and investigate rather than forcing.`
3. `git subtree split produces a history with no common ancestor with the template repository, so it can only be pushed with --force — use it for the first publish to an empty repository and never afterwards.`

## 8. 不得改动的范围（FR-017、FR-018）

- `template/` 下的任何文件内容不得改变。
- 不得向模板仓库推送任何内容、创建标签或发布。
