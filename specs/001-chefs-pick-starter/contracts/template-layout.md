# 契约：目录布局与起步引导层

对应需求：FR-001、FR-002、FR-003、FR-010、FR-011、FR-012、FR-013；宪章原则 IV、V。决策依据：[research.md](../research.md) R1、R2。

## 1. 两个根目录

| 目录 | 作用 | 是否发布 |
|---|---|---|
| 开发工作区根目录 `./` | Spec Kit（`.specify/`、`.claude/`、`specs/`）、维护工具 `tools/`，以及开发工作区自用的 `.gitignore` | 否 |
| `template/` | 公开模板仓库默认分支 `main` 上的全部内容 | 是，只发布这个目录的内容 |

`template/` 下**禁止**出现以下内容（C02 检查）：`.specify/`、`.claude/`、`specs/`、`tools/`、`.git/`、`__pycache__/`、`*.pyc`、`node_modules/`。

macOS 生成的 `.DS_Store` 由所有检查统一忽略，不作为问题报告：模板自带的 `.gitignore` 已经排除它，发布时不会被提交。

## 2. `template/` 的完整文件清单

"必须存在"一列为"是"的文件由 C01 检查。

| 路径（相对 `template/`） | 模块 | 级别 | 必须存在 | 所属层 |
|---|---|---|---|---|
| `README.md` | M01 | 必需 | 是 | 项目文件 |
| `LICENSE` | M02 | 必需 | 是 | 项目文件 |
| `.gitignore` | M03 | 必需 | 是 | 项目文件 |
| `CODE_OF_CONDUCT.md` | M04 | 推荐 | 是 | 项目文件 |
| `CONTRIBUTING.md` | M05 | 推荐 | 是 | 项目文件 |
| `SECURITY.md` | M06 | 推荐 | 是 | 项目文件 |
| `.github/ISSUE_TEMPLATE/bug_report.yml` | M07 | 推荐 | 是 | 项目文件 |
| `.github/ISSUE_TEMPLATE/feature_request.yml` | M07 | 推荐 | 是 | 项目文件 |
| `.github/ISSUE_TEMPLATE/config.yml` | M07 | 推荐 | 是 | 项目文件 |
| `.github/PULL_REQUEST_TEMPLATE.md` | M08 | 推荐 | 是 | 项目文件 |
| `CHANGELOG.md` | M09 | 推荐 | 是 | 项目文件 |
| `.github/release.yml` | M09 | 推荐 | 是 | 项目文件 |
| `.github/workflows/ci.yml` | M11 | 推荐 | 是 | 项目文件 |
| `.github/dependabot.yml` | M12 | 推荐 | 是 | 项目文件 |
| `.editorconfig` | M13 | 可选 | 是 | 项目文件 |
| `.pre-commit-config.yaml` | M14 | 可选 | 是 | 项目文件 |
| `.github/CODEOWNERS` | M15 | 可选 | 是 | 项目文件 |
| `.github/FUNDING.yml` | M16 | 可选 | 是 | 项目文件 |
| `.github/README.md` | — | — | 是 | 起步引导层（英文规范版本） |
| `.github/README.zh-CN.md` | — | — | 是 | 起步引导层（中文译本，功能 002 新增） |
| `.github/chefs-pick/SETUP.md` | — | — | 是 | 起步引导层（英文规范版本） |
| `.github/chefs-pick/SETUP.zh-CN.md` | — | — | 是 | 起步引导层（中文译本，功能 002 新增） |
| `.github/chefs-pick/GUIDE.md` | — | — | 是 | 起步引导层 |
| `.github/chefs-pick/SOURCES.md` | — | — | 是 | 起步引导层 |
| `.github/chefs-pick/MAINTAINING.md` | — | — | 是 | 起步引导层 |
| `.github/chefs-pick/CHANGELOG.md` | — | — | 是 | 起步引导层 |
| `.github/chefs-pick/LICENSE` | — | — | 是 | 起步引导层 |
| `.github/chefs-pick/UPGRADE-TO-TEAM.md` | — | — | 否（P4，可选） | 起步引导层 |

