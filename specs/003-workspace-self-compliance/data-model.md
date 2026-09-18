# Phase 1 数据模型：工作区自身遵守模板定下的规矩

本功能不引入运行时数据结构，只引入**校验对象**。以下是各对象的构成、约束与状态。

## 1. 工作区门面文档（Workspace front-page document）

工作区中面向读者、需受语言与事实约束的文档。

| 字段 | 取值 | 约束 |
|---|---|---|
| 路径 | 仓库根目录下的相对路径 | 目前恰好两份：`README.md`、`README.zh-CN.md` |
| 角色 | `source`（英文原文）｜ `translation`（译本） | 每份译本恰好对应一份原文 |
| 语言 | `en` ｜ `zh-CN` | 由文件名推定，不另行声明 |
| 语言入口 | 逐字固定的一行 | 见契约 §1；必须位于首个标题之后 |
| 章节锚点序列 | 有序的锚点 id 列表 | 两种语言版本必须逐字相同，见契约 §2 |
| 规范性声明 | 逐字固定的一段 | 仅 `translation` 有；`source` 不得出现 |
| 来源标记 | `<!-- translation-of: <源文件名> sha256:<16 hex> -->` | 仅 `translation` 有，且**恰好一处** |

**状态**：`translation` 相对其 `source` 有两种状态——**已对齐**（标记中的摘要等于源文件当前摘要）与**已过期**（不等）。已过期在日常校验中为 WARN，在 `--release` 下为 FAIL。这与模板译本的状态机同构（002 规格 FR-014、FR-015）。

## 2. 可机读事实（Machine-checkable fact）

首页中声明的、可从仓库直接测得的事实。

| 字段 | 说明 |
|---|---|
| 标识 | `template-file-count` ｜ `spec-directories` ｜ `check-count` |
| 声明值 | 从首页文本中按固定句式提取 |
| 实际值 | 从仓库现状测得 |
| 判定 | 声明值必须等于实际值 |

**实际值的来源**：

| 标识 | 实际值取自 |
|---|---|
| `template-file-count` | `template/` 下被 git 跟踪的文件数 |
| `spec-directories` | `specs/` 下的目录名集合 |
| `check-count` | 检查项注册表的条目数 |

**约束**：每项事实在**英文版与中文版中都要声明且都要核对**。只改一侧即为不一致，必须失败——这正是 002 中「同一数据出现两处必然漂移」的教训（002 契约 tooling-delta §8.5）。

**当前实测**：

| 标识 | 声明值 | 实际值 | 是否一致 |
|---|---|---|---|
| `template-file-count` | 26 | 28 | 否 |
| `spec-directories` | 仅 001 | 001、002、003 | 否 |
| `check-count` | 24 | 24（改造后 27） | 是（改造后需同步） |

## 3. 发布流程描述（Publishing procedure description）

工作区中描述如何把 `template/` 同步到模板仓库的文本。

| 字段 | 取值 |
|---|---|
| 位置 | `README.md` 的发布一节；`specs/001-chefs-pick-starter/quickstart.md` §B |
| 覆盖情形 | `first`（空仓库首次发布）｜ `subsequent`（已有内容的后续发布） |
| 安全性 | 执行后模板仓库原有提交与标签是否仍可从默认分支到达 |

**约束**：两个位置都必须覆盖 `first` 与 `subsequent` 两种情形；`subsequent` 的步骤必须是快进推送，且必须显式写明不得使用 `--force` 以及被拒绝时如何处置。

**当前状态**：两处都只覆盖 `first`；首页还把 `first` 的步骤当作通用步骤呈现，属直接错误。

## 4. 检查项（Check）

对既有检查项登记表的扩充，不改变其结构。

| 编号 | 名称 | 判定对象 | 失败方式 |
|---|---|---|---|
| C25 | Workspace language structure | 对象 1 | FAIL |
| C26 | Workspace facts | 对象 2 | FAIL |
| C27 | Workspace translation freshness | 对象 1 的状态 | WARN；`--release` 下 FAIL |

**约束**：三项均从**仓库根**解析路径，不受 `--template-dir` 影响；均不得改变 C01 ~ C24 对 `template/` 的任何判定（FR-016、SC-011）。
