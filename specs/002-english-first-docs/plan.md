# Implementation Plan: 英文为主、中文另起一份的文档语言结构

**Branch**: `claude/trusting-babbage-xq8avi`（规格目录 `002-english-first-docs`） | **Date**: 2026-09-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-english-first-docs/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

把起步引导层从"同文档内逐段中英并排"改成"英文规范版本 + 独立中文译本 + 语言入口"。

- **英文侧**：8 个引导层文件全部改为纯英文，删去中文段落、把双语标题与表头改成英文。英文内容基本已存在（92 个小节里只有 1 个需要补写，见 research R9），主体工作是删除与改标签，不是重写。
- **中文侧**：新增两份纯中文译本——`.github/README.zh-CN.md` 与 `.github/chefs-pick/SETUP.zh-CN.md`。其余四份文档只保留英文，不带语言入口。
- **可校验性**：两个语言版本的每个标题前加一个渲染后不可见的锚点，章节集合按锚点有序序列比对；每份译本记录英文原文的内容摘要作为来源标记，日常提示、发布门禁硬卡。
- **顺带堵一个旧洞**：逐字契约与 `template/` 之间既有的 12 处 Star 数漂移一并消除，并加校验阻断增量。

`template/` 文件数 26 → 28；`check_template.py` 校验项 22 → 24，并新增 `WARN` 状态与 `--update-digests` 维护开关。

## Technical Context

**Language/Version**：
- 模板内容：Markdown（引导层）与既有的 YAML、内联 Bash（本功能不动）。
- 维护工具：Python 3.10+（本机 3.14.6），只依赖标准库与 PyYAML 6.x；新增的摘要计算用标准库 `hashlib`。

**Primary Dependencies**：不引入任何新依赖。语言入口用纯文本链接而非徽章图片，正是为了不引入外部图片依赖（research R4）。

**Storage**：仅文件，无数据库。

**Testing**：
- `python3 -m unittest discover -s tools/tests`（现有 199 个用例，本功能新增用例后必须全绿）。
- `python3 tools/check_template.py`（22 → 24 项）；发布前追加 `--release`。
- 分阶段验收用 `--only C11`、`--only C23` 等单项运行。

**Target Platform**：github.com 上的公开模板仓库；维护者环境为装有 Python 3.10+ 的 macOS 或 Linux。

**Project Type**：纯内容型模板仓库，外加开发工作区里的维护脚本。本功能只触及引导层文档与维护脚本，不触及交付给使用者的项目文件。

**Performance Goals**：`check_template.py` 仍须在 5 秒内跑完；新增的 C23、C24 都是纯文本比对与一次 sha256，量级可忽略。

**Constraints**：
- 英文版散文中不得出现中文；中文版散文中不得出现连续 6 个及以上英文词（research R6）。
- 同一文档内禁止并排两种语言，标题、表头、列表项、单元格同样适用。
- 起步引导层仍须一条命令清理干净，且清理后无失效引用。
- 机器可刷新的数据（16 行摘要表、占位符登记表、认可度数据表）全模板各只有一份，位于英文原文中。
- 不改动生成仓库中交付给使用者的任何文件。

**Scale/Scope**：
- 8 个引导层文件改为纯英文（约 120 KB，其中 12,634 个中文字符要移除）。
- 2 个新译本文件。
- 4 个文件加章节锚点（约 40 处）。
- `check_template.py`：2 项重写（C11、C12）、6 项微调（C08、C13、C14、C17、C18、C19、C22）、2 项新增（C23、C24）。
- `verify_sources.py`：写入目标增加逐字契约。
- 逐字契约 `guidance-layer.md`：§0 与 §1 ~ §7 全部重写，§4.4 修正 12 个数字。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

对照宪章 **v2.1.0**。"设计前"是进入第 0 阶段前的判断，"设计后"依据 research、data-model 与 contracts 复核。

