"""Tests for C10 (template identity isolation) and C11 (guidance layer).

Contract: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.3,
``template-layout.md`` §3 §4, ``guidance-layer.md`` §0 §1 §2 §3 §7 §8,
``project-files.md`` M09, M15, M16.
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
# Guidance-layer fixtures (C11): bilingual headings, template identity allowed.
# --------------------------------------------------------------------------

GUIDE_EXTRA_BILINGUAL = [
    ("按语言补充", "Adding language-specific rules"),
    ("固定动作版本", "Pinning actions"),
    ("账号级默认文件", "Account-level default files"),
    ("中文译本", "Chinese translations"),
    ("模板版本追溯", "Tracing the template version"),
    ("更换许可证", "Changing the license"),
]


def guidance_home(title: str | None = None) -> str:
    """``.github/README.md`` satisfying every C11 requirement for the home page."""
    if title is None:
        title = ct.GUIDANCE_HOME_TITLE
    return (
        f"{title}\n"
        "\n"
        "每个模块都选用社区公认的佼佼者。\n"
        "\n"
        "Every module uses a widely adopted community pick.\n"
        "\n"
        "## 快速开始 / Quick start\n"
        "\n"
        "1. 按 [起步清单 / Setup checklist](chefs-pick/SETUP.md) 完成定制。\n"
        "2. 查阅 [模块讲解 / Module guide](chefs-pick/GUIDE.md)。\n"
        "\n"
        "## 完成后清理 / Clean up when done\n"
        "\n"
        "```bash\n"
        f"{ct.CLEANUP_COMMAND}\n"
        'git commit -m "chore: remove template guide"\n'
        "```\n"
        "\n"
        "## 反馈与联系 / Feedback and contact\n"
        "\n"
        "请在本仓库提 Issue。 / Please open an issue in this repository.\n"
    )


def guidance_setup() -> str:
    """``SETUP.md`` with S01-S09 and the verbatim placeholder table header."""
    steps = "\n".join(
        f"| S0{n} | 必做 / Required | 第 {n} 步 / Step {n} | 确认 / Verify {n} |"
        for n in range(1, 10)
    )
    return (
        "# 起步清单 / Setup checklist\n"
        "\n"
        "按顺序完成，大约 15 分钟。 / Work through it in order, about 15 minutes.\n"
        "\n"
        "## 占位符 / Placeholders\n"
        "\n"
        f"{ct.PLACEHOLDER_TABLE_HEADER}\n"
        "|---|---|---|---|\n"
        "| `CHANGEME_OWNER` | 账号 / Owner | `README.md` | `octocat` |\n"
        "\n"
        "## 步骤 / Steps\n"
        "\n"
        "| 编号 / ID | 类型 / Kind | 步骤 / Step | 如何确认 / How to verify |\n"
        "|---|---|---|---|\n"
        f"{steps}\n"
    )


def guidance_guide(skip: tuple[str, ...] = ()) -> str:
    """``GUIDE.md`` with ``## M01``-``## M16`` plus the 6 extra headings."""
    parts = [
        "# 模块讲解 / Module guide\n",
        "\n",
        "本页逐个讲解模块。 / This page walks through each module.\n",
    ]
    for n in range(1, 17):
        module = f"M{n:02d}"
        if module in skip:
            continue
        parts.append(
            f"\n## {module} 模块 / Module {module}\n"
            "\n"
            "### 为什么需要 / Why\n"
            "\n"
            "说明。 / Notes.\n"
            "\n"
            "### 如何定制 / Customize\n"
            "\n"
            "说明。 / Notes.\n"
            "\n"
            "### 如何删除 / Remove\n"
            "\n"
            "说明。 / Notes.\n"
        )
    for chinese, english in GUIDE_EXTRA_BILINGUAL:
        parts.append(f"\n## {chinese} / {english}\n\n说明。 / Notes.\n")
    return "".join(parts)


