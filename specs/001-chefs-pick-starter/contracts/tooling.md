# 契约：维护工具

对应需求：FR-008、FR-010、FR-012、FR-013、FR-025 ~ FR-028、FR-033、FR-035、FR-039；SC-003 ~ SC-008、SC-010、SC-012；宪章发布门禁。决策依据：[research.md](../research.md) R19。

**通用要求**：
- 所有工具都放在开发工作区的 `tools/` 下，不进入 `template/`。
- 需要 Python 3.10+，只依赖标准库和 PyYAML。
- 路径一律用 `pathlib`，文本一律按 UTF-8 读写。
- 所有检查都忽略 macOS 生成的 `.DS_Store` 文件。模板自带的 `.gitignore` 已经排除了它。

## 1. `tools/check_template.py`

### 1.1 命令行

```text
python3 tools/check_template.py [--template-dir PATH] [--release] [--today YYYY-MM-DD] [--only C01,C05,...] [--files PATH,...]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--template-dir` | `<仓库根>/template`，其中仓库根为本脚本所在目录的上一级 | 要校验的模板目录 |
| `--release` | 关闭 | 开启发布门禁：C12 要求所有日期距今不超过 30 天 |
| `--today` | 当天日期 | 覆盖"今天"，供测试使用 |
| `--only` | 全部 | 只运行列出的检查，用逗号分隔 |
| `--files` | 全部 | 用逗号分隔的路径（相对 `template/`），限制逐文件检查（C03、C08、C09、C10、C11、C14、C21）的检查范围，便于并行任务单独验收自己的文件。带这个参数时，C08 仍然读取登记表来判断占位符是否已登记，但不做"实际出现的文件集合等于登记表第 3 列"这项比对 |

**缺失文件的处理**：除 C01 外，每项检查只检查已经存在的文件。如果某项检查依赖的文件全部不存在，该项记为 SKIP，并注明缺少哪个文件。缺失的文件只由 C01 报告。这样，在模板逐步完成的过程中，也可以按用户故事分批验收。

因此，只有 C01 会因为模板尚未完成而 FAIL。模板还在逐步搭建时，验收命令应当用 `--only` 排除 C01，等收尾阶段再做全量运行。C13 和 C22 依赖多个文件：根目录 `README.md` 不存在时，它们记为 SKIP；C13 还要求 `SETUP.md` 存在，否则同样记为 SKIP。

**退出码**：
- `0`：所选检查全部通过，允许有 SKIP；
- `1`：至少一项 FAIL；
- `2`：使用或环境错误，例如模板目录不存在、缺少 PyYAML（此时打印 `python3 -m pip install pyyaml`）、`--only` 中有未知编号。

**输出格式**：
- 每项检查占一行：`PASS C01 <标题>`、`FAIL C01 <标题>` 或 `SKIP C01 <标题>: <原因>`；
- FAIL 行下面逐条列出问题，每条以两个空格加 `- ` 开头；
- 最后一行：`Summary: <p> passed, <f> failed, <s> skipped`。

### 1.2 代码结构

- `@dataclass Context`：包含 `template_dir: Path`、`release: bool`、`today: datetime.date`、`files: set[str] | None`。`files` 为 `None` 表示不限制。
- 读取文件：文本检查用 `read_text(path)`；**C21 必须用 `Path.read_bytes()` 判断行尾和换行符**。`Path.read_text()` 会按通用换行模式把 CRLF 静默转成 LF，导致 CRLF 检测永远通过。
- 辅助函数 `selected(ctx, rel_path) -> bool`：逐文件检查用它判断某个文件是否在检查范围内。
- `class SkipCheck(Exception)`：检查函数抛出它时，该项记为 SKIP。
- 每个检查写成一个函数 `check_cNN(ctx) -> list[str]`，返回问题列表，空列表表示通过；所有检查登记在有序字典 `CHECKS = {"C01": ("<标题>", check_c01), ...}` 中。
- 公共常量和辅助函数：
  - `GUIDANCE_FILE = ".github/README.md"`，`GUIDANCE_DIR = ".github/chefs-pick"`；
  - `is_guidance(rel_path)`：判断文件是否属于起步引导层；
  - `iter_files(root)`：遍历目录，按路径排序，跳过 `.DS_Store`；
  - `project_files(ctx)`：返回引导层以外的所有文件；
  - `read_text(path)`；
  - `load_yaml(path)`：使用 `yaml.safe_load`。
