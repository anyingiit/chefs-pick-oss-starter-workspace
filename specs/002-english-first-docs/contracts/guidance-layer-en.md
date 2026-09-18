# 契约：起步引导层改为英文规范版本

**对应**：FR-002、FR-003、FR-006、FR-007、FR-009 ~ FR-011、FR-016、FR-017；决策依据 [research.md](../research.md) R1b、R9 ~ R11。

本文件逐文件说明改造内容。**通则**：删除中文段落、把"中文 / English"式的标题与表头改成其英文部分、保留英文内容原样。除 §7 明确列出的一处外，**不得改写任何现存英文句子**。

## 0. 通用规则

1. **标题**：`## 你会得到什么 / What you get` → `## What you get`。取 ` / ` 之后的英文部分，前面加锚点行（仅 README 与 SETUP）。
2. **表格表头**：`| 模块 / Module |` → `| Module |`，逐格照此。
3. **行内并排**：形如 `中文句子。/ English sentence.` 的列表项与单元格，只保留英文部分，连同分隔的 ` / ` 一并删除。
4. **成段并排**：一段中文后跟一段英文的，删除中文段落，保留英文段落。
5. **不得删除信息**：若英文部分缺少中文部分才有的内容，按 §7 处理，不得默默丢失（SC-003 的"信息不减少"）。
6. **代码块、命令、文件路径、URL、Star 数、日期一律不动。**

## 1. `.github/README.md`（模板首页，英文规范版本）

- H1 改为 `# Chef's Pick OSS Starter`（去掉 ` · 主厨精选开源仓库起步模板`）。
- 按 [language-structure.md](./language-structure.md) §0 加锚点与语言入口。
- 删去 H1 下方那段引用块中的中文句，只留英文句，并把其中的 `[README.md](../README.md)` 保持不变。
- `## What you get` 的三级清单：`- \`README.md\` — 项目说明 / Project readme（M01）` → `- \`README.md\` — Project readme (M01)`。全角括号改半角。
- `## The picks at a glance` 的 16 行摘要表：表头改为 `| Module | Pick | Adoption | Verified |`；模块名列 `M01 项目说明 / README` → `M01 README`，其余 15 行照此；`平台官方功能 / Official platform feature` → `Official platform feature`；`事实标准 / De facto standard（454 adopters）` → `De facto standard (454 adopters)`。`<!-- summary:start -->` 与 `<!-- summary:end -->` 标记保留不动。
- 其余各节按 §0 通则删中文留英文。
- `## Clean up when done` 的 bash 代码块改为 language-structure §6 的新命令。

## 2. `.github/README.zh-CN.md`（新建，中文译本）

- 完整覆盖英文原文的 12 个章节，锚点序列与英文原文逐一相同（language-structure §3）。
- 头部顺序按 language-structure §0 的译本形态。
- `the-picks-at-a-glance` 一节逐字照抄 language-structure §5。
- 其余各节把英文内容译成中文；文件名、命令、产品名、许可证标识、模块编号不译。
- 指向只有英文版的文档（GUIDE、SOURCES、MAINTAINING、UPGRADE-TO-TEAM、CHANGELOG）时直接链接，**不加任何"目标是英文"的提示**（规格澄清第 7 问）。
- 不得出现连续 6 个及以上英文词（research R6）。

## 3. `.github/chefs-pick/SETUP.md`（起步清单，英文规范版本）

- H1 改为 `# Setup checklist`。加锚点与语言入口。
- 占位符登记表表头改为 `| Placeholder | Meaning | Files | Example |`；9 行内容的"含义"列取英文部分。
- 步骤表表头改为 `| ID | Kind | Step | How to verify |`；`必做 / Required` → `Required`，`选做 / Optional` → `Optional`；S01 ~ S09 的步骤与验证列取英文部分。
- 两条 `git grep` 命令一字不动。

## 4. `.github/chefs-pick/SETUP.zh-CN.md`（新建，中文译本）

