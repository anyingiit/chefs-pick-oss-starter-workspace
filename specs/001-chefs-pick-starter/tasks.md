---

description: "主厨精选开源仓库起步模板的实施任务清单"
---

# Tasks: 主厨精选开源仓库起步模板（Chef's Pick OSS Starter）

**Input**: Design documents from `specs/001-chefs-pick-starter/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/（template-layout、markers、project-files、guidance-layer、tooling）, quickstart.md；宪章 `.specify/memory/constitution.md` v1.0.1

**Tests**: 包含测试任务。plan.md 的 Implementation Notes 和 contracts/tooling.md §3 明确要求先写测试：每个检查项先写单元测试，确认失败后再实现，模板文件再用对应的检查项验收。

**Organization**: 任务按用户故事分组。各故事共用同一组模板文件，US2 ~ US5 在 US1 生成的文件基础上逐步补充，每个故事都有自己的一组校验，可单独验收。

## Format: `[ID] [P?] [Story] Description`

- **[P]**：可以并行（修改不同的文件，且不依赖尚未完成的任务）。各故事的测试任务（T033、T037、T040、T041、T046）虽然标了 [P]，但只表示文件不重叠，不得提前执行，必须紧接在各自的实现任务之前
- **[Story]**：任务所属的用户故事（US1 ~ US5）
- 每个任务下的子项依次说明：要读取的契约、所需数据、做法、验收方法

## 路径与执行约定（子代理必读）

- **前置条件**：宪章 v1.0.1 是 PATCH 级措辞澄清，按 Governance 需项目维护者确认后才生效。**确认之前不要开始 T001**，因为起步引导层的规定来自这次修订。
- **仓库根目录**：`/Users/user_laptop/Downloads/Temp_Workspace/chefs-pick-oss-starter`。下文路径都相对于这个目录，命令也都在这个目录下执行。
- **可以修改的文件**：只能修改任务里点名的文件。不得修改 `specs/`、`.specify/`、`.claude/` 下的任何内容。
- **逐字内容**：契约中标为"逐字"的内容必须原样复制。上游文件必须用 `gh api "repos/<owner>/<repo>/contents/<path>?ref=<提交哈希>" --jq .content | base64 -d` 按固定提交获取，并用 shell 重定向写入，不要手工重新输入，以免改动字节。
- **不自行做选型判断**：所有选型都已在 research.md 中定好。遇到以下情况时停止，把命令输出交给协调者，不要自行替换来源、修改契约或放宽检查逻辑：
  - 契约与上游实际内容不一致；
  - 验收失败，而且无法按契约修正；
  - 检查逻辑与契约互相矛盾。
- **禁止的操作**：初始化 Git、提交、推送、创建远程仓库、修改任何 GitHub 设置。网络访问只允许只读的 `gh api` 调用、`curl` 检查链接，以及运行 `tools/verify_sources.py`。
- **Python 要求**：Python 3.10+，只用标准库和 PyYAML。
- **串行修改**：`tools/check_template.py` 由多个任务依次修改，必须按这个顺序串行执行：T004 → T011 → T012 → T013 → T014 → T015 → T034 → T038 → T043 → T047。
- **串行修改（第二个共享文件）**：`template/.github/README.md` 也由多个任务依次修改，必须按这个顺序串行执行：T031 → T036 → T045 → T048（不实施 US4 时为 T031 → T036 → T048；不实施 US5 时到 T045 为止）。
- **测试的执行时机**：各故事新增检查项的测试文件（T033、T037、T040、T041、T046）都要紧接在它对应的实现任务之前编写，不要提前写。T016 不受这条限制：它测的是模板里的 `ci.yml`，文件不存在时以 `skipUnless` 跳过，可以和 US1 的实现任务并行。测试写完后处于失败状态（红灯），实现完成后才转为通过。因此阶段性验收不要用 `unittest discover` 跑全部测试，而要按任务里列出的测试模块名逐个运行。
- **校验项总数**：共 22 项（C01–C22）。模板尚未搭完时，只有 C01 会因为文件缺失而 FAIL，所以中途验收都要用 `--only` 排除 C01。
- **完成报告**：每个任务完成后都要运行它的验收命令，并在报告中附上输出的最后几行。

---

## Phase 1: Setup（共享基础）

**Purpose**：建立目录，准备测试样例。

- [X] T001 创建目录 `template/.github/ISSUE_TEMPLATE/`、`template/.github/workflows/`、`template/.github/chefs-pick/`、`tools/tests/fixtures/`
  - 读取：plan.md 的 "Project Structure"；contracts/template-layout.md §1
  - 验收：
    - `for d in template/.github/ISSUE_TEMPLATE template/.github/workflows template/.github/chefs-pick tools/tests/fixtures; do test -d "$d" || echo "missing $d"; done` 没有输出；
    - `python3 -c "import sys, yaml; assert sys.version_info >= (3, 10)"` 的退出码为 0。
- [X] T002 [P] 在开发工作区根目录创建 `.gitignore`
  - 读取：contracts/tooling.md §4（逐字）
  - 验收：`printf '__pycache__/\n*.pyc\n.DS_Store\n' | diff - .gitignore` 没有输出
- [X] T003 [P] 创建测试样例 `tools/tests/fixtures/pin_good.yml` 和 `tools/tests/fixtures/pin_bad.yml`
  - 读取：quickstart.md 附录 A（两段 YAML，逐字）
  - 验收：
    - `python3 -c "import yaml; [yaml.safe_load(open(p)) for p in ('tools/tests/fixtures/pin_good.yml', 'tools/tests/fixtures/pin_bad.yml')]"` 的退出码为 0；
    - `grep -c 'uses:' tools/tests/fixtures/pin_bad.yml` 输出 `4`。

---

## Phase 2: Foundational（校验框架，阻塞所有用户故事）

**Purpose**：建立 `tools/check_template.py` 的框架，以及 C01（实现于 T011，只在收尾阶段全量运行）以及 US1 要用到的检查项（C02、C03、C05、C06、C08、C09、C10、C11、C13、C14、C15、C17、C21、C22）和它们的单元测试。

**⚠️ CRITICAL**：本阶段完成之前，不得开始任何用户故事。

- [X] T004 创建 `tools/check_template.py` 框架，暂不实现具体检查
  - 读取：
    - contracts/tooling.md §1.1、§1.2；
    - contracts/template-layout.md §2、§6；
    - contracts/markers.md §1.2、§1.3、§2.2；
    - contracts/guidance-layer.md §2（占位符表表头）、§4.2（字段标签和级别取值）。
  - 做法：
    - 实现全部命令行参数（包括 `--files`）、退出码、输出格式、`Context`、`SkipCheck` 和 `selected()`；
    - 实现辅助函数 `iter_files`、`project_files`、`is_guidance`、`read_text`、`load_yaml` 和 `parse_placeholder_registry`；
    - 定义 §1.2 列出的全部常量，取值逐字照抄上面各契约章节；
    - 在 `CHECKS` 中按顺序登记 C01 ~ C22，检查函数暂时统一写成 `raise SkipCheck("not implemented")`。
  - 验收：
    - `python3 tools/check_template.py --template-dir /nonexistent; echo $?` 最后输出 `2`；
    - `python3 tools/check_template.py --only C99; echo $?` 最后输出 `2`；
    - `python3 tools/check_template.py` 最后一行为 `Summary: 0 passed, 0 failed, 22 skipped`。
- [X] T005 创建测试辅助模块 `tools/tests/helpers.py`（依赖 T004）
  - 读取：contracts/tooling.md §3（`helpers.py` 一行，以及开头的 `sys.path` 约定）
  - 验收：`python3 -c "import sys; sys.path.insert(0, 'tools/tests'); import helpers; print(helpers.write_tree, helpers.make_ctx, helpers.run_one)"` 的退出码为 0
- [X] T006 [P] 编写 `tools/tests/test_checks_layout.py`，覆盖 C01、C02、C03、C21（依赖 T005）
  - 读取：
    - contracts/tooling.md §1.3（C01、C02、C03、C21 所在行，以及 C21 的说明）、§3；
    - contracts/template-layout.md §2、§5。
  - 要求：
    - 每项检查至少写一个通过用例和一个失败用例；
    - C21 必须写四个用例，见 tooling §3 中该文件所在行：CRLF 失败（用 `Path.write_bytes(b"a\r\nb\r\n")` 直接写，不要改 `helpers.py`，因为 T006 ~ T010 并行共用它）、方括号中的字面回车符不报错（用 tooling §1.3 C21 给出的 `Icon[\r]` 那一行）、行尾空格失败、文件末尾缺换行失败。检查实现必须按字节读取，否则 CRLF 用例会误判通过。
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_layout.py'` 能运行，并因检查尚未实现而失败（预期的红灯）
- [X] T007 [P] 编写 `tools/tests/test_checks_automation.py`，覆盖 C05、C06（依赖 T005）
  - 读取：
    - contracts/tooling.md §1.3（C05、C06）、§3；
    - contracts/project-files.md 的 M11、M12（通过用例使用其中的逐字内容）。
  - 要求：C05 的失败用例至少包括以下四种：
    - 动作使用版本标签；
    - 动作只写了哈希，没有版本注释；
    - `permissions` 不是只读；
    - 缺少 `persist-credentials: false`。
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_automation.py'` 能运行，并出现失败（预期的红灯）
- [X] T008 [P] 编写 `tools/tests/test_checks_markers.py`，覆盖 C08、C09（依赖 T005）
  - 读取：
    - contracts/tooling.md §1.1（`--files`）、§1.3（C08、C09 的说明）、§3；
    - contracts/markers.md §1、§2；
    - contracts/guidance-layer.md §2（表头）。
  - 要求：
    - C08 的失败用例至少包括：出现未登记的占位符；出现禁止残留的标记；引导层的非 SETUP 文件中出现 `CHANGEME_`；
    - C08 另外验证：带 `--files` 时不做"实际出现的文件集合等于登记表第 3 列"这项比对，但仍然报告未登记的占位符；
    - C09 至少包括：第一行不一致；`LICENSE` 第一行不是 `MIT License`。
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_markers.py'` 能运行，并出现失败（预期的红灯）
- [X] T009 [P] 编写 `tools/tests/test_checks_identity.py`，覆盖 C10、C11（依赖 T005）
  - 读取：
    - contracts/tooling.md §1.3（C10、C11 的说明）；
    - contracts/template-layout.md §3、§4；
    - contracts/project-files.md 的 M09、M15、M16；
    - contracts/guidance-layer.md §1、§2、§3、§7、§8。
  - 要求：
    - C10 的失败用例至少包括：项目文件中出现 `Chef's Pick`；根目录 CHANGELOG 有两个二级标题；CODEOWNERS 中有生效行；FUNDING 中有值；
    - C10 另加一个失败用例：某个项目文件中出现中文字符（C10 要落实"协作文件用英文"）；
    - C11 至少包括：首页标题不符；某个标题行只有英文；GUIDE 缺少 `## M07`。
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_identity.py'` 能运行，并出现失败（预期的红灯）
- [X] T010 [P] 编写 `tools/tests/test_checks_links.py`，覆盖 C13、C14、C15、C17、C22（依赖 T005）
  - 读取：
    - contracts/tooling.md §1.3（C13、C14、C15、C17、C22 的说明）；
    - contracts/template-layout.md §3、§6；
    - contracts/project-files.md 的 M02。
  - 要求：失败用例至少包括以下五种：
    - C13：清理后，仍有项目文件引用 `chefs-pick/`；
    - C14：相对链接指向不存在的文件；
    - C15：第 3 行不符；
    - C17：GUIDE 的 M04 一节漏写了 `CONTRIBUTING.md`；
    - C22：删除 `CODE_OF_CONDUCT.md` 后，某个 YAML 配置文件仍然引用它。
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_links.py'` 能运行，并出现失败（预期的红灯）
- [X] T011 在 `tools/check_template.py` 中实现 C01、C02、C03、C21（依赖 T006）
  - 读取：同 T006
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_layout.py'` 全部通过
- [X] T012 在 `tools/check_template.py` 中实现 C05、C06（依赖 T007、T011）
  - 读取：同 T007
  - 注意：PyYAML 会把 `on` 键解析为 `True`，读取时需要兼容这两种写法
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_automation.py'` 全部通过
- [X] T013 在 `tools/check_template.py` 中实现 C08、C09（依赖 T008、T012）
  - 读取：同 T008
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_markers.py'` 全部通过
- [X] T014 在 `tools/check_template.py` 中实现 C10、C11（依赖 T009、T013）
  - 读取：同 T009
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_identity.py'` 全部通过
- [X] T015 在 `tools/check_template.py` 中实现 C13、C14、C15、C17、C22（依赖 T010、T014）
  - 读取：同 T010
  - 要求：C13 和 C22 都用 `tempfile.TemporaryDirectory` 复制模板目录，每轮结束都要清理
  - 验收：
    - `for m in test_checks_layout test_checks_automation test_checks_markers test_checks_identity test_checks_links; do PYTHONPATH=tools/tests python3 -m unittest "$m" || { echo "FAILED: $m"; exit 1; }; done`，5 个测试模块全部通过，且输出中没有 `FAILED:`。只跑本阶段这 5 个模块，其他故事的测试此时还不该存在；
    - `python3 tools/check_template.py --only C02,C03,C05,C06,C08,C09,C10,C11,C13,C14,C15,C17,C21,C22` 的最后一行显示 `0 failed`。此时 `template/` 只有空目录，各项应为 PASS 或 SKIP。不要运行不带 `--only` 的全量校验，因为 C01 必然报告文件缺失。

