"""Tests for C25 (Workspace language structure).

Contract: ``specs/003-workspace-self-compliance/contracts/tooling-delta-003.md``
§2 (path resolution and skip condition, shared with C26/C27) and §3 (the six
C25 assertions), together with ``contracts/workspace-structure.md`` §1
(language selector), §2 (anchor sequence), §3 (normative-version notice) and
§5 (language purity).

C25 deliberately resolves ``README.md`` / ``README.zh-CN.md`` relative to the
repository root (``Path(__file__).resolve().parent.parent`` inside
``check_template.py``), never to ``ctx.template_dir`` -- the workspace
homepage lives outside ``template/``, same rationale as check_c23. A naive
test that merely points ``--template-dir`` elsewhere would still read the
*real* ``README.md`` / ``README.zh-CN.md``. Following
``test_checks_contract_parity.py``'s approach, every test here instead
patches ``check_template.__file__`` (via ``FakeRepoRoot``) so C25 resolves
its paths under a throwaway temporary directory, and reads only that
directory's fixture files -- never the real ``README.md``,
``README.zh-CN.md``, ``template/`` or
``specs/001-chefs-pick-starter/contracts/guidance-layer.md``.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import make_ctx, run_one, write_tree  # noqa: E402

import check_template as ct  # noqa: E402


SOURCE_REL = "README.md"
TRANSLATION_REL = "README.zh-CN.md"

# Verbatim from workspace-structure.md §1.
SOURCE_SELECTOR = "**English** · [简体中文](README.zh-CN.md)"
TRANSLATION_SELECTOR = "[English](README.md) · **简体中文**"

# Verbatim from workspace-structure.md §3.
NOTICE = (
    "> 英文版是规范版本。本页与 "
    "[README.md](README.md) 不一致时，以英文版"
    "为准。"
)

# workspace-structure.md §2: 1 H1 anchor + 4 H2 anchors, exact order.
ANCHOR_SEQUENCE = [
    "chefs-pick-oss-starter-workspace",
    "layout",
    "common-commands",
    "publishing",
    "license",
]

ENGLISH_TITLE = "# Chef's Pick OSS Starter — development workspace"
CHINESE_TITLE = "# Chef's Pick OSS Starter — 开发工作区"

ENGLISH_SECTIONS = {
    "layout": ("## Layout", "The layout of this workspace is described here."),
    "common-commands": ("## Common commands", "The common commands are listed here."),
    "publishing": ("## Publishing", "The publishing process is described here."),
    "license": ("## License", "MIT, same as the template repository."),
}
CHINESE_SECTIONS = {
    "layout": ("## 目录结构", "这里是目录结构说明。"),
    "common-commands": ("## 常用命令", "这里是常用命令说明。"),
    "publishing": ("## 发布", "这里是发布说明。"),
    "license": ("## 许可证", "MIT 许可证，与模板仓库一致。"),
}


def _section(anchor_id: str, heading: str, body: str) -> str:
    return f"<!-- anchor: {anchor_id} -->\n{heading}\n\n{body}\n\n"


def valid_source_text() -> str:
    """A minimal, fully valid ``README.md`` (English edition)."""
    out = [
        f"<!-- anchor: {ANCHOR_SEQUENCE[0]} -->\n",
        f"{ENGLISH_TITLE}\n",
        "\n",
        f"{SOURCE_SELECTOR}\n",
        "\n",
        "This is the development workspace for the template repository.\n",
        "\n",
    ]
    for anchor_id in ANCHOR_SEQUENCE[1:]:
        heading, body = ENGLISH_SECTIONS[anchor_id]
        out.append(_section(anchor_id, heading, body))
    return "".join(out)


def valid_translation_text() -> str:
    """A minimal, fully valid ``README.zh-CN.md`` (Chinese edition)."""
    out = [
        f"<!-- anchor: {ANCHOR_SEQUENCE[0]} -->\n",
        f"{CHINESE_TITLE}\n",
        "\n",
        f"{TRANSLATION_SELECTOR}\n",
        "\n",
        f"{NOTICE}\n",
        "\n",
        "这是模板仓库的开发与维护工作区。\n",
        "\n",
    ]
    for anchor_id in ANCHOR_SEQUENCE[1:]:
        heading, body = CHINESE_SECTIONS[anchor_id]
        out.append(_section(anchor_id, heading, body))
    return "".join(out)


class FakeRepoRoot:
    """A temporary directory patched in as C25's repository root.

    Copied from ``test_checks_contract_parity.py``'s helper of the same
    name. Entering the context manager patches ``check_template.__file__``
    to ``<tmp>/tools/check_template.py`` (a path that need not exist on
    disk) so that ``check_c25``'s own ``repo_root = Path(__file__)
    .resolve().parent.parent`` resolves to ``<tmp>`` -- never to the real
    repository, and never to ``ctx.template_dir`` (which C25 ignores by
    design, per tooling-delta-003.md §2).
    """

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._patcher = mock.patch.object(
            ct, "__file__", str(self.root / "tools" / "check_template.py")
        )

    def __enter__(self) -> "FakeRepoRoot":
        self._patcher.start()
        return self

    def __exit__(self, *exc) -> None:
        self._patcher.stop()
        self._tmp.cleanup()

    def write(self, files: dict[str, str]) -> None:
        write_tree(self.root, files)


def base_files(source: str, translation: str | None) -> dict[str, str]:
    """``template/`` (so ``template_dir.is_dir()`` holds) plus the pair."""
    files = {
        "template/.keep": "",
        SOURCE_REL: source,
    }
    if translation is not None:
        files[TRANSLATION_REL] = translation
    return files


class TestC25WorkspaceLanguageStructure(unittest.TestCase):
    """C25: the workspace homepage's own language structure."""

    def test_valid_pair_passes(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write(base_files(valid_source_text(), valid_translation_text()))
            status, problems = run_one("C25", make_ctx(fake.root))
        self.assertEqual(status, "PASS", problems)

    def test_selector_misspelled_in_translation_fails(self) -> None:
        # README.md's selector must stay verbatim and present, or the check
        # never gets past the SKIP predicate (see
        # test_missing_selector_in_source_skips below). Only the
        # translation's selector is broken here -- missing the required
        # spaces around the middle dot, so it no longer matches
        # WORKSPACE_SELECTOR_LINES["README.zh-CN.md"] verbatim.
        broken_translation = valid_translation_text().replace(
            TRANSLATION_SELECTOR,
            "[English](README.md)·**简体中文**",
        )
        with FakeRepoRoot() as fake:
            fake.write(base_files(valid_source_text(), broken_translation))
            status, problems = run_one("C25", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(TRANSLATION_REL, joined)
        self.assertIn("language selector", joined)

    def test_anchor_renamed_in_translation_fails_naming_both_ids(self) -> None:
        # Rename the "layout" anchor to "structure" in the translation only;
        # the English edition keeps the canonical sequence.
        broken_translation = valid_translation_text().replace(
            "<!-- anchor: layout -->", "<!-- anchor: structure -->"
        )
        with FakeRepoRoot() as fake:
            fake.write(base_files(valid_source_text(), broken_translation))
            status, problems = run_one("C25", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(TRANSLATION_REL, joined)
        # The report must name both the missing (renamed-away) anchor id and
        # the unexpected (renamed-to) anchor id, not just say the sequence
        # is wrong.
        self.assertIn("missing", joined)
        self.assertIn("layout", joined)
        self.assertIn("unexpected", joined)
        self.assertIn("structure", joined)

    def test_chinese_prose_in_english_edition_fails(self) -> None:
        polluted_source = valid_source_text().replace(
            "This is the development workspace for the template repository.\n",
            "This is the development workspace for the template repository.\n"
            "这里混入了中文。\n",
        )
        with FakeRepoRoot() as fake:
            fake.write(base_files(polluted_source, valid_translation_text()))
            status, problems = run_one("C25", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(SOURCE_REL, joined)
        self.assertIn("CJK", joined)

    def test_overlong_english_run_in_translation_fails(self) -> None:
        # Seven consecutive English words in Chinese prose, well past the
        # "fewer than 6" limit (workspace-structure.md §5).
        long_run = "alpha bravo charlie delta echo foxtrot golf"
        polluted_translation = valid_translation_text().replace(
            "这里是目录结构说明。",
            f"这里是目录结构说明。 {long_run}",
        )
        with FakeRepoRoot() as fake:
            fake.write(base_files(valid_source_text(), polluted_translation))
            status, problems = run_one("C25", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(TRANSLATION_REL, joined)
        self.assertIn("longest run", joined)
        self.assertIn("7", joined)

    def test_notice_missing_from_translation_fails(self) -> None:
        stripped_translation = valid_translation_text().replace(f"{NOTICE}\n\n", "")
        with FakeRepoRoot() as fake:
            fake.write(base_files(valid_source_text(), stripped_translation))
            status, problems = run_one("C25", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(TRANSLATION_REL, joined)
        self.assertIn("normative notice", joined)

    def test_notice_present_in_english_edition_fails(self) -> None:
        polluted_source = valid_source_text().replace(
            "This is the development workspace for the template repository.\n",
            f"This is the development workspace for the template repository.\n"
            f"{NOTICE}\n",
        )
        with FakeRepoRoot() as fake:
            fake.write(base_files(polluted_source, valid_translation_text()))
            status, problems = run_one("C25", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(SOURCE_REL, joined)
        self.assertIn("normative notice", joined)

    def test_missing_selector_in_source_skips(self) -> None:
        # No language-selector line anywhere in README.md at all: this is
        # the tooling-delta-003.md §2 skip predicate (whether the
        # conversion has begun), not a FAIL -- independent of whether a
        # translation exists.
        no_selector_source = valid_source_text().replace(f"{SOURCE_SELECTOR}\n", "")
        self.assertNotIn(SOURCE_SELECTOR, no_selector_source)
        with FakeRepoRoot() as fake:
            fake.write(base_files(no_selector_source, None))
            status, reason = run_one("C25", make_ctx(fake.root))
        self.assertEqual(status, "SKIP", reason)
        self.assertIn(SOURCE_REL, " ".join(reason))


if __name__ == "__main__": # pragma: no cover
    unittest.main()
