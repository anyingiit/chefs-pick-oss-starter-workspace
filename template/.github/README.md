<!-- anchor: chefs-pick-oss-starter -->
# Chef's Pick OSS Starter

**English** · [简体中文](README.zh-CN.md)

This template gives a new open source repository every file it needs to collaborate. Each module uses a pick the community already recognizes, ready to use out of the box, and every choice states its source, its adoption evidence, and the date it was verified — never just the author's taste.

> This is the template's setup guide page. Your own project README lives at [README.md](../README.md); once you finish setup and delete this page, that file becomes the repository's front page.

<!-- anchor: what-you-get -->
## What you get

<!-- anchor: required -->
### Required

- `README.md` — Project readme (M01)
- `LICENSE` — License (M02)
- `.gitignore` — Ignore rules (M03)

<!-- anchor: recommended -->
### Recommended

- `CODE_OF_CONDUCT.md` — Code of conduct (M04)
- `CONTRIBUTING.md` — Contributing guide (M05)
- `SECURITY.md` — Security policy (M06)
- `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/ISSUE_TEMPLATE/config.yml` — Issue forms (M07)
- `.github/PULL_REQUEST_TEMPLATE.md` — Pull request template (M08)
- `CHANGELOG.md`, `.github/release.yml` — Changelog and release notes (M09)
- `.github/workflows/ci.yml` — Continuous integration (M11)
- `.github/dependabot.yml` — Dependency updates (M12)

<!-- anchor: optional -->
### Optional

- `.editorconfig` — EditorConfig (M13)
- `.pre-commit-config.yaml` — Pre-commit hooks (M14)
- `.github/CODEOWNERS` — Code owners (M15)
- `.github/FUNDING.yml` — Funding (M16)

Changelog automation (M10) ships as a recommendation only: it adds no files, and you pick the tool that suits your project.

<!-- anchor: the-picks-at-a-glance -->
## The picks at a glance

<!-- summary:start -->
| Module | Pick | Adoption | Verified |
|---|---|---|---|
| M01 README | Best-README-Template | ★ 16,360 (othneildrew/Best-README-Template) | 2026-09-18 |
| M02 License | choosealicense.com (MIT) | Official platform feature | 2026-09-18 |
| M03 Ignore rules | github/gitignore (Global) | ★ 175,816 (github/gitignore) | 2026-09-18 |
| M04 Code of Conduct | Contributor Covenant 2.1 | De facto standard (454 adopters) | 2026-09-18 |
| M05 Contributing guide | GitHub Open Source Guides | ★ 15,685 (github/opensource.guide) | 2026-09-18 |
| M06 Security policy | GitHub security policy + private vulnerability reporting | Official platform feature | 2026-09-18 |
| M07 Issue forms | GitHub Issue Forms | Official platform feature | 2026-09-18 |
| M08 Pull request template | GitHub pull request template | Official platform feature | 2026-09-18 |
| M09 Changelog & release notes | Keep a Changelog 1.1.0 + SemVer 2.0.0 | ★ 6,702 (olivierlacan/keep-a-changelog) | 2026-09-18 |
| M10 Changelog automation | changesets, git-cliff, release-please (recommendation only) | ★ 12,408 (changesets/changesets) | 2026-09-18 |
| M11 Continuous integration | actions/starter-workflows' Simple workflow | ★ 12,082 (actions/starter-workflows) | 2026-09-18 |
| M12 Dependency updates | GitHub Dependabot | Official platform feature | 2026-09-18 |
| M13 EditorConfig | EditorConfig | ★ 3,450 (editorconfig/editorconfig) | 2026-09-18 |
| M14 Pre-commit hooks | pre-commit + pre-commit-hooks | ★ 15,581 (pre-commit/pre-commit) | 2026-09-18 |
| M15 Code owners | GitHub CODEOWNERS | Official platform feature | 2026-09-18 |
| M16 Funding | GitHub sponsor button | Official platform feature | 2026-09-18 |<!-- summary:end -->

[Full selection list](chefs-pick/SOURCES.md)

<!-- anchor: how-we-pick -->
## How we pick

Picks follow a fixed order, and star counts alone are not enough:

1. The option with higher community adoption wins.
2. When adoption is comparable, the option that is easier to start with wins — fewer steps, no extra dependency, or built into the platform.
3. Only when options remain equally qualified does the author's preference decide, and it is labeled as such.

Adoption evidence always states its type: exact stars, rounded stars, estimated users, official platform feature, de facto standard (with named adopters), or not available. Numbers are recorded as measured, never guessed.

<!-- anchor: quick-start -->
## Quick start

1. Click **Use this template** to create your own repository.
2. Work through the [Setup checklist](chefs-pick/SETUP.md); it takes about 15 minutes.
3. Whenever you want to know what a module does, read the [Module guide](chefs-pick/GUIDE.md).

(Optional) Once the project has grown into a multi-person effort, see [Growing into a team project](chefs-pick/UPGRADE-TO-TEAM.md)

<!-- anchor: good-to-know -->
## Good to know

- **The bundled issue forms override your account-level defaults.** Because this template ships valid issue forms and config, the default issue templates in your account-level `.github` repository stop applying entirely.
- **Private vulnerability reporting and Discussions must be enabled by hand.** Both are repository settings that no template can switch on for you; the setup checklist covers them.
- **A repository generated from this template does not track it.** To follow later changes, watch the template's [CHANGELOG](chefs-pick/CHANGELOG.md) and port what you want.

<!-- anchor: clean-up-when-done -->
## Clean up when done

Once setup is done, remove the guide layer: your own readme becomes the repository's front page, and nothing of the template's own identity remains.

```bash
git rm -r .github/README.md .github/README.zh-CN.md .github/chefs-pick
git commit -m "chore: remove template guide"
```

On the web, delete this file and the `.github/chefs-pick` directory; the result is the same.

<!-- anchor: feedback-and-contact -->
## Feedback and contact

- The root `CODE_OF_CONDUCT.md` and `SECURITY.md` are skeletons for you to fill in: their contact addresses and issue links are placeholders and do not work in the template repository itself, so please do not use them to reach us.
- For a security issue in this template repository, report it privately from the Security tab with **Report a vulnerability**.
- For anything else, open an issue here or start a discussion; for a serious code of conduct problem, you can report the content to GitHub itself (the "reported content" setting is only available to public repositories owned by an organization).

<!-- anchor: license -->
## License

- This template is released under the MIT license; see [LICENSE](chefs-pick/LICENSE).
- Projects generated from this template need not keep any attribution to it: replace the copyright holder, or choose a different license entirely.
- The body of `CODE_OF_CONDUCT.md` comes from the Contributor Covenant under CC-BY-4.0, and its Attribution section must be kept.