**Checkpoint**：校验框架就绪，可以开始用户故事。

---

## Phase 3: User Story 1 - 个人开发者一键获得"五脏俱全"的新仓库 (Priority: P1) 🎯 MVP

**Goal**：
- `template/` 下有 18 个项目文件，覆盖 M01 ~ M16 中有文件的 15 个模块（M10 只在清单里推荐，没有文件）；
- 起步引导层中已有首页介绍、SETUP、GUIDE，以及模板自身的 CHANGELOG 和 LICENSE；
- 首页的选型摘要表留给 US2 补充。

**Independent Test**：
- `python3 tools/check_template.py --only C02,C03,C05,C06,C08,C09,C10,C11,C13,C14,C15,C17,C21,C22` 全部 PASS；
- `for m in test_checks_layout test_checks_automation test_checks_markers test_checks_identity test_checks_links test_ci_pin_check; do PYTHONPATH=tools/tests python3 -m unittest "$m" || { echo "FAILED: $m"; exit 1; }; done` 全部通过；
- 发布前按 quickstart 的 C 部分执行 V1、V2、V4。

### Tests for User Story 1

- [X] T016 [P] [US1] 编写 `tools/tests/test_ci_pin_check.py`（依赖 T003、T005）
  - 读取：contracts/tooling.md §3（`test_ci_pin_check.py` 一行）；quickstart.md 附录 A
  - 要求：
    - 用 PyYAML 读取 `template/.github/workflows/ci.yml`，找到名为 "Check that actions are pinned to full commit SHAs" 的步骤，取出它的 `run` 脚本；
    - 分别把两个样例复制到临时目录下的 `.github/workflows/ci.yml`，在该目录中用 `bash -c` 执行脚本；
    - 期望 `pin_good` 的退出码为 0，`pin_bad` 的退出码为 1，且 `pin_bad` 的输出中恰好有 3 行包含 `.github/workflows/ci.yml:`。`grep -Rn` 打印的是完整相对路径，判断时用"包含"匹配，不要用"以 `ci.yml:` 开头"；
    - `ci.yml` 不存在时用 `skipUnless` 跳过。
  - 验收：
    - T024 完成前，运行 `python3 -m unittest discover -s tools/tests -p 'test_ci_pin_check.py'` 显示 skipped；
    - T024 完成后应当通过，由 T032 复核。

