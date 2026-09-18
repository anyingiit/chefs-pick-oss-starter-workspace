"""Tests for C19 (team upgrade guide).

Contract: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.3 (C19) and
§3 (pass, fail, and SKIP when the file is absent);
``specs/001-chefs-pick-starter/contracts/guidance-layer.md`` §6 (the three
level-2 headings of ``UPGRADE-TO-TEAM.md``, matched on their English part).

``UPGRADE-TO-TEAM.md`` is optional P4 content, so its absence is a SKIP rather
than a FAIL.  Every case builds only that one file inside a fresh
``tempfile.TemporaryDirectory()``, generating it from ``check_template``'s own
``UPGRADE_HEADINGS`` constant so the fixtures cannot drift.
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


UPGRADE_PATH = f"{ct.GUIDANCE_DIR}/UPGRADE-TO-TEAM.md"

# The English fragment C19 matches on -> the Chinese half of the bilingual
# heading in guidance-layer.md §6.  Unknown fragments fall back to an
# English-only heading, which still carries the fragment.
CHINESE_HALF = {
    "Common additions": "常用增强项",
    "When to upgrade": "何时升级",
    "When you need foundation-level governance": "需要基金会级治理时",
    "What to add": "需要添加的内容",
    "No longer recommended": "不再推荐",
    "What not to add": "不需要添加的内容",
}

TITLE = "# 升级为团队项目 / Growing into a team project"


def heading(english: str) -> str:
    """The bilingual level-2 heading carrying *english*, as §6 writes them."""
    chinese = CHINESE_HALF.get(english)
    return f"## {chinese} / {english}" if chinese else f"## {english}"


def upgrade_md(headings) -> str:
    """A minimal UPGRADE-TO-TEAM.md containing exactly *headings*."""
    parts = [
        TITLE,
        "",
        "本页是可选的简要参考，5 分钟内可以读完。",
        "This page is an optional short reference; it reads in five minutes.",
        "",
    ]
    for english in headings:
        parts.append(heading(english))
        parts.append("")
        parts.append(f"说明 / Notes for {english}.")
        parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


class TestC19TeamUpgradeGuide(unittest.TestCase):
    """C19: UPGRADE-TO-TEAM.md carries the three level-2 headings of §6."""

    def setUp(self) -> None:
        # Guard the fixtures against a drifting constant: §1.3 requires three.
        self.assertEqual(len(ct.UPGRADE_HEADINGS), 3)

    def test_all_three_headings_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {UPGRADE_PATH: upgrade_md(ct.UPGRADE_HEADINGS)})
            status, problems = run_one("C19", make_ctx(tmp))
        self.assertEqual(status, "PASS", problems)

    def test_missing_one_heading_fails(self) -> None:
        kept = list(ct.UPGRADE_HEADINGS)[:-1]
        self.assertEqual(len(kept), 2)
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {UPGRADE_PATH: upgrade_md(kept)})
            status, problems = run_one("C19", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(problems)

    def test_missing_middle_heading_fails(self) -> None:
        kept = [ct.UPGRADE_HEADINGS[0], ct.UPGRADE_HEADINGS[2]]
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {UPGRADE_PATH: upgrade_md(kept)})
            status, problems = run_one("C19", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(problems)

    def test_missing_file_skips(self) -> None:
        """§1.3: the page is optional P4 content, so absence is SKIP."""
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {f"{ct.GUIDANCE_DIR}/GUIDE.md": "# Guide\n"})
            status, reason = run_one("C19", make_ctx(tmp))
        self.assertEqual(status, "SKIP", reason)
        self.assertIn("UPGRADE-TO-TEAM.md", " ".join(reason))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
