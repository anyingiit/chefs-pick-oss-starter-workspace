# 维护说明 / Maintaining the template

本页写给模板的维护者，说明认可度数据多久复核一次、怎样复核、什么情况下必须重新评估一个模块、动作的固定版本怎样更新、选型变更怎样记录，以及发布前必须逐项通过的门禁。使用模板的人不需要读这一页：起步请看 [起步清单 / Setup checklist](SETUP.md)，每个模块选了什么、凭什么选，见 [选型清单 / Selection list](SOURCES.md)。

This page is for the maintainers of the template. It covers how often the adoption data is re-checked, how to re-check it, when a module must be re-evaluated, how pinned action versions are updated, how selection changes are recorded, and the gates that must pass before every release. People who merely use the template do not need this page: start from the [Setup checklist](SETUP.md), and see the [Selection list](SOURCES.md) for what was picked and why.

本页提到的 `tools/` 命令都在模板的开发工作区中运行。`tools/` 目录不随模板发布，模板仓库里没有这个目录，所以这些命令一律写成行内代码，不写成链接。

The `tools/` commands mentioned on this page run in the development workspace of the template. The `tools/` directory is not shipped with the template and does not exist in the template repository, so those commands are always written as inline code and never as links.

## 复核周期 / Review cadence

- 认可度数据至少每 6 个月复核一次。
- 每次发布前也必须复核一次，不论距上次复核多久。
- 发布时，所有数据的核实日期都不得早于发布前 30 天；超过 30 天就先复核、刷新日期，再发布。

The adoption data is re-checked at least once every 6 months, and again before every release regardless of when the last review happened. At release time no verification date may be older than 30 days; if any date is older, refresh the data first and release afterwards.

## 复核步骤 / How to review

1. **刷新仓库数据 / Refresh the repository data.** 在开发工作区运行 `python3 tools/verify_sources.py --write`。`tools/` 不在模板仓库中，只有开发工作区才有这个脚本。手边没有开发工作区时，对认可度数据表中的每个仓库手动运行下面两条命令，再把结果填回表中：

   ```bash
   gh api repos/OWNER/REPO --jq '.stargazers_count, .forks_count, .archived, .default_branch'
   gh api repos/OWNER/REPO/commits/DEFAULT_BRANCH --jq .commit.committer.date
   ```

   第二条取的是默认分支最近一次提交的日期。不要用 `pushed_at`：任何分支的推送都会更新它，会让已经停更的上游看起来仍在维护。

2. **手动复核非仓库证据 / Re-check the non-repository evidence by hand.** 逐项确认标为「平台官方功能 / Official platform feature」的能力是否仍然存在、官方文档链接是否仍然有效。Contributor Covenant 的采用者数量用下面的命令重新统计：

   ```bash
   gh api "repos/EthicalSource/contributor_covenant/contents/assets/adopters.csv?ref=release" --jq .content | base64 -d | tail -n +2 | wc -l
   ```

   数量有变化时，同步修改 M04 的认可度证据和首页摘要表中对应的一行。

3. **检查触发条件 / Check the triggers.** 对照下一节，看有没有模块出现了必须重新评估的情况。脚本报告中的 `STALE` 和 `ARCHIVED` 标志直接对应第 1 条触发条件。

4. **更新核实日期 / Update the verification dates.** 受日期约束的共四处：`SOURCES.md` 顶部的数据核实日期行、各模块字段表的「核实日期 / Verified」格、认可度数据表的 `Verified` 列，以及首页摘要表的「核实日期 / Verified」列。`python3 tools/verify_sources.py --write` 会一并更新；手动复核时要四处都改。数据表的 `Last commit` 列记录的是上游的提交日期，不是核实日期，不参与这项约束。

Step 1 refreshes the repository data, with the two `gh api` commands above as the fallback when the development workspace is not at hand. Step 2 re-checks evidence that no API returns: whether each official platform feature still exists, and the Contributor Covenant adopter count, which is recounted with the command above and, when it changes, updated in both the M04 evidence and the summary table on the template home page. Step 3 looks for the re-evaluation triggers below. Step 4 updates the four places that carry a verification date; `Last commit` is an upstream commit date and is not one of them.

## 重新评估的触发条件 / Re-evaluation triggers

出现以下任一情况时，必须重新评估该模块：

1. 上游末次提交超过 12 个月。
2. 依赖已被广泛弃用的工具。
3. 出现认可度明显更高的候选。

判定时注意两点：「末次提交」以默认分支最近一次提交为准，也就是复核步骤第 1 步取到的那个日期，不是 `pushed_at`；仓库已归档视同满足第 1 条，不必再看日期。