### Implementation for User Story 1

- [X] T017 [P] [US1] 生成 `template/LICENSE`（M02）
  - 读取：contracts/project-files.md 的 M02；research.md §4
  - 数据：`gh api "repos/github/choosealicense.com/contents/_licenses/mit.txt?ref=58267f8f2c5c0099810849cfd7677f52ae0c0eb3" --jq .content | base64 -d`
  - 做法：
    - 删除开头两个 `---` 之间的 front matter 及其后的空行；
    - 用 `sed -e 's/\[year\]/CHANGEME_YEAR/' -e 's/\[fullname\]/CHANGEME_COPYRIGHT_HOLDER/'` 替换两个占位符。方括号必须转义，否则会被 `sed` 当成字符类；
    - 不加来源注释。
  - 验收：
    - `python3 tools/check_template.py --only C15,C21 --files LICENSE` 两项 PASS；
    - `sed -n '3p' template/LICENSE` 输出 `Copyright (c) CHANGEME_YEAR CHANGEME_COPYRIGHT_HOLDER`。
- [X] T018 [P] [US1] 生成 `template/.gitignore`（M03）
  - 读取：contracts/project-files.md 的 M03；research.md §4
  - 做法：
    1. 用 `printf` 写入 M03 规定的 3 行文件头。
    2. 按 `macOS`、`Windows`、`Linux`、`VisualStudioCode`、`JetBrains` 的顺序，依次追加：一个空行、一行 `# --- Global/<名称>.gitignore ---`，以及 `gh api "repos/github/gitignore/contents/Global/<名称>.gitignore?ref=356fd7baab4c05e092194a41f64dbd5afc8817e4" --jq .content | base64 -d` 的输出。
    3. 确认文件末尾恰好只有一个换行。
  - 验收：
    - `python3 tools/check_template.py --only C09,C21 --files .gitignore` 两项 PASS；
    - `grep -c '^# --- Global/' template/.gitignore` 输出 `5`；
    - `grep -c $'\r' template/.gitignore` 输出 `2`。
- [X] T019 [P] [US1] 编写 `template/README.md`（M01）
  - 读取：contracts/project-files.md 的 M01（13 项结构和"不得包含"清单）；contracts/markers.md §1.2、§2.2
  - 数据（仅作参考）：`gh api "repos/othneildrew/Best-README-Template/contents/BLANK_README.md?ref=fc444eb7b04b2e4863f6080b1507a219e95103fa" --jq .content | base64 -d`
  - 验收：
    - `python3 tools/check_template.py --only C08,C09,C21 --files README.md` 全部 PASS 或 SKIP（`SETUP.md` 尚未生成时 C08 记为 SKIP）。相对链接由 T032 统一验收，因为本文件链接的 `CONTRIBUTING.md` 等可能还在并行生成中；
    - `grep -cE 'Built With|Roadmap|Acknowledgments|contrib.rocks' template/README.md` 输出 `0`（`grep -c` 在计数为 0 时退出码是 1，这属于正常，看输出即可）。
- [X] T020 [P] [US1] 生成 `template/CODE_OF_CONDUCT.md`（M04）
  - 读取：contracts/project-files.md 的 M04；contracts/markers.md §2.2；research.md R4、§4
  - 做法：
    1. 用 `printf` 写入来源注释行和一个空行。
    2. 追加 `gh api "repos/EthicalSource/contributor_covenant/contents/content/version/2/1/code_of_conduct.md?ref=7255a28d23d5bc296de2e4e4e9bb5ee1126f1345" --jq .content | base64 -d` 的输出，但要去掉 `+++` front matter 及其后的空行。
    3. 用 `sed -e 's/\[INSERT CONTACT METHOD\]/CHANGEME_CONDUCT_EMAIL/'` 替换联系方式占位符（方括号要转义）。
  - 验收：
    - `python3 tools/check_template.py --only C08,C09,C21 --files CODE_OF_CONDUCT.md` 全部 PASS 或 SKIP（C08 同上）；
    - `grep -c 'version 2.1' template/CODE_OF_CONDUCT.md` 输出大于 `0`；
    - `grep -cF '[INSERT CONTACT METHOD]' template/CODE_OF_CONDUCT.md` 输出 `0`；
    - `grep -c '^+++' template/CODE_OF_CONDUCT.md` 输出 `0`。以上两条的退出码会是 1，这是 `grep -c` 计数为 0 时的正常行为，看输出即可。