| 门禁 | 依据 | 设计前 | 设计后 |
|---|---|---|---|
| G1 每个决定都有可核查的社区依据；作者偏好不得作为首要依据 | 原则 I | 通过：规格「背景与取证结论」给出 25 个仓库的一手抽样，逐段并排出现 0 次 | 通过：research R2、R3、R4 的选型都写明了依据与被否决的备选；R4 明确"不用徽章"是依据零依赖取向而非偏好 |
| G2 选型按三级规则取舍并写明级别与备选方案 | 原则 II | 通过 | 通过：research 每条决策都带"备选方案"与否决理由；R1（同目录 vs 子目录）、R2（锚点 vs 半译 vs 顺序比对）、R3（摘要 vs 提交哈希 vs 版本号）均为第 1 级 |
| G3 认可度证据如实标注、按期复核 | 原则 III | 通过：本功能不改动任何认可度数字的**取值** | 通过：R7 以 `template/` 为准修正契约，`template/` 的值来自 `verify_sources.py` 的 API 实时抓取，不是人工编造；C23 保证两处此后一致 |
| G4 一步生成；内容已填好；占位符统一；首次 CI 在空仓库通过 | 原则 IV | 通过：本功能不触及生成仓库的文件 | 通过：FR-009 明确不向生成仓库新增任何中文文件；占位符登记表仍是唯一一份（R10） |
| G5 引导层可一步移除，且移除后无失效引用 | 原则 IV | **需要设计确认**：新增的 `README.zh-CN.md` 在 `chefs-pick/` 之外 | 通过：R1 把它显式列入清理命令，命令仍是**一条**；C13、C22 按新命令与新文件集合改造 |
| G6 轻量而完整；附加内容可选、无可见副作用 | 原则 V | 通过 | 通过：锚点与来源标记都是 HTML 注释，渲染后可见字符数为 0（SC-013）；译本覆盖面收到 2 份，正是为了不让门禁 6 变成不可承受的负担 |
| G7 只面向 GitHub | 附加约束 | 通过 | 通过：R2 因 GitHub 不支持 `{#id}` 标题属性而选用 HTML 注释 |
| G8 **英文为规范版本；中文以独立译本提供；禁止同文档并排；语言入口统一且一步互达；译本与原文同处引导层；机器可读数据只一份** | 附加约束（v2.0.0 改写） | 通过：这正是本功能的目的 | 通过：R1 ~ R6 逐项落地；R10 保证登记表与摘要表各只一份 |
| G9 模板使用 MIT；声明生成项目无需保留模板署名 | 附加约束 | 通过 | 通过：R1b 只删 `chefs-pick/LICENSE` 末尾的中文段落，MIT 正文一字不动；中文读者所需信息在 `README.zh-CN.md` 保留 |
| G10 动作固定到提交哈希；令牌只读 | 附加约束 | 通过：本功能不触及工作流 | 通过 |
| G11 选型变更须同步更新清单与模板变更记录 | 开发流程 | 不适用：本功能不新增、替换或移除任何模块 | 不适用。但 `chefs-pick/CHANGELOG.md` 仍需记一笔文档语言结构的变更 |
| G12 自用一致性：模板仓库自身遵守它交付的规范 | 开发流程 | 通过 | 通过：改造后模板仓库自身就是"英文规范版本 + 中文译本 + 语言入口"的示范，与 FR-016 教给使用者的做法一致 |
| G13 **6 项**发布门禁，全部在创建 Release 之前完成 | 开发流程（v2.1.0 新增第 6 项） | **需要设计确认**：门禁 6 尚无自动化落点 | 通过：C24 在 `--release` 下按 FAIL 计，覆盖门禁 6 的全部可自动化部分；R9 要求 `MAINTAINING.md` 把 6 条门禁完整写成英文 |
| G14 体验指标不作为发布门槛 | 开发流程 | 通过 | 通过：规格已撤销唯一一条会误判的篇幅标准（SC-009） |

**结论**：全部门禁通过。G5 与 G13 在设计阶段得到落实（R1 的清理命令、C24 的发布口径），不构成违规，**Complexity Tracking 无需填写**。

## Project Structure

### Documentation (this feature)

```text
specs/002-english-first-docs/
├── spec.md                        # 功能规格（/speckit-specify、/speckit-clarify）
├── plan.md                        # 本文件（/speckit-plan）
├── research.md                    # 第 0 阶段：实现形态决策 R1 ~ R12
├── data-model.md                  # 第 1 阶段：实体与校验规则
├── quickstart.md                  # 第 1 阶段：验证步骤
├── contracts/                     # 第 1 阶段：逐字契约
│   ├── language-structure.md      # 语言入口、规范性声明、锚点、来源标记的逐字写法
│   ├── guidance-layer-en.md       # 8 份英文文档改造后的逐字结构
│   └── tooling-delta.md           # check_template.py 与 verify_sources.py 的改动
├── checklists/
│   └── requirements.md
└── tasks.md                       # 第 2 阶段（/speckit-tasks 生成，本命令不创建）
```