- 常量表必须与契约一致：
  - `REQUIRED_FILES`、`OPTIONAL_FILES`：来自 [template-layout.md](./template-layout.md) §2；
  - `SOURCE_COMMENTS`：路径到来源注释逐字内容的映射，来自 [markers.md](./markers.md) §2.2；
  - `LEGACY_MARKERS`：来自 markers §1.3；
  - `REMOVAL_REFS`：来自 template-layout §6；
  - `FIELD_LABELS` 与级别取值：来自 [guidance-layer.md](./guidance-layer.md) §4.2。
- 正则表达式：
  - `PLACEHOLDER_RE = r"CHANGEME_[A-Z0-9_]+"`
  - `IDENTITY_RE = r"(?i)chef'?s[ -]?pick|主厨精选"`
  - `STAR_RE = r"★ ([\d,]+) \(([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\)"`
  - `CLEANUP_COMMAND = "git rm -r .github/README.md .github/chefs-pick"`
- 标记常量：`<!-- adoption-data:start -->`、`<!-- adoption-data:end -->`、`<!-- summary:start -->`、`<!-- summary:end -->`。

### 1.3 检查项

| 编号 | 标题 | 通过条件 |
|---|---|---|
| C01 | Layout | `REQUIRED_FILES` 中的文件全部存在；除 `REQUIRED_FILES` 和 `OPTIONAL_FILES` 外没有其他文件 |
| C02 | No development files | 任何路径中都不含 `.specify`、`.claude`、`specs`、`tools`、`.git`、`__pycache__`、`node_modules` 这些目录名，也没有 `*.pyc` 文件 |
| C03 | YAML parses | 所有 `*.yml` 和 `*.yaml` 文件都能用 `yaml.safe_load` 解析 |
| C04 | Issue forms | 满足 [project-files.md](./project-files.md) M07 所列的全部条件 |
| C05 | CI workflow | 满足 project-files M11 所列的全部条件。注意 PyYAML 会把 `on` 键读成 `True`，必须兼容 |
| C06 | Dependabot | `version == 2`；至少有一个更新项同时满足 `package-ecosystem == "github-actions"`、`directory == "/"`，且 `schedule.interval` 不为空 |
| C07 | Release notes | `changelog.categories` 与 project-files M09 中的三个分类完全一致（标题、标签、顺序都相同） |
| C08 | Placeholders | 见下方说明 |
| C09 | Source comments | `SOURCE_COMMENTS` 中每个文件的第一行都与登记的内容逐字相同；根目录 `LICENSE` 的第一行是 `MIT License` |
| C10 | Template identity isolation | 见下方说明 |
| C11 | Guidance layer | 见下方说明 |
| C12 | Selection list | 见下方说明 |
| C13 | Cleanup simulation | 见下方说明 |
| C14 | Relative links | 见下方说明 |
| C15 | License | 根目录 `LICENSE` 满足以下条件：第 1 行为 `MIT License`；第 3 行为 `Copyright (c) CHANGEME_YEAR CHANGEME_COPYRIGHT_HOLDER`；包含 `Permission is hereby granted, free of charge`；包含 `THE SOFTWARE IS PROVIDED "AS IS"`；不包含 `[year]` 或 `[fullname]` |
| C16 | Code of conduct | 满足 project-files M04 中 C16 所列的条件 |
| C17 | Removal notes | 见下方说明 |
| C18 | Maintenance guide | `MAINTAINING.md` 包含 guidance-layer §5 列出的 6 个二级标题（按英文部分匹配），其中含 `Action updates` |
| C19 | Team upgrade guide | `UPGRADE-TO-TEAM.md` 包含 guidance-layer §6 列出的 3 个二级标题（按英文部分匹配）。文件不存在时记为 SKIP，因为它是可选的 P4 内容 |
| C20 | Contributor documents | 见下方说明 |
| C21 | Text format | 见下方说明 |
| C22 | Removal simulation | 见下方说明 |