- [X] T021 [P] [US1] 编写 `template/CONTRIBUTING.md`（M05，原创英文）
  - 读取：contracts/project-files.md 的 M05；contracts/markers.md §2.2；contracts/tooling.md §1.3 的 C20 说明（CONTRIBUTING 部分）
  - 验收：
    - `python3 tools/check_template.py --only C08,C09,C21 --files CONTRIBUTING.md` 全部 PASS 或 SKIP（C08 同上）。相对链接由 T032 统一验收；
    - `grep -c '^## ' template/CONTRIBUTING.md` 输出 `8`。
- [X] T022 [P] [US1] 编写 `template/SECURITY.md`（M06）
  - 读取：contracts/project-files.md 的 M06；contracts/markers.md §2.2；contracts/tooling.md §1.3 的 C20 说明（SECURITY 部分）
  - 验收：
    - `python3 tools/check_template.py --only C08,C09,C21 --files SECURITY.md` 全部 PASS 或 SKIP（C08 同上）；
    - `grep -c 'security/advisories/new' template/SECURITY.md` 输出大于 `0`。
- [X] T023 [P] [US1] 创建 Issue 表单 `template/.github/ISSUE_TEMPLATE/bug_report.yml`、`template/.github/ISSUE_TEMPLATE/feature_request.yml`、`template/.github/ISSUE_TEMPLATE/config.yml`（M07）
  - 读取：contracts/project-files.md 的 M07（三个文件都是逐字内容）
  - 验收：
    - `python3 tools/check_template.py --only C03,C08,C09,C21 --files .github/ISSUE_TEMPLATE/bug_report.yml,.github/ISSUE_TEMPLATE/feature_request.yml,.github/ISSUE_TEMPLATE/config.yml` 全部 PASS 或 SKIP（C08 同上）；
    - `grep -c 'required: true' template/.github/ISSUE_TEMPLATE/bug_report.yml` 输出 `4`；
    - `grep -c 'required: true' template/.github/ISSUE_TEMPLATE/feature_request.yml` 输出 `2`。
- [X] T024 [P] [US1] 创建 `template/.github/workflows/ci.yml`（M11）
  - 读取：contracts/project-files.md 的 M11（逐字）；contracts/markers.md §2.2
  - 数据：`actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1`（已包含在逐字内容中）
  - 验收：`python3 tools/check_template.py --only C03,C05,C09,C21 --files .github/workflows/ci.yml` 全部 PASS
- [X] T025 [P] [US1] 创建 `template/.github/dependabot.yml`（M12）
  - 读取：contracts/project-files.md 的 M12（逐字）
  - 验收：`python3 tools/check_template.py --only C03,C06,C09,C21 --files .github/dependabot.yml` 全部 PASS
- [X] T026 [P] [US1] 创建 `template/CHANGELOG.md`、`template/.github/release.yml`（M09）和 `template/.github/PULL_REQUEST_TEMPLATE.md`（M08）
  - 读取：contracts/project-files.md 的 M08、M09（三个文件都是逐字内容）
  - 验收：
    - `python3 tools/check_template.py --only C03,C08,C09,C21 --files CHANGELOG.md,.github/release.yml,.github/PULL_REQUEST_TEMPLATE.md` 全部 PASS 或 SKIP（C08 同上）；
    - `python3 tools/check_template.py --only C10 --files CHANGELOG.md` 结果为 PASS。
- [X] T027 [P] [US1] 创建可选模块文件 `template/.editorconfig`、`template/.pre-commit-config.yaml`、`template/.github/CODEOWNERS`、`template/.github/FUNDING.yml`（M13 ~ M16）
  - 读取：contracts/project-files.md 的 M13 ~ M16（四个文件都是逐字内容）
  - 数据：`rev: 3e8a8703264a2f4a69428a0aa4dcb512790b2c8c  # frozen: v6.0.0`（已包含在逐字内容中）
  - 验收：
    - `python3 tools/check_template.py --only C03,C08,C09,C21 --files .editorconfig,.pre-commit-config.yaml,.github/CODEOWNERS,.github/FUNDING.yml` 全部 PASS 或 SKIP（C08 同上）；
    - `python3 tools/check_template.py --only C10 --files .github/CODEOWNERS,.github/FUNDING.yml` 结果为 PASS。
- [X] T028 [P] [US1] 编写起步清单 `template/.github/chefs-pick/SETUP.md`（双语）
  - 读取：contracts/guidance-layer.md §0、§2（S01 ~ S09 步骤表）；contracts/markers.md §1.2（登记表）、§3（官方链接）
  - 验收：
    - `python3 tools/check_template.py --only C11,C21 --files .github/chefs-pick/SETUP.md` 全部 PASS；
    - C08 的整体比对和相对链接检查都放在 T032 中进行。
- [X] T029 [P] [US1] 编写模块讲解 `template/.github/chefs-pick/GUIDE.md`（双语）
  - 读取：
    - contracts/guidance-layer.md §0、§3（包括模块要点表和 6 个附加章节）；
    - contracts/template-layout.md §6；
    - contracts/markers.md §3；
    - research.md R11、R14、R15、R17。
  - 验收：
    - `python3 tools/check_template.py --only C11,C21 --files .github/chefs-pick/GUIDE.md` 全部 PASS；
    - C17 和相对链接检查都在 T032 中复核。
- [X] T030 [P] [US1] 编写模板自身的 `template/.github/chefs-pick/CHANGELOG.md` 和 `template/.github/chefs-pick/LICENSE`
  - 读取：contracts/guidance-layer.md §7（逐字）、§8；contracts/project-files.md 的 M02（许可证正文的获取方法）
  - 做法：
    1. 许可证正文用 T017 中的 `gh api` 命令获取，并同样删除 front matter。
    2. 把第 3 行改为 `Copyright (c) 2026 Chef's Pick OSS Starter contributors`。
    3. 按 §8 在正文后依次追加空行、`---`、空行，以及英文和中文两段附注。
  - 验收：`python3 tools/check_template.py --only C11,C21 --files .github/chefs-pick/CHANGELOG.md,.github/chefs-pick/LICENSE` 全部 PASS
- [X] T031 [P] [US1] 编写模板首页 `template/.github/README.md`（双语；摘要表的数据行和选型清单链接由 T036 补充）
  - 读取：contracts/guidance-layer.md §0、§1；contracts/template-layout.md §3；research.md F3、F9
  - 做法：
    - 第 3 节"主厨精选一览"在本任务中只写以下内容：该节标题、一行 `<!-- summary:start -->`、摘要表的表头行和分隔行、一行 `<!-- summary:end -->`。
    - 本任务不写 `chefs-pick/SOURCES.md` 链接。
    - 其余各节按 §1 完整写出。
  - 验收：`python3 tools/check_template.py --only C11,C21 --files .github/README.md` 全部 PASS。相对链接由 T032 统一验收
