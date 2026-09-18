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


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
