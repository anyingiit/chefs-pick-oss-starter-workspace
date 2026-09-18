"""Tests for C10 (template identity isolation) and C11 (language structure).

Contract: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.3,
``template-layout.md`` §3 §4, ``guidance-layer.md`` §0 §1 §2 §3 §7 §8,
``project-files.md`` M09, M15, M16.

C11 was rewritten wholesale by
``specs/002-english-first-docs/contracts/tooling-delta.md`` §4 (title
changed from "Guidance layer" to "Language structure"); its fixtures and
test cases below follow that contract's §4 C11 entry and §8.2.
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


# --------------------------------------------------------------------------
# Project-file fixtures (C10): English only, no template identity.
# --------------------------------------------------------------------------

CLEAN_README = (
    "# CHANGEME_PROJECT_NAME\n"
    "\n"
    "A short description of the project.\n"
)

CLEAN_CHANGELOG = (
    "# Changelog\n"
    "\n"
    "All notable changes to this project will be documented in this file.\n"
    "\n"
    "## [Unreleased]\n"
    "\n"
    "### Added\n"
    "\n"
    "- Initial project structure.\n"
)

CLEAN_CODEOWNERS = (
    "# Source: GitHub code owners (official)\n"
    "# Optional. Uncomment the line below to automatically request a review.\n"
    "# * @CHANGEME_OWNER\n"
)

CLEAN_FUNDING = (
    "# Source: GitHub sponsor button (official)\n"
    'github: # Up to 4 GitHub Sponsors usernames, for example [octocat]\n'
    'custom: # Up to 4 custom URLs, for example ["https://example.com/donate"]\n'
)


def clean_project_tree() -> dict[str, str]:
    """The minimal set of project files C10 looks at, all of them valid."""
    return {
        "README.md": CLEAN_README,
        "CHANGELOG.md": CLEAN_CHANGELOG,
        ".github/CODEOWNERS": CLEAN_CODEOWNERS,
        ".github/FUNDING.yml": CLEAN_FUNDING,
    }


# --------------------------------------------------------------------------
# Guidance-layer fixtures (C11): English originals + Chinese translations,
# each satisfying every one of the ten language-structure assertions
# (tooling-delta.md §4 C11). Built from ``ANCHOR_SEQUENCES`` rather than
# hard-coded headings, so a contract change to the sequence breaks loudly
# here instead of silently drifting.
# --------------------------------------------------------------------------

README_SEQ = ct.ANCHOR_SEQUENCES["README"]
SETUP_SEQ = ct.ANCHOR_SEQUENCES["SETUP"]

# id -> (heading level, English text, Chinese text) for every non-H1 anchor
# in the README sequence.
README_HEADINGS = {
    "what-you-get": (2, "What you get", "你会得到什么"),
    "required": (3, "Required", "必需"),
    "recommended": (3, "Recommended", "推荐"),
    "optional": (3, "Optional", "可选"),
    "the-picks-at-a-glance": (2, "The picks at a glance", "选型概览"),
    "how-we-pick": (2, "How we pick", "如何选型"),
    "quick-start": (2, "Quick start", "快速开始"),
    "good-to-know": (2, "Good to know", "须知事项"),
    "clean-up-when-done": (2, "Clean up when done", "完成后清理"),
    "feedback-and-contact": (2, "Feedback and contact", "反馈与联系"),
    "license": (2, "License", "许可证"),
}
SETUP_HEADINGS = {
    "placeholders": (2, "Placeholders", "占位符"),
    "steps": (2, "Steps", "步骤"),
}


def _anchor_block(anchor_id: str, level: int, heading: str, body: str) -> str:
    return f"<!-- anchor: {anchor_id} -->\n{'#' * level} {heading}\n\n{body}\n\n"


def guidance_home() -> str:
    """``.github/README.md``: English original, satisfying every C11 rule."""
    out = [
        f"<!-- anchor: {README_SEQ[0]} -->\n{ct.GUIDANCE_HOME_TITLE}\n\n",
        "**English** · [简体中文](README.zh-CN.md)\n\n",
        "This template gives your project a full set of starter files.\n\n",
    ]
    for anchor_id in README_SEQ[1:]:
        level, english, _chinese = README_HEADINGS[anchor_id]
        if anchor_id == "quick-start":
            body = (
                "1. Follow the [Setup checklist](chefs-pick/SETUP.md).\n"
                "2. Review the [Module guide](chefs-pick/GUIDE.md)."
            )
        elif anchor_id == "clean-up-when-done":
            body = (
                "```bash\n"
                f"{ct.CLEANUP_COMMAND}\n"
                'git commit -m "chore: remove template guide"\n'
                "```"
            )
        elif anchor_id == "feedback-and-contact":
            body = "Please open an issue in this repository."
        else:
            body = "Some plain English explanatory text."
        out.append(_anchor_block(anchor_id, level, english, body))
    return "".join(out)


def guidance_home_zh() -> str:
    """``.github/README.zh-CN.md``: the Chinese translation of the home page."""
    source_name = "README.md"
    notice = f"> 英文版是规范版本。本页与 [{source_name}]({source_name}) 不一致时，以英文版为准。"
    out = [
        f"<!-- anchor: {README_SEQ[0]} -->\n# 主厨精选开源起步模板\n\n",
        "[English](README.md) · **简体中文**\n\n",
        f"{notice}\n\n",
        "本模板为项目提供完整的起步文件。\n\n",
    ]
    for anchor_id in README_SEQ[1:]:
        level, _english, chinese = README_HEADINGS[anchor_id]
        out.append(_anchor_block(anchor_id, level, chinese, "相关说明文字。"))
    return "".join(out)


def guidance_setup() -> str:
    """``chefs-pick/SETUP.md``: English original."""
    out = [
        f"<!-- anchor: {SETUP_SEQ[0]} -->\n# Setup checklist\n\n",
        "**English** · [简体中文](SETUP.zh-CN.md)\n\n",
        "Work through this list in order.\n\n",
    ]
    for anchor_id in SETUP_SEQ[1:]:
        level, english, _chinese = SETUP_HEADINGS[anchor_id]
        out.append(_anchor_block(anchor_id, level, english, "Some plain English explanatory text."))
    return "".join(out)


def guidance_setup_zh() -> str:
    """``chefs-pick/SETUP.zh-CN.md``: the Chinese translation."""
    source_name = "SETUP.md"
    notice = f"> 英文版是规范版本。本页与 [{source_name}]({source_name}) 不一致时，以英文版为准。"
    out = [
        f"<!-- anchor: {SETUP_SEQ[0]} -->\n# 起步清单\n\n",
        "[English](SETUP.md) · **简体中文**\n\n",
        f"{notice}\n\n",
    ]
    for anchor_id in SETUP_SEQ[1:]:
        level, _english, chinese = SETUP_HEADINGS[anchor_id]
        out.append(_anchor_block(anchor_id, level, chinese, "相关说明文字。"))
    return "".join(out)


def guidance_guide() -> str:
    """``chefs-pick/GUIDE.md``: not a translation, so no selector or anchors.

    Includes the "Translating your own README" fenced-code demonstration
    (tooling-delta.md §8.2): the language-selector lines it shows verbatim
    are example text inside a fenced code block, not this document's own
    language entry, so C11 must not flag them.
    """
    return (
        "# Module guide\n\n"
        "This page walks through each module in plain English prose.\n\n"
        "## Translating your own README\n\n"
        "You can copy these two lines directly into your own files.\n\n"
        "In `README.md`:\n\n"
        "```markdown\n"
        "**English** · [简体中文](README.zh-CN.md)\n"
        "```\n\n"
        "In `README.zh-CN.md`:\n\n"
        "```markdown\n"
        "[English](README.md) · **简体中文**\n"
        "```\n"
    )


def guidance_guide_tilde() -> str:
    """Same as ``guidance_guide()``, but fenced with ``~~~`` instead of

    ```` ``` ````. tooling-delta.md §8.2's fenced-code exemption applies to
    either fence character (research.md R6), so this must pass exactly
    like ``guidance_guide()`` does.
    """
    return (
        "# Module guide\n\n"
        "This page walks through each module in plain English prose.\n\n"
        "## Translating your own README\n\n"
        "You can copy these two lines directly into your own files.\n\n"
        "In `README.md`:\n\n"
        "~~~markdown\n"
        "**English** · [简体中文](README.zh-CN.md)\n"
        "~~~\n\n"
        "In `README.zh-CN.md`:\n\n"
        "~~~markdown\n"
        "[English](README.md) · **简体中文**\n"
        "~~~\n"
    )


GUIDANCE_CHANGELOG = (
    "# Template changelog\n"
    "\n"
    "This file records changes to the template itself.\n"
    "\n"
    "## [Unreleased]\n"
    "\n"
    "### Added\n"
    "\n"
    "- First version.\n"
)

GUIDANCE_LICENSE = (
    "MIT License\n"
    "\n"
    "Copyright (c) 2026 Chef's Pick OSS Starter contributors\n"
    "\n"
    "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
    'of this software. THE SOFTWARE IS PROVIDED "AS IS".\n'
)


def full_guidance_tree() -> dict[str, str]:
    return {
        ".github/README.md": guidance_home(),
        ".github/README.zh-CN.md": guidance_home_zh(),
        ".github/chefs-pick/SETUP.md": guidance_setup(),
        ".github/chefs-pick/SETUP.zh-CN.md": guidance_setup_zh(),
        ".github/chefs-pick/GUIDE.md": guidance_guide(),
        ".github/chefs-pick/CHANGELOG.md": GUIDANCE_CHANGELOG,
        ".github/chefs-pick/LICENSE": GUIDANCE_LICENSE,
    }


class CheckTestCase(unittest.TestCase):
    """Base class: build a tree in a throwaway directory and run one check."""

    def check(self, check_id: str, tree: dict[str, str], **ctx_kw):
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, tree)
            return run_one(check_id, make_ctx(tmp, **ctx_kw))

    def assertPass(self, check_id: str, tree: dict[str, str], **ctx_kw):
        status, problems = self.check(check_id, tree, **ctx_kw)
        self.assertEqual(status, "PASS", f"{check_id}: {problems}")

    def assertFail(self, check_id: str, tree: dict[str, str], **ctx_kw):
        status, problems = self.check(check_id, tree, **ctx_kw)
        self.assertEqual(status, "FAIL", f"{check_id}: {problems}")
        self.assertTrue(problems, f"{check_id} failed without reporting a problem")
        return problems


# --------------------------------------------------------------------------
# C10 Template identity isolation
# --------------------------------------------------------------------------


class TestC10TemplateIdentityIsolation(CheckTestCase):
    def test_pass_clean_project_files(self):
        self.assertPass("C10", clean_project_tree())

    def test_pass_identity_and_chinese_allowed_in_guidance_layer(self):
        files = clean_project_tree()
        files.update(full_guidance_tree())
        self.assertPass("C10", files)

    def test_fail_identity_in_project_file(self):
        files = clean_project_tree()
        files["README.md"] = (
            "# CHANGEME_PROJECT_NAME\n"
            "\n"
            "Generated from the Chef's Pick OSS Starter template.\n"
        )
        self.assertFail("C10", files)

    def test_fail_chinese_in_project_file(self):
        files = clean_project_tree()
        files["CONTRIBUTING.md"] = (
            "# Contributing\n"
            "\n"
            "欢迎参与本项目的贡献。\n"
        )
        self.assertFail("C10", files)

    def test_fail_changelog_has_two_level_two_headings(self):
        files = clean_project_tree()
        files["CHANGELOG.md"] = (
            "# Changelog\n"
            "\n"
            "## [Unreleased]\n"
            "\n"
            "## [1.0.0] - 2026-01-01\n"
            "\n"
            "### Added\n"
            "\n"
            "- Initial project structure.\n"
        )
        self.assertFail("C10", files)

    def test_fail_codeowners_has_effective_line(self):
        files = clean_project_tree()
        files[".github/CODEOWNERS"] = (
            "# Source: GitHub code owners (official)\n"
            "* @CHANGEME_OWNER\n"
        )
        self.assertFail("C10", files)

    def test_fail_funding_has_a_non_null_value(self):
        files = clean_project_tree()
        files[".github/FUNDING.yml"] = (
            "# Source: GitHub sponsor button (official)\n"
            "github: [octocat]\n"
            "custom:\n"
        )
        self.assertFail("C10", files)

    def test_files_option_limits_the_scope(self):
        files = clean_project_tree()
        files["CONTRIBUTING.md"] = (
            "# Contributing\n"
            "\n"
            "Generated from the Chef's Pick OSS Starter template.\n"
        )
        # Out of scope: the offending file is not listed in --files.
        self.assertPass("C10", files, files={"README.md"})
        # In scope: the same tree fails once the file is selected.
        self.assertFail("C10", files, files={"CONTRIBUTING.md"})


# --------------------------------------------------------------------------
# C11 Language structure (tooling-delta.md §4 C11)
# --------------------------------------------------------------------------


class TestC11LanguageStructure(CheckTestCase):
    def test_pass_full_guidance_layer(self):
        self.assertPass("C11", full_guidance_tree())

    def test_pass_partial_guidance_layer(self):
        # C11 only looks at guidance files that already exist. README.md's
        # selector line points at README.zh-CN.md, so that sibling must be
        # present too for mutual reachability (assertion 3) to hold.
        self.assertPass(
            "C11",
            {
                ".github/README.md": guidance_home(),
                ".github/README.zh-CN.md": guidance_home_zh(),
            },
        )

    def test_pass_guidance_layer_with_project_files_present(self):
        files = clean_project_tree()
        files.update(full_guidance_tree())
        self.assertPass("C11", files)

    def test_pass_selector_demo_inside_fenced_code_block_is_ignored(self):
        # tooling-delta.md §8.2: GUIDE.md's "Translating your own README"
        # section shows the language-selector lines verbatim inside a
        # fenced code block. That is example text for the reader to copy,
        # not this document's own language entry, so it must not FAIL.
        self.assertPass("C11", {".github/chefs-pick/GUIDE.md": guidance_guide()})

    def test_pass_selector_demo_inside_tilde_fenced_code_block_is_ignored(self):
        # FIXED (Finding 5): ``_strip_fenced_code`` used to recognise only
        # backtick fences. The same "Translating your own README" demo,
        # fenced with ``~~~`` instead, must be ignored exactly like the
        # backtick-fenced version is.
        self.assertPass(
            "C11", {".github/chefs-pick/GUIDE.md": guidance_guide_tilde()}
        )

    # -- 1. Purity ---------------------------------------------------------

    def test_fail_purity_english_body_contains_chinese(self):
        files = full_guidance_tree()
        files[".github/README.md"] = guidance_home().replace(
            "This template gives your project a full set of starter files.",
            "This template gives your project 一些中文文字 a full set of starter files.",
        )
        problems = self.assertFail("C11", files)
        self.assertTrue(
            any(".github/README.md" in p and "purity" in p for p in problems),
            f"expected a purity problem naming .github/README.md: {problems}",
        )

    def test_fail_purity_chinese_translation_has_six_english_words(self):
        files = full_guidance_tree()
        files[".github/README.zh-CN.md"] = guidance_home_zh().replace(
            "相关说明文字。",
            "相关说明文字 This is a long run of english words here now.",
            1,
        )
        problems = self.assertFail("C11", files)
        self.assertTrue(
            any(".github/README.zh-CN.md" in p and "purity" in p for p in problems),
            f"expected a purity problem naming .github/README.zh-CN.md: {problems}",
        )

    # -- 2. Language selector ------------------------------------------------

    def test_fail_language_entry_missing(self):
        files = full_guidance_tree()
        files[".github/README.md"] = guidance_home().replace(
            "**English** · [简体中文](README.zh-CN.md)\n\n", "", 1
        )
        problems = self.assertFail("C11", files)
        self.assertTrue(
            any(".github/README.md" in p and "language selector" in p for p in problems),
            f"expected a language-selector problem naming .github/README.md: {problems}",
        )

    def test_fail_language_entry_misplaced(self):
        files = full_guidance_tree()
        # An extra blank line between the H1 and the selector line breaks
        # the "exactly one blank line after the H1" rule.
        files[".github/README.md"] = guidance_home().replace(
            f"{ct.GUIDANCE_HOME_TITLE}\n\n**English**",
            f"{ct.GUIDANCE_HOME_TITLE}\n\n\n**English**",
            1,
        )
        problems = self.assertFail("C11", files)
        self.assertTrue(
            any(".github/README.md" in p and "language selector" in p for p in problems),
            f"expected a language-selector problem naming .github/README.md: {problems}",
        )

    def test_fail_language_entry_leaks_into_non_translated_doc(self):
        files = full_guidance_tree()
        # A real (non-fenced) link to the Chinese translation inside
        # GUIDE.md, which is not one of the translated documents.
        files[".github/chefs-pick/GUIDE.md"] = guidance_guide() + (
            "\nSee the [Chinese translation](README.zh-CN.md) for more.\n"
        )
        problems = self.assertFail("C11", files)
        self.assertTrue(
            any(".github/chefs-pick/GUIDE.md" in p and "language selector" in p for p in problems),
            f"expected a language-selector problem naming GUIDE.md: {problems}",
        )

    # -- 4. Anchors ----------------------------------------------------------

    def test_fail_anchor_sequence_does_not_match(self):
        files = full_guidance_tree()
        files[".github/README.md"] = guidance_home().replace(
            "<!-- anchor: required -->", "<!-- anchor: requirements-typo -->", 1
        )
        problems = self.assertFail("C11", files)
        # SC-013: the report must name both the offending translation file
        # and the specific anchor id, not just say "anchors are wrong".
        self.assertTrue(
            any(
                ".github/README.md" in p and "requirements-typo" in p
                for p in problems
            ),
            f"expected a problem naming both the file and the bad anchor id: {problems}",
        )

    def test_fail_anchor_count_does_not_match_heading_count(self):
        files = full_guidance_tree()
        # Drop one anchor line, leaving its heading without an anchor
        # directly above it.
        files[".github/README.md"] = guidance_home().replace(
            "<!-- anchor: license -->\n", "", 1
        )
        problems = self.assertFail("C11", files)
        self.assertTrue(
            any(".github/README.md" in p and "anchor" in p for p in problems),
            f"expected an anchors problem naming .github/README.md: {problems}",
        )

    # -- 5. Normative-version notice ------------------------------------------

    def test_fail_translation_missing_normative_notice(self):
        files = full_guidance_tree()
        notice = (
            "> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，"
            "以英文版为准。"
        )
        files[".github/README.zh-CN.md"] = guidance_home_zh().replace(
            f"{notice}\n\n", "", 1
        )
        problems = self.assertFail("C11", files)
        self.assertTrue(
            any(".github/README.zh-CN.md" in p and "normative" in p for p in problems),
            f"expected a normative-notice problem naming .github/README.zh-CN.md: {problems}",
        )

    # -- 7. Single-source markers ---------------------------------------------

    def test_fail_translation_contains_single_source_marker(self):
        files = full_guidance_tree()
        files[".github/README.zh-CN.md"] = guidance_home_zh() + (
            "\n| Placeholder | Meaning | Files | Example |\n"
        )
        problems = self.assertFail("C11", files)
        self.assertTrue(
            any(
                ".github/README.zh-CN.md" in p and "single source" in p
                for p in problems
            ),
            f"expected a single-source problem naming .github/README.zh-CN.md: {problems}",
        )

    # -- 6, 8, 9, 10: preserved assertions -------------------------------------

    def test_fail_home_title_not_verbatim(self):
        files = full_guidance_tree()
        files[".github/README.md"] = guidance_home().replace(
            ct.GUIDANCE_HOME_TITLE, "# Chef's Pick OSS Starter Template", 1
        )
        self.assertFail("C11", files)

    def test_fail_home_missing_cleanup_command(self):
        files = full_guidance_tree()
        files[".github/README.md"] = guidance_home().replace(
            ct.CLEANUP_COMMAND, "rm -r .github/README.md"
        )
        self.assertFail("C11", files)

    def test_fail_template_changelog_without_version_heading(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/CHANGELOG.md"] = (
            "# Template changelog\n"
            "\n"
            "This file records changes to the template itself.\n"
        )
        self.assertFail("C11", files)

    def test_fail_template_license_copyright_line(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/LICENSE"] = GUIDANCE_LICENSE.replace(
            "Copyright (c) 2026 Chef's Pick OSS Starter contributors",
            "Copyright (c) 2026 CHANGEME_COPYRIGHT_HOLDER",
        )
        self.assertFail("C11", files)

    # -- scope and skip --------------------------------------------------------

    def test_files_option_limits_the_scope(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/CHANGELOG.md"] = (
            "# Template changelog\n\nNo version heading here.\n"
        )
        # Out of scope: the broken CHANGELOG.md is not selected.
        self.assertPass("C11", files, files={".github/README.md"})
        # In scope: the same tree fails once CHANGELOG.md is selected.
        self.assertFail("C11", files, files={".github/chefs-pick/CHANGELOG.md"})

    def test_skip_when_no_guidance_files_exist(self):
        status, reason = self.check("C11", clean_project_tree())
        self.assertEqual(status, "SKIP", reason)
        # tooling.md §1.1: a SKIP must say which file is missing.
        self.assertTrue(
            any(
                token in text
                for text in reason
                for token in ("README", "chefs-pick", "guidance", "引导")
            ),
            f"expected the skip reason to name the missing file: {reason}",
        )


if __name__ == "__main__":
    unittest.main()
