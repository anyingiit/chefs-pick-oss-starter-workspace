"""Tests for C08 (Placeholders) and C09 (Source comments).

Contracts: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.3,
``contracts/markers.md`` §1 and §2, ``contracts/guidance-layer.md`` §2.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from helpers import make_ctx, run_one, write_tree  # noqa: E402

import check_template as ct  # noqa: E402


SETUP_PATH = ".github/chefs-pick/SETUP.md"
GUIDE_PATH = ".github/chefs-pick/GUIDE.md"


def setup_md(registry: dict[str, list[str]]) -> str:
    """Build a SETUP.md whose placeholder table lists *registry*.

    The header is verbatim from guidance-layer.md §2; columns 1 and 3 hold
    their values in backticks so ``parse_placeholder_registry`` can read them.
    """
    lines = [
        "# 起步清单 / Setup checklist",
        "",
        "## 占位符 / Placeholders",
        "",
        ct.PLACEHOLDER_TABLE_HEADER,
        "|---|---|---|---|",
    ]
    for name, files in registry.items():
        cell = "、".join(f"`{rel}`" for rel in files)
        lines.append(f"| `{name}` | 含义 / Meaning | {cell} | `example` |")
    lines += ["", "## 步骤 / Steps", "", "S01 … S09", ""]
    return "\n".join(lines)


def source_line(rel_path: str) -> str:
    return ct.SOURCE_COMMENTS[rel_path]


LICENSE_BODY = (
    "MIT License\n"
    "\n"
    "Copyright (c) CHANGEME_YEAR CHANGEME_COPYRIGHT_HOLDER\n"
    "\n"
    'Permission is hereby granted, free of charge, to any person obtaining a copy.\n'
)


class TestPlaceholderTableFixture(unittest.TestCase):
    """The fixture builder must produce a table the parser understands."""

    def test_table_round_trips_through_parser(self):
        text = setup_md(
            {
                "CHANGEME_OWNER": ["README.md", "SECURITY.md"],
                "CHANGEME_PROJECT_NAME": ["README.md"],
            }
        )
        self.assertEqual(
            ct.parse_placeholder_registry(text),
            {
                "CHANGEME_OWNER": {"README.md", "SECURITY.md"},
                "CHANGEME_PROJECT_NAME": {"README.md"},
            },
        )


class TestC08Placeholders(unittest.TestCase):
    def test_pass(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    SETUP_PATH: setup_md(
                        {
                            "CHANGEME_OWNER": ["README.md", "SECURITY.md"],
                            "CHANGEME_PROJECT_NAME": ["README.md"],
                        }
                    ),
                    "README.md": "# CHANGEME_PROJECT_NAME\n\nBy CHANGEME_OWNER.\n",
                    "SECURITY.md": "# Security\n\nSee CHANGEME_OWNER.\n",
                },
            )
            status, problems = run_one("C08", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_pass_ignores_registered_files_that_do_not_exist_yet(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    SETUP_PATH: setup_md(
                        {"CHANGEME_OWNER": ["README.md", "SECURITY.md"]}
                    ),
                    "README.md": "# Demo\n\nBy CHANGEME_OWNER.\n",
                },
            )
            status, problems = run_one("C08", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_unregistered_placeholder(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    SETUP_PATH: setup_md({"CHANGEME_OWNER": ["README.md"]}),
                    "README.md": "# Demo\n\nBy CHANGEME_OWNER for CHANGEME_MYSTERY.\n",
                },
            )
            status, problems = run_one("C08", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_legacy_marker_in_project_file(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    SETUP_PATH: setup_md({"CHANGEME_OWNER": ["README.md"]}),
                    "README.md": "# Demo\n\nBy CHANGEME_OWNER.\n",
                    "CONTRIBUTING.md": (
                        "# Contributing\n\nOpen https://github.com/github_username/x.\n"
                    ),
                },
            )
            status, problems = run_one("C08", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_changeme_in_guidance_file_other_than_setup(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    SETUP_PATH: setup_md({"CHANGEME_OWNER": ["README.md"]}),
                    GUIDE_PATH: (
                        "# 模块讲解 / Module guide\n\n把 CHANGEME_OWNER 换成你的账号。\n"
                    ),
                    "README.md": "# Demo\n\nBy CHANGEME_OWNER.\n",
                },
            )
            status, problems = run_one("C08", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_registered_file_set_does_not_match(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    SETUP_PATH: setup_md(
                        {"CHANGEME_OWNER": ["README.md", "SECURITY.md"]}
                    ),
                    "README.md": "# Demo\n\nBy CHANGEME_OWNER.\n",
                    # SECURITY.md exists but never uses the placeholder.
                    "SECURITY.md": "# Security\n\nNothing to see here.\n",
                },
            )
            status, problems = run_one("C08", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_files_skips_the_file_set_comparison(self):
        """With --files, the "actual files == column 3" comparison is dropped."""
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    SETUP_PATH: setup_md(
                        {"CHANGEME_OWNER": ["README.md", "SECURITY.md"]}
                    ),
                    "README.md": "# Demo\n\nBy CHANGEME_OWNER.\n",
                    "SECURITY.md": "# Security\n\nNothing to see here.\n",
                },
            )
            status, problems = run_one(
                "C08", make_ctx(root, files={"README.md"})
            )
            self.assertEqual(status, "PASS", problems)

    def test_files_still_reports_unregistered_placeholders(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    SETUP_PATH: setup_md({"CHANGEME_OWNER": ["README.md"]}),
                    "README.md": "# Demo\n\nBy CHANGEME_OWNER for CHANGEME_MYSTERY.\n",
                },
            )
            status, problems = run_one(
                "C08", make_ctx(root, files={"README.md"})
            )
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_skip_without_setup_md(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(root, {"README.md": "# Demo\n\nBy CHANGEME_OWNER.\n"})
            status, _reason = run_one("C08", make_ctx(root))
            self.assertEqual(status, "SKIP")


class TestC09SourceComments(unittest.TestCase):
    def test_pass(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    "README.md": source_line("README.md") + "\n\n# Demo\n",
                    ".gitignore": source_line(".gitignore") + "\n\n*.log\n",
                    ".github/workflows/ci.yml": (
                        source_line(".github/workflows/ci.yml") + "\nname: CI\n"
                    ),
                    "LICENSE": LICENSE_BODY,
                },
            )
            status, problems = run_one("C09", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_first_line_does_not_match_registry(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    "README.md": "<!-- Source: somewhere else -->\n\n# Demo\n",
                    "LICENSE": LICENSE_BODY,
                },
            )
            status, problems = run_one("C09", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_source_comment_not_on_the_first_line(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    "README.md": "# Demo\n\n" + source_line("README.md") + "\n",
                },
            )
            status, problems = run_one("C09", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_license_first_line(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    "README.md": source_line("README.md") + "\n\n# Demo\n",
                    "LICENSE": "The MIT License (MIT)\n\nCopyright (c) 2026 Ada\n",
                },
            )
            status, problems = run_one("C09", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_files_limits_the_scope(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(
                root,
                {
                    # Wrong, but not selected.
                    "README.md": "<!-- Source: somewhere else -->\n\n# Demo\n",
                    "LICENSE": LICENSE_BODY,
                },
            )
            status, problems = run_one("C09", make_ctx(root, files={"LICENSE"}))
            self.assertEqual(status, "PASS", problems)

    def test_skip_when_no_relevant_file_exists(self):
        with tempfile.TemporaryDirectory() as root:
            write_tree(root, {SETUP_PATH: setup_md({})})
            status, _reason = run_one("C09", make_ctx(root))
            self.assertEqual(status, "SKIP")


if __name__ == "__main__":
    unittest.main()
