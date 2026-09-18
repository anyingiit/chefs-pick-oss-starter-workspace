# Implementation Plan: 工作区自身遵守模板定下的规矩

**Branch**: `claude/trusting-babbage-xq8avi` | **Date**: 2026-09-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-workspace-self-compliance/spec.md`

## Summary

工作区不检查自己，于是两处同时腐化：发布流程写错到会损坏模板仓库的 `v1.0.0` 发布，首页还留着 002 已从模板清除的中英并排写法，外加 2 处事实与仓库现状不符。

做法是把 002 已经建成的那套机制**扩展作用域**，而不是新建一套：首页转为英文规范版 + 独立中文译本，沿用同样的语言入口、章节锚点与内容摘要；新增三项检查（C25 ~ C27），从仓库根解析路径、复用现有算法函数，把语言、章节、新鲜度、事实四类判定纳入日常校验；发布流程按今天实测的结论重写，区分首次与后续两种情形并显式禁止强推。

## Technical Context

**Language/Version**: Python 3.11（校验工具）；Markdown（文档）

**Primary Dependencies**: 仅标准库；`hashlib`、`re`、`pathlib` 均已在用

**Storage**: 无。判定对象是仓库中的文件本身

**Testing**: `unittest`，现有 239 个用例，位于 `tools/tests/`

**Target Platform**: 本地开发工作区；无 CI

**Project Type**: 文档 + 单文件校验脚本

**Performance Goals**: 不适用。整套校验当前 0.2 秒内完成，新增三项不改变量级

**Constraints**:
- `template/` 下任何文件逐字节不变（FR-017、SC-010）
- C01 ~ C24 对 `template/` 的判定逐项不变（FR-016、SC-011）
- 不新增命令；三项新检查并入既有的日常校验与发布门禁（FR-015）

**Scale/Scope**: 2 份文档（1 改 1 建）、1 份快速开始指南补充、1 个脚本增 3 项检查、若干测试用例

## Constitution Check

*GATE: 通过后方可进入 Phase 0。Phase 1 设计完成后复查。*

| 条款 | 判定 | 依据 |
|---|---|---|
| 原则 I 社区依据优先 | 不适用 | 本功能不新增或替换任何模块 |
| 原则 II 认可度优先 | 不适用 | 同上 |
| 原则 III 来源与认可度透明 | 不适用 | 不改动选型数据 |
| 原则 IV 开箱即用 | **通过** | 不改 `template/`，一步清理与生成仓库的行为完全不变（FR-017） |
| 原则 V 轻量而完整 | **通过** | 只加 3 项检查与 1 份译本；不引入依赖、不新增命令 |
| 附加约束 · 平台 | 不适用 | 不涉及平台能力 |
| 附加约束 · 文档语言 | **通过（见下）** | 条款点名的适用对象是 `template/` 下的六份使用者文档，豁免对象是规格、规划、宪章等开发过程文件；工作区首页两者皆非，宪章对它**沉默**。本功能把同一做法扩展到首页，不与条款中任何一句相抵触。维护者已于 2026-09-18 裁定无需先行修订宪章（spec.md Dependencies） |
| 附加约束 · 许可证与署名 | 不适用 | 不改许可证 |
| 附加约束 · 自动化安全基线 | 不适用 | 不改工作流 |
| 质量门禁 · 规格驱动 | **通过** | 本功能正按 specify → plan → tasks 推进 |
| 质量门禁 · 选型变更 | 不适用 | 无选型变更 |
| 质量门禁 · **自用一致性** | **通过，且本功能正是为它服务** | 条款要求「模板仓库自身必须遵循它交付给使用者的规范」。002 把这条落实到了 `template/`，本功能把同一精神落实到承载工作区门面的那份文档 |
| 质量门禁 · 发布门禁 | **通过** | 新增的 C25、C26 并入日常校验并在 `--release` 下同样生效；C27 沿用 002 既定的 WARN／FAIL 分野。门禁**条目数不变**，仍为 6 项——新增判定并入既有的自动化部分，不新增人工步骤 |

**结论**：无违反，无需填写 Complexity Tracking。

### Phase 1 设计后复查

设计完成后逐条复看，判定不变。三点值得记下：

1. C25 ~ C27 全部从仓库根解析路径并忽略 `--template-dir`，沿用 C23 已有的写法，没有为此改动任何既有检查的代码路径——原则 IV 与 FR-016 因此在实现层面而非口头上成立。
2. 语言判定复用 `strip_for_purity`、`cjk_count`、`longest_english_run`，新鲜度复用 `DIGEST_RE` 与同一段 `update_digests` 替换实现，FR-014「与模板译本同一套判定」是字面成立的，不是近似。
3. 发布门禁条目数仍为 6。002 的 SC-010 曾规定「门禁项数增加不超过 1 项」且已用掉那 1 项；本功能不再新增门禁条目，只扩大既有自动化门禁的覆盖面。

## Project Structure

### Documentation (this feature)

```text
specs/003-workspace-self-compliance/
├── plan.md                              # 本文件
├── spec.md                              # 规格
├── research.md                          # Phase 0：R1 ~ R10
├── data-model.md                        # Phase 1：四类校验对象
├── quickstart.md                        # Phase 1：A/B/C/D 四部分验收
├── contracts/
│   ├── workspace-structure.md           # 逐字契约：首页的语言与事实结构
│   └── tooling-delta-003.md             # 逐字契约：tools/ 相对 002 的增量
├── checklists/requirements.md           # 规格质量检查表
└── tasks.md                             # /speckit-tasks 产出，本命令不创建
```

### Source Code (repository root)

```text
README.md                    # 改：转为英文规范版，补锚点与语言入口，重写发布一节，订正 3 项事实
README.zh-CN.md              # 新建：中文译本

