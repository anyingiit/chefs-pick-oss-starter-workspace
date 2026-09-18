"""Tests for C24 (translation freshness) and ``--update-digests``.

Contract: ``specs/002-english-first-docs/contracts/tooling-delta.md`` §1.1
(the WARN state and its exit-code rules), §1.2 (``--update-digests``) and
§5 C24:

- for every translation, recompute the sha256 (first 16 hex digits) of the
  same-directory English source named by its ``<!-- translation-of: ...
  -->`` marker;
- a stale-but-well-formed digest is a WARN (exit code 0), or a FAIL under
  ``--release`` (exit code 1) -- this WARN/FAIL split (FR-014) is the part
  this suite pins down by asserting the process exit code, not merely the
  printed status word;
- a missing marker, a malformed marker, or a marker naming a source file
  that does not exist is always a FAIL, never a WARN;
- no translation present is a SKIP.

Every fixture uses one translation pair, ``.github/README.md`` (the
English source) and ``.github/README.zh-CN.md`` (its translation) --
the minimal pair ``find_translations`` recognises, per §1.3's
``^(?P<id>[A-Za-z-]+)\\.(?P<lang>[a-z]{2}(-[A-Z]{2})?)\\.md$`` naming rule.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import make_ctx, run_one, write_tree  # noqa: E402

import check_template as ct  # noqa: E402


SOURCE_REL = ".github/README.md"
TRANSLATION_REL = ".github/README.zh-CN.md"

SOURCE_TEXT = "# Chef's Pick OSS Starter\n\nSome English content.\n"


def source_digest(text: str = SOURCE_TEXT) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def marker(digest: str, source_name: str = "README.md") -> str:
    return f"<!-- translation-of: {source_name} sha256:{digest} -->"


def translation_text(marker_line: str | None) -> str:
    lines = []
    if marker_line is not None:
        lines.append(marker_line)
    lines += ["# 主厨精选 OSS 启动模板", "", "中文内容。", ""]
    return "\n".join(lines)


class TestC24TranslationFreshness(unittest.TestCase):
    """C24: a translation's recorded source digest matches the real one."""

    def test_matching_digest_passes(self) -> None:
        digest = source_digest()
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    SOURCE_REL: SOURCE_TEXT,
                    TRANSLATION_REL: translation_text(marker(digest)),
                },
            )
            status, problems = run_one("C24", make_ctx(tmp))
        self.assertEqual(status, "PASS", problems)

    def test_stale_digest_without_release_warns_and_exits_zero(self) -> None:
        stale_digest = "0" * 16
        self.assertNotEqual(stale_digest, source_digest())
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    SOURCE_REL: SOURCE_TEXT,
                    TRANSLATION_REL: translation_text(marker(stale_digest)),
                },
            )
            ctx = make_ctx(tmp, release=False)
            with self.assertRaises(ct.WarnCheck) as caught:
                ct.check_c24(ctx)
            self.assertTrue(caught.exception.args[0])

            # FR-014: WARN never affects the exit code (§1.1), so the whole
            # process must still exit 0 -- this is the assertion that must
            # not be replaced by "the output said WARN".
            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = ct.main(
                    ["--template-dir", tmp, "--only", "C24"]
                )
        self.assertEqual(exit_code, 0)

    def test_stale_digest_with_release_fails_and_exits_one(self) -> None:
        stale_digest = "0" * 16
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    SOURCE_REL: SOURCE_TEXT,
                    TRANSLATION_REL: translation_text(marker(stale_digest)),
                },
            )
            ctx = make_ctx(tmp, release=True)
            # Under --release the same staleness is returned as an ordinary
            # FAIL list, not raised as a WarnCheck (§1.1).
            problems = ct.check_c24(ctx)
            self.assertTrue(problems)

            # And the process-level exit code must be 1, not merely a
            # printed "FAIL" -- the point of FR-014's release gate.
            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = ct.main(
                    ["--template-dir", tmp, "--only", "C24", "--release"]
                )
        self.assertEqual(exit_code, 1)

    def test_missing_marker_line_fails_not_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    SOURCE_REL: SOURCE_TEXT,
                    TRANSLATION_REL: translation_text(None),
                },
            )
            status, problems = run_one("C24", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(any("missing or malformed" in p for p in problems))

    def test_malformed_marker_fails_not_warns(self) -> None:
        # Well short of the 16 lowercase hex digits DIGEST_RE requires, so
        # the whole line fails to match and is treated as absent.
        bad_marker = "<!-- translation-of: README.md sha256:abc -->"
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    SOURCE_REL: SOURCE_TEXT,
                    TRANSLATION_REL: translation_text(bad_marker),
                },
            )
            status, problems = run_one("C24", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(any("missing or malformed" in p for p in problems))

    def test_no_translation_present_skips(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {"README.md": "just a project file\n"})
            status, reason = run_one("C24", make_ctx(tmp))
        self.assertEqual(status, "SKIP", reason)

    # ------------------------------------------------------------------
    # FIXED: tooling-delta.md §5 C24 also requires a FAIL when "the source
    # marker names a source file that does not exist". check_c24's own
    # source code always contained that branch (the
    # `if not source_path.is_file():` check right after a marker is
    # matched), but it used to be unreachable through the public
    # Context-based API: check_c24 only ever iterates
    # `find_translations(root).items()`, and find_translations() used to
    # register a (translation, source) pair only when
    # `(root / source_rel).is_file()` was already True. So a translation
    # whose declared source was missing was invisible to check_c24 -- it
    # was not iterated at all, and (if it was the only translation
    # present) the check reported SKIP ("no translation is present")
    # rather than FAIL.
    #
    # find_translations() now registers a translation by filename
    # convention alone, regardless of whether its declared source exists,
    # so check_c24 can see it and apply the missing-source FAIL branch.
    # See test_missing_source_file_fails_not_skips below.
    # ------------------------------------------------------------------

    def test_files_naming_only_source_still_catches_stale_translation(self) -> None:
        # FIXED (Finding 1): a source/translation pair is selected when
        # EITHER member is selected, not only when the translation itself
        # is named. Naming just the English source with --files must not
        # let a stale translation slip through as an unselected PASS.
        stale_digest = "0" * 16
        self.assertNotEqual(stale_digest, source_digest())
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    SOURCE_REL: SOURCE_TEXT,
                    TRANSLATION_REL: translation_text(marker(stale_digest)),
                },
            )
            ctx = make_ctx(tmp, files=[SOURCE_REL])
            with self.assertRaises(ct.WarnCheck) as caught:
                ct.check_c24(ctx)
            self.assertTrue(
                any(TRANSLATION_REL in p for p in caught.exception.args[0]),
                caught.exception.args[0],
            )

    def test_duplicate_source_markers_fail(self) -> None:
        # FIXED (Finding 6, uniqueness half): two marker lines for the same
        # source must FAIL outright, naming the file and how many markers
        # were found, rather than silently using whichever comes first.
        digest = source_digest()
        duplicated = "\n".join(
            [marker(digest), marker("0" * 16), "# 主厨精选 OSS 启动模板", ""]
        )
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    SOURCE_REL: SOURCE_TEXT,
                    TRANSLATION_REL: duplicated,
                },
            )
            status, problems = run_one("C24", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(
            any(
                TRANSLATION_REL in p and "2" in p and "README.md" in p
                for p in problems
            ),
            problems,
        )

    def test_missing_source_file_fails_not_skips(self) -> None:
        # The translation exists and has a well-formed marker, but the
        # source file it names is not present anywhere in the tree.
        digest = source_digest()
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    TRANSLATION_REL: translation_text(marker(digest)),
                },
            )
            self.assertFalse((Path(tmp) / SOURCE_REL).exists())

            status, problems = run_one("C24", make_ctx(tmp))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(
            any("README.md" in p and "does not exist" in p for p in problems),
            problems,
        )


