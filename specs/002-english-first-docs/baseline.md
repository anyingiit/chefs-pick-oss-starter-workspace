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

_待 T033 填写。_

## 人工验收（T037）

_待 T037 填写。_
