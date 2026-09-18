# 基线与验证记录

本文件由 T001 创建，T033、T037 追加。

## 改造前基线（T001，2026-09-18）

| 项目 | 命令 | 实测 | 期望 | 结论 |
|---|---|---|---|---|
| 单元测试 | `python3 -m unittest discover -s tools/tests` | `Ran 199 tests` / `OK` | `OK`（199 个用例） | ✅ 相符 |
| 结构校验 | `python3 tools/check_template.py` | `Summary: 22 passed, 0 failed, 0 skipped` | 同左 | ✅ 相符 |
| 模板文件数 | `git ls-files template/ \| wc -l` | `26` | `26` | ✅ 相符 |

三项全部符合，改造可以开始。

## C24 行为验证（T033）

扰动方式：把 `template/.github/README.md` 中的 `ready to use out of the box` 临时改为
`ready to use straight out of the box`（纯散文改动，不触碰锚点、清理命令等其他检查项的判据）。

| # | 命令 | 实测输出 | 退出码 | 期望 | 结论 |
|---|---|---|---|---|---|
| 1 | `python3 tools/check_template.py` | `WARN C24 Translation freshness`（指名 `README.zh-CN.md` 摘要过期）<br>`Summary: 23 passed, 0 failed, 1 warned, 0 skipped` | `0` | WARN 且退出码 0 | ✅ 相符（FR-014） |
| 2 | `python3 tools/check_template.py --release` | `FAIL C24 Translation freshness`<br>`Summary: 23 passed, 1 failed, 0 warned, 0 skipped` | `1` | FAIL 且退出码 1 | ✅ 相符（FR-015、宪章发布门禁 6） |
| 3 | `git checkout -- template/.github/README.md` 后再跑 A2 | `Summary: 24 passed, 0 failed, 0 warned, 0 skipped` | `0` | 恢复全绿 | ✅ 相符 |

还原后 `git status --short template/` 无输出，工作区干净。

注：首次尝试的扰动（在文件末尾追加空行）同时触发了 C21，掩盖了 C24 的退出码，已换成上述纯散文扰动重做。

## 人工验收（T037）

| 编号 | 期望 | 实测 | 结论 |
|---|---|---|---|
| V1 | 渲染后看不到 `<!-- anchor:` 与 `<!-- translation-of:`；语言入口显示为一行 | 四个带锚点的文件中，非 HTML 注释形式的标记行数 = 0；四条语言入口均为第 4 行单行，逐字为 `**English** · [简体中文](README.zh-CN.md)`、`[English](README.md) · **简体中文**`、`**English** · [简体中文](SETUP.zh-CN.md)`、`[English](SETUP.md) · **简体中文**` | ✅ 通过 |
| V2 | 英文首页一步到中文首页，且能一步返回 | 两对文档双向互指，四个链接目标文件均存在 | ✅ 通过 |
| V3 | 通读中文首页无需回查英文；12 个章节一个不少 | README 英/中锚点序列均为 12 项且逐项相同；SETUP 均为 3 项且相同；章节覆盖率 100% | ✅ 通过 |
| V4 | 通读英文首页不遇中文散文，也无内容缺口 | 按契约 §5 剥离后，`README.md` 与 `SETUP.md` 的 CJK 计数均为 0；两份译本的最长连续英文词串分别为 5 与 3（均小于 6） | ✅ 通过 |
| V5 | 从中文首页点向模块讲解落到英文，且没有任何"目标是英文"的提示 | `README.zh-CN.md` 与 `SETUP.zh-CN.md` 中逐链接英文提示条数均为 0；全文仅有的 `English` 字样就是顶部语言入口本身 | ✅ 通过 |
| V6 | 一条清理命令执行完毕后引导层文件消失，`git grep -n 'chefs-pick'` 无输出 | 在由 `template/` 生成的测试仓库中执行 `git rm -r .github/README.md .github/README.zh-CN.md .github/chefs-pick`，退出码 0；文件数 28 → 18；`git grep -n 'chefs-pick'` 无输出（退出码 1） | ✅ 通过 |
| V10 | `## Release gates` 英文完整列出 6 条，正文 `gate 2`、`gate 4` 仍指向原来那两条 | 该节以 `All six gates must pass **before** the Release is created:` 开头，其下 6 条编号门禁全为英文（第 6 条为新增的译本对齐门禁）；正文中的 `gate 2`（首次 CI 通过）与 `gate 4`（社区标准全绿）指向未变 | ✅ 通过 |

七项全部通过。

注：V5 首次探测返回 1，经复核是探测表达式把 `and` / `or` 混用而未加括号导致的误报；V4 首次探测返回 4 个残留 CJK，原因是调用 `strip_for_purity()` 时把文件名误当成了语言入口参数，语言入口中的「简体中文」因而未被剥离。两处都是探测脚本自身的缺陷，文档本身无需改动。
