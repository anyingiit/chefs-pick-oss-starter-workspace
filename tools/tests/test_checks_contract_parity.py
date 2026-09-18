"""Tests for C23 (contract parity).

Contract: ``specs/002-english-first-docs/contracts/tooling-delta.md`` §1.1
(SKIP is unaffected by the exit code / WARN framework) and §5 C23:

- left side: every ``★ N (owner/repo)`` in
  ``specs/001-chefs-pick-starter/contracts/guidance-layer.md``;
- right side: every ``★ N (owner/repo)`` in any ``.md`` file under
  ``template/``;
- for every ``owner/repo`` on both sides, ``N`` must agree, reported as
  ``owner/repo: contract N1 vs template N2``;
- a repo on only one side is not an error;
- a missing contract file is a SKIP.

C23's own docstring says it deliberately resolves both paths *relative to
the repository root* (``Path(__file__).resolve().parent.parent``), never to
``ctx.template_dir`` -- so ``--template-dir`` (and therefore the ``ctx``
built by ``helpers.make_ctx``) has no effect on it. The only seam the real
implementation exposes for injecting a fixture is the module's own
``__file__`` global: ``check_c23`` recomputes ``Path(__file__)`` on every
call, and a function's bare ``__file__`` reference is looked up from the
module's globals at call time, so patching ``check_template.__file__`` to a
path under a temporary directory redirects ``repo_root`` there without
touching ``tools/check_template.py`` and without needing a real
``tools/check_template.py`` to exist at that patched path (``Path.resolve()``
does not require the path to exist). This is the "monkeypatch" branch of
the task description; no full repo checkout is necessary.
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


CONTRACT_REL = "specs/001-chefs-pick-starter/contracts/guidance-layer.md"


class FakeRepoRoot:
    """A temporary directory patched in as C23's repository root.

    Entering the context manager patches ``check_template.__file__`` to
    ``<tmp>/tools/check_template.py`` (a path that need not exist on disk)
    so that ``check_c23``'s own ``repo_root = Path(__file__).resolve()
    .parent.parent`` resolves to ``<tmp>``.
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


class TestC23ContractParity(unittest.TestCase):
    """C23: the 001 contract's star counts agree with ``template/``."""

    def test_matching_counts_pass(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    CONTRACT_REL: "See ★ 1,234 (octocat/hello-world).\n",
                    "template/GUIDE.md": "Cited as ★ 1,234 (octocat/hello-world).\n",
                }
            )
            # ctx.template_dir is irrelevant to C23; point it anywhere sane.
            status, problems = run_one("C23", make_ctx(fake.root))
        self.assertEqual(status, "PASS", problems)

    def test_mismatched_count_fails_with_both_numbers(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    CONTRACT_REL: "See ★ 1,234 (octocat/hello-world).\n",
                    "template/GUIDE.md": "Cited as ★ 999 (octocat/hello-world).\n",
                }
            )
            status, problems = run_one("C23", make_ctx(fake.root))
        self.assertEqual(status, "FAIL", problems)
        joined = "\n".join(problems)
        self.assertIn("octocat/hello-world", joined)
        # The report must carry both the contract-side and the
        # template-side figures, not just one of them.
        self.assertIn("1234", joined)
        self.assertIn("999", joined)

    def test_repo_on_only_one_side_passes(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write(
                {
                    CONTRACT_REL: (
                        "See ★ 1,234 (octocat/hello-world) and "
                        "★ 42 (only/in-contract).\n"
                    ),
                    "template/GUIDE.md": (
                        "Cited as ★ 1,234 (octocat/hello-world) and "
                        "★ 7 (only/in-template).\n"
                    ),
                }
            )
            status, problems = run_one("C23", make_ctx(fake.root))
        self.assertEqual(status, "PASS", problems)

    def test_missing_contract_file_skips(self) -> None:
        with FakeRepoRoot() as fake:
            fake.write({"template/GUIDE.md": "Cited as ★ 1 (a/b).\n"})
            status, reason = run_one("C23", make_ctx(fake.root))
        self.assertEqual(status, "SKIP", reason)
        self.assertIn("guidance-layer.md", " ".join(reason))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
