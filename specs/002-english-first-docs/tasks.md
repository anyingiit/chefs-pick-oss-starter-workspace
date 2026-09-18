---

description: "Task list template for feature implementation"
---

# Tasks: 英文为主、中文另起一份的文档语言结构

**Input**: Design documents from `/specs/002-english-first-docs/`

**Prerequisites**: [plan.md](./plan.md)、[spec.md](./spec.md)、[research.md](./research.md)、[data-model.md](./data-model.md)、[contracts/](./contracts/)

**Tests**: 本功能**要求测试**。规格 FR-013 ~ FR-015 把校验本身当作交付物，`tools/tests/` 下的用例是它的验收手段，因此测试任务是必须的，不是可选的。

**Organization**: 任务按用户故事分组，每组可独立实现与验收。

## Format: `[ID] [P?] [Story] Description`

- **[P]**：可并行（不同文件、无未完成依赖）
- **[Story]**：所属用户故事（US1 ~ US4）
- 每个任务都写明完整文件路径

## 执行约定（每个任务都适用）

本清单面向 **Sonnet 级子代理**逐个执行。因此：

1. **一个任务只改一个文件**。跨文件的改动已拆开。
2. **没有判断题**。所有形态决策已在 [research.md](./research.md) 定死，所有逐字内容已在 [contracts/](./contracts/) 写明。任务里出现的固定数据（锚点 id、语言入口串、12 个 Star 数）已就地给出，不需要去别处查。
3. **每个任务自带验收命令**，跑通才算完成。
4. **遇到契约与现状不符时停下来报告**，不得自行发挥。尤其是：`chefs-pick/LICENSE` 的 MIT 正文一个字符都不许改；认可度数字不许凭记忆填写；现存英文句子不许"顺手润色"（唯一例外是 T025 的门禁补全，契约已写明）。
5. **改造期间 `check_template.py` 会红**，这是预期的。用 `--only`/`--files` 单项验收，全量绿灯在 Phase 7 收口。

---

## Phase 1: Setup（基线）

**Purpose**: 记下改造前的真实状态，作为后续回归的对照

- [X] T001 在仓库根运行 `python3 -m unittest discover -s tools/tests 2>&1 | tail -3`、`python3 tools/check_template.py | tail -1` 与 `git ls-files template/ | wc -l`，把三个结果写入 `specs/002-english-first-docs/baseline.md`。期望值分别为 `OK`（199 个用例）、`Summary: 22 passed, 0 failed, 0 skipped`、`26`。任一不符则停下来报告，不要开始改造。

---

## Phase 2: Foundational（阻塞性前置）

**Purpose**: 校验工具的框架、常量与检查项。所有用户故事的验收都依赖它。

**⚠️ CRITICAL**: 本阶段完成前不要动 `template/` 下任何文件。

**注意**：T002 ~ T009 都改 `tools/check_template.py` 同一个文件，必须**串行**执行，不得并行。

