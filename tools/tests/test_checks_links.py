"""Tests for C13 Cleanup simulation, C14 Relative links, C15 License,
C17 Removal notes and C22 Removal simulation.

See ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.1, §1.3 and §3,
``specs/001-chefs-pick-starter/contracts/template-layout.md`` §3 and §6,
``specs/001-chefs-pick-starter/contracts/project-files.md`` M02, and
``specs/002-english-first-docs/contracts/tooling-delta.md`` §4 (the new
``CLEANUP_COMMAND`` and deleted-file set for C13/C22, and C17's English
literals) and §8.3 (``_iter_links`` stripping fenced code blocks before C14
looks for link targets).
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_template as ct  # noqa: E402
from helpers import make_ctx, run_one, write_tree  # noqa: E402


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

# project-files.md M02: the MIT text with the two upstream placeholders
# replaced.  Line 1 is ``MIT License``, line 3 the copyright line.
MIT_LICENSE = """MIT License

Copyright (c) 2026 anyingiit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# guidance-layer.md §2: SETUP.md's placeholder registry, parsed by
# ``ct.parse_placeholder_registry``.
SETUP_MD = (
    "# 起步设置 / Setup\n"
    "\n"
    "## 占位符 / Placeholders\n"
    "\n"
    + ct.PLACEHOLDER_TABLE_HEADER
    + "\n"
    "|---|---|---|---|\n"
    "| `Chefs Pick Oss Starter Workspace` | 项目名称 / Project name | `README.md` | `my-project` |\n"
    "| `2026` | 版权年份 / Copyright year | `LICENSE` | `2026` |\n"
    "| `anyingiit` | 版权人 / Copyright holder | `LICENSE` | `Ada Lovelace` |\n"
)

# M12, verbatim from project-files.md; satisfies C06.
DEPENDABOT_YML = (
    ct.SOURCE_COMMENTS[".github/dependabot.yml"] + "\n"
    "# Add an entry for each package manager your project uses (see the link above).\n"
    "version: 2\n"
    "updates:\n"
    '  - package-ecosystem: "github-actions"\n'
    '    directory: "/"\n'
    "    schedule:\n"
    '      interval: "weekly"\n'
)


def cleanup_tree() -> dict[str, str]:
    """A template that is clean once the guidance layer is removed (C13)."""
    return {
        "README.md": (
            "# Chefs Pick Oss Starter Workspace\n"
            "\n"
            "A short description.\n"
            "\n"
            "Released under the [MIT License](LICENSE).\n"
        ),
        "LICENSE": MIT_LICENSE,
        ct.GUIDANCE_FILE: (
            ct.GUIDANCE_HOME_TITLE + "\n"
            "\n"
            "先读 chefs-pick/SETUP.md / Start with chefs-pick/SETUP.md.\n"
            "\n"
            "```sh\n"
            + ct.CLEANUP_COMMAND + "\n"
            "```\n"
        ),
        ct.GUIDANCE_DIR + "/SETUP.md": SETUP_MD,
    }


# --------------------------------------------------------------------------
# C13 Cleanup simulation
# --------------------------------------------------------------------------


