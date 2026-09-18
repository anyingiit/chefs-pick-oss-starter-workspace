"""Tests for C18 (maintenance guide).

Contract: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.1 (missing
files are SKIP, reported only by C01), §1.3 (C18) and §3;
``specs/001-chefs-pick-starter/contracts/guidance-layer.md`` §5 (the six level-2
headings of ``MAINTAINING.md``, matched on their English part, one of which is
``Action updates``).

Every case builds only ``.github/chefs-pick/MAINTAINING.md`` -- the single file
C18 depends on -- inside a fresh ``tempfile.TemporaryDirectory()``.  Fixtures are
generated from ``check_template``'s own ``MAINTAINING_HEADINGS`` constant so that
they cannot drift away from the list the check matches against.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import make_ctx, run_one, write_tree  # noqa: E402

import check_template as ct  # noqa: E402


MAINTAINING_PATH = f"{ct.GUIDANCE_DIR}/MAINTAINING.md"

# The English fragment C18 matches on -> the Chinese half of the bilingual
# heading it is written with in guidance-layer.md §5.  Unknown fragments fall
# back to an English-only heading, which still carries the fragment, so a change
# to MAINTAINING_HEADINGS can never silently break the fixtures.
CHINESE_HALF = {
    "Review cadence": "复核周期",
    "Review cycle": "复核周期",
    "How to review": "复核步骤",
    "Refreshing the data": "刷新数据",
    "Re-evaluation triggers": "重新评估的触发条件",
    "Changing a pick": "变更选型",
    "Action updates": "动作版本更新",
    "Recording changes": "变更记录规则",
    "Release gates": "发布门禁",
    "Release steps": "发布步骤",
}

TITLE = "# 维护说明 / Maintaining this template"


def heading(english: str) -> str:
    """The bilingual level-2 heading carrying *english*, as §5 writes them."""
    chinese = CHINESE_HALF.get(english)
    return f"## {chinese} / {english}" if chinese else f"## {english}"


def maintaining_md(headings) -> str:
    """A minimal MAINTAINING.md containing exactly *headings*."""
    parts = [TITLE, ""]
    for english in headings:
        parts.append(heading(english))
        parts.append("")
        parts.append(f"说明 / Notes for {english}.")
        parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


class TestC18MaintenanceGuide(unittest.TestCase):
    """C18: MAINTAINING.md carries the six level-2 headings of §5."""

    def setUp(self) -> None:
        # Guard the fixtures against a drifting constant: §1.3 requires six
        # headings and names ``Action updates`` explicitly.
        self.assertEqual(len(ct.MAINTAINING_HEADINGS), 6)
        self.assertIn("Action updates", ct.MAINTAINING_HEADINGS)

    def test_all_six_headings_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {MAINTAINING_PATH: maintaining_md(ct.MAINTAINING_HEADINGS)},
            )
            status, problems = run_one("C18", make_ctx(tmp))
        self.assertEqual(status, "PASS", problems)

    def test_missing_action_updates_fails(self) -> None:
        """§1.3 names ``Action updates`` explicitly, so it gets its own case."""
        kept = [h for h in ct.MAINTAINING_HEADINGS if h != "Action updates"]
        self.assertEqual(len(kept), 5)
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {MAINTAINING_PATH: maintaining_md(kept)})
            status, problems = run_one("C18", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(problems)

    def test_missing_last_heading_fails(self) -> None:
        kept = list(ct.MAINTAINING_HEADINGS)[:-1]
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {MAINTAINING_PATH: maintaining_md(kept)})
            status, problems = run_one("C18", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(problems)

    def test_headings_demoted_to_level_three_fail(self) -> None:
        """§5 asks for level-2 headings; deeper ones do not satisfy C18."""
        text = maintaining_md(ct.MAINTAINING_HEADINGS).replace("\n## ", "\n### ")
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {MAINTAINING_PATH: text})
            status, problems = run_one("C18", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(problems)

    def test_missing_file_skips(self) -> None:
        """§1.1: a check whose only file is absent is SKIP, not FAIL."""
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {f"{ct.GUIDANCE_DIR}/GUIDE.md": "# Guide\n"})
            status, reason = run_one("C18", make_ctx(tmp))
        self.assertEqual(status, "SKIP", reason)
        self.assertIn("MAINTAINING.md", " ".join(reason))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
