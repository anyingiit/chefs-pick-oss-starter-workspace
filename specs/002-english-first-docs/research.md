# 研究与决策：英文为主、中文另起一份的文档语言结构

**对应**：[spec.md](./spec.md) 的 FR-001 ~ FR-018；宪章 v2.1.0「附加约束 · 文档语言」与「发布门禁」第 6 项。

本文件把规格中留给规划阶段的实现形态逐项定死。**实现任务不得在这些问题上自行判断**；与本文件不符时停下来报告，不要自行替换方案。

## 1. 现状基线（实测）

| 文件 | 字节 | 中文字符 | 英文字母 | 处置 |
|---|---:|---:|---:|---|
| `.github/README.md` | 10,319 | 1,034 | 4,633 | 改为纯英文，另起 `README.zh-CN.md` |
| `.github/chefs-pick/SETUP.md` | 8,137 | 694 | 4,198 | 改为纯英文，另起 `SETUP.zh-CN.md` |
| `.github/chefs-pick/GUIDE.md` | 44,914 | 5,041 | 20,945 | 改为纯英文 |
| `.github/chefs-pick/SOURCES.md` | 40,646 | 3,797 | 18,161 | 改为纯英文 |
| `.github/chefs-pick/MAINTAINING.md` | 10,626 | 1,508 | 4,190 | 改为纯英文 |
| `.github/chefs-pick/UPGRADE-TO-TEAM.md` | 4,140 | 388 | 2,145 | 改为纯英文 |
| `.github/chefs-pick/CHANGELOG.md` | 597 | 40 | 291 | 改为纯英文 |
| `.github/chefs-pick/LICENSE` | 1,433 | 132 | — | 改为纯英文（见 R1b） |
| **合计** | **120,812** | **12,634** | **54,563** | `template/` 文件数 26 → 28 |

英文侧完整性抽查：对 92 个含实质中文的小节做英/中密度比对，只有 1 个小节的英文明显短于中文——`MAINTAINING.md §发布门禁 / Release gates`（英/中比 0.71），其英文段落说了 "All five gates must pass" 却从未列出这 5 条。其余 91 个小节的英文已是完整对应，改造时直接保留即可（见 R9）。

## 2. 决策

### R1 译本的文件命名与位置

**决策**：`<NAME>.zh-CN.md`，与其英文原文**同目录**。

- `.github/README.md`（英文，规范版本）+ `.github/README.zh-CN.md`
- `.github/chefs-pick/SETUP.md`（英文，规范版本）+ `.github/chefs-pick/SETUP.zh-CN.md`

**理由**：`.zh-CN` 是 BCP 47 写法，也是取证样本中最常见的形式（LobeChat、思源笔记）。同目录保证两个语言版本到任何目标的相对路径深度一致，译本可以照抄英文原文的链接而不必逐条改写，也让 C14 的相对链接校验对两者用同一套规则。

**备选方案**：把中文首页放到 `.github/chefs-pick/README.zh-CN.md`，好处是清理命令一个字都不用改；否决理由是它与英文首页不同级，所有相对链接都要改写一遍，且"首页"藏进子目录不合直觉。

**清理命令的连带变化**：`.github/README.zh-CN.md` 在 `chefs-pick/` 之外，必须显式列入清理命令。新的逐字命令是

```bash
git rm -r .github/README.md .github/README.zh-CN.md .github/chefs-pick
```

仍然是**一条**命令，满足 FR-010 与宪章原则 IV 的"一步移除"。`SETUP.zh-CN.md` 在 `chefs-pick/` 内，被目录删除覆盖，不需要单独列出。

### R1b `.github/chefs-pick/LICENSE` 的处置

**决策**：改为纯英文，删去末尾那段中文说明。

**理由**：FR-003 禁止任何一份文档内并排两种语言，不限于 FR-006 列出的六份。该文件末尾现有一段英文说明加一段中文说明，属于并排。中文读者需要的信息（生成项目无需保留模板署名）在 `README.zh-CN.md` 的许可证一节中保留。

**注意**：MIT 正文本身不得改动，否则 GitHub 识别不出许可证类型；只删末尾 `---` 之后的中文段落。

### R2 章节锚点

**决策**：HTML 注释，单独成行，紧贴标题上方，中间不留空行。

```markdown
<!-- anchor: what-you-get -->
## What you get
```

