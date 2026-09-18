# 原始输入：`/speckit-specify`（2026-09-17）

> 本文件逐字保存用户调用 `/speckit-specify` 时提供的完整输入（交接文档 + 报告 1 + 报告 2 + 最终请求），作为 [spec.md](./spec.md) 的来源记录，也是规划阶段的数据依据。
> 原文中的 Star 数等认可度数据核实于 2026-09-17，写入模板前须重新核实并更新核实日期。

---

# chefs-pick-oss-starter 项目背景（交接给 Claude Code）

本文件总结了用户在 claude.ai 上与 Claude 的完整对话，帮助 Claude Code 了解这个项目的来龙去脉。随附两份调研报告的完整版，细节以报告为准：

- **报告 1**：《GitHub 仓库模板"主厨精选"深度调研报告》
- **报告 2**：《GitHub 仓库模板"主厨精选"深度调研报告（修订版）》

报告 2 只重写了"个人小项目"场景。它的"团队/组织项目"和"大型开源项目"两节只写了"沿用原报告"，完整内容要看报告 1。两份报告的数据核实日期都是 2026-09-17。

---

## 1. 项目是什么

`chefs-pick-oss-starter`（主厨精选开源仓库起步模板）是一个 GitHub 模板仓库。它把开源社区里各个模块公认的佼佼者预先挑好、拼好，让个人项目和团队项目开箱即用地拥有一个完整仓库的全部核心要素。开源贡献者不必再处理这些琐事，只需专注于自己的想法和创作。

## 2. 为什么做

用户最初想找的是一个"主厨精选"式的模板仓库：文件成套、功能全、社区认可度高，并且包含"一个好的仓库应该有什么"的讲解和实际填好的示范。

深度调研（报告 1）的结论是：**不存在这样的单一仓库**。星数最高的模板仓库只覆盖一部分需求，例如 othneildrew/Best-README-Template 只做 README，cookiecutter 只是脚手架引擎。成套的模板仓库星数都很低：cncf/project-template 81 星，microsoft/repo-templates 87 星，概念上最接近的 dec0dOS/amazing-github-template 约 700 星。

但是，**各个模块的佼佼者已经基本有明确答案**。它们贡献活跃、使用人数多，有些已经是事实标准，例如 github/gitignore、Contributor Covenant、Keep a Changelog。

本项目要填补的就是这个空白：使用者不必自己去搜集每个模块谁是佼佼者，也不必费力把它们拼接起来。

## 3. 核心原则（用户明确提出）

1. **选择必须有社区依据，而不是作者的一厢情愿。** 依据包括 Star 数、被成功开源项目实际采用的程度、是否已成为事实标准。只看星数不够：golang-standards/project-layout 约有 5.5 万星，但 Go 团队明确表示它不是官方标准，本项目不采用也不推荐它。
2. **选择优先级：** 先看社区认可度；认可度相当时，选对仓库持有者来说更容易起步的那个。
3. **多个选项同样合格时**，允许按作者个人喜好选择。
4. **每个模块都要标注来源**，以及大致使用人数（估算）或 Star 数，帮助使用者建立信任。
5. **服务对象**是个人项目和团队项目的快速起步。
6. **个人小项目不使用重型模板，但要"麻雀虽小，五脏俱全"**，Issue 模板、PR 模板、CHANGELOG 等都要有。这是用户审阅报告 1 时专门提出的修改意见，报告 2 据此重写了个人小项目方案。

## 4. 命名

- **仓库名（用户已选定）**：`chefs-pick-oss-starter`
  - `chefs-pick`：主厨精选，每个模块都经过挑选
  - `oss`：开源软件
  - `starter`：起步用，开箱即用
- **以下为 Claude 的建议，用户尚未确认：**
  - README 标题：`Chef's Pick OSS Starter · 主厨精选开源仓库起步模板`
  - About 描述：*Chef's pick starter for open-source repos — community-proven best-of-breed essentials, ready to use.*
  - Topics：`template`、`starter`、`open-source`、`best-practices`、`community-health`、`github-template`

## 5. 模块选型

### 5.1 核心方案（来自报告 2 的个人小项目方案）

认可度数据来自报告，核实日期为 2026-09-17。

| 模块 | 文件 | 选定来源 | 认可度 | 级别 |
|---|---|---|---|---|
| README | `README.md` | othneildrew/Best-README-Template（用其 `BLANK_README.md`）；备选 RichardLitt/standard-readme | 16.4k 星；备选 6.2k 星 | 必需 |
| 许可证 | `LICENSE` | choosealicense.com + SPDX 标识，默认 MIT | GitHub 官方 | 必需 |
| 忽略规则 | `.gitignore` | github/gitignore | 约 17.5 万星 | 必需 |
| 行为准则 | `CODE_OF_CONDUCT.md` | Contributor Covenant（最新为 3.0，GitHub 网页内置模板为 2.1） | 官网称被全球最大 10 个开源项目中的 9 个采用 | 推荐 |
| 贡献指南 | `CONTRIBUTING.md` | GitHub 官方文档；参考范例 jessesquires/.github（作者鼓励复用） | 官方文档；范例仅约 6 星 | 推荐 |
| 安全策略 | `SECURITY.md` | GitHub 私有漏洞报告（Private Vulnerability Reporting）+ 精简 SECURITY.md | GitHub 官方 | 推荐 |
| Issue 模板 | `.github/ISSUE_TEMPLATE/bug_report.yml`、`feature_request.yml`、`config.yml` | GitHub 官方 Issue Forms（YAML） | GitHub 官方 | 推荐 |
| PR 模板 | `.github/PULL_REQUEST_TEMPLATE.md` | GitHub 官方格式，清单式 | GitHub 官方 | 推荐 |
| 变更日志 | `CHANGELOG.md`、`.github/release.yml` | Keep a Changelog + SemVer；默认搭配 GitHub 自动生成 Release Notes | Keep a Changelog 6.4k 星 | 推荐 |
| 变更日志自动化 | 视工具而定 | Node 项目用 changesets；非 Node 用 git-cliff；需要自动开发版 PR 时用 release-please | changesets 12.4k 星；git-cliff 超过 1 万星；release-please 由 googleapis 维护 | 可选 |
| CI | `.github/workflows/ci.yml` | actions/starter-workflows（lint + test） | 约 12.1k 星，GitHub 官方 | 推荐 |
| 依赖更新 | `.github/dependabot.yml` | GitHub Dependabot，先管理 `github-actions` 生态 | GitHub 官方 | 推荐 |
| 其他 | `.editorconfig`、pre-commit、`CODEOWNERS`、`.github/FUNDING.yml` | 按需 | — | 可选 |

