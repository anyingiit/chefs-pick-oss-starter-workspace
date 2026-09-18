# 契约：项目文件内容

对应需求：FR-007、FR-011、FR-014 ~ FR-024、FR-039；宪章原则 IV、V 及附加约束。决策依据：[research.md](../research.md) R4 ~ R16。

**通用规则**：
- 所有项目文件都用英文。
- 每个文件的第一行是来源注释，逐字内容见 [markers.md](./markers.md) §2.2；`LICENSE` 除外。
- 占位符只能使用 [markers.md](./markers.md) §1.2 登记表中列出的。
- 本文件中标为"逐字"的内容必须原样使用。标为"结构"的内容可以调整措辞，但必须包含列出的全部要素。
- 从上游获取文件的命令模板见 research §4。

---

## M01 `README.md`（结构）

以 Best-README-Template 的 `BLANK_README.md`（固定提交 `fc444eb7b04b2e4863f6080b1507a219e95103fa`）为基础精简，依次包含：

1. 第 1 行：来源注释。
2. `<a id="readme-top"></a>`。
3. `# Chefs Pick Oss Starter Workspace`，下一段为 `This is the development and maintenance workspace for the template repository.`。
4. 两个徽章，写在同一段：
   - `[![CI](https://github.com/anyingiit/chefs-pick-oss-starter-workspace/actions/workflows/ci.yml/badge.svg)](https://github.com/anyingiit/chefs-pick-oss-starter-workspace/actions/workflows/ci.yml)`
   - `[![License](https://img.shields.io/github/license/anyingiit/chefs-pick-oss-starter-workspace)](LICENSE)`
5. 一行两个链接，中间用 ` · ` 分隔：
   - `[Report a bug](https://github.com/anyingiit/chefs-pick-oss-starter-workspace/issues/new?template=bug_report.yml)`
   - `[Request a feature](https://github.com/anyingiit/chefs-pick-oss-starter-workspace/issues/new?template=feature_request.yml)`
6. 折叠目录：`<details><summary>Table of Contents</summary>` 中放一个有序列表，依次链接到 `#about-the-project`、`#getting-started`、`#usage`、`#contributing`、`#license`、`#contact`。
7. `## About The Project`：写 `This is the development and maintenance workspace for the template repository.`，再加一句 "See the [open issues](https://github.com/anyingiit/chefs-pick-oss-starter-workspace/issues) for planned features and known issues."
8. `## Getting Started`，包含两个小节：
   - `### Prerequisites`：列表中只有 `- Git`。
   - `### Installation`：给出 `git clone https://github.com/anyingiit/chefs-pick-oss-starter-workspace.git` 和 `cd chefs-pick-oss-starter-workspace`，写在 `sh` 代码块中。
9. `## Usage`：`sh` 代码块，内容为 `chefs-pick-oss-starter-workspace --help`。
10. `## Contributing`：链接到 `CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`，并说明安全问题见 `SECURITY.md`。三个链接都用相对路径。
11. `## License`：`Distributed under the MIT License. See [LICENSE](LICENSE) for details.`
12. `## Contact`：`Project link: [https://github.com/anyingiit/chefs-pick-oss-starter-workspace](https://github.com/anyingiit/chefs-pick-oss-starter-workspace)`。
13. 文件末尾：`<p align="right">(<a href="#readme-top">back to top</a>)</p>`。

**不得包含**：Built With、Roadmap、Acknowledgments、Top contributors（contrib.rocks）、社交账号链接、个人邮箱，以及 [markers.md](./markers.md) §1.3 列出的残留标记。

## M02 `LICENSE`（逐字）

取 `github/choosealicense.com@58267f8f2c5c0099810849cfd7677f52ae0c0eb3` 中 `_licenses/mit.txt` 的正文，处理方式如下：
- 去掉文件开头两个 `---` 之间的 front matter，以及紧随其后的空行。
- `[year]` 换成 `2026`，`[fullname]` 换成 `anyingiit`。方括号在 `sed` 中是字符类，必须转义，命令为 `sed -e 's/\[year\]/2026/' -e 's/\[fullname\]/anyingiit/'`。
- 不加来源注释，其余文字一个字符都不改。

