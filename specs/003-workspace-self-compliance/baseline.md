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

_待填写。_

## 人工验收（T018）

_待填写。_