需要留意的几处：

- **贡献指南的社区依据偏弱。** 官方文档有权威性，但参考范例 jessesquires/.github 星数很低，是按实用性入选的。可能需要补充更有说服力的来源。
- **stevemao/github-issue-templates**（约 4.4k 星）在报告 1 中被推荐给团队项目，但报告 2 已将其降级为"仅作参考"：它更新不活跃，而且 GitHub 已原生支持 Issue Forms。
- 各文件的最小可用写法和示例 YAML（`config.yml`、`release.yml`、`dependabot.yml`、PR 模板）见报告 2。

### 5.2 目标目录结构（来自报告 2）

```
my-small-project/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   └── config.yml
│   ├── workflows/
│   │   └── ci.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── dependabot.yml
│   └── release.yml
├── .editorconfig            # 可选
├── .gitignore
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── SECURITY.md
```

### 5.3 团队及更大型项目的补充（来自报告 1）

- **骨架参考**：dec0dOS/amazing-github-template（约 700 星，基于 Cookiecutter，适合参考写法而非直接照搬），或 microsoft/repo-templates（87 星，微软全组织的默认文件集）。
- **在核心方案之上增加**：`CODEOWNERS`、pre-commit、dependabot 或 renovate。
- **质量门禁**：ossf/scorecard（5.4k 星）、todogroup/repolinter。
- **基金会级或需要治理结构的项目**：cncf/project-template（81 星，但是 CNCF 官方模板，含 GOVERNANCE、MAINTAINERS）、DSACMS/repo-scaffolder；目标是拿到 OpenSSF Best Practices Badge。

### 5.4 语言相关脚手架（来自报告 1，是否纳入尚未决定）

- **Python**：cookiecutter-uv（1,319 星）、cookiecutter-pypackage（4,587 星）、cookiecutter-data-science（10.0k 星）、scientific-python/cookie（409 星）。cookiecutter-hypermodern-python 自 2023 年 7 月起已停滞，不建议使用。
- **JS/TS**：gjuchault/typescript-library-starter；tsdx（11.5k 星）状态不稳定，采用前需确认。
- **Go**：golang-templates/seed（566 星）；目录布局遵循官方的 go.dev/doc/modules/layout。
- **Rust**：cargo-generate 加社区模板，目前没有绝对主导的选项。

## 6. 已知注意事项

- **账号级 `.github` 仓库的覆盖规则。** 只要某个仓库自己的 `.github/ISSUE_TEMPLATE` 里有任何文件（包括 `config.yml`），使用者账号级 `.github` 仓库里的默认 Issue 模板就会全部失效。本模板生成的仓库自带 ISSUE_TEMPLATE，因此会覆盖这些默认模板，README 中应说明这一点。另外，LICENSE 不能作为账号默认文件下发。
- **私有漏洞报告需要手动开启。** 如果 SECURITY.md 引导用户使用私有漏洞报告按钮，使用者必须先在仓库设置中开启该功能，否则按钮不会出现。
- **Star 数是动态数据。** 报告中部分数字是四舍五入值，个别没有取到（如 repolinter、部分 TS starter）。对话中零散出现的数字以报告为准。写进仓库前应重新核实，并注明核实日期。
- **上游许可证。** 本仓库会收录或改写上游文件，需要逐一核对上游许可证并按要求署名。例如 Contributor Covenant 采用知识共享（CC）署名类许可，使用时要保留署名。

## 7. 尚未决定的事项

以下事项请先与用户确认，不要自行假设：

- 个人版和团队版如何组织：同一个模板加可选文件、分两个目录，还是做成两个模板仓库。
- 是否包含语言相关的脚手架，还是只提供语言无关的核心文件。
- 模块来源和 Star 数写在哪里（例如单独的来源清单文件、README 中的表格、各文件头部注释），以及是否需要定期更新这些数字。
- 本仓库自身使用什么许可证。
- 文档语言：中文、英文还是双语。
- 第 4 节中 README 标题、About 描述和 Topics 的建议是否采用。

## 8. 建议的开工顺序

1. 阅读本文件和两份报告。
2. 就第 7 节的待定事项与用户确认。
3. 用 GitHub API 或 `gh` 重新核实各模块的 Star 数和维护状态，记录核实日期。
4. 按第 5 节创建文件，为每个模块标注来源和认可度数据。
5. 在 GitHub 仓库设置中勾选 "Template repository"，并用 Insights → Community Standards 页面自检。

---

## 附：对话历程

