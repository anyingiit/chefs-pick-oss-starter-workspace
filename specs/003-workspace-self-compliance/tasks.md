# Tasks: 工作区自身遵守模板定下的规矩

**Feature**: `specs/003-workspace-self-compliance/` | **Plan**: [plan.md](./plan.md)

## Format: `[ID] [P?] [Story] Description`

`[P]` 表示可与同批其他 `[P]` 任务并行（不同文件、互不依赖）。`[USn]` 对应规格中的用户故事。

## 执行约定（每个任务都适用）

- 每个任务只改**一个文件**。任务里写「逐字」的内容必须一字不差地照抄，不得润色、不得改标点。
- 契约指的是 `specs/003-workspace-self-compliance/contracts/` 下的文件。引用某一节时，照该节办即可，不需要另作判断。
- 每个任务自带验收命令，命令的期望输出就写在任务里。验收不通过不得标记完成。
- **Phase 3 完成后到 Phase 4 完成前，整套校验会失败**（判据已就位而文档尚未改造）。这是预期状态，不是出错，不要因此回退工具改动。
- `template/` 下的任何文件一个字节都不能改。

---

## Phase 1: Setup（基线）

- [ ] T001 在 `specs/003-workspace-self-compliance/baseline.md` 新建文件，记录改造前基线。逐条运行并把实测值填进一张三列表格（项目 / 命令 / 实测）：`python3 -m unittest discover -s tools/tests 2>&1 | tail -3` 取用例数与结果；`python3 tools/check_template.py | tail -1` 取汇总行；`git ls-files template/ | wc -l` 取文件数；`python3 -c "import re;print(len(re.findall(r'[一-鿿]',open('README.md',encoding='utf-8').read())))"` 取首页中文字符数。期望值分别是 `Ran 239 tests` / `OK`、`Summary: 24 passed, 0 failed, 0 warned, 0 skipped`、`28`、`288`。文件中另留两个空小节，标题逐字为 `## C26、C27 行为验证（T017）` 与 `## 人工验收（T018）`，正文各写一行 `_待填写。_`。验收：`grep -c '^## ' specs/003-workspace-self-compliance/baseline.md` 输出 `3`。

---

## Phase 2: Foundational（阻塞性前置）

- [ ] T002 在 `tools/check_template.py` 中，紧接现有 `SINGLE_SOURCE_MARKERS` 常量之后，新增契约 [tooling-delta-003.md](./contracts/tooling-delta-003.md) §1 给出的四个常量：`WORKSPACE_SOURCE`、`WORKSPACE_TRANSLATION`、`WORKSPACE_SELECTOR_LINES`、`WORKSPACE_ANCHOR_SEQUENCE`，取值逐字照抄该节。只加常量，不加函数，不改动任何现有代码行。验收：`python3 -c "import sys;sys.path.insert(0,'tools');import check_template as c;print(c.WORKSPACE_SOURCE, c.WORKSPACE_TRANSLATION, len(c.WORKSPACE_SELECTOR_LINES), len(c.WORKSPACE_ANCHOR_SEQUENCE))"` 输出 `README.md README.zh-CN.md 2 5`，且 `python3 tools/check_template.py | tail -1` 仍输出 `Summary: 24 passed, 0 failed, 0 warned, 0 skipped`。

---

## Phase 3: User Story 4 - 工作区的合规由校验自动判定 (Priority: P3) — 先行，因为它为后续文档改造提供判据

**Story goal**：语言、章节、事实、新鲜度四类判定全部进入日常校验，不满足时按契约规定的方式失败。

**Independent test**：人为制造每一类违规，确认校验按契约规定的严重级别失败并指名问题。

