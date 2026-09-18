# 调研记录：主厨精选开源仓库起步模板

**对应规格**：[spec.md](./spec.md) ｜ **对应计划**：[plan.md](./plan.md)

**核实时间**：2026-09-18（本地时间；GitHub API 查询时间为 2026-09-17T16:55Z）

**核实方法**：
- 仓库数据：`gh api repos/<owner>/<repo>`（已登录账号，只读查询）；"默认分支最近提交"取自 `gh api repos/<owner>/<repo>/commits/<默认分支>` 返回的提交日期。
- 平台规则：GitHub Docs 文章接口 `https://docs.github.com/api/article/body?pathname=/en/...`。
- 上游内容：直接读取上游仓库文件，并记录固定的提交哈希。

本文件中的 Star 数都是 API 返回的精确整数。实施阶段写入模板前，必须用 `tools/verify_sources.py` 重新核实（宪章原则 III）。

## 1. 认可度数据快照

| 仓库 | Stars | Forks | 默认分支最近提交 | 许可证 | 已归档 | 在本项目中的用途 |
|---|---:|---:|---|---|---|---|
| github/gitignore | 175,810 | 82,184 | 2026-09-11 | CC0-1.0 | 否 | M03 选定来源 |
| othneildrew/Best-README-Template | 16,360 | 23,014 | 2026-04-18 | Unlicense | 否 | M01 选定来源 |
| RichardLitt/standard-readme | 6,367 | 2,507 | 2026-06-17 | MIT | 否 | M01 备选 |
| race2infinity/The-Documentation-Compendium | 6,036 | 739 | 2025-10-31 | 无 | 否 | M01 备选（原 kylelobo 名下） |
| Louis3797/awesome-readme-template | 1,861 | 437 | 2022-04-07 | CC0-1.0 | 否 | M01 备选（已停滞） |
| EthicalSource/contributor_covenant | 2,259 | 1,435 | 2026-05-20 | 仓库为 Hippocratic License；准则文本另有许可 | 否 | M04 选定来源 |
| olivierlacan/keep-a-changelog | 6,702 | 3,537 | 2026-09-03 | MIT | 否 | M09 选定来源 |
| semver/semver | 7,852 | 784 | 2025-11-05 | 无（CC BY 3.0 文本） | 否 | M09 选定来源 |
| actions/starter-workflows | 12,080 | 7,328 | 2026-08-03 | MIT | 否 | M11 结构参考 |
| actions/checkout | 8,882 | 2,779 | 2026-07-20 | MIT | 否 | M11 使用的动作 |
| github/choosealicense.com | 4,201 | 1,628 | 2026-09-10 | MIT | 否 | M02 选定来源 |
| spdx/license-list-data | 697 | 207 | 2026-09-16 | 无 | 否 | M02 许可证标识 |
| github/opensource.guide | 15,684 | 15,523 | 2026-09-04 | CC-BY-4.0 | 否 | M05 选定来源 |
| jessesquires/.github | 42 | 28 | 2023-03-26 | MIT | 否 | M05 备选（已停滞） |
| stevemao/github-issue-templates | 4,461 | 5,550 | 2024-03-20 | 未识别 | 否 | M07/M08 排除 |
| changesets/changesets | 12,405 | 832 | 2026-09-14 | MIT | 否 | M10 推荐 |
| orhun/git-cliff | 12,245 | 325 | 2026-09-13 | Apache-2.0 | 否 | M10 推荐 |
| googleapis/release-please | 7,505 | 589 | 2026-09-14 | Apache-2.0 | 否 | M10 推荐 |
| editorconfig/editorconfig | 3,450 | 119 | 2025-04-21 | 无 | 否 | M13 选定来源（已重新评估） |
| pre-commit/pre-commit | 15,581 | 1,010 | 2026-08-17 | MIT | 否 | M14 选定来源 |
| pre-commit/pre-commit-hooks | 6,681 | 798 | 2026-08-17 | MIT | 否 | M14 使用的钩子 |
| dependabot/dependabot-core | 5,772 | 1,524 | 2026-09-17 | MIT | 否 | M12 选定来源 |
| renovatebot/renovate | 22,523 | 3,315 | 2026-09-17 | AGPL-3.0 | 否 | M12 备选；升级指引 |
| ossf/scorecard | 5,694 | 724 | 2026-09-08 | Apache-2.0 | 否 | M11 依据；升级指引 |
| DavidAnson/markdownlint | 6,345 | 946 | 2026-07-28 | MIT | 否 | M11 备选 |
| rhysd/actionlint | 4,234 | 271 | 2026-04-19 | MIT | 否 | M11 备选 |
| super-linter/super-linter | 10,597 | 1,080 | 2026-09-17 | MIT | 否 | M11 备选 |
| zgosalvez/github-actions-ensure-sha-pinned-actions | 55 | 16 | 2026-09-05 | MIT | 否 | M11 备选 |
| golang-standards/project-layout | 56,601 | 5,425 | 2026-04-28 | 未识别 | 否 | 排除（反例） |
| cookiecutter/cookiecutter | 25,091 | 2,277 | 2026-03-04 | BSD-3-Clause | 否 | 排除（生成器） |
| copier-org/copier | 3,577 | 273 | 2026-09-07 | MIT | 否 | 排除（生成器） |
| cncf/project-template | 82 | 46 | 2026-08-11 | Apache-2.0 | 否 | 升级指引 |
| microsoft/repo-templates | 89 | 93 | 2026-08-24 | MIT | 否 | 升级指引 |
| dec0dOS/amazing-github-template | 710 | 259 | 2021-12-08 | MIT | 否 | 排除（已停滞，基于生成器） |
| maehr/github-template | 23 | 6 | 2026-03-06 | AGPL-3.0 | 否 | 排除（认可度低） |
| todogroup/repolinter | 465 | 74 | 2026-02-06 | Apache-2.0 | **是** | 排除（已归档） |
| ossf/best-practices-badge | 1,360 | 233 | 2026-09-15 | MIT | 否 | 升级指引（OpenSSF Best Practices Badge） |