- 覆盖 3 个章节，锚点序列与英文原文相同。
- `placeholders` 一节开头逐字照抄 language-structure §5，不复制登记表。
- `steps` 一节的 S01 ~ S09 用中文表格呈现，表头 `| 编号 | 类型 | 步骤 | 如何确认 |`，内容译自英文原文。步骤编号 `S01` ~ `S09` 与命令不译。

## 5. `.github/chefs-pick/GUIDE.md`（模块讲解，只有英文）

- 全文按 §0 通则改为纯英文。16 个模块标题 `## M01 项目说明 / README` → `## M01 README`。
- 每个模块的 `文件 / Files:` 行 → `Files:`；`级别 / Level:` → `Level:`；`必需 / Required` → `Required`。
- 小节标题 `### 为什么需要 / Why` → `### Why`；`### 如何定制 / Customize` → `### Customize`；`### 如何删除 / Remove` → `### Remove`。
- `### Remove` 下的三个条目：`- 删除文件 / Delete:` → `- Delete:`；`- 同步修改 / Update:` → `- Update:`；`- 失去什么 / What you lose:` → `- What you lose:`。这三项的中文正文删除，保留其后已有的英文段落；若英文段落遗漏了中文列出的引用方，按 §7 补齐。
- 附录标题：`## 按语言补充 / Adding language-specific rules` → `## Adding language-specific rules`；`## 固定动作版本 / Pinning actions` → `## Pinning actions`；`## 账号级默认文件 / Account-level default files` → `## Account-level default files`；`## 模板版本追溯 / Tracing the template version` → `## Tracing the template version`；`## 更换许可证 / Changing the license` → `## Changing the license`。
- 正文内指向这些小节的锚点链接（形如 `#更换许可证--changing-the-license`）必须同步改成新的英文锚点（`#changing-the-license`），否则 C14 会失败。
- **`## 中文译本 / Chinese translations` 一节按 §6 整体替换。**

## 6. `GUIDE.md` 的多语言 README 小节（FR-016）

把原 `## 中文译本 / Chinese translations` 替换为 `## Translating your own README`，内容必须包含：

1. 惯例做法：`README.md` 保持英文作为规范版本，另起 `README.zh-CN.md`，顶部放一行语言入口。给出可直接抄用的两行写法（与 language-structure §1 同形，但目标指向使用者自己的文件）。
2. 依据：点名采用同一做法的广泛项目（至少包含 dify、RAGFlow、LobeChat、SiYuan、Ant Design、RustDesk），并说明这些项目的根 README 都是英文规范版本。
3. 保留原表格中的官方译本链接，改为英文表头 `| File | Official Chinese translation |`，四行内容（`CODE_OF_CONDUCT.md`、`CHANGELOG.md`、Versioning、`CONTRIBUTING.md`）与 URL 不变。
4. 保留原有提示：替换译本时保留文件首行的来源注释。
5. 提醒这是本模板自己采用的做法，模板仓库本身就是示范。

## 7. `.github/chefs-pick/MAINTAINING.md`（维护说明，只有英文）

除按 §0 通则改为纯英文外，还有三处实质变化：

1. **补全发布门禁**（research R9）。这是全部 92 个小节中唯一英文明显短于中文的一处：现有英文只说 "All five gates must pass" 却从不列出门禁内容。改造后 `## Release gates` 必须用英文完整列出门禁，并按宪章 v2.1.0 变为 **6 条**：

   1. 全部认可度数据的核实日期不早于发布前 30 天；
   2. 从模板新生成的仓库核心要素齐全，首次 CI 通过；
   3. 占位符一次搜索全部找到；引导层之外无模板作者身份信息、模板版本历史或开发过程文件；执行清理命令后引导层被完整移除且无失效引用；
   4. 按起步清单完成定制后，社区标准自检页全部达标；
   5. 全部动作引用固定到提交哈希，工作流令牌默认只读；
   6. 全部译本与当前英文原文对齐。

   正文中原有的 "gate 2"、"gate 4" 编号引用保持指向同一条，不得因新增第 6 条而错位。