- [ ] T003 在 `tools/check_template.py` 中新增函数 `check_c25(ctx)`，实现契约 [tooling-delta-003.md](./contracts/tooling-delta-003.md) §3 的六项判定。路径解析按该契约 §2：用 `repo_root = Path(__file__).resolve().parent.parent`，**不得**使用 `ctx.template_dir`，并在文档字符串中写明这一点（照 `check_c23` 的写法）。`README.md` 或 `README.zh-CN.md` 不存在时 `raise SkipCheck`。语言纯度一项必须调用现有的 `strip_for_purity`、`cjk_count`、`longest_english_run`，不得另写实现。锚点不一致的报告写法与 `check_c11` 完全一致（`expected:` / `found:` / 非空时 `missing:` / `unexpected:`）。只加这一个函数，暂不注册。验收：`python3 -c "import sys;sys.path.insert(0,'tools');import check_template as c;print(callable(c.check_c25))"` 输出 `True`，且 `python3 tools/check_template.py | tail -1` 仍输出 `Summary: 24 passed, 0 failed, 0 warned, 0 skipped`。
- [ ] T004 在 `tools/check_template.py` 中新增函数 `check_c26(ctx)`，实现契约 §4 的三项判定。路径解析同 T003。声明值按契约 [workspace-structure.md](./contracts/workspace-structure.md) §6 的句式提取：英文版用 `` `template/` holds (\d+) files `` 与 `(\d+) structural checks``，中文版用 `` `template/` 共 (\d+) 个文件 `` 与 `(\d+) 项结构校验`；规格目录一项判定 `specs/` 下每个目录名是否以 `` `specs/<目录名>/` `` 形式出现。实际值分别取 `template/` 下被 git 跟踪的文件数（用 `iter_files`）、`len(CHECKS)`、`specs/` 下的目录名集合。每条问题信息必须同时含声明值与实际值，写法逐字照契约 §4 给出的两个样例。句式缺失时同样 FAIL，信息写成 `f"{rel}: no template file count found"` 一类。只加这一个函数，暂不注册。验收：`python3 -c "import sys;sys.path.insert(0,'tools');import check_template as c;print(callable(c.check_c26))"` 输出 `True`，且 `python3 tools/check_template.py | tail -1` 仍输出 `Summary: 24 passed, 0 failed, 0 warned, 0 skipped`。
- [ ] T005 在 `tools/check_template.py` 中新增函数 `check_c27(ctx)`，实现契约 §5：与 `check_c24` 同构，对象换成工作区首页。来源标记缺失、格式不符、或多于一处一律 FAIL；标记合法但摘要过期则 `raise WarnCheck([...])`，信息逐字为 `f"{WORKSPACE_TRANSLATION}: source marker is stale for {WORKSPACE_SOURCE} (recorded {old}, current {new}); run python3 tools/check_template.py --update-digests"`。摘要算法复用 `hashlib.sha256(path.read_bytes()).hexdigest()[:16]`。路径解析同 T003。只加这一个函数，暂不注册。验收：`python3 -c "import sys;sys.path.insert(0,'tools');import check_template as c;print(callable(c.check_c27))"` 输出 `True`，且 `python3 tools/check_template.py | tail -1` 仍输出 `Summary: 24 passed, 0 failed, 0 warned, 0 skipped`。
- [ ] T006 在 `tools/check_template.py` 的 `CHECKS` 注册表中，紧接 `"C24"` 那一行之后，逐字追加契约 §6 的三行注册项。不改动任何既有注册行。验收：`python3 -c "import sys;sys.path.insert(0,'tools');import check_template as c;print(len(c.CHECKS))"` 输出 `27`；此时 `python3 tools/check_template.py | tail -1` 预计输出 `Summary: 24 passed, 3 failed, 0 warned, 0 skipped`（文档尚未改造，三项新检查必然失败），这是预期状态。
- [ ] T007 在 `tools/check_template.py` 的 `update_digests()` 中，于处理完 `template/` 下译本的循环之后，追加处理工作区首页译本的分支，按契约 §7 **复用同一段替换实现**：单处正则替换、`write_bytes` 写回、发现重复标记时打印 `f"{WORKSPACE_TRANSLATION}: skipped (found {n} source marker lines for {WORKSPACE_SOURCE}; expected exactly one)"` 并原样保留文件。不得为工作区另写一份替换逻辑。工作区译本不存在时静默跳过。验收：`python3 tools/check_template.py --update-digests` 不报错且退出码为 0（此时工作区译本尚不存在，应静默跳过）。

---

## Phase 4: User Story 1 + 2 + 3 - 文档改造 (Priority: P1/P2)

**Story goal**：首页转为英文规范版 + 独立中文译本，发布流程写对，三项事实与仓库现状一致。

**Independent test**：见 quickstart.md 的 A7、A8、A9 与 V1 ~ V4。

- [ ] T008 [US1][US2][US3] 用契约 [workspace-structure.md](./contracts/workspace-structure.md) §9 代码块中的内容**整体替换** `README.md` 的全部内容，一字不差，包括空行。该代码块用四个反引号围栏包裹，照抄时不要把最外层的四反引号写进文件。替换后文件不含任何 `<!-- translation-of:` 行。验收：`python3 -c "import re;print(len(re.findall(r'[一-鿿]',open('README.md',encoding='utf-8').read())))"` 输出 `4`（仅语言入口中的「简体中文」四字）；`grep -c '^<!-- anchor: ' README.md` 输出 `5`；`grep -c 'translation-of' README.md` 输出 `0`。
- [ ] T009 [US2] 新建 `README.zh-CN.md`，内容为契约 §10 代码块中的全部内容，一字不差，包括空行与那一行填着 16 个 `0` 的来源标记。同样不要把最外层的四反引号写进文件。验收：`grep -c '^<!-- anchor: ' README.zh-CN.md` 输出 `5`；`grep -c '^<!-- translation-of: README.md sha256:0\{16\} -->$' README.zh-CN.md` 输出 `1`；`python3 -c "
import sys;sys.path.insert(0,'tools')
from check_template import strip_for_purity, longest_english_run
print(longest_english_run(strip_for_purity(open('README.zh-CN.md',encoding='utf-8').read(),'[English](README.md) · **简体中文**')))"` 输出小于 `6` 的整数。
- [ ] T010 运行 `python3 tools/check_template.py --update-digests`，把 `README.zh-CN.md` 的来源标记刷新为 `README.md` 的当前摘要。不得手算摘要，不得手改那一行。验收：`grep -c '0\{16\}' README.zh-CN.md` 输出 `0`；`python3 tools/check_template.py --only C27 | head -1` 输出 `PASS C27 Workspace translation freshness`。
- [ ] T011 [US1] 在 `specs/001-chefs-pick-starter/quickstart.md` 的 §B 第 2 步中，把现有那条 `开发工作区已是 Git 仓库时` 的子项改写为两条：第一条保留现有 `git subtree split` 步骤，但把引导语改为逐字的 `**首次发布到空仓库时**（本步骤只适用于这一种情形）：`；第二条新增，引导语逐字为 `**后续发布到已有内容的仓库时**：`，正文指向 `README.md` 的 `Publishing` 一节，并逐字写明 `绝不要强制推送；subtree split 切出的历史与模板仓库没有共同祖先，强推会让 v1.0.0 标签指向的提交不再可达。`。不改动 §B 的其他步骤。验收：`grep -c '首次发布到空仓库时\|后续发布到已有内容的仓库时' specs/001-chefs-pick-starter/quickstart.md` 输出 `2`；`grep -c 'v1.0.0 标签指向的提交不再可达' specs/001-chefs-pick-starter/quickstart.md` 输出 `1`。