### Source Code (repository root)

```text
./                                          # 开发工作区
├── .specify/memory/constitution.md          # v2.1.0（已修订，本功能不再改动）
├── specs/001-chefs-pick-starter/
│   └── contracts/guidance-layer.md          # 【改】§0 双语规则重写；§1~§7 改为英文结构；§4.4 修正 12 个数字
├── tools/
│   ├── check_template.py                    # 【改】C08、C11~C14、C17~C19、C22；新增 C23、C24、WARN、--update-digests
│   ├── verify_sources.py                    # 【改】写入目标增加逐字契约
│   └── tests/
│       ├── test_checks_identity.py          # 【改】C11 用例整体重写
│       ├── test_checks_selection.py         # 【改】C12 英文字面量
│       ├── test_checks_links.py             # 【改】C13、C14、C17、C22
│       ├── test_checks_markers.py           # 【改】C08 表头
│       ├── test_checks_maintaining.py       # 【改】C18 六条门禁
│       ├── test_checks_upgrade.py           # 【改】C19 英文
│       ├── test_checks_contract_parity.py   # 【新】C23
│       ├── test_checks_translation.py       # 【新】C24 与 --update-digests
│       ├── test_verify_sources.py           # 【改】契约写入
│       └── test_real_template.py            # 【改】真实模板的语言结构断言
└── template/.github/
    ├── README.md                            # 【改】纯英文 + 语言入口 + 锚点
    ├── README.zh-CN.md                      # 【新】纯中文译本
    └── chefs-pick/
        ├── SETUP.md                         # 【改】纯英文 + 语言入口 + 锚点
        ├── SETUP.zh-CN.md                   # 【新】纯中文译本
        ├── GUIDE.md                         # 【改】纯英文（含 FR-016 的新小节）
        ├── SOURCES.md                       # 【改】纯英文
        ├── MAINTAINING.md                   # 【改】纯英文 + 6 条门禁 + --update-digests
        ├── UPGRADE-TO-TEAM.md               # 【改】纯英文
        ├── CHANGELOG.md                     # 【改】纯英文 + 记一笔本次变更
        └── LICENSE                          # 【改】删末尾中文段落
```

**Structure Decision**：沿用 001 的"开发工作区 + `template/` 子目录"结构，不新增目录层级。译本与其英文原文同目录（research R1），使两者到任何目标的相对路径深度一致。

## Implementation Notes（供 /speckit-tasks 使用）

**执行模型**：协调由强模型负责，每个任务由 Sonnet 级子代理独立执行。因此任务必须满足：

1. **只做一件事**，且目标文件路径写全。跨 8 个文件的"批量改英文"必须拆成 8 个任务。
2. **不含任何判断题**。所有形态决策已在 [research.md](./research.md) 定死，所有逐字内容已在 [contracts/](./contracts/) 写明。任务只需引用契约的章节号。
3. **自带验收命令**，通常是 `python3 tools/check_template.py --only C11 --files <路径>` 或 `python3 -m unittest tools.tests.test_checks_identity`。
4. **需要的固定数据就地给出**：锚点 id 列表、语言入口逐字串、要修正的 12 个 Star 数，都写进任务描述，不让子代理去别处找。
5. **子代理遇到契约与现状不符时必须停下来报告**，不得自行发挥。尤其是：MIT 正文不得改动；认可度数字不得凭记忆填写；英文段落不得"顺手润色"。

**依赖顺序**：
- 先改 `check_template.py` 的检查项与单元测试（红灯），再改模板文件（转绿）。这样每个文档任务都有明确的验收信号。
- C23 与契约数字修正可以与文档改造并行，二者不相交。
- 两份译本必须在其英文原文定稿之后再写，否则来源标记一写就过期。
- `--update-digests` 在全部文档任务完成后统一运行一次。

**禁止的操作**：初始化 Git 远程、创建 Release、修改 GitHub 仓库设置、刷新认可度数据（`verify_sources.py --write` 属于维护动作，不在本功能范围内）。

## Complexity Tracking

无。宪章 v2.1.0 的 14 项门禁全部通过，G5 与 G13 由设计决策（research R1、R3）落实，不属于需要说明的违规。
