# Chef's Pick OSS Starter · 主厨精选开源仓库起步模板

本模板为一个新的开源仓库准备好协作所需的全部基础文件。每个模块都选用社区公认的佼佼者，开箱即用；每一项选择都注明选定来源、认可度证据和核实日期，不凭个人偏好拍板。

This template gives a new open source repository every file it needs to collaborate. Each module uses a pick the community already recognizes, ready to use out of the box, and every choice states its source, its adoption evidence, and the date it was verified — never just the author's taste.

> 这是模板的起步引导页。你的项目说明在根目录的 [README.md](../README.md)，完成起步并删除本页后，它会显示在这里。
>
> This is the template's setup guide page. Your own project README lives at [README.md](../README.md); once you finish setup and delete this page, that file becomes the repository's front page.

## 你会得到什么 / What you get

### 必需 / Required

- `README.md` — 项目说明 / Project readme（M01）
- `LICENSE` — 许可证 / License（M02）
- `.gitignore` — 忽略规则 / Ignore rules（M03）

### 推荐 / Recommended

- `CODE_OF_CONDUCT.md` — 行为准则 / Code of conduct（M04）
- `CONTRIBUTING.md` — 贡献指南 / Contributing guide（M05）
- `SECURITY.md` — 安全策略 / Security policy（M06）
- `.github/ISSUE_TEMPLATE/bug_report.yml`、`.github/ISSUE_TEMPLATE/feature_request.yml`、`.github/ISSUE_TEMPLATE/config.yml` — Issue 表单 / Issue forms（M07）
- `.github/PULL_REQUEST_TEMPLATE.md` — 合并请求模板 / Pull request template（M08）
- `CHANGELOG.md`、`.github/release.yml` — 变更日志与发布说明 / Changelog and release notes（M09）
- `.github/workflows/ci.yml` — 自动检查 / Continuous integration（M11）
- `.github/dependabot.yml` — 依赖自动更新 / Dependency updates（M12）

### 可选 / Optional

- `.editorconfig` — 编辑器格式配置 / EditorConfig（M13）
- `.pre-commit-config.yaml` — 提交前检查 / Pre-commit hooks（M14）
- `.github/CODEOWNERS` — 代码负责人 / Code owners（M15）
- `.github/FUNDING.yml` — 赞助入口 / Funding（M16）

变更日志自动化（M10）只给出推荐，不附带文件，由你按项目类型选择。

Changelog automation (M10) ships as a recommendation only: it adds no files, and you pick the tool that suits your project.

## 主厨精选一览 / The picks at a glance

<!-- summary:start -->
| 模块 / Module | 选定来源 / Pick | 认可度 / Adoption | 核实日期 / Verified |
|---|---|---|---|
| M01 项目说明 / README | Best-README-Template | ★ 16,360 (othneildrew/Best-README-Template) | 2026-09-18 |
| M02 许可证 / License | choosealicense.com（MIT） | 平台官方功能 / Official platform feature | 2026-09-18 |
| M03 忽略规则 / Ignore rules | github/gitignore（Global） | ★ 175,816 (github/gitignore) | 2026-09-18 |
| M04 行为准则 / Code of Conduct | Contributor Covenant 2.1 | 事实标准 / De facto standard（454 adopters） | 2026-09-18 |
| M05 贡献指南 / Contributing guide | GitHub Open Source Guides | ★ 15,685 (github/opensource.guide) | 2026-09-18 |
| M06 安全策略 / Security policy | GitHub 安全策略 + 私有漏洞报告 | 平台官方功能 / Official platform feature | 2026-09-18 |
| M07 Issue 表单 / Issue forms | GitHub Issue Forms | 平台官方功能 / Official platform feature | 2026-09-18 |
| M08 合并请求模板 / Pull request template | GitHub 合并请求模板 | 平台官方功能 / Official platform feature | 2026-09-18 |
| M09 变更日志与发布说明 / Changelog & release notes | Keep a Changelog 1.1.0 + SemVer 2.0.0 | ★ 6,702 (olivierlacan/keep-a-changelog) | 2026-09-18 |
| M10 变更日志自动化 / Changelog automation | changesets、git-cliff、release-please（只推荐） | ★ 12,408 (changesets/changesets) | 2026-09-18 |
| M11 自动检查 / Continuous integration | actions/starter-workflows 的 Simple workflow | ★ 12,082 (actions/starter-workflows) | 2026-09-18 |
| M12 依赖自动更新 / Dependency updates | GitHub Dependabot | 平台官方功能 / Official platform feature | 2026-09-18 |
| M13 编辑器格式配置 / EditorConfig | EditorConfig | ★ 3,450 (editorconfig/editorconfig) | 2026-09-18 |
| M14 提交前检查 / Pre-commit hooks | pre-commit + pre-commit-hooks | ★ 15,581 (pre-commit/pre-commit) | 2026-09-18 |
| M15 代码负责人 / Code owners | GitHub CODEOWNERS | 平台官方功能 / Official platform feature | 2026-09-18 |
| M16 赞助入口 / Funding | GitHub 赞助按钮 | 平台官方功能 / Official platform feature | 2026-09-18 |<!-- summary:end -->