**许可证列的两种口径**：
- 选型清单的机器可读数据表，与刷新脚本 `tools/verify_sources.py` 的输出保持一致，只写 GitHub API 返回的 `license.spdx_id`。API 返回 `NOASSERTION` 或空值时写 `unknown`。按这个规则，写 `unknown` 的仓库有：`race2infinity/The-Documentation-Compendium`、`EthicalSource/contributor_covenant`、`semver/semver`、`actions/starter-workflows`、`stevemao/github-issue-templates`、`editorconfig/editorconfig`、`golang-standards/project-layout`。
- 上表的"许可证"列，以及选型清单各模块的"上游许可证"字段，写的是查阅许可证文件后得到的实际许可证，例如 `actions/starter-workflows` 的 LICENSE 文件是 MIT。

其他认可度证据：
- **Contributor Covenant**：官方采用者名单（上游 `assets/adopters.csv`）收录 454 个项目，其中重点采用者 42 个，包括 .NET Foundation、Bootstrap、Bundler、Cloud Native Computing Foundation、CocoaPods、curl、Django、Elixir 等。
- **GitHub 平台功能**（Issue Forms、PR 模板、安全策略、私有漏洞报告、自动生成发布说明、Dependabot、CODEOWNERS、FUNDING、模板仓库）：证据类型为"平台官方功能"。

## 2. 决策

### R1 开发工作区与模板内容的布局

- **Decision**：模板仓库默认分支上的全部内容放在 `template/` 子目录；维护脚本放在 `tools/`；`.specify/`、`.claude/`、`specs/` 留在开发工作区。发布时只把 `template/` 的内容推送到公开模板仓库的默认分支 `main`，做法见 [quickstart.md](./quickstart.md)。
- **Rationale**：GitHub 从模板建仓库时，默认只复制默认分支（F6）；宪章原则 IV 禁止开发过程文件进入生成仓库。放在子目录里，本地开发、校验脚本和 Spec Kit 可以共存，也不依赖分支切换。
- **Alternatives**：
  - 同一仓库用两个分支：容易误操作；使用者勾选 "Include all branches" 时，开发文件仍会被复制。
  - 在起步清单里要求使用者删除开发文件：违反宪章原则 IV。
  - 改用脚手架生成器：违反宪章原则 V。