---

## Phase 5: 测试

- [ ] T012 [P] 新建 `tools/tests/test_workspace_language.py`，覆盖 C25：语言入口缺失或写错、锚点序列不一致（改名一处，断言报告同时含 `missing:` 与 `unexpected:`）、英文版混入中文散文、中文版出现过长英文词串、中文版缺规范性声明、英文版出现规范性声明。全部用临时目录夹具，通过打补丁 `check_template.__file__` 的方式隔离（照 `test_checks_contract_parity.py` 中 `FakeRepoRoot` 的既有写法），**不得读写真实的 `README.md` 或 `template/`**。验收：`python3 -m unittest tools.tests.test_workspace_language -v 2>&1 | tail -3` 末尾为 `OK`，用例数不少于 6。
- [ ] T013 [P] 新建 `tools/tests/test_workspace_facts.py`，覆盖 C26：文件数声明值与实际值不符（断言报告同时含两个数字）、校验项数不符、缺某个规格目录、句式完全缺失。隔离方式与并行约束同 T012。验收：`python3 -m unittest tools.tests.test_workspace_facts -v 2>&1 | tail -3` 末尾为 `OK`，用例数不少于 4。
- [ ] T014 在 `tools/tests/test_checks_translation.py` 中追加覆盖 C27 与 `update_digests` 工作区分支的用例：来源标记缺失时 FAIL、重复标记时 FAIL 且 `--update-digests` 拒绝并原样保留文件、摘要过期时为 WARN 而 `--release` 下为 FAIL。隔离方式同 T012。不得削弱或删除本文件中任何既有用例。验收：`python3 -m unittest tools.tests.test_checks_translation 2>&1 | tail -3` 末尾为 `OK`，用例数比改前多至少 3 个。

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T015 全量运行 `python3 -m unittest discover -s tools/tests`，确认全绿且用例数不少于 245。任一失败则定位到具体检查项修复，不得跳过或删除用例。验收：输出末尾为 `OK`。
- [ ] T016 全量运行 `python3 tools/check_template.py`，确认末行为 `Summary: 27 passed, 0 failed, 0 warned, 0 skipped` 且退出码为 0；再运行 `python3 tools/check_template.py --release`，确认退出码为 0 且无 FAIL。验收：两条命令的 `echo $?` 均输出 `0`。
- [ ] T017 按 [quickstart.md](./quickstart.md) 的 A10 执行 C26 与 C27 的行为验证，把四次命令的实测输出与退出码记入 `specs/003-workspace-self-compliance/baseline.md` 的 `## C26、C27 行为验证（T017）` 一节。期望：C26 为 `FAIL C26` 且报告同时含 `99` 与 `28`、退出码 1；C27 日常为 `WARN C27` 退出码 0、`--release` 为 `FAIL C27` 退出码 1；两次 `git checkout --` 还原后 `git status --short` 无输出。验收：该节不再含 `_待填写。_`，且还原后 `git status --short` 无输出。
- [ ] T018 按 [quickstart.md](./quickstart.md) §B 执行人工验收 V1 ~ V4 与 V7（V5、V6 需要真实的测试模板仓库，若本环境无法创建则在记录中写明「未执行，原因：无法创建测试仓库」，不得标记为通过），把每一项的实际结果记入 `baseline.md` 的 `## 人工验收（T018）` 一节。验收：该节逐项列出 V1 ~ V7 的结论，且 V1 ~ V4、V7 五项均记为通过。
- [ ] T019 按 [quickstart.md](./quickstart.md) §C 执行四项回归确认：`git diff --stat fb3ce9a HEAD -- template/` 无输出；`python3 tools/check_template.py --only C01,C11,C23,C24` 全部 PASS；`git ls-files template/ | wc -l` 输出 `28`；`git diff --stat fb3ce9a HEAD -- tools/verify_sources.py` 无输出。任一不符则回到对应任务修复。验收：四项全部符合。

