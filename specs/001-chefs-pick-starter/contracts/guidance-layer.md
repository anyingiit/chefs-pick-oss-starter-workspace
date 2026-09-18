# 契约：起步引导层

对应需求：FR-004、FR-009、FR-012、FR-013、FR-018、FR-025 ~ FR-027、FR-029 ~ FR-034、FR-036 ~ FR-038、FR-039；宪章原则 I ~ III。决策依据：[research.md](../research.md) R2、R4 ~ R21。

## 0. 通用规则

- **双语写法**（R18，C11 检查）：
  - 引导层中每个 Markdown 文件的每一行标题（代码块外以 `#` 开头的行）都必须同时含有中文字符和英文字母，写法统一为"中文 / English"。
  - 两个例外：变更记录中形如 `## [1.0.0] - 2026-10-01` 或 `## [Unreleased]` 的版本标题，只含版本号和日期，不受双语规则约束；§4.3 的机器可读数据表表头保持英文，便于脚本解析。
  - 每个标题下先写中文，再写英文。
  - 表格表头写成双语；名称、数字和链接不重复。
- **占位符**：引导层中不得出现 `CHANGEME_*`，只有 `SETUP.md` 的占位符登记表例外。
- **链接**：
  - 指向项目文件时用相对路径（相对于当前文件）。
  - 指向引导层内其他文件时也用相对路径。
  - 指向开发工作区 `tools/` 的内容只能写成代码格式，不得写成链接，因为该目录不在模板仓库中。
- **数字格式**：Star 数统一写成 `★ 16,360 (owner/repo)`，带千分位逗号，括号内是仓库路径。`tools/verify_sources.py` 会按这个格式批量更新，C12 会逐一核对。

## 1. `.github/README.md`（模板首页）

必须依次包含以下标题，中英文部分逐字：

1. `# Chef's Pick OSS Starter · 主厨精选开源仓库起步模板`（C11 检查第一行标题）
   - 标题下写中英文各一段简介：各模块都选用社区公认的佼佼者，开箱即用，每项选择都注明来源和认可度。
   - 接着是一段引用块，中英文各一句："这是模板的起步引导页。你的项目说明在根目录的 `README.md`，完成起步并删除本页后，它会显示在这里。" 链接写成 `[README.md](../README.md)`。
2. `## 你会得到什么 / What you get`：按必需、推荐、可选三级列出文件，每个文件后附模块编号。
3. `## 主厨精选一览 / The picks at a glance`
   - 放一张 16 行的摘要表，用 `<!-- summary:start -->` 和 `<!-- summary:end -->` 包起来。
   - 表头：`| 模块 / Module | 选定来源 / Pick | 认可度 / Adoption | 核实日期 / Verified |`。
   - 16 行的逐字内容见 §4.5。
   - 表后附链接 `[完整选型清单 / Full selection list](chefs-pick/SOURCES.md)`。
4. `## 选型原则 / How we pick`：用中英文各写一遍三级取舍规则（与宪章原则 II 一致），并注明"只看 Star 数不够"。
5. `## 快速开始 / Quick start`：
   1. 点击 **Use this template** 创建仓库；
   2. 按 `[起步清单 / Setup checklist](chefs-pick/SETUP.md)` 完成定制；
   3. 查阅 `[模块讲解 / Module guide](chefs-pick/GUIDE.md)`。
6. `## 注意事项 / Good to know`，写明三点：
   - 本模板自带 Issue 表单，会让账号级 `.github` 仓库里的默认 Issue 模板整体失效（research F3）；
   - 私有漏洞报告和讨论区需要手动开启；
   - 从模板生成的仓库不会随模板自动更新，请关注模板变更记录，并附链接 `[CHANGELOG](chefs-pick/CHANGELOG.md)`。
7. `## 完成后清理 / Clean up when done`：先用中英文各一句说明作用，再给出下面这个 `bash` 代码块（C11 检查该命令字符串）：

   ```bash
   git rm -r .github/README.md .github/chefs-pick
   git commit -m "chore: remove template guide"
   ```

   之后说明网页操作方法：删除这个文件和 `.github/chefs-pick` 目录。
8. `## 反馈与联系 / Feedback and contact`（C11 检查这一标题），写明三点：
   - 根目录的 `CODE_OF_CONDUCT.md` 和 `SECURITY.md` 是供使用者定制的骨架，其中的联系邮箱、Issue 入口链接都是占位符，在模板仓库里不可用；
   - 本模板仓库自身的安全问题，请在 Security 标签页用 **Report a vulnerability** 私下报告；
   - 其他反馈请在本仓库提 Issue 或到 Discussions 讨论；涉及行为准则的严重问题，可使用 GitHub 的内容举报功能向 GitHub 举报（"接受内容举报"设置只对组织账号的公共仓库开放，见 research F10）。