2. **新增译本维护小节** `## Keeping the translations in step`：说明译本只覆盖 README 与 SETUP；改动英文原文后运行 `python3 tools/check_template.py` 会以 `WARN` 提示哪份译本过期；更新译文后运行 `python3 tools/check_template.py --update-digests` 刷新来源标记；发布前 `--release` 会把过期的译本按 FAIL 处理。

3. **复核步骤第 4 步**受日期约束的位置仍是四处，不因本功能增减。

## 8. `.github/chefs-pick/SOURCES.md`（选型清单，只有英文）

- H1 → `# Selection list`；`数据核实日期 / Data verified:` → `Data verified:`。
- `## 选型规则 / Selection rules` → `## Selection rules`；六种证据类型的列表项去掉中文，保留 `Exact stars`、`Rounded stars`、`Estimated users`、`Official platform feature`、`De facto standard`、`Not available`。
- 16 个模块的字段表：表头 `| 字段 / Field | 内容 / Value |` → `| Field | Value |`；八个字段名改为 `Files`、`Level`、`Pick`、`Version`、`Upstream license`、`Evidence`、`Rule`、`Verified`；级别取值改为 `Required`/`Recommended`/`Optional`/`Optional (recommendation only)`。
- 每个模块删除 `**入选理由**` 中文段落，保留 `**Rationale**` 英文段落。
- `**备选方案 / Alternatives**` → `**Alternatives**`；各条目只保留英文部分。
- M12 的 `**Rationale**` 段落必须含 `comparable adoption` 字样（规则 2 的依据要求，C12 检查）。
- `## 排除的候选 / Excluded candidates` → `## Excluded candidates`；表头首格 `候选 / Candidate` → `Candidate`，其余两格 → `Adoption`、`Reason`；9 行理由只留英文。
- `## 认可度数据 / Adoption data` → `## Adoption data`；`<!-- adoption-data:start/end -->` 之间的 36 行表格**一字不动**。
- `## 数据说明 / About the data` → `## About the data`，删中文段留英文段。

## 9. `.github/chefs-pick/UPGRADE-TO-TEAM.md`（团队升级指引，只有英文）

- H1 → `# Growing into a team project`；两个小节标题取英文部分。
- 增强项表格表头 → `| Addition | Purpose | Source | Adoption |`，五行内容只留英文。
- "需要基金会级治理时"与"不再推荐"两节的条目改为纯英文，`认可度 / Adoption：` → `Adoption:`，`来源 / Source：` → `Source:`。
- 表中的 Star 数一字不动。

## 10. `.github/chefs-pick/CHANGELOG.md`（模板变更记录，只有英文）

- H1 → `# Template changelog`；删中文说明段，保留英文段。
- `### Added / 新增` → `### Added`。
- `## [1.0.0] - 2026-09-18` 下现有条目改为纯英文。
- 在 `## [Unreleased]` 下新增一条：

  ```markdown
  ### Changed

  - Documentation is now English-first: the guide layer is a single-language English edition, with Simplified Chinese supplied as separate `README.zh-CN.md` and `SETUP.zh-CN.md` files reached from a language selector. The previous side-by-side bilingual layout is gone.
  ```

- `## [Unreleased]` 与 `## [1.0.0] - 2026-09-18` 属版本标题，不加锚点也不受双语规则约束。

## 11. `.github/chefs-pick/LICENSE`（模板自身的许可证）

- MIT 正文（第 1 行到 `SOFTWARE.` 那一行）**一个字符都不得改动**，否则 GitHub 识别不出许可证类型。
- 删除末尾 `---` 之后的中文段落，保留其上的英文段落。
- `Copyright (c) 2026 Chef's Pick OSS Starter contributors` 必须仍在第 3 行（C11 原有断言，改造后由 C15 承担）。
