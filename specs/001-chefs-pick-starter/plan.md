# Implementation Plan: 主厨精选开源仓库起步模板（Chef's Pick OSS Starter）

**Branch**: `001-chefs-pick-starter`（当前目录尚未初始化 Git） | **Date**: 2026-09-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-chefs-pick-starter/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

交付一个语言无关、面向个人项目的 GitHub 模板仓库。使用者一键生成新仓库后，就拥有"五脏俱全"的核心文件，每个模块都能追溯到社区公认的来源。

**模板内容的组成**：
- **放置位置**：全部放在开发工作区的 `template/` 子目录中，发布时只把这个目录的内容推送到公开模板仓库（R1）。
- **项目文件**：英文，填好即可使用；项目专属信息使用统一的 `CHANGEME_*` 占位符（R3）。每个文件首行带一行来源注释，许可证文件除外。
- **起步引导层**：包括模板首页介绍 `.github/README.md` 和目录 `.github/chefs-pick/`（起步清单、讲解、选型清单、维护说明等），全部双语。GitHub 会优先展示 `.github` 下的 README，所以首页会先显示这一层；使用者完成起步后，用一条命令即可整体移除（R2）。
- **自动化配置**：只使用官方动作，并固定到完整提交哈希，令牌只读（R12）。
- **选型依据**：已于 2026-09-18 用 GitHub API 核实，见 [research.md](./research.md)。

**维护工具**：开发工作区的 `tools/` 下提供两个 Python 脚本，都不进入模板。
- `check_template.py`：校验模板结构和发布门禁，包括清理后的状态。
- `verify_sources.py`：刷新认可度数据。

## Technical Context

**Language/Version**：
- 模板内容：Markdown、YAML，以及 GitHub Actions 工作流里的内联 Bash（运行器为 `ubuntu-latest`）。
- 维护工具：Python 3.10+（本机为 3.14.6），只依赖标准库和 PyYAML 6.x。

**Primary Dependencies**：
- GitHub 平台能力：模板仓库、社区健康文件、Issue Forms、自动生成的发布说明、Dependabot、Actions、私有漏洞报告。
- 动作：`actions/checkout` v7.0.1（`3d3c42e5aac5ba805825da76410c181273ba90b1`）。
- 上游内容（均固定到提交，见 research §4）：Contributor Covenant 2.1、`github/gitignore` Global 模板、Best-README-Template 的 BLANK_README、choosealicense 的 MIT 文本、Keep a Changelog 1.1.0、`pre-commit-hooks` v6.0.0。
- 维护数据刷新：已登录的 `gh` CLI。

**Storage**：仅文件，无数据库。

**Testing**：
- `python3 -m unittest discover -s tools/tests`（维护工具的单元测试，含正反例夹具）。分阶段验收时按测试模块名逐个运行，避免把尚未实现的检查所对应的红灯测试计入。
- `python3 tools/check_template.py`（结构校验，共 24 项）；发布前追加 `--release` 参数。模板尚未完成时，用 `--only` 排除 C01。
- 平台验证由维护者手动完成：发布内容与设置见 quickstart 的 B 部分；发布门禁 2 和 4 要在创建 Release 之前，用从模板生成的测试仓库验证，见 quickstart 的 C 部分。

**Target Platform**：
- 模板本身：github.com 上的公开模板仓库。
- 生成仓库的 CI：`ubuntu-latest`。
- 维护者环境：macOS 或 Linux，需装有 Python 3.10+ 和 `gh`。

**Project Type**：纯内容型模板仓库，外加开发工作区里的维护脚本。

**Performance Goals**：
- 生成仓库的首次 CI 在 1 分钟内完成（由 quickstart 的 V1 记录实际耗时）。
- 起步清单 15 分钟内完成（观察指标，SC-001，由 V4 记录）。
- `check_template.py` 在 5 秒内跑完（由 quickstart 的 A5 和任务 T050 计时验证）。

**Constraints**：
- 不使用生成器；只提供与语言无关的内容；不包含团队版。
- 起步引导层用中英双语；协作文件用英文。
- 所有动作固定到提交哈希，令牌只读。
- 开发文件不进入 `template/`。
- 起步引导层能用一条命令清理，且清理后不留失效引用。
- 模板仓库使用 MIT 许可证，保留上游要求的署名，不给使用者增加额外合规负担。

**Scale/Scope**：
- 16 个模块（M01–M16），24 项校验（C01–C24）。
- `template/` 下共 26 个文件：18 个项目文件（含 4 个可选文件）和 8 个起步引导层文件（含 1 个可选的团队升级指引）。
- research §1 追踪 37 个上游仓库，选型清单的认可度数据表收录其中 36 个（`spdx/license-list-data` 不列）；另有 GitHub 平台官方功能等非仓库来源。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

对照宪章 v1.0.1。"设计前"一列是进入第 0 阶段前的判断；"设计后"一列根据 research、data-model 和 contracts 复核。