9. `## 许可证 / License`：
   - 本模板以 MIT 发布，附 `[LICENSE](chefs-pick/LICENSE)`；
   - 由本模板生成的项目无需保留模板署名，可以自由替换版权人或更换许可证；
   - `CODE_OF_CONDUCT.md` 的正文属于 Contributor Covenant，采用 CC BY 4.0，须保留其 Attribution 段落。

## 2. `.github/chefs-pick/SETUP.md`（起步清单）

1. `# 起步清单 / Setup checklist`，下接中英文各一段说明：按顺序完成，大约 15 分钟。
2. `## 占位符 / Placeholders`
   - 收录 [markers.md](./markers.md) §1.2 登记表的全部行，表头逐字写作 `| 占位符 / Placeholder | 含义 / Meaning | 出现的文件 / Files | 示例 / Example |`。第 1 列和第 3 列里的占位符、文件路径都放在反引号中，C08 会解析这两列。
   - 给出两条搜索命令：
     - `git grep -n CHANGEME -- . ':(exclude).github/chefs-pick'`：清理前使用，排除本登记表；
     - `git grep -n CHANGEME`：清理后使用。
3. `## 步骤 / Steps`：一张表，列为 `| 编号 / ID | 类型 / Kind | 步骤 / Step | 如何确认 / How to verify |`，内容必须覆盖下列 9 步，顺序固定。

| ID | 类型 | 步骤要点（中英文都要写） | 如何确认 |
|---|---|---|---|
| S01 | 必做 / Required | 替换全部占位符，参见上面的登记表 | 清理前的搜索命令没有输出 |
| S02 | 必做 / Required | 在仓库首页 About（齿轮图标）中填写简介，可选填写 Topics。如果仓库属于组织账号，还要在 Settings → Moderation options → Reported content 中开启内容举报（个人账号仓库没有这个设置，见 research F10；社区档案接口含 `content_reports_enabled` 字段，页面是否列出这一项在 V4 中确认） | 仓库首页右侧显示简介；社区标准页上与仓库设置相关的项目都已完成 |
| S03 | 必做 / Required | 开启私有漏洞报告：Settings → Advanced Security → Private vulnerability reporting；附官方文档链接（markers §3） | Security 页出现 **Report a vulnerability** |
| S04 | 必做 / Required | 开启讨论区：Settings → General → Features → Discussions。如果不开启讨论区，就把两处都改成你自己的求助渠道：`.github/ISSUE_TEMPLATE/config.yml` 中的讨论区链接，以及 `CONTRIBUTING.md` 的 Questions 一节 | New issue 页面上的求助链接可以打开，且 `CONTRIBUTING.md` 指向的渠道与之一致 |
| S05 | 必做 / Required | 确认许可证：默认 MIT；要更换时，到 choosealicense.com 选好后替换 `LICENSE`，并同步修改 `README.md` 的 License 一节 | 仓库首页显示正确的许可证 |
| S06 | 必做 / Required | 按项目语言补充三项：`.gitignore` 规则（取自 github/gitignore）；`ci.yml` 的检查与测试步骤，新增的动作要固定到哈希（见 GUIDE 的"固定动作版本"一节）；`dependabot.yml` 的依赖生态 | 推送后 CI 通过 |
| S07 | 选做 / Optional | 逐个决定推荐和可选模块是否保留，删除方法见 GUIDE | 保留的可选模块都已按说明启用 |
| S08 | 必做 / Required | 清理起步引导层，运行 README 首页给出的清理命令 | 仓库首页显示你自己的 `README.md` |
| S09 | 必做 / Required | 最终验收 | Insights → Community Standards 各项都是绿勾；`git grep -n CHANGEME` 没有输出；CI 通过。自检页只会列出你的账号类型支持的项（例如内容举报只对组织账号的公共仓库出现），所以列出的项都应当能补齐 |

## 3. `.github/chefs-pick/GUIDE.md`（模块讲解）

