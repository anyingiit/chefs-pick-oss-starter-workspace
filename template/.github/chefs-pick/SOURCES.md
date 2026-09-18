# Selection list

Data verified: 2026-09-18

This file records, module by module, the pick, its adoption evidence, the alternatives considered, and why they were not chosen, so that every choice can be re-checked.

## Selection rules

Picks are made with three rules applied in order. Rule 1 goes by community adoption: the candidate with clearly higher adoption wins. Rule 2 is used when rule 1 cannot separate the candidates, and picks whichever is easier for a repository owner to start with. Rule 3 is used only when the first two cannot separate them, and records the author's preference explicitly. The "Rule" field holds `1`, `2`, `3` or `1 + 2`; `1 + 2` means rule 1 already decided and rule 2 points the same way, while a bare `2` requires the rationale to state why adoption is judged comparable. Star counts alone are not enough, so every pick carries concrete evidence.

Adoption evidence uses exactly these six labels:

- `Exact stars`
- `Rounded stars`
- `Estimated users` (must state how it was estimated)
- `Official platform feature`
- `De facto standard` (must name specific adopters)
- `Not available` (must state what was used instead)

Review cadence: at least once every six months, and again before every release, with no verification date older than 30 days at release time.

## Modules

### M01 README

| Field | Value |
|---|---|
| Files | `README.md` |
| Level | Required |
| Pick | [Best-README-Template](https://github.com/othneildrew/Best-README-Template) |
| Version | othneildrew/Best-README-Template@fc444eb |
| Upstream license | Unlicense |
| Evidence | Exact stars: ★ 16,360 (othneildrew/Best-README-Template) |
| Rule | 1 |
| Verified | 2026-09-18 |

**Rationale**: It is by far the most widely adopted README template, so rule 1 settles the choice on its own. It is released under the Unlicense, so reuse needs no attribution, and the sections of `BLANK_README.md` cover exactly what a visitor reads first; dropping the project-specific sections leaves a clean skeleton.

**Alternatives**

- standard-readme — Exact stars: ★ 6,367 (RichardLitt/standard-readme) — it needs an extra linter and imposes a fixed section structure
- The-Documentation-Compendium — Exact stars: ★ 6,036 (race2infinity/The-Documentation-Compendium) — it has no license, so it cannot be reused safely
- awesome-readme-template — Exact stars: ★ 1,861 (Louis3797/awesome-readme-template) — no updates since 2022

### M02 License

| Field | Value |
|---|---|
| Files | `LICENSE` |
| Level | Required |
| Pick | [MIT on choosealicense.com](https://choosealicense.com/licenses/mit/), SPDX identifier `MIT` |
| Version | github/choosealicense.com@58267f8 |
| Upstream license | MIT |
| Evidence | Official platform feature: GitHub's own license picker; Exact stars: ★ 4,202 (github/choosealicense.com) |
| Rule | 1 |
| Verified | 2026-09-18 |

**Rationale**: The license text comes from choosealicense.com, which GitHub itself runs, so the source is authoritative and verifiable and rule 1 decides. MIT is short and minimally restrictive, which suits a personal project as a default, and GitHub detects it correctly on the repository home page.

**Alternatives**

- Other OSI licenses — Not available — the handover already fixed MIT as the default, and users can swap it themselves

### M03 Ignore rules

| Field | Value |
|---|---|
| Files | `.gitignore` |
| Level | Required |
| Pick | [github/gitignore's Global templates](https://github.com/github/gitignore) |
| Version | github/gitignore@356fd7b |
| Upstream license | CC0-1.0 |
| Evidence | Exact stars: ★ 175,816 (github/gitignore) |
| Rule | 1 |
| Verified | 2026-09-18 |

**Rationale**: This is GitHub's own collection of ignore rules and its adoption dwarfs every comparable option, so rule 1 decides. It is CC0-1.0, so the text can be included directly, and the Global templates are language-independent, which is exactly what is needed to keep operating-system and editor files out of the repository.

**Alternatives**

- the gitignore.io service — Not available — it depends on a third-party service and is less adopted than the official collection

### M04 Code of Conduct

| Field | Value |
|---|---|
| Files | `CODE_OF_CONDUCT.md` |
| Level | Recommended |
| Pick | [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) |
| Version | 2.1 (EthicalSource/contributor_covenant@7255a28) |
| Upstream license | CC-BY-4.0 |
| Evidence | De facto standard: 454 projects on the official adopters list, among them the .NET Foundation, Bootstrap, Cloud Native Computing Foundation, curl and Django; Exact stars: ★ 2,259 (EthicalSource/contributor_covenant) |
| Rule | 1 + 2 |
| Verified | 2026-09-18 |

**Rationale**: Under rule 1, the 2.x series is the most widely adopted code of conduct, with 454 projects on the official adopters list, among them the .NET Foundation, Bootstrap, CNCF, curl and Django. Rule 2 points the same way: 2.1 is CC BY 4.0 and only needs a contact method filled in, whereas 3.0 moved to CC BY-SA 4.0, which requires share-alike for modified versions and a rewritten enforcement section, making it heavier to start with.

**Alternatives**

- Contributor Covenant 3.0 — De facto standard — it uses CC BY-SA 4.0 and requires rewriting the whole enforcement section
- Contributor Covenant 2.0 — Official platform feature — it is the version GitHub's API returns, but 2.1 supersedes it
- Django Code of Conduct — Official platform feature — its adoption is much narrower

### M05 Contributing guide

| Field | Value |
|---|---|
| Files | `CONTRIBUTING.md` |
| Level | Recommended |
| Pick | [GitHub Open Source Guides](https://opensource.guide/starting-a-project/) + [GitHub Docs](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors) |
| Version | structure only, the text is original |
| Upstream license | CC-BY-4.0 (no text copied) |
| Evidence | Exact stars: ★ 15,685 (github/opensource.guide); Official platform feature: GitHub Docs |
| Rule | 1 |
| Verified | 2026-09-18 |

**Rationale**: GitHub's own Open Source Guides are the most widely adopted source in this area, and together with the matching GitHub Docs article they settle the choice under rule 1. The template borrows only their section structure and writes its own concise English text, so no CC BY attribution obligation arises, while the source comment still names the references.

**Alternatives**

- jessesquires/.github — Exact stars: ★ 42 (jessesquires/.github) — its default branch was last committed to on 2023-03-26, more than 12 months ago, and the community evidence is weak

### M06 Security policy

| Field | Value |
|---|---|
| Files | `SECURITY.md` |
| Level | Recommended |
| Pick | [GitHub Security policy](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy) + [Private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository) |
| Version | — |
| Upstream license | Official docs |
| Evidence | Official platform feature |
| Rule | 1 + 2 |
| Verified | 2026-09-18 |

**Rationale**: Under rule 1, both the security policy file and private vulnerability reporting are built into GitHub, the community profile check looks for `SECURITY.md` directly, and no third-party option competes. Rule 2 agrees: enabling private reporting is a single setting, and reporters submit from the Security tab without exchanging keys.

**Alternatives**

- An email address or PGP key only — Not available — it requires key exchange, is harder to start with, and reports stay outside the platform's advisory workflow

### M07 Issue forms

| Field | Value |
|---|---|
| Files | `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/ISSUE_TEMPLATE/config.yml` |
| Level | Recommended |
| Pick | [GitHub Issue Forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms) |
| Version | — |
| Upstream license | Official docs |
| Evidence | Official platform feature |
| Rule | 1 + 2 |
| Verified | 2026-09-18 |

**Rationale**: Under rule 1, issue forms are GitHub's official way to collect structured reports, the community profile check expects a valid `name` and `description`, and the third-party template collections all predate them. Rule 2 agrees: forms can mark key fields as required and apply labels automatically, so reporters do not have to copy a format by hand.

**Alternatives**

- stevemao/github-issue-templates — Exact stars: ★ 4,461 (stevemao/github-issue-templates) — it predates issue forms and its default branch has had no commits since 2024-03-20
- Markdown templates — Official platform feature — they cannot make fields required, so reports often arrive incomplete

### M08 Pull request template

| Field | Value |
|---|---|
| Files | `.github/PULL_REQUEST_TEMPLATE.md` |
| Level | Recommended |
| Pick | [GitHub Pull request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository) |
| Version | — |
| Upstream license | Official docs |
| Evidence | Official platform feature |
| Rule | 1 + 2 |
| Verified | 2026-09-18 |

**Rationale**: Under rule 1, a single pull request template is GitHub's officially supported form, and a file at `.github/PULL_REQUEST_TEMPLATE.md` is filled into every pull request description automatically. Rule 2 agrees: one file and one checklist means a personal project never has to pick a template.

**Alternatives**

- stevemao/github-issue-templates — Exact stars: ★ 4,461 (stevemao/github-issue-templates) — same as M07: it predates the official form and is no longer updated
- A directory of several templates — Official platform feature — a personal project does not need it, and it forces contributors to pick a template via the URL

### M09 Changelog & release notes

| Field | Value |
|---|---|
| Files | `CHANGELOG.md`, `.github/release.yml` |
| Level | Recommended |
| Pick | [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) + [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) + [GitHub Automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes) |
| Version | KaC 1.1.0 (2.0.0 is still an unreleased draft); SemVer 2.0.0 |
| Upstream license | MIT; CC-BY-3.0; Official docs |
| Evidence | Exact stars: ★ 6,702 (olivierlacan/keep-a-changelog), ★ 7,853 (semver/semver); Official platform feature: automatically generated release notes |
| Rule | 1 |
| Verified | 2026-09-18 |

**Rationale**: Keep a Changelog and Semantic Versioning are the two most widely adopted specifications for a human-readable history, so rule 1 decides; 1.1.0 is the current released version while 2.0.0 is still an unreleased draft, so the pick is pinned to 1.1.0. Release-note grouping is left to GitHub's built-in feature, which keys off the default `bug` and `enhancement` labels and adds no dependency.

**Alternatives**

- Release notes only, with no changelog file — Official platform feature — a core element would be missing and the history would not be readable inside the repository
- Keep a Changelog 2.0.0 — De facto standard — it is not released yet and remains a draft

### M10 Changelog automation

| Field | Value |
|---|---|
| Files | — |
| Level | Optional (recommendation only) |
| Pick | [changesets](https://github.com/changesets/changesets), [git-cliff](https://github.com/orhun/git-cliff), [release-please](https://github.com/googleapis/release-please) |
| Version | chosen by the user |
| Upstream license | MIT; Apache-2.0 or MIT; Apache-2.0 |
| Evidence | Exact stars: ★ 12,408 (changesets/changesets), ★ 12,245 (orhun/git-cliff), ★ 7,509 (googleapis/release-please) |
| Rule | 1 + 2 |
| Verified | 2026-09-18 |

**Rationale**: Under rule 1, each of the three leads adoption in its own ecosystem: changesets for Node projects, git-cliff as a single language-agnostic binary, and release-please for projects on Conventional Commits that want an automated release pull request. Rule 2 decides that none is enabled by default: the template ships no file here, the M09 default is usually enough for a personal project, and a tool can be added later by project type.

**Alternatives**

- GitHub's automatically generated release notes — Official platform feature — it is the M09 default, needs no dependency and is usually enough for a personal project, which is why no tool is enabled here by default

### M11 Continuous integration

| Field | Value |
|---|---|
| Files | `.github/workflows/ci.yml` |
| Level | Recommended |
| Pick | [actions/starter-workflows's Simple workflow](https://github.com/actions/starter-workflows/blob/main/ci/blank.yml) + [actions/checkout](https://github.com/actions/checkout) |
| Version | actions/checkout@3d3c42e (v7.0.1) |
| Upstream license | MIT; MIT |
| Evidence | Exact stars: ★ 12,082 (actions/starter-workflows), ★ 8,884 (actions/checkout); basis for pinning to a hash: Official platform feature (GitHub Docs secure-use reference) and Exact stars ★ 5,694 (ossf/scorecard) |
| Rule | 1 + 2 |
| Verified | 2026-09-18 |

**Rationale**: Under rule 1, the starter workflow collection is maintained by GitHub itself and `actions/checkout` is the most widely used action, while pinning actions to a full commit hash is backed both by GitHub's secure-use reference and by OpenSSF Scorecard. Rule 2 agrees: the Simple workflow passes on an empty repository, so users only fill in their own lint and test commands at the marked places instead of learning a whole CI configuration first.

**Alternatives**

- super-linter — Exact stars: ★ 10,598 (super-linter/super-linter) — its image is large and runs slowly
- markdownlint — Exact stars: ★ 6,345 (DavidAnson/markdownlint) — the README skeleton contains HTML, so it produces false positives without extra rule tuning
- actionlint — Exact stars: ★ 4,235 (rhysd/actionlint) — there is no official action, so it needs a download script or Docker
- github-actions-ensure-sha-pinned-actions — Exact stars: ★ 55 (zgosalvez/github-actions-ensure-sha-pinned-actions) — adoption is low and it means trusting one more third-party action

### M12 Dependency updates

| Field | Value |
|---|---|
| Files | `.github/dependabot.yml` |
| Level | Recommended |
| Pick | [GitHub Dependabot](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference) |
| Version | — |
| Upstream license | MIT (dependabot-core) |
| Evidence | Official platform feature; Exact stars: ★ 5,773 (dependabot/dependabot-core) |
| Rule | 2 |
| Verified | 2026-09-18 |

**Rationale**: Both are de facto standards with comparable adoption; Dependabot is built into the platform and needs no installation. Adoption is judged comparable because both are used at scale: Renovate's repository has more stars (★ 22,527 (renovatebot/renovate)), while Dependabot, as a built-in feature, has no comparable star count at all — `dependabot/dependabot-core` is only its implementation repository — so rule 1 cannot separate them and rule 2 applies. Dependabot also keeps the trailing version comment in step when it bumps an action hash, which fits the pinning style used in M11.

**Alternatives**

- Renovate — Exact stars: ★ 22,527 (renovatebot/renovate) — it requires installing a GitHub App and writing its own configuration, is licensed AGPL-3.0, and is listed in the team upgrade guide instead

### M13 EditorConfig

| Field | Value |
|---|---|
| Files | `.editorconfig` |
| Level | Optional |
| Pick | [EditorConfig](https://editorconfig.org) |
| Version | — |
| Upstream license | Unknown |
| Evidence | Exact stars: ★ 3,450 (editorconfig/editorconfig); review note: default branch last committed to on 2025-04-21, re-evaluated under constitution principle III and kept |
| Rule | 1 |
| Verified | 2026-09-18 |

**Rationale**: For unifying encoding, line endings and indentation there is no second candidate with comparable adoption, and mainstream editors support it natively or through an official plugin, so rule 1 decides. The upstream default branch was last committed to on 2025-04-21, more than 12 months ago, so it was re-evaluated under constitution principle III: the specification itself is stable and the low activity reflects that stability rather than abandonment, so the pick stands.

**Alternatives**

- No comparable alternative — Not available — editor-specific settings files do not carry across editors

### M14 Pre-commit hooks

| Field | Value |
|---|---|
| Files | `.pre-commit-config.yaml` |
| Level | Optional |
| Pick | [pre-commit](https://pre-commit.com) + [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks) |
| Version | pre-commit-hooks@3e8a870 (v6.0.0) |
| Upstream license | MIT; MIT |
| Evidence | Exact stars: ★ 15,581 (pre-commit/pre-commit), ★ 6,681 (pre-commit/pre-commit-hooks) |
| Rule | 1 |
| Verified | 2026-09-18 |

**Rationale**: pre-commit is the most widely adopted cross-language hook manager and its official hook collection is just as widely used, so rule 1 decides. The `rev` is pinned to a full commit hash with a version comment, matching the approach in M11, and nothing happens until `pre-commit install` is run, so shipping the file by default disturbs nobody.

**Alternatives**

- Plain Git hook scripts — Not available — they cannot be shared and are not version-controlled

### M15 Code owners

| Field | Value |
|---|---|
| Files | `.github/CODEOWNERS` |
| Level | Optional |
| Pick | [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) |
| Version | — |
| Upstream license | Official docs |
| Evidence | Official platform feature |
| Rule | 1 |
| Verified | 2026-09-18 |

**Rationale**: Automatic review requests are built into GitHub and driven directly by the path rules in `CODEOWNERS`, with no third-party option able to do the same, so rule 1 decides. Every line in the shipped file is a comment, so nothing takes effect until the project has collaborators and the lines are uncommented.

**Alternatives**

- No comparable alternative — Not available — it is a built-in platform feature and no third-party tool can take over review requests

### M16 Funding

| Field | Value |
|---|---|
| Files | `.github/FUNDING.yml` |
| Level | Optional |
| Pick | [GitHub Sponsor button](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository) |
| Version | — |
| Upstream license | Official docs |
| Evidence | Official platform feature |
| Rule | 1 |
| Verified | 2026-09-18 |

**Rationale**: The sponsor button on a repository page can only be driven by `.github/FUNDING.yml`, which is GitHub's single official mechanism, so rule 1 decides. The template keeps the format the settings page generates, with only the empty `github:` and `custom:` keys, so no sponsor button appears by default.

**Alternatives**

- Hand-written funding links in the README — Not available — it does not produce the repository's sponsor button

## Excluded candidates

| Candidate | Adoption | Reason |
|---|---|---|
| golang-standards/project-layout | ★ 56,602 (golang-standards/project-layout) | the Go team states explicitly that it is not an official standard, so the high star count is not authoritative |
| cookiecutter/cookiecutter | ★ 25,091 (cookiecutter/cookiecutter) | it is a scaffolding generator that needs a separate install and its own workflow, against the choice of a ready-to-use template repository |
| stevemao/github-issue-templates | ★ 4,461 (stevemao/github-issue-templates) | superseded by the official issue forms, and its default branch has had no commits since 2024-03-20 |
| copier-org/copier | ★ 3,579 (copier-org/copier) | also a generator: users must install a tool before they can create a project |
| dec0dOS/amazing-github-template | ★ 710 (dec0dOS/amazing-github-template) | it is built on cookiecutter and its default branch has had no commits since 2021-12-08 |
| todogroup/repolinter | ★ 465 (todogroup/repolinter), archived | the repository is archived and unmaintained, which counts as abandoned under constitution principle III |
| cncf/project-template | ★ 82 (cncf/project-template) | it targets foundation-level governance, far beyond what a personal project needs, so it is listed only in the team upgrade guide |
| jessesquires/.github | ★ 42 (jessesquires/.github) | adoption is low and its default branch was last committed to on 2023-03-26, more than 12 months ago, so it is kept only as a reference example |
| maehr/github-template | ★ 23 (maehr/github-template) | adoption is low and it is licensed AGPL-3.0, which puts an extra compliance burden on users |

## Adoption data

The table below is a machine-readable adoption snapshot, refreshed in bulk by `tools/verify_sources.py`. `Last commit` is the date of the most recent commit on the default branch, not `pushed_at`; `License` holds only the SPDX identifier returned by the GitHub API, or `unknown` when none is returned.

<!-- adoption-data:start -->
| Repo | Stars | Forks | Last commit | License | Archived | Verified |
|---|---:|---:|---|---|---|---|
| github/gitignore | 175,816 | 82,186 | 2026-09-11 | CC0-1.0 | no | 2026-09-18 |
| othneildrew/Best-README-Template | 16,360 | 23,013 | 2026-04-18 | Unlicense | no | 2026-09-18 |
| RichardLitt/standard-readme | 6,367 | 2,507 | 2026-06-17 | MIT | no | 2026-09-18 |
| race2infinity/The-Documentation-Compendium | 6,036 | 739 | 2025-10-31 | unknown | no | 2026-09-18 |
| Louis3797/awesome-readme-template | 1,861 | 437 | 2022-04-07 | CC0-1.0 | no | 2026-09-18 |
| EthicalSource/contributor_covenant | 2,259 | 1,435 | 2026-05-20 | unknown | no | 2026-09-18 |
| olivierlacan/keep-a-changelog | 6,702 | 3,537 | 2026-09-03 | MIT | no | 2026-09-18 |
| semver/semver | 7,853 | 785 | 2025-11-05 | unknown | no | 2026-09-18 |
| actions/starter-workflows | 12,082 | 7,329 | 2026-08-03 | unknown | no | 2026-09-18 |
| actions/checkout | 8,884 | 2,779 | 2026-07-20 | MIT | no | 2026-09-18 |
| github/choosealicense.com | 4,202 | 1,628 | 2026-09-10 | MIT | no | 2026-09-18 |
| github/opensource.guide | 15,685 | 15,524 | 2026-09-04 | CC-BY-4.0 | no | 2026-09-18 |
| jessesquires/.github | 42 | 28 | 2023-03-26 | MIT | no | 2026-09-18 |
| stevemao/github-issue-templates | 4,461 | 5,550 | 2024-03-20 | unknown | no | 2026-09-18 |
| changesets/changesets | 12,408 | 833 | 2026-09-14 | MIT | no | 2026-09-18 |
| orhun/git-cliff | 12,245 | 326 | 2026-09-13 | Apache-2.0 | no | 2026-09-18 |
| googleapis/release-please | 7,509 | 589 | 2026-09-14 | Apache-2.0 | no | 2026-09-18 |
| editorconfig/editorconfig | 3,450 | 119 | 2025-04-21 | unknown | no | 2026-09-18 |
| pre-commit/pre-commit | 15,581 | 1,009 | 2026-08-17 | MIT | no | 2026-09-18 |
| pre-commit/pre-commit-hooks | 6,681 | 799 | 2026-08-17 | MIT | no | 2026-09-18 |
| dependabot/dependabot-core | 5,773 | 1,524 | 2026-09-17 | MIT | no | 2026-09-18 |
| renovatebot/renovate | 22,527 | 3,315 | 2026-09-17 | AGPL-3.0 | no | 2026-09-18 |
| ossf/scorecard | 5,694 | 724 | 2026-09-08 | Apache-2.0 | no | 2026-09-18 |
| DavidAnson/markdownlint | 6,345 | 946 | 2026-07-28 | MIT | no | 2026-09-18 |
| rhysd/actionlint | 4,235 | 272 | 2026-04-19 | MIT | no | 2026-09-18 |
| super-linter/super-linter | 10,598 | 1,080 | 2026-09-17 | MIT | no | 2026-09-18 |
| zgosalvez/github-actions-ensure-sha-pinned-actions | 55 | 16 | 2026-09-05 | MIT | no | 2026-09-18 |
| golang-standards/project-layout | 56,602 | 5,425 | 2026-04-28 | unknown | no | 2026-09-18 |
| cookiecutter/cookiecutter | 25,091 | 2,277 | 2026-03-04 | BSD-3-Clause | no | 2026-09-18 |
| copier-org/copier | 3,579 | 273 | 2026-09-07 | MIT | no | 2026-09-18 |
| cncf/project-template | 82 | 46 | 2026-08-11 | Apache-2.0 | no | 2026-09-18 |
| microsoft/repo-templates | 89 | 93 | 2026-08-24 | MIT | no | 2026-09-18 |
| dec0dOS/amazing-github-template | 710 | 259 | 2021-12-08 | MIT | no | 2026-09-18 |
| maehr/github-template | 23 | 6 | 2026-03-06 | AGPL-3.0 | no | 2026-09-18 |
| todogroup/repolinter | 465 | 74 | 2026-02-06 | Apache-2.0 | yes | 2026-09-18 |
| ossf/best-practices-badge | 1,360 | 233 | 2026-09-17 | MIT | no | 2026-09-18 |
<!-- adoption-data:end -->

## About the data

Repository data comes from the GitHub API. Stars and forks are the exact integers the API returns, written with thousands separators. `Last commit` is the date of the most recent commit on the default branch rather than `pushed_at`, because `pushed_at` is bumped by a push to any branch and would hide an abandoned upstream. `Archived` is the API's archive flag. `License` holds only `license.spdx_id`, written as `unknown` when the API returns `NOASSERTION` or no value, which is why it can differ from the "Upstream license" field of a module: that field records the actual license found by reading the upstream license file. Non-repository evidence falls into two groups: official platform features are verified against the corresponding GitHub Docs article, and the Contributor Covenant adopter count comes from the official adopters list in the upstream repository. The review cadence, the review steps and the refresh command are documented in `MAINTAINING.md`, in this same directory.