处理后，第 1 行为 `MIT License`，第 3 行为 `Copyright (c) 2026 anyingiit`（C15 检查）。

## M03 `.gitignore`（逐字拼接）

```text
# Source: github/gitignore Global templates (CC0-1.0) — https://github.com/github/gitignore/tree/356fd7baab4c05e092194a41f64dbd5afc8817e4/Global
# Add the rules for your language or framework from https://github.com/github/gitignore
# (for example, append the contents of Python.gitignore or Node.gitignore below).

# --- Global/macOS.gitignore ---
<该文件在固定提交中的全文>

# --- Global/Windows.gitignore ---
<全文>

# --- Global/Linux.gitignore ---
<全文>

# --- Global/VisualStudioCode.gitignore ---
<全文>

# --- Global/JetBrains.gitignore ---
<全文>
```

- 五个上游文件都取自固定提交 `356fd7baab4c05e092194a41f64dbd5afc8817e4`，内容保持原样。
- 每段之间空一行，文件末尾只保留一个换行。
- **必须用命令逐字节拼接**，例如 `gh api ... --jq .content | base64 -d >> 文件`，不要用编辑器重新输入。原因是 `Global/macOS.gitignore` 中 `Icon[\r]` 和 `.HFS+ Private Directory Data[\r]` 两行的方括号里各有一个字面的回车符。拼接后 `grep -c $'\r' template/.gitignore` 必须输出 `2`。

## M04 `CODE_OF_CONDUCT.md`（逐字加替换）

1. 第 1 行：来源注释。第 2 行：空行。
2. 从第 3 行起，放入 `EthicalSource/contributor_covenant@7255a28d23d5bc296de2e4e4e9bb5ee1126f1345` 中 `content/version/2/1/code_of_conduct.md` 的内容，处理方式如下：
   - 删除开头的 TOML front matter（从第一行 `+++` 到第二行 `+++`，含这两行），并删除紧随其后的空行。
   - 把 `[INSERT CONTACT METHOD]` 换成 `leoycwan@gmail.com`。删除 front matter 之后全文只有一处；未删除 front matter 时，第 4 行的 `reportingPlaceholder` 也含这个字符串。方括号要转义，命令为 `sed -e 's/\[INSERT CONTACT METHOD\]/leoycwan@gmail.com/'`。
   - 其余内容一律不改，包括 `## Attribution` 段落及文末的全部链接引用定义。

C16 检查以下几点：
- 包含 `version 2.1`；
- 包含 `leoycwan@gmail.com`；
- 不包含 `[INSERT CONTACT METHOD]`；
- 不包含 `+++`；
- 包含 `## Attribution`。

## M05 `CONTRIBUTING.md`（结构，原创英文）

依次包含以下小节，一级标题为 `# Contributing`：
1. 开头的欢迎语，1 ~ 2 句。
2. `## Code of Conduct`：链接到 `CODE_OF_CONDUCT.md`，并说明参与即表示同意遵守。
3. `## Ways to contribute`：列出报告缺陷、建议功能、改进文档、提交代码。
4. `## Reporting bugs`：先搜索已有 Issue，然后通过 **Bug report** 表单（Issues → New issue）提交，并填完所有必填项。
5. `## Suggesting features`：通过 **Feature request** 表单提交，并说明想解决的问题。
6. `## Reporting security issues`：不要公开提交，按 `SECURITY.md` 的说明报告（相对链接）。
7. `## Submitting pull requests`：有序列表，依次为：
   1. Fork 仓库，并从 `main` 创建分支。
   2. 遵循现有代码风格。
   3. 为改动添加或更新测试。
   4. 如属值得记录的改动，在 `CHANGELOG.md` 的 `Unreleased` 下记一笔（相对链接）。
   5. 确认 CI 检查通过。
   6. 发起合并请求并填写模板。
8. `## Development setup`：链接到 `README.md#getting-started`。
9. `## Questions`：去 GitHub Discussions 的 Discussions 标签页提问，而不是开 Issue。

**不得包含**：外链到本仓库 Issue 页面的绝对链接（避免增加占位符），以及任何占位符。

## M06 `SECURITY.md`（结构）