- [X] T002 在 `tools/check_template.py` 中新增 `WARN` 结果状态，按 [contracts/tooling-delta.md](./contracts/tooling-delta.md) §1.1：新增 `class WarnCheck(Exception)`（`args[0]` 为问题列表）；输出行格式 `WARN C24 <标题>`，问题逐条以两个空格加 `- ` 开头；汇总行改为 `Summary: <p> passed, <f> failed, <w> warned, <s> skipped`；WARN 不影响退出码，但带 `--release` 时会 WARN 的检查改按 FAIL 计。验收：`python3 tools/check_template.py | tail -1` 输出含 `warned`。
- [X] T003 在 `tools/check_template.py` 中新增 `--update-digests` 命令行参数，按 tooling-delta §1.2：对每份译本重新计算其英文原文完整字节的 sha256 前 16 位，就地改写来源标记行，只改那一行；输出每个被更新的文件与新旧摘要，无变化时输出 `No digest needed updating.`；带该参数时不运行任何检查，退出码 0 或 2。此时还没有译本，应输出 `No digest needed updating.`。验收：`python3 tools/check_template.py --update-digests` 退出码为 0。
- [X] T004 在 `tools/check_template.py` 中把全部含中文的字面量常量改为英文，并新增常量，按 tooling-delta §2。逐项对照：`GUIDANCE_HOME_TITLE` → `# Chef's Pick OSS Starter`；`CLEANUP_COMMAND` → `git rm -r .github/README.md .github/README.zh-CN.md .github/chefs-pick`；`PLACEHOLDER_TABLE_HEADER` → `| Placeholder | Meaning | Files | Example |`；`FIELD_LABELS` → `Files`/`Level`/`Pick`/`Version`/`Upstream license`/`Evidence`/`Rule`/`Verified`；级别取值 → `Required`/`Recommended`/`Optional`/`Optional (recommendation only)`；证据类型 → `Exact stars`/`Rounded stars`/`Estimated users`/`Official platform feature`/`De facto standard`/`Not available`。**`IDENTITY_RE` 保持不变**（它检测作者身份泄漏，`主厨精选` 仍须识别）。同时新增 `TRANSLATED_DOCS`、`SELECTOR_LINES`、`ANCHOR_RE`、`DIGEST_RE`、`ANCHOR_SEQUENCES`、`SINGLE_SOURCE_MARKERS` 六个常量，取值逐字照抄 tooling-delta §2 的代码块。验收：`python3 -c "import ast,sys; ast.parse(open('tools/check_template.py').read())"` 无输出。
- [X] T005 在 `tools/check_template.py` 中新增三个纯度判定辅助函数与译本发现逻辑，按 tooling-delta §1.3 与 §3：`strip_for_purity(text, selector_line)` 依次删除围栏代码块（含围栏行）、HTML 注释、行内代码、Markdown 链接的 `(目标)` 部分、裸 URL、与 `selector_line` 逐字相同的行；`cjk_count(text)` 数 U+4E00–U+9FFF；`longest_english_run(text)` 返回最长连续英文词个数，词为 `[A-Za-z][A-Za-z'’-]*`，词间只隔空格或半角标点算连续，出现中文即中断。译本发现：引导层内文件名匹配 `^(?P<id>[A-Za-z-]+)\.(?P<lang>[a-z]{2}(-[A-Z]{2})?)\.md$` 且同目录存在 `<id>.md` 者即为译本。验收：`python3 -c "import sys; sys.path.insert(0,'tools'); import check_template as c; print(c.cjk_count('中a文'), c.longest_english_run('one two three'))"` 输出 `2 3`。
- [ ] T006 在 `tools/check_template.py` 中整体重写 `check_c11`，标题改为 `Language structure`，按 tooling-delta §4 的 C11 条目实现全部 10 项断言（纯度、语言入口存在与位置、非译本文档不得有入口、互达、锚点有序序列、锚点数等于标题数、非锚点文档不得有锚点行、译本规范性声明、英文原文不得有声明、首页首行锚点次行标题、译本不得含 `SINGLE_SOURCE_MARKERS`、保留原有 `CLEANUP_COMMAND`/`chefs-pick/SETUP.md`/`chefs-pick/GUIDE.md`/`## Feedback and contact` 断言、`chefs-pick/CHANGELOG.md` 含 `## [`、`chefs-pick/LICENSE` 第 3 行为 `Copyright (c) 2026 Chef's Pick OSS Starter contributors`）。此时对真实模板必然 FAIL，属预期。验收：`python3 tools/check_template.py --only C11 | head -1` 输出 `FAIL C11 Language structure`。
- [ ] T007 在 `tools/check_template.py` 中把 `check_c12` 的全部字面量改为英文，按 tooling-delta §4 的 C12 条目：八个字段名、级别取值、六种证据类型、`Data verified:`、`## Excluded candidates`、表头首格 `Field`/`Module`/`Candidate`；删去对 `**入选理由**` 的检查只保留 `**Rationale**`；`**备选方案 / Alternatives**` → `**Alternatives**`；规则为 `2` 时正文须含 `comparable adoption`。日期新鲜度逻辑不动。验收：`python3 tools/check_template.py --only C12 | head -1` 输出 `FAIL C12`（模板尚未改造，属预期）。
- [ ] T008 在 `tools/check_template.py` 中调整 C08、C13、C14、C17、C18、C19、C22 七项，按 tooling-delta §4 对应条目：C08 换英文表头；C13/C22 使用新 `CLEANUP_COMMAND`，被删集合含 `.github/README.md`、`.github/README.zh-CN.md` 与 `.github/chefs-pick/` 整个目录；C14 覆盖两个新文件，带 `#` 的链接只校验文件存在不校验锚点；C17 字面量改 `- Delete:`/`- Update:`/`- What you lose:`；C18 新增两项断言（`## Release gates` 一节须有 6 个有序列表项；全文须含 `--update-digests`）；C19 字面量改英文。验收：`python3 tools/check_template.py --only C08,C13,C14,C17,C18,C19,C22 | tail -1` 能正常输出汇总行（不因异常中断）。
- [ ] T009 在 `tools/check_template.py` 中新增 `check_c23`（标题 `Contract parity`）与 `check_c24`（标题 `Translation freshness`），并登记进 `CHECKS`，按 tooling-delta §5。C23：比对 `specs/001-chefs-pick-starter/contracts/guidance-layer.md` 与 `template/` 下全部 `.md` 中的 `★ N (owner/repo)`，同一仓库的 `N` 必须相等，不等则报 `owner/repo: contract N1 vs template N2`；只出现在一侧的不报错；契约文件不存在记 SKIP；路径相对仓库根（脚本所在目录的上一级），不受 `--template-dir` 影响。C24：对每份译本读取来源标记，重算英文原文摘要，不等时不带 `--release` 抛 `WarnCheck`、带 `--release` 返回问题列表；缺标记、格式不符、`source` 文件不存在一律 FAIL；无译本记 SKIP。验收：`python3 tools/check_template.py --only C23 | head -1` 输出 `FAIL C23 Contract parity`（12 处漂移尚未修正，属预期）。
- [ ] T010 [P] 重写 `tools/tests/test_checks_identity.py` 中的 C11 用例，按 tooling-delta §7：覆盖英文版含中文（FAIL）、中文版含 6 个连续英文词（FAIL）、语言入口缺失（FAIL）、入口位置错（FAIL）、非译本文档出现入口（FAIL）、锚点序列与常量不符（FAIL）、锚点数不等于标题数（FAIL）、译本缺规范性声明（FAIL）、译本含 `| Placeholder | Meaning | Files | Example |`（FAIL）、全部合规（PASS）。必须使用 `tools/tests/helpers.py` 既有的临时模板夹具，不得依赖真实 `template/`。**锚点序列不符的那个用例还必须断言报文内容**：报文须同时含出问题的译本文件名与具体的锚点 id（SC-013 要求"100% 能指名是哪一份译本、哪一个章节锚点"，只断言 FAIL 不够）。验收：`python3 -m unittest tools.tests.test_checks_identity -v 2>&1 | tail -3` 输出 `OK`。
- [ ] T011 [P] 更新 `tools/tests/test_checks_selection.py`，把 C12 用例的全部双语字面量改为 T007 采用的英文字面量，并新增反例"规则为 2 但 `**Rationale**` 段落不含 `comparable adoption`"（FAIL）。验收：`python3 -m unittest tools.tests.test_checks_selection 2>&1 | tail -3` 输出 `OK`。
- [ ] T012 [P] 更新 `tools/tests/test_checks_links.py`，按 T008 的新清理命令与新文件集合调整 C13、C14、C17、C22 的夹具与断言；新增用例：清理后仍有文件链接到 `.github/README.zh-CN.md`（FAIL）。验收：`python3 -m unittest tools.tests.test_checks_links 2>&1 | tail -3` 输出 `OK`。
- [ ] T013 [P] 更新 `tools/tests/test_checks_markers.py`，把 C08 用例的登记表表头改为 `| Placeholder | Meaning | Files | Example |`。验收：`python3 -m unittest tools.tests.test_checks_markers 2>&1 | tail -3` 输出 `OK`。
- [ ] T014 [P] 更新 `tools/tests/test_checks_maintaining.py`，把 C18 用例改英文字面量，并新增两个反例：`## Release gates` 只有 5 个有序列表项（FAIL）、全文不含 `--update-digests`（FAIL）。验收：`python3 -m unittest tools.tests.test_checks_maintaining 2>&1 | tail -3` 输出 `OK`。
- [ ] T015 [P] 更新 `tools/tests/test_checks_upgrade.py`，把 C19 用例的字面量改为英文。验收：`python3 -m unittest tools.tests.test_checks_upgrade 2>&1 | tail -3` 输出 `OK`。
- [ ] T016 [P] 新建 `tools/tests/test_checks_contract_parity.py`，覆盖 C23 的四种情形：两侧数字一致（PASS）、某仓库不一致（FAIL 且报文含 `contract` 与 `template` 两个值）、某仓库只出现在一侧（PASS）、契约文件不存在（SKIP）。用临时目录构造契约文件与模板，不依赖真实文件。验收：`python3 -m unittest tools.tests.test_checks_contract_parity 2>&1 | tail -3` 输出 `OK`。
- [ ] T017 [P] 新建 `tools/tests/test_checks_translation.py`，覆盖 C24 与 `--update-digests`：摘要一致（PASS）、摘要过期且不带 `--release`（WARN，退出码 0）、摘要过期且带 `--release`（FAIL，退出码 1）、缺来源标记行（FAIL）、来源标记格式错（FAIL）、`source` 指向的文件不存在（FAIL）、无译本（SKIP）；`--update-digests` 的就地改写正确且再次运行输出 `No digest needed updating.`（幂等）。验收：`python3 -m unittest tools.tests.test_checks_translation 2>&1 | tail -3` 输出 `OK`。
- [X] T018 在 `tools/verify_sources.py` 中把写入目标增加 `specs/001-chefs-pick-starter/contracts/guidance-layer.md`（相对仓库根，不受 `--template-dir` 影响），按 tooling-delta §6：刷新时用与 `template/` 相同的规则替换其中的 `★ N (owner/repo)`；文件不存在时跳过并在报告中注明，不报错；只读模式也把契约的差异列进报告。验收：`python3 -c "import ast; ast.parse(open('tools/verify_sources.py').read())"` 无输出，且 `grep -c 'guidance-layer' tools/verify_sources.py` 大于 0。
- [ ] T019 [P] 在 `tools/tests/test_verify_sources.py` 中新增契约写入用例：构造一个含 `★ 1,000 (a/b)` 的临时契约文件与对应模板，运行写入后契约中的值被更新；契约文件不存在时不抛异常。验收：`python3 -m unittest tools.tests.test_verify_sources 2>&1 | tail -3` 输出 `OK`。
- [X] T020 在 `specs/001-chefs-pick-starter/contracts/guidance-layer.md` 中修正 12 处认可度数字，以 `template/` 为准（research R7）。逐项替换：`8,882`→`8,884`（actions/checkout）、`12,080`→`12,082`（actions/starter-workflows）、`12,405`→`12,408`（changesets/changesets）、`5,772`→`5,773`（dependabot/dependabot-core）、`4,201`→`4,202`（github/choosealicense.com）、`175,810`→`175,816`（github/gitignore）、`15,684`→`15,685`（github/opensource.guide）、`7,505`→`7,509`（googleapis/release-please）、`22,523`→`22,527`（renovatebot/renovate）、`4,234`→`4,235`（rhysd/actionlint）、`7,852`→`7,853`（semver/semver）、`10,597`→`10,598`（super-linter/super-linter）。只改这 12 个数字，文件其余部分一律不动。验收：`python3 tools/check_template.py --only C23 | head -1` 输出 `PASS C23 Contract parity`。