- **id 字符集**：`[a-z0-9][a-z0-9-]*`，由英文标题转 kebab-case 得到，同一文档内唯一。
- **适用范围**：只有两个语言版本的那四个文件——`.github/README.md`、`.github/README.zh-CN.md`、`.github/chefs-pick/SETUP.md`、`.github/chefs-pick/SETUP.zh-CN.md`。代码块内的 `#` 行不算标题，不加锚点。
- **比对方式**：两个语言版本的锚点 id **有序序列**必须逐一相同。用有序序列而不是集合，是为了让重排章节也能被发现；译本本就应当镜像原文结构。
- **其余四份只有英文版的文档不加锚点**：没有比对对象，加了是纯噪音。后续若为某份文档新增译本，必须同时给它的英文原文补上锚点（FR-006）。

**理由**：HTML 注释在 GitHub 渲染后完全不可见（SC-013 要求可见字符数为 0），`grep` 一行正则即可取出，且不依赖任何 Markdown 扩展。GitHub 不支持 `{#id}` 这类标题属性语法，会原样渲染成可见文本，因此排除。

**备选方案**：中文版保留英文标题只译正文（锚点天然稳定，但中文文档读起来是半译）；按标题层级与顺序比对（零成本，但无法定位是哪一节，且重排必然误报）。两者均已在规格澄清第 6 问中记录并否决。

### R3 来源标记

**决策**：内容摘要，写成 HTML 注释，放在译本规范性声明的下一行。

```markdown
<!-- translation-of: README.md sha256:3f2a91c04b7e8d16 -->
```

- **摘要算法**：对英文原文文件的**完整字节**求 sha256，取十六进制前 16 位（64 位，足够）。
- **文件名**：只写同目录下英文原文的文件名，不写路径。
- **判定**：`check_template.py` 重新计算并比对。不一致时日常校验记为 `WARN`（不影响退出码），`--release` 下记为 `FAIL`（宪章发布门禁第 6 项）。
- **更新方式**：`python3 tools/check_template.py --update-digests` 把全部译本的摘要刷新为当前值。译者**改完译文之后**才运行它。

**理由**：提交哈希不可用——模板仓库的内容由 `git subtree split` 单向发布，同一份文件在开发工作区与模板仓库中的提交哈希不同，写进模板的哈希在模板仓库里无从校验。内容摘要只依赖文件字节，两处都能算出同一个值，且英文原文一改摘要必变，不存在"改了却忘了推进标记"的可能。人工版本号则完全依赖自觉，已否决。

### R4 语言入口的逐字写法

**决策**：行内文本链接，当前语言为粗体纯文本，其余语言为链接，中间用 ` · ` 分隔。放在 H1 标题下方，上下各空一行。

| 文件 | 逐字内容 |
|---|---|
| `.github/README.md` | `**English** · [简体中文](README.zh-CN.md)` |
| `.github/README.zh-CN.md` | `[English](README.md) · **简体中文**` |
| `.github/chefs-pick/SETUP.md` | `**English** · [简体中文](SETUP.zh-CN.md)` |
| `.github/chefs-pick/SETUP.zh-CN.md` | `[English](SETUP.md) · **简体中文**` |

**理由**：取证样本中 Ant Design（`… · English · [中文](./README-zh_CN.md)`）与 LobeChat（`**English** · [简体中文](./README.zh-CN.md)`）都用这种写法。不用徽章图片：徽章要从 shields.io 拉图，给模板引入一个外部图片依赖，与"零依赖"取向冲突，且图片挂掉时语言入口就消失了。

### R5 规范性声明的逐字写法

**决策**：译本中，紧接语言入口之后的引用块，随后是来源标记。

```markdown
> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。
```

`SETUP.zh-CN.md` 中把两处 `README.md` 换成 `SETUP.md`。英文版不放任何对应内容——英文本身就是规范版本，声明它是同义反复。

### R6 语言纯度的判定算法

两类文档的判定规则不同，必须都能由脚本确定性地跑出来。

**共同的预处理**（按顺序）：
1. 删除围栏代码块（``` 与 ``` 之间，含围栏行）；
2. 删除 HTML 注释（`<!--` 到 `-->`，含标记本身）；
3. 删除行内代码（一对反引号之间的内容）；
4. 删除 Markdown 链接的目标部分，即 `[文本](目标)` 中的 `(目标)`；
5. 删除裸 URL（`https?://` 开头到空白为止）；
6. 删除语言入口那一行（按 R4 的四个逐字串精确匹配）。

**英文版**：预处理后，中文字符（U+4E00–U+9FFF）数必须为 0。

**中文版**：预处理后，不得出现连续 6 个及以上的英文词。一个"英文词"指 `[A-Za-z][A-Za-z'’-]*`，词之间只隔空格或标点。阈值取 6 是为了放过产品名与专有名词——`GitHub Open Source Guides`（4 词）、`Insights → Community Standards`（3 词）、`Contributor Covenant 2.1`（2 词）都能通过，而一个真正的英文句子几乎不可能短于 6 词。