class TestUpdateDigests(unittest.TestCase):
    """``--update-digests`` rewrites only the source-marker line, in place."""

    def test_rewrites_only_the_digest_line(self) -> None:
        stale_digest = "0" * 16
        correct_digest = source_digest()
        before_lines = [
            marker(stale_digest),
            "# 主厨精选 OSS 启动模板",
            "",
            "中文内容，包含标点。",
            "",
            "* 列表项一",
            "* 列表项二",
            "",
        ]
        before_text = "\n".join(before_lines)
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {SOURCE_REL: SOURCE_TEXT, TRANSLATION_REL: before_text})
            translation_path = Path(tmp) / TRANSLATION_REL

            with contextlib.redirect_stdout(io.StringIO()) as out:
                ct.update_digests(Path(tmp))

            self.assertIn(stale_digest, out.getvalue())
            self.assertIn(correct_digest, out.getvalue())

            after_text = translation_path.read_text(encoding="utf-8")
            after_lines = after_text.split("\n")

        self.assertEqual(after_lines[0], marker(correct_digest))
        # Every line other than the marker itself must be byte-for-byte
        # unchanged -- this is the "only that one line" assertion.
        self.assertEqual(after_lines[1:], before_lines[1:])
        self.assertEqual(len(after_lines), len(before_lines))

    def test_duplicate_markers_refused_and_file_left_untouched(self) -> None:
        # FIXED (Finding 6, uniqueness half): update_digests must not
        # silently update whichever duplicate marker comes first -- it must
        # refuse the file, print a clear message, and leave every byte of
        # the file untouched.
        stale_digest = "0" * 16
        before_text = "\n".join(
            [marker(stale_digest), marker("1" * 16), "# 主厨精选 OSS 启动模板", ""]
        )
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {SOURCE_REL: SOURCE_TEXT, TRANSLATION_REL: before_text})
            translation_path = Path(tmp) / TRANSLATION_REL
            before_bytes = translation_path.read_bytes()

            with contextlib.redirect_stdout(io.StringIO()) as out:
                ct.update_digests(Path(tmp))

            after_bytes = translation_path.read_bytes()

        self.assertEqual(before_bytes, after_bytes)
        output = out.getvalue()
        self.assertIn(TRANSLATION_REL, output)
        self.assertIn("2", output)
        self.assertIn("README.md", output)

    def test_valid_marker_plus_malformed_duplicate_refused_and_untouched(self) -> None:
        # FIXED (Finding 5): ``_refresh_translation_digest`` is the shared
        # substitution implementation behind ``update_digests()`` for both
        # ``template/`` translations (this test) and the workspace
        # translation (see test_checks_translation's C27 test of the same
        # name). It must detect a malformed duplicate marker as a
        # candidate too, and refuse the whole file, rather than refreshing
        # the one well-formed marker line and silently leaving the
        # malformed duplicate behind.
        digest = source_digest()
        malformed = "<!-- translation-of: README.md sha256:NOTHEX -->"
        before_text = "\n".join(
            [marker(digest), malformed, "# 主厨精选 OSS 启动模板", ""]
        )
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {SOURCE_REL: SOURCE_TEXT, TRANSLATION_REL: before_text})
            translation_path = Path(tmp) / TRANSLATION_REL
            before_bytes = translation_path.read_bytes()

            with contextlib.redirect_stdout(io.StringIO()) as out:
                ct.update_digests(Path(tmp))

            after_bytes = translation_path.read_bytes()

        self.assertEqual(before_bytes, after_bytes)
        output = out.getvalue()
        self.assertIn(TRANSLATION_REL, output)
        self.assertIn("2", output)
        self.assertIn("README.md", output)

    def test_mixed_crlf_lf_endings_only_digest_bytes_change(self) -> None:
        # FIXED (Finding 4): update_digests must not open the file in text
        # mode (which would translate every "\n" to os.linesep on write),
        # and must not split on a single detected newline style (which
        # would corrupt marker detection / leave stray "\n" characters
        # embedded when a file mixes CRLF and LF). Every byte outside the
        # marker's digest must be identical before and after.
        stale_digest = "0" * 16
        correct_digest = source_digest()
        # A deliberately mixed-ending file: the marker line ends CRLF, the
        # rest end LF only.
        before_bytes = (
            marker(stale_digest).encode("utf-8")
            + b"\r\n"
            + "# 主厨精选 OSS 启动模板".encode("utf-8")
            + b"\n"
            + b"\n"
            + "中文内容，包含标点。".encode("utf-8")
            + b"\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, {SOURCE_REL: SOURCE_TEXT})
            translation_path = Path(tmp) / TRANSLATION_REL
            translation_path.write_bytes(before_bytes)

            with contextlib.redirect_stdout(io.StringIO()) as out:
                ct.update_digests(Path(tmp))

            after_bytes = translation_path.read_bytes()

        self.assertIn(stale_digest, out.getvalue())
        self.assertIn(correct_digest, out.getvalue())

        expected_bytes = (
            marker(correct_digest).encode("utf-8")
            + before_bytes[len(marker(stale_digest).encode("utf-8")) :]
        )
        self.assertEqual(after_bytes, expected_bytes)
        # Explicitly confirm the CRLF right after the marker, and the bare
        # LF endings later in the file, both survive untouched.
        self.assertIn(b"-->\r\n", after_bytes)
        self.assertNotIn(b"\r\n" + "中文内容，包含标点。".encode("utf-8"), after_bytes)

    def test_idempotent_second_run_updates_nothing(self) -> None:
        correct_digest = source_digest()
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(
                tmp,
                {
                    SOURCE_REL: SOURCE_TEXT,
                    TRANSLATION_REL: translation_text(marker(correct_digest)),
                },
            )
            translation_path = Path(tmp) / TRANSLATION_REL
            before_bytes = translation_path.read_bytes()

            with contextlib.redirect_stdout(io.StringIO()) as out:
                ct.update_digests(Path(tmp))

            after_bytes = translation_path.read_bytes()

        self.assertEqual(out.getvalue().strip(), "No digest needed updating.")
        self.assertEqual(before_bytes, after_bytes)


# ----------------------------------------------------------------------
# T014: C27 (Workspace translation freshness) and ``update_digests()``'s
# workspace branch.
#
# Contract: ``specs/003-workspace-self-compliance/contracts/tooling-delta-003.md``
# §5 C27 and §7. C27 is check_c24's structural twin, retargeted at the
# workspace homepage: ``README.md`` is the English source and
# ``README.zh-CN.md`` is its translation. Unlike check_c24, check_c27
# resolves both paths as ``Path(check_template.__file__).resolve().parent
# .parent`` -- the repository root -- and deliberately ignores
# ``ctx.template_dir`` (tooling-delta-003.md §2), the same rationale as
# check_c23, check_c25 and check_c26. A test that only pointed
# ``--template-dir`` elsewhere would still read the *real* ``README.md`` /
# ``README.zh-CN.md``, so every fixture here instead patches
# ``check_template.__file__`` via the ``FakeRepoRoot`` helper (copied from
# ``test_checks_contract_parity.py``, ``test_workspace_language.py`` and
# ``test_workspace_facts.py``) so the check's own path resolution lands
# under a throwaway temporary directory. ``update_digests()``'s workspace
# branch resolves ``repo_root`` the exact same way, so ``FakeRepoRoot``
# isolates that too. No test below reads or writes the real ``README.md``,
# ``README.zh-CN.md``, ``template/`` or
# ``specs/001-chefs-pick-starter/contracts/guidance-layer.md``.
#
# check_c27 (and check_c25/check_c26) SKIP unless ``README.md`` contains
# the language-selector line verbatim, so every fixture meant to be
# evaluated (rather than skipped) includes it.
# ----------------------------------------------------------------------

WORKSPACE_SOURCE_REL = "README.md"
WORKSPACE_TRANSLATION_REL = "README.zh-CN.md"

# Verbatim from tooling-delta-003.md §1's WORKSPACE_SELECTOR_LINES["README.md"].
WORKSPACE_SELECTOR_LINE = "**English** · [简体中文](README.zh-CN.md)"

WORKSPACE_SOURCE_TEXT = (
    "# Chef's Pick OSS Starter Workspace\n\n"
    f"{WORKSPACE_SELECTOR_LINE}\n\n"
    "Some workspace content.\n"
)


def workspace_source_digest(text: str = WORKSPACE_SOURCE_TEXT) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def workspace_marker(digest: str, source_name: str = "README.md") -> str:
    return f"<!-- translation-of: {source_name} sha256:{digest} -->"


def workspace_translation_text(marker_line: str | None) -> str:
    lines = []
    if marker_line is not None:
        lines.append(marker_line)
    lines += ["# 主厨精选 OSS 启动模板工作区", "", "中文内容。", ""]
    return "\n".join(lines)


def workspace_base_files(translation: str | None) -> dict[str, str]:
    """``template/`` (so ``template_dir.is_dir()`` holds) plus the pair."""
    files: dict[str, str] = {
        "template/.keep": "",
        WORKSPACE_SOURCE_REL: WORKSPACE_SOURCE_TEXT,
    }
    if translation is not None:
        files[WORKSPACE_TRANSLATION_REL] = translation
    return files


class FakeRepoRoot:
    """A temporary directory patched in as C27's repository root.

    Copied from ``test_checks_contract_parity.py``'s helper of the same
    name. Entering the context manager patches ``check_template.__file__``
    to ``<tmp>/tools/check_template.py`` (a path that need not exist on
    disk) so that ``check_c27``'s own ``repo_root = Path(__file__)
    .resolve().parent.parent`` resolves to ``<tmp>`` -- never to the real
    repository, and never to ``ctx.template_dir`` (which C27 ignores by
    design, per tooling-delta-003.md §2). ``update_digests()``'s workspace
    branch recomputes ``repo_root`` the same way, so this also isolates it
    from the real ``README.md`` / ``README.zh-CN.md``.
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


class TestC27WorkspaceTranslationFreshness(unittest.TestCase):
    """C27: the workspace homepage's translation stays fresh."""

    def test_fresh_marker_passes(self) -> None:
        digest = workspace_source_digest()
        with FakeRepoRoot() as fake:
            fake.write(
                workspace_base_files(
                    workspace_translation_text(workspace_marker(digest))
                )
            )
            status, problems = run_one("C27", make_ctx(fake.root))
        self.assertEqual(status, "PASS", problems)

    def test_source_marker_absent_fails(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write(workspace_base_files(workspace_translation_text(None)))
            status, problems = run_one("C27", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        self.assertTrue(
            any("missing or malformed" in p for p in problems), problems
        )
        self.assertTrue(
            any(WORKSPACE_TRANSLATION_REL in p for p in problems), problems
        )

    def test_duplicate_source_markers_fail_and_update_digests_refuses(self) -> None:
        # FAIL half: two marker lines for the same source must FAIL
        # outright, naming the file, how many markers were found, and the
        # source name -- same shape as check_c24's duplicate-marker FAIL.
        digest = workspace_source_digest()
        duplicated = "\n".join(
            [
                workspace_marker(digest),
                workspace_marker("0" * 16),
                "# 主厨精选 OSS 启动模板工作区",
                "",
            ]
        )
        with FakeRepoRoot() as fake:
            fake.write(workspace_base_files(duplicated))
            status, problems = run_one("C27", make_ctx(fake.root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(
                any(
                    WORKSPACE_TRANSLATION_REL in p
                    and "2" in p
                    and "README.md" in p
                    for p in problems
                ),
                problems,
            )

            # ``--update-digests`` half: it must refuse the file (never
            # guess which duplicate is authoritative) and leave every byte
            # of it untouched.
            translation_path = fake.root / WORKSPACE_TRANSLATION_REL
            before_bytes = translation_path.read_bytes()

            with contextlib.redirect_stdout(io.StringIO()) as out:
                ct.update_digests(fake.root / "template")

            after_bytes = translation_path.read_bytes()

        self.assertEqual(before_bytes, after_bytes)
        output = out.getvalue()
        self.assertIn(WORKSPACE_TRANSLATION_REL, output)
        self.assertIn("2", output)
        self.assertIn("README.md", output)

    def test_stale_marker_without_release_warns_with_exact_message_and_exits_zero(
        self,
    ) -> None:
        stale_digest = "0" * 16
        current_digest = workspace_source_digest()
        self.assertNotEqual(stale_digest, current_digest)
        with FakeRepoRoot() as fake:
            fake.write(
                workspace_base_files(
                    workspace_translation_text(workspace_marker(stale_digest))
                )
            )
            ctx = make_ctx(fake.root, release=False)
            with self.assertRaises(ct.WarnCheck) as caught:
                ct.check_c27(ctx)
            messages = caught.exception.args[0]
            self.assertTrue(messages)
            self.assertEqual(
                messages[0],
                f"{WORKSPACE_TRANSLATION_REL}: source marker is stale for "
                f"README.md (recorded {stale_digest}, current "
                f"{current_digest}); run python3 tools/check_template.py "
                "--update-digests",
            )

            # FR-014 (§1.1): WARN never affects the exit code, so the whole
            # process must still exit 0.
            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = ct.main(
                    ["--template-dir", str(fake.root), "--only", "C27"]
                )
        self.assertEqual(exit_code, 0)

    def test_stale_marker_with_release_fails_and_exits_one(self) -> None:
        stale_digest = "0" * 16
        with FakeRepoRoot() as fake:
            fake.write(
                workspace_base_files(
                    workspace_translation_text(workspace_marker(stale_digest))
                )
            )
            ctx = make_ctx(fake.root, release=True)
            # Under --release the same staleness is returned as an ordinary
            # FAIL list, not raised as a WarnCheck (§1.1).
            problems = ct.check_c27(ctx)
            self.assertTrue(problems)

            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = ct.main(
                    [
                        "--template-dir",
                        str(fake.root),
                        "--only",
                        "C27",
                        "--release",
                    ]
                )
        self.assertEqual(exit_code, 1)

    def test_missing_selector_in_source_fails(self) -> None:
        # FIXED (Finding 2): no language-selector line anywhere in
        # README.md used to be the tooling-delta-003.md §2 SkipCheck
        # predicate -- deleting or misspelling that one line silently
        # turned C27 (and C25, C26) off. It is now a FAIL, naming
        # README.md and what is missing; ``template/`` still exists here,
        # so this is not the "not the workspace repository" case that
        # remains a SkipCheck (see test_missing_template_dir_still_skips).
        no_selector_source = WORKSPACE_SOURCE_TEXT.replace(
            f"{WORKSPACE_SELECTOR_LINE}\n\n", ""
        )
        self.assertNotIn(WORKSPACE_SELECTOR_LINE, no_selector_source)
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    "template/.keep": "",
                    WORKSPACE_SOURCE_REL: no_selector_source,
                }
            )
            status, problems = run_one("C27", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(WORKSPACE_SOURCE_REL, joined)
        self.assertIn("language selector", joined)

    def test_missing_readme_fails(self) -> None:
        # FIXED (Finding 2): README.md itself missing is a FAIL, not a
        # SkipCheck, once ``template/`` exists.
        with FakeRepoRoot() as fake:
            fake.write({"template/.keep": ""})
            status, problems = run_one("C27", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(WORKSPACE_SOURCE_REL, joined)
        self.assertIn("does not exist", joined)

    def test_missing_template_dir_still_skips(self) -> None:
        # The one remaining SkipCheck predicate (Finding 2): ``template/``
        # does not exist at all, i.e. this is not the workspace repository.
        with FakeRepoRoot() as fake:
            fake.write({WORKSPACE_SOURCE_REL: WORKSPACE_SOURCE_TEXT})
            self.assertFalse((fake.root / "template").exists())
            status, reason = run_one("C27", make_ctx(fake.root))
        self.assertEqual(status, "SKIP", reason)

    def test_valid_marker_plus_malformed_duplicate_fails_and_refresh_refuses(
        self,
    ) -> None:
        # FIXED (Finding 5): a well-formed marker line sitting next to a
        # malformed duplicate for the same source used to slip through as
        # a PASS -- DIGEST_RE's strict match found only the well-formed
        # line and never noticed the malformed one. Candidate detection
        # (permissive on the digest) must catch both lines and FAIL with
        # "found 2 source marker lines", and update-digests must refuse to
        # touch the file rather than refreshing the valid line and leaving
        # the malformed one behind.
        digest = workspace_source_digest()
        malformed = "<!-- translation-of: README.md sha256:NOTHEX -->"
        mixed = "\n".join(
            [
                workspace_marker(digest),
                malformed,
                "# 主厨精选 OSS 启动模板工作区",
                "",
            ]
        )
        with FakeRepoRoot() as fake:
            fake.write(workspace_base_files(mixed))
            status, problems = run_one("C27", make_ctx(fake.root))
            self.assertEqual(status, "FAIL", problems)
            self.assertTrue(
                any(
                    WORKSPACE_TRANSLATION_REL in p
                    and "2" in p
                    and "README.md" in p
                    for p in problems
                ),
                problems,
            )

            translation_path = fake.root / WORKSPACE_TRANSLATION_REL
            before_bytes = translation_path.read_bytes()

            with contextlib.redirect_stdout(io.StringIO()) as out:
                ct.update_digests(fake.root / "template")

            after_bytes = translation_path.read_bytes()

        self.assertEqual(before_bytes, after_bytes)
        self.assertIn(WORKSPACE_TRANSLATION_REL, out.getvalue())

    def test_missing_translation_fails_naming_it(self) -> None:
        # FIXED (Finding 6): the selector is in place but
        # README.zh-CN.md itself does not exist -- C27 must FAIL naming
        # the missing marker/file, not skip.
        with FakeRepoRoot() as fake:
            fake.write(workspace_base_files(None))
            status, problems = run_one("C27", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn(WORKSPACE_TRANSLATION_REL, joined)
        self.assertIn("missing or malformed", joined)


class TestUpdateDigestsWorkspaceBranch(unittest.TestCase):
    """``update_digests()``'s workspace branch (tooling-delta-003.md §7).

    Reuses the exact same in-place substitution helper as the ``template/``
    translations -- not a second implementation -- so this pins down only
    the parts specific to routing through the workspace paths.
    """

    def test_rewrites_only_the_workspace_digest_line(self) -> None:
        stale_digest = "0" * 16
        correct_digest = workspace_source_digest()
        before_lines = [
            workspace_marker(stale_digest),
            "# 主厨精选 OSS 启动模板工作区",
            "",
            "中文内容，包含标点。",
            "",
        ]
        before_text = "\n".join(before_lines)
        with FakeRepoRoot() as fake:
            fake.write(workspace_base_files(before_text))
            translation_path = fake.root / WORKSPACE_TRANSLATION_REL

            with contextlib.redirect_stdout(io.StringIO()) as out:
                ct.update_digests(fake.root / "template")

            self.assertIn(stale_digest, out.getvalue())
            self.assertIn(correct_digest, out.getvalue())

            after_text = translation_path.read_text(encoding="utf-8")
            after_lines = after_text.split("\n")

        self.assertEqual(after_lines[0], workspace_marker(correct_digest))
        self.assertEqual(after_lines[1:], before_lines[1:])
        self.assertEqual(len(after_lines), len(before_lines))

    def test_missing_workspace_translation_is_silently_skipped(self) -> None:
        # tooling-delta-003.md §7: silently skipped when the workspace
        # translation does not exist yet -- must not raise, and must not
        # create the file.
        with FakeRepoRoot() as fake:
            fake.write(workspace_base_files(None))
            translation_path = fake.root / WORKSPACE_TRANSLATION_REL
            self.assertFalse(translation_path.exists())

            with contextlib.redirect_stdout(io.StringIO()) as out:
                ct.update_digests(fake.root / "template")

            self.assertFalse(translation_path.exists())
        self.assertEqual(out.getvalue().strip(), "No digest needed updating.")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
