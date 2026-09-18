# 契约：占位符与来源注释

对应需求：FR-007、FR-008、FR-028、FR-037；宪章原则 III、IV。决策依据：[research.md](../research.md) R3、R18。

## 1. 占位符

### 1.1 语法

- 正则：`CHANGEME_[A-Z0-9_]+`。
- 一条命令即可找出全部占位符：`git grep -n CHANGEME`。未初始化 Git 的目录可用 `grep -rn CHANGEME .`。
- 占位符只能出现在项目文件中。起步引导层（`SETUP.md`）只能以登记表的形式列出它们，不得在正文示例中使用。

### 1.2 登记表

C08 检查要求：项目文件中出现的每个占位符都必须在下表中；对每个占位符，它实际出现的文件必须与下表第 3 列中**已经存在**的文件完全一致（模板逐步完成时，尚未创建的文件不算问题）。`SETUP.md` 必须按 [guidance-layer.md](./guidance-layer.md) §2 规定的表头收录下表的全部行。

| 占位符 | 含义 / Meaning | 出现的文件（相对 `template/`） | 示例 / Example |
|---|---|---|---|
| `CHANGEME_OWNER` | GitHub 用户名或组织名 / GitHub user or organization | `README.md`、`SECURITY.md`、`CHANGELOG.md`、`.github/ISSUE_TEMPLATE/config.yml`、`.github/CODEOWNERS` | `octocat` |
| `CHANGEME_REPO` | 仓库名 / Repository name | `README.md`、`SECURITY.md`、`CHANGELOG.md`、`.github/ISSUE_TEMPLATE/config.yml` | `hello-world` |
| `CHANGEME_PROJECT_NAME` | 项目显示名称 / Project display name | `README.md` | `Hello World` |
| `CHANGEME_PROJECT_DESCRIPTION` | 一句话简介 / One-sentence description | `README.md` | `A tiny tool that says hello.` |
| `CHANGEME_USAGE_EXAMPLE` | 最简单的使用示例 / Minimal usage example | `README.md` | `hello --name Ada` |
| `CHANGEME_YEAR` | 版权年份 / Copyright year | `LICENSE` | `2026` |
| `CHANGEME_COPYRIGHT_HOLDER` | 版权人 / Copyright holder | `LICENSE` | `Ada Lovelace` |
| `CHANGEME_SECURITY_EMAIL` | 安全问题备用邮箱 / Fallback email for security reports | `SECURITY.md` | `security@example.com` |
| `CHANGEME_CONDUCT_EMAIL` | 行为准则举报邮箱 / Email for Code of Conduct reports | `CODE_OF_CONDUCT.md` | `conduct@example.com` |

### 1.3 禁止残留的标记（C08 检查）

项目文件中不得出现下列上游占位写法或待办标记：
- `github_username`、`repo_name`、`project_title`、`project_description`、`project_license`
- `twitter_handle`、`linkedin_username`、`email_client`
- `[INSERT CONTACT METHOD]`、`[year]`、`[fullname]`
- `TODO`、`FIXME`
- `$default-branch`

## 2. 来源注释

### 2.1 格式（C09 检查）

- **位置**：每个项目文件的**第一行**。`LICENSE` 不加注释，否则 GitHub 识别许可证类型可能受影响。
- **Markdown 文件**：`<!-- Source: <名称> (<许可证或 official>) — <https 链接> -->`。
- **其他文件**（YAML、`.gitignore`、`.editorconfig`、`CODEOWNERS`）：`# Source: <名称> (<许可证或 official>) — <https 链接>`。
- **多个来源**：写在同一行，用 `; ` 分隔，例如 `A (…) — URL; B (…) — URL`。
- **分隔符**：名称与链接之间用空格加 em dash（U+2014）加空格。
- **校验正则**：
  - Markdown：`^<!-- Source: .+ — https://\S+.* -->$`
  - 其他文件：`^# Source: .+ — https://\S+`
