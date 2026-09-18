"""Tests for the automation checks: C05 (CI workflow) and C06 (Dependabot).

Contract: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.1, §1.3, §3 and
``specs/001-chefs-pick-starter/contracts/project-files.md`` M11, M12.

Every case builds only the files the check under test needs, inside a fresh
``tempfile.TemporaryDirectory()``.
"""

from __future__ import annotations

import tempfile
import unittest

from helpers import make_ctx, run_one, write_tree

CI_PATH = ".github/workflows/ci.yml"
DEPENDABOT_PATH = ".github/dependabot.yml"

# Verbatim content of project-files.md M11.
CI_YML = r"""# Source: GitHub starter workflow "Simple workflow" (MIT) — https://github.com/actions/starter-workflows/blob/main/ci/blank.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

# The workflow token is read-only by default.
# Grant extra permissions to a single job only when that job needs them.
permissions:
  contents: read

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false

      - name: Check that actions are pinned to full commit SHAs
        shell: bash
        run: |
          # Every `uses:` must reference a full 40-character commit SHA followed by a
          # version comment, for example:
          #   uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
          # Local actions (./path) and Docker images (docker://) are skipped.
          set -euo pipefail
          unpinned="$(grep -RnE '^[[:space:]]*(-[[:space:]]+)?uses:' .github/workflows \
            | grep -vE "uses:[[:space:]]*['\"]?(\./|docker://)" \
            | grep -vE "@[0-9a-f]{40}['\"]?[[:space:]]+#[[:space:]]*v?[0-9]" || true)"
          if [ -n "$unpinned" ]; then
            echo "::error::Pin these actions to a full-length commit SHA with a version comment:"
            echo "$unpinned"
            exit 1
          fi
          echo "All actions are pinned to full-length commit SHAs."

      # Add your project's linters below this line.

  test:
    name: Test
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false

      # Replace the step below with your project's test command. Pin any setup
      # action you add to a full commit SHA, like the checkout step above.
      - name: Run tests
        run: echo "No tests yet. Replace this step with your project's test command."
"""

# Verbatim content of project-files.md M12.
DEPENDABOT_YML = """# Source: GitHub Dependabot (official) — https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference
# Add an entry for each package manager your project uses (see the link above).
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
"""

# The first `uses:` line of the workflow -- the one the mutations target.
FIRST_USES = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1"


def mutate(text: str, old: str, new: str) -> str:
    """Replace the first occurrence of *old*, asserting it was present."""
    if old not in text:  # pragma: no cover - guards against a stale fixture
        raise AssertionError(f"fixture no longer contains: {old!r}")
    return text.replace(old, new, 1)


class CheckC05CIWorkflowTest(unittest.TestCase):
    """C05: project-files.md M11."""

    def run_c05(self, ci_text: str | None):
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {} if ci_text is None else {CI_PATH: ci_text})
            return run_one("C05", make_ctx(tmp))

    def assert_fails(self, ci_text: str):
        status, problems = self.run_c05(ci_text)
        self.assertEqual(status, "FAIL")
        self.assertTrue(problems, "a failing check must report at least one problem")
        return problems

    # -- pass ---------------------------------------------------------------

    def test_verbatim_workflow_passes(self):
        status, problems = self.run_c05(CI_YML)
        self.assertEqual(status, "PASS", problems)

    def test_quoted_on_key_passes(self):
        """PyYAML reads a bare ``on:`` as the boolean True; ``"on":`` stays a string.

        Both spellings must be accepted (tooling.md §1.3, C05).
        """
        text = mutate(CI_YML, "\non:\n", '\n"on":\n')
        status, problems = self.run_c05(text)
        self.assertEqual(status, "PASS", problems)

    # -- fail ---------------------------------------------------------------

    def test_action_pinned_to_version_tag_fails(self):
        self.assert_fails(mutate(CI_YML, FIRST_USES, "actions/checkout@v4"))

    def test_sha_without_version_comment_fails(self):
        text = mutate(
            CI_YML,
            FIRST_USES,
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
        )
        self.assert_fails(text)

    def test_permissions_not_read_only_fails(self):
        text = mutate(CI_YML, "permissions:\n  contents: read", "permissions:\n  contents: write")
        self.assert_fails(text)

    def test_missing_persist_credentials_fails(self):
        text = mutate(CI_YML, "\n        with:\n          persist-credentials: false", "")
        self.assert_fails(text)

    def test_missing_trigger_fails(self):
        self.assert_fails(mutate(CI_YML, "  workflow_dispatch:\n", ""))

    def test_missing_job_fails(self):
        self.assert_fails(mutate(CI_YML, "  lint:\n    name: Lint", "  build:\n    name: Build"))

    # -- skip ---------------------------------------------------------------

    def test_missing_workflow_skips(self):
        status, reason = self.run_c05(None)
        self.assertEqual(status, "SKIP")
        self.assertIn("ci.yml", " ".join(reason))


class CheckC06DependabotTest(unittest.TestCase):
    """C06: version 2 plus a github-actions entry for "/" with a schedule."""

    def run_c06(self, text: str | None):
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {} if text is None else {DEPENDABOT_PATH: text})
            return run_one("C06", make_ctx(tmp))

    def assert_fails(self, text: str):
        status, problems = self.run_c06(text)
        self.assertEqual(status, "FAIL")
        self.assertTrue(problems, "a failing check must report at least one problem")
        return problems

    # -- pass ---------------------------------------------------------------

    def test_verbatim_dependabot_passes(self):
        status, problems = self.run_c06(DEPENDABOT_YML)
        self.assertEqual(status, "PASS", problems)

    # -- fail ---------------------------------------------------------------

    def test_wrong_version_fails(self):
        self.assert_fails(mutate(DEPENDABOT_YML, "version: 2", "version: 1"))

    def test_no_github_actions_entry_fails(self):
        text = mutate(
            DEPENDABOT_YML,
            'package-ecosystem: "github-actions"',
            'package-ecosystem: "npm"',
        )
        self.assert_fails(text)

    def test_wrong_directory_fails(self):
        self.assert_fails(mutate(DEPENDABOT_YML, 'directory: "/"', 'directory: "/subdir"'))

    def test_empty_interval_fails(self):
        self.assert_fails(mutate(DEPENDABOT_YML, 'interval: "weekly"', 'interval: ""'))

    # -- skip ---------------------------------------------------------------

    def test_missing_dependabot_skips(self):
        status, reason = self.run_c06(None)
        self.assertEqual(status, "SKIP")
        self.assertIn("dependabot.yml", " ".join(reason))


if __name__ == "__main__":
    unittest.main()