1. **一个好仓库需要哪些文件。** 分为必备（README、LICENSE、.gitignore）、协作相关（CONTRIBUTING、CODE_OF_CONDUCT、SECURITY、Issue/PR 模板、CODEOWNERS）、工程质量（CI、dependabot、CHANGELOG、锁文件、代码风格配置、tests、docs）和按需添加（.env.example、Makefile、Dockerfile、.gitattributes、CITATION.cff、SUPPORT.md、FUNDING.yml）四类。
2. **社区公认的单文件标准。** 包括 github/gitignore、choosealicense.com 与 SPDX、Contributor Covenant、Keep a Changelog、语义化版本、Conventional Commits、CITATION.cff、OpenSSF Scorecard 等。
3. **成套的模板仓库。** 推荐了 cncf/project-template、microsoft/repo-templates、google/new-project。
4. **含讲解和示范的模板。** 推荐了 DSACMS/repo-scaffolder、The Good Docs Project、The-Documentation-Compendium。
5. **"主厨精选"。** 推荐了 scientific-python/cookie 和 cncf/project-template，用户认为星数太低。
6. **深度调研，产出报告 1。** 结论是不存在单一的主厨精选仓库，改为提供按模块组合的菜单，并按个人、团队、基金会级场景给出推荐。
7. **用户审阅报告 1，产出报告 2。** 用户要求个人小项目方案"麻雀虽小，五脏俱全"，报告 2 据此重写了该场景。
8. **用户决定自建本项目。** 说明了项目目的和选型原则，经过两轮命名讨论，选定 `chefs-pick-oss-starter`。


----

# GitHub 仓库模板"主厨精选"深度调研报告

## TL;DR
- **不存在**一个星数很高（>5,000 星）、同时满足"成套已填好的社区健康文件 + 内嵌'为什么需要每个文件'讲解"的单一"主厨精选"仓库。星数最高的模板仓库要么只做 README（othneildrew/Best-README-Template，16.4k 星），要么是通用脚手架引擎（cookiecutter/cookiecutter，25.1k 星）；概念上最接近你需求的 dec0dOS/amazing-github-template 只有约 700 星。这是一个真实的生态缺口。
- 因此正确策略是**组一套"功能强大的菜单"**：用真正被大规模采用的"事实标准"单件（github/gitignore 约 17.5 万星、Contributor Covenant、Keep a Changelog 6.4k 星）拼装，再按语言选一个高认可度的完整脚手架（Python 用 cookiecutter-pypackage / cookiecutter-uv，Go 用 golang-templates/seed 等）。
- 你之前不满意的 scientific-python/cookie（409 星）和 cncf/project-template（81 星）星数确实低，但要注意：**星数 ≠ 权威性**——cncf/project-template 是 CNCF 官方基金会级模板；反例是 golang-standards/project-layout 有约 5.5 万星，却被 Go 官方明确否认为"标准"。

## Key Findings

1. **没有单一完美选项。** 高星模板仓库都只覆盖你需求的一部分。"填好的成套文件 + 内嵌教学讲解"这一组合，在 >5,000 星这一档是空白。

2. **概念上最接近的单一仓库是 dec0dOS/amazing-github-template（约 700 星）**：它捆绑了 README、LICENSE、CONTRIBUTING、CODE_OF_CONDUCT、SECURITY、Issue/PR/Actions 模板，并在 README 中解释每个文件为什么重要（引用 "Readme Driven Development" 理念）。缺点是星数低、内容偏可配置模板而非"填满的示范项目"。

3. **"事实标准"单件的采用率远比模板仓库的星数更有说服力：**
   - **github/gitignore**：约 175.7k 星（star-history.com 记录 "175.7k stars, 1.7k contributors"；Gitstar Ranking 交叉核对为 175,578 星、全球仓库排名第 30）、约 82k fork——GitHub 上最受欢迎的模板集合之一，几乎所有项目的 .gitignore 都源于此。数字为四舍五入快照，非精确 API 整数。
   - **Contributor Covenant**：其官网明确写 "It's been adopted by thousands of communities, including 9 of the 10 largest open source projects in the world."（被数千个社区采用，包括全球最大 10 个开源项目中的 9 个）。Wikipedia 列出具体采用者 "Linux, Swift, Go, and JRuby"，企业签署方包括 "Apple, Microsoft, Intel, Eclipse and GitLab"；是 GitHub 新建 CODE_OF_CONDUCT 时的内置选项。
   - **Keep a Changelog**：6.4k 星、3.6k fork，CHANGELOG 写法的通用参照，正在筹备 2.0。

4. **要警惕"名字像官方、其实不是"的陷阱**：golang-standards/project-layout 有约 5.5 万星（DEV Community 分析原文 "55k stars, zero blessing from the Go team"），org 名带 "standards"，但 Go 团队从未背书。2021 年 4 月 9 日 Go 技术负责人 Russ Cox 在 issue #117（标题 "this is not a standard Go project layout"）逐字写道：*"The README makes clear that this is not official, but even the claim 'it is a set of common historical and emerging project layout patterns in the Go ecosystem' is not accurate. For example, the vast majority of packages in the Go ecosystem do not put the importable packages in a pkg subdirectory. More generally what is described here is just very complex, and Go repos tend to be much simpler."* 该争论曾登上 Hacker News 首页。对小项目而言照搬它反而有害。

5. **Python 生态是完整脚手架最成熟的**：cookiecutter-pypackage（4,587 星，2026-03 仍活跃）、cookiecutter-data-science（10.0k 星）、cookiecutter-uv（1,319 星，采用 uv/ruff 现代工具链）都活跃；但经典的 cookiecutter-hypermodern-python（1,916 星）末次提交停在 2023-07，已被 uv-forge 取代——采用需注意。

## Details