**Checkpoint**：此时 `python3 -m unittest discover -s tools/tests` 应全绿，`--only C23` 通过，C11/C12 对真实模板仍红（模板尚未改造）。

---

## Phase 3: User Story 1 - 英文读者读到一份纯英文的模板首页 (Priority: P1) 🎯 MVP

**Goal**: 8 份引导层文档全部变成纯英文，首页带语言入口与锚点。

**Independent Test**: `.github/README.md` 除语言入口行外中文字符数为 0，且 12 个章节锚点齐备。整项 C11 要到两份译本建好（T030）之后才会绿，因为语言入口的互达断言依赖译本文件存在。

**通则**（每个任务都适用，详见 [contracts/guidance-layer-en.md](./contracts/guidance-layer-en.md) §0）：标题取 ` / ` 之后的英文部分；表头逐格取英文；行内并排只留英文并删去 ` / `；成段并排删中文段留英文段；代码块、命令、路径、URL、Star 数、日期一律不动；**不得改写任何现存英文句子**。

- [X] T021 [US1] 把 `template/.github/README.md` 改为纯英文，按 guidance-layer-en §1 与 [contracts/language-structure.md](./contracts/language-structure.md) §0 §1 §3 §6。H1 改为 `# Chef's Pick OSS Starter`；在每个标题上方紧贴加锚点行，12 个锚点按顺序为 `chefs-pick-oss-starter`、`what-you-get`、`required`、`recommended`、`optional`、`the-picks-at-a-glance`、`how-we-pick`、`quick-start`、`good-to-know`、`clean-up-when-done`、`feedback-and-contact`、`license`；H1 下方空一行后加语言入口 `**English** · [简体中文](README.zh-CN.md)`；摘要表表头改为 `| Module | Pick | Adoption | Verified |`，16 行模块名去掉中文（如 `M01 项目说明 / README` → `M01 README`），`<!-- summary:start -->`/`<!-- summary:end -->` 标记与日期列不动；清理命令代码块改为 `git rm -r .github/README.md .github/README.zh-CN.md .github/chefs-pick`。验收（此时 `README.zh-CN.md` 尚不存在，语言入口的互达断言必然失败，**不要**用整项 C11 验收）：`python3 -c "import re;t=open('template/.github/README.md',encoding='utf-8').read();b=''.join(l for l in t.splitlines(True) if '简体中文' not in l);print('CJK=%d anchors=%d'%(sum(1 for c in b if '\u4e00'<=c<='\u9fff'),len(re.findall('^<!-- anchor: ',t,re.M))))"` 输出 `CJK=0 anchors=12`。
- [X] T022 [P] [US1] 把 `template/.github/chefs-pick/SETUP.md` 改为纯英文，按 guidance-layer-en §3 与 language-structure §0 §1 §3。H1 改为 `# Setup checklist`；3 个锚点按顺序为 `setup-checklist`、`placeholders`、`steps`；H1 下方加语言入口 `**English** · [简体中文](SETUP.zh-CN.md)`；登记表表头改为 `| Placeholder | Meaning | Files | Example |`，9 行的含义列取英文；步骤表表头改为 `| ID | Kind | Step | How to verify |`，`必做 / Required`→`Required`、`选做 / Optional`→`Optional`，S01 ~ S09 取英文部分；两条 `git grep` 命令一字不动。验收（同 T021，此时 `SETUP.zh-CN.md` 尚不存在）：`python3 -c "import re;t=open('template/.github/chefs-pick/SETUP.md',encoding='utf-8').read();b=''.join(l for l in t.splitlines(True) if '简体中文' not in l);print('CJK=%d anchors=%d'%(sum(1 for c in b if '\u4e00'<=c<='\u9fff'),len(re.findall('^<!-- anchor: ',t,re.M))))"` 输出 `CJK=0 anchors=3`。
- [X] T023 [P] [US1] 把 `template/.github/chefs-pick/GUIDE.md` 改为纯英文，按 guidance-layer-en §5。16 个模块标题如 `## M01 项目说明 / README` → `## M01 README`；`文件 / Files:`→`Files:`、`级别 / Level:`→`Level:`、`必需 / Required`→`Required`；小节标题 `### 为什么需要 / Why`→`### Why`、`### 如何定制 / Customize`→`### Customize`、`### 如何删除 / Remove`→`### Remove`；`### Remove` 下三条改为 `- Delete:`、`- Update:`、`- What you lose:`，删中文正文保留其后已有英文段落，若英文段落遗漏了中文列出的引用方则补齐；五个附录标题取英文部分；正文内形如 `#更换许可证--changing-the-license` 的锚点链接同步改为 `#changing-the-license` 等纯英文形式。**本任务不动 `## 中文译本 / Chinese translations` 一节**，它由 T035 处理。不加章节锚点，不加语言入口。验收：`python3 tools/check_template.py --only C14,C17 | tail -1` 汇总行无 FAIL。
- [X] T024 [P] [US1] 把 `template/.github/chefs-pick/SOURCES.md` 改为纯英文，按 guidance-layer-en §8。H1→`# Selection list`；`数据核实日期 / Data verified:`→`Data verified:`；`## 选型规则 / Selection rules`→`## Selection rules`，六种证据类型只留 `Exact stars`/`Rounded stars`/`Estimated users`/`Official platform feature`/`De facto standard`/`Not available`；16 个模块的字段表表头→`| Field | Value |`，八个字段名→`Files`/`Level`/`Pick`/`Version`/`Upstream license`/`Evidence`/`Rule`/`Verified`，级别取值→`Required`/`Recommended`/`Optional`/`Optional (recommendation only)`；删 `**入选理由**` 中文段保留 `**Rationale**` 英文段；`**备选方案 / Alternatives**`→`**Alternatives**` 且条目只留英文；M12 的 `**Rationale**` 必须含 `comparable adoption`；`## 排除的候选 / Excluded candidates`→`## Excluded candidates`，表头→`| Candidate | Adoption | Reason |`，9 行只留英文；`## 认可度数据 / Adoption data`→`## Adoption data`，`<!-- adoption-data:start -->` 与 `<!-- adoption-data:end -->` 之间的 36 行表格**一字不动**；`## 数据说明 / About the data`→`## About the data`。不加锚点，不加语言入口。验收：`python3 tools/check_template.py --only C12 | head -1` 输出 `PASS C12`。
- [X] T025 [P] [US1] 把 `template/.github/chefs-pick/MAINTAINING.md` 改为纯英文，按 guidance-layer-en §7 第 1、3 条。除通则外，`## Release gates` 一节必须用英文完整列出 **6** 条有序门禁：(1) 全部认可度数据的核实日期不早于发布前 30 天；(2) 新生成仓库核心要素齐全、首次 CI 通过；(3) 占位符一次搜索全部找到，引导层之外无模板作者身份信息、模板版本历史或开发过程文件，执行清理命令后引导层完整移除且无失效引用；(4) 按起步清单完成定制后社区标准自检页全部达标；(5) 全部动作引用固定到提交哈希、工作流令牌默认只读；(6) 全部译本与当前英文原文对齐。正文中原有的 `gate 2`、`gate 4` 编号引用必须仍指向同一条，不得错位；`All five gates` 改为 `All six gates`。**本任务不加"Keeping the translations in step"小节**，它由 T032 处理。不加锚点，不加语言入口。验收：`python3 tools/check_template.py --only C18 | head -1` 输出 `FAIL`（缺 `--update-digests`，由 T032 补上），且 `grep -c '^   *[1-6]\.' template/.github/chefs-pick/MAINTAINING.md` 不小于 6。
- [X] T026 [P] [US1] 把 `template/.github/chefs-pick/UPGRADE-TO-TEAM.md` 改为纯英文，按 guidance-layer-en §9。H1→`# Growing into a team project`；两个小节标题取英文；增强项表格表头→`| Addition | Purpose | Source | Adoption |`，5 行只留英文；末两节条目改纯英文，`认可度 / Adoption：`→`Adoption:`、`来源 / Source：`→`Source:`；表中 Star 数一字不动。不加锚点，不加语言入口。验收：`python3 tools/check_template.py --only C19 | head -1` 输出 `PASS C19`。
- [X] T027 [P] [US1] 把 `template/.github/chefs-pick/CHANGELOG.md` 改为纯英文，按 guidance-layer-en §10。H1→`# Template changelog`；删中文说明段保留英文段；`### Added / 新增`→`### Added`；`## [1.0.0] - 2026-09-18` 下条目改纯英文；在 `## [Unreleased]` 下新增 `### Changed` 与一条记录，逐字为：`- Documentation is now English-first: the guide layer is a single-language English edition, with Simplified Chinese supplied as separate `README.zh-CN.md` and `SETUP.zh-CN.md` files reached from a language selector. The previous side-by-side bilingual layout is gone.`。版本标题不加锚点。验收：`python3 -c "import re;t=open('template/.github/chefs-pick/CHANGELOG.md',encoding='utf-8').read();b=''.join(l for l in t.splitlines(True) if '简体中文' not in l);print('CJK=%d anchors=%d'%(sum(1 for c in b if '\u4e00'<=c<='\u9fff'),len(re.findall('^<!-- anchor: ',t,re.M))))"` 输出 `CJK=0 anchors=0`。
- [X] T028 [P] [US1] 把 `template/.github/chefs-pick/LICENSE` 改为纯英文，按 guidance-layer-en §11。**MIT 正文（第 1 行到 `SOFTWARE.` 那一行）一个字符都不得改动**；只删除末尾 `---` 之后的中文段落，保留其上的英文段落；`Copyright (c) 2026 Chef's Pick OSS Starter contributors` 必须仍在第 3 行。验收：`python3 tools/check_template.py --only C15 | head -1` 输出 `PASS C15`。

