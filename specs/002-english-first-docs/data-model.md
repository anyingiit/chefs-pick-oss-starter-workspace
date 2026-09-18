# 数据模型：文档的语言结构

**对应**：[spec.md](./spec.md) 的 Key Entities 与 FR-001 ~ FR-018；实现形态见 [research.md](./research.md)。

本功能没有数据库，实体都是文件与文件内的标记。本文件定义每个实体的字段、取值约束和相互关系，供 `check_template.py` 的检查项直接实现。

## 1. 文档 (Document)

一份面向使用者的模板说明。它有且只有一个规范语言版本（英文）。

| 字段 | 取值 | 约束 |
|---|---|---|
| `id` | 文件基名，如 `README`、`SETUP` | 在其所在目录内唯一 |
| `canonical_path` | 英文原文的相对路径 | 必须存在；必须位于起步引导层内 |
| `editions` | 语言版本集合 | 必含 `en`；`en` 的路径即 `canonical_path` |
| `translated` | 布尔 | 仅 `README` 与 `SETUP` 为真（FR-006） |

**全集**（8 份，其中 2 份有译本）：

| id | 英文原文 | 中文译本 | 有语言入口 | 有锚点 |
|---|---|---|---|---|
| `README` | `.github/README.md` | `.github/README.zh-CN.md` | 是 | 是 |
| `SETUP` | `.github/chefs-pick/SETUP.md` | `.github/chefs-pick/SETUP.zh-CN.md` | 是 | 是 |
| `GUIDE` | `.github/chefs-pick/GUIDE.md` | — | 否 | 否 |
| `SOURCES` | `.github/chefs-pick/SOURCES.md` | — | 否 | 否 |
| `MAINTAINING` | `.github/chefs-pick/MAINTAINING.md` | — | 否 | 否 |
| `UPGRADE-TO-TEAM` | `.github/chefs-pick/UPGRADE-TO-TEAM.md` | — | 否 | 否 |
| `CHANGELOG` | `.github/chefs-pick/CHANGELOG.md` | — | 否 | 否 |
| `LICENSE` | `.github/chefs-pick/LICENSE` | — | 否 | 否 |

`LICENSE` 不是 Markdown，不参与锚点与语言入口规则，只受"单语"约束（research R1b）。

## 2. 语言版本 (Language edition)

某份文档在某种语言下的完整内容，单语呈现，独立成文件。

| 字段 | 取值 | 约束 |
|---|---|---|
| `lang` | `en` 或 `zh-CN` | 由文件名推导：`<id>.<lang>.md` 中的 `<lang>`；无后缀即 `en` |
| `path` | 相对路径 | 必须与其 `canonical` 同目录（research R1） |
| `is_canonical` | 布尔 | 仅 `lang == "en"` 为真 |
| `purity` | 见下 | 必须通过 |
| `anchors` | 有序的锚点 id 序列 | 与同文档其他版本逐一相同 |

**纯度约束**（research R6，预处理后判定）：

| `lang` | 判定 |
|---|---|
| `en` | 中文字符（U+4E00–U+9FFF）数为 0 |
| `zh-CN` | 不出现连续 6 个及以上英文词（词 = `[A-Za-z][A-Za-z'’-]*`） |

**预处理**（按顺序删除）：围栏代码块 → HTML 注释 → 行内代码 → Markdown 链接的 `(目标)` 部分 → 裸 URL → 语言入口行。

**状态转移**：一份译本只有两种状态——**已跟上**（来源标记等于英文原文当前摘要）与**已过期**（不等）。没有中间态。过期不阻断日常校验，但阻断发布（FR-014、FR-015）。

## 3. 语言入口 (Language selector)

文档顶部列出该文档全部语言版本的一行导航。

| 字段 | 取值 | 约束 |
|---|---|---|
| `line` | 逐字串 | 取自 [contracts/language-structure.md](./contracts/language-structure.md) §1 的四选一 |
| `position` | 行号 | H1 标题之后，上下各恰好一个空行 |
| `entries` | 语言 → 目标 | 当前语言为粗体纯文本，其余为相对链接 |

**约束**：
- 只出现在 `translated == true` 的文档上（FR-004）。其余文档一行都不许有。
- 列出的每个目标文件必须存在（FR-008）。
- 互达：从任一版本的入口出发，一步到达同文档的其他任一版本（FR-005）。
- 是全文档唯一允许含非本语言字符串的一行（纯度判定时被剔除）。