### R2 起步引导层

- **Decision**：
  - `template/.github/README.md` 作为模板首页介绍（双语）。GitHub 优先展示 `.github` 下的 README（F1）。
  - `template/.github/chefs-pick/` 存放起步清单、讲解、选型清单、维护说明、可选的团队升级指引，以及模板自身的变更记录和许可证。
  - 项目自身的 README 骨架放在 `template/README.md`。
  - 清理命令只有一条：`git rm -r .github/README.md .github/chefs-pick`。清理后，根目录的 README 自动成为首页。
- **Rationale**：FR-027 要求模板首页展示介绍和摘要表，而 GitHub 会把同样的文件复制到生成仓库，所以介绍一定会被复制。可行的做法是把它做成明确标注、可一步移除的引导层（宪章 v1.0.1 原则 IV）。借助 README 位置优先级，项目骨架从一开始就在正式位置，清理时只需删除，不必移动文件。
- **Alternatives**：
  - 根 README 放介绍，项目骨架放在别处：清理时要移动文件，容易出错。
  - 介绍和骨架写在同一个 README 里、用标记分隔：首页内容混杂，清理时要手动编辑。
  - 用 Actions 工作流自动清理：`GITHUB_TOKEN` 不能修改 `.github/workflows/`，工作流无法删除自己，会留下残留，而且需要写权限。

### R3 占位符格式

- **Decision**：统一使用 `CHANGEME_<NAME>` 格式，`<NAME>` 只含大写字母、数字和下划线。一条 `git grep -n CHANGEME` 即可找出全部占位符。完整登记表见 [contracts/markers.md](./contracts/markers.md)。
- **Rationale**：这种写法在 URL、YAML 普通标量、Markdown 和许可证文本中都合法。Markdown 中，单词内部的下划线不会触发强调。
- **Alternatives**：
  - `{{NAME}}`：YAML 会把 `{` 开头的值解析为映射，花括号在 URL 中也不合法。
  - `<NAME>`：Markdown 会把它当作 HTML 标签，渲染后消失。
  - `[NAME]`：在 URL 中不合法，在 Markdown 中可能被当作链接引用。
  - `__NAME__`：Markdown 会渲染成粗体。
  - 沿用上游各自的写法（`github_username`、`[INSERT CONTACT METHOD]`、`[fullname]`）：格式不统一，违反 FR-008。

### R4 行为准则版本

- **Decision**：采用 **Contributor Covenant 2.1** 英文原文，取自 `EthicalSource/contributor_covenant@7255a28d23d5bc296de2e4e4e9bb5ee1126f1345` 的 `content/version/2/1/code_of_conduct.md`。
  - 去掉站点使用的 TOML front matter（`+++` 包围的部分）。
  - 把 `[INSERT CONTACT METHOD]` 换成 `CHANGEME_CONDUCT_EMAIL`。
  - 原样保留 Attribution 段落。
  - 适用规则：第 1 级和第 2 级。
- **Rationale**：
  - 2.x 是采用最广的版本系列。GitHub 行为准则接口（`GET /codes_of_conduct/contributor_covenant`）目前返回的仍是 2.0；2.1 是 2.x 的最新版，并有官方简体中文译本。
  - 3.0（2025-07 发布）改用 **CC BY-SA 4.0**，修改后的准则须按相同方式共享，会给使用者增加合规负担，违反宪章附加约束。3.0 除了联系方式，还要求改写一整段执行说明，起步更费事。
  - 2.1 的许可证为 CC BY 4.0。依据：上游仓库 2016–2022 年的 `LICENSE.md`；2.1 文本自带 Attribution 段落，须原样保留。
- **Alternatives**：
  - 3.0：见上文。
  - 2.0：GitHub 接口提供的版本，已被 2.1 取代。
  - Django Code of Conduct：GitHub 接口提供的另一选项，采用面较窄。
- **复核触发**：3.0 的采用面明显扩大，或 GitHub 接口升级到 3.x 时，重新评估。

### R5 README 骨架

