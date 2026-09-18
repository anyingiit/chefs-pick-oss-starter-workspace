# 验证指南：英文为主、中文另起一份的文档语言结构

**对应**：[spec.md](./spec.md) 的 SC-001 ~ SC-014；[plan.md](./plan.md)。

本文件只写**怎么验**，不写怎么实现。全部命令在开发工作区根目录运行。

## 前置条件

- Python 3.10+（本机 3.14.6），已安装 PyYAML 6.x。
- 不需要网络，也不需要 `gh` CLI——本功能不刷新认可度数据。

## A. 自动验证

按顺序执行，全部通过才算完成。

| 编号 | 命令 | 期望 | 覆盖 |
|---|---|---|---|
| A1 | `python3 -m unittest discover -s tools/tests` | `OK`，用例数不少于改造前的 199 | 全部检查项的正反例 |
| A2 | `python3 tools/check_template.py` | 末行 `Summary: 24 passed, 0 failed, 0 warned, 0 skipped` | 全部结构约束 |
| A3 | `python3 tools/check_template.py --release` | 同上，退出码 0 | 发布口径（C24 按 FAIL 计） |
| A4 | `python3 tools/check_template.py --only C11` | `PASS C11 Language structure` | SC-001、SC-002、SC-005、SC-006、SC-008、SC-013；FR-002 ~ FR-008 |
| A5 | `python3 tools/check_template.py --only C23` | `PASS C23 Contract parity` | SC-014、FR-018 |
| A6 | `python3 tools/check_template.py --only C24` | `PASS C24 Translation freshness` | SC-011、FR-012、FR-014 |
| A7 | `python3 tools/check_template.py --only C13,C22` | 两项都 PASS | SC-007、FR-010 |
| A8 | `python3 tools/check_template.py --only C14` | `PASS C14 Relative links` | 两个新文件的链接可解析 |
| A9 | `time python3 tools/check_template.py` | 实际耗时不超过 5 秒 | plan 的 Performance Goals |

### A10 语言纯度的独立复核

不依赖 `check_template.py` 自身，另跑一遍计数，防止检查项与实现同时写错：

```bash
python3 - <<'PY'
import os, re
G = 'template/.github'
def cjk(s): return sum(1 for c in s if '一' <= c <= '鿿')
en = ['README.md', 'chefs-pick/GUIDE.md', 'chefs-pick/SOURCES.md',
      'chefs-pick/MAINTAINING.md', 'chefs-pick/UPGRADE-TO-TEAM.md',
      'chefs-pick/CHANGELOG.md', 'chefs-pick/SETUP.md', 'chefs-pick/LICENSE']
zh = ['README.zh-CN.md', 'chefs-pick/SETUP.zh-CN.md']
for f in en:
    t = open(os.path.join(G, f), encoding='utf-8').read()
    # 语言入口行是唯一允许含中文的一行
    t = '\n'.join(l for l in t.split('\n') if '简体中文' not in l)
    print(f'{f:<34} CJK={cjk(t)}   {"OK" if cjk(t)==0 else "*** FAIL ***"}')
for f in zh:
    t = open(os.path.join(G, f), encoding='utf-8').read()
    runs = max((len(m.split()) for m in re.findall(r"(?:[A-Za-z][A-Za-z'’-]*(?:\s+|$)){2,}", t)), default=0)
    print(f'{f:<34} 最长英文词串={runs}   {"OK" if runs < 6 else "需人工复核"}')
PY
```

期望：8 个英文文件的 `CJK` 全为 0；两份译本的最长英文词串小于 6（大于等于 6 时人工看一眼是不是产品名连写，不是就改）。

### A11 锚点不可见

```bash
grep -c '^<!-- anchor: ' template/.github/README.md template/.github/README.zh-CN.md \
       template/.github/chefs-pick/SETUP.md template/.github/chefs-pick/SETUP.zh-CN.md
```

期望：前两个文件各 12，后两个各 3。锚点是 HTML 注释，GitHub 渲染后可见字符数为 0（SC-013）。

