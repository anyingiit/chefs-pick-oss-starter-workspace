# 升级为团队项目 / Growing into a team project

本页是可选的简要参考，列出项目从个人维护走向多人协作时常见的增强项，5 分钟内可以读完；本模板不包含这些文件，需要时自行添加。

This page is an optional short reference listing the additions a project commonly makes as it grows from solo maintenance into team collaboration; it reads in five minutes, and none of these files ship with the template, so add them when you need them.

## 常用增强项 / Common additions

| 增强项 / Addition | 作用 / Purpose | 来源 / Source | 认可度 / Adoption |
|---|---|---|---|
| CODEOWNERS 的团队用法 / CODEOWNERS for teams | 按路径指定负责的团队，合并请求自动请求他们审阅 / Assign an owning team per path so pull requests request their review automatically | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners | 平台官方功能 / Official platform feature |
| 规则集 / Rulesets | 为默认分支设定必需的审阅和状态检查，取代逐条分支保护 / Require reviews and status checks on the default branch, superseding one-off branch protection | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets | 平台官方功能 / Official platform feature |
| Renovate | 比 Dependabot 更灵活的依赖升级：可分组、可排期、可自动合并 / Dependency updates with more control than Dependabot: grouping, schedules, automerge | https://github.com/renovatebot/renovate | ★ 22,527 (renovatebot/renovate) |
| pre-commit | 提交前统一运行格式化与检查；个人版已作为可选模块 M14 提供，团队可以在 CI 中强制执行 / Runs formatters and linters before each commit; the solo setup already ships as optional module M14, and a team can enforce it in CI | https://github.com/pre-commit/pre-commit | ★ 15,581 (pre-commit/pre-commit) |
| OpenSSF Scorecard | 自动评估仓库的供应链安全实践，给出可逐项跟进的改进建议 / Scores a repository's supply-chain security practices and lists concrete items to follow up | https://github.com/ossf/scorecard | ★ 5,694 (ossf/scorecard) |

## 需要基金会级治理时 / When you need foundation-level governance

项目捐给基金会，或者需要正式的治理、管理委员会和商标约定时，可以参考下面三项。它们面向组织，对个人项目来说过重。

When a project is donated to a foundation, or needs formal governance, a steering committee and trademark rules, the three references below apply. They target organizations and are too heavy for a personal project.

- `cncf/project-template`（CNCF 官方的项目治理文件集，含 GOVERNANCE、MAINTAINERS、CHARTER 等）/ CNCF's official set of project governance documents, including GOVERNANCE, MAINTAINERS and CHARTER — 认可度 / Adoption：★ 82 (cncf/project-template)；来源 / Source：https://github.com/cncf/project-template
- `microsoft/repo-templates`（微软对外开源仓库使用的模板与合规文件）/ The templates and compliance files Microsoft uses for its public open source repositories — 认可度 / Adoption：★ 89 (microsoft/repo-templates)；来源 / Source：https://github.com/microsoft/repo-templates
- OpenSSF Best Practices Badge（按问卷自评开源最佳实践，通过后可在 README 上展示徽章）/ A self-assessment questionnaire on open source best practices that awards a badge to display in your README — 认可度 / Adoption：★ 1,360 (ossf/best-practices-badge)；来源 / Source：https://bestpractices.dev

## 不再推荐 / No longer recommended

- `todogroup/repolinter`（检查仓库是否具备社区健康文件的工具，上游仓库已归档，不再维护）/ A linter that checked whether a repository had its community health files; the upstream repository is archived and no longer maintained — 认可度 / Adoption：★ 465 (todogroup/repolinter)；来源 / Source：https://github.com/todogroup/repolinter