`template/` 下不得出现上表以外的文件（C01 检查）。

## 3. 起步引导层

- **定义**：起步引导层恰好由 `template/.github/README.md`、它在同目录下的各语言译本（形如 `README.<lang>.md`）和 `template/.github/chefs-pick/` 目录下的全部文件组成。其余文件统称"项目文件"。译本必须计入引导层，否则会被当作项目文件，导致"项目文件不得含中文""项目文件不得链接进引导层"等检查误报。
- **首页展示**：GitHub 优先展示 `.github/README.md`（research F1），所以模板仓库首页和刚生成的仓库首页显示的都是它；根目录的 `README.md` 是项目骨架。
- **清理命令**：唯一的清理命令是 `git rm -r .github/README.md .github/README.zh-CN.md .github/chefs-pick`，之后提交即可。首页的译本在 `chefs-pick/` 之外，必须显式列出；仍然只有一条命令。在网页上操作时，删除这个文件和这个目录即可。
- **清理后必须满足以下条件**（C13 检查）：
  1. `.github/README.md`、`.github/README.zh-CN.md` 和 `.github/chefs-pick/` 都不存在，根目录的 `README.md` 成为首页。
  2. 其余文件中不出现 `chefs-pick/` 或 `.github/README.md` 字样，也没有指向它们的链接。
  3. 其余文件中没有模板身份字样：正则 `(?i)chef'?s[ -]?pick` 或 `主厨精选` 都没有匹配。
  4. 占位符仍然只有登记表中的 `CHANGEME_*`（见 [markers.md](./markers.md)）。

## 4. 模板身份隔离（C10 检查）

- 模板身份字样（见上面的正则）只允许出现在起步引导层中。
- 项目文件中不得出现以下内容：模板作者的姓名、联系方式或赞助链接；模板自身的版本号或变更历史。
- 根目录 `CHANGELOG.md` 只能有一个二级标题 `## [Unreleased]`。

## 5. 通用文件格式

- 编码 UTF-8、换行符 LF、文件末尾保留一个换行、行尾不留空格或制表符（C21 检查）。本项目不使用 Markdown 的"行尾两个空格"换行写法。另外，`.gitignore` 的上游 macOS 规则中，`Icon[\r]` 和 `.HFS+ Private Directory Data[\r]` 两行的方括号里各有一个字面的回车符。这是上游有意写的，必须原样保留，它们不是 CRLF 换行。
- 默认分支名固定为 `main`。从模板生成的仓库沿用这个分支名（research F6、R12）。
- 项目文件中的相对链接只能指向项目文件；起步引导层可以链接项目文件，反向不行。

## 6. 删除模块的影响（FR-013，C17 检查）

GUIDE.md 中每个推荐或可选模块的"如何删除 / Remove"小节，必须列出所有引用了该模块文件名的其他项目文件，并说明需要同步修改的地方。C17 检查文档是否写全，C22 用删除模拟验证删除后其余模块仍然可用。按本契约的内容，至少包括：

| 模块 | 引用它的项目文件 |
|---|---|
| M04 `CODE_OF_CONDUCT.md` | `README.md`、`CONTRIBUTING.md` |
| M05 `CONTRIBUTING.md` | `README.md` |
| M06 `SECURITY.md` | `README.md`、`CONTRIBUTING.md` |
| M07 `bug_report.yml`、`feature_request.yml` | `README.md`（Report a bug 和 Request a feature 链接） |
| M09 `CHANGELOG.md` | `CONTRIBUTING.md`、`.github/PULL_REQUEST_TEMPLATE.md` |
| M11 `ci.yml` | `README.md`（CI 徽章） |

M08、M12、M13、M14、M15、M16 没有被其他项目文件引用，但 GUIDE 仍须写明删除方法和对应功能消失后的影响。
