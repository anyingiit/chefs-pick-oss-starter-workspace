"""Tests for C26 (Workspace facts).

Contract: ``specs/003-workspace-self-compliance/contracts/tooling-delta-003.md``
§4 C26, and ``specs/003-workspace-self-compliance/contracts/workspace-structure.md``
§6.

C26 reads the declared facts out of the workspace homepage (``README.md``)
and its Chinese translation (``README.zh-CN.md``) and compares them against
the repository's actual state:

- the ``template/`` file count, declared as
  ``` `template/` holds <N> files ``` in English and
  ``` `template/` 共 <N> 个文件 ``` in Chinese;
- the structural check count, declared as ``<N> structural checks`` in
  English and ``<N> 项结构校验`` in Chinese;
- every directory under ``specs/`` must appear as ``` `specs/<name>/` ```
  in both files.

Like C23 and C25, ``check_c26``'s own docstring says it deliberately
resolves ``repo_root`` as ``Path(__file__).resolve().parent.parent``,
independent of ``ctx.template_dir`` -- so an unpatched test would read the
*real* ``README.md``, ``README.zh-CN.md``, ``template/`` and ``specs/``.
This module reuses the ``FakeRepoRoot`` monkeypatch approach from
``test_checks_contract_parity.py``: patching ``check_template.__file__`` to
a path under a temporary directory redirects ``repo_root`` there without
touching ``tools/check_template.py`` and without needing a real
``tools/check_template.py`` to exist at that patched path.

No test here reads or writes the real ``README.md``, ``README.zh-CN.md``,
``template/`` or ``specs/001-chefs-pick-starter/contracts/guidance-layer.md``
-- every fixture lives under its own ``tempfile.TemporaryDirectory``.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import make_ctx, run_one, write_tree  # noqa: E402

import check_template as ct  # noqa: E402


README = "README.md"
README_ZH = "README.zh-CN.md"
SELECTOR_LINE = "**English** · [简体中文](README.zh-CN.md)"

# check_c26 compares the declared "structural checks" count against
# ``len(CHECKS)`` in the *real* module -- FakeRepoRoot only redirects the
# path resolution, not the CHECKS dict itself -- so fixtures must declare
# whatever the real module currently holds to be considered "correct".
ACTUAL_CHECKS = len(ct.CHECKS)


class FakeRepoRoot:
    """A temporary directory patched in as C26's repository root.

    Entering the context manager patches ``check_template.__file__`` to
    ``<tmp>/tools/check_template.py`` (a path that need not exist on disk)
    so that ``check_c26``'s own ``repo_root = Path(__file__).resolve()
    .parent.parent`` resolves to ``<tmp>``.

    check_c26 now derives the ``template/`` file count from git-tracked
    files (Finding 4), via ``git -C <repo_root> ls-files``, so *root* must
    be a real (if throwaway) git repository for that to succeed: ``write``
    runs ``git init`` once and ``git add -A`` after writing files, staging
    everything written so far as tracked. A file created directly on disk
    afterwards (not through ``write``) stays untracked, which is exactly
    what the untracked-file test below needs.
    """

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._patcher = mock.patch.object(
            ct, "__file__", str(self.root / "tools" / "check_template.py")
        )
        self._git_initialized = False

    def __enter__(self) -> "FakeRepoRoot":
        self._patcher.start()
        return self

    def __exit__(self, *exc) -> None:
        self._patcher.stop()
        self._tmp.cleanup()

    def write(self, files: dict[str, str]) -> None:
        write_tree(self.root, files)
        if not self._git_initialized:
            subprocess.run(
                ["git", "init", "-q"], cwd=self.root, check=True,
                capture_output=True,
            )
            self._git_initialized = True
        subprocess.run(
            ["git", "add", "-A"], cwd=self.root, check=True, capture_output=True,
        )


def readme_en(
    *,
    file_count: int,
    checks_count: int,
    spec_dirs: list[str],
    include_file_count: bool = True,
    include_checks_count: bool = True,
) -> str:
    lines = ["# Chef's Pick OSS Starter Workspace", "", SELECTOR_LINE, ""]
    if include_file_count:
        lines.append(f"`template/` holds {file_count} files.")
        lines.append("")
    if include_checks_count:
        lines.append(f"The tooling runs {checks_count} structural checks.")
        lines.append("")
    for name in spec_dirs:
        lines.append(f"See `specs/{name}/` for details.")
    lines.append("")
    return "\n".join(lines)


def readme_zh(
    *,
    file_count: int,
    checks_count: int,
    spec_dirs: list[str],
    include_file_count: bool = True,
    include_checks_count: bool = True,
) -> str:
    lines = ["# Chef's Pick OSS Starter Workspace", ""]
    if include_file_count:
        lines.append(f"`template/` 共 {file_count} 个文件。")
        lines.append("")
    if include_checks_count:
        lines.append(f"本工具共有 {checks_count} 项结构校验。")
        lines.append("")
    for name in spec_dirs:
        lines.append(f"参见 `specs/{name}/`。")
    lines.append("")
    return "\n".join(lines)


class TestC26WorkspaceFacts(unittest.TestCase):
    """C26: README.md / README.zh-CN.md's declared facts agree with reality."""

    def test_all_facts_correct_in_both_editions_passes(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/a.md": "a\n",
                    "template/b.md": "b\n",
                    "template/c.txt": "c\n",
                    "specs/only-feature/.keep": "",
                    README: readme_en(
                        file_count=3,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                    README_ZH: readme_zh(
                        file_count=3,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                }
            )
            status, problems = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "PASS", problems)

    def test_wrong_template_file_count_fails_with_both_numbers(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/a.md": "a\n",
                    "template/b.md": "b\n",
                    "template/c.txt": "c\n",
                    "specs/only-feature/.keep": "",
                    # Declared as 12 files but only 3 actually exist.
                    README: readme_en(
                        file_count=12,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                    README_ZH: readme_zh(
                        file_count=3,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                }
            )
            status, problems = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(README, joined)
        self.assertIn("12", joined)
        self.assertIn("3", joined)

    def test_wrong_structural_check_count_fails_with_both_numbers(self) -> None:
        wrong = ACTUAL_CHECKS + 72  # arbitrary, distinct digit sequence
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/a.md": "a\n",
                    "specs/only-feature/.keep": "",
                    README: readme_en(
                        file_count=1,
                        checks_count=wrong,
                        spec_dirs=["only-feature"],
                    ),
                    README_ZH: readme_zh(
                        file_count=1,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                }
            )
            status, problems = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(README, joined)
        self.assertIn(str(wrong), joined)
        self.assertIn(str(ACTUAL_CHECKS), joined)

    def test_missing_spec_directory_in_one_edition_fails_naming_it(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/a.md": "a\n",
                    "specs/alpha-feature/.keep": "",
                    "specs/beta-feature/.keep": "",
                    README: readme_en(
                        file_count=1,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["alpha-feature", "beta-feature"],
                    ),
                    # Chinese edition forgets beta-feature.
                    README_ZH: readme_zh(
                        file_count=1,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["alpha-feature"],
                    ),
                }
            )
            status, problems = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(README_ZH, joined)
        self.assertIn("beta-feature", joined)

    def test_missing_file_count_phrase_fails_with_expected_message(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/a.md": "a\n",
                    "specs/only-feature/.keep": "",
                    README: readme_en(
                        file_count=1,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                        include_file_count=False,
                    ),
                    README_ZH: readme_zh(
                        file_count=1,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                }
            )
            status, problems = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(f"{README}: no template file count found", joined)

    def test_english_correct_chinese_stale_still_fails(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/a.md": "a\n",
                    "template/b.md": "b\n",
                    "specs/only-feature/.keep": "",
                    README: readme_en(
                        file_count=2,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                    # Chinese edition is stale: still declares 1 file.
                    README_ZH: readme_zh(
                        file_count=1,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                }
            )
            status, problems = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(README_ZH, joined)
        self.assertIn("1", joined)
        self.assertIn("2", joined)

    def test_no_language_selector_line_fails(self) -> None:
        # FIXED (Finding 2): the language-selector line missing from
        # README.md used to be a SkipCheck predicate -- deleting or
        # misspelling that one line silently turned C25, C26 and C27 all
        # off. It is now a FAIL, naming README.md and what is missing.
        # ``template/`` still exists here, so this is not the "not the
        # workspace repository at all" case that remains a SkipCheck.
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/a.md": "a\n",
                    "specs/only-feature/.keep": "",
                    README: (
                        "# Chef's Pick OSS Starter Workspace\n\n"
                        "`template/` holds 1 files.\n\n"
                        f"The tooling runs {ACTUAL_CHECKS} structural checks.\n\n"
                        "See `specs/only-feature/` for details.\n"
                    ),
                }
            )
            status, problems = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(README, joined)
        self.assertIn("language selector", joined)

    def test_missing_readme_fails(self) -> None:
        # FIXED (Finding 2): README.md itself missing is a FAIL, not a
        # SkipCheck, once ``template/`` exists (i.e. this is genuinely the
        # workspace repository).
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/a.md": "a\n",
                    "specs/only-feature/.keep": "",
                }
            )
            status, problems = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(README, joined)
        self.assertIn("does not exist", joined)

    def test_missing_template_dir_still_skips(self) -> None:
        # The one remaining SkipCheck predicate (Finding 2): ``template/``
        # does not exist at all, i.e. this is not the workspace repository.
        # No fixture path below is under "template/", so fake.write() never
        # creates that directory.
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "specs/only-feature/.keep": "",
                    README: readme_en(
                        file_count=0,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                }
            )
            self.assertFalse((fake.root / "template").exists())
            status, reason = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "SKIP", reason)

    def test_missing_translation_fails_naming_it(self) -> None:
        # FIXED (Finding 6): the selector is in place but README.zh-CN.md
        # itself does not exist -- C26 must record a FAIL naming the
        # missing file, not silently drop it from the set it validates.
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/a.md": "a\n",
                    "specs/only-feature/.keep": "",
                    README: readme_en(
                        file_count=1,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                }
            )
            self.assertFalse((fake.root / README_ZH).exists())
            status, problems = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(README_ZH, joined)
        self.assertIn("does not exist", joined)

    def test_untracked_file_under_template_does_not_change_count(self) -> None:
        # FIXED (Finding 4): the declared count is compared against
        # git-tracked files under template/, not a filesystem walk -- a
        # stray untracked file (a scratch probe, a build artefact) must
        # not make a correct declaration look wrong.
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/a.md": "a\n",
                    "template/b.md": "b\n",
                    "specs/only-feature/.keep": "",
                    README: readme_en(
                        file_count=2,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                    README_ZH: readme_zh(
                        file_count=2,
                        checks_count=ACTUAL_CHECKS,
                        spec_dirs=["only-feature"],
                    ),
                }
            )
            # Written directly to disk, deliberately bypassing fake.write()
            # (and therefore "git add"), so it stays untracked.
            (fake.root / "template" / ".scratch-probe").write_text(
                "not tracked\n", encoding="utf-8"
            )
            status, problems = run_one("C26", make_ctx(fake.root))
        self.assertEqual(status, "PASS", problems)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
