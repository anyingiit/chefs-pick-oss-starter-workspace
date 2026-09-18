"""Tests for the contributor-facing checks: C04, C07, C16 and C20.

Contract: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.1, §1.3, §3 and
``specs/001-chefs-pick-starter/contracts/project-files.md`` M04 ~ M09.

Every case builds only the files the check under test needs, inside a fresh
``tempfile.TemporaryDirectory()``.  Fixtures reuse ``check_template``'s own
constants (``SOURCE_COMMENTS``) so that the first line of each file cannot drift
away from the registry.
"""

from __future__ import annotations

import tempfile
import unittest

from helpers import make_ctx, run_one, write_tree

import check_template as ct  # noqa: E402  (helpers puts tools/ on sys.path)

BUG_PATH = ".github/ISSUE_TEMPLATE/bug_report.yml"
FEATURE_PATH = ".github/ISSUE_TEMPLATE/feature_request.yml"
CONFIG_PATH = ".github/ISSUE_TEMPLATE/config.yml"
RELEASE_PATH = ".github/release.yml"
COC_PATH = "CODE_OF_CONDUCT.md"
SECURITY_PATH = "SECURITY.md"
CONTRIBUTING_PATH = "CONTRIBUTING.md"
PR_PATH = ".github/PULL_REQUEST_TEMPLATE.md"
README_PATH = "README.md"


def with_source(rel: str, body: str) -> str:
    """Prefix *body* with the registered source comment of *rel*."""
    return ct.SOURCE_COMMENTS[rel] + "\n" + body


def mutate(text: str, old: str, new: str) -> str:
    """Replace the first occurrence of *old*, asserting it was present."""
    if old not in text:  # pragma: no cover - guards against a stale fixture
        raise AssertionError(f"fixture no longer contains: {old!r}")
    return text.replace(old, new, 1)


def swap(text: str, first: str, second: str) -> str:
    """Exchange the first occurrence of *first* with the one of *second*."""
    marker = "\x00SWAP\x00"
    text = mutate(text, first, marker)
    text = mutate(text, second, first)
    return mutate(text, marker, second)


# --------------------------------------------------------------------------
# Fixtures -- verbatim from project-files.md
# --------------------------------------------------------------------------

# M07
BUG_REPORT_YML = with_source(
    BUG_PATH,
    """name: Bug report
description: Report something that is not working as expected.
title: "[Bug]: "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to report a bug! Please search the existing issues first to avoid duplicates.
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Describe the actual behavior you observed.
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: List the steps needed to reproduce the problem.
      placeholder: |
        1. ...
        2. ...
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: Describe what you expected to happen instead.
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Project version, operating system, and any other relevant details.
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs or screenshots
      description: Paste any relevant log output. It will be formatted as code automatically.
      render: shell
    validations:
      required: false
""",
)

# M07
FEATURE_REQUEST_YML = with_source(
    FEATURE_PATH,
    """name: Feature request
description: Suggest an idea or improvement for this project.
title: "[Feature]: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for the suggestion! Please search the existing issues first to see if it has already been proposed.
  - type: textarea
    id: problem
    attributes:
      label: What problem would this solve?
      description: Describe the problem or need behind this request.
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Proposed solution
      description: Describe what you would like to happen.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      description: Describe any other solutions or workarounds you have considered.
    validations:
      required: false
  - type: textarea
    id: context
    attributes:
      label: Additional context
      description: Add any other context, links, or screenshots.
    validations:
      required: false
""",
)

# M07
CONFIG_YML = with_source(
    CONFIG_PATH,
    """blank_issues_enabled: false
contact_links:
  - name: Questions and help
    url: https://github.com/CHANGEME_OWNER/CHANGEME_REPO/discussions
    about: Please ask and answer questions in GitHub Discussions.
  - name: Report a security vulnerability
    url: https://github.com/CHANGEME_OWNER/CHANGEME_REPO/security/advisories/new
    about: Please report security vulnerabilities privately, not in public issues.
""",
)

# M09
RELEASE_YML = with_source(
    RELEASE_PATH,
    """changelog:
  categories:
    - title: New Features
      labels:
        - enhancement
    - title: Bug Fixes
      labels:
        - bug
    - title: Other Changes
      labels:
        - "*"
""",
)

