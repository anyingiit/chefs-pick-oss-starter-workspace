# 起步清单 / Setup checklist

按下面的顺序完成这份清单，大约需要 15 分钟：先替换占位符，再补齐仓库设置和项目文件，最后清理这一层起步引导内容。

Work through this checklist in order; it takes about 15 minutes. Replace the placeholders first, then complete the repository settings and the project files, and remove this guide layer last.

## 占位符 / Placeholders

下表登记了模板中的全部占位符。逐个替换成你自己的项目信息，不要留下任何一个。

The table below registers every placeholder in the template. Replace each one with your own project information, and leave none behind.

| 占位符 / Placeholder | 含义 / Meaning | 出现的文件 / Files | 示例 / Example |
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

清理起步引导层之前，用下面这条命令查找还没替换的占位符。它会排除本页的登记表，所以登记表不会被算进结果。

Before you remove the guide layer, use this command to find the placeholders you have not replaced yet. It excludes the registry table on this page, so the table itself is not counted.

```bash
git grep -n CHANGEME -- . ':(exclude).github/chefs-pick'
```

清理起步引导层之后，用下面这条命令做最终确认。

After you remove the guide layer, use this command for the final check.

```bash
git grep -n CHANGEME
```

两条命令都不应该有任何输出。

Neither command should print anything.

## 步骤 / Steps

| 编号 / ID | 类型 / Kind | 步骤 / Step | 如何确认 / How to verify |
|---|---|---|---|
| S01 | 必做 / Required | 替换全部占位符，逐项对照上面的登记表。/ Replace every placeholder, working through the registry table above. | 清理前的搜索命令没有输出。/ The pre-cleanup search command prints nothing. |
| S02 | 必做 / Required | 在仓库首页的 About（齿轮图标）中填写简介，可选填写 Topics。如果仓库属于组织账号，再到 Settings → Moderation options → Reported content 开启内容举报；个人账号的仓库没有这一项设置。/ Fill in the description under About (the gear icon) on the repository home page, and optionally add topics. If the repository belongs to an organization, also enable reported content under Settings → Moderation options → Reported content; repositories owned by a personal account do not have this setting. | 仓库首页右侧显示简介；社区标准页上与仓库设置相关的项目都已完成。/ The description shows on the right-hand side of the repository home page, and every settings-related item on the community standards page is complete. |
| S03 | 必做 / Required | 开启私有漏洞报告：Settings → Advanced Security → Private vulnerability reporting（[官方文档 / Official docs](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)）。/ Enable private vulnerability reporting under Settings → Advanced Security → Private vulnerability reporting. | Security 页出现 **Report a vulnerability**。/ The Security tab shows **Report a vulnerability**. |
| S04 | 必做 / Required | 开启讨论区：Settings → General → Features → Discussions（[官方文档 / Official docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/enabling-or-disabling-github-discussions-for-a-repository)）。如果不开启讨论区，就把两处都改成你自己的求助渠道：[`.github/ISSUE_TEMPLATE/config.yml`](../ISSUE_TEMPLATE/config.yml) 中的讨论区链接，以及 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 的 Questions 一节。/ Enable Discussions under Settings → General → Features → Discussions. If you decide not to, point both places at your own support channel: the discussions link in [`.github/ISSUE_TEMPLATE/config.yml`](../ISSUE_TEMPLATE/config.yml) and the Questions section of [`CONTRIBUTING.md`](../../CONTRIBUTING.md). | New issue 页面上的求助链接可以打开，且 `CONTRIBUTING.md` 指向的渠道与之一致。/ The support link on the New issue page opens, and the channel named in `CONTRIBUTING.md` is the same one. |
| S05 | 必做 / Required | 确认许可证：默认是 MIT。要更换时，先在 [choosealicense.com](https://choosealicense.com/licenses/mit/) 选好许可证，替换 [`LICENSE`](../../LICENSE)，并同步修改 [`README.md`](../../README.md) 的 License 一节。/ Confirm the license: MIT is the default. To use a different one, pick it on [choosealicense.com](https://choosealicense.com/licenses/mit/), replace [`LICENSE`](../../LICENSE), and update the License section of [`README.md`](../../README.md) to match. | 仓库首页显示正确的许可证。/ The repository home page shows the right license. |
| S06 | 必做 / Required | 按项目语言补充三项：`.gitignore` 规则，取自 `github/gitignore`；`ci.yml` 的检查与测试步骤，新增的动作要固定到哈希，见[模块讲解 / Module guide](GUIDE.md) 的「固定动作版本 / Pinning actions」一节；`dependabot.yml` 的依赖生态。/ Add three things for your project's language: the `.gitignore` rules, taken from `github/gitignore`; the lint and test steps in `ci.yml`, pinning any action you add to a commit hash as described in the "Pinning actions" section of the [module guide](GUIDE.md); and your dependency ecosystems in `dependabot.yml`. | 推送后 CI 通过。/ CI passes after you push. |
| S07 | 选做 / Optional | 逐个决定推荐模块和可选模块是否保留，每个模块的删除方法见[模块讲解 / Module guide](GUIDE.md)。/ Decide one by one whether to keep each recommended and optional module; the [module guide](GUIDE.md) explains how to remove each of them. | 保留的可选模块都已按说明启用。/ Every optional module you kept has been enabled as its instructions describe. |
| S08 | 必做 / Required | 清理起步引导层，运行[模板首页 / Template home page](../README.md)给出的清理命令。/ Remove the guide layer by running the cleanup command given on the [template home page](../README.md). | 仓库首页显示你自己的 `README.md`。/ The repository home page shows your own `README.md`. |
| S09 | 必做 / Required | 最终验收。/ Run the final check. | Insights → Community Standards 各项都是绿勾；`git grep -n CHANGEME` 没有输出；CI 通过。自检页只会列出你的账号类型支持的项，例如内容举报只对组织账号的公共仓库出现，所以列出的项都应当能补齐。/ Every item under Insights → Community Standards has a green check, `git grep -n CHANGEME` prints nothing, and CI passes. The page only lists the items your account type supports — reported content, for example, appears only for public repositories owned by an organization — so everything it lists should be something you can complete. |