## 4. 规范性声明 (Canonical notice)

译本中告知读者"英文版为准"的固定引用块。

| 字段 | 取值 | 约束 |
|---|---|---|
| `text` | 逐字串 | 取自 contracts/language-structure.md §2 |
| `position` | 行号 | 紧接语言入口之后 |
| `target` | 英文原文文件名 | 必须与同文档的 `canonical` 一致 |

只出现在译本中。英文版不得有对应内容——英文即规范版本，声明它是同义反复（research R5）。

## 5. 章节锚点 (Section anchor)

标题前的语言无关标识，渲染后不可见。

| 字段 | 取值 | 约束 |
|---|---|---|
| `id` | `[a-z0-9][a-z0-9-]*` | 同一文档内唯一 |
| `line` | `<!-- anchor: <id> -->` | 单独成行 |
| `position` | 行号 | 紧贴标题行上方，中间不得有空行 |

**约束**：
- 只出现在 `translated == true` 的文档的各语言版本中。
- 该文档每一个标题（H1–H6，代码块内的除外）都必须有且只有一个锚点。
- 同文档各语言版本的锚点 id **有序序列**必须逐一相同（FR-013）。
- 渲染后可见字符数为 0（SC-013）。

**锚点全集**（逐字，见 contracts/language-structure.md §3）：

| 文档 | 锚点序列 |
|---|---|
| `README` | `chefs-pick-oss-starter`、`what-you-get`、`required`、`recommended`、`optional`、`the-picks-at-a-glance`、`how-we-pick`、`quick-start`、`good-to-know`、`clean-up-when-done`、`feedback-and-contact`、`license` |
| `SETUP` | `setup-checklist`、`placeholders`、`steps` |

## 6. 来源标记 (Source marker)

译本中记录其所依据的那一版英文原文的标识。

| 字段 | 取值 | 约束 |
|---|---|---|
| `source` | 英文原文文件名 | 同目录下必须存在 |
| `digest` | `sha256:` + 16 位小写十六进制 | 等于英文原文完整字节的 sha256 前 16 位 |
| `line` | `<!-- translation-of: <source> sha256:<16hex> -->` | 单独成行 |
| `position` | 行号 | 紧接规范性声明之后 |

**约束**：
- 每份译本有且只有一个来源标记。
- 只出现在译本中。
- 摘要不匹配时：日常校验记 `WARN`，`--release` 记 `FAIL`（FR-014、FR-015、宪章发布门禁 6）。
- 由 `python3 tools/check_template.py --update-digests` 统一刷新，译者改完译文之后运行。

## 7. 单一数据源 (Single-source data)

由工具批量刷新或逐项核对的结构化数据，全模板各只有一份，位于英文原文中（FR-011）。

| 数据 | 唯一位置 | 译本中的处理 |
|---|---|---|
| 16 行认可度摘要表 | `.github/README.md` 的 `<!-- summary:start/end -->` 之间 | `README.zh-CN.md` 保留同名同锚点章节，写中文说明并链接到英文原文，不复制表格 |
| 占位符登记表 | `.github/chefs-pick/SETUP.md` 的 Placeholders 一节 | `SETUP.zh-CN.md` 保留同名同锚点章节，写中文说明并链接，不复制表格 |
| 认可度数据表 | `.github/chefs-pick/SOURCES.md` 的 `<!-- adoption-data:start/end -->` 之间 | 该文档无译本，不涉及 |

**约束**：这三张表在整个 `template/` 中各只允许出现一次（SC-012）。译本中出现表头字面量即视为复制，判失败。

## 8. 契约数字一致性 (Contract parity)

不是文件内的实体，而是两份文件之间的关系约束，由新增的 C23 校验。

| 字段 | 取值 |
|---|---|
| `left` | `specs/001-chefs-pick-starter/contracts/guidance-layer.md` 中的全部 `★ N (owner/repo)` |
| `right` | `template/` 下全部 Markdown 中的全部 `★ N (owner/repo)` |
| 约束 | 同一 `owner/repo` 在 `left` 与 `right` 中的 `N` 必须相等 |

存量差异 12 处，取值以 `right` 为准（research R7 列出逐项新旧值）。