# M04: the source comment, a blank line, then the Contributor Covenant 2.1 text
# with its TOML front matter removed and the contact placeholder substituted.
# Only the passages C16 looks at are reproduced here.
CODE_OF_CONDUCT_MD = with_source(
    COC_PATH,
    """
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders responsible for enforcement at
CHANGEME_CONDUCT_EMAIL. All complaints will be reviewed and investigated
promptly and fairly.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.1, available at
[https://www.contributor-covenant.org/version/2/1/code_of_conduct.html][v2.1].

[homepage]: https://www.contributor-covenant.org
[v2.1]: https://www.contributor-covenant.org/version/2/1/code_of_conduct.html
""",
)

# M06
SECURITY_MD = with_source(
    SECURITY_PATH,
    """# Security Policy

## Supported Versions

Security updates are provided for the latest release only.

| Version | Supported |
| --- | --- |
| Latest release | :white_check_mark: |
| Older releases | :x: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public issues, discussions, or pull requests.**

Report it privately instead. Open the **Security** tab of this repository and choose **Report a vulnerability**, or go directly to https://github.com/CHANGEME_OWNER/CHANGEME_REPO/security/advisories/new. If private vulnerability reporting is unavailable, email CHANGEME_SECURITY_EMAIL.

Please include:

- A description of the vulnerability and the impact you expect it to have.
- Steps to reproduce it, or a proof of concept.
- The versions that are affected.

We will acknowledge your report and keep you informed as we investigate and fix the issue.
""",
)

# M05
CONTRIBUTING_MD = with_source(
    CONTRIBUTING_PATH,
    """# Contributing

Thanks for your interest in this project. Every kind of contribution is welcome.

## Code of Conduct

This project is governed by its [Code of Conduct](CODE_OF_CONDUCT.md). By taking part in this project you agree to abide by its terms.

## Ways to contribute

- Report a bug you ran into.
- Suggest a feature or an improvement.
- Improve the documentation, including examples and typo fixes.
- Contribute code through a pull request.

## Reporting bugs

Search the existing issues first. If nothing matches, open a new issue from the Issues tab (Issues, then New issue) and pick the **Bug report** form. Please fill in every required field.

## Suggesting features

Open a new issue from the Issues tab and pick the **Feature request** form. Describe the problem you want to solve before the solution you have in mind.

## Reporting security issues

Do not report security issues in public. Follow the steps in the [security policy](SECURITY.md) instead.

## Submitting pull requests

1. Fork the repository and create a branch from `main`.
2. Follow the existing code style.
3. Add or update tests that cover your change.
4. If the change is worth recording, add an entry under `Unreleased` in the [changelog](CHANGELOG.md).
5. Make sure the CI checks pass.
6. Open a pull request and fill in the template.

## Development setup

See [Getting started](README.md#getting-started) for how to install the dependencies and run the project locally.

## Questions

For questions about using the project, start a thread in the Discussions tab instead of opening an issue.
""",
)

# M08
PULL_REQUEST_TEMPLATE_MD = with_source(
    PR_PATH,
    """## Description

<!-- What does this pull request change, and why? -->

## Related issue

Closes #

## Checklist

- [ ] Tests pass locally
- [ ] `CHANGELOG.md` is updated (if applicable)
- [ ] Documentation is updated (if applicable)
""",
)

# Only the part of the README that C20 looks at.
README_MD = with_source(
    README_PATH,
    """# CHANGEME_PROJECT_NAME

[Report a bug](https://github.com/CHANGEME_OWNER/CHANGEME_REPO/issues/new?template=bug_report.yml) · [Request a feature](https://github.com/CHANGEME_OWNER/CHANGEME_REPO/issues/new?template=feature_request.yml)

## Getting started

Describe how to install and run the project here.
""",
)


class CheckCase(unittest.TestCase):
    """Shared plumbing: run one check over a freshly written minimal tree."""

    check_id = ""

    def run_check(self, files: dict[str, str]):
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, files)
            return run_one(self.check_id, make_ctx(tmp))

    def assert_passes(self, files: dict[str, str]):
        status, problems = self.run_check(files)
        self.assertEqual(status, "PASS", problems)

    def assert_fails(self, files: dict[str, str]):
        status, problems = self.run_check(files)
        self.assertEqual(status, "FAIL")
        self.assertTrue(problems, "a failing check must report at least one problem")
        return problems

    def assert_skips(self, files: dict[str, str]):
        status, reason = self.run_check(files)
        self.assertEqual(status, "SKIP", reason)
        return reason