- **Decision**：以 `othneildrew/Best-README-Template@fc444eb7b04b2e4863f6080b1507a219e95103fa` 的 `BLANK_README.md` 为基础。它采用 Unlicense，无需署名。
  - 保留的章节：标题与简介、两个徽章（CI、许可证）、目录、About、Getting Started（Prerequisites、Installation）、Usage、Contributing、License、Contact（只放项目链接）。
  - 上游的 `github_username` 等占位符统一换成 `CHANGEME_*`。
  - 删除的内容：Built With、Roadmap、Acknowledgments、Top contributors 和社交链接。这些内容是项目专属的，且不属于核心要素，按宪章原则 V 精简。
  - 适用规则：第 1 级。
- **Rationale**：该模板是认可度最高的 README 模板，已知 Star 数远高于其他候选。
- **Alternatives**：
  - `RichardLitt/standard-readme`（6,367★）：规范性强，但需要额外的检查工具和章节约束。
  - `race2infinity/The-Documentation-Compendium`（6,036★）：没有许可证，不能安全复用。
  - `Louis3797/awesome-readme-template`（1,861★）：2022 年后没有更新。

### R6 贡献指南

- **Decision**：结构参考 GitHub Open Source Guides（`github/opensource.guide`，15,684★，CC-BY-4.0）的 "Writing your contributing guidelines" 和 GitHub Docs 的 "Setting guidelines for repository contributors"。正文是本项目原创的简洁英文，不复制上游文字，因此没有 CC BY 署名义务；来源注释仍注明参考来源。
- **Rationale**：原报告以 `jessesquires/.github` 为范例，社区依据偏弱；opensource.guide 由 GitHub 官方维护，认可度更高。适用规则：第 1 级。
- **Alternatives**：`jessesquires/.github`（42★，默认分支最近提交 2023-03-26，已超过 12 个月）降为参考。

### R7 安全策略

- **Decision**：采用 GitHub 安全策略加私有漏洞报告，两者都是官方功能。文件包含四部分：
  - 支持版本表。
  - 私下报告方式：Security 页的 "Report a vulnerability"，并附直达链接 `https://github.com/CHANGEME_OWNER/CHANGEME_REPO/security/advisories/new`。
  - 备用邮箱 `CHANGEME_SECURITY_EMAIL`。
  - 明确要求不要公开提交漏洞。

  起步清单把"开启私有漏洞报告"列为必做步骤（F4）。适用规则：第 1 级和第 2 级。
- **Alternatives**：只留邮箱或 PGP。需要交换密钥，起步更难。

### R8 Issue 表单

- **Decision**：采用 GitHub Issue Forms（官方功能）。
  - `bug_report.yml`：必填项为实际行为、复现步骤、期望行为、运行环境；选填项为日志；标签 `bug`。
  - `feature_request.yml`：必填项为要解决的问题、建议方案；选填项为备选方案、补充信息；标签 `enhancement`。
  - `config.yml`：关闭空白 Issue；`contact_links` 指向讨论区和私下报告漏洞入口。

  每个表单都必须有合法的 `name` 和 `description`，这是社区标准自检的要求（F2）。适用规则：第 1 级和第 2 级。
- **Alternatives**：
  - `stevemao/github-issue-templates`（4,461★）：默认分支最近提交 2024-03-20，早于 Issue Forms，排除。
  - Markdown 模板：无法强制必填。

### R9 合并请求模板

- **Decision**：采用 GitHub 官方的 `.github/PULL_REQUEST_TEMPLATE.md`，清单式，分三节：Description、Related issue、Checklist。
- **说明**：文件里的来源注释会随模板进入每个合并请求的描述（渲染时不可见），GUIDE 中会说明这一点。适用规则：第 1 级和第 2 级。
- **Alternatives**：多模板目录。个人项目不需要。

### R10 变更记录与发布说明

- **Decision**：
  - 根目录 `CHANGELOG.md` 遵循 Keep a Changelog **1.1.0** 和 SemVer 2.0.0。1.1.0 是当前已发布的版本，2.0.0 仍是未发布草稿（F7）。
  - 文件只包含 `## [Unreleased]` 一节（附示例条目 "Initial project structure."），以及 `[Unreleased]` 链接 `https://github.com/CHANGEME_OWNER/CHANGEME_REPO/commits/main`。
  - `.github/release.yml` 设三个分类：New Features（`enhancement`）、Bug Fixes（`bug`）、Other Changes（`*`）。
