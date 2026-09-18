# 契约：维护工具的改动

**对应**：FR-011 ~ FR-015、FR-018；决策依据 [research.md](../research.md) R3、R6 ~ R8、R11。

本文件只写**相对现状的增量**。未提及的部分保持 [001 的 tooling.md](../../001-chefs-pick-starter/contracts/tooling.md) 原样。

## 1. `check_template.py` 的框架变化

### 1.1 新增 `WARN` 状态

现有结果只有 PASS / FAIL / SKIP，C24 需要第四种。

- 新增 `class WarnCheck(Exception)`：检查函数抛出它时该项记为 WARN，异常的 `args[0]` 是问题列表。
- 输出行：`WARN C24 <标题>`，问题逐条列在下面，格式与 FAIL 相同（两个空格加 `- `）。
- 汇总行改为：`Summary: <p> passed, <f> failed, <w> warned, <s> skipped`。
- **退出码**：WARN 不影响退出码（仍为 0）。带 `--release` 时，会 WARN 的检查改按 FAIL 计，退出码为 1。

### 1.2 新增 `--update-digests`

```text
python3 tools/check_template.py --update-digests [--template-dir PATH]
```

- 对每份译本，重新计算其英文原文的 sha256 前 16 位，就地改写该译本的来源标记行。
- 只改来源标记行，其余字节不动。
- 输出每个被更新的文件与新旧摘要；无变化时输出 `No digest needed updating.`。
- 与其他检查互斥：带这个参数时不运行任何检查，退出码 0（成功）或 2（使用错误）。

### 1.3 译本的发现方式

不写死语言列表（research R12）。在起步引导层内，文件名匹配 `^(?P<id>[A-Za-z-]+)\.(?P<lang>[a-z]{2}(-[A-Z]{2})?)\.md$` 且同目录存在 `<id>.md` 的，即为 `<id>.md` 的译本。当前只会匹配到 `README.zh-CN.md` 与 `SETUP.zh-CN.md`。

## 2. 常量改动（research R11）

| 常量 | 新值 |
|---|---|
| `GUIDANCE_HOME_TITLE` | `# Chef's Pick OSS Starter` |
| `CLEANUP_COMMAND` | `git rm -r .github/README.md .github/README.zh-CN.md .github/chefs-pick` |
| `PLACEHOLDER_TABLE_HEADER` | `\| Placeholder \| Meaning \| Files \| Example \|` |
| `FIELD_LABELS` | `Files`、`Level`、`Pick`、`Version`、`Upstream license`、`Evidence`、`Rule`、`Verified` |
| 级别取值 | `Required`、`Recommended`、`Optional`、`Optional (recommendation only)` |
| 证据类型 | `Exact stars`、`Rounded stars`、`Estimated users`、`Official platform feature`、`De facto standard`、`Not available` |
| `IDENTITY_RE` | **保持不变**：`(?i)chef'?s[ -]?pick\|主厨精选`。它检测模板作者身份是否泄漏进生成仓库，与文档语言无关，且 `主厨精选` 仍可能出现在中文译本中，必须继续识别 |

新增常量：

```python
TRANSLATED_DOCS = {".github/README.md", ".github/chefs-pick/SETUP.md"}
SELECTOR_LINES = {  # 路径 -> 逐字语言入口，取自 language-structure.md §1
    ".github/README.md": "**English** · [简体中文](README.zh-CN.md)",
    ".github/README.zh-CN.md": "[English](README.md) · **简体中文**",
    ".github/chefs-pick/SETUP.md": "**English** · [简体中文](SETUP.zh-CN.md)",
    ".github/chefs-pick/SETUP.zh-CN.md": "[English](SETUP.md) · **简体中文**",
}
ANCHOR_RE = re.compile(r"^<!-- anchor: ([a-z0-9][a-z0-9-]*) -->$")
DIGEST_RE = re.compile(r"^<!-- translation-of: (\S+) sha256:([0-9a-f]{16}) -->$")
ANCHOR_SEQUENCES = {  # 取自 language-structure.md §3
    "README": ["chefs-pick-oss-starter", "what-you-get", "required", "recommended",
               "optional", "the-picks-at-a-glance", "how-we-pick", "quick-start",
               "good-to-know", "clean-up-when-done", "feedback-and-contact", "license"],
    "SETUP": ["setup-checklist", "placeholders", "steps"],
}
SINGLE_SOURCE_MARKERS = ["| Placeholder | Meaning | Files | Example |",
                         "<!-- summary:start -->", "<!-- adoption-data:start -->"]
```

