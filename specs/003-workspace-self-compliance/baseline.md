# 基线与验证记录

本文件由 T001 创建，T017、T018 追加。

## 改造前基线（T001，2026-09-18）

| 项目 | 命令 | 实测 |
|---|---|---|
| 单元测试 | `python3 -m unittest discover -s tools/tests 2>&1 \| tail -3` | `Ran 239 tests in 0.399s` / 空行 / `OK` |
| 结构校验 | `python3 tools/check_template.py \| tail -1` | `Summary: 24 passed, 0 failed, 0 warned, 0 skipped` |
| 模板文件数 | `git ls-files template/ \| wc -l` | `28` |
| 首页中文字符数 | `python3 -c "import re;print(len(re.findall(r'[一-鿿]',open('README.md',encoding='utf-8').read())))"` | `288` |

四项实测值与期望值（`Ran 239 tests` / `OK`、`Summary: 24 passed, 0 failed, 0 warned, 0 skipped`、`28`、`288`）逐一相符，改造可以开始。

## C26、C27 行为验证（T017）

按 [quickstart.md](./quickstart.md) A10 执行，全部符合契约。

| # | 扰动 | 命令 | 实测输出 | 退出码 | 期望 | 结论 |
|---|---|---|---|---|---|---|
| 1 | `README.md` 中 `holds 28 files` 改为 `holds 99 files` | `--only C26` | `FAIL C26 Workspace facts`<br>`  - README.md: template file count says 99, actual 28` | `1` | 硬失败且同时给出声明值与实际值 | ✅ 相符（FR-012） |
| 2 | `README.md` 中一句英文散文改动 | `--only C27` | `WARN C27 Workspace translation freshness`<br>`  - README.zh-CN.md: source marker is stale for README.md (recorded b46563346c02a932, current 1880d420cfc391b4); run python3 tools/check_template.py --update-digests` | `0` | 只提示，不影响退出码 | ✅ 相符（FR-014） |
| 3 | 承接第 2 项 | `--only C27 --release` | `FAIL C27 Workspace translation freshness`（同一条信息） | `1` | 发布门禁下硬失败 | ✅ 相符（FR-015） |
| 4 | `git checkout -- README.md` 还原 | `git status --short` | 无输出 | — | 工作区干净 | ✅ 相符 |

另外单独验证了契约 §2 的跳过判据（analyze 第 2 轮的修正点）：

| 状态 | 三项检查的表现 |
|---|---|
| `README.md` 无语言入口（改造未开始） | `SKIP C25/C26/C27: README.md: language-selector line not present yet` |
| `README.md` 有语言入口但译本不存在 | `FAIL C25/C26/C27`，共 `24 passed, 3 failed` |

第二行是关键：若按第 1 轮的写法以「译本缺失」为跳过条件，译本一旦被误删，三项检查会全部静默失效，而首页那条指向不存在文件的死链无人发现。


## 人工验收（T018）

| 编号 | 期望 | 实测 | 结论 |
|---|---|---|---|
| V1 | 渲染后看不到 `<!-- anchor:` 与 `<!-- translation-of:`；语言入口为一行 | 两份首页各 5 个锚点，全部为 HTML 注释独占一行；来源标记同为 HTML 注释；语言入口各为单独一行，逐字为 `**English** · [简体中文](README.zh-CN.md)` 与 `[English](README.md) · **简体中文**` | ✅ 通过（SC-012、SC-005） |
| V2 | 从英文首页一步到中文首页，且能一步返回 | 两份文件双向互指，链接目标均存在 | ✅ 通过（SC-005） |
| V3 | 通读中文首页无需回查英文；5 个章节一个不少 | 锚点序列两侧逐字相同，均为 5 项；章节覆盖率 100% | ✅ 通过（SC-004、SC-006） |
| V4 | 通读英文首页不遇中文散文，也无内容缺口 | 按契约 §5 剥离后 `README.md` 的中文字符数为 0（改造前 288）；译本最长连续英文词串为 4（小于 6） | ✅ 通过（SC-002、SC-003） |
| V5 | 在**已有历史和标签**的测试模板仓库上走一遍后续发布 | **仍未在真实模板仓库上执行**。两项旁证：（一）2026-09-18 对真实模板仓库的那次实际同步走的就是「在克隆中替换内容后快进推送」，`v1.0.0` 指向的 `99cba97` 至今仍可从默认分支到达（已于 1.1.0 发布后复验）；（二）评审提出三项缺陷后，修正版的八步流程在一个专门搭建的合成夹具上端到端验过——夹具同时具备「克隆落后于远端」「克隆带有无关本地提交」「源树删掉一个文件」「某路径由文件变为目录」四种条件，旧流程在该夹具上如实崩溃（`cp` 报错、删除未生效），新流程正确暂存 `D sub/gone.txt`、处理类型变更并快进推送成功 | ⚠️ 未在真实仓库执行，合成夹具已端到端验证 |
| V6 | 在空仓库上走一遍首次发布 | **本轮未执行**，原因同 V5。该步骤本身未改动，与 1.0.0 发布时所用一致 | ⚠️ 未执行 |
| V7 | `quickstart.md` §B 已补后续发布步骤并写明原步骤只适用于空仓库 | §B 第 2 步已拆为「**首次发布到空仓库时**（本步骤只适用于这一种情形）」与「**后续发布到已有内容的仓库时**」两条，后者指向首页 `Publishing` 一节并写明强推会让 `v1.0.0` 标签指向的提交不再可达 | ✅ 通过（SC-009、FR-004） |