### 一、为什么"主厨精选"不存在（结论论证）
用户想要的是三合一：(1) 成套文件；(2) 内嵌"每个文件为什么/写什么"的讲解；(3) 已填好的示范而非空模板；且高认可度。调研显示：
- 星数最高的两个（cookiecutter/cookiecutter 25.1k、Best-README-Template 16.4k）都不满足 (1)(2)：前者是模板引擎，后者只做 README 且内容是占位示例。
- 满足 (1)(2) 的仓库（cncf/project-template 81 星、microsoft/repo-templates 87 星、dec0dOS/amazing-github-template 约 700 星）星数都远低于 5,000。
- 且这些成套仓库多用 TODO 占位符而非"填满内容"，与用户"要填好的示范"要求有落差。

因此本报告给出"菜单 + 按场景组合"的方案。

### 二、菜单表（核实日期：2026-09-17，数据来自各仓库 GitHub 页面；k 为四舍五入，精确整数处已标注）

**A. 通用社区健康文件 / 事实标准单件**

| 名称 | 链接 | 类别 | Star | 维护状态 | 采用情况 | 优缺点 |
|---|---|---|---|---|---|---|
| github/gitignore | github.com/github/gitignore | .gitignore 模板集 | 约 175.7k | 活跃 | 事实标准，几乎全网采用 | 优：权威、覆盖全语言；缺：只是 .gitignore |
| Contributor Covenant | contributor-covenant.org（EthicalSource/contributor_covenant）| 行为准则 | — | 活跃 | 全球最大 10 个 OSS 中 9 个 | 优：GitHub 内置、40+ 语言翻译；缺：仅 CoC |
| olivierlacan/keep-a-changelog | github.com/olivierlacan/keep-a-changelog | CHANGELOG 规范 | 6.4k | 活跃（2.0 筹备）| 通用参照 | 优：清晰规范；缺：需手动维护 |
| dec0dOS/amazing-github-template | github.com/dec0dOS/amazing-github-template | 成套仓库模板+讲解 | 约 700 | 较活跃 | 中小项目 | 优：最接近"主厨精选"；缺：星数低、非填满示范 |
| cncf/project-template | github.com/cncf/project-template | 基金会级成套模板 | 81 | 活跃 | CNCF 官方 | 优：权威、每文件带 TODO 指引；缺：占位符、星低 |
| microsoft/repo-templates | github.com/microsoft/repo-templates | 组织默认模板 | 87 | 维护中 | 微软全组织 | 优：企业实战默认值；缺：无教学讲解 |
| jessesquires/.github | github.com/jessesquires/.github | 个人 .github 范例 | 约 6 | 活跃 | 常被博客引用 | 优：真实范例；缺：非通用高星模板 |

**B. README 模板**

| 名称 | 链接 | Star | 维护状态 | 优缺点 |
|---|---|---|---|---|
| othneildrew/Best-README-Template | github.com/othneildrew/Best-README-Template | 16.4k（23k fork）| 活跃（v1.1.2, 2024-12）| 优：最高星、美观、含 BLANK 模板；缺：仅 README、Unlicense |
| RichardLitt/standard-readme | github.com/RichardLitt/standard-readme | 6.2k | 活跃 | 优：规范 + linter；源于 IPFS 实践 |
| kylelobo/The-Documentation-Compendium | github.com/kylelobo/The-Documentation-Compendium | 约 5.1k | 低活跃 | 优：多种 README 模板 + 写作 tips |
| Louis3797/awesome-readme-template | github.com/Louis3797/awesome-readme-template | 1.9k | 基本停滞 | 缺：纯占位内容 |

**C. Issue/PR 模板**

| 名称 | 链接 | Star | 维护状态 | 说明 |
|---|---|---|---|---|
| stevemao/github-issue-templates | github.com/stevemao/github-issue-templates | 4.3–4.5k | 活跃 | Issue/PR/安全模板合集 |

**D. 完整项目脚手架（按语言）**

| 名称 | 语言 | Star | 维护状态 | 备注 |
|---|---|---|---|---|
| cookiecutter/cookiecutter | 通用引擎 | 25.1k | 活跃 | 脚手架生成引擎本身 |
| copier-org/copier | 通用引擎 | 3.5k | 活跃（v9.17.1, 2026-08）| 支持 `copier update` 增量更新，现代替代 |
| drivendataorg/cookiecutter-data-science | Python/数据 | 10.0k | 活跃 | 数据科学项目事实标准 |
| audreyfeldroy/cookiecutter-pypackage | Python | 4,587 | 活跃（2026-03）| 经典 Python 包模板 |
| pyscaffold/pyscaffold | Python | 2.3k | 活跃（v4.6, 2025-09）| `putup` 命令行生成器 |
| cookiecutter-hypermodern-python | Python | 1,916 | 停滞（2023-07）| 已被 uv-forge 取代，慎用 |
| cookiecutter-uv | Python | 1,319 | 活跃（2026-04）| uv/ruff 现代工具链 |
| ionelmc/cookiecutter-pylibrary | Python | 1,299 | 活跃（2026-04）| 多环境 tox 强 |
| scientific-python/cookie | Python | 409 | 非常活跃 | 科学计算，11 种后端，支持 copier/cookiecutter/cruft |
| golang-templates/seed | Go | 566 | 活跃 | Go 仓库模板，CI/Makefile/VS Code 完整 |
| jaredpalmer/tsdx | TS | 11.5k | 半停滞后 2.0 重写 | 零配置 TS 包 CLI |
| gjuchault/typescript-library-starter | TS | — | 活跃 | Biome、Node 原生 test runner |
| alexjoverm/typescript-library-starter | TS | — | 老牌 | Rollup/Jest（部分工具已过时）|

**E. 仓库质量检查工具**