**Checkpoint**：8 份英文文档改造完毕。此时**整项 C11 仍会 FAIL**——两个语言入口指向的译本文件还不存在，互达断言过不去。这是 T029/T030 的前置信号，属预期；各文档的纯度与锚点已由各任务自带的验收命令单独确认。

---

## Phase 4: User Story 2 - 中文读者读到一份纯中文的完整文档 (Priority: P2)

**Goal**: 新增两份纯中文译本，与英文原文章节一一对应。

**Independent Test**: 两份译本的锚点序列与英文原文逐一相同，且预处理后不出现连续 6 个及以上英文词。

**前置**：必须在 T021、T022 完成之后执行，否则来源标记一写就过期。

- [X] T029 [US2] 新建 `template/.github/README.zh-CN.md`，按 guidance-layer-en §2 与 language-structure §0 §1 §2 §3 §4 §5 §6。头部顺序：锚点行 `<!-- anchor: chefs-pick-oss-starter -->`、H1 `# Chef's Pick OSS Starter`、空行、语言入口 `[English](README.md) · **简体中文**`、空行、规范性声明 `> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。`、空行、来源标记 `<!-- translation-of: README.md sha256:0000000000000000 -->`（占位值，T031 统一刷新）。12 个锚点与中文标题按 language-structure §3 的表格逐字照抄。`the-picks-at-a-glance` 一节逐字照抄 language-structure §5，**不得复制那张 16 行摘要表**。清理命令代码块与英文原文完全相同。指向 GUIDE/SOURCES/MAINTAINING 等只有英文版的文档时直接链接，**不加任何"目标是英文"的提示**。验收（另一份译本可能尚未建好，整项 C11 要到 T030 之后才会绿）：`python3 -c "import re;t=open('template/.github/README.zh-CN.md',encoding='utf-8').read();print('anchors=%d sel=%d notice=%d digest=%d'%(len(re.findall('^<!-- anchor: ',t,re.M)),t.count('[English](README.md) · **简体中文**'),t.count('> 英文版是规范版本。'),len(re.findall('^<!-- translation-of: ',t,re.M))))"` 输出 `anchors=12 sel=1 notice=1 digest=1`。
- [X] T030 [P] [US2] 新建 `template/.github/chefs-pick/SETUP.zh-CN.md`，按 guidance-layer-en §4 与 language-structure §0 §1 §2 §3 §4 §5。头部顺序同 T029，语言入口为 `[English](SETUP.md) · **简体中文**`，规范性声明为 `> 英文版是规范版本。本页与 [SETUP.md](SETUP.md) 不一致时，以英文版为准。`，来源标记为 `<!-- translation-of: SETUP.md sha256:0000000000000000 -->`。3 个锚点与中文标题为 `setup-checklist`/`# 起步清单`、`placeholders`/`## 占位符`、`steps`/`## 步骤`。`placeholders` 一节开头逐字照抄 language-structure §5，**不得复制登记表**，其后给出两条 `git grep` 命令的中文说明（命令本身照抄不译）。`steps` 一节用中文表格呈现 S01 ~ S09，表头 `| 编号 | 类型 | 步骤 | 如何确认 |`，步骤编号与命令不译。验收：`python3 -c "import re;t=open('template/.github/chefs-pick/SETUP.zh-CN.md',encoding='utf-8').read();print('anchors=%d sel=%d notice=%d digest=%d'%(len(re.findall('^<!-- anchor: ',t,re.M)),t.count('[English](SETUP.md) · **简体中文**'),t.count('> 英文版是规范版本。'),len(re.findall('^<!-- translation-of: ',t,re.M))))"` 输出 `anchors=3 sel=1 notice=1 digest=1`；随后 `python3 tools/check_template.py --only C11 | head -1` 输出 `PASS C11 Language structure`（两份译本齐备，互达断言此时才成立）。