class TestC13CleanupSimulation(unittest.TestCase):
    """tooling.md §1.3 C13; template-layout.md §3."""

    def test_pass_nothing_left_behind_after_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(tmp, cleanup_tree())
            status, problems = run_one("C13", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_project_file_still_mentions_chefs_pick_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = cleanup_tree()
            files["README.md"] += (
                "\nSetup notes live in chefs-pick/SETUP.md.\n"
            )
            root = write_tree(tmp, files)
            status, problems = run_one("C13", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_project_file_keeps_template_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = cleanup_tree()
            files["README.md"] += "\nGenerated from Chef's Pick OSS Starter.\n"
            root = write_tree(tmp, files)
            status, problems = run_one("C13", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_unregistered_placeholder_survives_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = cleanup_tree()
            files["README.md"] += "\nContact CHANGEME_CONTACT_EMAIL.\n"
            root = write_tree(tmp, files)
            status, problems = run_one("C13", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_project_file_still_links_to_readme_zh_cn(self):
        """tooling-delta.md §4 C13/C22: the deleted set now also includes
        ``.github/README.zh-CN.md``; a surviving link to it must FAIL."""
        with tempfile.TemporaryDirectory() as tmp:
            files = cleanup_tree()
            files["README.md"] += (
                "\nRead this in [Chinese](.github/README.zh-CN.md) too.\n"
            )
            root = write_tree(tmp, files)
            status, problems = run_one("C13", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_skip_without_root_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = cleanup_tree()
            del files["README.md"]
            root = write_tree(tmp, files)
            status, _reason = run_one("C13", make_ctx(root))
            self.assertEqual(status, "SKIP")

    def test_skip_without_setup_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = cleanup_tree()
            del files[ct.GUIDANCE_DIR + "/SETUP.md"]
            root = write_tree(tmp, files)
            status, _reason = run_one("C13", make_ctx(root))
            self.assertEqual(status, "SKIP")


# --------------------------------------------------------------------------
# C14 Relative links
# --------------------------------------------------------------------------


class TestC14RelativeLinks(unittest.TestCase):
    """tooling.md §1.3 C14."""

    def test_pass_all_targets_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    "README.md": (
                        "# Project\n"
                        "\n"
                        "- [License](LICENSE)\n"
                        "- [Contributing](CONTRIBUTING.md#ways-to-contribute)\n"
                        "- [Bug report](.github/ISSUE_TEMPLATE/bug_report.yml)\n"
                        "- [Upstream](https://example.com/docs)\n"
                        "- [Mail](mailto:maintainer@example.com)\n"
                        "- [Top](#project)\n"
                        '- <a href="CONTRIBUTING.md">Contributing</a>\n'
                    ),
                    "CONTRIBUTING.md": (
                        "# Contributing\n"
                        "\n"
                        "## Ways to contribute\n"
                        "\n"
                        "Back to the [README](README.md).\n"
                    ),
                    "LICENSE": MIT_LICENSE,
                    ".github/ISSUE_TEMPLATE/bug_report.yml": "name: Bug report\n",
                },
            )
            status, problems = run_one("C14", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_pass_link_to_a_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    "README.md": "# Project\n\nSee [workflows](.github/workflows).\n",
                    ".github/workflows/ci.yml": "name: CI\n",
                },
            )
            status, problems = run_one("C14", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_relative_link_target_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    "README.md": (
                        "# Project\n"
                        "\n"
                        "See the [contributing guide](CONTRIBUTING.md).\n"
                    ),
                    "LICENSE": MIT_LICENSE,
                },
            )
            status, problems = run_one("C14", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_href_target_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    "README.md": '# Project\n\n<a href="docs/usage.md">Usage</a>\n',
                },
            )
            status, problems = run_one("C14", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_pass_fenced_code_block_link_is_ignored(self):
        """tooling-delta.md §8.3: ``_iter_links`` strips fenced code blocks,
        so a tutorial snippet showing the language-selector syntax (which
        points at a file that does not exist alongside the guide) is not
        treated as a real link."""
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    ct.GUIDANCE_DIR + "/GUIDE.md": (
                        "# Module guide\n"
                        "\n"
                        "## Translating your own README\n"
                        "\n"
                        "Add a language selector like this:\n"
                        "\n"
                        "```markdown\n"
                        "[English](README.md) · **简体中文**\n"
                        "```\n"
                    ),
                },
            )
            status, problems = run_one("C14", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_pass_tilde_fenced_code_block_link_is_ignored(self):
        # FIXED (Finding 5): ``_strip_fenced_code`` used to recognise only
        # backtick fences, so a ``~~~`` block's relative-link-looking
        # content reached C14 as if it were real prose. It must be
        # stripped exactly like a backtick fence is.
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    ct.GUIDANCE_DIR + "/GUIDE.md": (
                        "# Module guide\n"
                        "\n"
                        "## Translating your own README\n"
                        "\n"
                        "Add a language selector like this:\n"
                        "\n"
                        "~~~markdown\n"
                        "[English](README.md) · **简体中文**\n"
                        "~~~\n"
                    ),
                },
            )
            status, problems = run_one("C14", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_project_file_links_into_guidance_layer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(
                tmp,
                {
                    "README.md": (
                        "# Project\n"
                        "\n"
                        "See the [module guide](.github/chefs-pick/GUIDE.md).\n"
                    ),
                    ct.GUIDANCE_DIR + "/GUIDE.md": "# 模块指南 / Module guide\n",
                },
            )
            status, problems = run_one("C14", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)


# --------------------------------------------------------------------------
# C15 License
# --------------------------------------------------------------------------


class TestC15License(unittest.TestCase):
    """tooling.md §1.3 C15; project-files.md M02."""

    def test_pass_verbatim_mit_license(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(tmp, {"LICENSE": MIT_LICENSE})
            status, problems = run_one("C15", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_copyright_line_not_placeholderised(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = MIT_LICENSE.replace(
                "Copyright (c) 2026 anyingiit",
                "Copyright (c) 2026 Example Maintainer",
            )
            root = write_tree(tmp, {"LICENSE": text})
            status, problems = run_one("C15", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_upstream_brackets_left_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = MIT_LICENSE.replace(
                "Copyright (c) 2026 anyingiit",
                "Copyright (c) [year] [fullname]",
            )
            root = write_tree(tmp, {"LICENSE": text})
            status, problems = run_one("C15", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_warranty_paragraph_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = MIT_LICENSE.split('THE SOFTWARE IS PROVIDED "AS IS"')[0]
            root = write_tree(tmp, {"LICENSE": text})
            status, problems = run_one("C15", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_skip_without_license(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(tmp, {"README.md": "# Project\n"})
            status, _reason = run_one("C15", make_ctx(root))
            self.assertEqual(status, "SKIP")


# --------------------------------------------------------------------------
# C17 Removal notes
# --------------------------------------------------------------------------


def guide_md(sections: dict[str, list[str]]) -> str:
    """A GUIDE.md whose ``## Mxx`` sections name the referring files.

    tooling-delta.md §4 C17: the ``### Remove`` sub-section's literals are
    now English (``- Delete:``, ``- Update:``, ``- What you lose:``).
    """
    parts = ["# Module guide\n"]
    for module in sorted(sections):
        refs = sections[module]
        listed = ", ".join(f"`{ref}`" for ref in refs) if refs else "no other file"
        parts.append(
            f"\n## {module} module\n"
            "\n"
            "### Remove\n"
            "\n"
            "- Delete: the files of this module.\n"
            f"- Update: {listed}.\n"
            "- What you lose: the guidance this module provided.\n"
        )
    return "".join(parts)


def default_sections() -> dict[str, list[str]]:
    """The referrers template-layout.md §6 records, i.e. ``ct.REMOVAL_REFS``."""
    return {module: list(refs) for module, (_files, refs) in ct.REMOVAL_REFS.items()}


def removal_notes_tree(sections: dict[str, list[str]] | None = None) -> dict[str, str]:
    """M04 and M05 present, each referenced by the files template-layout §6 lists."""
    if sections is None:
        sections = default_sections()
    return {
        "README.md": (
            "# Project\n"
            "\n"
            "- [Code of conduct](CODE_OF_CONDUCT.md)\n"
            "- [Contributing](CONTRIBUTING.md)\n"
        ),
        "CONTRIBUTING.md": (
            "# Contributing\n"
            "\n"
            "## Code of Conduct\n"
            "\n"
            "This project follows [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).\n"
        ),
        "CODE_OF_CONDUCT.md": "# Contributor Covenant Code of Conduct\n",
        ct.GUIDANCE_DIR + "/GUIDE.md": guide_md(sections),
    }


class TestC17RemovalNotes(unittest.TestCase):
    """tooling.md §1.3 C17; template-layout.md §6."""

    def test_pass_every_referrer_listed_in_its_module_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(tmp, removal_notes_tree())
            status, problems = run_one("C17", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_m04_section_omits_contributing(self):
        with tempfile.TemporaryDirectory() as tmp:
            sections = default_sections()
            sections["M04"] = ["README.md"]
            root = write_tree(tmp, removal_notes_tree(sections))
            status, problems = run_one("C17", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_auto_discovered_referrer_not_mentioned(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = removal_notes_tree()
            # SECURITY.md (M06) also refers to CODE_OF_CONDUCT.md, but the M04
            # section does not mention SECURITY.md.
            files["SECURITY.md"] = (
                "# Security Policy\n"
                "\n"
                "Reporters are held to CODE_OF_CONDUCT.md as well.\n"
            )
            root = write_tree(tmp, files)
            status, problems = run_one("C17", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_skip_without_guide(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = removal_notes_tree()
            del files[ct.GUIDANCE_DIR + "/GUIDE.md"]
            root = write_tree(tmp, files)
            status, _reason = run_one("C17", make_ctx(root))
            self.assertEqual(status, "SKIP")


# --------------------------------------------------------------------------
# C22 Removal simulation
# --------------------------------------------------------------------------


def removal_sim_tree() -> dict[str, str]:
    """M04 and M12 present; deleting either leaves the rest working."""
    return {
        "README.md": (
            "# Project\n"
            "\n"
            "- [Code of conduct](CODE_OF_CONDUCT.md)\n"
            "- [License](LICENSE)\n"
        ),
        "LICENSE": MIT_LICENSE,
        "CODE_OF_CONDUCT.md": "# Contributor Covenant Code of Conduct\n",
        ".github/dependabot.yml": DEPENDABOT_YML,
    }


class TestC22RemovalSimulation(unittest.TestCase):
    """tooling.md §1.3 C22 (M04-M16 with files; M10 has none)."""

    def test_pass_each_module_can_be_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = write_tree(tmp, removal_sim_tree())
            status, problems = run_one("C22", make_ctx(root))
            self.assertEqual(status, "PASS", problems)

    def test_fail_yaml_config_still_references_removed_code_of_conduct(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = removal_sim_tree()
            files[".github/ISSUE_TEMPLATE/config.yml"] = (
                "blank_issues_enabled: false\n"
                "contact_links:\n"
                '  - name: "Code of conduct"\n'
                '    url: "https://github.com/CHANGEME_GITHUB_OWNER/chefs-pick-oss-starter-workspace_NAME/blob/main/CODE_OF_CONDUCT.md"\n'
                '    about: "Read this before taking part."\n'
            )
            root = write_tree(tmp, files)
            status, problems = run_one("C22", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_fail_broken_link_unrelated_to_the_removed_module(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = removal_sim_tree()
            files["README.md"] += "- [Support](SUPPORT.md)\n"
            root = write_tree(tmp, files)
            status, problems = run_one("C22", make_ctx(root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(problems)

    def test_skip_without_root_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = removal_sim_tree()
            del files["README.md"]
            root = write_tree(tmp, files)
            status, _reason = run_one("C22", make_ctx(root))
            self.assertEqual(status, "SKIP")


if __name__ == "__main__":
    unittest.main()