- **适用规则**：第 1 级。
- **复核触发**：Keep a Changelog 2.0.0 正式发布时。
- **Alternatives**：只用发布说明、不保留 CHANGELOG。与宪章原则 V 的核心要素清单冲突。

### R11 变更日志自动化（可选，只推荐）

- **Decision**：按项目类型推荐，默认一个都不启用：
  - Node 项目：changesets（12,405★，MIT）。
  - 非 Node 项目：git-cliff（12,245★，Apache-2.0/MIT，单一可执行文件）。
  - 采用 Conventional Commits 并希望自动发起发版合并请求：release-please（7,505★，Apache-2.0）。
- **Rationale**：对个人项目来说，平台自动生成的发布说明已经够用，而且零依赖。适用规则：第 1 级和第 2 级（三个工具各自是所属生态里认可度最高的，再按项目类型取舍）。

### R12 自动检查（CI）

- **Decision**：结构取自 `actions/starter-workflows` 的 `ci/blank.yml`（官方 "Simple workflow"，MIT），但文字为本项目原创。
  - 触发：推送到 `main`、以 `main` 为目标的合并请求、手动触发（`workflow_dispatch`）。
  - 权限：顶层 `permissions: contents: read`。
  - `lint` 作业：检出代码，并检查所有动作都已固定到完整提交哈希（用 grep 实现）。
  - `test` 作业：一个打印提示后成功退出的占位步骤。
  - `actions/checkout` 固定为 `3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1`，并设置 `persist-credentials: false`。

  模板生成的仓库沿用模板默认分支的名字，所以 `main` 在生成仓库中同样成立（F6）。
  - 适用规则：第 1 级和第 2 级。
- **Rationale**：官方起步模板认可度最高，在空仓库上一定能通过。哈希检查是唯一与语言无关、又直接落实 FR-039 的检查，而且不引入第三方动作。
- **Alternatives**：
  - super-linter（10,597★）：镜像庞大、运行慢，违反宪章原则 V。
  - markdownlint（6,345★）：README 骨架含 HTML，需要额外调整规则，容易误报，因此不作为默认。
  - actionlint（4,234★）：没有官方动作，需要下载脚本或使用 Docker。
  - `zgosalvez/github-actions-ensure-sha-pinned-actions`（55★）：认可度低，而且它本身又是一个需要信任的第三方动作。

### R13 依赖自动更新

- **Decision**：采用 Dependabot（GitHub 内置；`dependabot/dependabot-core` 5,772★）。配置为 `package-ecosystem: github-actions`、`directory: "/"`、每周一次。Dependabot 升级哈希时会同步更新行尾的版本注释（F8）。
- **Rationale**：适用规则第 2 级。Dependabot 与 Renovate 都是事实标准，认可度相当；Dependabot 由平台内置、不需要安装，起步更容易。
- **Alternatives**：Renovate（22,523★，AGPL-3.0，需要安装 App 并编写配置），放入团队升级指引。

### R14 忽略规则

- **Decision**：采用 `github/gitignore@356fd7baab4c05e092194a41f64dbd5afc8817e4` 的 Global 模板：`macOS`、`Windows`、`Linux`、`VisualStudioCode`、`JetBrains`。按原文拼接，每段前加一行分段注释。文件头注释说明如何按语言补充规则，并附 github/gitignore 链接。
- **Alternatives**：gitignore.io（Toptal）。依赖第三方服务，认可度不如官方集合。适用规则：第 1 级。

### R15 可选模块

四个可选模块都适用第 1 级：各自领域内没有认可度接近的候选。