GUIDANCE_CHANGELOG = (
    "# 模板变更记录 / Template changelog\n"
    "\n"
    "本文件记录模板自身的变更。\n"
    "\n"
    "This file records changes to the template itself.\n"
    "\n"
    "## [Unreleased] / 未发布\n"
    "\n"
    "### Added / 新增\n"
    "\n"
    "- 首个版本。 / First version.\n"
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
        ".github/chefs-pick/SETUP.md": guidance_setup(),
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
# C11 Guidance layer
# --------------------------------------------------------------------------


class TestC11GuidanceLayer(CheckTestCase):
    def test_pass_full_guidance_layer(self):
        self.assertPass("C11", full_guidance_tree())

    def test_pass_partial_guidance_layer(self):
        # C11 only looks at guidance files that already exist.
        self.assertPass("C11", {".github/README.md": guidance_home()})

    def test_pass_guidance_layer_with_project_files_present(self):
        files = clean_project_tree()
        files.update(full_guidance_tree())
        self.assertPass("C11", files)

    def test_fail_home_title_not_verbatim(self):
        files = full_guidance_tree()
        files[".github/README.md"] = guidance_home(title="# Chef's Pick OSS Starter")
        self.assertFail("C11", files)

    def test_fail_home_missing_cleanup_command(self):
        files = full_guidance_tree()
        files[".github/README.md"] = guidance_home().replace(
            ct.CLEANUP_COMMAND, "rm -r .github/README.md"
        )
        self.assertFail("C11", files)

    def test_fail_home_missing_feedback_heading(self):
        files = full_guidance_tree()
        files[".github/README.md"] = guidance_home().replace(
            "## 反馈与联系 / Feedback and contact", "## 反馈 / Feedback"
        )
        self.assertFail("C11", files)

    def test_fail_english_only_heading_in_guidance_markdown(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/MAINTAINING.md"] = (
            "# 维护说明 / Maintaining\n"
            "\n"
            "## Review cadence\n"
            "\n"
            "至少每 6 个月复核一次。 / Review at least every 6 months.\n"
        )
        problems = self.assertFail("C11", files)
        self.assertTrue(
            any("MAINTAINING" in p for p in problems),
            f"expected the offending file to be named: {problems}",
        )

    def test_pass_version_heading_is_exempt_from_the_bilingual_rule(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/CHANGELOG.md"] = (
            "# 模板变更记录 / Template changelog\n"
            "\n"
            "本文件记录模板自身的变更。 / Changes to the template itself.\n"
            "\n"
            "## [Unreleased]\n"
            "\n"
            "## [1.0.0] - 2026-10-01\n"
            "\n"
            "### 新增 / Added\n"
            "\n"
            "- 首个版本。 / First version.\n"
        )
        self.assertPass("C11", files)

    def test_fail_guide_missing_m07(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/GUIDE.md"] = guidance_guide(skip=("M07",))
        self.assertFail("C11", files)

    def test_fail_guide_missing_extra_heading(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/GUIDE.md"] = guidance_guide().replace(
            "## 固定动作版本 / Pinning actions", "## 动作 / Actions"
        )
        self.assertFail("C11", files)

    def test_fail_setup_missing_a_step(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/SETUP.md"] = guidance_setup().replace(
            "| S07 | 必做 / Required | 第 7 步 / Step 7 | 确认 / Verify 7 |\n", ""
        )
        self.assertFail("C11", files)

    def test_fail_setup_missing_placeholder_table_header(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/SETUP.md"] = guidance_setup().replace(
            ct.PLACEHOLDER_TABLE_HEADER,
            "| 占位符 | 含义 | 出现的文件 | 示例 |",
        )
        self.assertFail("C11", files)

    def test_fail_template_license_copyright_line(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/LICENSE"] = GUIDANCE_LICENSE.replace(
            "Copyright (c) 2026 Chef's Pick OSS Starter contributors",
            "Copyright (c) 2026 CHANGEME_COPYRIGHT_HOLDER",
        )
        self.assertFail("C11", files)

    def test_fail_template_changelog_without_version_heading(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/CHANGELOG.md"] = (
            "# 模板变更记录 / Template changelog\n"
            "\n"
            "本文件记录模板自身的变更。 / Changes to the template itself.\n"
        )
        self.assertFail("C11", files)

    def test_files_option_limits_the_scope(self):
        files = full_guidance_tree()
        files[".github/chefs-pick/GUIDE.md"] = guidance_guide(skip=("M07",))
        # Out of scope: GUIDE.md is broken but not selected.
        self.assertPass("C11", files, files={".github/README.md"})
        # In scope: the same tree fails once GUIDE.md is selected.
        self.assertFail("C11", files, files={".github/chefs-pick/GUIDE.md"})

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