1. `# 模块讲解 / Module guide`，下接中英文各一段，说明怎样使用本指南。
2. 每个模块一个二级标题，16 个都要有，写法如 `## M01 项目说明 / README`。每个模块下有三个三级标题：
   - `### 为什么需要 / Why`
   - `### 如何定制 / Customize`
   - `### 如何删除 / Remove`

   M10 是例外，三级标题改为 `### 如何选择 / How to choose`，内容是一张按项目类型推荐工具的表，并写明默认不启用任何工具。

   M01 ~ M03 的"如何删除"小节写"不建议删除 / Not recommended"，并说明原因。其余模块的"如何删除"小节必须写明三点：
   - 要删除哪些文件；
   - 按 [template-layout.md](./template-layout.md) §6，需要同步修改哪些项目文件（写出文件名，C17 检查）；
   - 删除后失去什么功能，以及社区标准自检中的哪一项会变为未完成。

   各模块的要点：

   | 模块 | 为什么需要 | 如何定制 | 删除时的特别说明 |
   |---|---|---|---|
   | M01 | 访客首先阅读的内容 | 替换占位符，补全 About 和 Usage；更换许可证时同步修改 License 一节 | — |
   | M02 | 没有许可证，别人不能合法使用你的代码；许可证无法通过账号级默认文件继承 | 填写年份和版权人；更换许可证时同步修改 README | — |
   | M03 | 避免把系统和编辑器产生的文件提交进仓库 | 从 github/gitignore 追加对应语言的规则 | — |
   | M04 | 明确参与规则，是社区标准自检项 | 填写举报邮箱；可附官方中文译本链接 | 修改 `README.md`、`CONTRIBUTING.md` 中的引用 |
   | M05 | 告诉别人怎样参与贡献 | 补充开发环境和测试命令；不使用讨论区时，同步修改 Questions 一节指向的渠道（与 S04 对应） | 修改 `README.md` 中的引用 |
   | M06 | 为漏洞报告提供私下渠道 | 填写备用邮箱；完成 S03；按需调整支持版本表 | 修改 `README.md`、`CONTRIBUTING.md` 中的引用；`config.yml` 中的安全链接只在开启私有漏洞报告后可用 |
   | M07 | 结构化收集问题；关闭空白 Issue；会覆盖账号级默认 Issue 模板 | 增删字段；改标签时同步修改 `release.yml` | 删除整个 `ISSUE_TEMPLATE` 目录后，空白 Issue 恢复，账号级默认模板重新生效；修改 `README.md` 中的两个链接 |
   | M08 | 给合并请求提供自检清单 | 调整清单项；说明第一行来源注释会进入每个合并请求的描述，但渲染时不可见 | 调整 `CONTRIBUTING.md` 中"填写模板"的措辞 |
   | M09 | 让人读得懂的变更历史，并让发布说明自动分类 | 在 Unreleased 下记录改动；发布时把 Unreleased 改成版本号；分类依赖默认标签 `bug` 和 `enhancement` | 删除 `CHANGELOG.md` 时，修改 `CONTRIBUTING.md` 和 `.github/PULL_REQUEST_TEMPLATE.md`；删除 `release.yml` 后，发布说明不再分类 |
   | M10 | 需要自动生成变更日志时使用 | 按项目类型选择：changesets、git-cliff 或 release-please | —（没有文件） |
   | M11 | 自动检查每次推送，并检查动作是否都已固定哈希 | 在标注位置添加 lint 和 test 步骤 | 修改 `README.md` 中的 CI 徽章；Dependabot 继续运行，但没有可更新的内容 |
   | M12 | 自动升级动作，保持安全 | 添加项目用到的依赖生态 | 删除后，已固定的哈希不再自动升级，需要手动维护 |
   | M13 | 统一编码、换行和缩进 | 按语言补充缩进规则 | 不影响其他文件。说明：它只影响本地编辑器的空白与编码处理，不会在 GitHub 页面或协作流程中产生可见效果，因此默认就启用（见 spec FR-014） |
   | M14 | 在提交前发现问题 | 安装 pre-commit 后运行 `pre-commit install` | 不影响其他文件 |
   | M15 | 自动请求代码审阅 | 取消注释，并填入所有者 | 不影响其他文件 |
   | M16 | 显示赞助按钮 | 为对应的键填写值 | 不影响其他文件 |

3. 其他二级标题，都必须有：
   - `## 按语言补充 / Adding language-specific rules`：说明如何补充 `.gitignore`、CI 步骤和 Dependabot 生态。
   - `## 固定动作版本 / Pinning actions`：说明以下几点：
     - 查询哈希的命令：`gh api repos/OWNER/ACTION/commits/vX.Y.Z --jq .sha`；
     - 引用写法：`uses: owner/action@<40 位哈希> # vX.Y.Z`；
     - Dependabot 升级哈希时会同时更新版本注释；
     - CI 会拦下没有固定哈希的引用；
     - 附安全使用参考链接（markers §3）。
   - `## 账号级默认文件 / Account-level default files`：说明账号级 `.github` 仓库的作用，以及两条规则：自带 Issue 表单会覆盖账号级默认模板；许可证不能由账号统一提供。附官方链接。
   - `## 中文译本 / Chinese translations`：列出 markers §3 中的四个中文链接，并说明协作文件默认用英文，中文项目可以自行替换。
   - `## 模板版本追溯 / Tracing the template version`：说明用仓库初始提交的日期对照模板变更记录；也可以在自己的 CHANGELOG 中记一笔所用的模板版本，这一步可选。
   - `## 更换许可证 / Changing the license`：到 choosealicense.com 选择许可证，替换 `LICENSE`，并修改 `README.md` 的 License 一节。

