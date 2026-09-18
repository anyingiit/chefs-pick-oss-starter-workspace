<!-- anchor: chefs-pick-oss-starter -->
# Chef's Pick OSS Starter

[English](README.md) · **简体中文**

> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。

<!-- translation-of: README.md sha256:78e378abcfaabf21 -->

本模板为新建的开源仓库提供协作所需的全部文件。每个模块都采用社区已广泛认可的选型，开箱即用；每一项选择都注明其来源、认可度证据和核实日期——而不仅仅是作者的个人偏好。

> 这是模板的起步引导页。你自己项目的说明文档位于 [README.md](../README.md)；完成设置并删除本页后，该文件将成为仓库的首页。

<!-- anchor: what-you-get -->
## 你会得到什么

<!-- anchor: required -->
### 必需

- `README.md` — 项目说明 (M01)
- `LICENSE` — 许可证 (M02)
- `.gitignore` — 忽略规则 (M03)

<!-- anchor: recommended -->
### 推荐

- `CODE_OF_CONDUCT.md` — 行为准则 (M04)
- `CONTRIBUTING.md` — 贡献指南 (M05)
- `SECURITY.md` — 安全策略 (M06)
- `.github/ISSUE_TEMPLATE/bug_report.yml`、`.github/ISSUE_TEMPLATE/feature_request.yml`、`.github/ISSUE_TEMPLATE/config.yml` — Issue 表单 (M07)
- `.github/PULL_REQUEST_TEMPLATE.md` — Pull Request 模板 (M08)
- `CHANGELOG.md`、`.github/release.yml` — 变更日志与发布说明 (M09)
- `.github/workflows/ci.yml` — 持续集成 (M11)
- `.github/dependabot.yml` — 依赖更新 (M12)

<!-- anchor: optional -->
### 可选

- `.editorconfig` — EditorConfig (M13)
- `.pre-commit-config.yaml` — Pre-commit 钩子 (M14)
- `.github/CODEOWNERS` — 代码所有者 (M15)
- `.github/FUNDING.yml` — 赞助信息 (M16)

变更日志自动化 (M10) 只作为推荐提供：它不添加任何文件，具体工具由你根据项目需要自行挑选。

<!-- anchor: the-picks-at-a-glance -->
## 主厨精选一览

16 个模块的选定来源、认可度证据和核实日期，汇总在英文原文的 [The picks at a glance](README.md#the-picks-at-a-glance) 一节。那张表由工具批量刷新，全模板只有一份，所以这里不另存一份。

完整选型清单见 [SOURCES.md](chefs-pick/SOURCES.md)，其中逐个模块记录了备选方案与未选原因。该文档只有英文版。

<!-- anchor: how-we-pick -->
## 选型原则

选型遵循固定的优先顺序，仅凭 Star 数并不足够：

1. 社区认可度更高的选项胜出。
2. 当认可度相当时，更易于上手的选项胜出——步骤更少、不需要额外依赖，或是平台内置功能。
3. 只有在各选项条件相当、难分高下时，才由作者的偏好决定，并会明确标注这一点。

认可度证据始终注明其类型：精确 Star 数、取整 Star 数、估算用户数、平台官方功能、事实标准（并列出采用者）、或无可用数据。数字均按实测记录，绝不臆测。

<!-- anchor: quick-start -->
## 快速开始

1. 点击 **Use this template** 创建属于你自己的仓库。
2. 按照 [起步清单](chefs-pick/SETUP.md) 逐步完成设置，大约需要 15 分钟。
3. 想了解某个模块的作用时，随时查阅 [模块说明](chefs-pick/GUIDE.md)。

（可选）当项目发展为多人协作项目后，参见 [升级为团队项目](chefs-pick/UPGRADE-TO-TEAM.md)。

<!-- anchor: good-to-know -->
## 注意事项

- **随附的 Issue 表单会覆盖你账号级别的默认设置。** 由于本模板自带了有效的 Issue 表单与配置，你账号级 `.github` 仓库中的默认 Issue 模板将完全失效。
- **私密漏洞报告和 Discussions 功能需要手动开启。** 这两项都是仓库设置，任何模板都无法替你打开；起步清单中会说明这两步。
- **由本模板生成的仓库不会跟踪模板本身。** 若想了解后续更新，请关注模板的 [变更日志](chefs-pick/CHANGELOG.md)，按需自行移植。

<!-- anchor: clean-up-when-done -->
## 完成后清理

设置完成后，移除引导层：你自己的说明文档将成为仓库首页，模板自身不再留下任何痕迹。

```bash
git rm -r .github/README.md .github/README.zh-CN.md .github/chefs-pick
git commit -m "chore: remove template guide"
```

如果在网页端操作，删除 `.github/README.md`、`.github/README.zh-CN.md` 和 `.github/chefs-pick` 目录，效果相同。

<!-- anchor: feedback-and-contact -->
## 反馈与联系

- 根目录下的 `CODE_OF_CONDUCT.md` 和 `SECURITY.md` 只是供你自行填写的骨架：其中的联系地址和 Issue 链接均为占位符，在模板仓库本身并不可用，请不要用它们联系我们。
- 如果发现本模板仓库自身存在安全问题，请通过 Security 标签页的 **Report a vulnerability** 私下提交。
- 其他事项请在此提交 Issue 或发起 Discussion；如遇严重的行为准则问题，也可以直接向 GitHub 举报该内容（"reported content" 设置仅面向由组织拥有的公开仓库开放）。

<!-- anchor: license -->
## 许可证

- 本模板依据 MIT 许可证发布，详见 [LICENSE](chefs-pick/LICENSE)。
- 由本模板生成的项目无需保留任何指向模板的署名：可以替换版权所有者，或直接选用其他许可证。
- `CODE_OF_CONDUCT.md` 的正文内容来自 Contributor Covenant，遵循 CC-BY-4.0 协议，其中的 Attribution 章节必须保留。
