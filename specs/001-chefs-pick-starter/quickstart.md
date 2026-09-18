# 验证指南：主厨精选开源仓库起步模板

本文件说明如何证明功能按规格工作，不包含实现代码。各文件的契约见 [contracts/](./contracts/)，校验项的定义见 [contracts/tooling.md](./contracts/tooling.md)。

**顺序很重要**：宪章要求 5 项发布门禁在**创建 Release 之前**全部通过，其中门禁 2（生成仓库首次自动检查通过）和门禁 4（社区标准全绿）只能用从模板生成的测试仓库验证。因此本文件的顺序是：A 本地验证 → B 发布内容与设置 → C 用测试仓库做发布前验证 → D 创建 Release。

## 0. 前提

- Python 3.10+ 和 PyYAML。缺少 PyYAML 时，运行 `python3 -m pip install pyyaml`。
- `bash`、`grep`。
- 已登录的 `gh`。只有刷新认可度数据时才需要。
- B、C、D 三部分需要维护者的 GitHub 账号，由维护者手动完成。

## A. 本地验证（开发工作区）

| 步骤 | 命令 | 期望结果 | 覆盖 |
|---|---|---|---|
| A1 单元测试 | `python3 -m unittest discover -s tools/tests` | `OK`。`template/` 尚未完成时，部分测试会显示为 skipped | 工具本身 |
| A2 结构校验 | `python3 tools/check_template.py` | 最后一行为 `Summary: 24 passed, 0 failed, 0 warned, 0 skipped`；未提供可选的 `UPGRADE-TO-TEAM.md` 时为 `23 passed, 0 failed, 0 warned, 1 skipped`（C19 跳过） | SC-003、SC-006、SC-007、SC-010、SC-012；FR-001 ~ FR-039 的静态部分 |
| A3 刷新认可度数据 | `python3 tools/verify_sources.py --write` | 退出码为 0；报告中没有 `ARCHIVED` 或未评估过的 `STALE` 出现在选定来源上 | 宪章原则 III；SC-008 |
| A4 发布门禁（自动部分） | `python3 tools/check_template.py --release` | 0 项失败 | 宪章发布门禁 1、3、5，以及门禁 2 中"核心要素齐全"的静态部分 |
| A5 校验耗时 | `time python3 tools/check_template.py` | 实际耗时不超过 5 秒 | plan 的 Performance Goals |
| A6 清理模拟与删除模拟 | 已包含在 A2 的 C13、C22 中 | 两项都是 PASS | FR-011 ~ FR-013；SC-007；发布门禁 3 |
| A7 哈希检查脚本 | 已包含在 A1 的 `test_ci_pin_check.py` 中 | 正例退出码为 0，反例退出码为 1 | FR-039；SC-012 |

`--only` 参数可以用来只运行某一项校验，例如编写某个文件时运行 `python3 tools/check_template.py --only C05`。

## B. 发布内容与设置（维护者手动完成）

1. 在 GitHub 上新建公开仓库 `chefs-pick-oss-starter`，默认分支为 `main`。
2. 把 `template/` 中的内容（包括隐藏文件）作为该仓库 `main` 分支的全部内容，任选一种方式：
   - **首次发布到空仓库时**（本步骤只适用于这一种情形）：先运行 `git subtree split --prefix=template -b publish`，再运行 `git push <模板仓库远程名> publish:main`。
   - **后续发布到已有内容的仓库时**：按仓库根目录 `README.md` 的 `Publishing` 一节操作。绝不要强制推送；subtree split 切出的历史与模板仓库没有共同祖先，强推会让 v1.0.0 标签指向的提交不再可达。
   - **直接复制**：克隆空的模板仓库，把 `template/` 下的所有内容复制进去，然后提交并推送。
   - 两种方式都**不要**把开发工作区中的其他目录推送到模板仓库。
3. 在仓库设置中完成以下几项：
   - 勾选 **Template repository**。
   - 按 FR-038 填写 About 简介和 Topics。
   - 开启 Private vulnerability reporting。
   - 开启 Discussions。
   - 仓库属于组织账号时，在 Settings → Moderation options → Reported content 开启内容举报（个人账号仓库没有这一项，见 research F10）。这一条与 SETUP 的 S02 同口径。
4. 确认 Insights → Community Standards 中各项都是绿勾（FR-035），并且 Actions 页面上 `main` 分支的 CI 通过。这里与 V4 同一口径：列出的项都应当能完成，出现无法开启的项时停止并报告，不得自行放行。
5. **不要在模板仓库上合并 Dependabot 的合并请求**。它们只是"有新版本"的提示，处理方式见起步引导层中 MAINTAINING 的"动作版本更新"一节：回到开发工作区更新后重新发布。直接在模板仓库合并，会让下一次发布推送被拒绝。

## C. 发布前验证（用模板生成一个测试仓库）

这一部分必须在创建 Release 之前完成。V1 对应发布门禁 2，V4 对应发布门禁 4。

