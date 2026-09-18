# Growing into a team project

This page is an optional short reference listing the additions a project commonly makes as it grows from solo maintenance into team collaboration; it reads in five minutes, and none of these files ship with the template, so add them when you need them.

## Common additions

| Addition | Purpose | Source | Adoption |
|---|---|---|---|
| CODEOWNERS for teams | Assign an owning team per path so pull requests request their review automatically | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners | Official platform feature |
| Rulesets | Require reviews and status checks on the default branch, superseding one-off branch protection | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets | Official platform feature |
| Renovate | Dependency updates with more control than Dependabot: grouping, schedules, automerge | https://github.com/renovatebot/renovate | ★ 22,527 (renovatebot/renovate) |
| pre-commit | Runs formatters and linters before each commit; the solo setup already ships as optional module M14, and a team can enforce it in CI | https://github.com/pre-commit/pre-commit | ★ 15,581 (pre-commit/pre-commit) |
| OpenSSF Scorecard | Scores a repository's supply-chain security practices and lists concrete items to follow up | https://github.com/ossf/scorecard | ★ 5,694 (ossf/scorecard) |

## When you need foundation-level governance

When a project is donated to a foundation, or needs formal governance, a steering committee and trademark rules, the three references below apply. They target organizations and are too heavy for a personal project.

- `cncf/project-template` — CNCF's official set of project governance documents, including GOVERNANCE, MAINTAINERS and CHARTER — Adoption: ★ 82 (cncf/project-template); Source: https://github.com/cncf/project-template
- `microsoft/repo-templates` — The templates and compliance files Microsoft uses for its public open source repositories — Adoption: ★ 89 (microsoft/repo-templates); Source: https://github.com/microsoft/repo-templates
- OpenSSF Best Practices Badge — A self-assessment questionnaire on open source best practices that awards a badge to display in your README — Adoption: ★ 1,360 (ossf/best-practices-badge); Source: https://bestpractices.dev

## No longer recommended

- `todogroup/repolinter` — A linter that checked whether a repository had its community health files; the upstream repository is archived and no longer maintained — Adoption: ★ 465 (todogroup/repolinter); Source: https://github.com/todogroup/repolinter
