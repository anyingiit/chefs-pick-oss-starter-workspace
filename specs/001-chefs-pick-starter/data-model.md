# 数据模型：主厨精选开源仓库起步模板

本项目没有数据库。"数据"指起步引导层文档中的结构化内容：选型清单 `SOURCES.md` 和起步清单 `SETUP.md`。维护工具会读取并校验这些内容，所以格式必须严格遵守本文件和 [contracts/guidance-layer.md](./contracts/guidance-layer.md)。

## 实体

### Module（模块）

仓库的一个核心要素。

| 字段 | 类型 | 规则 |
|---|---|---|
| id | `M01`–`M16` | 固定编号，唯一，含义见下方模块目录 |
| name | 中文名 / English name | 双语，例如"行为准则 / Code of Conduct" |
| level | 必需 / 推荐 / 可选 | 必须与 FR-003 一致 |
| files | `template/` 下的相对路径列表 | M10 没有文件，写作"—" |
| chosen_source | → Source | 每个模块有且只有一个选定来源；M10 例外，是按项目类型推荐的三个工具 |
| removal | 删除方法与影响（双语） | 必需模块写"不建议删除"；其余模块必须写明删除后的影响（FR-013） |

### Source（来源）

模块内容或所遵循规范的上游出处。

| 字段 | 类型 | 规则 |
|---|---|---|
| id | `owner/repo`，或 `platform:<feature>` | 唯一 |
| name | 文本 | — |
| url | https 链接 | 必须能访问 |
| type | repository / platform-feature / specification | — |
| license | 三种取值之一 | SPDX 标识（如 `MIT`）；平台官方功能写"官方文档 / Official docs"；确实取不到时写"未识别 / Unknown"（FR-031） |
| pinned_ref | 40 位提交哈希（可选） | 模板直接收录或改写上游文件时必填（见 research §4） |
| last_commit | `YYYY-MM-DD` | 默认分支最近一次提交的日期。不要用 `pushed_at`，它会因任何分支的推送而更新 |
| status | active / stale / archived | `last_commit` 距今超过 365 天为 stale；仓库已归档为 archived |

### AdoptionEvidence（认可度证据）

| 字段 | 类型 | 规则 |
|---|---|---|
| source | → Source | 每个 Source 至少一条 |
| type | 枚举（见下） | 必须如实标注（FR-026） |
| value | 整数或文本 | Star 数写精确整数，用千分位逗号；文本证据必须写明具体采用者或出处 |
| origin | 链接或 API | 例如 `gh api repos/<owner>/<repo>` |
| verified | `YYYY-MM-DD` | 任何时候距当天都不超过 183 天；发布时距发布日不超过 30 天（SC-008）。受此约束的日期字段清单见 [contracts/tooling.md](./contracts/tooling.md) 的 C12；`last_commit` 不在其中 |

证据类型（写法固定，双语）：

- `精确 Star 数 / Exact stars`
- `四舍五入 Star 数 / Rounded stars`
- `估算使用人数 / Estimated users`：必须附估算依据
- `平台官方功能 / Official platform feature`
- `事实标准 / De facto standard`：必须附具体采用者
- `未取得 / Not available`：必须附替代证据

### SelectionDecision（选型决定）

| 字段 | 类型 | 规则 |
|---|---|---|
| module | → Module | 一对一 |
| rule | `1`、`2`、`3`，或组合写法 `1 + 2` | 含义见下方"取舍规则的写法" |
| rationale | 中文段落 + 英文段落 | 必填 |
| alternatives | 列表：来源名称、证据、未选原因（双语） | 至少一项；确实没有候选时写"无同类候选 / No comparable alternative"并说明原因 |
| review_status | 有效 / 需重新评估 | 见状态流转 |

**取舍规则的写法**：

- `1`：仅凭社区认可度即可决定，其他候选的认可度明显更低。
- `2`：候选之间认可度相当，靠"对仓库持有者更容易起步"决定。使用这一写法时，入选理由必须写明判定"认可度相当"的依据（宪章原则 II）。
- `3`：候选同样合格，按作者个人偏好决定。理由中必须写明"作者偏好 / author's preference"。
- `1 + 2`：第 1 级已能决定，第 2 级也指向同一选择。理由中要分别说明这两点。因为没有主张"认可度相当"，所以不需要额外写判定依据。

### ExcludedCandidate（排除的候选）

| 字段 | 类型 | 规则 |
|---|---|---|
| source | → Source | — |
| evidence | 同 AdoptionEvidence | — |
| reason | 中文 + 英文 | 必填（宪章原则 I） |

### Placeholder（占位符）

| 字段 | 类型 | 规则 |
|---|---|---|
| token | 满足 `^CHANGEME_[A-Z0-9_]+$` 的字符串 | 唯一 |
| meaning | 中文 + 英文 | — |
| files | `template/` 下的相对路径列表 | 至少一个；只能出现在项目文件中，不能出现在起步引导层之外的其他位置 |
| example | 文本 | 替换示例 |

完整登记表见 [contracts/markers.md](./contracts/markers.md)，并须按 [contracts/guidance-layer.md](./contracts/guidance-layer.md) §2 规定的表头写进 `SETUP.md`。