## 3. 纯度判定的公共函数

```python
def strip_for_purity(text: str, selector_line: str | None) -> str
```

按 research R6 依次删除：围栏代码块（含围栏行）→ HTML 注释 → 行内代码 → Markdown 链接的 `(目标)` 部分 → 裸 URL → 与 `selector_line` 逐字相同的那一行。返回剩余文本。

```python
def cjk_count(text: str) -> int          # U+4E00–U+9FFF 的字符数
def longest_english_run(text: str) -> int  # 最长的连续英文词个数，词 = [A-Za-z][A-Za-z'’-]*
```

"连续"的判定：两个词之间只隔空格、半角标点或换行时算连续；出现任何中文字符即中断。

## 4. 改造的检查项

### C08 占位符（微调）
表头常量换成英文（§2）。其余逻辑不变。译本不参与登记表比对——`SETUP.zh-CN.md` 不含登记表是设计要求，不是缺失。

### C11 语言结构（整体重写，标题改为 `Language structure`）
对起步引导层的每个 Markdown 文件，逐条判定下列断言；任一不满足即 FAIL，且报文必须指名是哪个文件、哪一条断言：

1. **纯度**：`.md` 文件按其 `lang` 判定（§3）。英文版 `cjk_count == 0`；中文版 `longest_english_run < 6`。`LICENSE` 不是 Markdown，单独判定 `cjk_count == 0`。
2. **语言入口**：路径在 `SELECTOR_LINES` 中的文件，必须恰好包含那一行逐字内容，且它出现在 H1 之后、与 H1 之间恰好一个空行。不在表中的引导层文件，**不得**包含 `SELECTOR_LINES` 的任何一个值，也不得包含 `](README.zh-CN.md)`、`](SETUP.zh-CN.md)` 之类指向译本的链接。
3. **互达**：入口中列出的每个相对目标文件都必须存在。
4. **锚点**：属于 `ANCHOR_SEQUENCES` 的四个文件，其锚点有序序列必须与常量逐一相同；每个标题上方必须紧贴一个锚点行，且锚点数等于标题数。其余引导层文件不得出现 `ANCHOR_RE` 能匹配的行。
5. **规范性声明**：每份译本必须含逐字的引用块（language-structure §2），且英文原文不得含它。
6. **首页标题**：`.github/README.md` 第一行是锚点行，第二行是 `GUIDANCE_HOME_TITLE`。
7. **单一数据源**：译本中不得出现 `SINGLE_SOURCE_MARKERS` 中的任何一个。
8. 保留原有断言：`.github/README.md` 必须含 `CLEANUP_COMMAND`、`chefs-pick/SETUP.md`、`chefs-pick/GUIDE.md` 与 `## Feedback and contact`。
9. `chefs-pick/CHANGELOG.md` 至少有一个 `## [` 版本标题（原有断言保留）。
10. `chefs-pick/LICENSE` 第 3 行仍是 `Copyright (c) 2026 Chef's Pick OSS Starter contributors`。

### C12 选型清单（字面量改英文）
八个字段名、级别取值、六种证据类型、`Data verified:`、`## Excluded candidates`、表头首格 `Field` / `Module` / `Candidate` 全部换英文；只检查 `**Rationale**` 段落（删去对 `**入选理由**` 的检查）；`**Alternatives**`；规则为 `2` 时正文须含 `comparable adoption`。日期新鲜度逻辑不变。

### C13 / C22 清理与删除模拟
使用新的 `CLEANUP_COMMAND`。被删集合为 `.github/README.md`、`.github/README.zh-CN.md` 与 `.github/chefs-pick/` 整个目录。模拟删除后，剩余文件中不得残留指向这些路径的链接。

