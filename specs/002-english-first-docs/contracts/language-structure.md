# 契约：语言结构（逐字）

**对应**：FR-001 ~ FR-008、FR-012、FR-013；决策依据 [research.md](../research.md) R1 ~ R6。

本文件给出四处标记的**逐字内容**。实现任务照抄，不得改写措辞、空格或标点。

## 0. 文件头部的固定顺序

有两个语言版本的文档，其文件开头必须严格按下列顺序排列。

**英文原文**（`.github/README.md`、`.github/chefs-pick/SETUP.md`）：

```markdown
<!-- anchor: <H1 的锚点 id> -->
# <英文标题>

<语言入口行>

<正文第一段……>
```

**中文译本**（`.github/README.zh-CN.md`、`.github/chefs-pick/SETUP.zh-CN.md`）：

```markdown
<!-- anchor: <H1 的锚点 id> -->
# <中文标题>

<语言入口行>

<规范性声明引用块>

<来源标记行>

<正文第一段……>
```

各元素之间恰好一个空行。锚点行与标题行之间**不得**有空行。

## 1. 语言入口（FR-004、FR-005）

逐字四选一，不得增减空格：

| 文件 | 逐字内容 |
|---|---|
| `.github/README.md` | `**English** · [简体中文](README.zh-CN.md)` |
| `.github/README.zh-CN.md` | `[English](README.md) · **简体中文**` |
| `.github/chefs-pick/SETUP.md` | `**English** · [简体中文](SETUP.zh-CN.md)` |
| `.github/chefs-pick/SETUP.zh-CN.md` | `[English](SETUP.md) · **简体中文**` |

分隔符是 U+00B7 中点，左右各一个半角空格。

**其余六份文档（GUIDE、SOURCES、MAINTAINING、UPGRADE-TO-TEAM、CHANGELOG、LICENSE）不得出现语言入口，也不得出现任何关于**该文档自身**语言的说明。**

这一条约束的是文档谈论它自己：不写「本文为英文版」「中文版见……」之类的话。它不约束文档把「多语言文档怎么做」当作**内容**来讲——`GUIDE.md` 按 [guidance-layer-en.md](./guidance-layer-en.md) §6 必须有的 `## Translating your own README` 一节，讲的是**使用者自己仓库**的 README 怎么分英文版和中文译本，与 `GUIDE.md` 自己用什么语言写无关，因此不在禁止之列。该节中作为范例出现的语言入口写法位于围栏代码块内，按 §5 的纯度算法在判定前先被剥离，既不构成 `GUIDE.md` 的语言入口，也不计入它的语言纯度。

## 2. 规范性声明（FR-001）

只出现在译本中，逐字：

`.github/README.zh-CN.md`：

```markdown
> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。
```

`.github/chefs-pick/SETUP.zh-CN.md`：

```markdown
> 英文版是规范版本。本页与 [SETUP.md](SETUP.md) 不一致时，以英文版为准。
```

英文原文中**不得**出现任何对应内容。

## 3. 章节锚点（FR-007、FR-013）

写法：

```markdown
<!-- anchor: what-you-get -->
## What you get
```

- 单独成行，紧贴标题行上方，中间不得有空行。
- id 只用 `[a-z0-9][a-z0-9-]*`，同一文档内唯一。
- 只加在 `README`、`SETUP` 两份文档的两个语言版本上，共四个文件。
- 该文档每个标题（H1–H6，围栏代码块内的 `#` 行不算）都必须有且只有一个锚点。

**`README` 的锚点序列**（12 个，顺序固定）：

| # | 锚点 id | 英文标题 | 中文标题 |
|---|---|---|---|
| 1 | `chefs-pick-oss-starter` | `# Chef's Pick OSS Starter` | `# Chef's Pick OSS Starter` |
| 2 | `what-you-get` | `## What you get` | `## 你会得到什么` |
| 3 | `required` | `### Required` | `### 必需` |
| 4 | `recommended` | `### Recommended` | `### 推荐` |
| 5 | `optional` | `### Optional` | `### 可选` |
| 6 | `the-picks-at-a-glance` | `## The picks at a glance` | `## 主厨精选一览` |
| 7 | `how-we-pick` | `## How we pick` | `## 选型原则` |
| 8 | `quick-start` | `## Quick start` | `## 快速开始` |
| 9 | `good-to-know` | `## Good to know` | `## 注意事项` |
| 10 | `clean-up-when-done` | `## Clean up when done` | `## 完成后清理` |
| 11 | `feedback-and-contact` | `## Feedback and contact` | `## 反馈与联系` |
| 12 | `license` | `## License` | `## 许可证` |

H1 两侧都是 `Chef's Pick OSS Starter`：它是产品名，不翻译（FR-002 豁免产品名）。

**`SETUP` 的锚点序列**（3 个，顺序固定）：

| # | 锚点 id | 英文标题 | 中文标题 |
|---|---|---|---|
| 1 | `setup-checklist` | `# Setup checklist` | `# 起步清单` |
| 2 | `placeholders` | `## Placeholders` | `## 占位符` |
| 3 | `steps` | `## Steps` | `## 步骤` |

## 4. 来源标记（FR-012）

写法：

```markdown
<!-- translation-of: README.md sha256:0123456789abcdef -->
```

- `sha256:` 后是英文原文**完整字节**的 sha256 十六进制小写前 16 位。
- 第一个字段只写同目录下英文原文的文件名，不写路径。
- 每份译本有且只有一行，位置见 §0。
- 实现时不要手算摘要：先写占位值 `sha256:0000000000000000`，全部文档定稿后运行 `python3 tools/check_template.py --update-digests` 统一填入。

## 5. 单一数据源在译本中的写法（FR-011）

译本保留章节与锚点，但不复制表格。

`.github/README.zh-CN.md` 的 `the-picks-at-a-glance` 一节，逐字：

```markdown
<!-- anchor: the-picks-at-a-glance -->
## 主厨精选一览

16 个模块的选定来源、认可度证据和核实日期，汇总在英文原文的 [The picks at a glance](README.md#the-picks-at-a-glance) 一节。那张表由工具批量刷新，全模板只有一份，所以这里不另存一份。

完整选型清单见 [SOURCES.md](chefs-pick/SOURCES.md)，其中逐个模块记录了备选方案与未选原因。该文档只有英文版。
```

`.github/chefs-pick/SETUP.zh-CN.md` 的 `placeholders` 一节，开头逐字：

```markdown
<!-- anchor: placeholders -->
## 占位符

模板中的全部占位符登记在英文原文的 [Placeholders](SETUP.md#placeholders) 一节。那张表是唯一的一份，逐项列出占位符的名称、含义、出现的文件和示例值；名称、路径和示例都是标识符，不作翻译，所以这里不重复。

逐个替换，不要留下任何一个。
```

其后仍需给出 §1 中那两条查找命令的中文说明（命令本身逐字照抄英文原文，不翻译）。

**禁止**：译本中不得出现 `| Placeholder | Meaning | Files | Example |`、`<!-- summary:start -->`、`<!-- adoption-data:start -->` 中的任何一个。出现即视为复制了单一数据源。

## 6. 清理命令（FR-010）

`.github/README.md` 的 `clean-up-when-done` 一节与 `.github/README.zh-CN.md` 的对应节，都必须逐字包含：

```bash
git rm -r .github/README.md .github/README.zh-CN.md .github/chefs-pick
```

`tools/check_template.py` 的 `CLEANUP_COMMAND` 常量同步改成这一串。