## 4. `.github/chefs-pick/SOURCES.md`（选型清单）

### 4.1 结构

1. `# 选型清单 / Selection list`
2. 一行数据核实日期，逐字格式：`数据核实日期 / Data verified: 2026-09-18`（C12 检查；刷新脚本会改写这一行的日期）。
3. `## 选型规则 / Selection rules`：写三级规则（与宪章原则 II 一致）、证据类型的六种写法（见 [data-model.md](../data-model.md)），以及复核周期（至少每 6 个月一次，每次发布前也要复核）。
4. `## 模块 / Modules`：按 M01 ~ M16 的顺序，每个模块一节，格式见 §4.2。
5. `## 排除的候选 / Excluded candidates`：表头为 `| 候选 / Candidate | 认可度 / Adoption | 排除理由 / Reason |`，行内容取自 research R21，至少 8 行。"认可度"列统一写成 `★ N (owner/repo)`，已归档的仓库在后面加注"已归档 / archived"；排除理由写成中英双语。
6. `## 认可度数据 / Adoption data`：机器可读的表格，格式见 §4.3。
7. `## 数据说明 / About the data`：说明数据的核实方式（GitHub API，Star 数为精确值）、非仓库证据的出处，以及维护说明所在的文件名 `MAINTAINING.md`（写成行内代码，不要写成链接：它与本文件同目录，但由 US4 创建，写成链接会让链接检查在 US2 阶段失败）。

### 4.2 每个模块一节（C12 检查字段是否齐全）

```markdown
### M04 行为准则 / Code of Conduct

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `CODE_OF_CONDUCT.md` |
| 级别 / Level | 推荐 / Recommended |
| 选定来源 / Pick | [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) |
| 版本或提交 / Version | 2.1（EthicalSource/contributor_covenant@7255a28） |
| 上游许可证 / Upstream license | CC-BY-4.0 |
| 认可度证据 / Evidence | 事实标准 / De facto standard：…；★ 2,259 (EthicalSource/contributor_covenant) |
| 取舍规则 / Rule | 1 + 2 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：（中文段落，依据 research 中对应的 R 节）

**Rationale**: (English paragraph)

**备选方案 / Alternatives**

- 名称 — 证据 — 未选原因（中文） / reason (English)
```

- 8 个字段标签必须与示例逐字一致。
- 级别只能写 `必需 / Required`、`推荐 / Recommended`、`可选 / Optional`。M10 写作 `可选（只推荐）/ Optional (recommendation only)`。

### 4.3 认可度数据表（机器可读）

```markdown
<!-- adoption-data:start -->
| Repo | Stars | Forks | Last commit | License | Archived | Verified |
|---|---:|---:|---|---|---|---|
| github/gitignore | 175,810 | 82,184 | 2026-09-11 | CC0-1.0 | no | 2026-09-18 |
<!-- adoption-data:end -->
```

- `Last commit` 写默认分支最近一次提交的日期，不是 `pushed_at`。宪章原则 III 按"末次提交"判断上游是否停更，而 `pushed_at` 会因任何分支的推送而更新。

- 每个在引导层中以 `★ N (owner/repo)` 形式出现过的仓库，都必须在这张表里有一行，并且 N 与 Stars 列相同（C12 检查）。
- 按 research §1 填写，共 36 行：M01 ~ M16 中引用的 27 个仓库，加上排除清单的 7 个，以及升级指引的 2 个（`microsoft/repo-templates`、`ossf/best-practices-badge`）。表中可以有暂时未被引用的仓库，反向不做要求。research §1 中其余仓库（如 `spdx/license-list-data`）不列。
- License 列只写 GitHub API 返回的 `license.spdx_id`；API 返回 `NOASSERTION` 或空值时写 `unknown`。哪些仓库写 `unknown`，见 research §1 的"许可证列的两种口径"。Archived 列只能写 `yes` 或 `no`。

### 4.4 各模块的字段取值

各模块的字段取值如下，全部来自 research，实施时照抄，不得改动。证据类型必须使用 [data-model.md](../data-model.md) 规定的双语标签；"上游许可证"一列只能写 SPDX 标识、`官方文档 / Official docs` 或 `未识别 / Unknown`；一个模块引用多个上游时，用 `；` 分隔多个取值。注意用 SPDX 的写法：`CC-BY-4.0`、`CC-BY-3.0`、`CC0-1.0`，不要写成 `CC BY 4.0`。

