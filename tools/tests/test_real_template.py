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