重新取舍时按三级规则，顺序不变：先比社区认可度，认可度更高的优先；认可度相当时，选对仓库持有者更容易起步的方案，例如步骤更少、无需额外依赖或由平台内置，并写明判定「认可度相当」的依据；仍然同样合格时，才可以按个人偏好选择，并且必须注明。结论是换掉还是保留，都要在 `SOURCES.md` 中更新该模块的字段、入选理由和备选方案，保留时写明已经重新评估过（例如 M13 的复核说明），并按下面的变更记录规则记一笔。

A module must be re-evaluated when any of these holds: the last upstream commit is more than 12 months old; it depends on a widely deprecated tool; or a clearly better-adopted candidate has appeared. "Last commit" means the most recent commit on the default branch — the date fetched in step 1, never `pushed_at` — and an archived repository counts as meeting the first trigger without further checking. Re-pick with the same three-tier rule: higher community adoption first; when adoption is comparable, the option that is easier to start with (fewer steps, no extra dependency, built into the platform), stating the basis for calling adoption comparable; and only when candidates remain equally qualified may personal preference decide, which must be noted. Whether the pick changes or stands, update the module's fields, rationale and alternatives in `SOURCES.md` — recording that it was re-evaluated when it stands — and record the change as described below.

## 动作版本更新 / Action updates

模板仓库上的 Dependabot 合并请求只当作「有新版本」的提示，**不要直接在模板仓库合并**。模板仓库的内容是从开发工作区单向发布过去的，直接合并会让下一次发布推送被拒绝。

正确做法是回到开发工作区更新，再重新发布：

1. 更新 `template/` 中对应的 40 位提交哈希和行尾的版本注释。
2. 同步更新逐字契约与 research 中记录的固定版本，让它们与 `template/` 一致。
3. 跑完校验，确认没有失败项。
4. 把改动重新发布到模板仓库。模板仓库的内容更新后，对应的 Dependabot 合并请求会自动关闭，不需要手动处理。

Treat a Dependabot pull request on the template repository as a notification that a new version exists, and **do not merge it there**. Publishing to the template repository is one-way, so merging directly makes the next release push fail. Instead, update the pinned hash and the trailing version comment in `template/` in the development workspace, update the pinned versions recorded in the verbatim contracts and in research so they match, run the checks, and publish again. Once the template repository's content is updated, the corresponding pull request closes by itself.

## 变更记录规则 / Recording changes

新增、替换或移除模块时，必须在**同一次改动**中同时更新两个文件：`SOURCES.md` 里该模块的来源、认可度证据、核实日期、入选理由和备选方案，以及 [CHANGELOG.md](CHANGELOG.md) 里 `Unreleased` 节下的一条记录。记录按 Added、Changed、Removed 分类，并写明这样改的原因。只更新其中一个，就会让选型清单和变更记录对不上。

A selection change updates both files in the same commit: the module's source, evidence, verification date, rationale and alternatives in `SOURCES.md`, and an entry under `Unreleased` in [CHANGELOG.md](CHANGELOG.md). Entries go under Added, Changed or Removed and always state the reason for the change. Updating only one of the two leaves the selection list and the changelog out of step.

## 发布门禁 / Release gates

下面 5 项门禁必须**在创建 Release 之前**全部通过，一项不过就不发布：

1. 所有认可度数据的核实日期不早于发布前 30 天。
2. 从模板新生成的仓库核心要素齐全，首次自动检查通过。
3. 占位符能一次搜索全部找到；起步引导层之外没有模板作者身份信息、模板版本历史或开发过程文件；执行清理命令后，起步引导层被完整移除，且没有留下失效的引用。
4. 按起步清单完成定制后，社区标准自检页全部达标。
5. 所有动作引用都已固定到提交哈希，工作流令牌默认只读。

能自动检查的部分，在开发工作区运行 `python3 tools/check_template.py --release`，它会按发布口径校验（核实日期收紧到 30 天）。

其中两项自动检查覆盖不到，必须用从模板生成的测试仓库人工验证：门禁 2 的「首次 CI 通过」，即新生成仓库的第一次自动检查运行成功；以及门禁 4 的社区标准全绿，即按起步清单完成定制后，Insights → Community Standards 各项都是绿勾。这两项的具体步骤见开发工作区中 `quickstart.md` 的 C 部分。

All five gates must pass **before** the Release is created. Run `python3 tools/check_template.py --release` in the development workspace for the parts that can be checked automatically; the `--release` flag tightens the verification dates to 30 days. Two items are out of reach of that command and must be verified by hand in a test repository generated from the template: the first CI run passing on the new repository (gate 2) and every item on Insights → Community Standards showing a green check after the setup checklist has been completed (gate 4). The steps for both are in part C of `quickstart.md` in the development workspace.