class CheckC04IssueFormsTest(CheckCase):
    """C04: project-files.md M07."""

    check_id = "C04"

    def forms(self, bug=None, feature=None, config=None) -> dict[str, str]:
        return {
            BUG_PATH: BUG_REPORT_YML if bug is None else bug,
            FEATURE_PATH: FEATURE_REQUEST_YML if feature is None else feature,
            CONFIG_PATH: CONFIG_YML if config is None else config,
        }

    # -- pass ---------------------------------------------------------------

    def test_verbatim_forms_pass(self):
        self.assert_passes(self.forms())

    def test_only_config_present_passes(self):
        """§1.1: a check only looks at the files that are actually there."""
        self.assert_passes({CONFIG_PATH: CONFIG_YML})

    # -- fail ---------------------------------------------------------------

    def test_steps_not_required_fails(self):
        """tasks.md: `steps` must stay a required field."""
        bug = mutate(
            BUG_REPORT_YML,
            "        2. ...\n    validations:\n      required: true",
            "        2. ...\n    validations:\n      required: false",
        )
        self.assert_fails(self.forms(bug=bug))

    def test_blank_issues_enabled_true_fails(self):
        """tasks.md: blank issues must stay disabled."""
        config = mutate(CONFIG_YML, "blank_issues_enabled: false", "blank_issues_enabled: true")
        self.assert_fails(self.forms(config=config))

    def test_what_happened_not_required_fails(self):
        bug = mutate(
            BUG_REPORT_YML,
            "      description: Describe the actual behavior you observed.\n"
            "    validations:\n      required: true",
            "      description: Describe the actual behavior you observed.\n"
            "    validations:\n      required: false",
        )
        self.assert_fails(self.forms(bug=bug))

    def test_expected_field_missing_fails(self):
        bug = mutate(
            BUG_REPORT_YML,
            """  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: Describe what you expected to happen instead.
    validations:
      required: true
""",
            "",
        )
        self.assert_fails(self.forms(bug=bug))

    def test_environment_not_required_fails(self):
        bug = mutate(
            BUG_REPORT_YML,
            "      description: Project version, operating system, and any other"
            " relevant details.\n    validations:\n      required: true",
            "      description: Project version, operating system, and any other"
            " relevant details.\n    validations:\n      required: false",
        )
        self.assert_fails(self.forms(bug=bug))

    def test_feature_problem_not_required_fails(self):
        feature = mutate(
            FEATURE_REQUEST_YML,
            "      description: Describe the problem or need behind this request.\n"
            "    validations:\n      required: true",
            "      description: Describe the problem or need behind this request.\n"
            "    validations:\n      required: false",
        )
        self.assert_fails(self.forms(feature=feature))

    def test_feature_solution_not_required_fails(self):
        feature = mutate(
            FEATURE_REQUEST_YML,
            "      description: Describe what you would like to happen.\n"
            "    validations:\n      required: true",
            "      description: Describe what you would like to happen.\n"
            "    validations:\n      required: false",
        )
        self.assert_fails(self.forms(feature=feature))

    def test_empty_labels_fails(self):
        feature = mutate(FEATURE_REQUEST_YML, 'labels: ["enhancement"]', "labels: []")
        self.assert_fails(self.forms(feature=feature))

    def test_missing_description_fails(self):
        bug = mutate(
            BUG_REPORT_YML,
            "description: Report something that is not working as expected.",
            'description: ""',
        )
        self.assert_fails(self.forms(bug=bug))

    def test_single_contact_link_fails(self):
        config = mutate(
            CONFIG_YML,
            """  - name: Report a security vulnerability
    url: https://github.com/CHANGEME_OWNER/CHANGEME_REPO/security/advisories/new
    about: Please report security vulnerabilities privately, not in public issues.
""",
            "",
        )
        self.assert_fails(self.forms(config=config))

    def test_contact_link_outside_the_repository_fails(self):
        config = mutate(
            CONFIG_YML,
            "url: https://github.com/CHANGEME_OWNER/CHANGEME_REPO/discussions",
            "url: https://example.com/discussions",
        )
        self.assert_fails(self.forms(config=config))

    # -- skip ---------------------------------------------------------------

    def test_no_issue_template_files_skips(self):
        self.assert_skips({})