1. 第 1 行：来源注释。
2. `# Security Policy`
3. `## Supported Versions`：先写一句 "Security updates are provided for the latest release only."，再放一张两行表格：`Latest release | :white_check_mark:` 和 `Older releases | :x:`。
4. `## Reporting a Vulnerability`，包含以下内容：
   - 加粗句：**Please do not report security vulnerabilities through public issues, discussions, or pull requests.**
   - 私下报告方式：打开 **Security** 标签页，选择 **Report a vulnerability**；或直接访问 `https://github.com/anyingiit/chefs-pick-oss-starter-workspace/security/advisories/new`。
   - 备用联系方式："If private vulnerability reporting is unavailable, email leoycwan@gmail.com."
   - 报告应包含的信息：漏洞描述与影响、复现步骤或概念验证、受影响的版本。
   - 最后一句："We will acknowledge your report and keep you informed as we investigate and fix the issue."（不承诺具体天数）

## M07 Issue 表单（逐字）

### `.github/ISSUE_TEMPLATE/bug_report.yml`

```yaml
# Source: GitHub issue forms (official) — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
name: Bug report
description: Report something that is not working as expected.
title: "[Bug]: "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to report a bug! Please search the existing issues first to avoid duplicates.
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Describe the actual behavior you observed.
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: List the steps needed to reproduce the problem.
      placeholder: |
        1. ...
        2. ...
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: Describe what you expected to happen instead.
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Project version, operating system, and any other relevant details.
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs or screenshots
      description: Paste any relevant log output. It will be formatted as code automatically.
      render: shell
    validations:
      required: false
```

### `.github/ISSUE_TEMPLATE/feature_request.yml`

```yaml
# Source: GitHub issue forms (official) — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
name: Feature request
description: Suggest an idea or improvement for this project.
title: "[Feature]: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for the suggestion! Please search the existing issues first to see if it has already been proposed.
  - type: textarea
    id: problem
    attributes:
      label: What problem would this solve?
      description: Describe the problem or need behind this request.
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Proposed solution
      description: Describe what you would like to happen.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      description: Describe any other solutions or workarounds you have considered.
    validations:
      required: false
  - type: textarea
    id: context
    attributes:
      label: Additional context
      description: Add any other context, links, or screenshots.
    validations:
      required: false
```

### `.github/ISSUE_TEMPLATE/config.yml`

```yaml
# Source: GitHub issue template chooser (official) — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
blank_issues_enabled: false
contact_links:
  - name: Questions and help
    url: https://github.com/anyingiit/chefs-pick-oss-starter-workspace/discussions
    about: Please ask and answer questions in GitHub Discussions.
  - name: Report a security vulnerability
    url: https://github.com/anyingiit/chefs-pick-oss-starter-workspace/security/advisories/new
    about: Please report security vulnerabilities privately, not in public issues.
```

C04 检查以下内容：
- 两个表单都有非空的 `name`、`description`、`labels` 和 `body`；
- `bug_report` 中 `what-happened`、`steps`、`expected`、`environment` 为必填；
- `feature_request` 中 `problem`、`solution` 为必填；
- `config.yml` 中 `blank_issues_enabled` 为 `false`，且至少有两个 `contact_links`，每个的 `url` 都以 `https://github.com/anyingiit/chefs-pick-oss-starter-workspace/` 开头。

## M08 `.github/PULL_REQUEST_TEMPLATE.md`（逐字）

```markdown
<!-- Source: GitHub pull request template (official) — https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository -->
## Description

<!-- What does this pull request change, and why? -->

## Related issue

Closes #

## Checklist

- [ ] Tests pass locally
- [ ] `CHANGELOG.md` is updated (if applicable)
- [ ] Documentation is updated (if applicable)
```

## M09 `CHANGELOG.md`（逐字）与 `.github/release.yml`（逐字）

```markdown
<!-- Source: Keep a Changelog 1.1.0 (MIT) — https://keepachangelog.com/en/1.1.0/ -->
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project structure.

[Unreleased]: https://github.com/anyingiit/chefs-pick-oss-starter-workspace/commits/main
```

```yaml
# Source: GitHub automatically generated release notes (official) — https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes
changelog:
  categories:
    - title: New Features
      labels:
        - enhancement
    - title: Bug Fixes
      labels:
        - bug
    - title: Other Changes
      labels:
        - "*"
```