| 模块 | 选定来源（链接） | 版本或提交 | 上游许可证 | 认可度证据 | 规则 | 备选方案（证据；原因） |
|---|---|---|---|---|---|---|
| M01 | Best-README-Template（https://github.com/othneildrew/Best-README-Template） | othneildrew/Best-README-Template@fc444eb | Unlicense | 精确 Star 数 / Exact stars：★ 16,360 (othneildrew/Best-README-Template) | 1 | standard-readme：精确 Star 数 ★ 6,367 (RichardLitt/standard-readme)，需要额外的检查工具和章节约束；The-Documentation-Compendium：精确 Star 数 ★ 6,036 (race2infinity/The-Documentation-Compendium)，没有许可证；awesome-readme-template：精确 Star 数 ★ 1,861 (Louis3797/awesome-readme-template)，2022 年后没有更新 |
| M02 | choosealicense.com 的 MIT（https://choosealicense.com/licenses/mit/），SPDX `MIT` | github/choosealicense.com@58267f8 | MIT | 平台官方功能 / Official platform feature：GitHub 运营的许可证选择器；精确 Star 数 / Exact stars：★ 4,201 (github/choosealicense.com) | 1 | 其他 OSI 许可证：未取得 / Not available；交接文档已把 MIT 定为默认，使用者可以自行更换 |
| M03 | github/gitignore 的 Global 模板（https://github.com/github/gitignore） | github/gitignore@356fd7b | CC0-1.0 | 精确 Star 数 / Exact stars：★ 175,810 (github/gitignore) | 1 | gitignore.io 在线服务：未取得 / Not available；依赖第三方服务 |
| M04 | Contributor Covenant 2.1（https://www.contributor-covenant.org/version/2/1/code_of_conduct/） | 2.1（EthicalSource/contributor_covenant@7255a28） | CC-BY-4.0 | 事实标准 / De facto standard：官方采用者名单收录 454 个项目，包括 .NET Foundation、Bootstrap、Cloud Native Computing Foundation、curl、Django；精确 Star 数 / Exact stars：★ 2,259 (EthicalSource/contributor_covenant) | 1 + 2 | Contributor Covenant 3.0：事实标准 / De facto standard，采用 CC BY-SA 4.0，并要求改写执行说明；Contributor Covenant 2.0：平台官方功能 / Official platform feature，已被 2.1 取代；Django Code of Conduct：平台官方功能 / Official platform feature，采用面较窄 |
| M05 | GitHub Open Source Guides（https://opensource.guide/starting-a-project/）+ GitHub Docs（markers §2.2 中 CONTRIBUTING 行的链接） | 只参考结构，正文为原创 | CC-BY-4.0（未复制文字） | 精确 Star 数 / Exact stars：★ 15,684 (github/opensource.guide)；平台官方功能 / Official platform feature：GitHub Docs | 1 | jessesquires/.github：精确 Star 数 ★ 42 (jessesquires/.github)，默认分支最近提交为 2023-03-26，已超过 12 个月 |
| M06 | GitHub 安全策略与私有漏洞报告（链接见 markers §2.2、§3） | — | 官方文档 / Official docs | 平台官方功能 / Official platform feature | 1 + 2 | 只提供邮箱或 PGP：未取得 / Not available；需要交换密钥，起步更难 |
| M07 | GitHub Issue Forms（链接见 markers §2.2） | — | 官方文档 / Official docs | 平台官方功能 / Official platform feature | 1 + 2 | stevemao/github-issue-templates：精确 Star 数 ★ 4,461 (stevemao/github-issue-templates)，早于 Issue Forms，2024-03-20 之后没有提交；Markdown 模板：平台官方功能 / Official platform feature，无法强制必填 |
| M08 | GitHub 合并请求模板（链接见 markers §2.2） | — | 官方文档 / Official docs | 平台官方功能 / Official platform feature | 1 + 2 | stevemao/github-issue-templates：精确 Star 数 ★ 4,461 (stevemao/github-issue-templates)，理由同上；多模板目录：平台官方功能 / Official platform feature，个人项目不需要 |
| M09 | Keep a Changelog 1.1.0（https://keepachangelog.com/en/1.1.0/）+ Semantic Versioning 2.0.0（https://semver.org/spec/v2.0.0.html）+ GitHub 自动生成的发布说明（链接见 markers §2.2） | KaC 1.1.0（2.0.0 仍是未发布草稿）；SemVer 2.0.0 | MIT；CC-BY-3.0；官方文档 / Official docs | 精确 Star 数 / Exact stars：★ 6,702 (olivierlacan/keep-a-changelog)、★ 7,852 (semver/semver)；平台官方功能 / Official platform feature：自动生成的发布说明 | 1 | 只用发布说明、不保留 CHANGELOG：平台官方功能 / Official platform feature，会缺少核心要素；Keep a Changelog 2.0.0：事实标准 / De facto standard，尚未发布 |
| M10 | changesets（https://github.com/changesets/changesets）、git-cliff（https://github.com/orhun/git-cliff）、release-please（https://github.com/googleapis/release-please） | 由使用者选定 | MIT；Apache-2.0 或 MIT；Apache-2.0 | 精确 Star 数 / Exact stars：★ 12,405 (changesets/changesets)、★ 12,245 (orhun/git-cliff)、★ 7,505 (googleapis/release-please) | 1 + 2 | GitHub 自动生成的发布说明：平台官方功能 / Official platform feature，即 M09 的默认方案；零依赖，个人项目通常已够用 |
| M11 | actions/starter-workflows 的 Simple workflow（https://github.com/actions/starter-workflows/blob/main/ci/blank.yml）+ actions/checkout（https://github.com/actions/checkout） | actions/checkout@3d3c42e（v7.0.1） | MIT；MIT | 精确 Star 数 / Exact stars：★ 12,080 (actions/starter-workflows)、★ 8,882 (actions/checkout)；固定哈希的依据：平台官方功能 / Official platform feature（GitHub Docs 安全使用参考）与精确 Star 数 / Exact stars ★ 5,694 (ossf/scorecard) | 1 + 2 | super-linter：精确 Star 数 ★ 10,597 (super-linter/super-linter)，镜像庞大、运行慢；markdownlint：精确 Star 数 ★ 6,345 (DavidAnson/markdownlint)，README 含 HTML，容易误报；actionlint：精确 Star 数 ★ 4,234 (rhysd/actionlint)，没有官方动作；github-actions-ensure-sha-pinned-actions：精确 Star 数 ★ 55 (zgosalvez/github-actions-ensure-sha-pinned-actions)，认可度低，且要额外信任一个第三方动作 |
| M12 | GitHub Dependabot（链接见 markers §2.2） | — | MIT（dependabot-core） | 平台官方功能 / Official platform feature；精确 Star 数 / Exact stars：★ 5,772 (dependabot/dependabot-core) | 2 | Renovate：精确 Star 数 ★ 22,523 (renovatebot/renovate)，需要安装 App 并编写配置，许可证为 AGPL-3.0 |
| M13 | EditorConfig（https://editorconfig.org） | — | 未识别 / Unknown | 精确 Star 数 / Exact stars：★ 3,450 (editorconfig/editorconfig)；复核说明：默认分支最近提交为 2025-04-21，已按宪章原则 III 重新评估并保留 | 1 | 无同类候选：未取得 / Not available；各编辑器的私有配置不能跨编辑器使用 |
| M14 | pre-commit（https://pre-commit.com）+ pre-commit-hooks（https://github.com/pre-commit/pre-commit-hooks） | pre-commit-hooks@3e8a870（v6.0.0） | MIT；MIT | 精确 Star 数 / Exact stars：★ 15,581 (pre-commit/pre-commit)、★ 6,681 (pre-commit/pre-commit-hooks) | 1 | 原生 Git 钩子脚本：未取得 / Not available；无法共享，也不受版本管理 |
| M15 | GitHub CODEOWNERS（链接见 markers §2.2） | — | 官方文档 / Official docs | 平台官方功能 / Official platform feature | 1 | 无同类候选：未取得 / Not available；这是平台内置功能 |
| M16 | GitHub 赞助按钮（链接见 markers §2.2） | — | 官方文档 / Official docs | 平台官方功能 / Official platform feature | 1 | 在 README 中手写赞助链接：未取得 / Not available；这样不会显示仓库的赞助按钮 |