**Checkpoint**：`python3 tools/check_template.py --only C11` 整体应 PASS。

---

## Phase 5: User Story 3 - 维护者不会让译本悄悄失效 (Priority: P3)

**Goal**: 来源标记填入真值，维护说明写清怎么用，发布门禁有自动落点。

**Independent Test**: 改动英文原文任意一句后运行 `python3 tools/check_template.py` 出现 `WARN C24` 且退出码为 0；加 `--release` 则 `FAIL C24` 且退出码为 1。

- [ ] T031 [US3] 在仓库根运行 `python3 tools/check_template.py --update-digests`，把 `template/.github/README.zh-CN.md` 与 `template/.github/chefs-pick/SETUP.zh-CN.md` 的来源标记从占位值 `sha256:0000000000000000` 刷新为真实摘要。不要手算摘要，也不要手改这两行。验收：`python3 tools/check_template.py --only C24 | head -1` 输出 `PASS C24 Translation freshness`，且再次运行 `--update-digests` 输出 `No digest needed updating.`。
- [X] T032 [US3] 在 `template/.github/chefs-pick/MAINTAINING.md` 中新增英文小节 `## Keeping the translations in step`，按 [contracts/guidance-layer-en.md](./contracts/guidance-layer-en.md) §7 第 2 条：说明译本只覆盖 README 与 SETUP 两份文档；改动英文原文后 `python3 tools/check_template.py` 会以 `WARN` 提示哪份译本过期且不影响退出码；更新译文后运行 `python3 tools/check_template.py --update-digests` 刷新来源标记；发布前 `--release` 会把过期译本按 FAIL 处理，对应发布门禁第 6 条。全节用英文书写，不加锚点。验收：`python3 tools/check_template.py --only C18 | head -1` 输出 `PASS C18`。
- [ ] T033 [US3] 验证 WARN/FAIL 两条路径确实生效：在 `template/.github/README.md` 的任意一段英文末尾临时追加一个句号，运行 `python3 tools/check_template.py | grep -E '^(WARN|FAIL) C24'` 应出现 `WARN C24` 且 `echo $?` 为 0；再运行 `python3 tools/check_template.py --release | grep -E '^FAIL C24'` 应出现且退出码为 1；随后 `git checkout -- template/.github/README.md` 还原。把三次输出记入 `specs/002-english-first-docs/baseline.md` 的"C24 行为验证"一节。验收：还原后 `git status --short template/` 无输出。