- [X] T032 [US1] 对 `template/` 下 US1 的全部文件和 `tools/tests/` 做集成验收，并按契约修正（依赖 T016 ~ T031）
  - 做法：
    1. 运行 `python3 tools/check_template.py --only C02,C03,C05,C06,C08,C09,C10,C11,C13,C14,C15,C17,C21,C22`。
    2. 运行 `for m in test_checks_layout test_checks_automation test_checks_markers test_checks_identity test_checks_links test_ci_pin_check; do PYTHONPATH=tools/tests python3 -m unittest "$m" || { echo "FAILED: $m"; exit 1; }; done`。只跑这 6 个模块：其他故事的测试要到各自阶段才写。
    3. 如有 FAIL，只能按相应契约章节修改出错的模板文件。不得修改契约，也不得修改检查逻辑来迁就文件。如果确认是检查逻辑有误，停止并报告。
  - 验收：
    - 上述 14 项检查全部 PASS；
    - 6 个测试模块都输出 `OK`，并且 `test_ci_pin_check` 没有被跳过。

**Checkpoint**：US1 可独立验收，这是 MVP 的核心部分。

---

## Phase 4: User Story 2 - 潜在使用者核查每个模块的选型依据 (Priority: P1)

**Goal**：
- 完成 `SOURCES.md` 选型清单；
- 为模板首页补上 16 行摘要表和选型清单链接。

**Independent Test**：
- `python3 tools/check_template.py --only C11,C12,C14,C21` 全部 PASS；
- 发布前按 quickstart 的 C 部分执行 V6。

### Tests for User Story 2

- [X] T033 [P] [US2] 编写 `tools/tests/test_checks_selection.py`，覆盖 C12（依赖 T015，并紧接着执行 T034）
  - 读取：
    - contracts/tooling.md §1.3 的 C12 说明、§3（`test_checks_selection.py` 一行，列出了全部失败用例）；
    - contracts/guidance-layer.md §4.1（"排除的候选"一节的行数要求）、§4.2、§4.3、§4.4（各模块的字段取值，其中"取舍规则的写法"一条说明了 `2` 与 `1 + 2` 的区别）；
    - data-model.md 的"取舍规则的写法"（`2` 与 `1 + 2` 的区别）；
    - data-model.md 中 AdoptionEvidence 的日期规则："任何时候距当天都不超过 183 天；发布时距发布日不超过 30 天"。
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_selection.py'` 能运行，并出现失败（预期的红灯）

### Implementation for User Story 2

- [X] T034 [US2] 在 `tools/check_template.py` 中实现 C12（依赖 T033、T015）
  - 读取：同 T033。C12 的完整定义见 tooling §1.3，实现时特别注意其中这几条：入选理由与 Rationale 段落非空、备选方案至少一项、证据格含双语证据类型标签、首页摘要表 16 行且依次以 M01 ~ M16 开头、只有四处日期参与新鲜度检查（`Last commit` 列不参与）、有"排除的候选"一节且表格至少 8 行且每行 3 格非空、取舍规则恰好为 `2` 的模块入选理由含"认可度相当"（`1 + 2` 不受此约束）
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_selection.py'` 全部通过
- [X] T035 [P] [US2] 编写选型清单 `template/.github/chefs-pick/SOURCES.md`（双语；依赖 Phase 2）
  - 读取：
    - contracts/guidance-layer.md §0、§4（§4.1 ~ §4.4 全部）；
    - research.md：§1 的数据表及"许可证列的两种口径"、R4 ~ R21（入选理由、备选方案、排除理由）；
    - data-model.md："证据类型"的 6 种写法、"模块目录"。
  - 数据：
    - 所有核实日期一律写 `2026-09-18`；
    - 认可度数据表按 guidance-layer §4.3 写 36 行，Stars、Forks、`Last commit`、Archived 列取自 research §1。`Last commit` 是默认分支最近一次提交的日期，不是 `pushed_at`；
    - License 列只写 API 返回的 SPDX 标识，按 research §1 的规定，其中 7 个仓库写 `unknown`；
    - 各模块的字段取值见 guidance-layer §4.4，照抄即可，证据类型的双语标签已经写在那张表里；
    - 维护说明只写文件名 `MAINTAINING.md`（行内代码），不要写成链接：它由 T044 创建，写成链接会让 T036 的链接检查失败。
  - 验收：
    - `python3 tools/check_template.py --only C11,C14,C21 --files .github/chefs-pick/SOURCES.md` 全部 PASS；
    - `grep -c '^### M' template/.github/chefs-pick/SOURCES.md` 输出 `16`；
    - `awk '/adoption-data:start/{f=1;next}/adoption-data:end/{f=0}f' template/.github/chefs-pick/SOURCES.md | grep -c '^| [A-Za-z0-9_.-]*/'` 输出 `36`。
- [X] T036 [US2] 在 `template/.github/README.md` 中补上摘要表的数据行和选型清单链接（依赖 T031、T034、T035）
  - 读取：contracts/guidance-layer.md §1 第 3 节、§4.5（16 行逐字内容）
  - 做法：
    - 在两个 summary 标记之间的表头下方，照抄 §4.5 给出的 16 行，核实日期写 `2026-09-18`；
    - 认可度列中的 Star 数必须与 `SOURCES.md` 数据表中的当前值一致；
    - 在表格后面加上 `[完整选型清单 / Full selection list](chefs-pick/SOURCES.md)`。
  - 验收：`python3 tools/check_template.py --only C11,C12,C14,C21` 全部 PASS

**Checkpoint**：US1 和 US2 都已完成，首个版本的必需内容已经齐备。

---

## Phase 5: User Story 3 - 生成仓库的外部贡献者获得清晰的参与路径 (Priority: P2)

**Goal**：验证并保证面向贡献者的内容质量，涉及 Issue 表单、合并请求模板、安全策略、贡献指南、行为准则和发布说明分类。

**Independent Test**：
- `python3 tools/check_template.py --only C04,C07,C16,C20` 全部 PASS；
- 发布前按 quickstart 的 C 部分执行 V3、V5、V8、V9。

### Tests for User Story 3

- [X] T037 [P] [US3] 编写 `tools/tests/test_checks_contributor.py`，覆盖 C04、C07、C16、C20（依赖 T015，并紧接着执行 T038）
  - 读取：
    - contracts/tooling.md §1.3（C04、C07、C16 所在行，以及 C20 的说明）、§3；
    - contracts/project-files.md 的 M04、M05、M06、M07、M08、M09。
  - 要求：失败用例至少包括以下几种：
    - C04：`bug_report` 的 `steps` 不是必填；`config.yml` 中 `blank_issues_enabled: true`。
    - C07：分类的顺序不对。
    - C16：仍残留 `[INSERT CONTACT METHOD]`。
    - C20：SECURITY 缺少加粗的警示句；PR 模板只有 2 个清单项。
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_contributor.py'` 能运行，并出现失败（预期的红灯）

### Implementation for User Story 3