class CheckC07ReleaseNotesTest(CheckCase):
    """C07: ``changelog.categories`` must match project-files.md M09 exactly."""

    check_id = "C07"

    # -- pass ---------------------------------------------------------------

    def test_verbatim_release_yml_passes(self):
        self.assert_passes({RELEASE_PATH: RELEASE_YML})

    # -- fail ---------------------------------------------------------------

    def test_categories_out_of_order_fails(self):
        """tasks.md: the order of the three categories is part of the contract."""
        text = swap(
            RELEASE_YML,
            "    - title: New Features\n      labels:\n        - enhancement\n",
            "    - title: Bug Fixes\n      labels:\n        - bug\n",
        )
        self.assert_fails({RELEASE_PATH: text})

    def test_renamed_category_fails(self):
        text = mutate(RELEASE_YML, "title: New Features", "title: Features")
        self.assert_fails({RELEASE_PATH: text})

    def test_wrong_label_fails(self):
        text = mutate(RELEASE_YML, "        - enhancement", "        - feature")
        self.assert_fails({RELEASE_PATH: text})

    def test_missing_category_fails(self):
        text = mutate(
            RELEASE_YML,
            '    - title: Other Changes\n      labels:\n        - "*"\n',
            "",
        )
        self.assert_fails({RELEASE_PATH: text})

    def test_extra_category_fails(self):
        text = RELEASE_YML + "    - title: Documentation\n      labels:\n        - docs\n"
        self.assert_fails({RELEASE_PATH: text})

    # -- skip ---------------------------------------------------------------

    def test_missing_release_yml_skips(self):
        reason = self.assert_skips({})
        self.assertIn("release.yml", " ".join(reason))


class CheckC16CodeOfConductTest(CheckCase):
    """C16: the five conditions listed under project-files.md M04."""

    check_id = "C16"

    # -- pass ---------------------------------------------------------------

    def test_substituted_covenant_passes(self):
        self.assert_passes({COC_PATH: CODE_OF_CONDUCT_MD})

    # -- fail ---------------------------------------------------------------

    def test_contact_placeholder_left_in_fails(self):
        """tasks.md: `[INSERT CONTACT METHOD]` must have been substituted."""
        text = mutate(
            CODE_OF_CONDUCT_MD, "CHANGEME_CONDUCT_EMAIL", "[INSERT CONTACT METHOD]"
        )
        self.assert_fails({COC_PATH: text})

    def test_missing_version_2_1_fails(self):
        text = mutate(CODE_OF_CONDUCT_MD, "version 2.1", "version 2.0")
        self.assert_fails({COC_PATH: text})

    def test_missing_changeme_conduct_email_fails(self):
        text = mutate(
            CODE_OF_CONDUCT_MD, "CHANGEME_CONDUCT_EMAIL", "conduct@example.com"
        )
        self.assert_fails({COC_PATH: text})

    def test_front_matter_left_in_fails(self):
        text = mutate(
            CODE_OF_CONDUCT_MD,
            "\n# Contributor Covenant Code of Conduct",
            '\n+++\ntitle = "Contributor Covenant Code of Conduct"\n+++\n'
            "\n# Contributor Covenant Code of Conduct",
        )
        self.assert_fails({COC_PATH: text})

    def test_missing_attribution_section_fails(self):
        text = mutate(CODE_OF_CONDUCT_MD, "## Attribution", "## Credits")
        self.assert_fails({COC_PATH: text})

    # -- skip ---------------------------------------------------------------

    def test_missing_code_of_conduct_skips(self):
        reason = self.assert_skips({})
        self.assertIn("CODE_OF_CONDUCT.md", " ".join(reason))