- 备选方案的未选原因要写成中英双语。
- 取舍规则的写法（`1`、`2`、`3`、`1 + 2`）见 data-model.md 的"取舍规则的写法"。使用 `2` 时，入选理由必须写明"认可度相当"的判定依据：M12 要写成"Dependabot 与 Renovate 都是事实标准，认可度相当；Dependabot 由平台内置、不需要安装，起步更容易 / Both are de facto standards with comparable adoption; Dependabot is built into the platform and needs no installation"。

### 4.5 首页摘要表的 16 行（逐字）

`.github/README.md` 第 3 节两个 summary 标记之间，除表头和分隔行外，必须依次是以下 16 行。"核实日期"一列写当次数据核实日期，初次写入为 `2026-09-18`，之后由 `tools/verify_sources.py` 统一刷新。

```markdown
| M01 项目说明 / README | Best-README-Template | ★ 16,360 (othneildrew/Best-README-Template) | 2026-09-18 |
| M02 许可证 / License | choosealicense.com（MIT） | 平台官方功能 / Official platform feature | 2026-09-18 |
| M03 忽略规则 / Ignore rules | github/gitignore（Global） | ★ 175,810 (github/gitignore) | 2026-09-18 |
| M04 行为准则 / Code of Conduct | Contributor Covenant 2.1 | 事实标准 / De facto standard（454 adopters） | 2026-09-18 |
| M05 贡献指南 / Contributing guide | GitHub Open Source Guides | ★ 15,684 (github/opensource.guide) | 2026-09-18 |
| M06 安全策略 / Security policy | GitHub 安全策略 + 私有漏洞报告 | 平台官方功能 / Official platform feature | 2026-09-18 |
| M07 Issue 表单 / Issue forms | GitHub Issue Forms | 平台官方功能 / Official platform feature | 2026-09-18 |
| M08 合并请求模板 / Pull request template | GitHub 合并请求模板 | 平台官方功能 / Official platform feature | 2026-09-18 |
| M09 变更日志与发布说明 / Changelog & release notes | Keep a Changelog 1.1.0 + SemVer 2.0.0 | ★ 6,702 (olivierlacan/keep-a-changelog) | 2026-09-18 |
| M10 变更日志自动化 / Changelog automation | changesets、git-cliff、release-please（只推荐） | ★ 12,405 (changesets/changesets) | 2026-09-18 |
| M11 自动检查 / Continuous integration | actions/starter-workflows 的 Simple workflow | ★ 12,080 (actions/starter-workflows) | 2026-09-18 |
| M12 依赖自动更新 / Dependency updates | GitHub Dependabot | 平台官方功能 / Official platform feature | 2026-09-18 |
| M13 编辑器格式配置 / EditorConfig | EditorConfig | ★ 3,450 (editorconfig/editorconfig) | 2026-09-18 |
| M14 提交前检查 / Pre-commit hooks | pre-commit + pre-commit-hooks | ★ 15,581 (pre-commit/pre-commit) | 2026-09-18 |
| M15 代码负责人 / Code owners | GitHub CODEOWNERS | 平台官方功能 / Official platform feature | 2026-09-18 |
| M16 赞助入口 / Funding | GitHub 赞助按钮 | 平台官方功能 / Official platform feature | 2026-09-18 |
```