| 名称 | 链接 | Star | 维护状态 | 说明 |
|---|---|---|---|---|
| ossf/scorecard | github.com/ossf/scorecard | 5.4k（v5.4.0, 2025-11）| 活跃 | 安全健康自动评分（工具，非模板）|
| todogroup/repolinter | github.com/todogroup/repolinter | — | 维护中 | 检查缺失文件/规则 |
| OpenSSF Best Practices Badge | bestpractices.dev | — | 活跃 | 自评徽章，被大项目使用 |
| DSACMS/repo-scaffolder | github.com/DSACMS/repo-scaffolder | 48 | 活跃 | 美国联邦 OSS 分层 cookiecutter + 检查清单 |

### 三、争议与注意事项标注
- **golang-standards/project-layout（约 5.5 万星）：非官方、有争议。** Go 团队从未背书，Russ Cox 明确反对（见 Key Findings 第 4 点）；社区另建 go-standard/project-layout 反制。小项目照搬会过度工程化——官方指引 go.dev/doc/modules/layout 主张"从简单开始"。
- **cookiecutter-hypermodern-python（1,916 星）：已停止活跃开发（末次提交 2023-07），作者建议迁移到 uv-forge。**
- **Best-README-Template 使用 Unlicense**，商用/署名需求者注意。
- **tsdx（11.5k 星）**长期低活跃后推出 2.0 重写（基于 Rust 工具链），采用前确认其稳定性。

## Recommendations

**分场景推荐组合：**

1. **个人小项目（任意语言）**
   - README 用 othneildrew/Best-README-Template（16.4k 星，最省心）；
   - .gitignore 用 github/gitignore；
   - LICENSE 用 choosealicense.com 选 MIT；
   - 直接用 GitHub 网页 "Add file → 选择 CODE_OF_CONDUCT（内置 Contributor Covenant）"；
   - 不要照搬 golang-standards/project-layout 等重型布局。

2. **团队/公司开源项目**
   - 以 dec0dOS/amazing-github-template（约 700 星，最接近"主厨精选"）为骨架起步，或参考 microsoft/repo-templates 的默认值；
   - 加 Contributor Covenant + Keep a Changelog + stevemao/github-issue-templates；
   - 配 dependabot/renovate + GitHub Actions CI + pre-commit；
   - 用 ossf/scorecard 和 todogroup/repolinter 做质量门禁。

3. **基金会级/大型项目**
   - 直接用 cncf/project-template（81 星但为 CNCF 官方，含 GOVERNANCE/MAINTAINERS 等基金会必需文件），或 DSACMS/repo-scaffolder（分层 tier 的 cookiecutter，含 outbound checklist）；
   - 目标拿 OpenSSF Best Practices Badge。

4. **按语言的完整脚手架**
   - **Python**：现代新项目用 cookiecutter-uv（1,319 星）或 cookiecutter-pypackage（4,587 星）；数据科学用 cookiecutter-data-science（10.0k 星）；科学计算用 scientific-python/cookie（409 星，权威但星低）。避免 hypermodern-python（已停滞）。
   - **JS/TS**：库用 gjuchault/typescript-library-starter（现代工具链）；tsdx（11.5k 星）注意其半停滞/2.0 重写状态。
   - **Go**：用 golang-templates/seed（566 星）作仓库模板；项目布局遵循官方 go.dev/doc/modules/layout，勿盲从 golang-standards。
   - **Rust**：用 cargo-generate + 社区模板（目前无绝对主导的高星模板，按需选 CLI/service 模板）。

**触发重新评估的阈值/基准：**
- 若某脚手架末次提交超过 12 个月、或依赖了已废弃工具（如 Poetry→uv 迁移潮），应切换到活跃替代。
- 若你的项目要面向企业/合规，star 数应让位于"是否被同类知名项目采用 + 是否有 OpenSSF Badge"。
- 若将来出现一个 >5k 星、含填满示范 + 内嵌讲解的成套模板仓库，可直接取代本菜单的 A 段拼装方案——目前该缺口仍存在。

## Caveats
- GitHub 星/fork 数在仓库页面为四舍五入显示（如 "2.3k" "10.0k"），本报告在能取到精确整数处采用精确值（如 409、81、87、4,587、566），核实日期为 2026-09-17；数字随时间变化。
- 部分第三方聚合站（StackShare、star-history 快照等）存在缓存滞后，本报告以 github.com 实时页面为准。
- "被知名项目采用"的判断部分基于官方自述（如 Contributor Covenant 官网称"最大 10 个 OSS 项目中 9 个采用"），宜谨慎看待；Wikipedia/TechCrunch 提供了具体采用者交叉印证。
- 语言生态模板更新极快（尤其 Python 的 uv/ruff 浪潮），本报告快照可能在数月内部分过时。
- 本轮网络检索预算在完成主要候选核实后耗尽，个别工具（repolinter、部分 TS starter）的精确星数未逐一取到，已在表中留空并标注。

---

# GitHub 仓库模板"主厨精选"深度调研报告（修订版）

> 数据核实日期：2026-09-17。本次修订仅重写 "Recommendations → 分场景推荐组合 → 1. 个人小项目（任意语言）" 小节，并做保持一致性所需的最小改动（如同步行为准则版本与若干星数）；其余结构、菜单表、结论、争议标注、Caveats 全部保留。

