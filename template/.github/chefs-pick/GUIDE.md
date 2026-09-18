# Module guide

This page walks through the 16 modules in the template: why each one is here, how to adapt it to your project, and how to remove it cleanly when you do not want it. Work through the [Setup checklist](SETUP.md) first, then come back here and decide module by module. Which source each module was taken from, and the evidence behind that pick, is recorded in the [Selection list](SOURCES.md).

Before you remove any module, search the repository for its file name (`grep -rn "file-name" .`) to be sure no reference is left behind. The "Remove" section of each module already lists the known referrers.

## M01 README

Files: [`README.md`](../../README.md) · Level: Required

### Why

`README.md` is the first thing a visitor reads, and it is one of the items on the community standards checklist. It decides whether anyone keeps reading.

### Customize

Replace every placeholder in the file (the [Setup checklist](SETUP.md) lists them all), then fill in the About and Usage sections so a reader can tell at a glance what the project does and how to run it. If you switch licenses, update the license name in the License section to match.

### Remove

Not recommended. Without `README.md` the repository front page is just a file listing, the README item on the community standards page never completes, and links from almost every other file point nowhere.

## M02 License

Files: [`LICENSE`](../../LICENSE) · Level: Required

### Why

Without a license nobody may legally use, modify or redistribute your code, even if the repository is public. A license is also one of the few files that cannot be inherited from an account-level default file, so every repository needs its own copy.

### Customize