V1 ~ V4、V7 五项通过。V5、V6 仍记为未执行，按 T018 的要求如实记录而非标记通过——它们要的是在真实模板仓库上跑一遍**发布流程**，这与下一节的发布门禁验证不是一回事，不能相互顶替。

## 发布门禁 2 与 4 的验证（2026-09-18，1.1.0 发布后补做）

由维护者在真实测试仓库 [chefs-pick-gate-test-20260918](https://github.com/anyingiit/chefs-pick-gate-test-20260918) 上执行，该仓库于 2026-09-18T09:13:02Z 由模板的 **Use this template** 生成。本节记录的是**生成仓库**的行为，与 T018 的 V5、V6（发布流程）无关，二者覆盖面不同。

### 门禁 2 — 新仓库首次 CI 通过 ✅

| 项 | 实测 |
|---|---|
| 运行 | `35328390227`（`Initial commit`，run #1） |
| 结论 | `success` |
| 作业 | `Lint`、`Test` 各一，均 `success` |
| 并行性 | 两者同在 `09:13:16` 启动，分别落在 runner `1000004003` 与 `1000004004` 上，确为并行 |
| 总耗时 | `09:13:13 → 09:13:23`，**10 秒**（quickstart §C 的上限为 1 分钟） |

`Lint` 中的「Check that actions are pinned to full commit SHAs」一步通过，工作流内唯一的动作引用为 `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1`——**门禁 5 由此一并得到印证**。

### 门禁 4 — 社区标准 ✅（有一处保留）

构成条件逐项核对：`README.md`、`LICENSE`（MIT，GitHub 已识别）、`CODE_OF_CONDUCT.md`、`CONTRIBUTING.md`、`SECURITY.md`、两份 Issue 表单加 `config.yml`、`PULL_REQUEST_TEMPLATE.md` 全部存在；仓库已填 description 与 topics，Issues 与 Discussions 均已开启。

清理后的状态：`git grep CHANGEME` 无输出；引导层（两份 README 与 `chefs-pick/`）已消失；无失效引用；首页为使用者自己的 README；模板身份无残留——grep 命中的三条经核实全是**测试仓库自身的 URL**（仓库名恰好含 `chefs-pick`），排除仓库名后为零。

**保留一处**：Community Standards 页面本身，本环境可用的 GitHub API 工具读不到（无 community profile 接口）。已核对的是它的全部构成条件；页面上的绿勾采信维护者的报告。按 research F10，个人账号的公共仓库不会列出「内容举报」一项。

### 顺带覆盖

同一仓库上的清理提交（`chore: remove template guide`，run `35328816935`）CI 同样通过，耗时 7 秒，实际覆盖了 001 快速开始指南 §C 的 V7（删除模块后 CI 仍通过、不留失效链接）。

**结论**：六道发布门禁至此全部满足——1、3、5、6 由 `--release` 自动覆盖（退出码 0），2 与 4 由本次测试仓库人工确认。