class CheckC20ContributorDocumentsTest(CheckCase):
    """C20: tooling.md §1.3, "C20 Contributor documents"."""

    check_id = "C20"

    def docs(self, security=None, contributing=None, pr=None, readme=None):
        return {
            SECURITY_PATH: SECURITY_MD if security is None else security,
            CONTRIBUTING_PATH: CONTRIBUTING_MD if contributing is None else contributing,
            PR_PATH: PULL_REQUEST_TEMPLATE_MD if pr is None else pr,
            README_PATH: README_MD if readme is None else readme,
        }

    # -- pass ---------------------------------------------------------------

    def test_contract_conformant_documents_pass(self):
        self.assert_passes(self.docs())

    def test_only_readme_present_passes(self):
        """§1.1: the other three documents simply are not checked yet."""
        self.assert_passes({README_PATH: README_MD})

    # -- fail: SECURITY.md --------------------------------------------------

    def test_security_without_the_bold_warning_fails(self):
        """tasks.md: the verbatim bold sentence must be present."""
        security = mutate(
            SECURITY_MD,
            "**Please do not report security vulnerabilities through public issues,"
            " discussions, or pull requests.**",
            "Please avoid reporting security problems in public.",
        )
        self.assert_fails(self.docs(security=security))

    def test_security_without_advisory_url_fails(self):
        security = mutate(SECURITY_MD, "security/advisories/new", "security")
        self.assert_fails(self.docs(security=security))

    def test_security_without_email_placeholder_fails(self):
        security = mutate(SECURITY_MD, "CHANGEME_SECURITY_EMAIL", "security@example.com")
        self.assert_fails(self.docs(security=security))

    def test_security_without_supported_versions_heading_fails(self):
        security = mutate(SECURITY_MD, "## Supported Versions", "## Supported releases")
        self.assert_fails(self.docs(security=security))

    # -- fail: CONTRIBUTING.md ----------------------------------------------

    def test_contributing_headings_out_of_order_fails(self):
        contributing = swap(
            CONTRIBUTING_MD, "## Reporting bugs", "## Suggesting features"
        )
        self.assert_fails(self.docs(contributing=contributing))

    def test_contributing_without_changelog_link_fails(self):
        contributing = mutate(
            CONTRIBUTING_MD, "[changelog](CHANGELOG.md)", "the changelog"
        )
        self.assert_fails(self.docs(contributing=contributing))

    def test_contributing_without_code_of_conduct_link_fails(self):
        contributing = mutate(
            CONTRIBUTING_MD, "[Code of Conduct](CODE_OF_CONDUCT.md)", "Code of Conduct"
        )
        self.assert_fails(self.docs(contributing=contributing))

    def test_contributing_without_security_link_fails(self):
        contributing = mutate(
            CONTRIBUTING_MD, "[security policy](SECURITY.md)", "the security policy"
        )
        self.assert_fails(self.docs(contributing=contributing))

    def test_contributing_without_getting_started_link_fails(self):
        contributing = mutate(
            CONTRIBUTING_MD,
            "[Getting started](README.md#getting-started)",
            "the project README",
        )
        self.assert_fails(self.docs(contributing=contributing))

    def test_contributing_with_placeholder_fails(self):
        contributing = mutate(
            CONTRIBUTING_MD,
            "Thanks for your interest in this project.",
            "Thanks for your interest in CHANGEME_PROJECT_NAME.",
        )
        self.assert_fails(self.docs(contributing=contributing))

    # -- fail: .github/PULL_REQUEST_TEMPLATE.md ------------------------------

    def test_pull_request_template_with_two_checklist_items_fails(self):
        """tasks.md: the contract asks for exactly three ``- [ ] `` items."""
        pr = mutate(
            PULL_REQUEST_TEMPLATE_MD,
            "- [ ] Documentation is updated (if applicable)\n",
            "",
        )
        self.assert_fails(self.docs(pr=pr))

    def test_pull_request_template_with_four_checklist_items_fails(self):
        pr = PULL_REQUEST_TEMPLATE_MD + "- [ ] The branch is up to date with `main`\n"
        self.assert_fails(self.docs(pr=pr))

    def test_pull_request_template_without_closes_fails(self):
        pr = mutate(PULL_REQUEST_TEMPLATE_MD, "Closes #", "Fixes issue")
        self.assert_fails(self.docs(pr=pr))

    def test_pull_request_template_headings_out_of_order_fails(self):
        pr = swap(PULL_REQUEST_TEMPLATE_MD, "## Description", "## Related issue")
        self.assert_fails(self.docs(pr=pr))

    # -- fail: README.md -----------------------------------------------------

    def test_readme_without_bug_report_link_fails(self):
        readme = mutate(README_MD, "issues/new?template=bug_report.yml", "issues/new")
        self.assert_fails(self.docs(readme=readme))

    def test_readme_without_feature_request_link_fails(self):
        readme = mutate(
            README_MD, "issues/new?template=feature_request.yml", "discussions"
        )
        self.assert_fails(self.docs(readme=readme))

    # -- skip ---------------------------------------------------------------

    def test_no_contributor_documents_skips(self):
        self.assert_skips({})


if __name__ == "__main__":
    unittest.main()