每项检查所属的阶段：C01 在收尾阶段做全量运行；C02、C03、C05、C06、C08、C09、C10、C11、C13、C14、C15、C17、C21、C22 属于基础阶段，供 US1 使用；C12 属于 US2；C04、C07、C16、C20 属于 US3；C18 属于 US4；C19 属于 US5。全部共 22 项。C23、C24 由功能 002 新增，见 specs/002-english-first-docs/contracts/tooling-delta.md；C25 ~ C27 由功能 003 新增，见 specs/003-workspace-self-compliance/contracts/tooling-delta-003.md。含后续功能新增的部分，检查项现共 27 项。

**C08 Placeholders**：
- 从 `SETUP.md` 的占位符表中解析登记表：表头见 [guidance-layer.md](./guidance-layer.md) §2；第 1 列取反引号中的占位符，第 3 列取所有反引号中的路径。
- 项目文件中出现的占位符都必须在登记表中。
- 对每个占位符，只看登记表第 3 列中已经存在的文件：这些文件与该占位符实际出现的文件必须完全一致。
- 项目文件中不得出现任何 `LEGACY_MARKERS`，匹配时区分大小写。
- 引导层中，只有 `SETUP.md` 可以出现 `CHANGEME_`。
- `SETUP.md` 不存在时，记为 SKIP。

**C10 Template identity isolation**（受 `--files` 限制）：
- 所有项目文件都不匹配 `IDENTITY_RE`。
- 所有项目文件都不含中文字符（Unicode 区间 U+4E00 至 U+9FFF）。这落实 FR-037 和宪章附加约束："生成仓库中的协作文件及其中的来源注释使用英文"。
- 根目录 `CHANGELOG.md` 中以 `## ` 开头的行恰好只有一行，内容为 `## [Unreleased]`。
- `.github/CODEOWNERS` 中没有"非空且不以 `#` 开头"的行。
- `.github/FUNDING.yml` 解析后是一个映射，且所有值都为 `None`。

**C11 Guidance layer**（只检查已经存在的引导层文件，受 `--files` 限制）：
- `.github/README.md` 的第一行标题逐字为 `# Chef's Pick OSS Starter · 主厨精选开源仓库起步模板`，并且包含 `CLEANUP_COMMAND`、`chefs-pick/SETUP.md`、`chefs-pick/GUIDE.md` 三个字符串，以及标题 `## 反馈与联系 / Feedback and contact`。
- 引导层中所有 `.md` 文件的所有标题行（代码块内的除外）都同时含有中文字符（Unicode 区间 U+4E00 至 U+9FFF）和英文字母。例外：匹配 `^#{1,6} \[(Unreleased|[0-9]+\.[0-9]+\.[0-9]+)\]` 的版本标题不受此限，见 guidance-layer §0。
- `SETUP.md` 包含 `S01` 到 `S09`，并且包含 guidance-layer §2 规定的占位符表表头。
- `GUIDE.md` 包含以 `## M01` 到 `## M16` 开头的标题，以及 guidance-layer §3 列出的 6 个附加标题（按英文部分匹配）。
- 模板自身的 `CHANGELOG.md` 至少包含一个以 `## [` 开头的标题。
- 模板自身的 `LICENSE` 第 3 行逐字为 `Copyright (c) 2026 Chef's Pick OSS Starter contributors`。