---

## Phase 6: User Story 4 - 使用者学会给自己的项目做同样的事 (Priority: P3)

**Goal**: 模块讲解教使用者给自己的项目做"英文规范版本 + 中文译本 + 语言入口"，并注明依据。

**Independent Test**: 按该小节的指引可在空仓库落地一套双语 README，不需要额外查资料；每条建议都点名了采用同一做法的项目。

- [X] T034 [US4] 在 `template/.github/chefs-pick/GUIDE.md` 中把 `## 中文译本 / Chinese translations` 一节整体替换为 `## Translating your own README`，按 guidance-layer-en §6 的五项要求：(1) 惯例做法——`README.md` 保持英文作为规范版本、另起 `README.zh-CN.md`、顶部放一行语言入口，并给出可直接抄用的两行写法；(2) 依据——点名 dify、RAGFlow、LobeChat、SiYuan、Ant Design、RustDesk，说明这些项目的根 README 都是英文规范版本；(3) 保留原有官方译本链接表，表头改为 `| File | Official Chinese translation |`，四行内容与 URL 不变；(4) 保留"替换译本时保留文件首行来源注释"的提示；(5) 说明这正是本模板自己采用的做法。全节用英文书写。同时把 GUIDE 正文中指向旧锚点 `#中文译本--chinese-translations` 的链接改为 `#translating-your-own-readme`。验收：`python3 tools/check_template.py --only C11,C14 | tail -1` 汇总行无 FAIL。

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 跨产物一致性收尾、人工验收与全量回归