### A12 单一数据源只有一份

```bash
grep -rc '| Placeholder | Meaning | Files | Example |' template/ | grep -v ':0$'
grep -rc '<!-- summary:start -->' template/ | grep -v ':0$'
grep -rc '<!-- adoption-data:start -->' template/ | grep -v ':0$'
```

期望：每条命令各只输出一行，计数均为 1（SC-012）。

## B. 人工验证

自动检查覆盖不到的部分，改造完成后由维护者确认。

| 编号 | 步骤 | 期望 | 覆盖 |
|---|---|---|---|
| V1 | 在 GitHub 上预览 `template/.github/README.md` 的渲染结果 | 页面上看不到任何 `<!-- anchor:` 或 `<!-- translation-of:` 字样；语言入口显示为一行 `English · 简体中文` | SC-013 |
| V2 | 从英文首页点"简体中文" | 到达中文首页，其顶部有指回英文首页的入口 | SC-005、FR-005 |
| V3 | 通读中文首页 | 读完不需要回到英文版补齐任何内容；12 个章节一个不少 | SC-004、SC-006、FR-007 |
| V4 | 通读英文首页 | 读完不遇到任何中文散文，也没有需要中文才能理解的缺口 | SC-003、FR-001 |
| V5 | 从中文首页点向模块讲解 | 落到英文版，**没有**任何"目标是英文"的提示 | 规格澄清第 7 问 |
| V6 | 在测试仓库中执行 language-structure §6 的清理命令 | 一条命令执行完毕，`git status` 中不再有引导层文件；`git grep -n 'chefs-pick'` 无输出 | SC-007、FR-010 |
| V7 | 改动 `template/.github/README.md` 的任意一句英文后运行 `python3 tools/check_template.py` | 出现 `WARN C24`，指名 `README.zh-CN.md` 过期；退出码仍为 0 | FR-014 |
| V8 | 承接 V7，再运行 `--release` | `FAIL C24`，退出码 1 | FR-015、宪章发布门禁 6 |
| V9 | 承接 V8，更新译文后运行 `--update-digests`，再跑 A2 | 摘要被刷新，A2 恢复全绿 | FR-012 |
| V10 | 对照 `MAINTAINING.md` 的 `## Release gates` | 英文完整列出 **6** 条门禁；正文中的 "gate 2"、"gate 4" 仍指向原来那两条 | research R9、宪章 v2.1.0 |

V7 ~ V9 会改动工作区，做完后用 `git checkout -- template/` 还原。

## C. 回归确认

本功能不得改变的东西，逐项确认：

| 编号 | 命令 | 期望 |
|---|---|---|
| R1 | `git diff --stat template/ -- ':!*.github/README*' ':!*chefs-pick*'` | 无输出——交付给使用者的项目文件一个字节都没动（FR-009） |
| R2 | `python3 tools/check_template.py --only C15` | PASS——MIT 正文未被改动 |
| R3 | `grep -c '★' template/.github/chefs-pick/SOURCES.md` | 与改造前相同——认可度数字只改契约那一侧，模板侧不动 |
| R4 | `git ls-files template/ \| wc -l` | `28`（改造前 26，新增两份译本） |

## D. 验收对照表

| 成功标准 | 由谁验证 |
|---|---|
| SC-001、SC-002 英文版中文字符数为 0 | A4、A10 |
| SC-003、SC-004 两侧读者都不跳过内容 | V3、V4 |
| SC-005 一步互达 | A4、V2 |
| SC-006 章节覆盖率 100%，其余四份无译本无入口 | A4、V3 |
| SC-007 清理后无残留 | A7、V6 |
| SC-008 四项由日常校验硬失败 | A4 |
| SC-010 发布门禁只增 1 项 | V10 |
| SC-011 新鲜度由来源标记表示 | A6、V7 ~ V9 |
| SC-012 单一数据源各只一份 | A12 |
| SC-013 章节可定位、锚点不可见 | A11、V1 |
| SC-014 契约与模板数字一致 | A5 |