**理由**：中文版里必然出现英文标识符、命令、文件名、产品名与许可证标识（FR-002 已豁免），所以不能简单地"禁止英文字母"。以"连续英文词数"为判据，既能抓住成句的英文，又不会误伤这些必要成分。

### R7 逐字契约的数字漂移与防复发

**现状**：`specs/001-chefs-pick-starter/contracts/guidance-layer.md` §4.4 与 `template/` 之间有 12 个仓库的 Star 数不一致：

| 仓库 | 契约 | 模板 |
|---|---:|---:|
| `actions/checkout` | 8,882 | 8,884 |
| `actions/starter-workflows` | 12,080 | 12,082 |
| `changesets/changesets` | 12,405 | 12,408 |
| `dependabot/dependabot-core` | 5,772 | 5,773 |
| `github/choosealicense.com` | 4,201 | 4,202 |
| `github/gitignore` | 175,810 | 175,816 |
| `github/opensource.guide` | 15,684 | 15,685 |
| `googleapis/release-please` | 7,505 | 7,509 |
| `renovatebot/renovate` | 22,523 | 22,527 |
| `rhysd/actionlint` | 4,234 | 4,235 |
| `semver/semver` | 7,852 | 7,853 |
| `super-linter/super-linter` | 10,597 | 10,598 |

**成因**：`tools/verify_sources.py` 刷新数据时只回写 `template/` 下的三个文件（`SOURCES.md`、`.github/README.md`、`UPGRADE-TO-TEAM.md`），逐字契约无人同步；而 `check_template.py` 只校验 `template/` 目录，完全不看契约。于是每刷新一次数据，契约就再落后一次。

**决策**：以 `template/` 为准（那是真实发布出去的内容，且由 `verify_sources.py` 从 GitHub API 实时取得），把契约的 12 处改成模板的值；同时两侧同时堵住成因：

1. `verify_sources.py` 的写入目标增加逐字契约，刷新时一并更新其中的 `★ N (owner/repo)`；
2. 新增校验 **C23**，比对契约与 `template/` 中同一仓库的 Star 数，不一致即 FAIL。

**理由**：只补 12 个数字不解决问题——下一次 `--write` 会立刻重现同样的漂移（规格 FR-018 的原话）。两侧都动，才能既消除存量又阻断增量。

### R8 校验项的改造清单

| 编号 | 现状 | 改造 |
|---|---|---|
| C11 | 逐行检查引导层每个标题是否同时含中英文 | 整体重写为"语言结构"检查：英文版纯度、中文版纯度、语言入口存在且互指、锚点有序序列相同、译本含规范性声明。标题改为 `Language structure` |
| C12 | 字段标签、级别、证据类型、`数据核实日期 / Data verified:`、`## 排除的候选 / Excluded candidates`、`**入选理由**` 均为双语字面量 | 全部改为英文字面量（见 R11） |
| C13 | 清理模拟使用旧命令 | 改用 R1 的新命令；`README.zh-CN.md` 与 `SETUP.zh-CN.md` 一并纳入被删集合 |
| C22 | 删除模拟 | 同 C13，识别新增的两个译本文件 |
| C14 | 相对链接 | 无需改逻辑，但必须覆盖两个新文件；语言入口与规范性声明中的链接都要能解析 |
| C17 | 删除说明 | GUIDE 改为纯英文后，被检查的字面量随之改为英文 |
| C18 | 维护说明 | 除改英文外，还要求 §Release gates 完整列出 **6** 条门禁，并说明 `--update-digests` |
| C19 | 团队升级指引 | 改为纯英文 |
| C08 | 占位符登记表表头为双语字面量 | 改为英文（见 R11） |
| **C23** | 不存在 | 新增：逐字契约与 `template/` 的 Star 数一致（R7） |
| **C24** | 不存在 | 新增：译本来源标记与英文原文摘要一致。日常记 `WARN`，`--release` 记 `FAIL`（R3） |

**新增的 `WARN` 状态**：`check_template.py` 目前只有 PASS/FAIL/SKIP。C24 需要第四种结果。约定：输出行为 `WARN C24 <标题>`，问题逐条列在下面；汇总行改为 `Summary: <p> passed, <f> failed, <w> warned, <s> skipped`；`WARN` 不影响退出码，除非带 `--release`，此时 C24 直接按 FAIL 计。

### R9 `MAINTAINING.md` 的英文补全与门禁同步

`MAINTAINING.md §Release gates` 是全部 92 个小节中唯一英文明显短于中文的一处：中文列出 5 条门禁，英文只说 "All five gates must pass" 而从不列出是哪 5 条。改为纯英文后必须把这 5 条完整写成英文列表，并按宪章 v2.1.0 追加**第 6 条**"全部译本与当前英文原文对齐"，同时把"下面 5 项门禁 / All five gates" 改成 6 项。