| 场景 | 操作 | 期望结果 | 覆盖 |
|---|---|---|---|
| V1 首次 CI | 点击 **Use this template** 生成测试仓库，打开 Actions 页面 | 首次运行的 CI 通过，`Lint` 和 `Test` 两个作业都成功；记录整次运行的总耗时（两个作业并行）和每个作业的耗时，总耗时不超过 1 分钟 | 发布门禁 2；US1-AS4；SC-005；SC-012；plan 的 Performance Goals |
| V2 初始状态 | 查看测试仓库首页，克隆到本地后运行 `git grep -n CHANGEME -- . ':(exclude).github/chefs-pick'` | 首页显示起步引导页；搜索结果中只有登记表里的占位符；起步引导层以外没有模板身份字样 | US1-AS1、AS3、AS5 |
| V3 协作入口 | 点击 New issue，并发起一个合并请求 | 显示 2 个表单和 2 个链接，没有空白 Issue 选项；必填项为空时无法提交；合并请求描述已预填内容 | US3-AS1、AS2、AS3 |
| V4 起步清单 | 计时，按 SETUP 的 S01 ~ S09 完成。先记下社区标准页列出的全部检查项 | Community Standards 全部为绿勾；`git grep -n CHANGEME` 没有输出；首页显示你自己的 README；记录所用时间。按 F10 推断，自检页应当只列出该账号类型支持的项（内容举报只对组织账号的公共仓库出现；页面究竟是否列出这一项，由本项确认，见 SETUP 的 S02），因此列出的项都应当能完成：任何未达标项都视为门禁 4 未通过。万一自检页列出了该账号类型无法开启的项，停止并报告维护者，按宪章 Governance 处理，不得自行判定门禁通过 | 发布门禁 4；US1-AS2；SC-001（观察指标）、SC-002、SC-006 |
| V5 安全入口 | 完成 S03 后，打开 Security 页面 | 显示 **Report a vulnerability**；`SECURITY.md` 中的直达链接可以打开 | US3-AS4；FR-019 |
| V6 选型依据 | 从模板仓库首页出发，打开完整选型清单，找到任意一个模块 | 一次点击即可到达清单，能看到该模块的来源、证据、核实日期和理由 | US2；SC-004；SC-009（观察指标） |
| V7 删除模块 | 在测试仓库中删除 `.pre-commit-config.yaml`；再按 GUIDE 删除 `CHANGELOG.md` 并修改其引用方 | CI 仍然通过，不留下失效链接。全部模块的删除由 A2 的 C22 自动验证 | SC-007；FR-013 |
| V8 提交缺陷报告 | 计时，用 Bug report 表单提交一个缺陷 | 提交成功，并自动加上 `bug` 标签；记录所用时间 | SC-011（观察指标） |
| V9 发布说明 | 合并带 `enhancement` 和 `bug` 标签的合并请求，然后起草一个 Release 并点击 Generate release notes | 内容按 New Features、Bug Fixes、Other Changes 分组 | US3-AS5 |
| V10 账号级默认模板 | 如果账号下有带 Issue 模板的 `.github` 仓库，在测试仓库中点击 New issue | 显示的是测试仓库自己的表单，账号级默认模板不生效（与 GUIDE 的说明一致） | 边界情况：账号级默认 Issue 模板被覆盖 |
| V11 数据复核 | 在开发工作区运行 A3 | 数据和日期都已更新；如有 `STALE` 或 `ARCHIVED` 标志，按 MAINTAINING 重新评估 | US4 |
| V12 升级指引（可选） | 阅读 `UPGRADE-TO-TEAM.md` | 5 分钟内可以读完，每个增强项都有来源和认可度 | US5 |

验证完成后可以删除测试仓库。

## D. 创建 Release（维护者手动完成）

1. 确认 C 部分的 V1 和 V4 都已通过，也就是发布门禁 2 和 4 已满足。
2. 把 `.github/chefs-pick/CHANGELOG.md` 中的 `## [Unreleased] / 未发布` 改为 `## [1.0.0] - <日期>`，并在上方新增一个空的 `## [Unreleased] / 未发布` 节。
3. 再次运行 A4，确认 0 项失败。如果因为核实日期超过 30 天而失败，先跑 A3 刷新数据。
4. 按 B2 把改动重新发布到模板仓库，然后创建 GitHub Release `v1.0.0`，勾选 "Generate release notes"。

## 附录 A：哈希检查的测试样例

以下内容与 plan 阶段在本机实测时使用的样例相同，实施时原样写入对应文件。

`tools/tests/fixtures/pin_good.yml`（期望退出码为 0）：

```yaml
jobs:
  lint:
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: ./local-action
      - uses: docker://alpine:3
      - name: script mentioning uses
        run: |
          #   uses: actions/checkout@v4
          echo "uses: foo@v1"
  reuse:
    uses: owner/repo/.github/workflows/x.yml@0123456789abcdef0123456789abcdef01234567 # v1.2.3
```

`tools/tests/fixtures/pin_bad.yml`（期望退出码为 1，报告以下 3 行：`actions/checkout@v4`、只有哈希而没有版本注释的 `setup-node`、`other/action@main`）：

```yaml
jobs:
  lint:
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@3d3c42e5aac5ba805825da76410c181273ba90b1
      - uses: "owner/action@3d3c42e5aac5ba805825da76410c181273ba90b1" # v2.0.0
      -   uses:   other/action@main
```

测试时，把样例复制为临时目录下的 `.github/workflows/ci.yml`，再在该目录中执行脚本。`grep -Rn` 输出的每一行都以 `.github/workflows/ci.yml:` 开头，判断时按"包含"匹配，不要按"等于"匹配。