| 门禁 | 依据 | 设计前 | 设计后 |
|---|---|---|---|
| G1 每个模块都有可核查的社区依据；排除的知名候选有理由 | 原则 I | 通过（规格 FR-025、FR-026、FR-030） | 通过：research §1 列出 37 个仓库的实时数据（数据表收录 36 个），R21 给出排除理由；SOURCES 的结构见 [contracts/guidance-layer.md](./contracts/guidance-layer.md) |
| G2 每个选型决定写明取舍级别和备选方案 | 原则 II | 通过（FR-029） | 通过：R4、R5、R12、R13 写明了级别；SOURCES 条目必须包含"取舍规则"字段 |
| G3 证据类型如实标注；复核周期为 6 个月且发布前必复核；触发条件按"末次提交"判断 | 原则 III | 通过（FR-026、FR-033、SC-008） | 通过：research §5 已按默认分支最近提交做过一次触发器检查；`verify_sources.py` 取默认分支提交日期而非 `pushed_at`，`check_template.py` 的 C12 校验日期新鲜度 |
| G4 一步生成；内容已填好；统一占位符；首次 CI 在空仓库上通过 | 原则 IV | 通过（FR-001、FR-007、FR-008、FR-022） | 通过：R3、R12，C05、C08 |
| G5 作者身份和模板版本历史不作为生成项目自身的信息出现；介绍、讲解、许可证声明、变更记录只在可一步移除的引导层中；开发文件不进入生成仓库 | 原则 IV（v1.0.1） | **发现冲突，已修订宪章**：v1.0.0 的措辞禁止"模板自身的介绍"进入生成仓库，与 FR-011、FR-012 以及 GitHub 复制默认分支的行为（F6）矛盾。已修订为 v1.0.1（PATCH 澄清），并在第 1 轮分析后进一步明确"生效"的含义、把模板自身的许可证声明与变更记录一并纳入引导层；规格 FR-010 ~ FR-012 同步调整 | 通过：R1、R2、R16；C02、C10、C13 |
| G6 核心要素齐全；不用生成器或重型模板；只做语言无关内容；附加内容可选、无副作用、可单独删除 | 原则 V | 通过（FR-003、FR-005、FR-006、FR-013、FR-014） | 通过：R12 否决 super-linter；`CODEOWNERS` 与 `FUNDING.yml` 默认不生效（C10），`.pre-commit-config.yaml` 不安装 pre-commit 就没有效果，`.editorconfig` 只影响本地编辑器，按 FR-014 的定义不算可见副作用（R15）；逐模块删除由 C22 验证，删除说明由 C17 验证 |
| G7 只面向 GitHub | 附加约束 | 通过 | 通过 |
| G8 起步引导层双语，协作文件英文 | 附加约束 | 通过（FR-037） | 通过：R18；C11 用启发式方法检查 |
| G9 模板使用 MIT；声明生成项目无需保留模板署名；保留上游署名 | 附加约束 | 通过（FR-031、FR-036） | 通过：R4 选用 CC BY 4.0 的 2.1、避开 CC BY-SA 的 3.0；R16 |
| G10 动作固定到完整提交哈希并注明版本；令牌默认只读 | 附加约束 | 通过（FR-039、SC-012） | 通过：R12、R13；C05，CI 自带哈希检查 |
| G11 选型变更须同步更新清单和模板变更记录 | 开发流程 | 通过（FR-034） | 通过：MAINTAINING 的结构见 [contracts/guidance-layer.md](./contracts/guidance-layer.md) |
| G12 模板仓库自身遵守规范，包括社区标准全部达标、KaC + SemVer | 开发流程 | 通过（FR-035） | 通过：模板自身的变更记录采用 KaC 1.1.0，版本标题按 guidance-layer §0 的例外处理；模板仓库的社区标准在 quickstart B4 确认，生成仓库的在 V4 确认 |
| G13 5 项发布门禁，且全部在创建 Release 之前完成 | 开发流程 | 通过 | 通过：`check_template.py --release` 覆盖门禁 1、3、5 和门禁 2 的静态部分；门禁 2 的"首次 CI 通过"与门禁 4 由 quickstart 的 C 部分在创建 Release 前用测试仓库验证（V1、V4） |
| G14 体验指标不作为发布门槛 | 开发流程 | 通过（SC-001、SC-009、SC-011） | 通过 |

**结论**：G5 经宪章 v1.0.1 澄清后，全部门禁通过，Complexity Tracking 无需填写。v1.0.1 是 PATCH 级措辞澄清，按宪章 Governance 仍需项目维护者确认。

## Project Structure

### Documentation (this feature)

```text
specs/001-chefs-pick-starter/
├── spec.md              # 功能规格（/speckit-specify、/speckit-clarify）
├── input.md             # 原始输入：交接文档与两份调研报告
├── plan.md              # 本文件（/speckit-plan）
├── research.md          # 第 0 阶段：已核实数据与决策
├── data-model.md        # 第 1 阶段：实体与校验规则
├── quickstart.md        # 第 1 阶段：本地验证、发布、发布前验证的步骤
├── contracts/           # 第 1 阶段：文件级契约
│   ├── template-layout.md
│   ├── markers.md
│   ├── project-files.md
│   ├── guidance-layer.md
│   └── tooling.md
├── checklists/
│   └── requirements.md
└── tasks.md             # 第 2 阶段（/speckit-tasks 生成，本命令不创建）
```