Fill in the two placeholders for the copyright year and the copyright holder, and leave the rest of the text alone: once the MIT wording is edited, GitHub may stop recognising the license type. To use a different license, see [Changing the license](#changing-the-license) below.

### Remove

Not recommended. Removing it withdraws all permission to use the code, the license badge disappears from the repository page, and the License item on the community standards page stays unchecked.

## M03 Ignore rules

Files: [`.gitignore`](../../.gitignore) · Level: Required

### Why

It keeps the clutter produced by operating systems and editors (macOS, Windows, Linux, Visual Studio Code, JetBrains) out of the repository, where it is tedious to clean up after the fact.

### Customize

The template ships only the language-independent rules. Append the template for your language (Python, Node, Go and so on) from github.com/github/gitignore to the end of the file; see [Adding language-specific rules](#adding-language-specific-rules) below.

### Remove

Not recommended. Without it, build output, dependency directories and files such as `.DS_Store` get committed by accident, and once they are in the history they are hard to remove for good.

## M04 Code of Conduct

Files: [`CODE_OF_CONDUCT.md`](../../CODE_OF_CONDUCT.md) · Level: Recommended

### Why

It states the rules of participation and the reporting channel up front, so that when something goes wrong you have something to point at instead of improvising. It is also one of the community standards items.

### Customize

Fill in the placeholder for the reporting email address; it is the only thing in the file you must change. Projects working in Chinese can link the official Chinese translation, see [Chinese translations](#chinese-translations).

### Remove

Delete `CODE_OF_CONDUCT.md`. `README.md`, `CONTRIBUTING.md` and `.github/PULL_REQUEST_TEMPLATE.md` all reference it, so remove those links and the sentences around them; if you added a link to it in `.github/ISSUE_TEMPLATE/config.yml` or in an issue form, clean that up too. Afterwards the repository no longer advertises a code of conduct, new contributors do not see the rules of participation, and the Code of conduct item on the community standards page becomes incomplete.

## M05 Contributing guide

Files: [`CONTRIBUTING.md`](../../CONTRIBUTING.md) · Level: Recommended

### Why

It answers the question "I want to help, where do I start": how to report a problem, how to submit a change, how to set up a development environment. GitHub links to it from the new issue and new pull request pages.

### Customize

Fill in the real development setup steps and test commands for your project; the Development setup section is the part of the template that most needs your own words. If you do not plan to enable Discussions, point the Questions section at the channel you actually use (this matches step S04 of the setup checklist).

### Remove

Delete `CONTRIBUTING.md`, remove the Contributing link in `README.md`, and clean up any reference to it in `.github/ISSUE_TEMPLATE/config.yml`, in the issue forms (`bug_report.yml`, `feature_request.yml`), and in the checklist in `.github/PULL_REQUEST_TEMPLATE.md`. After that, the prompt linking to contribution guidelines no longer appears when someone opens an issue or a pull request, the process has to be conveyed by `README.md` alone, and the Contributing item on the community standards page becomes incomplete.

## M06 Security policy

Files: [`SECURITY.md`](../../SECURITY.md) · Level: Recommended

### Why

Vulnerabilities must not be reported through public issues. This file gives reporters a private route and states which versions are still supported. The repository's Security tab displays it directly.

### Customize

Fill in the fallback email placeholder, enable private vulnerability reporting as described in step S03 of the setup checklist ([official docs](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)), then adjust the supported versions table to match reality. Until private reporting is enabled the `security/advisories/new` link in the file does not work, which is exactly why the fallback email matters.

### Remove

Delete `SECURITY.md`, then remove the links in `README.md` and rewrite the Reporting security issues section of `CONTRIBUTING.md`, which is built entirely around it. The security link in `.github/ISSUE_TEMPLATE/config.yml` only works once private vulnerability reporting is enabled, so check whether you still want it, and clean up any mention of it in `bug_report.yml`, `feature_request.yml` or `.github/PULL_REQUEST_TEMPLATE.md` too. Afterwards the Security tab has no policy page, reporters have to guess at a private channel, and the Security policy item on the community standards page becomes incomplete.

## M07 Issue forms

Files: [`bug_report.yml`](../ISSUE_TEMPLATE/bug_report.yml), [`feature_request.yml`](../ISSUE_TEMPLATE/feature_request.yml), [`config.yml`](../ISSUE_TEMPLATE/config.yml) · Level: Recommended

### Why

Forms collect the information you always end up asking for (reproduction steps, expected result) as structured fields. `config.yml` turns off blank issues and routes support questions to a suitable channel.

Note: once a repository ships its own valid issue templates, the default issue templates from your account-level `.github` repository stop applying entirely; see [Account-level default files](#account-level-default-files).

### Customize

Add or remove fields as needed, but keep a valid `name` and `description` on every form or the community standards check will not pass. If you change the labels a form applies automatically, update the categories in [`release.yml`](../release.yml) to match, otherwise those entries drop out of the generated release notes.

### Remove

Delete the whole `.github/ISSUE_TEMPLATE/` directory, that is `bug_report.yml`, `feature_request.yml` and `config.yml` (deleting only the forms and keeping `config.yml` leaves a chooser page with external links and no templates at all). In `README.md`, the Report a bug and Request a feature links use `issues/new?template=...` and will break, so point them at plain `issues/new`; also rewrite the Reporting bugs and Suggesting features sections of `CONTRIBUTING.md` if they reference `bug_report.yml` or `feature_request.yml`. Afterwards blank issues are enabled again, the default issue templates from your account-level `.github` repository take effect again, reports lose their structure and their automatic labels, and the Issue templates item on the community standards page becomes incomplete.

## M08 Pull request template

Files: [`PULL_REQUEST_TEMPLATE.md`](../PULL_REQUEST_TEMPLATE.md) · Level: Recommended

### Why

It pre-fills a short self-check into the description box of every pull request: what changed, which issue it closes, whether it was tested. The round trips it saves during review outweigh the time spent filling it in.

### Customize

Adjust the checklist to the bar your project actually holds; three to five items is plenty, longer lists go unread.

One thing to know: the source comment on the first line travels with the template into the description of every pull request. It is an HTML comment, so it is invisible once rendered, but anyone editing the description sees that line. If you would rather not have it, delete that one line; nothing else in the template depends on it.

### Remove

Delete `.github/PULL_REQUEST_TEMPLATE.md`. In `CONTRIBUTING.md`, the Submitting pull requests section tells contributors to fill in the template, so reword it to match what you actually expect; if `README.md` or the maintenance notes in `CHANGELOG.md` mention the template, adjust those too. Afterwards the pull request description box starts out empty, linking the issue and running the self-check is left to the contributor, and the Pull request template item on the community standards page becomes incomplete.

## M09 Changelog and release notes

Files: [`CHANGELOG.md`](../../CHANGELOG.md), [`release.yml`](../release.yml) · Level: Recommended

### Why

`CHANGELOG.md` follows Keep a Changelog: a history written for humans, where one glance tells you what changed in which version. `release.yml` makes GitHub's automatically generated release notes group entries by category instead of listing pull request titles in one long run. One is written by you, the other is generated; they complement each other.

### Customize

Record changes under `## [Unreleased]` as you go; at release time rename that heading to the version number plus the date and start a fresh Unreleased. The categories in `release.yml` rely on GitHub's default `bug` and `enhancement` labels, so if you switch to your own label scheme, update the `labels` entries in that file as well.

### Remove

You can remove either file on its own: dropping `CHANGELOG.md` leaves you with generated release notes only, dropping `.github/release.yml` leaves you with a hand-written changelog. When you delete `CHANGELOG.md`, update `CONTRIBUTING.md`, which asks contributors to add an entry under Unreleased and links to the file, and `.github/PULL_REQUEST_TEMPLATE.md`, whose checklist includes updating the changelog; remove the link from `README.md` too if there is one. When you delete `.github/release.yml`, check whether the label settings in `bug_report.yml` and `feature_request.yml` still make sense. Without `CHANGELOG.md`, users have to read the commit history to tell versions apart; without `release.yml`, release notes fall back to an uncategorised list of pull requests and the `bug` and `enhancement` labels no longer group anything.

## M10 Changelog automation

Files: none · Level: Optional, recommendation only

### Why

Once a project grows, a hand-written changelog is easy to forget and easy to let drift out of sync with releases. At that point a tool can generate it from commits or from change files.

The template enables nothing and ships no file for this module: for a personal project, the hand-written changelog from M09 plus the platform's generated release notes is enough, and it adds no dependencies.

### How to choose

| Project type | Recommended tool | License | Notes |
|---|---|---|---|
| Node projects | changesets | MIT | A change file per change, aggregated at release time; fits the npm publishing flow |
| Non-Node projects | git-cliff | Apache-2.0 / MIT | A single binary that generates from commit history, tied to no language ecosystem |
| Conventional Commits plus automated release pull requests | release-please | Apache-2.0 | Maintains the version and opens release pull requests for you, but requires disciplined commit messages |

Each of the three is the most widely adopted option in its own ecosystem, so pick by project type rather than trying to rank them. Their adoption figures are recorded in the [Selection list](SOURCES.md).

## M11 Continuous integration

Files: [`ci.yml`](../workflows/ci.yml) · Level: Recommended

### Why

Every push and pull request runs the workflow automatically, so a broken change is caught before it is merged. The `lint` job in the template also checks that every action used in a workflow is pinned to a full commit hash, which is the one supply-chain check that is worth running in any language.

What ships is a skeleton: the `test` job prints a line and exits successfully, so it passes even on an empty repository.

### Customize

Add your project's real lint and test steps (installing dependencies, running tests) at the marked places in the file. Whenever you add a third-party action, pin it as described in [Pinning actions](#pinning-actions), otherwise the `lint` job fails outright.

### Remove

Delete `.github/workflows/ci.yml` (and the whole `.github/workflows/` directory if that was the only workflow). Remove the CI badge at the top of `README.md` that points at this workflow, or it will read "no status" forever, and update `CONTRIBUTING.md` or `.github/PULL_REQUEST_TEMPLATE.md` if either says `ci.yml` must pass. Afterwards nothing checks pushes and pull requests automatically and the hash-pinning check goes away; `.github/dependabot.yml` keeps running but has no workflow file left to update, so it effectively does nothing.

## M12 Dependency updates

Files: [`dependabot.yml`](../dependabot.yml) · Level: Recommended

### Why

Once actions are pinned to a commit hash they stop following upstream, security fixes included. Dependabot checks weekly, opens a pull request when a new version appears, and updates the version comment at the end of the line along with the hash.

### Customize

The template configures only the `github-actions` ecosystem. Add the ones your project uses (`npm`, `pip`, `gomod` and so on); see [Adding language-specific rules](#adding-language-specific-rules).

### Remove

Delete `.github/dependabot.yml`. No other file references it, so nothing else needs changing. Afterwards pinned hashes are never bumped automatically, the actions in `ci.yml` stay on their current versions, and keeping up with security updates becomes a manual chore (the command for looking up a hash is in the next section); the repository's Security tab also stops surfacing dependency update alerts.

## M13 EditorConfig

Files: [`.editorconfig`](../../.editorconfig) · Level: Optional

### Why

It unifies encoding, line endings, indentation and the final newline so that collaborators on different editors produce consistent whitespace, instead of diffs where the whole file appears to have changed. Mainstream editors support it natively or through an official plugin.

This module is on by default: it only affects whitespace handling in your local editor and has no visible effect on GitHub pages or on the collaboration flow, so there is nothing to switch on.

### Customize

The template sets only the general rules (UTF-8, LF, final newline, no trailing whitespace, two-space indentation for YAML). Add per-language indentation, for example four spaces under `[*.py]` or tabs under `[*.go]`.

### Remove

Delete `.editorconfig`. No other file is affected; the only thing to check is whether the Development setup section of `CONTRIBUTING.md` mentions it, in which case drop that sentence. Afterwards every editor falls back to its own defaults and inconsistent indentation and trailing whitespace start slipping into commits.

## M14 Pre-commit hooks

Files: [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) · Level: Optional

### Why

It catches trailing whitespace, missing final newlines, broken YAML, leftover conflict markers and oversized files before the commit is made, which is far quicker than waiting for CI and coming back to fix them.

### Customize

After installing pre-commit, run `pre-commit install` once in the repository; until you do, this file does nothing at all. You can then add language-specific hooks (formatters, linters). The `rev` values are pinned to commit hashes with a `# frozen:` version comment; keep that style when you upgrade.

### Remove

Delete `.pre-commit-config.yaml`; anyone who already ran `pre-commit install` should also run `pre-commit uninstall` to clear the local hook. No other file is affected, though you should drop the installation steps from the Development setup section of `CONTRIBUTING.md` if they are there. Afterwards formatting problems surface only in CI or in review.

## M15 Code owners

Files: [`CODEOWNERS`](../CODEOWNERS) · Level: Optional

### Why

It makes GitHub request a review from the right person or team automatically whenever a pull request touches a given path, instead of you adding reviewers by hand. For a solo project it adds little; it starts paying off once you have collaborators.

### Customize

Every line in the template is commented out, so nothing is in effect by default. Uncomment a line and put in your own user name or team, for example `* @your-name` to own the whole repository. An owner must have write access, otherwise the rule is silently ignored.

### Remove

Delete `.github/CODEOWNERS`. No other file references it. All you lose is the automatic reviewer request, and since the shipped file is entirely comments there is no functional difference either way. One caveat: if you enabled "require review from Code Owners" in branch protection or a ruleset, that rule will have no owners left to match, so adjust the ruleset as well.

## M16 Funding

Files: [`FUNDING.yml`](../FUNDING.yml) · Level: Optional

### Why

Once it is filled in, a Sponsor button appears on the repository page, giving anyone who wants to support the project an obvious route.

The file is only recognised when it sits in the `.github/` directory.

### Customize

The template keeps only the `github:` and `custom:` keys, both empty, so no Sponsor button appears by default. Filling in either one switches it on: `github:` takes a GitHub user or organization name, `custom:` takes a link to your own funding page. Delete the key you do not need rather than leaving it empty.

### Remove

Delete `.github/FUNDING.yml`. No other file references it. You lose the Sponsor button, but since the shipped values are empty the page looks the same before and after.

## Adding language-specific rules

The template deliberately stays language-neutral. These three places are where you fill in what your project actually uses.

Grab the matching template from github.com/github/gitignore (for example `Python.gitignore` or `Node.gitignore`) and append it to [`.gitignore`](../../.gitignore) with a comment naming the source and language, keeping the general rules that ship with the template. Add the install, lint and test steps for your language at the marked places in [`ci.yml`](../workflows/ci.yml), pinning any new third-party action as described below. Then add an entry under `updates` in [`dependabot.yml`](../dependabot.yml) with `package-ecosystem` set to `npm`, `pip`, `gomod`, `cargo` and so on, `directory` pointing at the folder holding the manifest, and the same weekly schedule.

## Pinning actions

Actions used in a workflow must be pinned to a full 40-character commit hash, never to a tag. Tags can be moved, hashes cannot, and this is the only reliable way to stop a compromised upstream from silently affecting your repository.

```bash
gh api repos/OWNER/ACTION/commits/vX.Y.Z --jq .sha
```

```yaml
uses: owner/action@<40-character hash> # vX.Y.Z
```

Look up the hash for a version with the `gh api` command above, reference the action with the hash plus a trailing version comment, and let Dependabot keep both in sync when it upgrades. The `lint` job in [`ci.yml`](../workflows/ci.yml) scans every workflow file and fails if a single reference is not pinned. The official [secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) has the background.

## Account-level default files

Create a repository named `.github` under your account and put community health files such as `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md` and `SECURITY.md` in it: they then serve as defaults for every repository you own, and a repository's own copy always wins.

Two exceptions are worth remembering. Issue templates are all-or-nothing: as soon as a repository has its own valid issue templates or `config.yml`, the defaults in the account-level `.github/ISSUE_TEMPLATE` stop applying entirely rather than being merged in, and since this template ships M07, every repository generated from it is in that situation. And a license cannot be provided centrally: `LICENSE` is not among the inheritable files, so every repository needs its own.

See the official docs: [Creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).

## 中文译本 / Chinese translations

模板里的协作文件默认用英文，因为开源协作的默认语言是英文，英文版本也最容易被外部贡献者读懂。如果你的项目主要面向中文使用者，可以把这些文件换成官方中文译本，或者在英文正文旁附一条译本链接。

The collaboration files in the template are in English, because English is the default language of open-source collaboration and the version outside contributors are most likely to read. If your project is aimed mainly at Chinese-speaking users, you can replace these files with the official Chinese translations, or link a translation alongside the English text.

| 文件 / File | 官方中文译本 / Official Chinese translation |
|---|---|
| `CODE_OF_CONDUCT.md` | https://www.contributor-covenant.org/zh-cn/version/2/1/code_of_conduct/ |
| `CHANGELOG.md` | https://keepachangelog.com/zh-CN/1.1.0/ |
| 版本号规则 / Versioning | https://semver.org/lang/zh-CN/ |
| `CONTRIBUTING.md` | https://opensource.guide/zh-hans/starting-a-project/ |

Contributor Covenant 还有其他语种的译本，列表见 https://www.contributor-covenant.org/translations/ 。替换译本时注意保留文件第一行的来源注释。

Contributor Covenant is available in other languages too; the list is at https://www.contributor-covenant.org/translations/ . When you swap in a translation, keep the source comment on the first line of the file.

## Tracing the template version

Nothing in a generated repository records which template version it came from, so the skeleton stays clean. To find out, compare the date of your repository's initial commit against the template's [changelog](CHANGELOG.md): a repository created from a template has exactly one initial commit, so the release dated no later than it is the one you started from.

Optional: add a line such as `Created from Chef's Pick OSS Starter vX.Y.Z` to your own `CHANGELOG.md`. It is not required, it just saves you the lookup later.

## Changing the license

The template ships MIT: permissive, short and the most widely adopted. To switch, do three things.

Compare the terms at [choosealicense.com](https://choosealicense.com/licenses/mit/) and pick one, replace the entire contents of [`LICENSE`](../../LICENSE) with the new license's full text and fill in the year and the copyright holder, and update the license name in the License section of [`README.md`](../../README.md). Do not reword the license text: GitHub identifies the license by matching it, and an edited copy may stop being recognised.