- [X] T038 [US3] 在 `tools/check_template.py` 中实现 C04、C07、C16、C20（依赖 T037、T034）
  - 读取：同 T037
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_contributor.py'` 全部通过
- [X] T039 [US3] 验收并修正协作入口文件，包括 `template/.github/ISSUE_TEMPLATE/`、`template/SECURITY.md`、`template/CONTRIBUTING.md` 等（依赖 T038、T032）
  - 做法：
    - 运行 `python3 tools/check_template.py --only C04,C07,C16,C20`。
    - 如有 FAIL，只能按 contracts/project-files.md 的 M04 ~ M09 和 M01 修改以下文件：
      - `template/.github/ISSUE_TEMPLATE/bug_report.yml`
      - `template/.github/ISSUE_TEMPLATE/feature_request.yml`
      - `template/.github/ISSUE_TEMPLATE/config.yml`
      - `template/.github/PULL_REQUEST_TEMPLATE.md`
      - `template/SECURITY.md`
      - `template/CONTRIBUTING.md`
      - `template/CODE_OF_CONDUCT.md`
      - `template/.github/release.yml`
      - `template/README.md`
  - 验收：
    - 这 4 项检查全部 PASS；
    - `python3 tools/check_template.py --only C08,C09,C14,C21` 仍然全部 PASS。

**Checkpoint**：外部贡献者的参与路径已经可以独立验收。

---

## Phase 6: User Story 4 - 模板维护者复核认可度数据并更新选型 (Priority: P3)

**Goal**：
- 提供数据刷新工具 `tools/verify_sources.py` 和维护说明 `MAINTAINING.md`；
- 完成一次数据刷新。

**Independent Test**：
- `python3 -m unittest discover -s tools/tests -p 'test_verify_sources.py'` 通过；
- `python3 tools/check_template.py --only C12,C18` 全部 PASS；
- 执行 quickstart 的 V11。

### Tests for User Story 4

- [X] T040 [P] [US4] 编写 `tools/tests/test_verify_sources.py`（依赖 T015，并紧接着执行 T042）
  - 读取：contracts/tooling.md §2（全部）、§3（`test_verify_sources.py` 一行）
  - 要求：
    - 通过 mock `fetch_repo` 模拟网络请求，测试中不访问网络；
    - 退出码 2 的用例 mock `gh_ready` 返回 `False`（也可以另写一个 mock `shutil.which` 返回 `None` 的用例）；
    - 其余用例都要 mock `gh_ready` 返回 `True`，否则测试会真的去执行 `gh auth status`。
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_verify_sources.py'` 能运行，并因 `verify_sources` 尚不存在而失败（预期的红灯）
- [X] T041 [P] [US4] 编写 `tools/tests/test_checks_maintaining.py`，覆盖 C18（依赖 T015，并紧接着执行 T043）
  - 读取：contracts/tooling.md §1.3 的 C18 行、§3；contracts/guidance-layer.md §5
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_maintaining.py'` 能运行，并出现失败（预期的红灯）

### Implementation for User Story 4

- [X] T042 [US4] 编写 `tools/verify_sources.py`（依赖 T040）
  - 读取：contracts/tooling.md §2；contracts/guidance-layer.md §0（Star 数写法）、§1 第 3 节（首页摘要表的日期列）、§4.1（"数据核实日期"一行）、§4.2（模块字段表的核实日期）、§4.3
  - 要点：`fetch_repo` 取默认分支最近一次提交的日期，不用 `pushed_at`；`gh_ready()` 单独成函数，便于测试 mock；只有全部仓库查询成功时才写入
  - 验收：
    - `python3 -m unittest discover -s tools/tests -p 'test_verify_sources.py'` 全部通过；
    - `python3 tools/verify_sources.py --help` 的退出码为 0。
- [X] T043 [US4] 在 `tools/check_template.py` 中实现 C18（依赖 T041、T038）
  - 读取：contracts/tooling.md §1.3 的 C18 行（6 个二级标题，含 `Action updates`）；contracts/guidance-layer.md §5
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_maintaining.py'` 全部通过
- [X] T044 [US4] 编写维护说明 `template/.github/chefs-pick/MAINTAINING.md`（双语；依赖 T043，以及 US1 的 T030）
  - 读取：
    - contracts/guidance-layer.md §0、§5；
    - 宪章 `.specify/memory/constitution.md` 的原则 III 和"发布门禁"（只读，用于照抄 3 个触发条件和 5 项门禁）。
  - 要求：
    - `tools/` 相关的命令只能写成行内代码，不得写成链接；
    - 触发条件照抄宪章原则 III 的 3 条，并写明"末次提交"以默认分支最近一次提交为准、已归档视同满足第 1 条；
    - 必须包含"动作版本更新 / Action updates"一节，说明模板仓库上的 Dependabot 合并请求不要直接合并；
    - 发布门禁一节写明：5 项门禁都在创建 Release 之前完成，其中门禁 2 的"首次 CI 通过"和门禁 4 用测试仓库人工验证
  - 验收：`python3 tools/check_template.py --only C11,C14,C18,C21 --files .github/chefs-pick/MAINTAINING.md` 全部 PASS
- [X] T045 [US4] 刷新 `template/.github/chefs-pick/SOURCES.md` 和 `template/.github/README.md` 中的认可度数据（依赖 T042、T036）
  - 做法：
    1. 运行 `gh auth status`，确认已经登录。
    2. 运行 `python3 tools/verify_sources.py`（只读），查看报告。
    3. 运行 `python3 tools/verify_sources.py --write`。
    4. 复核非仓库证据：用 `gh api "repos/EthicalSource/contributor_covenant/contents/assets/adopters.csv?ref=release" --jq .content | base64 -d | tail -n +2 | wc -l` 重新统计 Contributor Covenant 的采用者数量。与 SOURCES 中 M04 的数字不同时，同步更新 M04 的证据和首页摘要表里出现的该数字。
  - 规则：
    - M01 ~ M16 的"选定来源"，指各模块"认可度证据"中第一个 `★` 对应的仓库。
    - `STALE` 按默认分支最近提交判断，不看 `pushed_at`；
    - 如果某个选定来源出现 `ARCHIVED`、`RENAMED`，或出现 research §5 尚未记录的 `STALE` 标志：不得修改选型，也不要执行第 3 步；停止，并把报告交给协调者。按宪章原则 III，由维护者重新评估。
    - `editorconfig/editorconfig` 的 `STALE` 标志已在 research §5 中评估过，可以忽略。
    - 备选方案和排除清单中的仓库出现标志时，不影响本任务。
  - 验收：
    - `python3 tools/check_template.py --only C12` 结果为 PASS；
    - `grep -c "Data verified: $(date +%F)" template/.github/chefs-pick/SOURCES.md` 输出 `1`。

**Checkpoint**：维护流程可以独立运行，数据已刷新。

---

