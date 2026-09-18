# 契约：`tools/` 相对 002 的增量

只写与 002 交付状态的差异。未提及之处一律不动。

## 1. 新增常量

```python
WORKSPACE_SOURCE = "README.md"
WORKSPACE_TRANSLATION = "README.zh-CN.md"
WORKSPACE_SELECTOR_LINES = {
    "README.md": "**English** · [简体中文](README.zh-CN.md)",
    "README.zh-CN.md": "[English](README.md) · **简体中文**",
}
WORKSPACE_ANCHOR_SEQUENCE = [
    "chefs-pick-oss-starter-workspace", "layout",
    "common-commands", "publishing", "license",
]
```

## 2. 路径解析（复用 C23 的模式）

C25 ~ C27 一律用

```python
repo_root = Path(__file__).resolve().parent.parent
```

解析路径，**刻意忽略 `ctx.template_dir`**，并在各自的文档字符串中写明这一点，与 `check_c23` 的写法一致。理由见 research R3：工作区首页不在 `template/` 之下。

`template/` 不存在、`README.md` 不存在、**或 `README.zh-CN.md` 不存在**时，C25、C26、C27 三者一律抛 `SkipCheck`，不得 FAIL——与 C23 对缺失契约的处理同口径。译本缺失也要跳过，是因为改造过程中必然出现「英文原文已重写、译本尚未建立」的中间状态（tasks.md 的 T008 与 T009 之间），此时硬失败会把一个预期中的过渡态报成错误。

## 3. C25 Workspace language structure

判定项，任一不满足即 FAIL：

1. `README.md` 与 `README.zh-CN.md` 均存在。
2. 两份文件各自第 3 行（首个标题与一条空行之后）逐字等于 `WORKSPACE_SELECTOR_LINES` 中对应的那一行。
3. 两份文件的锚点序列均逐字等于 `WORKSPACE_ANCHOR_SEQUENCE`；不一致时报告必须给出 `expected:`、`found:`，并在非空时给出 `missing:` 与 `unexpected:`（与 C11 同一写法）。
4. 每个标题之前一行必须是锚点行；锚点数必须等于标题数。
5. `README.zh-CN.md` 含契约 §3 的规范性声明，逐字；`README.md` 不含。
6. 语言纯度按契约 §5 判定，复用 `strip_for_purity`、`cjk_count`、`longest_english_run`。

## 4. C26 Workspace facts

判定项，任一不满足即 FAIL。每条问题信息必须**同时给出声明值与实际值**：

1. 两份文件中按契约 §6 提取的 `template/` 文件数，必须等于 `template/` 下被 git 跟踪的文件数。
2. 两份文件中按契约 §6 提取的结构校验项数，必须等于 `CHECKS` 注册表的条目数。
3. `specs/` 下每一个目录名，都必须在两份文件中各自以 `` `specs/<目录名>/` `` 的形式出现至少一次。

问题信息的写法：

```
README.md: template file count says 26, actual 28
README.zh-CN.md: spec directory 003-workspace-self-compliance is not listed
```

取不到声明值（句式缺失）时同样 FAIL，信息写成 `README.md: no template file count found`。

## 5. C27 Workspace translation freshness

与 `check_c24` 同构，作用对象换成工作区首页：

- 来源标记缺失、格式不符、或多于一处 → **FAIL**（结构问题）。
- 标记存在且格式正确，但摘要不等于 `README.md` 当前摘要 → **WARN**（`--release` 下 FAIL），信息写成
  `README.zh-CN.md: source marker is stale for README.md (recorded <旧>, current <新>); run python3 tools/check_template.py --update-digests`。

## 6. 注册表

```python
"C25": ("Workspace language structure", lambda ctx: check_c25(ctx)),
"C26": ("Workspace facts", lambda ctx: check_c26(ctx)),
"C27": ("Workspace translation freshness", lambda ctx: check_c27(ctx)),
```

追加在 `"C24"` 之后。总数由 24 变为 **27**。

## 7. `update_digests()`

处理完 `template/` 下的译本后，再处理工作区首页的译本，**复用同一段替换实现**：单处正则替换、`write_bytes` 写回、发现重复标记则拒绝并原样保留文件。不得为工作区另写一份替换逻辑（research R9）。

## 8. 禁止事项

- 不得改动 `check_c01` ~ `check_c24` 中任何一行影响其对 `template/` 判定的代码。
- 不得改动 `strip_for_purity`、`cjk_count`、`longest_english_run`、`ANCHOR_RE`、`DIGEST_RE` 的行为；只允许调用。
- 不得改动 `tools/verify_sources.py`。
