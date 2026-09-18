"""Execute the CI workflow's SHA-pinning guard against the two fixtures.

Pulls the ``run`` script out of the step named "Check that actions are pinned
to full commit SHAs" in ``template/.github/workflows/ci.yml`` and runs it with
bash inside a throwaway repository built from each fixture.  See
``specs/001-chefs-pick-starter/contracts/tooling.md`` §3 and
``specs/001-chefs-pick-starter/quickstart.md`` appendix A.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml  # noqa: E402

TESTS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = TESTS_DIR / "fixtures"
REPO_ROOT = TESTS_DIR.parents[1]
CI_YML = REPO_ROOT / "template" / ".github" / "workflows" / "ci.yml"

STEP_NAME = "Check that actions are pinned to full commit SHAs"
WORKFLOW_REL = ".github/workflows/ci.yml"


def pin_script() -> str:
    """Return the ``run`` script of the pinning step in the CI workflow."""
    workflow = yaml.safe_load(CI_YML.read_text(encoding="utf-8"))
    for job in (workflow.get("jobs") or {}).values():
        for step in (job or {}).get("steps") or []:
            if isinstance(step, dict) and step.get("name") == STEP_NAME:
                return step["run"]
    raise AssertionError(f"no step named {STEP_NAME!r} in {CI_YML}")


@unittest.skipUnless(CI_YML.is_file(), f"{WORKFLOW_REL} does not exist yet")
class CiPinCheckTest(unittest.TestCase):
    """Run the extracted script over the good and bad sample workflows."""

    def run_on_fixture(self, fixture: str) -> subprocess.CompletedProcess:
        script = pin_script()
        with tempfile.TemporaryDirectory() as tmp:
            workflow = Path(tmp) / WORKFLOW_REL
            workflow.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(FIXTURES_DIR / fixture, workflow)
            return subprocess.run(
                ["bash", "-c", script],
                cwd=tmp,
                capture_output=True,
                text=True,
            )

    def test_pinned_workflow_passes(self):
        result = self.run_on_fixture("pin_good.yml")
        self.assertEqual(
            result.returncode,
            0,
            f"expected success\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_unpinned_workflow_fails_with_three_findings(self):
        result = self.run_on_fixture("pin_bad.yml")
        output = result.stdout + result.stderr
        self.assertEqual(
            result.returncode, 1, f"expected exit code 1\noutput:\n{output}"
        )
        # ``grep -Rn`` prints the full relative path, so match by containment.
        reported = [line for line in output.splitlines() if f"{WORKFLOW_REL}:" in line]
        self.assertEqual(len(reported), 3, f"expected 3 findings, got:\n{output}")
        joined = "\n".join(reported)
        for needle in ("actions/checkout@v4", "setup-node", "other/action@main"):
            self.assertIn(needle, joined)


if __name__ == "__main__":
    unittest.main()
