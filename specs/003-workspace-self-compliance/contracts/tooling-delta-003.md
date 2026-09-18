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

**跳过条件（已修正，见下方「原规则与废弃理由」）**：只有 `template/` 目录本身不存在时，C25、C26、C27 三者才抛 `SkipCheck`——即这压根不是工作区仓库本身，与 C23 对缺失契约的处理同口径。

`template/` 存在（即这确实是工作区仓库）之后，下列情形一律是 **FAIL**，不是 `SkipCheck`：

- `README.md` 不存在——信息形如 `README.md: file does not exist`；
- `README.md` 存在但找不到 `WORKSPACE_SELECTOR_LINES["README.md"]` 那一行——信息形如 `README.md: language selector: missing the verbatim line '...'`；
- 语言入口已就位但 `README.zh-CN.md` 不存在——本就应当判 FAIL（见下段），信息必须点名是 `README.zh-CN.md` 缺失。

三者共用的判定逻辑收敛到一个 `_workspace_gate(repo_root)` 辅助函数：只有 `template/` 缺失时它才抛 `SkipCheck`；`README.md` 缺失或缺少选择器行时，它返回一条 FAIL 信息供调用方直接返回，不再继续后续判定项。

译本缺失从来都不是跳过条件，这一点未变：`README.md` 的语言入口指向 `README.zh-CN.md`，若以译本缺失为跳过条件，则译本一旦被误删，三项检查会全部静默失效，而首页上那条指向不存在文件的死链无人发现。语言入口已就位而译本缺失，本就应当判 FAIL。

**原规则与废弃理由**：这一节在 003 功能改造进行中时，跳过条件原本还包含「`README.md` 不存在」与「`README.md` 中找不到选择器行」——判据是「语言入口是否已就位」，即本功能的改造是否已经开始，而不是译本文件是否存在。这是为了让改造过程中 `README.md` 已重写、译本尚未建立的那一小段（tasks.md 的 T008 与 T009 之间）不必整套校验报错，当时这是真实、刻意接受的过渡状态，不是误报。

但改造早已交付，`README.md` 已经带有选择器行；这条规则留到现在，就从「过渡期的迁移便利」变成了一个漏洞——只需删掉或改错 `README.md` 里那一行选择器文字（例如 `**English** · [简体中文](README.zh-CN.md)`），就能让语言结构（C25）、事实准确性（C26）、译文新鲜度（C27）三项检查同时静默跳过、全部不再执行，而 `python3 tools/check_template.py` 仍然报 exit code 0。这不是假设：删掉 `README.md` 里那一行，原本 27 项检查会变成 24 通过、0 失败、0 警告、3 跳过。因此现在把「`README.md` 缺失」与「选择器行缺失」都改判为 FAIL,只把「`template/` 不存在」这一个刻意保留为 `SkipCheck`——它对应的是「这根本不是工作区仓库」，与前两者「这确实是工作区仓库，但结构坏了」性质不同。

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

- 来源标记缺失、格式不符、或多于一处 → **FAIL**（结构问题）。「多于一处」按*候选*而非仅按格式正确的标记计数：任何形如 `<!-- translation-of: README.md sha256:... -->` 的行都算一个候选，摘要部分是否是合法的 16 位十六进制不影响它被计入候选数——一条格式正确的标记与一条摘要写错的重复标记并存时，必须判为「找到 2 处标记行」FAIL，而不是只看到那条格式正确的就判过。恰好一个候选时才检验其摘要格式是否合法；不合法同样按「缺失或格式不符」处理。
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