**C12 Selection list**（`SOURCES.md` 不存在，或首页摘要表的两个标记之间还没有数据行时，整项记为 SKIP。后者对应 US2 只完成了一半的中间状态）：
- `.github/README.md` 包含 `chefs-pick/SOURCES.md`。
- `SOURCES.md` 中有一行符合 `数据核实日期 / Data verified: YYYY-MM-DD`。
- `M01` 到 `M16` 每个模块都有一节，其字段表包含 8 个 `FIELD_LABELS`，级别取值合法，"核实日期"一格是合法日期。
- 每个模块一节中都有非空的 `**入选理由**` 段落、非空的 `**Rationale**` 段落，以及 `**备选方案 / Alternatives**` 下至少一个列表项（SC-003）。
- 每个模块的"认可度证据"格中，至少出现一个 data-model 规定的双语证据类型标签，例如 `精确 Star 数 / Exact stars`、`平台官方功能 / Official platform feature`。
- 认可度数据表能在两个标记之间解析出来，且每行有 7 列。
- 在 `.github/README.md`、`SOURCES.md`、`UPGRADE-TO-TEAM.md` 中，每个匹配 `STAR_RE` 的位置，其仓库都必须在数据表中，且数字与 Stars 列相同。
- 首页摘要表在两个标记之间恰好有 16 行数据（不含表头和分隔行），每行第 1 格依次以 `M01` 到 `M16` 开头。
- **受日期新鲜度约束的只有以下四处**：`数据核实日期 / Data verified:` 那一行；各模块字段表的"核实日期 / Verified"格；认可度数据表的 `Verified` 列；首页摘要表的"核实日期 / Verified"列。这四处距 `today` 不超过 183 天，开启 `--release` 时不超过 30 天。认可度数据表的 `Last commit` 列记录上游提交日期，本来就可能很旧，**不参与**这项检查。
- 每个模块"认可度证据"格中第一个 `★` 对应的仓库，在数据表中不得标为已归档（Archived 为 `yes`）。
- `SOURCES.md` 中有一节标题为 `## 排除的候选 / Excluded candidates`，其表格至少 8 行数据，每行的 3 格都非空（宪章原则 I：排除的知名候选必须记录理由；FR-030）。
- "取舍规则 / Rule"一格去掉空白后**恰好等于** `2` 的模块，其 `**入选理由**` 段落必须出现"认可度相当"字样（宪章原则 II；data-model 规定 `1 + 2` 不主张认可度相当，因此不受这条约束，不得把 `1 + 2` 一并判失败）。

**C13 Cleanup simulation**：
- 把模板目录复制到临时目录，删除 `GUIDANCE_FILE` 和 `GUIDANCE_DIR`，然后检查以下各项：
  - 所有剩余文件都不含 `chefs-pick/` 或 `.github/README.md` 字样；
  - 所有剩余文件都不匹配 `IDENTITY_RE`；
  - 占位符集合与登记表相同（登记表在删除之前解析）；
  - 根目录 `README.md` 存在；
  - 在副本上运行 C14 的逻辑，没有问题。
- 结束时删除临时目录。

**C14 Relative links**：
- 检查所有 `.md` 文件中的 `[文字](目标)` 和 `href="目标"`。
- 跳过以 `http://`、`https://`、`mailto:` 或 `#` 开头的目标；其余目标去掉 `#...` 和 `?...` 部分后，按所在文件的目录解析，结果必须是模板目录内一个存在的文件或目录。
- 项目文件中的链接不得指向引导层。

**C17 Removal notes**：
- 对 `REMOVAL_REFS` 中的每个模块，以及自动发现的引用都做检查。自动发现的方法：取该模块每个文件的文件名，在其他项目文件中查找，找到的文件都算引用方。
- 每个引用方的文件名都必须出现在 `GUIDE.md` 中该模块那一节里，即从 `## Mxx` 到下一个 `## ` 之间的文本。
- M01、M02、M03 不参与这项检查。

**C22 Removal simulation**（根目录 `README.md` 不存在时记为 SKIP）：
- 对 M04 ~ M16 中每个有文件的模块（M10 没有文件，跳过）逐一模拟：把模板目录复制到临时目录，删除该模块的全部文件，然后在副本上确认：
  - 所有 `*.yml`、`*.yaml` 仍能解析（等同 C03）；
  - `ci.yml` 若仍存在，仍满足 C05；`dependabot.yml` 若仍存在，仍满足 C06；
  - 其余文件中的相对链接仍然有效（等同 C14）。指向被删文件的链接不算问题，它们由 C17 保证已在 GUIDE 中写明修改方法；
  - 没有任何 YAML 配置文件引用被删掉的文件名。
- 每轮结束都要删除临时目录。这项检查落实 SC-007："逐一删除每个推荐或可选模块后，其余模块照常工作、自动检查仍然通过"。

**C20 Contributor documents**（逐个检查已经存在的文件）：
- `SECURITY.md` 同时包含以下内容：
  - 标题 `## Supported Versions`、`## Reporting a Vulnerability`；
  - 加粗句 `**Please do not report security vulnerabilities through public issues, discussions, or pull requests.**`；
  - `security/advisories/new`；
  - `CHANGEME_SECURITY_EMAIL`。