- **`.editorconfig`**
  - 来源：EditorConfig（`editorconfig/editorconfig` 3,450★）。
  - 该仓库默认分支最近提交是 2025-04-21，已超过 12 个月，按宪章要求重新评估。结论是保留：规范本身稳定，主流编辑器原生或通过插件支持，活跃度低是因为已经稳定，不是停滞。
  - 关于 FR-014："可见的副作用"指在 GitHub 页面或协作流程中出现的效果。`.editorconfig` 只影响本地编辑器的空白与编码处理，因此不算可见副作用，无需使用者手动启用。与模板自身文本格式约定的关系：两者方向一致（UTF-8、LF、文件末尾保留换行、去掉行尾空格），唯一的差别是本文件沿用上游通行做法，对 `*.md` 放行行尾空格以保留 Markdown 的"行尾两空格换行"写法；模板自身的文件一律不使用该写法，C21 仍对 `template/` 下每个文件全量检查行尾空格，所以两者不冲突。`.pre-commit-config.yaml` 的 `--markdown-linebreak-ext=md` 同理。
  - 只设置通用项：UTF-8、LF 换行、文件末尾保留换行、去掉行尾空格（`*.md` 除外）、YAML 两空格缩进。
- **`.pre-commit-config.yaml`**
  - 来源：pre-commit（15,581★，MIT）和 pre-commit-hooks v6.0.0（6,681★，MIT）。
  - `rev` 写作 `3e8a8703264a2f4a69428a0aa4dcb512790b2c8c  # frozen: v6.0.0`。
  - 启用的钩子：`trailing-whitespace`（带 `--markdown-linebreak-ext=md` 参数）、`end-of-file-fixer`、`check-yaml`、`check-merge-conflict`、`check-added-large-files`。
  - 不运行 `pre-commit install` 就没有任何效果。
- **`.github/CODEOWNERS`**：所有行都是注释（示例为 `# * @CHANGEME_OWNER`），默认不生效。
- **`.github/FUNDING.yml`**：沿用 GitHub 设置页生成的官方格式，只保留 `github:` 和 `custom:` 两个键，值都留空，因此不会出现赞助按钮。

### R16 许可证

- **Decision**：
  - 根目录 `LICENSE`：取 `github/choosealicense.com@58267f8f2c5c0099810849cfd7677f52ae0c0eb3` 中 `_licenses/mit.txt` 的 MIT 原文，去掉 front matter，把 `[year]` 和 `[fullname]` 分别换成 `CHANGEME_YEAR` 和 `CHANGEME_COPYRIGHT_HOLDER`。不加来源注释。
  - 模板自身的许可证：放在 `.github/chefs-pick/LICENSE`，采用 MIT，版权人写 "Chef's Pick OSS Starter contributors"，不写个人姓名。
  - 在 `.github/README.md` 和上述 LICENSE 中声明：用本模板生成的项目无需保留模板署名。
- **Rationale**：满足 FR-010、FR-024 和 FR-036。GitHub 按根目录的 LICENSE 识别出 MIT；模板作者的署名只出现在起步引导层中。

### R17 模板版本追溯

- **Decision**：不在生成项目里留下任何版本标记。
  - GitHub 从模板生成的仓库只有一个初始提交（F6），用它的日期对照模板变更记录里的发布日期，就能判断基于哪个版本。
  - GUIDE 建议使用者在自己的 CHANGELOG 中记一笔 "Created from Chef's Pick OSS Starter vX.Y.Z"（可选）。
- **Alternatives**：
  - 保留一个版本文件：违反"干净骨架"。
  - 在来源注释里写模板版本：来源注释只写上游来源（FR-028）。

### R18 双语写法

- **Decision**：起步引导层中的每篇文档都按以下规则写：
  - 一级和各级标题写成"中文 / English"。
  - 每个标题下先写中文段落，再写英文段落。
  - 表格表头写双语；名称、数字和链接不重复。

  生成仓库中的协作文件和来源注释只用英文。
- **Rationale**：落实 FR-037 和宪章附加约束。中英内容相邻，维护时不容易漏改。

### R19 维护工具

- **Decision**：使用 Python 3.10+，只依赖标准库和 PyYAML。
  - `tools/check_template.py`：结构校验和发布门禁校验，包含清理模拟。
  - `tools/verify_sources.py`：通过 `gh api` 刷新认可度数据。
  - `tools/tests/`：`unittest` 测试。