## Phase 7: User Story 5 - 项目发展为多人协作后获得简要的升级指引 (Priority: P4，可选)

**Goal**：提供团队升级指引 `UPGRADE-TO-TEAM.md`。这一阶段可以不做，不影响本期验收，此时 C19 会显示为 SKIP。

**Independent Test**：`python3 tools/check_template.py --only C11,C12,C14,C19,C21` 全部 PASS

### Tests for User Story 5

- [X] T046 [P] [US5] 编写 `tools/tests/test_checks_upgrade.py`，覆盖 C19（依赖 T015，并紧接着执行 T047；决定不做 US5 时不要创建这个文件）
  - 读取：contracts/tooling.md §1.3 的 C19 行、§3；contracts/guidance-layer.md §6
  - 要求：覆盖通过、失败和文件不存在时 SKIP 三种情况
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_upgrade.py'` 能运行，并出现失败（预期的红灯）

### Implementation for User Story 5

- [X] T047 [US5] 在 `tools/check_template.py` 中实现 C19（依赖 T046、T043）
  - 读取：同 T046（contracts/tooling.md §1.3 的 C19 行；contracts/guidance-layer.md §6 的三个二级标题）
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_checks_upgrade.py'` 全部通过
- [X] T048 [US5] 编写团队升级指引 `template/.github/chefs-pick/UPGRADE-TO-TEAM.md`（双语；依赖 T047，以及 US2 的 T035、T036，若同时实施 US4，还依赖 T045）
  - 读取：contracts/guidance-layer.md §0、§6；research.md R20；contracts/markers.md §2.2（CODEOWNERS 来源注释里的链接）、§3（规则集链接）
  - 数据：Star 数一律取自 `template/.github/chefs-pick/SOURCES.md` 认可度数据表的**当前值**，不使用 research 中的数字，因为这些数字可能已经刷新。本页涉及 `renovatebot/renovate`、`pre-commit/pre-commit`、`ossf/scorecard`、`cncf/project-template`、`microsoft/repo-templates`、`ossf/best-practices-badge`、`todogroup/repolinter`（"不再推荐"一节用它），这 7 个仓库都已在数据表中
  - 链接：表格"来源 / Source"一列按 guidance-layer §6 的"来源 / Source 一列的取值"填写，不得自行编造 URL。
  - 另一处改动：在 `template/.github/README.md` 的"快速开始"一节末尾加一行链接，内容见 guidance-layer §6 的"首页链接"。不实施 US5 时不要加这一行。
  - 验收：`python3 tools/check_template.py --only C11,C12,C14,C19,C21` 全部 PASS

**Checkpoint**：所有用户故事完成。

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**：全量校验、链接检查、发布门禁演练。

- [X] T049 编写 `tools/tests/test_real_template.py`（依赖 T032、T039、T044、T045；实施 US5 时还依赖 T047、T048）
  - 读取：contracts/tooling.md §3（`test_real_template.py` 一行）
  - 验收：`python3 -m unittest discover -s tools/tests -p 'test_real_template.py'` 通过，而且没有被跳过
- [X] T050 用 `tools/check_template.py` 对 `template/` 做全量校验（依赖 T049）
  - 做法：
    1. 运行 `python3 tools/check_template.py` 和 `python3 -m unittest discover -s tools/tests`。
    2. 如果 C01 报告有多余文件，先报告协调者，不要自行删除；如果报告缺少文件，回到对应任务补上。
    3. 运行 `time python3 tools/check_template.py`，记录耗时。
  - 验收：
    - check_template 的最后一行为 `Summary: 22 passed, 0 failed, 0 skipped`；未实施 US5 时为 `Summary: 21 passed, 0 failed, 1 skipped`。此时 C19 的 SKIP 原因有两种正常情况：T046 ~ T048 都没做时是 T004 留下的 `not implemented`；做了 T046、T047 而没做 T048 时是"文件不存在"。但 `template/.github/chefs-pick/UPGRADE-TO-TEAM.md` 已经存在时，C19 不得为 SKIP；
    - unittest 输出 `OK`；
    - 校验耗时不超过 5 秒（plan 的 Performance Goals）。
- [X] T051 [P] 检查 `template/` 中所有外部链接能否访问（依赖 T050）
  - 做法：
    1. 用 ``grep -rhoE 'https://[^][ )>"`，。；：、）]+' template | sed 's/[.,;:]$//' | grep -v CHANGEME_ | grep -v 'example\.com' | sort -u`` 提取链接。字符类同时排除 ASCII 方括号和中文全角标点：排除方括号是因为会把行为准则中形如 `[FAQ]` 的链接引用一起截进来，排除全角标点是因为双语正文里的 `。`、`）`、`，` 会被带进链接，导致 `curl` 报 `000`。`sed` 再去掉末尾的 ASCII 标点（提取结果确实会带上句末标点，例如 `https://editorconfig.org.`），去重必须放在最后一步，否则同一链接的带标点和不带标点两种形式都会保留。`example.com` 是 FUNDING 注释里的示例域名，按 RFC 2606 保留，不参与检查。
    2. 对每个链接运行 `curl -sS -o /dev/null -L --max-time 30 -w '%{http_code}'`。
  - 规则：返回值不是 `200` 的链接，要报告给协调者，不得自行替换来源或删除链接
  - 验收：所有链接都返回 `200`，或者已向协调者报告返回值不是 `200` 的链接
- [X] T052 [P] 核对 `template/` 中的文件清单（依赖 T050）
  - 做法：运行 `find template -type f ! -name .DS_Store | sort`，与 contracts/template-layout.md §2 对照
  - 验收：
    - 清单共 26 个文件，未实施 US5 时为 25 个；
    - `find template \( -name .specify -o -name .claude -o -name specs -o -name tools -o -name .git -o -name __pycache__ \)` 没有输出。
- [X] T053 用 `tools/check_template.py --release` 对 `template/` 做发布门禁演练（依赖 T050、T045）
  - 做法：
    1. 运行 `python3 tools/check_template.py --release`。如果失败的原因是核实日期早于 30 天前，先按 T045 的步骤刷新数据，然后重跑。
    2. 把以下内容汇总给协调者：本次运行结果；quickstart.md 的 B、C、D 三部分中需要维护者手动完成的步骤清单，并标明 C 部分的 V1、V4 对应发布门禁 2 和 4，必须在创建 Release 之前完成。
  - 规则：不得执行任何发布操作
  - 验收：`python3 tools/check_template.py --release` 的结果为 0 项失败

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup（Phase 1）**：不依赖其他阶段。T002 和 T003 在 T001 之后，两者可以并行。
- **Foundational（Phase 2）**：依赖 Setup，阻塞所有用户故事。
  - 顺序：T004 → T005 → T006 ~ T010（可并行）→ T011 → T012 → T013 → T014 → T015。