- [ ] T035 在 `specs/001-chefs-pick-starter/contracts/guidance-layer.md` 的 §0「通用规则」中，把"双语写法"整段替换为指向本功能新契约的说明：英文为规范版本、中文以独立译本提供、语言入口与章节锚点的逐字规则见 `specs/002-english-first-docs/contracts/language-structure.md`，§1 ~ §7 的文档结构见 `specs/002-english-first-docs/contracts/guidance-layer-en.md`。同时把 §1 ~ §7 中所有"必须同时含有中文字符和英文字母"一类的双语要求删除。**不要改动 §4.4、§4.5 的数据表**（T020 已处理）。验收：`grep -c '双语写法' specs/001-chefs-pick-starter/contracts/guidance-layer.md` 输出 `0`，且 `python3 tools/check_template.py --only C23 | head -1` 仍输出 `PASS C23`。
- [ ] T036 把校验项总数从 22 改为 24、并让汇总行含 `warned` 的表述同步到 **5 处**陈旧交叉引用。**明确裁定：`specs/001-chefs-pick-starter/tasks.md` 不在修改范围内**——它是已完成功能的执行记录，改它等于改历史；它里面的两处旧值由 T035 在 001 契约 §0 加的指向说明覆盖。要改的 5 处是：(1) `specs/001-chefs-pick-starter/quickstart.md` 第 19 行，`Summary: 22 passed, 0 failed, 0 skipped` → `Summary: 24 passed, 0 failed, 0 warned, 0 skipped`，同行括号中的 `21 passed, 0 failed, 1 skipped` → `23 passed, 0 failed, 0 warned, 1 skipped`；(2) `specs/001-chefs-pick-starter/plan.md` 第 40 行，`结构校验，共 22 项` → `结构校验，共 24 项`；(3) 同文件第 64 行，`22 项校验（C01–C22）` → `24 项校验（C01–C24）`；(4) `specs/001-chefs-pick-starter/contracts/tooling.md` 第 95 行，末句 `全部共 22 项。` → `全部共 24 项。C23、C24 由功能 002 新增，见 specs/002-english-first-docs/contracts/tooling-delta.md。`；(5) 工作区根 `README.md` 第 24 行，`# 22 项结构校验 / 22 structural checks` → `# 24 项结构校验 / 24 structural checks`。只改这些数字与汇总行措辞，不动其余内容。验收：`grep -rn '22 passed\|22 项\|22 structural checks\|C01–C22\|C01-C22' specs/001-chefs-pick-starter/quickstart.md specs/001-chefs-pick-starter/plan.md specs/001-chefs-pick-starter/contracts/tooling.md README.md` 无输出（命令刻意不含 `specs/001-chefs-pick-starter/tasks.md`，因为那一份按上面的裁定保持原样）。
- [ ] T037 按 [quickstart.md](./quickstart.md) §B 逐项执行人工验收 V1 ~ V6 与 V10，并把每一项的实际结果记入 `specs/002-english-first-docs/baseline.md` 的"人工验收"一节。这七项是 SC-003、SC-004、SC-010 的唯一执行者，并承担 SC-013 中自动检查够不到的那一半（锚点渲染后不可见）；锚点计数本身由 T041 覆盖。自动检查覆盖不到的是：V1 渲染后看不到 `<!-- anchor:` 与 `<!-- translation-of:`；V2 从英文首页一步到中文首页且能一步返回；V3 通读中文首页无需回查英文；V4 通读英文首页不遇中文散文也无内容缺口；V5 从中文首页点向模块讲解落到英文且无任何提示；V6 一条清理命令执行后 `git grep -n 'chefs-pick'` 无输出；V10 `MAINTAINING.md` 的 `## Release gates` 英文完整列出 6 条且正文的 `gate 2`、`gate 4` 仍指向原来那两条。任一项不符则回到对应文档任务修复，不得标记完成。验收：`baseline.md` 中"人工验收"一节的七项全部记为通过。
- [ ] T038 在仓库根运行 `python3 -m unittest discover -s tools/tests`，确认全绿且用例数不少于基线的 199。任一失败则定位到具体检查项修复，不得跳过或删除用例。验收：输出末尾为 `OK`。
- [ ] T039 在仓库根运行 `python3 tools/check_template.py`，确认末行为 `Summary: 24 passed, 0 failed, 0 warned, 0 skipped`。验收：退出码为 0。
- [ ] T040 在仓库根运行 `python3 tools/check_template.py --release`，确认退出码为 0 且无 FAIL。验收：`echo $?` 输出 `0`。
- [ ] T041 按 quickstart.md 的 A10、A11、A12 三段脚本逐一执行，确认：8 个英文文件 CJK 计数全为 0；两份译本最长英文词串小于 6；四个文件的锚点计数分别为 12、12、3、3；三条单一数据源标记各只出现 1 次。任一不符则回到对应文档任务修复。验收：三段脚本的输出全部符合期望值。
- [ ] T042 按 quickstart.md §C 执行四项回归确认：`git diff --stat template/ -- ':!*.github/README*' ':!*chefs-pick*'` 无输出（交付给使用者的项目文件未被改动）；`--only C15` PASS；`grep -c '★' template/.github/chefs-pick/SOURCES.md` 与基线相同；`git ls-files template/ | wc -l` 输出 `28`。验收：四项全部符合。

