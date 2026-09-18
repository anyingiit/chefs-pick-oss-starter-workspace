# 选型清单 / Selection list

数据核实日期 / Data verified: 2026-09-18

本文件逐个模块记录选定来源、认可度证据、备选方案和未选原因，让每一项选择都可以被复核。

This file records, module by module, the pick, its adoption evidence, the alternatives considered, and why they were not chosen, so that every choice can be re-checked.

## 选型规则 / Selection rules

取舍按三级规则依次进行：第 1 级看社区认可度，认可度明显更高的候选胜出；第 1 级分不出高下时用第 2 级，选对仓库持有者更容易起步的一项；前两级都分不出高下时才用第 3 级，按作者个人偏好决定，并在理由中写明"作者偏好 / author's preference"。表中的"取舍规则 / Rule"一格写 `1`、`2`、`3` 或 `1 + 2`：`1 + 2` 表示第 1 级已能决定、第 2 级也指向同一选择；写 `2` 时，入选理由必须写明判定"认可度相当"的依据。只看 Star 数不够，所以每一项都附具体证据。

Picks are made with three rules applied in order. Rule 1 goes by community adoption: the candidate with clearly higher adoption wins. Rule 2 is used when rule 1 cannot separate the candidates, and picks whichever is easier for a repository owner to start with. Rule 3 is used only when the first two cannot separate them, and records the author's preference explicitly. The "Rule" field holds `1`, `2`, `3` or `1 + 2`; `1 + 2` means rule 1 already decided and rule 2 points the same way, while a bare `2` requires the rationale to state why adoption is judged comparable. Star counts alone are not enough, so every pick carries concrete evidence.

认可度证据只使用以下六种写法 / Adoption evidence uses exactly these six labels:

- `精确 Star 数 / Exact stars`
- `四舍五入 Star 数 / Rounded stars`
- `估算使用人数 / Estimated users`（必须附估算依据 / must state how it was estimated）
- `平台官方功能 / Official platform feature`
- `事实标准 / De facto standard`（必须附具体采用者 / must name specific adopters）
- `未取得 / Not available`（必须附替代证据 / must state what was used instead）

复核周期：至少每 6 个月复核一次；每次发布前也要复核，发布时所有数据的核实日期不得早于发布前 30 天。

Review cadence: at least once every six months, and again before every release, with no verification date older than 30 days at release time.

## 模块 / Modules