## 5. `.github/chefs-pick/MAINTAINING.md`（维护说明）

必须包含以下二级标题：

- `## 复核周期 / Review cadence`：至少每 6 个月一次；每次发布前也要复核，发布时所有数据的核实日期不得早于发布前 30 天。
- `## 复核步骤 / How to review`，写明四步：
  1. 在开发工作区运行 `python3 tools/verify_sources.py --write`，写成代码格式，并注明 `tools/` 不在模板仓库中。没有开发工作区时，对认可度数据表中的每个仓库运行两条命令：`gh api repos/OWNER/REPO --jq '.stargazers_count, .forks_count, .archived, .default_branch'`，以及 `gh api repos/OWNER/REPO/commits/DEFAULT_BRANCH --jq .commit.committer.date`（取默认分支最近一次提交，不用 `pushed_at`）。
  2. 手动复核非仓库证据：平台官方功能是否仍然存在；Contributor Covenant 的采用者数量用 `gh api "repos/EthicalSource/contributor_covenant/contents/assets/adopters.csv?ref=release" --jq .content | base64 -d | tail -n +2 | wc -l` 重新统计，数量变化时同步修改 M04 的证据和首页摘要表。
  3. 检查是否出现重新评估的触发条件。
  4. 更新核实日期。
- `## 重新评估的触发条件 / Re-evaluation triggers`：照抄宪章原则 III 的 3 个触发条件（末次提交超过 12 个月、依赖已被广泛弃用的工具、出现认可度明显更高的候选），写明"末次提交"以默认分支最近一次提交为准、仓库已归档视同满足第 1 条，并说明怎样按三级规则重新取舍。
- `## 动作版本更新 / Action updates`：说明模板仓库上的 Dependabot 合并请求只当作"有新版本"的提示，不要直接在模板仓库合并。正确做法是在开发工作区更新 `template/` 中的哈希和版本注释，以及逐字契约与 research 中记录的固定版本，跑完校验后重新发布；模板仓库的内容更新后，对应的合并请求会自动关闭。直接在模板仓库合并会让下一次发布推送被拒绝，因为发布是单向的。
- `## 变更记录规则 / Recording changes`：选型变更必须在同一次改动中同时更新 `SOURCES.md` 和 `[CHANGELOG.md](CHANGELOG.md)`，用 Added、Changed、Removed 分类，并写明原因。
- `## 发布门禁 / Release gates`：列出宪章中的 5 项门禁，并写明门禁必须在创建 Release **之前**全部通过。自动检查命令为 `python3 tools/check_template.py --release`，写成代码格式；门禁 2 中"首次自动检查通过"和门禁 4"社区标准全绿"要用从模板生成的测试仓库人工验证，步骤见开发工作区中 quickstart 的 C 部分。

