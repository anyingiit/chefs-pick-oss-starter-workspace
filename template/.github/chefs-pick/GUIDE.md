# 模块讲解 / Module guide

本页逐个讲解模板里的 16 个模块：它为什么在这里、怎样改成你自己的项目、以及不需要时怎样干净地删掉。建议先按 [起步清单 / Setup checklist](SETUP.md) 完成必做步骤，再回到这里逐个模块决定去留。每个模块选定了哪个来源、凭什么选它，记在 [选型清单 / Selection list](SOURCES.md) 里。

This page walks through the 16 modules in the template: why each one is here, how to adapt it to your project, and how to remove it cleanly when you do not want it. Work through the [Setup checklist](SETUP.md) first, then come back here and decide module by module. Which source each module was taken from, and the evidence behind that pick, is recorded in the [Selection list](SOURCES.md).

删除任何模块之前，先在仓库里搜一遍它的文件名（`grep -rn "文件名" .`），确认没有遗漏的引用。每个模块的「如何删除 / Remove」小节都已经列出已知的引用方。

Before you remove any module, search the repository for its file name (`grep -rn "file-name" .`) to be sure no reference is left behind. The "Remove" section of each module already lists the known referrers.

## M01 项目说明 / README

文件 / Files: [`README.md`](../../README.md) · 级别 / Level: 必需 / Required

### 为什么需要 / Why

`README.md` 是访客打开仓库后首先阅读的内容，也是社区标准自检的检查项。它决定了别人愿不愿意继续看下去。

`README.md` is the first thing a visitor reads, and it is one of the items on the community standards checklist. It decides whether anyone keeps reading.

### 如何定制 / Customize

把文件里的占位符全部替换掉（清单见 [起步清单 / Setup checklist](SETUP.md)），补全 About 和 Usage 两节，让人一眼看懂项目做什么、怎么跑起来。如果你更换了许可证，记得同步修改 License 一节里的名称。

Replace every placeholder in the file (the [Setup checklist](SETUP.md) lists them all), then fill in the About and Usage sections so a reader can tell at a glance what the project does and how to run it. If you switch licenses, update the license name in the License section to match.

### 如何删除 / Remove

不建议删除 / Not recommended。没有 `README.md`，GitHub 首页只剩文件列表，社区标准自检的 README 一项永远不会完成，几乎所有其他文件里的链接也会指空。

Not recommended. Without `README.md` the repository front page is just a file listing, the README item on the community standards page never completes, and links from almost every other file point nowhere.

## M02 许可证 / License

文件 / Files: [`LICENSE`](../../LICENSE) · 级别 / Level: 必需 / Required

### 为什么需要 / Why

没有许可证，别人在法律上不能使用、修改或分发你的代码，哪怕仓库是公开的。许可证也是少数不能由账号级默认文件继承的文件之一，每个仓库都得自己带一份。

Without a license nobody may legally use, modify or redistribute your code, even if the repository is public. A license is also one of the few files that cannot be inherited from an account-level default file, so every repository needs its own copy.

### 如何定制 / Customize

