"""Run every check against the real ``template/`` directory.

Contract: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §3 -- no check
may FAIL.  When ``template/`` is not complete yet (C01 fails), the whole module
is skipped, so this file stays green while the template is still being built.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_template as ct  # noqa: E402

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "template"


def _layout_is_complete() -> bool:
    if not TEMPLATE_DIR.is_dir():
        return False
    ctx = ct.Context(template_dir=TEMPLATE_DIR)
    try:
        return not ct.CHECKS["C01"][1](ctx)
    except ct.SkipCheck:
        return False


@unittest.skipUnless(_layout_is_complete(), "template/ is not complete yet (C01 fails)")
class RealTemplateTests(unittest.TestCase):
    """Every registered check must pass or skip against the shipped template."""

    @classmethod
    def setUpClass(cls):
        cls.ctx = ct.Context(template_dir=TEMPLATE_DIR)

    def test_no_check_fails(self):
        failures = {}
        for check_id, (_title, func) in ct.CHECKS.items():
            try:
                problems = func(self.ctx)
            except ct.SkipCheck:
                continue
            if problems:
                failures[check_id] = problems
        self.assertEqual(failures, {}, f"checks reported problems: {failures}")


if __name__ == "__main__":
    unittest.main()


class RefreshPatternsMatchRealTemplateTests(unittest.TestCase):
    """``verify_sources.py``'s date patterns must match the real ``SOURCES.md``.

    These two patterns are string-matched against the labels actually written
    in the template.  When the guidance layer was converted to English the
    labels changed, but the patterns still demanded the old bilingual text, so
    ``--write`` refreshed every adoption figure while silently leaving all 17
    dates stale -- and the release gate would then reject data that had just
    been refreshed.  Nothing caught it, because the unit-test fixtures still
    carried the old bilingual labels too: the tests agreed with each other and
    with nothing else.  This test compares the patterns against the real file
    so the fixtures can never drift away from reality again.
    """

    def setUp(self) -> None:
        sources = TEMPLATE_DIR / ".github/chefs-pick/SOURCES.md"
        if not sources.is_file():
            self.skipTest("template/ has no SOURCES.md yet")
        self.text = sources.read_text(encoding="utf-8")
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        import verify_sources  # noqa: PLC0415

        self.verify_sources = verify_sources

    def test_data_verified_line_is_matched(self) -> None:
        found = self.verify_sources.DATA_VERIFIED_RE.findall(self.text)
        self.assertEqual(
            len(found),
            1,
            "DATA_VERIFIED_RE no longer matches the 'Data verified:' line in "
            "the real SOURCES.md; a refresh would leave that date stale",
        )

    def test_every_module_verified_cell_is_matched(self) -> None:
        import re

        actual = len(re.findall(r"\|\s*Verified\s*\|\s*\d{4}-\d{2}-\d{2}\s*\|", self.text))
        matched = len(self.verify_sources.VERIFIED_CELL_RE.findall(self.text))
        self.assertGreater(actual, 0, "the real SOURCES.md has no Verified cells")
        self.assertEqual(
            matched,
            actual,
            "VERIFIED_CELL_RE matches "
            f"{matched} of the {actual} module Verified cells in the real "
            "SOURCES.md; a refresh would leave the unmatched ones stale",
        )