- **Rationale**：本机（Python 3.14.6，PyYAML 6.0.3）和 GitHub 托管运行器都自带 Python 3。不需要引入 Node 依赖。
- **Alternatives**：
  - Bash：YAML 解析不可靠。
  - Node：额外依赖。
  - yq、actionlint、yamllint：本机未安装。

### R20 团队升级指引（可选，P4）

- **Decision**：只列条目和依据，不提供文件：
  - CODEOWNERS 的团队用法（官方功能）。
  - 分支保护或规则集（官方功能）。
  - Renovate（22,523★）。
  - pre-commit（15,581★）：个人版已作为可选模块提供，团队可在 CI 中强制执行。
  - OpenSSF Scorecard（5,694★）。
  - OpenSSF Best Practices Badge（`ossf/best-practices-badge` 1,360★，站点为 bestpractices.dev）。
  - `cncf/project-template`（82★，CNCF 官方）。
  - `microsoft/repo-templates`（89★，微软官方）。
- **说明**：`todogroup/repolinter` 已归档（465★），不再推荐。

### R21 排除清单

以下候选不采用，写入选型清单的"排除的候选"一节：
- `golang-standards/project-layout`（56,601★）：Go 团队明确表示它不是官方标准。
- `stevemao/github-issue-templates`（4,461★）：已被 Issue Forms 取代，默认分支自 2024-03-20 起没有新提交。
- `cookiecutter/cookiecutter`（25,091★）和 `copier-org/copier`（3,577★）：都是生成器，违反宪章原则 V。
- `cncf/project-template`（82★）：基金会级模板，只放进升级指引。
- `dec0dOS/amazing-github-template`（710★）：基于 cookiecutter，默认分支自 2021-12-08 起没有新提交。
- `maehr/github-template`（23★）：AGPL-3.0，认可度低。
- `jessesquires/.github`（42★）：降为参考范例。
- `todogroup/repolinter`：已归档。

## 3. 已核实的平台事实