- `CONTRIBUTING.md` 满足以下条件：
  - 依次包含标题 `# Contributing`、`## Code of Conduct`、`## Ways to contribute`、`## Reporting bugs`、`## Suggesting features`、`## Reporting security issues`、`## Submitting pull requests`、`## Development setup`、`## Questions`；
  - 链接到 `CODE_OF_CONDUCT.md`、`SECURITY.md`、`CHANGELOG.md`、`README.md#getting-started`；
  - 不含 `CHANGEME_`。
- `.github/PULL_REQUEST_TEMPLATE.md` 满足以下条件：
  - 依次包含标题 `## Description`、`## Related issue`、`## Checklist`；
  - 包含 `Closes #`；
  - 恰好有 3 个 `- [ ] ` 清单项。
- `README.md` 包含 `issues/new?template=bug_report.yml` 和 `issues/new?template=feature_request.yml`。

**C21 Text format**（逐文件检查，适用于 `template/` 下的所有文件；必须按字节读取）：
- 能按 UTF-8 解码。
- 文件末尾恰好是一个 `\n`。
- 没有以空格或制表符结尾的行，即不匹配 `[ \t]$`。
- 不含 `\r\n`。注意：`.gitignore` 的上游 macOS 规则中，`Icon[\r]` 和 `.HFS+ Private Directory Data[\r]` 两行的方括号里各有一个字面的 `\r`。它们不是 CRLF 换行，属于合法内容，不应被当作问题报告。

## 2. `tools/verify_sources.py`

### 2.1 命令行

```text
python3 tools/verify_sources.py [--template-dir PATH] [--write] [--today YYYY-MM-DD]
```

- **读取**：从 `<template>/.github/chefs-pick/SOURCES.md` 中两个 `adoption-data` 标记之间的表格读出所有仓库。
- **查询**：对每个仓库调用 `fetch_repo(slug)`。它先执行 `gh api repos/<slug>` 取 `full_name`、`stargazers_count`、`forks_count`、`archived`、`license.spdx_id`、`default_branch`，再执行 `gh api repos/<slug>/commits/<default_branch>` 取默认分支最近一次提交的日期，返回 `{"full_name", "stars", "forks", "last_commit"（YYYY-MM-DD）, "license"（SPDX 标识；值为 null 或 NOASSERTION 时写 "unknown"）, "archived"}`。不要使用 `pushed_at`：它会因任何分支的推送而更新，会漏掉已停更的上游（见 research §5）。
- **报告**：每个仓库输出一行，内容包括仓库名、`stars 旧值→新值`、`forks 旧值→新值`、默认分支最近提交日期、许可证、是否归档，以及以下标志：
  - `STALE`：默认分支最近提交距 `today` 超过 365 天；
  - `ARCHIVED`：仓库已归档；
  - `RENAMED→<full_name>`：接口返回的 `full_name` 与表中的仓库名不同（忽略大小写比较）。
- **提醒**：报告最后固定输出一行，提醒手动复核非仓库证据："Also re-check non-repository evidence manually: official platform features and the Contributor Covenant adopters list."
- **`--write`**：只有在所有仓库都查询成功时才写入，依次完成：
  1. 重写数据表，行序不变；Stars 和 Forks 带千分位逗号；`Last commit` 写默认分支最近提交日期；Archived 写 `yes` 或 `no`；Verified 写 `today`。
  2. 在 `.github/README.md`、`SOURCES.md`，以及存在时的 `UPGRADE-TO-TEAM.md` 中，把每一处 `★ N (slug)` 的 N 更新为新值。
  3. 把 `数据核实日期 / Data verified:` 后面的日期改成 `today`。
  4. 把 `SOURCES.md` 中所有 `| 核实日期 / Verified | <日期> |` 单元格，以及首页摘要表"核实日期"列的日期都改成 `today`。
- **退出码**：
  - `0`：成功；
  - `1`：至少一个仓库查询失败，此时不写入；
  - `2`：`gh_ready()` 返回 `False`。
