# 验收指南：工作区自身遵守模板定下的规矩

## A. 自动验证

| 编号 | 命令 | 期望 |
|---|---|---|
| A1 | `python3 -m unittest discover -s tools/tests` | 末尾 `OK`，用例数不少于 245 |
| A2 | `python3 tools/check_template.py` | 末行 `Summary: 27 passed, 0 failed, 0 warned, 0 skipped`，退出码 0 |
| A3 | `python3 tools/check_template.py --release` | 退出码 0，无 FAIL |
| A4 | `python3 tools/check_template.py --only C25` | PASS |
| A5 | `python3 tools/check_template.py --only C26` | PASS |
| A6 | `python3 tools/check_template.py --only C27` | PASS |

### A7 语言纯度的独立复核

不依赖 `check_template.py` 自身，另跑一遍计数：

```bash
python3 - <<'PY'
import re, sys
sys.path.insert(0, 'tools')
from check_template import strip_for_purity, cjk_count, longest_english_run
sel = {'README.md': '**English** · [简体中文](README.zh-CN.md)',
       'README.zh-CN.md': '[English](README.md) · **简体中文**'}
for f, s in sel.items():
    t = strip_for_purity(open(f, encoding='utf-8').read(), s)
    print(f'{f:<18} CJK={cjk_count(t):<5} 最长英文词串={longest_english_run(t)}')
PY
```

期望：`README.md` 的 `CJK` 为 0；`README.zh-CN.md` 的最长英文词串小于 6。

### A8 锚点不可见且两侧一致

```bash
grep -c '^<!-- anchor: ' README.md README.zh-CN.md
diff <(grep -o '^<!-- anchor: [a-z0-9-]*' README.md) \
     <(grep -o '^<!-- anchor: [a-z0-9-]*' README.zh-CN.md) && echo "锚点序列一致"
```

期望：两个文件各 5 个锚点；`diff` 无输出。

### A9 事实与实际一致

```bash
echo "template/ 实际文件数: $(git ls-files template/ | wc -l)"
grep -o '`template/` holds [0-9]* files' README.md
grep -o '`template/` 共 [0-9]* 个文件' README.zh-CN.md
echo "实际规格目录: $(ls specs/)"
for d in $(ls specs/); do
  grep -q "specs/$d/" README.md || echo "英文版缺: $d"
  grep -q "specs/$d/" README.zh-CN.md || echo "中文版缺: $d"
done
echo "检查项数: $(python3 -c "import sys;sys.path.insert(0,'tools');import check_template;print(len(check_template.CHECKS))")"
grep -o '[0-9]* structural checks' README.md
```

期望：声明值与实际值逐项相等；无「缺」字输出。

### A10 C26 与 C27 的行为验证

```bash
# 事实不符必须硬失败
sed -i 's/`template\/` holds 28 files/`template\/` holds 99 files/' README.md
python3 tools/check_template.py --only C26 ; echo "exit=$?"
git checkout -- README.md

# 译本过期只提示，发布门禁下硬失败
sed -i 's/development and maintenance workspace/development and maintenance work space/' README.md
python3 tools/check_template.py --only C27 ; echo "exit=$?"
python3 tools/check_template.py --only C27 --release ; echo "exit=$?"
git checkout -- README.md
```

期望：C26 输出 `FAIL C26` 且同时给出 `99` 与 `28`，退出码 1；C27 日常为 `WARN C27` 退出码 0，`--release` 为 `FAIL C27` 退出码 1；两次还原后 `git status --short` 无输出。

## B. 人工验收

| 编号 | 步骤 | 期望 | 覆盖 |
|---|---|---|---|
| V1 | 在 GitHub 上预览工作区首页 | 看不到任何 `<!-- anchor:` 或 `<!-- translation-of:` 字样；语言入口为一行 `English · 简体中文` | SC-005 |
| V2 | 从英文首页点「简体中文」 | 到达中文首页，其顶部有指回英文首页的入口 | SC-005 |
| V3 | 通读中文首页 | 读完不需要回查英文版；5 个章节一个不少 | SC-004、SC-006 |
| V4 | 通读英文首页 | 读完不遇到任何中文散文，也没有需要中文才能理解的缺口 | SC-002、SC-003 |
| V5 | 照英文首页的「后续发布」步骤，在一个**已有历史和标签**的测试模板仓库上走一遍 | 推送成功且为快进；原有提交与标签仍可从默认分支到达 | SC-001 |
| V6 | 照英文首页的「首次发布」步骤，在一个空仓库上走一遍 | 首次发布成功 | SC-009 |
| V7 | 对照 `specs/001-chefs-pick-starter/quickstart.md` §B | 已补上后续发布的步骤，并写明原步骤只适用于空仓库 | SC-009、FR-004 |

V5 的验证方法：

```bash
# 在测试克隆中，确认标签指向的提交仍可从默认分支到达
git -C <clone-path> merge-base --is-ancestor <标签指向的提交> origin/main && echo "可达 ✓"
```

## C. 回归确认

本功能不得改变的东西，逐项确认：

| 编号 | 命令 | 期望 |
|---|---|---|
| R1 | `git diff --stat <改造前提交> HEAD -- template/` | 无输出——`template/` 一个字节都没动（FR-017、SC-010） |
| R2 | `python3 tools/check_template.py --only C01,C11,C23,C24` | 全部 PASS，与改造前一致 |
| R3 | `git ls-files template/ \| wc -l` | `28`，与改造前相同 |
| R4 | `git diff --stat <改造前提交> HEAD -- tools/verify_sources.py` | 无输出——本功能不碰数据刷新工具（契约 §8） |

## D. 验收对照表

| 成功标准 | 由谁执行 |
|---|---|
| SC-001 原有提交与标签 100% 可达 | V5 |
| SC-002 英文版中文字符数为 0 | A7、V4 |
| SC-003、SC-004 两侧读者都不跳过内容 | V3、V4 |
| SC-005 一步互达 | A4、V1、V2 |
| SC-006 章节覆盖率 100% | A8、V3 |
| SC-007 事实偏差为 0 | A9、A5 |
| SC-008 四类判定全部由日常校验硬失败 | A4、A5、A10 |
| SC-009 两处发布流程均覆盖两种情形 | V6、V7 |
| SC-010 `template/` 逐字节未变 | R1、R3 |
| SC-011 既有 24 项判定不变 | R2 |