specs/001-chefs-pick-starter/
└── quickstart.md            # 改：§B 补后续发布的步骤

tools/
├── check_template.py        # 改：新增 C25 ~ C27；update_digests 覆盖工作区译本
└── tests/
    ├── test_workspace_language.py   # 新建：C25
    ├── test_workspace_facts.py      # 新建：C26
    └── test_checks_translation.py   # 改：补 C27 与 update_digests 的工作区分支

template/                    # 不动一个字节
```

**Structure Decision**：沿用工作区既有布局，不引入新目录。三项新检查写在 `check_template.py` 内而非拆出新模块，理由是 FR-015 要求它们并入同一条命令，且现有 24 项检查也都在这一个文件里——为 3 项检查拆模块会让文件组织与检查编号的对应关系断裂。

## Phase 0：调研

见 [research.md](./research.md)。十个问题全部有结论，无遗留 NEEDS CLARIFICATION。最关键的一条是 R1：`git subtree split` 与模板仓库现有历史没有共同祖先（实测 `git merge-base --is-ancestor` 返回否），因此按 README 字面执行只能强推，而强推会让 `v1.0.0` 标签指向的 `99cba97` 从任何分支都不可达。

## Phase 1：设计与契约

见 [data-model.md](./data-model.md)、[contracts/](./contracts/)、[quickstart.md](./quickstart.md)。

契约把实现所需的每一处逐字内容都固定下来：语言入口两行、锚点序列 5 项、规范性声明一句、来源标记格式、三项事实的承载句式、后续发布的命令块与三句警告。任务阶段只需照抄，不需要再做设计判断。

## 实施顺序

1. 基线：记录改造前的测试数、检查数、`template/` 文件数与首页中文字符数。
2. 工具先行：C25 ~ C27 与 `update_digests` 的工作区分支。此时检查会失败，因为文档还没改——这是预期的，先让判据存在。
3. 文档：重写 `README.md`，新建 `README.zh-CN.md`，刷新摘要。
4. 补 `specs/001-chefs-pick-starter/quickstart.md` §B。
5. 测试与回归：新增用例，确认既有 24 项判定与 `template/` 内容均未改变。

第 2 步先于第 3 步，是为了让文档改造有可执行的判据可依；但这会使中间状态的整套校验短暂失败，任务描述中必须写明，以免执行者误以为出错而回退。