### C14 相对链接
逻辑不变，但必须覆盖两个新文件。语言入口、规范性声明与 §5 中指向英文原文带 `#锚点` 的链接都要能解析——带 `#` 的链接只校验文件存在，不校验锚点（锚点由 C11 单独保证）。

### C17 删除说明
`GUIDE.md` 的 `### Remove` 小节字面量改英文：`- Delete:`、`- Update:`、`- What you lose:`。

### C18 维护说明
除字面量改英文外，新增两项断言：`## Release gates` 一节必须出现 6 个有序列表项；全文必须含 `--update-digests`。

### C19 团队升级指引
字面量改英文，其余不变。

## 5. 新增的检查项

### C23 契约数字一致（标题 `Contract parity`）

- 左侧：`specs/001-chefs-pick-starter/contracts/guidance-layer.md` 中全部 `★ N (owner/repo)`。
- 右侧：`template/` 下全部 `.md` 中全部 `★ N (owner/repo)`。
- 对每个同时出现在两侧的 `owner/repo`，`N` 必须相等；不等则逐条报告 `owner/repo: contract N1 vs template N2`。
- 只出现在一侧的仓库不报错（契约会提到模板未收录的候选）。
- 契约文件不存在时记为 SKIP。
- **路径来源**：相对仓库根，不受 `--template-dir` 影响；仓库根取脚本所在目录的上一级。

### C24 译本新鲜度（标题 `Translation freshness`）

- 对每份译本：读取其来源标记行，取出 `source` 与 `digest`。
- 重新计算同目录下 `source` 文件完整字节的 sha256 前 16 位。
- 不等时：不带 `--release` 抛 `WarnCheck`，带 `--release` 返回问题列表（按 FAIL 计）。
- 缺少来源标记行、格式不符、或 `source` 指向的文件不存在：**一律按 FAIL**，不是 WARN。这些是结构问题，不是新鲜度问题。
- 没有任何译本时记为 SKIP。

## 6. `verify_sources.py` 的改动（FR-018）

- 写入目标增加 `specs/001-chefs-pick-starter/contracts/guidance-layer.md`（相对仓库根，不受 `--template-dir` 影响）。
- 刷新时，对该文件中的 `★ N (owner/repo)` 按与 `template/` 相同的规则替换 `N`。
- 该文件不存在时跳过并在报告中注明，不报错。
- 只读模式（不带 `--write`）同样把契约的差异列进报告。

## 7. 测试

| 文件 | 变化 |
|---|---|
| `tools/tests/test_checks_identity.py` | C11 用例整体重写：纯度正反例、语言入口缺失/错位/串到非译本文档、锚点序列不符、锚点与标题数不等、译本缺规范性声明、译本含单一数据源标记 |
| `tools/tests/test_checks_selection.py` | C12 全部字面量改英文；新增"规则 2 但正文缺 `comparable adoption`"反例 |
| `tools/tests/test_checks_links.py` | C13、C14、C17、C22 按新命令与新文件集合调整 |
| `tools/tests/test_checks_markers.py` | C08 表头改英文 |
| `tools/tests/test_checks_maintaining.py` | C18 新增"门禁只有 5 条"与"缺 `--update-digests`"两个反例 |
| `tools/tests/test_checks_upgrade.py` | C19 字面量改英文 |
| `tools/tests/test_checks_contract_parity.py` | **新建**：C23 的一致、不一致、单侧出现、契约缺失四种情形 |
| `tools/tests/test_checks_translation.py` | **新建**：C24 的一致（PASS）、摘要过期（WARN；`--release` 下 FAIL）、缺标记（FAIL）、格式错（FAIL）、无译本（SKIP）；以及 `--update-digests` 的就地改写与幂等 |
| `tools/tests/test_verify_sources.py` | 新增契约写入用例 |
| `tools/tests/test_real_template.py` | 对真实 `template/` 断言：8 个英文文件 `cjk_count == 0`（`README.zh-CN.md`、`SETUP.zh-CN.md` 除外）、两份译本 `longest_english_run < 6`、四个文件锚点序列正确、C23 与 C24 通过 |

所有新增测试必须使用 `tools/tests/helpers.py` 既有的临时模板夹具方式，不得依赖真实 `template/`（`test_real_template.py` 除外）。