## TL;DR
- **个人小项目应遵循"麻雀虽小、五脏俱全"**：用轻量、官方或高认可度的单文件来源，把 README、LICENSE、.gitignore、行为准则、贡献指南、安全策略、Issue/PR 模板、CHANGELOG、最小 CI、依赖更新一次性配齐，而**不**动用 `cookiecutter` / `cncf/project-template` 等重型脚手架。
- **优先"官方内置 + 单文件"路线**：Issue 用 GitHub 官方 Issue Forms（YAML）、CHANGELOG 优先用 GitHub 自动生成 Release Notes（`.github/release.yml`）、CI 用 `actions/starter-workflows`（约 12.1k 星，官方）、依赖用 `dependabot.yml`——这些都零维护成本且被 GitHub 官方支持。
- **账号级 `.github` 公共仓库**可为名下所有小项目下发默认社区健康文件；但要注意：一旦某仓库自己的 `.github/ISSUE_TEMPLATE` 里有任何文件（哪怕只是 `config.yml`），账号默认的 Issue 模板夹会被**整体覆盖失效**；且许可证无法作为默认文件下发。

## Key Findings
- "五脏俱全"的最小集合共 13 类文件：README、LICENSE、.gitignore 为绝对必需；行为准则、贡献指南、安全策略、Issue/PR 模板、CHANGELOG 为强烈推荐；CI、Dependabot 及一批可选文件按需添加。
- 大多数社区健康文件 GitHub 已内置生成器或官方语法（网页 "Add file" 向导、Issue Forms、自动 Release Notes、Dependabot、starter-workflows），个人项目基本不需要第三方模板仓库；第三方仓库的主要价值是"抄一份现成写法"。
- CHANGELOG 自动化工具按项目类型分流：Node 项目用 **changesets**（12.4k 星）；非 Node / 想要单文件二进制用 **git-cliff**（orhun/git-cliff，已越过 1 万星，Apache-2.0 或 MIT 双许可）；Conventional Commits + 想自动发版 PR 用 **release-please**（googleapis 维护，Apache-2.0）；但对绝大多数个人小项目，**GitHub 内置自动生成 Release Notes** 已够用且零依赖。
- 账号默认社区健康文件的覆盖规则是"文件夹级全有或全无"——GitHub 官方文档明确："if a repository has any files in its own `.github/ISSUE_TEMPLATE` folder … none of the contents of the default `.github/ISSUE_TEMPLATE` folder will be used."

## Details

### （菜单表沿用）主厨精选一览
| 类别 | 主厨精选来源 | 认可度 | 备注 |
|---|---|---|---|
| README | othneildrew/Best-README-Template | 16.4k 星（23k forks，Unlicense） | Public template，含 `BLANK_README.md` 精简版 |
| README 规范 | RichardLitt/standard-readme | 6.2k 星（2.5k forks） | 章节规范 + 徽章 |
| LICENSE | choosealicense.com / SPDX | GitHub 官方 | 网页向导内置 |
| .gitignore | github/gitignore | GitHub 官方 | 数百种语言模板 |
| 行为准则 | Contributor Covenant 3.0（2.1 为上一版） | 事实标准 | GitHub 网页内置模板 |
| Issue/PR 模板 | GitHub Issue Forms（官方 YAML） | GitHub 官方 | 见下文 |
| CHANGELOG | Keep a Changelog + SemVer | 事实标准 | 可配 GitHub 自动 Release Notes |
| CI | actions/starter-workflows | 约 12.1k 星，官方 | lint + test 起步 |
| 依赖更新 | dependabot.yml | GitHub 官方 | 最小配置 |
| 重型布局（反例） | golang-standards/project-layout、cncf/project-template、cookiecutter | — | 个人小项目不要照搬 |

（结论、争议标注见文末各节，保持不变。）

---

### Recommendations（分场景推荐组合）

#### 1. 个人小项目（任意语言）——轻量但五脏俱全

**设计原则**：只用官方内置或高认可度的单文件来源，一次配齐；能用 GitHub 网页/内置功能生成的就不引第三方；坚决不动用 `cncf/project-template`、`cookiecutter` 大型脚手架。以下每项标注【必需】/【推荐】/【可选】。

**① README.md【必需】**
- 推荐来源：**othneildrew/Best-README-Template**（16.4k 星、23k forks、Unlicense，Public template；仓库自带 `BLANK_README.md` 精简版）。若嫌其偏"作品集"风格，可改用 **RichardLitt/standard-readme**（6.2k 星，"A standard style for README files"）的最小章节规范。
- 最小可用写法：项目名 + 一句话简介 → 安装 → 用法 → 许可证。个人小项目直接用 `BLANK_README.md`，搜索替换 `github_username`、`repo_name`、`project_title` 等占位符即可，其余高级章节（Roadmap、致谢）可删。

**② LICENSE【必需】**
- 推荐来源：**choosealicense.com**（GitHub 官方运营）；许可证标识遵循 **SPDX**。
- 最小可用写法：GitHub 网页 "Add file → Create new file → 输入 `LICENSE` → 右侧 Choose a license template" 选 MIT，填年份和姓名即可。**注意**：许可证不能作为账号默认社区健康文件下发（"You cannot create a default license file."），必须每个仓库各放一份。

**③ .gitignore【必需】**
- 推荐来源：**github/gitignore**（GitHub 官方维护的数百种语言模板）。
- 最小可用写法：新建仓库时在 "Add .gitignore" 下拉里按语言选择；已有仓库可从该仓库对应语言文件复制。

**④ CODE_OF_CONDUCT.md【推荐】**
- 推荐来源：**Contributor Covenant**（开源界事实标准）。最新版为 **3.0**（由 Organization for Ethical Source 于 2025-07-28 发布，官方称其为 "a major rewrite … adopted by thousands of open source communities, including Linux, Mastodon"，将旧的四级 "Enforcement Guidelines" 阶梯改写为 "Addressing and Repairing Harm" 结构）；GitHub 网页内置的行为准则模板历史上提供 **2.1** 文本，二者皆可用于个人小项目。
- 最小可用写法：仓库 "Add file → 选择 CODE_OF_CONDUCT 模板 → Contributor Covenant"，把联系邮箱填进 enforcement/举报段即可，无需改动正文；若想用 3.0，可直接从 contributor-covenant.org 复制。