### Source Code (repository root)

```text
./                                   # 开发工作区（不作为模板发布）
├── .claude/  .specify/  specs/      # Spec Kit 与 AI 助手配置（不进入模板）
├── .gitignore                       # 开发工作区自用：__pycache__/、*.pyc、.DS_Store
├── tools/                           # 维护工具（不进入模板）
│   ├── check_template.py
│   ├── verify_sources.py
│   └── tests/
│       ├── helpers.py
│       ├── test_checks_layout.py        # C01–C03、C21
│       ├── test_checks_automation.py    # C05、C06
│       ├── test_checks_markers.py       # C08、C09
│       ├── test_checks_identity.py      # C10、C11
│       ├── test_checks_links.py         # C13–C15、C17、C22
│       ├── test_checks_selection.py     # C12
│       ├── test_checks_contributor.py   # C04、C07、C16、C20
│       ├── test_checks_maintaining.py   # C18
│       ├── test_checks_upgrade.py       # C19
│       ├── test_ci_pin_check.py
│       ├── test_verify_sources.py
│       ├── test_real_template.py
│       └── fixtures/
└── template/                        # = 公开模板仓库默认分支的全部内容
    ├── .editorconfig                # M13 可选
    ├── .gitignore                   # M03 必需
    ├── .pre-commit-config.yaml      # M14 可选
    ├── CHANGELOG.md                 # M09 推荐（项目骨架，只有 Unreleased）
    ├── CODE_OF_CONDUCT.md           # M04 推荐
    ├── CONTRIBUTING.md              # M05 推荐
    ├── LICENSE                      # M02 必需（MIT，版权人为占位符）
    ├── README.md                    # M01 必需（项目骨架）
    ├── SECURITY.md                  # M06 推荐
    └── .github/
        ├── CODEOWNERS               # M15 可选（全部注释）
        ├── FUNDING.yml              # M16 可选（值为空）
        ├── ISSUE_TEMPLATE/
        │   ├── bug_report.yml       # M07 推荐
        │   ├── config.yml           # M07 推荐
        │   └── feature_request.yml  # M07 推荐
        ├── PULL_REQUEST_TEMPLATE.md # M08 推荐
        ├── dependabot.yml           # M12 推荐
        ├── release.yml              # M09 推荐
        ├── workflows/
        │   └── ci.yml               # M11 推荐
        ├── README.md                # 起步引导层：模板首页（双语）
        └── chefs-pick/              # 起步引导层（双语）
            ├── SETUP.md             # 起步清单与占位符登记表
            ├── GUIDE.md             # 各模块讲解、定制方法、删除方法
            ├── SOURCES.md           # 选型清单（完整数据）
            ├── MAINTAINING.md       # 模板维护说明
            ├── UPGRADE-TO-TEAM.md   # 可选（P4）：团队升级指引
            ├── CHANGELOG.md         # 模板自身的变更记录
            └── LICENSE              # 模板自身的许可证（MIT）
```

**Structure Decision**：采用"开发工作区 + `template/` 子目录"的结构（R1）。M10（变更日志自动化）没有对应文件，只在 SOURCES 和 GUIDE 中推荐。每个文件的内容契约见 [contracts/](./contracts/)，实体定义见 [data-model.md](./data-model.md)。

## Implementation Notes（供 /speckit-tasks 使用）

- **前置条件**：宪章 v1.0.1 是 PATCH 级措辞澄清，按 Governance 需项目维护者确认后才生效。确认之前不要开始 T001。
- **执行方式**：任务由 Sonnet 级子代理执行，Opus 级主代理负责协调。每个任务都必须能独立完成，并写明以下内容：
  - 目标文件的完整路径。
  - 需要读取的契约章节。
  - 需要用到的固定数据：提交哈希、Star 数、链接等，统一取自 research.md。
  - 验收命令，通常是 `python3 tools/check_template.py --only <检查编号>` 或 `unittest`。
- **任务不得要求子代理自行做选型判断**：所有选型已在 research.md 中确定。如果上游内容与契约不符，子代理应停下来报告，不得自行替换来源。
- **网络访问**：只允许用 `gh api` 按固定提交哈希获取上游文件（research §4 给出了命令模板）。刷新认可度数据时只运行 `tools/verify_sources.py`。
- **禁止的操作**：初始化 Git、提交、推送、创建远程仓库、修改 GitHub 设置。这些属于发布步骤，由维护者按 quickstart 手动完成。
- **测试先行**：先实现 `check_template.py` 的检查项和单元测试，再编写模板文件。每写完一个模板文件，就跑它对应的检查项。

## Complexity Tracking

无。宪章检查中唯一的冲突（G5）已通过宪章 v1.0.1 的措辞澄清解决，不属于需要特殊说明的违规。