- **函数划分**：`gh_ready() -> bool`（先用 `shutil.which("gh")` 判断是否安装，再执行 `gh auth status` 判断是否已登录）、`parse_adoption_table(text)`、`render_adoption_table(rows)`、`fetch_repo(slug)`、`apply_updates(files: dict[str, str], results, today) -> dict[str, str]`、`main(argv=None) -> int`。测试会 mock `fetch_repo` 和 `gh_ready`，所以这两个函数里不要夹带其他逻辑。

## 3. 测试（`python3 -m unittest discover -s tools/tests`）

每个测试文件开头都要执行 `sys.path.insert(0, str(Path(__file__).resolve().parents[1]))`，以便导入 `tools/` 下的模块。

| 文件 | 覆盖内容 |
|---|---|
| `tools/tests/helpers.py` | 共享的辅助函数：`write_tree(root, files: dict[str, str])` 在临时目录中写入文件；`make_ctx(root, **kw)` 构造 `Context`；`run_one(check_id, ctx)` 返回 `(status, problems)`。本文件不含测试用例 |
| `tools/tests/test_checks_layout.py` | C01、C02、C03、C21：每项至少一个通过用例和一个失败用例。每个用例都在临时目录中只构造与该检查相关的最少文件。C21 必须包含四个用例：CRLF 失败（写入字节 `b"a\r\nb\r\n"`）、方括号中的字面 CR 不报错、行尾空格失败、文件末尾缺换行失败 |
| `tools/tests/test_checks_automation.py` | C05、C06：同上。C05 的通过用例使用 project-files M11 的逐字内容 |
| `tools/tests/test_checks_markers.py` | C08、C09：同上，并覆盖 `--files` 参数下的行为 |
| `tools/tests/test_checks_identity.py` | C10、C11：同上。C10 另加一个失败用例：某个项目文件中出现中文字符 |
| `tools/tests/test_checks_links.py` | C13、C14、C15、C17、C22：同上。C22 的失败用例：删除 `CODE_OF_CONDUCT.md` 后，某个 YAML 配置文件仍然引用它 |
| `tools/tests/test_checks_selection.py` | C12：通过用例；以及以下失败用例：Star 数不一致、缺少字段、选定来源已归档、日期超过 183 天、开启 `--release` 时日期超过 30 天、摘要表不足 16 行、缺少"排除的候选"一节或其表格不足 8 行、取舍规则恰好为 `2` 的模块入选理由中没有"认可度相当"；以及一个 `1 + 2` 且不写"认可度相当"的通过用例 |
| `tools/tests/test_checks_contributor.py` | C04、C07、C16、C20：每项至少一个通过用例和一个失败用例 |
| `tools/tests/test_checks_maintaining.py` | C18：通过用例和失败用例 |
| `tools/tests/test_checks_upgrade.py` | C19：通过、失败，以及文件不存在时记为 SKIP |
| `tools/tests/test_real_template.py` | 对真实的 `template/` 运行全部检查，要求没有 FAIL；`template/` 不完整时用 `skipUnless` 跳过，条件为 C01 通过 |
| `tools/tests/test_verify_sources.py` | 数据表解析后再渲染与原文一致；`apply_updates` 能正确替换 Star 数、`Last commit` 和日期；`STALE`、`ARCHIVED`、`RENAMED` 标志正确；`gh_ready()` 被 mock 为 `False` 时退出码为 2；任一仓库查询失败时不写入。测试全程不访问网络：mock `fetch_repo` 和 `gh_ready` |
| `tools/tests/test_ci_pin_check.py` | 从 `template/.github/workflows/ci.yml` 中取出名为 "Check that actions are pinned to full commit SHAs" 的步骤的 `run` 脚本（文件不存在时跳过），在两个临时仓库中用 `bash` 执行：`fixtures/pin_good.yml` 期望退出码为 0；`fixtures/pin_bad.yml` 期望退出码为 1，且输出恰好列出 3 条未固定的引用 |
| `tools/tests/fixtures/pin_good.yml`、`pin_bad.yml` | 内容与 plan 阶段实测用的样例一致，见 [quickstart.md](../quickstart.md) 附录 A |

## 4. 开发工作区的 `.gitignore`

位于开发工作区根目录，不在 `template/` 中，逐字内容：

```text
__pycache__/
*.pyc
.DS_Store
```