## 6. `.github/chefs-pick/UPGRADE-TO-TEAM.md`（可选，P4）

- **标题**：`# 升级为团队项目 / Growing into a team project`。
- **开头说明**：中英文各一句，说明本页是可选的简要参考，5 分钟内可以读完。
- **`## 常用增强项 / Common additions`**：一张表，表头为 `| 增强项 / Addition | 作用 / Purpose | 来源 / Source | 认可度 / Adoption |`，行内容如下：
  - CODEOWNERS 的团队用法（平台官方功能）；
  - 规则集（平台官方功能，附 markers §3 的链接）；
  - Renovate（★ 22,523 (renovatebot/renovate)）；
  - pre-commit（★ 15,581 (pre-commit/pre-commit)）：个人版已作为可选模块 M14 提供，团队可以在 CI 中强制执行；
  - OpenSSF Scorecard（★ 5,694 (ossf/scorecard)）。
- **`## 需要基金会级治理时 / When you need foundation-level governance`**：列出以下三项：
  - cncf/project-template（★ 82 (cncf/project-template)，CNCF 官方）；
  - microsoft/repo-templates（★ 89 (microsoft/repo-templates)）；
  - OpenSSF Best Practices Badge（★ 1,360 (ossf/best-practices-badge)，站点为 https://bestpractices.dev）。
- **`## 不再推荐 / No longer recommended`**：todogroup/repolinter（★ 465 (todogroup/repolinter)，已归档）。
- **来源 / Source 一列的取值**（不得自行编造）：仓库类条目写 `https://github.com/<slug>`，`<slug>` 取本行括号中的仓库名；平台官方功能写官方文档链接——CODEOWNERS 用 markers §2.2 中 `.github/CODEOWNERS` 来源注释里的那条链接，规则集用 markers §3 的"规则集"链接；OpenSSF Best Practices Badge 写 https://bestpractices.dev 。
- **首页链接**：本页存在时，`.github/README.md` 的"快速开始"一节末尾要加一行 `（可选）项目发展为多人协作后，参阅 [升级为团队项目 / Growing into a team project](chefs-pick/UPGRADE-TO-TEAM.md)`。这一行由创建本页的同一个任务添加；不实施 US5 时，首页不得出现这个链接，否则相对链接检查会失败。

## 7. `.github/chefs-pick/CHANGELOG.md`（模板自身的变更记录，逐字）

```markdown
# 模板变更记录 / Template changelog

本文件记录 Chef's Pick OSS Starter 模板自身的变更。

This file records changes to the Chef's Pick OSS Starter template itself.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] / 未发布

### Added / 新增

- 首个版本：16 个模块（M01–M16）、起步引导层和选型清单。 / First version: 16 modules (M01–M16), the setup guide layer, and the selection list.
```

发布时，维护者把 `## [Unreleased] / 未发布` 改为 `## [1.0.0] - YYYY-MM-DD`（Keep a Changelog 的标准写法，只含版本号和日期，按 §0 的例外不受双语规则约束），并在上方新增一个空的 `## [Unreleased] / 未发布` 节。

## 8. `.github/chefs-pick/LICENSE`（模板自身的许可证，逐字加附注）

1. 正文与 [project-files.md](./project-files.md) 中的 M02 相同，但第 3 行写为 `Copyright (c) 2026 Chef's Pick OSS Starter contributors`。
2. 正文之后空一行，写 `---`，再空一行，然后写下面两段附注：
   - `Note: Projects generated from the Chef's Pick OSS Starter template are not required to retain this copyright and permission notice. You may replace the copyright holder in your project's LICENSE or choose a different license. Upstream content keeps its own license: CODE_OF_CONDUCT.md is Contributor Covenant 2.1 (CC BY 4.0) and must keep its Attribution section.`
   - `说明：由 Chef's Pick OSS Starter 模板生成的项目无需保留本版权和许可声明，可以替换项目 LICENSE 中的版权人，也可以改用其他许可证。上游内容仍适用其原有许可证：CODE_OF_CONDUCT.md 为 Contributor Covenant 2.1（CC BY 4.0），须保留其 Attribution 段落。`