### M01 项目说明 / README

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `README.md` |
| 级别 / Level | 必需 / Required |
| 选定来源 / Pick | [Best-README-Template](https://github.com/othneildrew/Best-README-Template) |
| 版本或提交 / Version | othneildrew/Best-README-Template@fc444eb |
| 上游许可证 / Upstream license | Unlicense |
| 认可度证据 / Evidence | 精确 Star 数 / Exact stars：★ 16,360 (othneildrew/Best-README-Template) |
| 取舍规则 / Rule | 1 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：它是 README 模板中认可度最高的一个，Star 数远高于其他候选，第 1 级即可决定。它采用 Unlicense，复用时不需要署名；`BLANK_README.md` 的章节划分正好覆盖访客最先要看的内容，去掉项目专属章节后就是一份干净的骨架。

**Rationale**: It is by far the most widely adopted README template, so rule 1 settles the choice on its own. It is released under the Unlicense, so reuse needs no attribution, and the sections of `BLANK_README.md` cover exactly what a visitor reads first; dropping the project-specific sections leaves a clean skeleton.

**备选方案 / Alternatives**

- standard-readme — 精确 Star 数 / Exact stars：★ 6,367 (RichardLitt/standard-readme) — 需要额外的检查工具和章节约束 / it needs an extra linter and imposes a fixed section structure
- The-Documentation-Compendium — 精确 Star 数 / Exact stars：★ 6,036 (race2infinity/The-Documentation-Compendium) — 没有许可证，不能安全复用 / it has no license, so it cannot be reused safely
- awesome-readme-template — 精确 Star 数 / Exact stars：★ 1,861 (Louis3797/awesome-readme-template) — 2022 年后没有更新 / no updates since 2022

### M02 许可证 / License

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `LICENSE` |
| 级别 / Level | 必需 / Required |
| 选定来源 / Pick | [choosealicense.com 的 MIT / MIT on choosealicense.com](https://choosealicense.com/licenses/mit/)，SPDX 标识 `MIT` |
| 版本或提交 / Version | github/choosealicense.com@58267f8 |
| 上游许可证 / Upstream license | MIT |
| 认可度证据 / Evidence | 平台官方功能 / Official platform feature：GitHub 运营的许可证选择器；精确 Star 数 / Exact stars：★ 4,202 (github/choosealicense.com) |
| 取舍规则 / Rule | 1 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：许可证正文取自 GitHub 自己运营的 choosealicense.com，是权威且可核对的出处，第 1 级即可决定。MIT 条款简短、限制最少，适合作为个人项目的默认许可证；GitHub 也能据此在仓库首页正确识别出许可证类型。

**Rationale**: The license text comes from choosealicense.com, which GitHub itself runs, so the source is authoritative and verifiable and rule 1 decides. MIT is short and minimally restrictive, which suits a personal project as a default, and GitHub detects it correctly on the repository home page.

**备选方案 / Alternatives**

- 其他 OSI 许可证 / Other OSI licenses — 未取得 / Not available — 交接文档已把 MIT 定为默认，使用者可以自行更换 / the handover already fixed MIT as the default, and users can swap it themselves

### M03 忽略规则 / Ignore rules

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `.gitignore` |
| 级别 / Level | 必需 / Required |
| 选定来源 / Pick | [github/gitignore 的 Global 模板 / Global templates](https://github.com/github/gitignore) |
| 版本或提交 / Version | github/gitignore@356fd7b |
| 上游许可证 / Upstream license | CC0-1.0 |
| 认可度证据 / Evidence | 精确 Star 数 / Exact stars：★ 175,816 (github/gitignore) |
| 取舍规则 / Rule | 1 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：这是 GitHub 官方维护的忽略规则集合，认可度在同类中遥遥领先，第 1 级即可决定。它采用 CC0-1.0，可以直接收录；Global 部分与语言无关，正好满足"先挡住系统和编辑器产生的文件"这一需求。

**Rationale**: This is GitHub's own collection of ignore rules and its adoption dwarfs every comparable option, so rule 1 decides. It is CC0-1.0, so the text can be included directly, and the Global templates are language-independent, which is exactly what is needed to keep operating-system and editor files out of the repository.

**备选方案 / Alternatives**

- gitignore.io 在线服务 / the gitignore.io service — 未取得 / Not available — 依赖第三方服务，认可度不如官方集合 / it depends on a third-party service and is less adopted than the official collection

### M04 行为准则 / Code of Conduct

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `CODE_OF_CONDUCT.md` |
| 级别 / Level | 推荐 / Recommended |
| 选定来源 / Pick | [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) |
| 版本或提交 / Version | 2.1（EthicalSource/contributor_covenant@7255a28） |
| 上游许可证 / Upstream license | CC-BY-4.0 |
| 认可度证据 / Evidence | 事实标准 / De facto standard：官方采用者名单收录 454 个项目，包括 .NET Foundation、Bootstrap、Cloud Native Computing Foundation、curl、Django；精确 Star 数 / Exact stars：★ 2,259 (EthicalSource/contributor_covenant) |
| 取舍规则 / Rule | 1 + 2 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：第 1 级看认可度，2.x 系列是采用最广的行为准则，官方采用者名单收录 454 个项目，包括 .NET Foundation、Bootstrap、CNCF、curl、Django。第 2 级也指向同一选择：2.1 采用 CC BY 4.0，使用者只需填一个联系方式即可生效，而 3.0 改用 CC BY-SA 4.0，修改后须按相同方式共享，还要改写一整段执行说明，起步负担明显更重。

**Rationale**: Under rule 1, the 2.x series is the most widely adopted code of conduct, with 454 projects on the official adopters list, among them the .NET Foundation, Bootstrap, CNCF, curl and Django. Rule 2 points the same way: 2.1 is CC BY 4.0 and only needs a contact method filled in, whereas 3.0 moved to CC BY-SA 4.0, which requires share-alike for modified versions and a rewritten enforcement section, making it heavier to start with.

**备选方案 / Alternatives**

- Contributor Covenant 3.0 — 事实标准 / De facto standard — 采用 CC BY-SA 4.0，并要求改写整段执行说明 / it uses CC BY-SA 4.0 and requires rewriting the whole enforcement section
- Contributor Covenant 2.0 — 平台官方功能 / Official platform feature — GitHub 接口提供的版本，已被 2.1 取代 / it is the version GitHub's API returns, but 2.1 supersedes it
- Django Code of Conduct — 平台官方功能 / Official platform feature — 采用面较窄 / its adoption is much narrower

### M05 贡献指南 / Contributing guide

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `CONTRIBUTING.md` |
| 级别 / Level | 推荐 / Recommended |
| 选定来源 / Pick | [GitHub Open Source Guides](https://opensource.guide/starting-a-project/) + [GitHub Docs](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors) |
| 版本或提交 / Version | 只参考结构，正文为原创 / structure only, the text is original |
| 上游许可证 / Upstream license | CC-BY-4.0（未复制文字 / no text copied） |
| 认可度证据 / Evidence | 精确 Star 数 / Exact stars：★ 15,685 (github/opensource.guide)；平台官方功能 / Official platform feature：GitHub Docs |
| 取舍规则 / Rule | 1 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：GitHub 官方维护的开源指南是这一领域认可度最高的出处，配合 GitHub Docs 的对应条目，第 1 级即可决定。本模板只参考它们的章节结构，正文为原创的简洁英文，因此没有 CC BY 的署名义务，但来源注释仍注明参考来源。

**Rationale**: GitHub's own Open Source Guides are the most widely adopted source in this area, and together with the matching GitHub Docs article they settle the choice under rule 1. The template borrows only their section structure and writes its own concise English text, so no CC BY attribution obligation arises, while the source comment still names the references.

**备选方案 / Alternatives**

- jessesquires/.github — 精确 Star 数 / Exact stars：★ 42 (jessesquires/.github) — 默认分支最近提交为 2023-03-26，已超过 12 个月，社区依据偏弱 / its default branch was last committed to on 2023-03-26, more than 12 months ago, and the community evidence is weak

### M06 安全策略 / Security policy

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `SECURITY.md` |
| 级别 / Level | 推荐 / Recommended |
| 选定来源 / Pick | [GitHub 安全策略 / Security policy](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy) + [私有漏洞报告 / Private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository) |
| 版本或提交 / Version | — |
| 上游许可证 / Upstream license | 官方文档 / Official docs |
| 认可度证据 / Evidence | 平台官方功能 / Official platform feature |
| 取舍规则 / Rule | 1 + 2 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：第 1 级看认可度，安全策略和私有漏洞报告都是 GitHub 内置的平台功能，社区标准自检也直接检查 `SECURITY.md`，没有第三方候选能与之相比。第 2 级同样指向它：开启私有漏洞报告只需在设置里勾一个开关，报告人在 Security 页就能提交，不必交换密钥。

**Rationale**: Under rule 1, both the security policy file and private vulnerability reporting are built into GitHub, the community profile check looks for `SECURITY.md` directly, and no third-party option competes. Rule 2 agrees: enabling private reporting is a single setting, and reporters submit from the Security tab without exchanging keys.

**备选方案 / Alternatives**

- 只提供邮箱或 PGP 公钥 / An email address or PGP key only — 未取得 / Not available — 需要交换密钥，起步更难，而且报告不会进入平台的通报流程 / it requires key exchange, is harder to start with, and reports stay outside the platform's advisory workflow

### M07 Issue 表单 / Issue forms

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `.github/ISSUE_TEMPLATE/bug_report.yml`、`.github/ISSUE_TEMPLATE/feature_request.yml`、`.github/ISSUE_TEMPLATE/config.yml` |
| 级别 / Level | 推荐 / Recommended |
| 选定来源 / Pick | [GitHub Issue Forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms) |
| 版本或提交 / Version | — |
| 上游许可证 / Upstream license | 官方文档 / Official docs |
| 认可度证据 / Evidence | 平台官方功能 / Official platform feature |
| 取舍规则 / Rule | 1 + 2 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：第 1 级看认可度，Issue 表单是 GitHub 官方的结构化提问方式，社区标准自检要求表单有合法的 `name` 和 `description`，第三方模板集合都是它出现之前的产物。第 2 级也指向它：表单可以把关键字段设为必填，并自动打上标签，提问者不必自己照着说明抄格式。

**Rationale**: Under rule 1, issue forms are GitHub's official way to collect structured reports, the community profile check expects a valid `name` and `description`, and the third-party template collections all predate them. Rule 2 agrees: forms can mark key fields as required and apply labels automatically, so reporters do not have to copy a format by hand.

**备选方案 / Alternatives**

- stevemao/github-issue-templates — 精确 Star 数 / Exact stars：★ 4,461 (stevemao/github-issue-templates) — 早于 Issue Forms，默认分支 2024-03-20 之后没有提交 / it predates issue forms and its default branch has had no commits since 2024-03-20
- Markdown 模板 / Markdown templates — 平台官方功能 / Official platform feature — 无法强制必填，收到的信息经常不完整 / they cannot make fields required, so reports often arrive incomplete

### M08 合并请求模板 / Pull request template

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `.github/PULL_REQUEST_TEMPLATE.md` |
| 级别 / Level | 推荐 / Recommended |
| 选定来源 / Pick | [GitHub 合并请求模板 / Pull request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository) |
| 版本或提交 / Version | — |
| 上游许可证 / Upstream license | 官方文档 / Official docs |
| 认可度证据 / Evidence | 平台官方功能 / Official platform feature |
| 取舍规则 / Rule | 1 + 2 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：第 1 级看认可度，单文件的合并请求模板是 GitHub 官方支持的写法，放在 `.github/PULL_REQUEST_TEMPLATE.md` 就会自动填入每个合并请求的描述。第 2 级也指向它：只有一个文件、一份清单，个人项目不需要选择模板的步骤。

**Rationale**: Under rule 1, a single pull request template is GitHub's officially supported form, and a file at `.github/PULL_REQUEST_TEMPLATE.md` is filled into every pull request description automatically. Rule 2 agrees: one file and one checklist means a personal project never has to pick a template.

**备选方案 / Alternatives**

- stevemao/github-issue-templates — 精确 Star 数 / Exact stars：★ 4,461 (stevemao/github-issue-templates) — 同 M07：早于官方写法，且已停止更新 / same as M07: it predates the official form and is no longer updated
- 多模板目录 / A directory of several templates — 平台官方功能 / Official platform feature — 个人项目不需要，还要求提交者在 URL 上选模板 / a personal project does not need it, and it forces contributors to pick a template via the URL

### M09 变更日志与发布说明 / Changelog & release notes

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `CHANGELOG.md`、`.github/release.yml` |
| 级别 / Level | 推荐 / Recommended |
| 选定来源 / Pick | [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) + [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) + [GitHub 自动生成的发布说明 / Automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes) |
| 版本或提交 / Version | KaC 1.1.0（2.0.0 仍是未发布草稿 / 2.0.0 is still an unreleased draft）；SemVer 2.0.0 |
| 上游许可证 / Upstream license | MIT；CC-BY-3.0；官方文档 / Official docs |
| 认可度证据 / Evidence | 精确 Star 数 / Exact stars：★ 6,702 (olivierlacan/keep-a-changelog)、★ 7,853 (semver/semver)；平台官方功能 / Official platform feature：自动生成的发布说明 |
| 取舍规则 / Rule | 1 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：Keep a Changelog 与语义化版本是写给人看的变更历史里认可度最高的两份规范，第 1 级即可决定；1.1.0 是当前已发布的版本，2.0.0 仍是未发布草稿，所以固定在 1.1.0。发布说明分类交给 GitHub 的官方功能，依赖默认标签 `bug` 和 `enhancement`，不引入任何依赖。

**Rationale**: Keep a Changelog and Semantic Versioning are the two most widely adopted specifications for a human-readable history, so rule 1 decides; 1.1.0 is the current released version while 2.0.0 is still an unreleased draft, so the pick is pinned to 1.1.0. Release-note grouping is left to GitHub's built-in feature, which keys off the default `bug` and `enhancement` labels and adds no dependency.

**备选方案 / Alternatives**

- 只用发布说明、不保留 CHANGELOG / Release notes only, with no changelog file — 平台官方功能 / Official platform feature — 会缺少核心要素，仓库里读不到变更历史 / a core element would be missing and the history would not be readable inside the repository
- Keep a Changelog 2.0.0 — 事实标准 / De facto standard — 尚未发布，仍是草稿 / it is not released yet and remains a draft

### M10 变更日志自动化 / Changelog automation

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | — |
| 级别 / Level | 可选（只推荐）/ Optional (recommendation only) |
| 选定来源 / Pick | [changesets](https://github.com/changesets/changesets)、[git-cliff](https://github.com/orhun/git-cliff)、[release-please](https://github.com/googleapis/release-please) |
| 版本或提交 / Version | 由使用者选定 / chosen by the user |
| 上游许可证 / Upstream license | MIT；Apache-2.0 或 MIT；Apache-2.0 |
| 认可度证据 / Evidence | 精确 Star 数 / Exact stars：★ 12,408 (changesets/changesets)、★ 12,245 (orhun/git-cliff)、★ 7,509 (googleapis/release-please) |
| 取舍规则 / Rule | 1 + 2 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：第 1 级看认可度，这三个工具各自是所属生态里认可度最高的：Node 生态用 changesets，与语言无关的项目用单一可执行文件的 git-cliff，采用 Conventional Commits 并希望自动发起发版合并请求的用 release-please。第 2 级决定的是"默认一个都不启用"：模板不提供任何文件，个人项目用 M09 的默认方案通常已经够用，需要时再按项目类型选一个。

**Rationale**: Under rule 1, each of the three leads adoption in its own ecosystem: changesets for Node projects, git-cliff as a single language-agnostic binary, and release-please for projects on Conventional Commits that want an automated release pull request. Rule 2 decides that none is enabled by default: the template ships no file here, the M09 default is usually enough for a personal project, and a tool can be added later by project type.

**备选方案 / Alternatives**

- GitHub 自动生成的发布说明 / GitHub's automatically generated release notes — 平台官方功能 / Official platform feature — 即 M09 的默认方案；零依赖，个人项目通常已够用，所以本模块默认不启用任何工具 / it is the M09 default, needs no dependency and is usually enough for a personal project, which is why no tool is enabled here by default

### M11 自动检查 / Continuous integration

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `.github/workflows/ci.yml` |
| 级别 / Level | 推荐 / Recommended |
| 选定来源 / Pick | [actions/starter-workflows 的 Simple workflow](https://github.com/actions/starter-workflows/blob/main/ci/blank.yml) + [actions/checkout](https://github.com/actions/checkout) |
| 版本或提交 / Version | actions/checkout@3d3c42e（v7.0.1） |
| 上游许可证 / Upstream license | MIT；MIT |
| 认可度证据 / Evidence | 精确 Star 数 / Exact stars：★ 12,082 (actions/starter-workflows)、★ 8,884 (actions/checkout)；固定哈希的依据：平台官方功能 / Official platform feature（GitHub Docs 安全使用参考）与精确 Star 数 / Exact stars ★ 5,694 (ossf/scorecard) |
| 取舍规则 / Rule | 1 + 2 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：第 1 级看认可度，官方起步工作流集合是 GitHub 自己维护的，`actions/checkout` 是使用最广的动作；把动作固定到完整提交哈希的做法同时有 GitHub Docs 的安全使用参考和 OpenSSF Scorecard 作为依据。第 2 级也指向它：Simple workflow 在空仓库上一定能通过，使用者只需在标注位置补上自己的检查和测试命令，不必先学一整套 CI 配置。

**Rationale**: Under rule 1, the starter workflow collection is maintained by GitHub itself and `actions/checkout` is the most widely used action, while pinning actions to a full commit hash is backed both by GitHub's secure-use reference and by OpenSSF Scorecard. Rule 2 agrees: the Simple workflow passes on an empty repository, so users only fill in their own lint and test commands at the marked places instead of learning a whole CI configuration first.

**备选方案 / Alternatives**

- super-linter — 精确 Star 数 / Exact stars：★ 10,598 (super-linter/super-linter) — 镜像庞大、运行慢 / its image is large and runs slowly
- markdownlint — 精确 Star 数 / Exact stars：★ 6,345 (DavidAnson/markdownlint) — README 骨架含 HTML，容易误报，需要额外调整规则 / the README skeleton contains HTML, so it produces false positives without extra rule tuning
- actionlint — 精确 Star 数 / Exact stars：★ 4,235 (rhysd/actionlint) — 没有官方动作，需要下载脚本或使用 Docker / there is no official action, so it needs a download script or Docker
- github-actions-ensure-sha-pinned-actions — 精确 Star 数 / Exact stars：★ 55 (zgosalvez/github-actions-ensure-sha-pinned-actions) — 认可度低，且要额外信任一个第三方动作 / adoption is low and it means trusting one more third-party action

### M12 依赖自动更新 / Dependency updates

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `.github/dependabot.yml` |
| 级别 / Level | 推荐 / Recommended |
| 选定来源 / Pick | [GitHub Dependabot](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference) |
| 版本或提交 / Version | — |
| 上游许可证 / Upstream license | MIT（dependabot-core） |
| 认可度证据 / Evidence | 平台官方功能 / Official platform feature；精确 Star 数 / Exact stars：★ 5,773 (dependabot/dependabot-core) |
| 取舍规则 / Rule | 2 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：Dependabot 与 Renovate 都是事实标准，认可度相当；Dependabot 由平台内置、不需要安装，起步更容易。判定"认可度相当"的依据是：两者都被大规模采用，Renovate 的仓库 Star 数更高（★ 22,527 (renovatebot/renovate)），而 Dependabot 作为平台内置功能没有可比的 Star 数，`dependabot/dependabot-core` 只是它的实现仓库，所以第 1 级分不出高下，改用第 2 级。Dependabot 升级动作哈希时还会同步更新行尾的版本注释，与 M11 的固定哈希写法正好配合。

**Rationale**: Both are de facto standards with comparable adoption; Dependabot is built into the platform and needs no installation. Adoption is judged comparable because both are used at scale: Renovate's repository has more stars (★ 22,527 (renovatebot/renovate)), while Dependabot, as a built-in feature, has no comparable star count at all — `dependabot/dependabot-core` is only its implementation repository — so rule 1 cannot separate them and rule 2 applies. Dependabot also keeps the trailing version comment in step when it bumps an action hash, which fits the pinning style used in M11.

**备选方案 / Alternatives**

- Renovate — 精确 Star 数 / Exact stars：★ 22,527 (renovatebot/renovate) — 需要安装 App 并编写配置，许可证为 AGPL-3.0；已放入团队升级指引 / it requires installing a GitHub App and writing its own configuration, is licensed AGPL-3.0, and is listed in the team upgrade guide instead

### M13 编辑器格式配置 / EditorConfig

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `.editorconfig` |
| 级别 / Level | 可选 / Optional |
| 选定来源 / Pick | [EditorConfig](https://editorconfig.org) |
| 版本或提交 / Version | — |
| 上游许可证 / Upstream license | 未识别 / Unknown |
| 认可度证据 / Evidence | 精确 Star 数 / Exact stars：★ 3,450 (editorconfig/editorconfig)；复核说明：默认分支最近提交为 2025-04-21，已按宪章原则 III 重新评估并保留 |
| 取舍规则 / Rule | 1 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：统一编码、换行和缩进这件事上没有认可度接近的第二个候选，主流编辑器原生支持或有官方插件，第 1 级即可决定。上游默认分支最近提交是 2025-04-21，已超过 12 个月，按宪章原则 III 重新评估：规范本身已经稳定，活跃度低是稳定的结果而不是停滞，因此保留。

**Rationale**: For unifying encoding, line endings and indentation there is no second candidate with comparable adoption, and mainstream editors support it natively or through an official plugin, so rule 1 decides. The upstream default branch was last committed to on 2025-04-21, more than 12 months ago, so it was re-evaluated under constitution principle III: the specification itself is stable and the low activity reflects that stability rather than abandonment, so the pick stands.

**备选方案 / Alternatives**

- 无同类候选 / No comparable alternative — 未取得 / Not available — 各编辑器的私有配置不能跨编辑器使用 / editor-specific settings files do not carry across editors

### M14 提交前检查 / Pre-commit hooks

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `.pre-commit-config.yaml` |
| 级别 / Level | 可选 / Optional |
| 选定来源 / Pick | [pre-commit](https://pre-commit.com) + [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks) |
| 版本或提交 / Version | pre-commit-hooks@3e8a870（v6.0.0） |
| 上游许可证 / Upstream license | MIT；MIT |
| 认可度证据 / Evidence | 精确 Star 数 / Exact stars：★ 15,581 (pre-commit/pre-commit)、★ 6,681 (pre-commit/pre-commit-hooks) |
| 取舍规则 / Rule | 1 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：pre-commit 是跨语言钩子管理器中认可度最高的一个，官方钩子集合 pre-commit-hooks 同样广泛使用，第 1 级即可决定。配置中的 `rev` 固定到完整提交哈希并附版本注释，与 M11 的做法一致；不运行 `pre-commit install` 就不会有任何效果，所以默认存在也不会打扰使用者。

**Rationale**: pre-commit is the most widely adopted cross-language hook manager and its official hook collection is just as widely used, so rule 1 decides. The `rev` is pinned to a full commit hash with a version comment, matching the approach in M11, and nothing happens until `pre-commit install` is run, so shipping the file by default disturbs nobody.

**备选方案 / Alternatives**

- 原生 Git 钩子脚本 / Plain Git hook scripts — 未取得 / Not available — 无法共享，也不受版本管理 / they cannot be shared and are not version-controlled

### M15 代码负责人 / Code owners

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `.github/CODEOWNERS` |
| 级别 / Level | 可选 / Optional |
| 选定来源 / Pick | [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) |
| 版本或提交 / Version | — |
| 上游许可证 / Upstream license | 官方文档 / Official docs |
| 认可度证据 / Evidence | 平台官方功能 / Official platform feature |
| 取舍规则 / Rule | 1 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：自动请求代码审阅是 GitHub 的内置功能，由平台按 `CODEOWNERS` 的路径规则直接生效，没有第三方候选能做到同样的事，第 1 级即可决定。模板里所有行都是注释，默认不生效，等到项目有了协作者再取消注释即可。

**Rationale**: Automatic review requests are built into GitHub and driven directly by the path rules in `CODEOWNERS`, with no third-party option able to do the same, so rule 1 decides. Every line in the shipped file is a comment, so nothing takes effect until the project has collaborators and the lines are uncommented.

**备选方案 / Alternatives**

- 无同类候选 / No comparable alternative — 未取得 / Not available — 这是平台内置功能，第三方工具无法接管审阅请求 / it is a built-in platform feature and no third-party tool can take over review requests

### M16 赞助入口 / Funding

| 字段 / Field | 内容 / Value |
|---|---|
| 文件 / Files | `.github/FUNDING.yml` |
| 级别 / Level | 可选 / Optional |
| 选定来源 / Pick | [GitHub 赞助按钮 / Sponsor button](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository) |
| 版本或提交 / Version | — |
| 上游许可证 / Upstream license | 官方文档 / Official docs |
| 认可度证据 / Evidence | 平台官方功能 / Official platform feature |
| 取舍规则 / Rule | 1 |
| 核实日期 / Verified | 2026-09-18 |

**入选理由**：仓库页面上的赞助按钮只能由 `.github/FUNDING.yml` 驱动，这是 GitHub 官方的唯一做法，第 1 级即可决定。模板沿用设置页生成的官方格式，只保留 `github:` 和 `custom:` 两个键且值为空，因此默认不会出现赞助按钮。

**Rationale**: The sponsor button on a repository page can only be driven by `.github/FUNDING.yml`, which is GitHub's single official mechanism, so rule 1 decides. The template keeps the format the settings page generates, with only the empty `github:` and `custom:` keys, so no sponsor button appears by default.

**备选方案 / Alternatives**

- 在 README 中手写赞助链接 / Hand-written funding links in the README — 未取得 / Not available — 这样不会显示仓库的赞助按钮 / it does not produce the repository's sponsor button

## 排除的候选 / Excluded candidates

| 候选 / Candidate | 认可度 / Adoption | 排除理由 / Reason |
|---|---|---|
| golang-standards/project-layout | ★ 56,602 (golang-standards/project-layout) | Go 团队明确表示它不是官方标准，Star 数高但不能作为权威依据 / the Go team states explicitly that it is not an official standard, so the high star count is not authoritative |
| cookiecutter/cookiecutter | ★ 25,091 (cookiecutter/cookiecutter) | 它是脚手架生成器，需要额外安装和一套自己的工作流，违反"模板仓库开箱即用"的取舍 / it is a scaffolding generator that needs a separate install and its own workflow, against the choice of a ready-to-use template repository |
| stevemao/github-issue-templates | ★ 4,461 (stevemao/github-issue-templates) | 已被官方 Issue Forms 取代，默认分支自 2024-03-20 起没有新提交 / superseded by the official issue forms, and its default branch has had no commits since 2024-03-20 |
| copier-org/copier | ★ 3,579 (copier-org/copier) | 同为生成器，使用者必须先安装工具才能创建项目 / also a generator: users must install a tool before they can create a project |
| dec0dOS/amazing-github-template | ★ 710 (dec0dOS/amazing-github-template) | 基于 cookiecutter，且默认分支自 2021-12-08 起没有新提交 / it is built on cookiecutter and its default branch has had no commits since 2021-12-08 |
| todogroup/repolinter | ★ 465 (todogroup/repolinter)，已归档 / archived | 仓库已归档，不再维护，按宪章原则 III 视同停更 / the repository is archived and unmaintained, which counts as abandoned under constitution principle III |
| cncf/project-template | ★ 82 (cncf/project-template) | 面向基金会级治理，条目远超个人项目所需，只放进团队升级指引 / it targets foundation-level governance, far beyond what a personal project needs, so it is listed only in the team upgrade guide |
| jessesquires/.github | ★ 42 (jessesquires/.github) | 认可度低，默认分支最近提交为 2023-03-26，已超过 12 个月，只降为参考范例 / adoption is low and its default branch was last committed to on 2023-03-26, more than 12 months ago, so it is kept only as a reference example |
| maehr/github-template | ★ 23 (maehr/github-template) | 认可度低，且采用 AGPL-3.0，会给使用者带来额外的合规负担 / adoption is low and it is licensed AGPL-3.0, which puts an extra compliance burden on users |

## 认可度数据 / Adoption data

下表是机器可读的认可度快照，`tools/verify_sources.py` 按这张表批量刷新。`Last commit` 是默认分支最近一次提交的日期，不是 `pushed_at`；`License` 只写 GitHub API 返回的 SPDX 标识，取不到时写 `unknown`。

The table below is a machine-readable adoption snapshot, refreshed in bulk by `tools/verify_sources.py`. `Last commit` is the date of the most recent commit on the default branch, not `pushed_at`; `License` holds only the SPDX identifier returned by the GitHub API, or `unknown` when none is returned.

<!-- adoption-data:start -->
| Repo | Stars | Forks | Last commit | License | Archived | Verified |
|---|---:|---:|---|---|---|---|
| github/gitignore | 175,816 | 82,186 | 2026-09-11 | CC0-1.0 | no | 2026-09-18 |
| othneildrew/Best-README-Template | 16,360 | 23,013 | 2026-04-18 | Unlicense | no | 2026-09-18 |
| RichardLitt/standard-readme | 6,367 | 2,507 | 2026-06-17 | MIT | no | 2026-09-18 |
| race2infinity/The-Documentation-Compendium | 6,036 | 739 | 2025-10-31 | unknown | no | 2026-09-18 |
| Louis3797/awesome-readme-template | 1,861 | 437 | 2022-04-07 | CC0-1.0 | no | 2026-09-18 |
| EthicalSource/contributor_covenant | 2,259 | 1,435 | 2026-05-20 | unknown | no | 2026-09-18 |
| olivierlacan/keep-a-changelog | 6,702 | 3,537 | 2026-09-03 | MIT | no | 2026-09-18 |
| semver/semver | 7,853 | 785 | 2025-11-05 | unknown | no | 2026-09-18 |
| actions/starter-workflows | 12,082 | 7,329 | 2026-08-03 | unknown | no | 2026-09-18 |
| actions/checkout | 8,884 | 2,779 | 2026-07-20 | MIT | no | 2026-09-18 |
| github/choosealicense.com | 4,202 | 1,628 | 2026-09-10 | MIT | no | 2026-09-18 |
| github/opensource.guide | 15,685 | 15,524 | 2026-09-04 | CC-BY-4.0 | no | 2026-09-18 |
| jessesquires/.github | 42 | 28 | 2023-03-26 | MIT | no | 2026-09-18 |
| stevemao/github-issue-templates | 4,461 | 5,550 | 2024-03-20 | unknown | no | 2026-09-18 |
| changesets/changesets | 12,408 | 833 | 2026-09-14 | MIT | no | 2026-09-18 |
| orhun/git-cliff | 12,245 | 326 | 2026-09-13 | Apache-2.0 | no | 2026-09-18 |
| googleapis/release-please | 7,509 | 589 | 2026-09-14 | Apache-2.0 | no | 2026-09-18 |
| editorconfig/editorconfig | 3,450 | 119 | 2025-04-21 | unknown | no | 2026-09-18 |
| pre-commit/pre-commit | 15,581 | 1,009 | 2026-08-17 | MIT | no | 2026-09-18 |
| pre-commit/pre-commit-hooks | 6,681 | 799 | 2026-08-17 | MIT | no | 2026-09-18 |
| dependabot/dependabot-core | 5,773 | 1,524 | 2026-09-17 | MIT | no | 2026-09-18 |
| renovatebot/renovate | 22,527 | 3,315 | 2026-09-17 | AGPL-3.0 | no | 2026-09-18 |
| ossf/scorecard | 5,694 | 724 | 2026-09-08 | Apache-2.0 | no | 2026-09-18 |
| DavidAnson/markdownlint | 6,345 | 946 | 2026-07-28 | MIT | no | 2026-09-18 |
| rhysd/actionlint | 4,235 | 272 | 2026-04-19 | MIT | no | 2026-09-18 |
| super-linter/super-linter | 10,598 | 1,080 | 2026-09-17 | MIT | no | 2026-09-18 |
| zgosalvez/github-actions-ensure-sha-pinned-actions | 55 | 16 | 2026-09-05 | MIT | no | 2026-09-18 |
| golang-standards/project-layout | 56,602 | 5,425 | 2026-04-28 | unknown | no | 2026-09-18 |
| cookiecutter/cookiecutter | 25,091 | 2,277 | 2026-03-04 | BSD-3-Clause | no | 2026-09-18 |
| copier-org/copier | 3,579 | 273 | 2026-09-07 | MIT | no | 2026-09-18 |
| cncf/project-template | 82 | 46 | 2026-08-11 | Apache-2.0 | no | 2026-09-18 |
| microsoft/repo-templates | 89 | 93 | 2026-08-24 | MIT | no | 2026-09-18 |
| dec0dOS/amazing-github-template | 710 | 259 | 2021-12-08 | MIT | no | 2026-09-18 |
| maehr/github-template | 23 | 6 | 2026-03-06 | AGPL-3.0 | no | 2026-09-18 |
| todogroup/repolinter | 465 | 74 | 2026-02-06 | Apache-2.0 | yes | 2026-09-18 |
| ossf/best-practices-badge | 1,360 | 233 | 2026-09-17 | MIT | no | 2026-09-18 |
<!-- adoption-data:end -->

## 数据说明 / About the data

仓库数据来自 GitHub API：Star 数和 Fork 数是接口返回的精确整数，写成带千分位逗号的形式；`Last commit` 取默认分支最近一次提交的日期，不用 `pushed_at`，因为后者会被任何分支的推送更新，从而漏掉已经停更的上游；`Archived` 取接口的归档标志；`License` 只写 `license.spdx_id`，接口返回 `NOASSERTION` 或空值时写 `unknown`，因此它与各模块"上游许可证"一栏可能不同，后者写的是查阅许可证文件后得到的实际许可证。非仓库证据分两类：平台官方功能以 GitHub Docs 的对应条目为准；Contributor Covenant 的采用者数量取自上游仓库的官方采用者名单。维护者的复核周期、复核步骤和刷新命令写在同目录的 `MAINTAINING.md` 中。

Repository data comes from the GitHub API. Stars and forks are the exact integers the API returns, written with thousands separators. `Last commit` is the date of the most recent commit on the default branch rather than `pushed_at`, because `pushed_at` is bumped by a push to any branch and would hide an abandoned upstream. `Archived` is the API's archive flag. `License` holds only `license.spdx_id`, written as `unknown` when the API returns `NOASSERTION` or no value, which is why it can differ from the "Upstream license" field of a module: that field records the actual license found by reading the upstream license file. Non-repository evidence falls into two groups: official platform features are verified against the corresponding GitHub Docs article, and the Contributor Covenant adopter count comes from the official adopters list in the upstream repository. The review cadence, the review steps and the refresh command are documented in `MAINTAINING.md`, in this same directory.