| 编号 | 事实 | 出处 |
|---|---|---|
| F1 | 同一仓库有多个 README 时，按 `.github` → 根目录 → `docs` 的顺序展示第一个 | [About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) |
| F2 | 社区标准自检检查 README、CODE_OF_CONDUCT、LICENSE、CONTRIBUTING、安全策略、Issue 模板等；Issue Forms 必须有合法的 `name` 和 `description` 才算通过 | [About community profiles](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories) |
| F3 | 仓库自带合法的 Issue 模板或配置时，账号级 `.github/ISSUE_TEMPLATE` 全部不生效；不能创建默认 LICENSE；`FUNDING.yml` 必须放在 `.github` | [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) |
| F4 | 私有漏洞报告只能由公共仓库的所有者或管理员开启 | [Configuring private vulnerability reporting for a repository](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository) |
| F5 | 把动作固定到完整提交哈希，是目前唯一能把动作当作不可变版本使用的方式 | [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) |
| F6 | 从模板创建仓库时，默认只复制默认分支（可选 Include all branches）；新仓库只有一个提交 | [Creating a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) |
| F7 | Keep a Changelog 已发布的最新版本是 1.1.0；2.0.0 是未发布草稿 | 上游 `olivierlacan/keep-a-changelog` 的 `tools/version_routing.rb` |
| F8 | Dependabot 更新 GitHub Actions 时会维护行尾的版本注释 | 上游 `dependabot/dependabot-core` 的 `github_actions/lib/dependabot/github_actions/file_updater.rb`（VersionCommenter） |
| F9 | 讨论区需要在仓库设置中手动开启 | [Enabling or disabling GitHub Discussions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/enabling-or-disabling-github-discussions-for-a-repository) |
| F10 | "接受内容举报"（reported content）只能为组织账号拥有的公共仓库开启；社区档案接口包含 `content_reports_enabled` 字段 | [Managing how contributors report abuse](https://docs.github.com/en/communities/moderating-comments-and-conversations/managing-how-contributors-report-abuse-in-your-organizations-repository) |

模板文件的来源注释中要引用的 GitHub Docs 链接，均已在 2026-09-18 确认可以访问，完整清单见 [contracts/markers.md](./contracts/markers.md)。

## 4. 固定的上游版本

| 上游 | 引用 | 提交哈希 | 用于 |
|---|---|---|---|
| actions/checkout | v7.0.1（发布于 2026-07-20） | `3d3c42e5aac5ba805825da76410c181273ba90b1` | `.github/workflows/ci.yml` |
| pre-commit/pre-commit-hooks | v6.0.0 | `3e8a8703264a2f4a69428a0aa4dcb512790b2c8c` | `.pre-commit-config.yaml` |
| github/gitignore | main（2026-09-11） | `356fd7baab4c05e092194a41f64dbd5afc8817e4` | `.gitignore` |
| EthicalSource/contributor_covenant | release（2026-05-20） | `7255a28d23d5bc296de2e4e4e9bb5ee1126f1345` | `CODE_OF_CONDUCT.md` |
| github/choosealicense.com | gh-pages（2026-09-10） | `58267f8f2c5c0099810849cfd7677f52ae0c0eb3` | `LICENSE` |
| othneildrew/Best-README-Template | main（2026-04-18） | `fc444eb7b04b2e4863f6080b1507a219e95103fa` | `README.md` |

获取上游文件的命令模板：

```bash
gh api "repos/<owner>/<repo>/contents/<path>?ref=<commit-sha>" --jq .content | base64 -d
```

## 5. 复核触发器检查（宪章原则 III）

- **已归档**：`todogroup/repolinter`，从升级指引中移除。
- **默认分支最近提交超过 12 个月**（以 2026-09-18 为准；宪章原则 III 规定按"末次提交"判断，不按 `pushed_at`）：
  - `jessesquires/.github`（2023-03-26）：降为参考。
  - `stevemao/github-issue-templates`（2024-03-20）：排除。
  - `dec0dOS/amazing-github-template`（2021-12-08）：排除。
  - `Louis3797/awesome-readme-template`（2022-04-07）：仅作备选说明。
  - `editorconfig/editorconfig`（2025-04-21）：已重新评估，保留（见 R15）。
- **最新版本发布超过 12 个月，但仓库仍活跃**：`pre-commit/pre-commit-hooks` 的 v6.0.0 发布于 2025-08-09，默认分支最近提交为 2026-08-17，保留。
- **说明**：`pushed_at` 会因任何分支的推送而更新，因此按它判断会漏掉已停更的上游。例如 `jessesquires/.github` 的 `pushed_at` 是 2024-08-14，而默认分支最近提交是 2023-03-26。

## 6. 与原调研报告的差异

- **GitHub 内置行为准则版本**：GitHub 接口提供的是 Contributor Covenant 2.0，不是报告所说的 2.1。
- **Contributor Covenant 3.0 的许可证**：CC BY-SA 4.0，报告未提及。
- **Keep a Changelog 2.0**：仍未发布，当前版本是 1.1.0。
- **todogroup/repolinter**：已归档，报告写的是"维护中"。
- **jessesquires/.github**：42★，报告写约 6★；默认分支最近提交为 2023-03-26，已超过 12 个月。
- **The-Documentation-Compendium**：已迁到 `race2infinity` 名下，6,036★，没有许可证。
- **maehr/github-template**：许可证是 AGPL-3.0。
- **数字更新**（报告值 → 当前值）：
  - Best-README-Template：16.4k → 16,360
  - standard-readme：6.2k → 6,367
  - keep-a-changelog：6.4k → 6,702
  - starter-workflows：约 12.1k → 12,080
  - changesets：12.4k → 12,405
  - git-cliff：>10k → 12,245
  - release-please：7,505（报告未给出数字）
  - scorecard：5.4k → 5,694
  - golang-standards/project-layout：约 5.5 万 → 56,601
- **actions/checkout**：当前最新版本是 v7.0.1，报告的 starter-workflows 示例使用的是 v4。
- **OpenSSF Best Practices Badge**：仓库已从 `coreinfrastructure/best-practices-badge` 迁到 `ossf/best-practices-badge`（1,360★，MIT）。
- **内容举报**：GitHub 的"接受内容举报"设置只对组织账号的公共仓库开放，个人账号仓库没有这一项（见 F10）。