**⑤ CONTRIBUTING.md【推荐】**
- 推荐来源：可参考 GitHub 官方文档 "Setting guidelines for repository contributors"；高认可度且可复用的范例是 **jessesquires/.github** 里的 `CONTRIBUTING.md`（作者明确写明"Please feel free to adopt this guide in your own projects. Fork it wholesale or remix it"）。
- 最小可用写法：三段即可——如何提 Issue、如何提 PR（fork → 分支 → 提交 → PR）、代码风格/测试要求各一句。

**⑥ SECURITY.md【推荐】**
- 推荐来源：GitHub 官方安全策略文档 + 开启仓库的 **Private Vulnerability Reporting（私有漏洞报告）**。
- 最小可用写法：先到 Settings → Advanced Security / Code security 开启 Private vulnerability reporting（公共仓库免费，开启后 Security 页会出现 "Report a vulnerability" 按钮，报告全程私有、无需交换 PGP 密钥）；SECURITY.md 里写清两点——"支持的版本" + "请通过 Security 页私有报告，不要开公开 Issue"。**坑点**：SECURITY.md 若指向私有报告按钮，务必确认该功能已开启，否则按钮不存在、指引失效。

**⑦ Issue 模板【推荐】**
- 推荐来源：**优先用 GitHub 官方 Issue Forms（YAML 结构化表单）**，放在 `.github/ISSUE_TEMPLATE/` 下（issue forms 需 `.yml` 扩展名，经典 Markdown 模板用 `.md`）。第三方合集 **stevemao/github-issue-templates**（约 4.4k 星）仅作参考——其 README 已自述 "GitHub now also supports multiple issue templates"，属偏历史性质、更新不活跃，不建议直接照搬。
- 最小可用写法：建 `bug_report.yml` 与 `feature_request.yml` 两个表单，再加 `config.yml` 关闭空白 Issue、把使用求助引流到 Discussions：
  ```yaml
  # .github/ISSUE_TEMPLATE/config.yml
  blank_issues_enabled: false
  contact_links:
    - name: 使用问题请到 Discussions
      url: https://github.com/OWNER/REPO/discussions
      about: 提问和求助请走这里，不要开 Issue
  ```
  （`blank_issues_enabled: false` 后，写权限以上的维护者仍会看到标注 "Maintainers only" 的空白选项，Read/Triage 角色只看到配置的模板。）

**⑧ PR 模板【推荐】**
- 推荐来源：GitHub 官方 `.github/PULL_REQUEST_TEMPLATE.md`。
- 最小可用写法（清单式）：
  ```markdown
  ## 变更说明
  <!-- 这个 PR 做了什么、为什么 -->
  ## 关联 Issue
  Closes #
  ## 自检清单
  - [ ] 本地测试通过
  - [ ] 更新了 CHANGELOG（如适用）
  - [ ] 更新了文档（如适用）
  ```

**⑨ CHANGELOG.md【推荐】**
- 格式：**Keep a Changelog + 语义化版本 SemVer**（两者均为事实标准）。
- 轻量自动化选型（按项目类型）：
  - **个人小项目首选：GitHub 内置自动生成 Release Notes**——发布 Release 时点 "Generate release notes"，用 `.github/release.yml` 定制分类，零依赖。示例：
    ```yaml
    # .github/release.yml
    changelog:
      categories:
        - title: 🎉 新功能
          labels: ["enhancement"]
        - title: 🐛 修复
          labels: ["bug"]
        - title: 其它
          labels: ["*"]
    ```
  - **Node/前端项目**：changesets（12.4k 星，MIT，专为版本与 changelog 设计，PR 驱动、monorepo 支持最好）。
  - **非 Node / 想要单文件二进制、从 Git 历史生成 `CHANGELOG.md`**：git-cliff（orhun/git-cliff，已越过 1 万星，Rust 单二进制，`brew install` 即用、无 Node 依赖、速度快）。
  - **Conventional Commits + 想自动开"发版 PR"**：release-please（googleapis 维护，Apache-2.0，官方 Action 为 GitHub 认证伙伴）——功能强但较重，需要 Conventional Commits 规范与额外权限/PAT。
- **结论**：个人小项目最合适的是 **GitHub 内置 Release Notes**；只有当你坚持在仓库里维护一个 `CHANGELOG.md` 文件、又采用规范化提交时，才上 git-cliff（无 Node 依赖）或 changesets（Node 生态）。release-please 对个人小项目通常属过度配置。

**⑩ 最小 CI【推荐】**
- 推荐来源：**`actions/starter-workflows`**（约 12.1k 星，GitHub 官方；注意该仓库当前不接受外部贡献，仅作起步模板源）。
- 最小可用写法：在仓库 Actions 页选官方起步模板，或手写 `.github/workflows/ci.yml` 做 lint + test 两步，触发 `push` 与 `pull_request`。

**⑪ 依赖更新【推荐】**
- 推荐来源：GitHub 官方 **Dependabot**，配置文件 `.github/dependabot.yml`。
- 最小可用写法（先把 Actions 自身管起来，再按语言加一段；GitHub Actions 生态的 `directory` 用 `/` 即会扫描 `.github/workflows`）：
  ```yaml
  version: 2
  updates:
    - package-ecosystem: "github-actions"
      directory: "/"
      schedule:
        interval: "weekly"
  ```

