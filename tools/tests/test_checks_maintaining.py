"""Tests for C18 (maintenance guide).

Contract: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.1 (missing
files are SKIP, reported only by C01), §1.3 (C18) and §3;
``specs/001-chefs-pick-starter/contracts/guidance-layer.md`` §5 (the six level-2
headings of ``MAINTAINING.md``, matched on their English part, one of which is
``Action updates``); ``specs/002-english-first-docs/contracts/tooling-delta.md``
§4 C18 (the headings' literals are now English-only, and two new assertions:
the ``## Release gates`` section must have exactly 6 ordered-list items, and
the page must mention ``--update-digests``).

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

TITLE = "# Maintaining this template"

# tooling-delta.md §4 C18 (research.md R9): the page must mention this flag
# somewhere -- put it under "Action updates", where it belongs in the real
# template.
DIGESTS_MENTION = (
    "Run `python3 tools/check_template.py --update-digests` after editing "
    "a translation's English source."
)


def maintaining_md(headings, *, gate_items: int = 6, mention_digests: bool = True) -> str:
    """A minimal MAINTAINING.md containing exactly *headings*.

    ``## Release gates``, when present among *headings*, gets *gate_items*
    ordered-list items (tooling-delta.md §4 C18 wants exactly 6).
    ``--update-digests`` is mentioned under ``## Action updates`` when
    *mention_digests* is true and that heading is present.
    """
    parts = [TITLE, ""]
    for english in headings:
        parts.append(f"## {english}")
        parts.append("")
        if english == "Release gates":
            for index in range(1, gate_items + 1):
                parts.append(f"{index}. Gate item {index}.")
            parts.append("")
        elif english == "Action updates" and mention_digests:
            parts.append(DIGESTS_MENTION)
            parts.append("")
        else:
            parts.append(f"Notes for {english}.")
            parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


class TestC18MaintenanceGuide(unittest.TestCase):
    """C18: MAINTAINING.md carries the six level-2 headings of §5, a
    six-item ``Release gates`` list, and a mention of ``--update-digests``."""

    def setUp(self) -> None:
        # Guard the fixtures against a drifting constant: §1.3 requires six
        # headings and names ``Action updates`` explicitly; tooling-delta.md
        # §4 C18 additionally depends on ``Release gates`` being one of them.
        self.assertEqual(len(ct.MAINTAINING_HEADINGS), 6)
        self.assertIn("Action updates", ct.MAINTAINING_HEADINGS)
        self.assertIn("Release gates", ct.MAINTAINING_HEADINGS)

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

    def test_release_gates_with_five_items_fails(self) -> None:
        """tooling-delta.md §4 C18: exactly 6 ordered-list items are required
        under ``## Release gates`` -- five is not enough."""
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    MAINTAINING_PATH: maintaining_md(
                        ct.MAINTAINING_HEADINGS, gate_items=5
                    )
                },
            )
            status, problems = run_one("C18", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(problems)

    def test_missing_update_digests_mention_fails(self) -> None:
        """tooling-delta.md §4 C18: the page must mention ``--update-digests``
        somewhere; a page that never does must FAIL."""
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    MAINTAINING_PATH: maintaining_md(
                        ct.MAINTAINING_HEADINGS, mention_digests=False
                    )
                },
            )
            status, problems = run_one("C18", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(problems)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
