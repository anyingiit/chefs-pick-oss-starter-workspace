<!-- anchor: setup-checklist -->
# 起步清单

[English](SETUP.md) · **简体中文**

> 英文版是规范版本。本页与 [SETUP.md](SETUP.md) 不一致时，以英文版为准。

<!-- translation-of: SETUP.md sha256:0000000000000000 -->

按顺序完成这份清单，大约需要 15 分钟。先替换占位符，再完成仓库设置和项目文件，最后移除本引导层。

<!-- anchor: placeholders -->
## 占位符

模板中的全部占位符登记在英文原文的 [Placeholders](SETUP.md#placeholders) 一节。那张表是唯一的一份，逐项列出占位符的名称、含义、出现的文件和示例值；名称、路径和示例都是标识符，不作翻译，所以这里不重复。

逐个替换，不要留下任何一个。

在清理引导层之前，用下面这条命令查找还没替换完的占位符；它排除了本层自己的登记表，所以不会把表格算进去。

```bash
git grep -n CHANGEME -- . ':(exclude).github/chefs-pick'
```

清理引导层之后，用这条命令做最终确认。

```bash
git grep -n CHANGEME
```

这两条命令都不应该有任何输出。

<!-- anchor: steps -->
## 步骤

| 编号 | 类型 | 步骤 | 如何确认 |
|---|---|---|---|
| S01 | 必做 | 按照上面的登记表，逐个替换占位符。 | 清理前的查找命令没有任何输出。 |
| S02 | 必做 | 在仓库首页的 `About`（齿轮图标）下填写项目描述，也可以顺便加上 `topics`。如果仓库属于某个组织，还需在 `Settings → Moderation options → Reported content` 开启举报内容功能；个人账号名下的仓库没有这项设置。 | 仓库首页右侧会显示这段描述，社区标准页面上与设置相关的各项也都已完成。 |
| S03 | 必做 | 在 `Settings → Advanced Security → Private vulnerability reporting` 开启私有漏洞报告功能（[官方文档](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)）。 | Security 标签页会显示 **Report a vulnerability**。 |
| S04 | 必做 | 在 `Settings → General → Features → Discussions` 开启 Discussions 功能（[官方文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/enabling-or-disabling-github-discussions-for-a-repository)）。如果决定不开启，请把两处都指向你自己的支持渠道：[`.github/ISSUE_TEMPLATE/config.yml`](../ISSUE_TEMPLATE/config.yml) 中的 discussions 链接，以及 [`CONTRIBUTING.md`](../../CONTRIBUTING.md) 的 Questions 一节。 | New issue 页面上的支持链接能打开，且 `CONTRIBUTING.md` 中提到的渠道与之一致。 |
| S05 | 必做 | 确认许可证：默认是 MIT。如果要换成别的，先在 [choosealicense.com](https://choosealicense.com/licenses/mit/) 选定，替换 [`LICENSE`](../../LICENSE) 文件，并相应更新 [`README.md`](../../README.md) 的 License 一节。 | 仓库首页显示的许可证与之一致。 |
| S06 | 必做 | 针对你项目所用的语言，补充三件事：来自 `github/gitignore` 的 `.gitignore` 规则；`ci.yml` 中的 lint 与 test 步骤，新增的任何 action 都要按 [模块讲解](GUIDE.md) 中 "Pinning actions" 一节所述固定到提交哈希；以及 `dependabot.yml` 中你用到的依赖生态。 | 推送之后 CI 能通过。 |
| S07 | 选做 | 逐个决定是否保留每个推荐和可选模块；[模块讲解](GUIDE.md) 说明了如何移除每一个模块。 | 保留下来的每个可选模块都已按其说明启用。 |
| S08 | 必做 | 运行 [模板首页](../README.md) 给出的清理命令，移除引导层。 | 仓库首页显示的是你自己的 `README.md`。 |
| S09 | 必做 | 运行最终检查。 | `Insights → Community Standards` 下的每一项都显示绿色勾选，`git grep -n CHANGEME` 没有任何输出，且 CI 通过。该页面只会列出你的账号类型支持的项目——比如举报内容功能，只出现在组织名下的公开仓库——所以列出的每一项都应该是你能够完成的。 |