C07 检查三个分类，要求标题和标签与上面完全一致。

## M11 `.github/workflows/ci.yml`（逐字）

```yaml
# Source: GitHub starter workflow "Simple workflow" (MIT) — https://github.com/actions/starter-workflows/blob/main/ci/blank.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

# The workflow token is read-only by default.
# Grant extra permissions to a single job only when that job needs them.
permissions:
  contents: read

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false

      - name: Check that actions are pinned to full commit SHAs
        shell: bash
        run: |
          # Every `uses:` must reference a full 40-character commit SHA followed by a
          # version comment, for example:
          #   uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
          # Local actions (./path) and Docker images (docker://) are skipped.
          set -euo pipefail
          unpinned="$(grep -RnE '^[[:space:]]*(-[[:space:]]+)?uses:' .github/workflows \
            | grep -vE "uses:[[:space:]]*['\"]?(\./|docker://)" \
            | grep -vE "@[0-9a-f]{40}['\"]?[[:space:]]+#[[:space:]]*v?[0-9]" || true)"
          if [ -n "$unpinned" ]; then
            echo "::error::Pin these actions to a full-length commit SHA with a version comment:"
            echo "$unpinned"
            exit 1
          fi
          echo "All actions are pinned to full-length commit SHAs."

      # Add your project's linters below this line.

  test:
    name: Test
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false

      # Replace the step below with your project's test command. Pin any setup
      # action you add to a full commit SHA, like the checkout step above.
      - name: Run tests
        run: echo "No tests yet. Replace this step with your project's test command."
```

上面的哈希检查脚本已在 2026-09-18 本机实测：
- 通过的情况：固定到哈希并注明版本的引用、本地动作、Docker 镜像、可复用工作流，以及出现在注释或脚本里的 `uses:` 字样。
- 被拦下的情况：版本标签、只有哈希但缺版本注释、`@main`。

C05 检查以下内容：
- 用 PyYAML 解析时，`on` 键会被读成布尔值 `True`，必须兼容这个键名；触发条件包含 `push`、`pull_request`、`workflow_dispatch`。
- 顶层 `permissions` 恰好是 `{contents: read}`。
- 存在 `lint` 和 `test` 两个作业。
- 所有 `uses` 的值都满足 `^[^@\s]+@[0-9a-f]{40}$`，且源文件对应行带有 `# v<数字>` 注释。
- 所有使用 `actions/checkout` 的步骤都设置了 `with.persist-credentials: false`。

## M12 `.github/dependabot.yml`（逐字）

```yaml
# Source: GitHub Dependabot (official) — https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference
# Add an entry for each package manager your project uses (see the link above).
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## M13 `.editorconfig`（逐字）

```ini
# Source: EditorConfig (official specification) — https://editorconfig.org
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.{yml,yaml}]
indent_style = space
indent_size = 2
```

## M14 `.pre-commit-config.yaml`（逐字）

```yaml
# Source: pre-commit and pre-commit-hooks (MIT) — https://pre-commit.com
# Optional: run `pre-commit install` once to run these checks before each commit.
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: 3e8a8703264a2f4a69428a0aa4dcb512790b2c8c  # frozen: v6.0.0
    hooks:
      - id: trailing-whitespace
        args: [--markdown-linebreak-ext=md]
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-merge-conflict
      - id: check-added-large-files
```

## M15 `.github/CODEOWNERS`（逐字，默认不生效）

```text
# Source: GitHub code owners (official) — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
# Optional. Uncomment the line below to automatically request a review from the
# repository owner on every pull request.
# * @anyingiit
```

C10 检查：文件中不能有非空且不以 `#` 开头的行。

## M16 `.github/FUNDING.yml`（逐字，默认不生效）

```yaml
# Source: GitHub sponsor button (official) — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository
# Optional. Add your usernames or links to show a "Sponsor" button on the repository page.
github: # Up to 4 GitHub Sponsors usernames, for example [octocat]
custom: # Up to 4 custom URLs, for example ["https://example.com/donate"]
```

C10 检查：解析后，所有键的值都为空（`null`）。