- **US1（Phase 3）**：依赖 Phase 2。
  - T016 ~ T031 可以并行；T016 还依赖 T003。
  - T032 在 T016 ~ T031 全部完成后执行。
- **US2（Phase 4）**：依赖 Phase 2。
  - T033 紧接在 T034 之前执行，不要提前写测试。
  - T036 依赖 US1 的 T031，因为它要在首页文件里补内容。
  - T034 必须排在 T015 之后，因为两者修改同一个文件。
- **US3（Phase 5）**：依赖 Phase 2。
  - T037 紧接在 T038 之前执行。
  - T039 验收的是 US1 生成的文件，因此依赖 T032。
  - T038 必须排在 T034 之后，因为两者修改同一个文件。
- **US4（Phase 6）**：依赖 Phase 2；T044 还依赖 US1 的 T030，因为 MAINTAINING 要链接 `chefs-pick/CHANGELOG.md`，C14 才能通过。
  - T040 紧接在 T042 之前执行，T041 紧接在 T043 之前执行。
  - T045 依赖 US2 的 T036 和本阶段的 T042。
  - T043 必须排在 T038 之后，因为两者修改同一个文件。
- **US5（Phase 7，可选）**：依赖 Phase 2；T048 还依赖 US2 的 T035、T036，因为本页的 Star 数取自 `SOURCES.md`，验收又要跑 C12。
  - T046 紧接在 T047 之前执行；决定不做 US5 时，这两个任务都不做，C19 会一直显示 SKIP。
  - T047 必须排在 T043 之后，因为两者修改同一个文件。
  - 如果同时实施 US4，T048 在 T045 之后执行，这样 Star 数取的是刷新后的值。
- **Polish（Phase 8）**：依赖所有要实施的用户故事。T049 在 T044、T045（以及实施 US5 时的 T047、T048）之后执行。

### User Story Dependencies

- **US1（P1）**：没有其他故事依赖，是 MVP 的核心。
- **US2（P1）**：需要 US1 生成的首页文件（T031）。校验子集（C12）独立。
- **US3（P2）**：验收的是 US1 生成的协作文件。校验子集（C04、C07、C16、C20）独立。
- **US4（P3）**：数据刷新需要 US2 生成的选型清单。校验子集（C18）和工具测试独立。
- **US5（P4，可选）**：只需要 US2 的数据表提供 Star 数；可以不做。

### Within Each User Story

- 测试任务先写，并确认失败（红灯），然后才实现检查项，最后用检查项验收模板文件。测试任务与它对应的实现任务要连着做，中间不要插入其他阶段的验收。
- 按"检查项 → 模板文件 → 集成验收"的顺序推进。
- `tools/check_template.py` 的修改顺序固定为：T004 → T011 → T012 → T013 → T014 → T015 → T034 → T038 → T043 → T047。

### Parallel Opportunities

- Phase 1：T002 和 T003 可以并行。
- Phase 2：T006 ~ T010 这 5 个测试文件可以并行。
- US1：T016 ~ T031 这 16 个任务修改的文件互不重叠，可以全部并行。
- 各故事的测试文件（T033、T037、T040、T041、T046）必须紧接在各自的实现任务之前编写，不要提前：它们写完后处于失败状态，会让阶段性的全量测试运行失败。
- US2 的 T035 可以与 US1 的文件任务并行。
- Polish：T051 和 T052 可以并行。

---

## Parallel Example: Phase 2 测试

```bash
# T005 完成后，同时派发 5 个子代理：
Task: "T006 编写 tools/tests/test_checks_layout.py（C01、C02、C03、C21）"
Task: "T007 编写 tools/tests/test_checks_automation.py（C05、C06）"
Task: "T008 编写 tools/tests/test_checks_markers.py（C08、C09）"
Task: "T009 编写 tools/tests/test_checks_identity.py（C10、C11）"
Task: "T010 编写 tools/tests/test_checks_links.py（C13、C14、C15、C17、C22）"
```

## Parallel Example: User Story 1

```bash
# T015 完成后，同时派发以下子代理（每个任务修改的文件互不重叠）：
Task: "T016 编写 tools/tests/test_ci_pin_check.py"
Task: "T017 生成 template/LICENSE"
Task: "T018 生成 template/.gitignore"
Task: "T019 编写 template/README.md"
Task: "T020 生成 template/CODE_OF_CONDUCT.md"
Task: "T021 编写 template/CONTRIBUTING.md"
Task: "T022 编写 template/SECURITY.md"
Task: "T023 创建 template/.github/ISSUE_TEMPLATE/ 下的 3 个表单"
Task: "T024 创建 template/.github/workflows/ci.yml"
Task: "T025 创建 template/.github/dependabot.yml"
Task: "T026 创建 CHANGELOG.md、release.yml、PULL_REQUEST_TEMPLATE.md"
Task: "T027 创建 4 个可选模块文件"
Task: "T028 编写 template/.github/chefs-pick/SETUP.md"
Task: "T029 编写 template/.github/chefs-pick/GUIDE.md"
Task: "T030 编写模板自身的 CHANGELOG 与 LICENSE"
Task: "T031 编写 template/.github/README.md"
# 以上全部完成后，再执行 T032 做集成验收
```

---

## Implementation Strategy

### MVP First

1. 完成 Phase 1 和 Phase 2，得到校验框架。
2. 完成 Phase 3（US1），然后**停下来验收**：运行 US1 的独立测试。
3. 完成 Phase 4（US2）。spec 规定 US1 和 US2 都必须在首个版本中交付，因此首个可发布版本等于 US1 加 US2。

### Incremental Delivery

1. Setup + Foundational → 校验框架就绪。
2. US1 → 起步模板可用，可以独立验收。
3. US2 → 选型依据齐全，达到首个版本的最低发布线。
4. US3 → 协作入口的质量经过检查。
5. US4 → 数据刷新；发布前必须完成，因为发布门禁要求数据在 30 天内核实过。
6. US5（可选）→ 团队升级指引。
7. Polish → 全量校验、链接检查、发布门禁演练；之后由维护者按 quickstart 手动发布。

### 协调者（Opus）的调度建议

- 每个子代理只派发一个任务，并在任务说明中附上本文件的"路径与执行约定"一节。
- 并行任务完成后，协调者统一运行该阶段 Checkpoint 中列出的命令。
- 子代理报告"停止"时，协调者必须先判断属于哪种情况：契约问题、上游变化，还是需要维护者决策。判断清楚后再继续，不得让子代理自行调整选型。

---

## Notes

- 任务编号表示执行顺序；[P] 表示修改的文件互不重叠，可以并行。
- [Story] 标签用于把任务追溯到 spec.md 中的用户故事。
- 不提交代码：本仓库尚未初始化 Git，提交和发布都由维护者手动完成（见 quickstart.md 的 B 部分）。
- 避免：含糊的任务、多个任务同时修改同一文件、让子代理自行做选型判断。