**⑫ 可选文件【可选】**
- `.editorconfig`（统一缩进/换行）、pre-commit（本地钩子）、`CODEOWNERS`（自动指派审阅）、`.github/FUNDING.yml`（赞助入口）。个人小项目按需添加，不加也不影响"五脏俱全"。

**⑬ 账号级默认社区健康文件技巧【可选但强烈推荐】**
- 建一个名为 **`.github` 的公共仓库**，把 CODE_OF_CONDUCT/CONTRIBUTING/SECURITY 等放进去，即可被你名下所有"未自带该类型文件"的仓库继承，省去逐仓库复制。GitHub 的查找顺序为：当前仓库的 `.github/` → 根目录 → `docs/`，找不到再回退到账号 `.github` 仓库同样顺序。
- **关键坑（官方明文）**："However, if a repository has any files in its own `.github/ISSUE_TEMPLATE` folder, such as issue templates or a `config.yml` file, none of the contents of the default `.github/ISSUE_TEMPLATE` folder will be used." 即：仓库本地 ISSUE_TEMPLATE 只要有一个文件，账号默认 Issue 模板夹**整体失效**（全有或全无）。此外**许可证无法作为默认文件下发**。

**示例目录树**
```
my-small-project/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   └── config.yml
│   ├── workflows/
│   │   └── ci.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── dependabot.yml
│   └── release.yml
├── .editorconfig            # 可选
├── .gitignore
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── SECURITY.md
```

**可直接参考的真实仓库范例**
- **jessesquires/.github**（约 6 星，MIT，活跃）：个人账号默认社区健康文件的经典示范，CONTRIBUTING/SECURITY/SUPPORT 齐全、作者鼓励复用，且其博客亲测记录了"账号默认 Issue 模板"的历史坑，参考价值高于星数。
- **maehr/github-template**（约 23 星，Public template，活跃）：明确面向小项目的轻量模板，语言无关，含 CHANGELOG（git-cliff + Keep a Changelog）、CODE_OF_CONDUCT、CONTRIBUTING、SECURITY 与 `ISSUE_TEMPLATE/config.yml`——最接近"轻量且五脏俱全"的可抄样板（引用前建议手动确认其 Issue 模板是否为 YAML 表单及是否含 PR 模板）。
- **dec0dOS/amazing-github-template**（约 710 星，259 forks）：文件最齐（含 PR 模板、CODEOWNERS、labels、stale/lock/CodeQL 等 Actions），但基于 **Cookiecutter** 脚手架（`cookiecutter.json` / Jinja 变量），宜"看写法"而非直接当轻量样板。
- 反例：**sindresorhus/awesome**（约 506k 星）虽极受欢迎，但 `.github/` 仅有 `workflows/`，无 SECURITY、无 `ISSUE_TEMPLATE`、无 CHANGELOG，不满足"五脏俱全"清单，不宜作本场景范例。

**自检**：配齐后到仓库 **Insights → Community Standards** 页做勾选自检，绿勾越多说明社区健康文件越完整。

**保留提醒**：不要照搬 **golang-standards/project-layout** 等重型目录布局——它并非官方标准，对个人小项目属过度工程。

#### 2. 团队/组织项目
（沿用原报告，保持不变。）

#### 3. 需要合规/治理的大型开源项目
（沿用原报告，保持不变。）

## Caveats
- **星数为动态数据**，本报告核实于 2026-09-17，此后会变化；决策时以仓库当日页面为准。个别仓库不同页面显示的星/叉数存在小幅不一致（如 Best-README-Template 在不同缓存页显示 15.5k–16.4k 星，本报告取 star-history 的 16.4k），属抓取时点差异。
- **行为准则版本**：Contributor Covenant 3.0 已于 2025-07-28 发布并成为最新版；GitHub 网页内置模板历史上仍提供 2.1 文本。若追求最新可手动采用 3.0，否则沿用内置 2.1 也完全可接受。
- **"账号默认 Issue 模板对个人账号是否生效"存在历史争议**：早年（jessesquires 2020 年博客）记录个人账号默认 Issue 模板存在无法生效的 bug；但当前 GitHub 官方文档已把 Issue/PR 模板列为组织与个人账号**均支持**的默认社区健康文件类型。无论是否生效，"仓库本地 `.github/ISSUE_TEMPLATE` 有文件即整体覆盖默认夹"这一规则明确成立。
- **stevemao/github-issue-templates**（约 4.4k 星）属早期合集、更新不活跃，且 GitHub 已原生支持 Issue Forms，故仅列为"参考写法"而非首选。
- **release-please、changesets、git-cliff 面向不同生态**，对个人小项目多为过度配置；本报告据此给出分流建议，核心结论是个人小项目优先用 GitHub 内置 Release Notes。


----

请求：根据最后一篇文档创建一个开源仓库，作用是帮助个人项目/团队项目快速起步，起因是市面上没有现成的“主厨精选”仓库，但是开源仓库中各个模块的佼佼者已经基本有明确答案，他们贡献活跃度高，使用人数多，某些仓库甚至已经成为了事实上的标准，而这个仓库的目的就是可以免去搜集各个模块中哪些是佼佼者，也不用费力的将他们拼接起来，仓库提供开箱即用的体验，所有完整仓库的核心要素都包括了，开源贡献者无需费力处理这些问题，只需关注自己的想法和创作本身即可。

项目的亮点是所有模块的选择相对来说都是社区中的佼佼者，并不是我的一厢情愿，但也不排除可以多选的情况下我依据个人喜好作出选择。每个模块。标注出所有模块的来源和他们的的大致使用人数（估算）或者start数量，帮助使用者建立信任。

我的个人喜好是：优先社区认可度，如果认可度度相同的情况下，是否易于仓库持有者起步
