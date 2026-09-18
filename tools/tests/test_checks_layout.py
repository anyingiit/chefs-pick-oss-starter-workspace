"""Tests for C01 Layout, C02 No development files, C03 YAML parses, C21 Text format.

See ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.3 and §3, and
``specs/001-chefs-pick-starter/contracts/template-layout.md`` §1, §2, §5.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_template as ct  # noqa: E402
from helpers import make_ctx, run_one, write_tree  # noqa: E402


def full_layout() -> dict[str, str]:
    """Minimal content for every file C01 requires."""
    return {rel: "x\n" for rel in ct.REQUIRED_FILES}


class TestC01Layout(unittest.TestCase):
    """C01: every REQUIRED_FILES entry exists; nothing beyond REQUIRED + OPTIONAL."""

    def test_pass_all_required_files_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(tmp, full_layout())
            status, problems = run_one("C01", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_pass_optional_file_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = full_layout()
            for rel in ct.OPTIONAL_FILES:
                files[rel] = "x\n"
            root = write_tree(tmp, files)
            status, problems = run_one("C01", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_missing_required_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = full_layout()
            del files["LICENSE"]
            root = write_tree(tmp, files)
            status, problems = run_one("C01", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_unexpected_extra_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = full_layout()
            files["NOTES.md"] = "x\n"
            root = write_tree(tmp, files)
            status, problems = run_one("C01", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)


class TestC02NoDevelopmentFiles(unittest.TestCase):
    """C02: no .specify/.claude/specs/tools/.git/__pycache__/node_modules, no *.pyc."""

    def test_pass_only_project_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    "README.md": "# Project\n",
                    ".github/workflows/ci.yml": "name: CI\n",
                },
            )
            status, problems = run_one("C02", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_development_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    "README.md": "# Project\n",
                    "tools/check_template.py": "print(1)\n",
                    "specs/001-feature/spec.md": "# Spec\n",
                },
            )
            status, problems = run_one("C02", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_pyc_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    "README.md": "# Project\n",
                    "scripts/helper.pyc": "\n",
                },
            )
            status, problems = run_one("C02", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)


class TestC03YamlParses(unittest.TestCase):
    """C03: every *.yml / *.yaml file parses with yaml.safe_load."""

    def test_pass_valid_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    ".github/dependabot.yml": (
                        "version: 2\n"
                        "updates:\n"
                        '  - package-ecosystem: "github-actions"\n'
                        '    directory: "/"\n'
                        "    schedule:\n"
                        "      interval: weekly\n"
                    ),
                    ".pre-commit-config.yaml": "repos: []\n",
                },
            )
            status, problems = run_one("C03", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_broken_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    ".github/dependabot.yml": "version: 2\nupdates: [\n",
                },
            )
            status, problems = run_one("C03", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)


class TestC21TextFormat(unittest.TestCase):
    """C21: UTF-8, exactly one trailing newline, no trailing blanks, no CRLF."""

    def test_fail_crlf_line_endings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_bytes(b"a\r\nb\r\n")
            status, problems = run_one("C21", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_pass_literal_cr_inside_brackets(self):
        # .gitignore's upstream macOS rules keep a literal CR inside the
        # brackets; the line itself still ends with LF, so it is not CRLF.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".gitignore").write_bytes(
                b".DS_Store\n"
                b"Icon[\r]\n"
                b".HFS+ Private Directory Data[\r]\n"
            )
            status, problems = run_one("C21", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_trailing_whitespace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_bytes(b"# Project\ntrailing space \nend\n")
            status, problems = run_one("C21", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_missing_final_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_bytes(b"# Project\nno newline at eof")
            status, problems = run_one("C21", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)


if __name__ == "__main__":
    unittest.main()