- **语言与措辞**：注释只用英文，不得提及模板本身（参见 [template-layout.md](./template-layout.md) §4）。

### 2.2 各文件的注释原文

实施时逐字使用下表内容，链接均已于 2026-09-18 确认可以访问。

| 文件 | 第一行（逐字） |
|---|---|
| `README.md` | `<!-- Source: Best-README-Template BLANK_README (Unlicense) — https://github.com/othneildrew/Best-README-Template -->` |
| `CODE_OF_CONDUCT.md` | `<!-- Source: Contributor Covenant 2.1 (CC BY 4.0) — https://www.contributor-covenant.org/version/2/1/code_of_conduct/ -->` |
| `CONTRIBUTING.md` | `<!-- Source: GitHub Open Source Guides (CC BY 4.0, structure only) — https://opensource.guide/starting-a-project/; GitHub Docs (official) — https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors -->` |
| `SECURITY.md` | `<!-- Source: GitHub security policy and private vulnerability reporting (official) — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy -->` |
| `CHANGELOG.md` | `<!-- Source: Keep a Changelog 1.1.0 (MIT) — https://keepachangelog.com/en/1.1.0/ -->` |
| `.github/PULL_REQUEST_TEMPLATE.md` | `<!-- Source: GitHub pull request template (official) — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository -->` |
| `.gitignore` | `# Source: github/gitignore Global templates (CC0-1.0) — https://github.com/github/gitignore/tree/356fd7baab4c05e092194a41f64dbd5afc8817e4/Global` |
| `.editorconfig` | `# Source: EditorConfig (official specification) — https://editorconfig.org` |
| `.pre-commit-config.yaml` | `# Source: pre-commit and pre-commit-hooks (MIT) — https://pre-commit.com` |
| `.github/CODEOWNERS` | `# Source: GitHub code owners (official) — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners` |
| `.github/FUNDING.yml` | `# Source: GitHub sponsor button (official) — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository` |
| `.github/ISSUE_TEMPLATE/bug_report.yml` | `# Source: GitHub issue forms (official) — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms` |
| `.github/ISSUE_TEMPLATE/feature_request.yml` | `# Source: GitHub issue forms (official) — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms` |
| `.github/ISSUE_TEMPLATE/config.yml` | `# Source: GitHub issue template chooser (official) — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository` |
| `.github/dependabot.yml` | `# Source: GitHub Dependabot (official) — https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference` |
| `.github/release.yml` | `# Source: GitHub automatically generated release notes (official) — https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes` |
| `.github/workflows/ci.yml` | `# Source: GitHub starter workflow "Simple workflow" (MIT) — https://github.com/actions/starter-workflows/blob/main/ci/blank.yml` |

**说明**：合并请求模板第一行的注释会随模板进入每个合并请求的描述。渲染时看不到它，GUIDE 的 M08 小节会说明这一点。

## 3. 其他可引用的官方链接

以下链接已确认可访问，只能在起步引导层中使用：

- 私有漏洞报告：https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository
- 开启讨论区：https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/enabling-or-disabling-github-discussions-for-a-repository
- 账号级默认社区健康文件：https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file
- 固定动作版本（安全使用参考）：https://docs.github.com/en/actions/reference/security/secure-use
- 从模板创建仓库：https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template
- 规则集：https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- 选择许可证：https://choosealicense.com/licenses/mit/
- 中文译本：
  - Contributor Covenant 2.1：https://www.contributor-covenant.org/zh-cn/version/2/1/code_of_conduct/
  - Keep a Changelog 1.1.0：https://keepachangelog.com/zh-CN/1.1.0/
  - 语义化版本：https://semver.org/lang/zh-CN/
  - 开源指南：https://opensource.guide/zh-hans/starting-a-project/
- 其他：https://www.contributor-covenant.org/translations/、https://bestpractices.dev