---

## Dependencies & Execution Order

### 阶段依赖

- **Phase 1（T001）**：无依赖，最先执行。
- **Phase 2（T002）**：依赖 T001。
- **Phase 3（T003 ~ T007）**：T003、T004、T005 依赖 T002，三者之间互不依赖但改同一文件，必须串行；T006 依赖 T003 ~ T005 全部完成；T007 依赖 T002。
- **Phase 4（T008 ~ T011）**：T008 依赖 T006（需要 C25、C26 已注册才能验证）；T009 依赖 T008；T010 依赖 T009 与 T007；T011 依赖 T008。
- **Phase 5（T012 ~ T014）**：全部依赖 Phase 3 完成；T012、T013 可并行（不同文件），T014 与它们也可并行。
- **Phase 6（T015 ~ T019）**：依赖前述全部。

### 同文件串行约束

- `tools/check_template.py`：T002 → T003 → T004 → T005 → T006 → T007，严格串行。
- `README.md`：T008 单独占用。
- `specs/003-workspace-self-compliance/baseline.md`：T001 → T017 → T018。

### 并行机会

- T012、T013、T014 三项测试任务可同时进行（三个不同文件）。
- T011 与 T009、T010 可并行（`quickstart.md` 与首页译本互不相干）。

---

## Implementation Strategy

### MVP（只做 US1）

只修发布流程：T001 → T008 的发布一节 → T011。这样最危险的缺陷即刻消除，语言与事实改造可以随后进行。但本功能的四个故事共用同一份文件，拆开做会让 `README.md` 被改两次，因此建议一次做完。

### 增量交付顺序

1. Phase 1 ~ 2：基线与常量。
2. Phase 3：判据先就位（此时校验会失败，属预期）。
3. Phase 4：文档改造，校验转绿。
4. Phase 5 ~ 6：测试与回归。

### 任务粒度自检

19 个任务逐条满足：每条只动一个文件；逐字内容要么就地给出、要么明确指向契约的某一节（T008、T009 指向 §9、§10 的完整代码块，不需要执行者撰写任何散文）；固定数据（28、27、5、288、239、245）全部就地写明；每条自带可执行的验收命令与期望输出。T001、T015 ~ T019 是纯验证与记录任务，验收即执行本身。

唯一需要执行者注意而非判断的是：Phase 3 完成后到 Phase 4 完成前整套校验会失败，这一点已写进执行约定与 T006 的验收说明，不构成判断题。