---

## Dependencies & Execution Order

### 阶段依赖

- **Phase 1（T001）**：无依赖，最先执行。
- **Phase 2（T002 ~ T020）**：依赖 Phase 1。**阻塞所有用户故事**——校验工具是全部验收命令的基础。
- **Phase 3（US1，T021 ~ T028）**：依赖 Phase 2。
- **Phase 4（US2，T029 ~ T030）**：依赖 T021、T022（译本的来源标记必须基于定稿的英文原文）。
- **Phase 5（US3，T031 ~ T033）**：T031 依赖 T029、T030；T032 依赖 T025；T033 依赖 T031。
- **Phase 6（US4，T034）**：依赖 T023（同一文件，串行）。
- **Phase 7（T035 ~ T042）**：T035 依赖 T020；T036 依赖 T009（C23、C24 登记后总数才是 24）；T037 依赖全部文档任务；T038 ~ T042 依赖其余全部。

### 用户故事依赖

- **US1（P1）**：只依赖 Phase 2，可独立交付 —— **这就是 MVP**。
- **US2（P2）**：依赖 US1 的 T021、T022。
- **US3（P3）**：依赖 US2。
- **US4（P3）**：只依赖 US1 的 T023，与 US2、US3 互不相干，可并行。

### 同文件串行约束

- `tools/check_template.py`：T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009，**必须串行**。
- `template/.github/chefs-pick/MAINTAINING.md`：T025 → T032。
- `template/.github/chefs-pick/GUIDE.md`：T023 → T034。
- `specs/001-chefs-pick-starter/contracts/guidance-layer.md`：T020 → T035。
- `specs/002-english-first-docs/baseline.md`：T001 → T033 → T037。

### 并行机会

- Phase 2 的测试任务：T010、T011、T012、T013、T014、T015、T016、T017、T019 共 9 个，全部不同文件，可同时派给 9 个子代理。
- Phase 3 的文档任务：T022 ~ T028 共 7 个，全部不同文件，可同时派发（T021 建议先单独完成）。
- Phase 4 的 T030 可与 T029 并行。
- Phase 7 的 T035、T036 互不相干，可并行。

```text
# 示例：Phase 2 测试任务一次性并行派发
Task: "重写 tools/tests/test_checks_identity.py 的 C11 用例"     # T010
Task: "更新 tools/tests/test_checks_selection.py 的 C12 字面量"  # T011
Task: "更新 tools/tests/test_checks_links.py"                    # T012
Task: "更新 tools/tests/test_checks_markers.py 的 C08 表头"      # T013
Task: "更新 tools/tests/test_checks_maintaining.py 的 C18 用例"  # T014
Task: "更新 tools/tests/test_checks_upgrade.py 的 C19 字面量"    # T015
Task: "新建 tools/tests/test_checks_contract_parity.py"          # T016
Task: "新建 tools/tests/test_checks_translation.py"              # T017
Task: "在 tools/tests/test_verify_sources.py 新增契约写入用例"   # T019
```

---

## Implementation Strategy

### MVP（只做 US1）

Phase 1 + Phase 2 + Phase 3 = T001 ~ T028。交付后模板仓库首页已是一份干净的英文文档，英文读者的问题当场解决。此时还没有中文译本，语言入口指向的文件不存在——**所以 MVP 若要单独发布，T021、T022 的语言入口行必须一并删除**，否则 C11 的互达断言会失败。完整交付时不存在这个问题。

### 增量交付顺序

1. **Phase 1 + 2** → 校验工具就位，测试全绿，契约漂移消除。
2. **Phase 3（US1）** → 英文侧完成，MVP 可验收。
3. **Phase 4（US2）** → 中文侧完成，双语能力恢复。
4. **Phase 5（US3）** → 防腐机制就位，发布门禁有落点。
5. **Phase 6（US4）** → 把做法教给使用者。
6. **Phase 7** → 跨产物一致性收尾、人工验收、全量回归。

### 任务粒度自检

每个任务都满足：单一文件、无判断题、逐字内容与固定数据就地给出或明确指向契约的某一节、自带可执行的验收命令。T033、T037 ~ T042 是纯验证与同步任务，不改实现代码，验收即执行本身。
