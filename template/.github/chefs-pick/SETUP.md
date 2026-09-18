<!-- anchor: setup-checklist -->
# Setup checklist

**English** · [简体中文](SETUP.zh-CN.md)

Work through this checklist in order; it takes about 15 minutes. Replace the placeholders first, then complete the repository settings and the project files, and remove this guide layer last.

<!-- anchor: placeholders -->
## Placeholders

The table below registers every placeholder in the template. Replace each one with your own project information, and leave none behind.

| Placeholder | Meaning | Files | Example |
|---|---|---|---|
| `CHANGEME_OWNER` | GitHub user or organization | `README.md`、`SECURITY.md`、`CHANGELOG.md`、`.github/ISSUE_TEMPLATE/config.yml`、`.github/CODEOWNERS` | `octocat` |
| `CHANGEME_REPO` | Repository name | `README.md`、`SECURITY.md`、`CHANGELOG.md`、`.github/ISSUE_TEMPLATE/config.yml` | `hello-world` |
| `CHANGEME_PROJECT_NAME` | Project display name | `README.md` | `Hello World` |
| `CHANGEME_PROJECT_DESCRIPTION` | One-sentence description | `README.md` | `A tiny tool that says hello.` |
| `CHANGEME_USAGE_EXAMPLE` | Minimal usage example | `README.md` | `hello --name Ada` |
| `CHANGEME_YEAR` | Copyright year | `LICENSE` | `2026` |
| `CHANGEME_COPYRIGHT_HOLDER` | Copyright holder | `LICENSE` | `Ada Lovelace` |
| `CHANGEME_SECURITY_EMAIL` | Fallback email for security reports | `SECURITY.md` | `security@example.com` |
| `CHANGEME_CONDUCT_EMAIL` | Email for Code of Conduct reports | `CODE_OF_CONDUCT.md` | `conduct@example.com` |

Before you remove the guide layer, use this command to find the placeholders you have not replaced yet. It excludes the registry table on this page, so the table itself is not counted.

```bash
git grep -n CHANGEME -- . ':(exclude).github/chefs-pick'
```

After you remove the guide layer, use this command for the final check.

```bash
git grep -n CHANGEME
```

Neither command should print anything.

<!-- anchor: steps -->
## Steps

| ID | Kind | Step | How to verify |
|---|---|---|---|
| S01 | Required | Replace every placeholder, working through the registry table above. | The pre-cleanup search command prints nothing. |
| S02 | Required | Fill in the description under About (the gear icon) on the repository home page, and optionally add topics. If the repository belongs to an organization, also enable reported content under Settings → Moderation options → Reported content; repositories owned by a personal account do not have this setting. | The description shows on the right-hand side of the repository home page, and every settings-related item on the community standards page is complete. |
| S03 | Required | Enable private vulnerability reporting under Settings → Advanced Security → Private vulnerability reporting ([Official docs](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)). | The Security tab shows **Report a vulnerability**. |
| S04 | Required | Enable Discussions under Settings → General → Features → Discussions ([Official docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/enabling-or-disabling-github-discussions-for-a-repository)). If you decide not to, point both places at your own support channel: the discussions link in [`.github/ISSUE_TEMPLATE/config.yml`](../ISSUE_TEMPLATE/config.yml) and the Questions section of [`CONTRIBUTING.md`](../../CONTRIBUTING.md). | The support link on the New issue page opens, and the channel named in `CONTRIBUTING.md` is the same one. |
| S05 | Required | Confirm the license: MIT is the default. To use a different one, pick it on [choosealicense.com](https://choosealicense.com/licenses/mit/), replace [`LICENSE`](../../LICENSE), and update the License section of [`README.md`](../../README.md) to match. | The repository home page shows the right license. |
| S06 | Required | Add three things for your project's language: the `.gitignore` rules, taken from `github/gitignore`; the lint and test steps in `ci.yml`, pinning any action you add to a commit hash as described in the "Pinning actions" section of the [module guide](GUIDE.md); and your dependency ecosystems in `dependabot.yml`. | CI passes after you push. |
| S07 | Optional | Decide one by one whether to keep each recommended and optional module; the [module guide](GUIDE.md) explains how to remove each of them. | Every optional module you kept has been enabled as its instructions describe. |
| S08 | Required | Remove the guide layer by running the cleanup command given on the [template home page](../README.md). | The repository home page shows your own `README.md`. |
| S09 | Required | Run the final check. | Every item under Insights → Community Standards has a green check, `git grep -n CHANGEME` prints nothing, and CI passes. The page only lists the items your account type supports — reported content, for example, appears only for public repositories owned by an organization — so everything it lists should be something you can complete. |