### SetupStep（起步步骤）

| 字段 | 类型 | 规则 |
|---|---|---|
| id | `S01`… | 编号连续 |
| text | 中文 + 英文 | — |
| kind | 必做 / 选做 | — |
| verification | 文本 | 说明怎样确认这一步已完成 |

完整步骤表见 [contracts/guidance-layer.md](./contracts/guidance-layer.md)。最后两步固定为"清理起步引导层"和"最终验收"。

## 关系

```text
Module 1 ── 1 SelectionDecision ──> Source（选定来源）
                     └──> Source*（备选方案，附未选原因）
Source 1 ── * AdoptionEvidence
ExcludedCandidate ──> Source
Placeholder * ── * 模板项目文件
SetupStep ──> Placeholder（S01 替换全部占位符）
```

## 状态流转：SelectionDecision.review_status

```text
有效 ──(触发条件)──> 需重新评估 ──(按宪章原则 II 重新取舍)──> 有效（保留，附复核说明）
                                                    └──> 有效（换成新来源；模板变更记录写 Changed 或 Removed，并附原因）
```

触发条件（宪章原则 III 的 3 条）：
1. 上游末次提交距今超过 12 个月。以默认分支最近一次提交（`last_commit`）为准；仓库已归档视同满足本条件。
2. 上游依赖了已被广泛弃用的工具。
3. 出现认可度明显更高的候选。

## 模块目录（M01–M16）

此表是 `SOURCES.md` 和 `.github/README.md` 摘要表的权威来源。数字取自 [research.md](./research.md)，写入模板前须重新核实。

| id | 模块 / Module | 级别 | 文件（`template/` 下） | 选定来源 | 取舍规则 |
|---|---|---|---|---|---|
| M01 | 项目说明 / README | 必需 | `README.md` | othneildrew/Best-README-Template（BLANK_README，★16,360） | 1 |
| M02 | 许可证 / License | 必需 | `LICENSE` | choosealicense.com 的 MIT 文本 + SPDX 标识 `MIT`（GitHub 官方；★4,201） | 1 |
| M03 | 忽略规则 / Ignore rules | 必需 | `.gitignore` | github/gitignore 的 Global 模板（★175,810） | 1 |
| M04 | 行为准则 / Code of Conduct | 推荐 | `CODE_OF_CONDUCT.md` | Contributor Covenant 2.1（事实标准；官方采用者名单 454 个项目） | 1 + 2 |
| M05 | 贡献指南 / Contributing guide | 推荐 | `CONTRIBUTING.md` | GitHub Open Source Guides（★15,684）+ GitHub Docs | 1 |
| M06 | 安全策略 / Security policy | 推荐 | `SECURITY.md` | GitHub 安全策略 + 私有漏洞报告（平台官方功能） | 1 + 2 |
| M07 | Issue 表单 / Issue forms | 推荐 | `.github/ISSUE_TEMPLATE/bug_report.yml`、`feature_request.yml`、`config.yml` | GitHub Issue Forms（平台官方功能） | 1 + 2 |
| M08 | 合并请求模板 / Pull request template | 推荐 | `.github/PULL_REQUEST_TEMPLATE.md` | GitHub 合并请求模板（平台官方功能） | 1 + 2 |
| M09 | 变更日志与发布说明 / Changelog & release notes（合并了 FR-003 中的"变更日志"和"发布说明分类配置"两项） | 推荐 | `CHANGELOG.md`、`.github/release.yml` | Keep a Changelog 1.1.0（★6,702）+ SemVer 2.0.0（★7,852）+ GitHub 自动生成的发布说明 | 1 |
| M10 | 变更日志自动化 / Changelog automation | 可选（只推荐） | — | 按项目类型：changesets（★12,405）、git-cliff（★12,245）、release-please（★7,505） | 1 + 2 |
| M11 | 自动检查 / Continuous integration | 推荐 | `.github/workflows/ci.yml` | actions/starter-workflows 的 Simple workflow（★12,080）+ actions/checkout v7.0.1（★8,882）；按哈希固定的依据是 GitHub Docs 与 OpenSSF Scorecard（★5,694） | 1 + 2 |
| M12 | 依赖自动更新 / Dependency updates | 推荐 | `.github/dependabot.yml` | GitHub Dependabot（平台官方功能；dependabot-core ★5,772） | 2 |
| M13 | 编辑器格式配置 / EditorConfig | 可选 | `.editorconfig` | EditorConfig（★3,450；已重新评估，保留） | 1 |
| M14 | 提交前检查 / Pre-commit hooks | 可选 | `.pre-commit-config.yaml` | pre-commit（★15,581）+ pre-commit-hooks v6.0.0（★6,681） | 1 |
| M15 | 代码负责人 / Code owners | 可选 | `.github/CODEOWNERS` | GitHub CODEOWNERS（平台官方功能） | 1 |
| M16 | 赞助入口 / Funding | 可选 | `.github/FUNDING.yml` | GitHub 赞助按钮（平台官方功能） | 1 |

排除的候选见 [research.md](./research.md) 中的 R21；各模块的备选方案见 R4–R15。