这属于 FR-001 要求的"英文版必须完整自足"，不是规格 Out of Scope 所禁止的"借机重写论述"。

### R10 起步清单占位符登记表在译本中的处理

`SETUP.md` 保留唯一一张登记表。`SETUP.zh-CN.md` 保留同名同锚点的章节，但**不复制表格**，只写中文说明并链接到英文原文的该章节：

```markdown
<!-- anchor: placeholders -->
## 占位符

模板中的全部占位符登记在英文原文的 [Placeholders](SETUP.md#placeholders) 一节。那张表是唯一的一份，逐项列出占位符名称、含义、出现的文件和示例值；名称、路径和示例都是标识符，不作翻译。

替换时对照该表逐个处理，一个都不要漏下。清理起步引导层之前，用下面这条命令查找还没替换的占位符……
```

同理，`README.zh-CN.md` 的"主厨精选一览"一节不复制那张 16 行摘要表（它由 `verify_sources.py` 批量刷新），只写中文说明并链接到英文原文。这两处都由 FR-011 直接约束。

### R11 需要从双语改为英文的逐字字面量

`tools/check_template.py` 中所有含中文的字面量都要改。逐项对照：

| 位置 | 旧值 | 新值 |
|---|---|---|
| `GUIDANCE_HOME_TITLE` | `# Chef's Pick OSS Starter · 主厨精选开源仓库起步模板` | `# Chef's Pick OSS Starter` |
| `PLACEHOLDER_TABLE_HEADER` | `\| 占位符 / Placeholder \| 含义 / Meaning \| 出现的文件 / Files \| 示例 / Example \|` | `\| Placeholder \| Meaning \| Files \| Example \|` |
| `FIELD_LABELS` | `文件 / Files`、`级别 / Level`、`选定来源 / Pick`、`版本或提交 / Version`、`上游许可证 / Upstream license`、`认可度证据 / Evidence`、`取舍规则 / Rule`、`核实日期 / Verified` | `Files`、`Level`、`Pick`、`Version`、`Upstream license`、`Evidence`、`Rule`、`Verified` |
| 级别取值 | `必需 / Required`、`推荐 / Recommended`、`可选 / Optional`、`可选（只推荐）/ Optional (recommendation only)` | `Required`、`Recommended`、`Optional`、`Optional (recommendation only)` |
| 证据类型 | `精确 Star 数 / Exact stars` 等 6 个 | `Exact stars`、`Rounded stars`、`Estimated users`、`Official platform feature`、`De facto standard`、`Not available` |
| 反馈小节标题 | `## 反馈与联系 / Feedback and contact` | `## Feedback and contact` |
| 数据日期行 | `数据核实日期 / Data verified:` | `Data verified:` |
| 摘要表表头首格 | `模块 / Module` | `Module` |
| 字段表表头首格 | `字段 / Field` | `Field` |
| 理由段落标记 | `**入选理由**` 与 `**Rationale**` 两段 | 只保留 `**Rationale**` |
| 备选方案标记 | `**备选方案 / Alternatives**` | `**Alternatives**` |
| 规则 2 的措辞检查 | 正文须含 `认可度相当` | 正文须含 `comparable adoption` |
| 排除候选标题 | `## 排除的候选 / Excluded candidates` | `## Excluded candidates` |
| 排除表表头首格 | `候选 / Candidate` | `Candidate` |
| `IDENTITY_RE` | `(?i)chef'?s[ -]?pick\|主厨精选` | 保持不变——它用于检测模板作者身份是否泄漏进生成仓库，与文档语言无关，`主厨精选` 仍可能出现在中文译本里，必须继续识别 |

`.github/README.md` 的 16 行摘要表，模块名一列也从 `M01 项目说明 / README` 改为 `M01 README`，其余 15 行照此办理。

### R12 语言范围与后续扩展

本功能只做英文与简体中文。结构上不阻断扩展：新增一种语言时，只需新增 `<NAME>.<lang>.md`、把该语言登记进语言入口、给该文档的英文原文与新译本补上锚点。`check_template.py` 按文件名后缀发现译本，不写死语言列表。

## 3. 遗留与不做的事

- 不做自动翻译或机器翻译流水线。
- 不改动生成仓库中交付给使用者的任何文件（根目录 `README.md`、`LICENSE`、`CODE_OF_CONDUCT.md` 等），它们本来就是英文。
- 不借机重写文档论述。唯一的例外是 R9 所述的那一处英文补全，它是 FR-001 的直接要求。
- 认可度数据本身不在本功能中刷新；C23 只保证契约与模板一致，不保证两者都是最新的（那是宪章原则 III 与发布门禁 1 的职责）。
