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
| V5 | 在**已有历史和标签**的测试模板仓库上走一遍后续发布 | **本轮未执行**，原因：需要一个可写的测试模板仓库，本环境不便创建。但本流程的正确性已由 2026-09-18 对真实模板仓库的一次实际发布验证——当时正是按这套步骤在克隆中替换内容后快进推送，`v1.0.0` 标签指向的 `99cba97` 至今仍可从默认分支到达 | ⚠️ 未执行，另有实证 |
| V6 | 在空仓库上走一遍首次发布 | **本轮未执行**，原因同 V5。该步骤本身未改动，与 1.0.0 发布时所用一致 | ⚠️ 未执行 |
| V7 | `quickstart.md` §B 已补后续发布步骤并写明原步骤只适用于空仓库 | §B 第 2 步已拆为「**首次发布到空仓库时**（本步骤只适用于这一种情形）」与「**后续发布到已有内容的仓库时**」两条，后者指向首页 `Publishing` 一节并写明强推会让 `v1.0.0` 标签指向的提交不再可达 | ✅ 通过（SC-009、FR-004） |

V1 ~ V4、V7 五项通过。V5、V6 未执行，按 T018 的要求如实记录而非标记通过——它们需要真实的测试仓库，留待维护者在下一次发布时顺带确认。

