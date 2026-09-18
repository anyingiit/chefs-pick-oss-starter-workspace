# Maintaining the template

This page is for the maintainers of the template. It covers how often the adoption data is re-checked, how to re-check it, when a module must be re-evaluated, how pinned action versions are updated, how selection changes are recorded, and the gates that must pass before every release. People who merely use the template do not need this page: start from the [Setup checklist](SETUP.md), and see the [Selection list](SOURCES.md) for what was picked and why.

The `tools/` commands mentioned on this page run in the development workspace of the template. The `tools/` directory is not shipped with the template and does not exist in the template repository, so those commands are always written as inline code and never as links.

## Review cadence

The adoption data is re-checked at least once every 6 months, and again before every release regardless of when the last review happened. At release time no verification date may be older than 30 days; if any date is older, refresh the data first and release afterwards.

## How to review

1. **Refresh the repository data.**

   ```bash
   gh api repos/OWNER/REPO --jq '.stargazers_count, .forks_count, .archived, .default_branch'
   gh api repos/OWNER/REPO/commits/DEFAULT_BRANCH --jq .commit.committer.date
   ```

2. **Re-check the non-repository evidence by hand.**

   ```bash
   gh api "repos/EthicalSource/contributor_covenant/contents/assets/adopters.csv?ref=release" --jq .content | base64 -d | tail -n +2 | wc -l
   ```

3. **Check the triggers.**

4. **Update the verification dates.**

Step 1 refreshes the repository data, with the two `gh api` commands above as the fallback when the development workspace is not at hand. Step 2 re-checks evidence that no API returns: whether each official platform feature still exists, and the Contributor Covenant adopter count, which is recounted with the command above and, when it changes, updated in both the M04 evidence and the summary table on the template home page. Step 3 looks for the re-evaluation triggers below. Step 4 updates the four places that carry a verification date; `Last commit` is an upstream commit date and is not one of them.

## Re-evaluation triggers

A module must be re-evaluated when any of these holds: the last upstream commit is more than 12 months old; it depends on a widely deprecated tool; or a clearly better-adopted candidate has appeared. "Last commit" means the most recent commit on the default branch — the date fetched in step 1, never `pushed_at` — and an archived repository counts as meeting the first trigger without further checking. Re-pick with the same three-tier rule: higher community adoption first; when adoption is comparable, the option that is easier to start with (fewer steps, no extra dependency, built into the platform), stating the basis for calling adoption comparable; and only when candidates remain equally qualified may personal preference decide, which must be noted. Whether the pick changes or stands, update the module's fields, rationale and alternatives in `SOURCES.md` — recording that it was re-evaluated when it stands — and record the change as described below.

## Action updates

Treat a Dependabot pull request on the template repository as a notification that a new version exists, and **do not merge it there**. Publishing to the template repository is one-way, so merging directly makes the next release push fail. Instead, update the pinned hash and the trailing version comment in `template/` in the development workspace, update the pinned versions recorded in the verbatim contracts and in research so they match, run the checks, and publish again. Once the template repository's content is updated, the corresponding pull request closes by itself.

## Recording changes

A selection change updates both files in the same commit: the module's source, evidence, verification date, rationale and alternatives in `SOURCES.md`, and an entry under `Unreleased` in [CHANGELOG.md](CHANGELOG.md). Entries go under Added, Changed or Removed and always state the reason for the change. Updating only one of the two leaves the selection list and the changelog out of step.

## Keeping the translations in step

The translated files cover exactly two documents: `.github/README.md` has `.github/README.zh-CN.md`, and `.github/chefs-pick/SETUP.md` has `.github/chefs-pick/SETUP.zh-CN.md`. Every other guide-layer document is English-only and has no translated counterpart.

Each translated file carries a line of the form `<!-- translation-of: <source> sha256:<16 hex> -->`, recording a digest of the English source it was translated from. After an English source changes, running `python3 tools/check_template.py` flags the now-outdated translation with `WARN C24`; this warning does not affect the exit code, so ordinary development is not blocked by it.

After updating a translation to match its source, run `python3 tools/check_template.py --update-digests` to refresh that source marker to the current value. Do not compute the digest by hand and do not edit that line yourself.

Before a release, `python3 tools/check_template.py --release` treats an outdated translation as a **FAIL**, which makes the command exit 1. This is what release gate 6, "Every translation is aligned with its current English source," checks.

## Release gates

All six gates must pass **before** the Release is created:

1. No adoption verification date is older than 30 days before the release.
2. A repository newly generated from the template has every core element and its first CI run passes.
3. Every placeholder is found by a single search; outside the guide layer there is no template-author identity, no template version history and no development-process file; after the cleanup command the guide layer is gone and no broken reference is left behind.
4. After the setup checklist is complete, every item on the community standards page is green.
5. Every action reference is pinned to a full commit hash and the workflow token is read-only by default.
6. Every translation is aligned with its current English source.

Run `python3 tools/check_template.py --release` in the development workspace for the parts that can be checked automatically; the `--release` flag tightens the verification dates to 30 days. Two items are out of reach of that command and must be verified by hand in a test repository generated from the template: the first CI run passing on the new repository (gate 2) and every item on Insights → Community Standards showing a green check after the setup checklist has been completed (gate 4). The steps for both are in part C of `quickstart.md` in the development workspace.