[完整选型清单 / Full selection list](chefs-pick/SOURCES.md)

## 选型原则 / How we pick

选型按固定顺序取舍，只看 Star 数不够：

1. 社区认可度更高的方案优先。
2. 认可度相当时，选择对仓库持有者更容易起步的方案，例如步骤更少、无需额外依赖，或由平台内置。
3. 仍然同样合格时，才按作者个人偏好选择，并写明这是第 3 级。

Picks follow a fixed order, and star counts alone are not enough:

1. The option with higher community adoption wins.
2. When adoption is comparable, the option that is easier to start with wins — fewer steps, no extra dependency, or built into the platform.
3. Only when options remain equally qualified does the author's preference decide, and it is labeled as such.

认可度证据必须注明类型：精确 Star 数、四舍五入的 Star 数、估算使用人数、平台官方功能、事实标准（附具体采用者）或"未取得"。数字一律如实记录，不作估计。

Adoption evidence always states its type: exact stars, rounded stars, estimated users, official platform feature, de facto standard (with named adopters), or not available. Numbers are recorded as measured, never guessed.

## 快速开始 / Quick start

1. 点击 **Use this template** 创建你自己的仓库。 / Click **Use this template** to create your own repository.
2. 按 [起步清单 / Setup checklist](chefs-pick/SETUP.md) 完成定制，大约 15 分钟。 / Work through the [起步清单 / Setup checklist](chefs-pick/SETUP.md); it takes about 15 minutes.
3. 需要了解某个模块时，查阅 [模块讲解 / Module guide](chefs-pick/GUIDE.md)。 / Whenever you want to know what a module does, read the [模块讲解 / Module guide](chefs-pick/GUIDE.md).

（可选）项目发展为多人协作后，参阅 [升级为团队项目 / Growing into a team project](chefs-pick/UPGRADE-TO-TEAM.md)

## 注意事项 / Good to know

- **自带的 Issue 表单会覆盖账号级默认模板。** 本模板带有合法的 Issue 表单和配置，因此你账号级 `.github` 仓库里的默认 Issue 模板会整体失效。 / **The bundled issue forms override your account-level defaults.** Because this template ships valid issue forms and config, the default issue templates in your account-level `.github` repository stop applying entirely.
- **私有漏洞报告和讨论区需要手动开启。** 两者都是仓库设置中的开关，模板无法代为打开，起步清单里有对应步骤。 / **Private vulnerability reporting and Discussions must be enabled by hand.** Both are repository settings that no template can switch on for you; the setup checklist covers them.
- **从模板生成的仓库不会随模板自动更新。** 需要跟进改动时，请关注模板的 [CHANGELOG](chefs-pick/CHANGELOG.md)，自行挑选要同步的内容。 / **A repository generated from this template does not track it.** To follow later changes, watch the template's [CHANGELOG](chefs-pick/CHANGELOG.md) and port what you want.

## 完成后清理 / Clean up when done

完成起步后删除起步引导层，你的项目说明就会成为仓库首页，仓库里也不再留下模板自身的痕迹。

Once setup is done, remove the guide layer: your own readme becomes the repository's front page, and nothing of the template's own identity remains.

```bash
git rm -r .github/README.md .github/chefs-pick
git commit -m "chore: remove template guide"
```

在网页上操作时，删除这个文件和 `.github/chefs-pick` 目录即可，效果相同。

On the web, delete this file and the `.github/chefs-pick` directory; the result is the same.

## 反馈与联系 / Feedback and contact

- 根目录的 `CODE_OF_CONDUCT.md` 和 `SECURITY.md` 是供使用者定制的骨架，其中的联系邮箱和 Issue 入口链接都是占位符，在模板仓库里不可用，请不要照着它们联系本模板。 / The root `CODE_OF_CONDUCT.md` and `SECURITY.md` are skeletons for you to fill in: their contact addresses and issue links are placeholders and do not work in the template repository itself, so please do not use them to reach us.
- 本模板仓库自身的安全问题，请在 Security 标签页用 **Report a vulnerability** 私下报告。 / For a security issue in this template repository, report it privately from the Security tab with **Report a vulnerability**.
- 其他反馈请在本仓库提 Issue，或到 Discussions 讨论；涉及行为准则的严重问题，可以使用 GitHub 的内容举报功能向 GitHub 举报（"接受内容举报"设置只对组织账号的公共仓库开放）。 / For anything else, open an issue here or start a discussion; for a serious code of conduct problem, you can report the content to GitHub itself (the "reported content" setting is only available to public repositories owned by an organization).

## 许可证 / License

- 本模板以 MIT 发布，全文见 [LICENSE](chefs-pick/LICENSE)。 / This template is released under the MIT license; see [LICENSE](chefs-pick/LICENSE).
- 由本模板生成的项目无需保留模板署名，可以自由替换版权人，也可以更换许可证。 / Projects generated from this template need not keep any attribution to it: replace the copyright holder, or choose a different license entirely.
- `CODE_OF_CONDUCT.md` 的正文属于 Contributor Covenant，采用 CC-BY-4.0，须保留其 Attribution 段落。 / The body of `CODE_OF_CONDUCT.md` comes from the Contributor Covenant under CC-BY-4.0, and its Attribution section must be kept.