填写版权年份和版权人两个占位符即可，其余原文不要改动 —— MIT 文本一旦被改写，GitHub 就可能识别不出许可证类型。想换成别的许可证，见本页的 [更换许可证 / Changing the license](#更换许可证--changing-the-license)。

Fill in the two placeholders for the copyright year and the copyright holder, and leave the rest of the text alone: once the MIT wording is edited, GitHub may stop recognising the license type. To use a different license, see [Changing the license](#更换许可证--changing-the-license) below.

### 如何删除 / Remove

不建议删除 / Not recommended。删掉它等于收回所有使用许可，仓库首页不再显示许可证徽标，社区标准自检的 License 一项也不会完成。

Not recommended. Removing it withdraws all permission to use the code, the license badge disappears from the repository page, and the License item on the community standards page stays unchecked.

## M03 忽略规则 / Ignore rules

文件 / Files: [`.gitignore`](../../.gitignore) · 级别 / Level: 必需 / Required

### 为什么需要 / Why

它挡住操作系统和编辑器生成的杂物（macOS、Windows、Linux、Visual Studio Code、JetBrains），避免这些文件被提交进仓库后再也清理不干净。

It keeps the clutter produced by operating systems and editors (macOS, Windows, Linux, Visual Studio Code, JetBrains) out of the repository, where it is tedious to clean up after the fact.

### 如何定制 / Customize

模板只带与语言无关的通用规则。按你的项目语言，从 github.com/github/gitignore 里取对应的模板（Python、Node、Go 等）追加到文件末尾，写法见本页的 [按语言补充 / Adding language-specific rules](#按语言补充--adding-language-specific-rules)。

The template ships only the language-independent rules. Append the template for your language (Python, Node, Go and so on) from github.com/github/gitignore to the end of the file; see [Adding language-specific rules](#按语言补充--adding-language-specific-rules) below.

### 如何删除 / Remove

不建议删除 / Not recommended。删掉之后，构建产物、依赖目录和 `.DS_Store` 这类文件会随手被提交进来，而且一旦进入历史就很难彻底移除。

Not recommended. Without it, build output, dependency directories and files such as `.DS_Store` get committed by accident, and once they are in the history they are hard to remove for good.

## M04 行为准则 / Code of Conduct

文件 / Files: [`CODE_OF_CONDUCT.md`](../../CODE_OF_CONDUCT.md) · 级别 / Level: 推荐 / Recommended

### 为什么需要 / Why

它把参与规则和举报渠道写在明处，出问题时你有据可依，而不是临时表态。这也是社区标准自检的检查项。

It states the rules of participation and the reporting channel up front, so that when something goes wrong you have something to point at instead of improvising. It is also one of the community standards items.

### 如何定制 / Customize

填写举报邮箱占位符 —— 这是整个文件里唯一必须改的地方。中文项目可以在文件里附上官方中文译本的链接，见 [中文译本 / Chinese translations](#中文译本--chinese-translations)。

Fill in the placeholder for the reporting email address; it is the only thing in the file you must change. Projects working in Chinese can link the official Chinese translation, see [Chinese translations](#中文译本--chinese-translations).

### 如何删除 / Remove

- 删除文件 / Delete: `CODE_OF_CONDUCT.md`。
- 同步修改 / Update: `README.md` 和 `CONTRIBUTING.md` 里都引用了它，删掉相应的链接和整句话；如果 `.github/ISSUE_TEMPLATE/config.yml`、`bug_report.yml`、`feature_request.yml` 或 `.github/PULL_REQUEST_TEMPLATE.md` 里也提到过它，一并清理。
- 失去什么 / What you lose: 仓库不再显示「行为准则」标识，新贡献者提交 Issue 时也看不到参与规则；社区标准自检页上的 Code of conduct 一项会变为未完成。

Delete `CODE_OF_CONDUCT.md`. Both `README.md` and `CONTRIBUTING.md` reference it, so remove those links and the sentences around them; if you added a link to it in `.github/ISSUE_TEMPLATE/config.yml` or in an issue form, clean that up too. Afterwards the repository no longer advertises a code of conduct, new contributors do not see the rules of participation, and the Code of conduct item on the community standards page becomes incomplete.

## M05 贡献指南 / Contributing guide

文件 / Files: [`CONTRIBUTING.md`](../../CONTRIBUTING.md) · 级别 / Level: 推荐 / Recommended

### 为什么需要 / Why

它回答「我想帮忙，从哪儿下手」：报告问题、提交改动、搭建开发环境各走哪条路。GitHub 会在新建 Issue 和合并请求的页面上主动链接它。

It answers the question "I want to help, where do I start": how to report a problem, how to submit a change, how to set up a development environment. GitHub links to it from the new issue and new pull request pages.

### 如何定制 / Customize

补上你项目真实的开发环境步骤和测试命令 —— Development setup 一节是模板里最需要你亲手写的部分。如果你不打算开启讨论区，把 Questions 一节指向的渠道改成你实际使用的渠道（与起步清单 S04 对应）。

Fill in the real development setup steps and test commands for your project; the Development setup section is the part of the template that most needs your own words. If you do not plan to enable Discussions, point the Questions section at the channel you actually use (this matches step S04 of the setup checklist).

### 如何删除 / Remove

- 删除文件 / Delete: `CONTRIBUTING.md`。
- 同步修改 / Update: `README.md` 里有指向它的 Contributing 链接，删掉该链接；`.github/PULL_REQUEST_TEMPLATE.md` 的自检清单、`.github/ISSUE_TEMPLATE/config.yml`、`bug_report.yml` 和 `feature_request.yml` 里如果引用了它，一并清理。
- 失去什么 / What you lose: 新建 Issue 和合并请求时不再出现贡献指南的提示链接，贡献流程只能靠 `README.md` 里的只言片语传达；社区标准自检页上的 Contributing 一项会变为未完成。

Delete `CONTRIBUTING.md`, remove the Contributing link in `README.md`, and clean up any reference to it in `.github/ISSUE_TEMPLATE/config.yml`. After that, the prompt linking to contribution guidelines no longer appears when someone opens an issue or a pull request, the process has to be conveyed by `README.md` alone, and the Contributing item on the community standards page becomes incomplete.

## M06 安全策略 / Security policy

文件 / Files: [`SECURITY.md`](../../SECURITY.md) · 级别 / Level: 推荐 / Recommended

### 为什么需要 / Why

漏洞不能走公开 Issue 通报。这个文件给报告者一条私下的路，并说明哪些版本还在支持。仓库页面上的 Security 标签会直接展示它。

Vulnerabilities must not be reported through public issues. This file gives reporters a private route and states which versions are still supported. The repository's Security tab displays it directly.

### 如何定制 / Customize

填写备用邮箱占位符，按起步清单 S03 开启私有漏洞报告（[官方说明](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)），再按项目实际情况调整支持版本表。私有漏洞报告没开启时，文件里那条 `security/advisories/new` 链接不可用，所以备用邮箱一定要填。

Fill in the fallback email placeholder, enable private vulnerability reporting as described in step S03 of the setup checklist ([official docs](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)), then adjust the supported versions table to match reality. Until private reporting is enabled the `security/advisories/new` link in the file does not work, which is exactly why the fallback email matters.

### 如何删除 / Remove

- 删除文件 / Delete: `SECURITY.md`。
- 同步修改 / Update: `README.md` 和 `CONTRIBUTING.md` 里都引用了它（`CONTRIBUTING.md` 的 Reporting security issues 一节整节都围绕它），删掉链接并改写那一节；`.github/ISSUE_TEMPLATE/config.yml` 里的安全报告链接只在开启私有漏洞报告后才可用，删除本模块时顺带确认那条链接是否还要保留；`bug_report.yml`、`feature_request.yml` 和 `.github/PULL_REQUEST_TEMPLATE.md` 里如果提到过它，也一并清理。
- 失去什么 / What you lose: 仓库 Security 标签下不再有策略页，报告者没有明确的私下渠道，只能猜；社区标准自检页上的 Security policy 一项会变为未完成。

Delete `SECURITY.md`, then remove the links in `README.md` and rewrite the Reporting security issues section of `CONTRIBUTING.md`, which is built entirely around it. The security link in `.github/ISSUE_TEMPLATE/config.yml` only works once private vulnerability reporting is enabled, so check whether you still want it. Afterwards the Security tab has no policy page, reporters have to guess at a private channel, and the Security policy item on the community standards page becomes incomplete.

## M07 Issue 表单 / Issue forms

文件 / Files: [`bug_report.yml`](../ISSUE_TEMPLATE/bug_report.yml)、[`feature_request.yml`](../ISSUE_TEMPLATE/feature_request.yml)、[`config.yml`](../ISSUE_TEMPLATE/config.yml) · 级别 / Level: 推荐 / Recommended

### 为什么需要 / Why

表单把「复现步骤」「期望结果」这类必填信息结构化地收上来，省掉来回追问。`config.yml` 关掉了空白 Issue，并把求助类问题引到合适的渠道。

Forms collect the information you always end up asking for (reproduction steps, expected result) as structured fields. `config.yml` turns off blank issues and routes support questions to a suitable channel.

注意：仓库自带合法的 Issue 模板后，账号级 `.github` 仓库里的默认 Issue 模板会整体失效，见 [账号级默认文件 / Account-level default files](#账号级默认文件--account-level-default-files)。

Note: once a repository ships its own valid issue templates, the default issue templates from your account-level `.github` repository stop applying entirely; see [Account-level default files](#账号级默认文件--account-level-default-files).

### 如何定制 / Customize

按需要增删字段，每个表单都必须保留合法的 `name` 和 `description`，否则社区标准自检不算通过。如果你改了表单自动打的标签，记得同步修改 [`release.yml`](../release.yml) 里的分类规则，否则发布说明会漏掉这些条目。

Add or remove fields as needed, but keep a valid `name` and `description` on every form or the community standards check will not pass. If you change the labels a form applies automatically, update the categories in [`release.yml`](../release.yml) to match, otherwise those entries drop out of the generated release notes.

### 如何删除 / Remove

- 删除文件 / Delete: 整个 `.github/ISSUE_TEMPLATE/` 目录，即 `bug_report.yml`、`feature_request.yml` 和 `config.yml` 三个文件。只删表单、留下 `config.yml`，会得到一个只有外部链接、没有任何模板的选择页。
- 同步修改 / Update: `README.md` 里有 Report a bug 和 Request a feature 两个链接（`issues/new?template=...`），它们会失效，改成普通的 `issues/new`；`CONTRIBUTING.md` 的 Reporting bugs 和 Suggesting features 两节如果引用了 `bug_report.yml` 或 `feature_request.yml`，一并改写。
- 失去什么 / What you lose: 空白 Issue 恢复启用，账号级 `.github` 仓库里的默认 Issue 模板重新生效；问题不再结构化，标签也不再自动打上；社区标准自检页上的 Issue templates 一项会变为未完成。

Delete the whole `.github/ISSUE_TEMPLATE/` directory, that is `bug_report.yml`, `feature_request.yml` and `config.yml` (deleting only the forms and keeping `config.yml` leaves a chooser page with external links and no templates at all). In `README.md`, the Report a bug and Request a feature links use `issues/new?template=...` and will break, so point them at plain `issues/new`. Afterwards blank issues are enabled again, the default issue templates from your account-level `.github` repository take effect again, reports lose their structure and their automatic labels, and the Issue templates item on the community standards page becomes incomplete.

## M08 合并请求模板 / Pull request template

文件 / Files: [`PULL_REQUEST_TEMPLATE.md`](../PULL_REQUEST_TEMPLATE.md) · 级别 / Level: 推荐 / Recommended

### 为什么需要 / Why

它在每个合并请求的描述框里预填一份自检清单：改了什么、关联哪个 Issue、有没有自测。审阅时省下的来回，比写清单花的时间多。

It pre-fills a short self-check into the description box of every pull request: what changed, which issue it closes, whether it was tested. The round trips it saves during review outweigh the time spent filling it in.

### 如何定制 / Customize

按项目实际的门槛调整清单项，三五条就够，太长没人认真读。

需要知道的一点：文件第一行的来源注释会随模板一起进入每个合并请求的描述。它是 HTML 注释，渲染后看不见，但编辑描述时能看到那一行。不想要就删掉这一行，模板的其余部分不受影响。

Adjust the checklist to the bar your project actually holds; three to five items is plenty, longer lists go unread.

One thing to know: the source comment on the first line travels with the template into the description of every pull request. It is an HTML comment, so it is invisible once rendered, but anyone editing the description sees that line. If you would rather not have it, delete that one line; nothing else in the template depends on it.

### 如何删除 / Remove

- 删除文件 / Delete: `.github/PULL_REQUEST_TEMPLATE.md`。
- 同步修改 / Update: `CONTRIBUTING.md` 的 Submitting pull requests 一节里有「填写模板」这类措辞，改成你实际的要求；如果 `README.md` 或 `CHANGELOG.md` 里提到了这个模板，也一并调整。
- 失去什么 / What you lose: 合并请求描述框回到空白，关联 Issue 和自检清单要靠贡献者自觉；社区标准自检页上的 Pull request template 一项会变为未完成。

Delete `.github/PULL_REQUEST_TEMPLATE.md`. In `CONTRIBUTING.md`, the Submitting pull requests section tells contributors to fill in the template, so reword it to match what you actually expect; if the maintenance notes in `CHANGELOG.md` mention the template, adjust those too. Afterwards the pull request description box starts out empty, linking the issue and running the self-check is left to the contributor, and the Pull request template item on the community standards page becomes incomplete.

## M09 变更日志与发布说明 / Changelog and release notes

文件 / Files: [`CHANGELOG.md`](../../CHANGELOG.md)、[`release.yml`](../release.yml) · 级别 / Level: 推荐 / Recommended

### 为什么需要 / Why

`CHANGELOG.md` 按 Keep a Changelog 的写法，给人读的变更历史：一眼看出哪个版本动了什么。`release.yml` 让 GitHub 自动生成的发布说明按类别分组，而不是一长串合并请求标题。两者一个给人看，一个给机器生成，互相补位。

`CHANGELOG.md` follows Keep a Changelog: a history written for humans, where one glance tells you what changed in which version. `release.yml` makes GitHub's automatically generated release notes group entries by category instead of listing pull request titles in one long run. One is written by you, the other is generated; they complement each other.

### 如何定制 / Customize

日常把改动记在 `## [Unreleased]` 下；发布时把这个标题改成版本号加日期，再新建一个空的 Unreleased。`release.yml` 的分类依赖 GitHub 的默认标签 `bug` 和 `enhancement`，如果你改用自己的标签体系，要同步改这个文件里的 `labels`。

Record changes under `## [Unreleased]` as you go; at release time rename that heading to the version number plus the date and start a fresh Unreleased. The categories in `release.yml` rely on GitHub's default `bug` and `enhancement` labels, so if you switch to your own label scheme, update the `labels` entries in that file as well.

### 如何删除 / Remove

- 删除文件 / Delete: 可以只删其中一个。删 `CHANGELOG.md` 就只剩自动生成的发布说明；删 `.github/release.yml` 则保留手写变更日志。
- 同步修改 / Update: 删除 `CHANGELOG.md` 时，要改 `CONTRIBUTING.md`（它要求贡献者在 Unreleased 下记一笔，并链接到该文件）和 `.github/PULL_REQUEST_TEMPLATE.md`（自检清单里有更新变更日志这一项）；如果 `README.md` 里也链接了它，一并删掉。删除 `.github/release.yml` 时，确认 `bug_report.yml`、`feature_request.yml` 里的标签设置是否还有意义。
- 失去什么 / What you lose: 没有 `CHANGELOG.md`，使用者只能翻提交历史来判断版本之间的差异；没有 `release.yml`，发布说明退回未分类的合并请求列表，`bug` 和 `enhancement` 标签不再起分组作用。

You can remove either file on its own: dropping `CHANGELOG.md` leaves you with generated release notes only, dropping `.github/release.yml` leaves you with a hand-written changelog. When you delete `CHANGELOG.md`, update `CONTRIBUTING.md`, which asks contributors to add an entry under Unreleased and links to the file, and `.github/PULL_REQUEST_TEMPLATE.md`, whose checklist includes updating the changelog; remove the link from `README.md` too if there is one. Without `CHANGELOG.md`, users have to read the commit history to tell versions apart; without `release.yml`, release notes fall back to an uncategorised list of pull requests and the `bug` and `enhancement` labels no longer group anything.

## M10 变更日志自动化 / Changelog automation

文件 / Files: 无 / none · 级别 / Level: 可选，只推荐 / Optional, recommendation only

### 为什么需要 / Why

项目大了以后，手写变更日志容易漏记，也容易和发布节奏脱节。这时可以让工具从提交或变更片段里生成日志。

Once a project grows, a hand-written changelog is easy to forget and easy to let drift out of sync with releases. At that point a tool can generate it from commits or from change files.

模板默认不启用任何工具，也不带任何文件 —— 对个人项目来说，M09 的手写变更日志加上平台自动生成的发布说明已经够用，而且零依赖。

The template enables nothing and ships no file for this module: for a personal project, the hand-written changelog from M09 plus the platform's generated release notes is enough, and it adds no dependencies.

### 如何选择 / How to choose

| 项目类型 / Project type | 推荐工具 / Recommended tool | 许可证 / License | 说明 / Notes |
|---|---|---|---|
| Node 项目 / Node projects | changesets | MIT | 每个改动写一个变更片段，发版时汇总；与 npm 发布流程契合 / A change file per change, aggregated at release time; fits the npm publishing flow |
| 非 Node 项目 / Non-Node projects | git-cliff | Apache-2.0 / MIT | 单一可执行文件，从提交历史生成，不绑定任何语言生态 / A single binary that generates from commit history, tied to no language ecosystem |
| 采用 Conventional Commits 且希望自动发起发版合并请求 / Conventional Commits plus automated release pull requests | release-please | Apache-2.0 | 自动维护版本号并开发版合并请求，要求提交信息严格规范 / Maintains the version and opens release pull requests for you, but requires disciplined commit messages |

三个工具各自是所属生态里认可度最高的，按项目类型取舍即可，不必比较谁更好。它们的认可度数据记在 [选型清单 / Selection list](SOURCES.md)。

Each of the three is the most widely adopted option in its own ecosystem, so pick by project type rather than trying to rank them. Their adoption figures are recorded in the [Selection list](SOURCES.md).

## M11 自动检查 / Continuous integration

文件 / Files: [`ci.yml`](../workflows/ci.yml) · 级别 / Level: 推荐 / Recommended

### 为什么需要 / Why

每次推送和合并请求都自动跑一遍，坏掉的改动在合并之前就会被拦住。模板里的 `lint` 作业还会检查工作流里所有动作是否都固定到了完整提交哈希 —— 这是与语言无关、又实实在在提升供应链安全的一项检查。

Every push and pull request runs the workflow automatically, so a broken change is caught before it is merged. The `lint` job in the template also checks that every action used in a workflow is pinned to a full commit hash, which is the one supply-chain check that is worth running in any language.

模板自带的是一个空骨架：`test` 作业只打印一行提示就成功退出，所以在空仓库上也一定能通过。

What ships is a skeleton: the `test` job prints a line and exits successfully, so it passes even on an empty repository.

### 如何定制 / Customize

在文件里标注的位置补上你项目真实的 lint 和 test 步骤（安装依赖、跑测试）。新增任何第三方动作时，都要按 [固定动作版本 / Pinning actions](#固定动作版本--pinning-actions) 固定哈希，否则 `lint` 作业会直接失败。

Add your project's real lint and test steps (installing dependencies, running tests) at the marked places in the file. Whenever you add a third-party action, pin it as described in [Pinning actions](#固定动作版本--pinning-actions), otherwise the `lint` job fails outright.

### 如何删除 / Remove

- 删除文件 / Delete: `.github/workflows/ci.yml`（如果这是唯一的工作流，整个 `.github/workflows/` 目录也可以一起删）。
- 同步修改 / Update: `README.md` 顶部有一枚指向这个工作流的 CI 徽章，删掉它，否则徽章会一直显示 no status；`CONTRIBUTING.md` 和 `.github/PULL_REQUEST_TEMPLATE.md` 里如果提到 `ci.yml` 必须通过，也一并改写。
- 失去什么 / What you lose: 推送和合并请求不再自动检查，动作哈希固定的检查也随之消失；`.github/dependabot.yml` 仍然照常运行，但已经没有工作流文件可更新，实际上等于空转。

Delete `.github/workflows/ci.yml` (and the whole `.github/workflows/` directory if that was the only workflow). Remove the CI badge at the top of `README.md` that points at this workflow, or it will read "no status" forever. Afterwards nothing checks pushes and pull requests automatically and the hash-pinning check goes away; `.github/dependabot.yml` keeps running but has no workflow file left to update, so it effectively does nothing.

## M12 依赖自动更新 / Dependency updates

文件 / Files: [`dependabot.yml`](../dependabot.yml) · 级别 / Level: 推荐 / Recommended

### 为什么需要 / Why

动作固定到哈希以后就不会自动跟进上游更新，安全修复也拿不到。Dependabot 每周检查一次，发现新版本就提一个合并请求，并顺手把行尾的版本注释一起更新。

Once actions are pinned to a commit hash they stop following upstream, security fixes included. Dependabot checks weekly, opens a pull request when a new version appears, and updates the version comment at the end of the line along with the hash.

### 如何定制 / Customize

模板只配置了 `github-actions` 这一个生态。按项目语言追加对应的生态（`npm`、`pip`、`gomod` 等），写法见 [按语言补充 / Adding language-specific rules](#按语言补充--adding-language-specific-rules)。

The template configures only the `github-actions` ecosystem. Add the ones your project uses (`npm`, `pip`, `gomod` and so on); see [Adding language-specific rules](#按语言补充--adding-language-specific-rules).

### 如何删除 / Remove

- 删除文件 / Delete: `.github/dependabot.yml`。
- 同步修改 / Update: 不需要改其他文件，没有任何项目文件引用它。
- 失去什么 / What you lose: 已经固定的哈希不再自动升级，`ci.yml` 里的动作会停留在当前版本，安全更新要靠你自己定期手动查（查哈希的命令见下一节）；仓库的 Security 标签下也不再有依赖更新提醒。

Delete `.github/dependabot.yml`. No other file references it, so nothing else needs changing. Afterwards pinned hashes are never bumped automatically, the actions in `ci.yml` stay on their current versions, and keeping up with security updates becomes a manual chore (the command for looking up a hash is in the next section); the repository's Security tab also stops surfacing dependency update alerts.

## M13 编辑器格式配置 / EditorConfig

文件 / Files: [`.editorconfig`](../../.editorconfig) · 级别 / Level: 可选 / Optional

### 为什么需要 / Why

它统一编码、换行符、缩进和文件末尾换行，让不同编辑器的协作者产出一致的空白，避免「整个文件都变了」式的差异。主流编辑器原生支持或有官方插件。

It unifies encoding, line endings, indentation and the final newline so that collaborators on different editors produce consistent whitespace, instead of diffs where the whole file appears to have changed. Mainstream editors support it natively or through an official plugin.

这个模块默认就启用：它只影响本地编辑器的空白处理，不会在 GitHub 页面或协作流程里产生可见效果，所以不需要你手动开启。

This module is on by default: it only affects whitespace handling in your local editor and has no visible effect on GitHub pages or on the collaboration flow, so there is nothing to switch on.

### 如何定制 / Customize

模板只设了通用项（UTF-8、LF、末尾换行、去掉行尾空格、YAML 两空格缩进）。按语言补上缩进规则，例如给 `[*.py]` 设四空格、给 `[*.go]` 设制表符。

The template sets only the general rules (UTF-8, LF, final newline, no trailing whitespace, two-space indentation for YAML). Add per-language indentation, for example four spaces under `[*.py]` or tabs under `[*.go]`.

### 如何删除 / Remove

- 删除文件 / Delete: `.editorconfig`。
- 同步修改 / Update: 不影响其他文件；只有当你在 `CONTRIBUTING.md` 的开发环境一节里提到过它时，才要删掉那句话。
- 失去什么 / What you lose: 各人的编辑器各按各的默认设置走，缩进和行尾空白的差异会混进提交里。

Delete `.editorconfig`. No other file is affected; the only thing to check is whether the Development setup section of `CONTRIBUTING.md` mentions it, in which case drop that sentence. Afterwards every editor falls back to its own defaults and inconsistent indentation and trailing whitespace start slipping into commits.

## M14 提交前检查 / Pre-commit hooks

文件 / Files: [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) · 级别 / Level: 可选 / Optional

### 为什么需要 / Why

在提交之前就把行尾空格、文件末尾换行、YAML 语法错误、遗留的冲突标记和超大文件挡掉，比等自动检查跑完再回来修快得多。

It catches trailing whitespace, missing final newlines, broken YAML, leftover conflict markers and oversized files before the commit is made, which is far quicker than waiting for CI and coming back to fix them.

### 如何定制 / Customize

装好 pre-commit 之后，在仓库里运行一次 `pre-commit install`，钩子才会生效 —— 不运行这条命令，这个文件什么都不做。之后可以按语言追加钩子（格式化、lint 等）。`rev` 已经固定到提交哈希并带上 `# frozen:` 版本注释，升级时保持这个写法。

After installing pre-commit, run `pre-commit install` once in the repository; until you do, this file does nothing at all. You can then add language-specific hooks (formatters, linters). The `rev` values are pinned to commit hashes with a `# frozen:` version comment; keep that style when you upgrade.

### 如何删除 / Remove

- 删除文件 / Delete: `.pre-commit-config.yaml`。已经运行过 `pre-commit install` 的人还要运行 `pre-commit uninstall` 清掉本地钩子。
- 同步修改 / Update: 不影响其他文件；如果 `CONTRIBUTING.md` 的开发环境一节里写了安装步骤，删掉那几行。
- 失去什么 / What you lose: 格式问题只能等自动检查或审阅时才被发现。

Delete `.pre-commit-config.yaml`; anyone who already ran `pre-commit install` should also run `pre-commit uninstall` to clear the local hook. No other file is affected, though you should drop the installation steps from the Development setup section of `CONTRIBUTING.md` if they are there. Afterwards formatting problems surface only in CI or in review.

## M15 代码负责人 / Code owners

文件 / Files: [`CODEOWNERS`](../CODEOWNERS) · 级别 / Level: 可选 / Optional

### 为什么需要 / Why

它让 GitHub 在改动到指定路径时自动请求对应的人或团队来审阅，不用每次手动点。单人项目用处不大，有协作者之后才值得开。

It makes GitHub request a review from the right person or team automatically whenever a pull request touches a given path, instead of you adding reviewers by hand. For a solo project it adds little; it starts paying off once you have collaborators.

### 如何定制 / Customize

模板里所有行都是注释，所以默认不生效。取消注释并把所有者换成你的用户名或团队，例如 `* @your-name` 表示整个仓库都由你审阅。所有者必须对仓库有写权限，否则那条规则会被忽略。

Every line in the template is commented out, so nothing is in effect by default. Uncomment a line and put in your own user name or team, for example `* @your-name` to own the whole repository. An owner must have write access, otherwise the rule is silently ignored.

### 如何删除 / Remove

- 删除文件 / Delete: `.github/CODEOWNERS`。
- 同步修改 / Update: 不影响其他文件，没有任何项目文件引用它。
- 失去什么 / What you lose: 只是失去自动请求审阅这一便利。由于模板里的内容全是注释，删不删在功能上没有区别；如果你在分支保护或规则集里启用了「需要代码负责人审阅」，删除后那条规则将没有可匹配的所有者，务必一并调整规则设置。

Delete `.github/CODEOWNERS`. No other file references it. All you lose is the automatic reviewer request, and since the shipped file is entirely comments there is no functional difference either way. One caveat: if you enabled "require review from Code Owners" in branch protection or a ruleset, that rule will have no owners left to match, so adjust the ruleset as well.

## M16 赞助入口 / Funding

文件 / Files: [`FUNDING.yml`](../FUNDING.yml) · 级别 / Level: 可选 / Optional

### 为什么需要 / Why

填好之后，仓库页面上会出现一个 Sponsor 按钮，给愿意资助的人一条明确的路径。

Once it is filled in, a Sponsor button appears on the repository page, giving anyone who wants to support the project an obvious route.

这个文件必须放在 `.github/` 目录下才会被识别。

The file is only recognised when it sits in the `.github/` directory.

### 如何定制 / Customize

模板只保留了 `github:` 和 `custom:` 两个键，值都是空的，所以默认不会出现赞助按钮。给其中一个键填上值就会生效：`github:` 填 GitHub 用户名或组织名，`custom:` 填你自己的收款页面链接。不需要的键删掉，不要留空值。

The template keeps only the `github:` and `custom:` keys, both empty, so no Sponsor button appears by default. Filling in either one switches it on: `github:` takes a GitHub user or organization name, `custom:` takes a link to your own funding page. Delete the key you do not need rather than leaving it empty.

### 如何删除 / Remove

- 删除文件 / Delete: `.github/FUNDING.yml`。
- 同步修改 / Update: 不影响其他文件，没有任何项目文件引用它。
- 失去什么 / What you lose: 没有赞助按钮。由于模板里的值本来就是空的，删除前后的页面表现一样。

Delete `.github/FUNDING.yml`. No other file references it. You lose the Sponsor button, but since the shipped values are empty the page looks the same before and after.

## 按语言补充 / Adding language-specific rules

模板刻意不绑定任何语言，以下三处需要你按项目实际使用的语言补齐。

The template deliberately stays language-neutral. These three places are where you fill in what your project actually uses.

- **忽略规则 / Ignore rules**：到 github.com/github/gitignore 找到对应语言的模板（如 `Python.gitignore`、`Node.gitignore`），把内容追加到 [`.gitignore`](../../.gitignore) 末尾，前面加一行注释标明来源和语言。模板自带的是通用规则，不要删。
- **自动检查 / CI steps**：在 [`ci.yml`](../workflows/ci.yml) 标注的位置补上安装依赖、lint 和测试的步骤。新增第三方动作要固定哈希，见下一节。
- **依赖更新 / Dependency ecosystems**：在 [`dependabot.yml`](../dependabot.yml) 的 `updates` 下追加一段，`package-ecosystem` 填 `npm`、`pip`、`gomod`、`cargo` 等，`directory` 指向清单文件所在目录，`schedule` 沿用每周一次即可。

Grab the matching template from github.com/github/gitignore (for example `Python.gitignore` or `Node.gitignore`) and append it to [`.gitignore`](../../.gitignore) with a comment naming the source and language, keeping the general rules that ship with the template. Add the install, lint and test steps for your language at the marked places in [`ci.yml`](../workflows/ci.yml), pinning any new third-party action as described below. Then add an entry under `updates` in [`dependabot.yml`](../dependabot.yml) with `package-ecosystem` set to `npm`, `pip`, `gomod`, `cargo` and so on, `directory` pointing at the folder holding the manifest, and the same weekly schedule.

## 固定动作版本 / Pinning actions

工作流里的动作必须固定到完整的 40 位提交哈希，而不是标签。标签可以被重新指向，哈希不会，这是防止上游被篡改后悄悄影响你仓库的唯一可靠做法。

Actions used in a workflow must be pinned to a full 40-character commit hash, never to a tag. Tags can be moved, hashes cannot, and this is the only reliable way to stop a compromised upstream from silently affecting your repository.

1. 查询某个版本对应的哈希：

   ```bash
   gh api repos/OWNER/ACTION/commits/vX.Y.Z --jq .sha
   ```

2. 按下面的写法引用，行尾的注释记录人读的版本号：

   ```yaml
   uses: owner/action@<40 位哈希> # vX.Y.Z
   ```

3. Dependabot 升级哈希时，会把行尾的版本注释一起更新，所以这条注释始终可信。
4. [`ci.yml`](../workflows/ci.yml) 的 `lint` 作业会检查所有工作流文件，只要有一处没固定哈希就直接失败。
5. 更多背景见官方的[安全使用参考](https://docs.github.com/en/actions/reference/security/secure-use)。

Look up the hash for a version with the `gh api` command above, reference the action with the hash plus a trailing version comment, and let Dependabot keep both in sync when it upgrades. The `lint` job in [`ci.yml`](../workflows/ci.yml) scans every workflow file and fails if a single reference is not pinned. The official [secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) has the background.

## 账号级默认文件 / Account-level default files

在你的账号下建一个名叫 `.github` 的仓库，把 `CODE_OF_CONDUCT.md`、`CONTRIBUTING.md`、`SECURITY.md` 等社区健康文件放进去，它们就会成为你名下所有仓库的默认内容 —— 仓库自己有同名文件时，以仓库里的为准。

Create a repository named `.github` under your account and put community health files such as `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md` and `SECURITY.md` in it: they then serve as defaults for every repository you own, and a repository's own copy always wins.

有两条例外值得记住：

- **Issue 模板是「要么全用仓库的，要么全用账号的」**：只要仓库里有合法的 Issue 模板或 `config.yml`，账号级 `.github/ISSUE_TEMPLATE` 里的默认模板就会整体失效，不会和仓库的模板混在一起。本模板自带 M07，所以从它生成的仓库都属于这种情况。
- **许可证不能由账号统一提供**：`LICENSE` 不在可继承的文件之列，每个仓库都必须自带一份。

Two exceptions are worth remembering. Issue templates are all-or-nothing: as soon as a repository has its own valid issue templates or `config.yml`, the defaults in the account-level `.github/ISSUE_TEMPLATE` stop applying entirely rather than being merged in, and since this template ships M07, every repository generated from it is in that situation. And a license cannot be provided centrally: `LICENSE` is not among the inheritable files, so every repository needs its own.

官方说明：[创建默认社区健康文件 / Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)。

## 中文译本 / Chinese translations

模板里的协作文件默认用英文，因为开源协作的默认语言是英文，英文版本也最容易被外部贡献者读懂。如果你的项目主要面向中文使用者，可以把这些文件换成官方中文译本，或者在英文正文旁附一条译本链接。

The collaboration files in the template are in English, because English is the default language of open-source collaboration and the version outside contributors are most likely to read. If your project is aimed mainly at Chinese-speaking users, you can replace these files with the official Chinese translations, or link a translation alongside the English text.

| 文件 / File | 官方中文译本 / Official Chinese translation |
|---|---|
| `CODE_OF_CONDUCT.md` | https://www.contributor-covenant.org/zh-cn/version/2/1/code_of_conduct/ |
| `CHANGELOG.md` | https://keepachangelog.com/zh-CN/1.1.0/ |
| 版本号规则 / Versioning | https://semver.org/lang/zh-CN/ |
| `CONTRIBUTING.md` | https://opensource.guide/zh-hans/starting-a-project/ |

Contributor Covenant 还有其他语种的译本，列表见 https://www.contributor-covenant.org/translations/ 。替换译本时注意保留文件第一行的来源注释。

Contributor Covenant is available in other languages too; the list is at https://www.contributor-covenant.org/translations/ . When you swap in a translation, keep the source comment on the first line of the file.

## 模板版本追溯 / Tracing the template version

生成的仓库里不留任何模板版本标记，骨架保持干净。想知道自己是基于哪个版本生成的，用仓库初始提交的日期对照模板的[变更记录 / Changelog](CHANGELOG.md)：从模板生成的仓库只有一个初始提交，找到日期不晚于它的那个版本即可。

Nothing in a generated repository records which template version it came from, so the skeleton stays clean. To find out, compare the date of your repository's initial commit against the template's [changelog](CHANGELOG.md): a repository created from a template has exactly one initial commit, so the release dated no later than it is the one you started from.

可选做法：在你自己的 `CHANGELOG.md` 里记一笔 `Created from Chef's Pick OSS Starter vX.Y.Z`。这一步纯属可选，只是省得以后再查。

Optional: add a line such as `Created from Chef's Pick OSS Starter vX.Y.Z` to your own `CHANGELOG.md`. It is not required, it just saves you the lookup later.

## 更换许可证 / Changing the license

模板默认是 MIT：宽松、短、认可度最高。要换成别的许可证，按三步走。

The template ships MIT: permissive, short and the most widely adopted. To switch, do three things.

1. 到 [choosealicense.com](https://choosealicense.com/licenses/mit/) 比较各个许可证的条款，挑一个适合你项目的。
2. 用新许可证的完整原文替换 [`LICENSE`](../../LICENSE) 的全部内容，填好年份和版权人。原文不要改写，GitHub 靠比对原文识别许可证类型，改过之后仓库页面上可能显示不出许可证名称。
3. 修改 [`README.md`](../../README.md) 的 License 一节，把里面的许可证名称改成新的。

Compare the terms at [choosealicense.com](https://choosealicense.com/licenses/mit/) and pick one, replace the entire contents of [`LICENSE`](../../LICENSE) with the new license's full text and fill in the year and the copyright holder, and update the license name in the License section of [`README.md`](../../README.md). Do not reword the license text: GitHub identifies the license by matching it, and an edited copy may stop being recognised.
