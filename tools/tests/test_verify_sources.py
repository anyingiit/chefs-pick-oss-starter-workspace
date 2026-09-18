"""Tests for ``tools/verify_sources.py``.

Contracts: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §2 and §3,
``specs/001-chefs-pick-starter/contracts/guidance-layer.md`` §0, §1 (3),
§4.1, §4.2 and §4.3.

Written before the implementation (T040 precedes T042), so importing
``verify_sources`` fails until the tool exists.  That red light is expected.

The contract fixes the function names and signatures but not the shape of
their payloads, so these tests pin the reading that follows from §2:

* ``parse_adoption_table(text)`` takes the whole ``SOURCES.md`` text and
  returns one entry per data row, in table order;
* ``render_adoption_table(rows)`` turns those entries back into the table
  markdown (header row, separator row, data rows -- no ``adoption-data``
  markers), so that rendering what was parsed reproduces the original;
* ``apply_updates(files, results, today)`` takes ``{relative path: text}``,
  ``results`` as ``{slug: fetch_repo(slug) payload}``, and ``today`` as a
  ``datetime.date``; it returns the updated ``{relative path: text}``.

No test touches the network: ``gh_ready`` and ``fetch_repo`` are always
mocked.
"""

from __future__ import annotations

import datetime as dt
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import verify_sources as vs  # noqa: E402

SOURCES_REL = ".github/chefs-pick/SOURCES.md"
README_REL = ".github/README.md"

TABLE_HEADER = "| Repo | Stars | Forks | Last commit | License | Archived | Verified |"
TABLE_SEP = "|---|---:|---:|---|---|---|---|"

REMINDER = (
    "Also re-check non-repository evidence manually: official platform "
    "features and the Contributor Covenant adopters list."
)

# Two repositories are enough for the parse/render/update cases.
BASE_ROWS = [
    {
        "repo": "othneildrew/Best-README-Template",
        "stars": "16,360",
        "forks": "3,113",
        "last_commit": "2026-01-05",
        "license": "Unlicense",
        "archived": "no",
    },
    {
        "repo": "github/gitignore",
        "stars": "175,810",
        "forks": "82,184",
        "last_commit": "2026-02-11",
        "license": "CC0-1.0",
        "archived": "no",
    },
]

BASE_VERIFIED = "2026-03-01"
TODAY = dt.date(2026, 9, 18)


def row_line(row: dict, verified: str) -> str:
    return (
        f"| {row['repo']} | {row['stars']} | {row['forks']} | "
        f"{row['last_commit']} | {row['license']} | {row['archived']} | {verified} |"
    )


def adoption_table(rows, verified: str) -> str:
    """The table markdown between the two ``adoption-data`` markers."""
    lines = [TABLE_HEADER, TABLE_SEP] + [row_line(r, verified) for r in rows]
    return "\n".join(lines)


def sources_md(rows=None, verified: str = BASE_VERIFIED) -> str:
    """A minimal ``SOURCES.md``: §4.1 date line, §4.2 field tables, §4.3 table."""
    rows = BASE_ROWS if rows is None else rows
    sections = []
    for index, row in enumerate(rows, start=1):
        sections.append(
            f"### M{index:02d} 模块 / Module\n"
            "\n"
            "| 字段 / Field | 内容 / Value |\n"
            "|---|---|\n"
            "| Evidence | Exact stars: "
            f"★ {row['stars']} ({row['repo']}) |\n"
            f"| Verified | {verified} |\n"
        )
    return (
        "# Selection list\n"
        "\n"
        f"Data verified: {verified}\n"
        "\n"
        "## Modules\n"
        "\n"
        + "\n".join(sections)
        + "\n"
        "## 认可度数据 / Adoption data\n"
        "\n"
        "<!-- adoption-data:start -->\n"
        f"{adoption_table(rows, verified)}\n"
        "<!-- adoption-data:end -->\n"
    )


def readme_md(rows=None, verified: str = BASE_VERIFIED) -> str:
    """A minimal ``.github/README.md`` with the §1 (3) summary table."""
    rows = BASE_ROWS if rows is None else rows
    summary = "\n".join(
        f"| M{index:02d} 模块 / Module | {row['repo']} | "
        f"★ {row['stars']} ({row['repo']}) | {verified} |"
        for index, row in enumerate(rows, start=1)
    )
    return (
        "# Chef's Pick OSS Starter · 主厨精选开源仓库起步模板\n"
        "\n"
        "## 主厨精选一览 / The picks at a glance\n"
        "\n"
        "<!-- summary:start -->\n"
        "| Module | Pick | Adoption | Verified |\n"
        "|---|---|---|---|\n"
        f"{summary}\n"
        "<!-- summary:end -->\n"
    )


def payload(
    slug: str,
    stars: int,
    forks: int = 1_000,
    last_commit: str = "2026-09-10",
    license_: str = "MIT",
    archived: bool = False,
    full_name: str | None = None,
) -> dict:
    """A ``fetch_repo`` return value (tooling §2)."""
    return {
        "full_name": slug if full_name is None else full_name,
        "stars": stars,
        "forks": forks,
        "last_commit": last_commit,
        "license": license_,
        "archived": archived,
    }


def write_template(root: Path, rows=None, verified: str = BASE_VERIFIED) -> Path:
    """Write the two guidance-layer files a run needs, return the template dir."""
    rows = BASE_ROWS if rows is None else rows
    for rel, text in (
        (SOURCES_REL, sources_md(rows, verified)),
        (README_REL, readme_md(rows, verified)),
    ):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


class TempTemplateCase(unittest.TestCase):
    """Base class giving each test a throwaway template directory."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def snapshot(self) -> dict:
        return {
            rel: (self.root / rel).read_text(encoding="utf-8")
            for rel in (SOURCES_REL, README_REL)
        }

    def run_main(self, *args) -> tuple[int, str]:
        """Run ``main`` with the temp template dir; return (exit code, output).

        ``repo_root()`` is patched to this same temp directory for the
        duration of the call. ``main()`` resolves the verbatim contract
        (tooling-delta.md §6) from ``repo_root()``, deliberately independent
        of ``--template-dir`` -- so without this patch a ``--write`` run
        here would reach through to the *real* repository's
        ``specs/001-chefs-pick-starter/contracts/guidance-layer.md`` instead
        of staying inside the throwaway directory. See
        ``RealContractUntouchedTests`` for the regression guard.
        """
        out, err = io.StringIO(), io.StringIO()
        argv = ["--template-dir", str(self.root), "--today", TODAY.isoformat()]
        argv.extend(args)
        with mock.patch.object(vs, "repo_root", return_value=self.root), \
                redirect_stdout(out), redirect_stderr(err):
            code = vs.main(argv)
        return code, out.getvalue() + err.getvalue()


class AdoptionTableTests(unittest.TestCase):
    """tooling §3: parsing then rendering reproduces the original table."""

    def test_parse_then_render_round_trips(self) -> None:
        text = sources_md()
        rows = vs.parse_adoption_table(text)
        self.assertEqual(len(rows), len(BASE_ROWS))
        self.assertEqual(
            vs.render_adoption_table(rows).strip(),
            adoption_table(BASE_ROWS, BASE_VERIFIED).strip(),
        )

    def test_render_is_stable_on_a_second_round_trip(self) -> None:
        once = vs.render_adoption_table(vs.parse_adoption_table(sources_md()))
        twice = vs.render_adoption_table(vs.parse_adoption_table(sources_md()))
        self.assertEqual(once, twice)


class ApplyUpdatesTests(unittest.TestCase):
    """tooling §2 ``--write`` steps 1-4, exercised directly on text."""

    def setUp(self) -> None:
        self.files = {SOURCES_REL: sources_md(), README_REL: readme_md()}
        self.results = {
            "othneildrew/Best-README-Template": payload(
                "othneildrew/Best-README-Template",
                stars=16_500,
                forks=3_200,
                last_commit="2026-09-10",
                license_="Unlicense",
            ),
            "github/gitignore": payload(
                "github/gitignore",
                stars=176_000,
                forks=82_500,
                last_commit="2026-08-30",
                license_="CC0-1.0",
            ),
        }
        self.updated = vs.apply_updates(self.files, self.results, TODAY)

    def test_rewrites_the_data_table_keeping_row_order(self) -> None:
        sources = self.updated[SOURCES_REL]
        self.assertIn(
            "| othneildrew/Best-README-Template | 16,500 | 3,200 | 2026-09-10 "
            "| Unlicense | no | 2026-09-18 |",
            sources,
        )
        self.assertIn(
            "| github/gitignore | 176,000 | 82,500 | 2026-08-30 "
            "| CC0-1.0 | no | 2026-09-18 |",
            sources,
        )
        self.assertLess(
            sources.index("| othneildrew/Best-README-Template | 16,500"),
            sources.index("| github/gitignore | 176,000"),
        )

    def test_rewrites_star_counts_everywhere(self) -> None:
        for rel in (SOURCES_REL, README_REL):
            text = self.updated[rel]
            self.assertIn("★ 16,500 (othneildrew/Best-README-Template)", text)
            self.assertIn("★ 176,000 (github/gitignore)", text)
            self.assertNotIn("16,360", text)
            self.assertNotIn("175,810", text)

    def test_rewrites_all_four_date_places(self) -> None:
        sources = self.updated[SOURCES_REL]
        readme = self.updated[README_REL]
        # 1. the "Data verified" line
        self.assertIn("Data verified: 2026-09-18", sources)
        # 2. every module field-table "Verified" cell
        self.assertEqual(sources.count("| Verified | 2026-09-18 |"), 2)
        # 3. the "Verified" column of the adoption data table
        self.assertEqual(sources.count("| no | 2026-09-18 |"), 2)
        # 4. the "Verified" column of the summary table on the home page
        self.assertEqual(readme.count("| 2026-09-18 |"), 2)
        # and no stale date survives anywhere
        self.assertNotIn(BASE_VERIFIED, sources)
        self.assertNotIn(BASE_VERIFIED, readme)

    def test_keeps_an_archived_flag_as_yes(self) -> None:
        results = dict(self.results)
        results["github/gitignore"] = payload(
            "github/gitignore",
            stars=176_000,
            forks=82_500,
            last_commit="2026-08-30",
            license_="CC0-1.0",
            archived=True,
        )
        updated = vs.apply_updates(
            {SOURCES_REL: sources_md(), README_REL: readme_md()}, results, TODAY
        )
        self.assertIn(
            "| github/gitignore | 176,000 | 82,500 | 2026-08-30 "
            "| CC0-1.0 | yes | 2026-09-18 |",
            updated[SOURCES_REL],
        )


class ReportFlagTests(TempTemplateCase):
    """tooling §2: the STALE, ARCHIVED and RENAMED flags."""

    ROWS = [
        {
            "repo": "fresh/keeper",
            "stars": "1,000",
            "forks": "100",
            "last_commit": "2026-09-01",
            "license": "MIT",
            "archived": "no",
        },
        {
            "repo": "stale/upstream",
            "stars": "2,000",
            "forks": "200",
            "last_commit": "2025-01-01",
            "license": "MIT",
            "archived": "no",
        },
        {
            "repo": "sunset/upstream",
            "stars": "3,000",
            "forks": "300",
            "last_commit": "2026-05-01",
            "license": "MIT",
            "archived": "no",
        },
        {
            "repo": "old/name",
            "stars": "4,000",
            "forks": "400",
            "last_commit": "2026-06-01",
            "license": "MIT",
            "archived": "no",
        },
        {
            "repo": "Mixed/Case",
            "stars": "5,000",
            "forks": "500",
            "last_commit": "2026-07-01",
            "license": "MIT",
            "archived": "no",
        },
    ]

    # 2025-09-18 is exactly 365 days before TODAY, so 2025-01-01 is stale.
    FETCHED = {
        "fresh/keeper": payload("fresh/keeper", 1_100, last_commit="2026-09-01"),
        "stale/upstream": payload("stale/upstream", 2_100, last_commit="2025-01-01"),
        "sunset/upstream": payload(
            "sunset/upstream", 3_100, last_commit="2026-05-01", archived=True
        ),
        "old/name": payload(
            "old/name", 4_100, last_commit="2026-06-01", full_name="new/name"
        ),
        # same slug in a different case: not a rename
        "Mixed/Case": payload(
            "Mixed/Case", 5_100, last_commit="2026-07-01", full_name="mixed/case"
        ),
    }

    def setUp(self) -> None:
        super().setUp()
        write_template(self.root, self.ROWS)
        with mock.patch.object(vs, "gh_ready", return_value=True), mock.patch.object(
            vs, "fetch_repo", side_effect=lambda slug: self.FETCHED[slug]
        ):
            self.code, self.output = self.run_main()

    def line_for(self, slug: str) -> str:
        for line in self.output.splitlines():
            if slug in line:
                return line
        raise AssertionError(f"no report line mentions {slug!r}: {self.output!r}")

    def test_exit_code_is_zero(self) -> None:
        self.assertEqual(self.code, 0)

    def test_healthy_repository_has_no_flags(self) -> None:
        line = self.line_for("fresh/keeper")
        for flag in ("STALE", "ARCHIVED", "RENAMED"):
            self.assertNotIn(flag, line)

    def test_stale_flag(self) -> None:
        self.assertIn("STALE", self.line_for("stale/upstream"))
        self.assertNotIn("STALE", self.line_for("sunset/upstream"))

    def test_archived_flag(self) -> None:
        self.assertIn("ARCHIVED", self.line_for("sunset/upstream"))
        self.assertNotIn("ARCHIVED", self.line_for("fresh/keeper"))

    def test_renamed_flag(self) -> None:
        self.assertIn("RENAMED→new/name", self.line_for("old/name"))

    def test_case_only_difference_is_not_a_rename(self) -> None:
        self.assertNotIn("RENAMED", self.line_for("Mixed/Case"))

    def test_manual_reminder_is_printed(self) -> None:
        self.assertIn(REMINDER, self.output)


class MainExitCodeTests(TempTemplateCase):
    """tooling §2: exit codes 0, 1 and 2, and when writing happens."""

    def setUp(self) -> None:
        super().setUp()
        write_template(self.root)
        self.before = self.snapshot()
        self.fetched = {
            "othneildrew/Best-README-Template": payload(
                "othneildrew/Best-README-Template",
                stars=16_500,
                forks=3_200,
                last_commit="2026-09-10",
                license_="Unlicense",
            ),
            "github/gitignore": payload(
                "github/gitignore",
                stars=176_000,
                forks=82_500,
                last_commit="2026-08-30",
                license_="CC0-1.0",
            ),
        }

    def test_exit_code_zero_when_every_lookup_succeeds(self) -> None:
        with mock.patch.object(vs, "gh_ready", return_value=True), mock.patch.object(
            vs, "fetch_repo", side_effect=lambda slug: self.fetched[slug]
        ):
            code, output = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("othneildrew/Best-README-Template", output)
        # without --write nothing on disk changes
        self.assertEqual(self.snapshot(), self.before)

    def test_write_updates_the_files(self) -> None:
        with mock.patch.object(vs, "gh_ready", return_value=True), mock.patch.object(
            vs, "fetch_repo", side_effect=lambda slug: self.fetched[slug]
        ):
            code, _output = self.run_main("--write")
        self.assertEqual(code, 0)
        after = self.snapshot()
        self.assertIn("★ 16,500 (othneildrew/Best-README-Template)", after[SOURCES_REL])
        self.assertIn("★ 176,000 (github/gitignore)", after[README_REL])
        self.assertIn("Data verified: 2026-09-18", after[SOURCES_REL])
        self.assertIn(
            "| github/gitignore | 176,000 | 82,500 | 2026-08-30 "
            "| CC0-1.0 | no | 2026-09-18 |",
            after[SOURCES_REL],
        )

    def test_exit_code_one_and_no_write_when_a_lookup_fails(self) -> None:
        def fetch(slug):
            if slug == "github/gitignore":
                raise subprocess.CalledProcessError(1, ["gh", "api", f"repos/{slug}"])
            return self.fetched[slug]

        with mock.patch.object(vs, "gh_ready", return_value=True), mock.patch.object(
            vs, "fetch_repo", side_effect=fetch
        ):
            code, _output = self.run_main("--write")
        self.assertEqual(code, 1)
        self.assertEqual(self.snapshot(), self.before)

    def test_exit_code_two_when_gh_is_not_ready(self) -> None:
        with mock.patch.object(vs, "gh_ready", return_value=False), mock.patch.object(
            vs, "fetch_repo"
        ) as fetch:
            code, _output = self.run_main("--write")
        self.assertEqual(code, 2)
        fetch.assert_not_called()
        self.assertEqual(self.snapshot(), self.before)


class GhReadyTests(unittest.TestCase):
    """tooling §2: ``gh_ready`` checks the CLI is installed before anything else."""

    def test_false_when_gh_is_not_installed(self) -> None:
        with mock.patch.object(vs.shutil, "which", return_value=None) as which:
            self.assertFalse(vs.gh_ready())
        which.assert_called_once_with("gh")


class ReplaceStarRefsTests(unittest.TestCase):
    """T019: verbatim-contract writing (tooling-delta.md §6) -- ``replace_star_refs``."""

    def test_replaces_a_known_repos_star_count(self) -> None:
        text = "Before ★ 8,882 (actions/checkout) after."
        result = vs.replace_star_refs(text, {"actions/checkout": "9,000"})
        self.assertEqual(result, "Before ★ 9,000 (actions/checkout) after.")

    def test_leaves_an_unlisted_repo_untouched(self) -> None:
        # guidance-layer.md §0's own worked example uses the literal
        # "owner/repo" slug, which is not a real repository and never
        # appears in stars_by_repo -- it must survive verbatim.
        text = "§0 example: ★ 123 (owner/repo) illustrates the format."
        result = vs.replace_star_refs(text, {"actions/checkout": "9,000"})
        self.assertEqual(result, text)

    def test_replaces_every_occurrence_of_the_same_repo(self) -> None:
        text = (
            "First: ★ 1 (foo/bar). "
            "Second: ★ 1 (foo/bar). "
            "Third: ★ 1 (foo/bar)."
        )
        result = vs.replace_star_refs(text, {"foo/bar": "2"})
        self.assertEqual(result.count("★ 2 (foo/bar)"), 3)
        self.assertNotIn("★ 1 (foo/bar)", result)


class ContractStarDiffsTests(unittest.TestCase):
    """T019: verbatim-contract drift reporting -- ``contract_star_diffs``."""

    def test_reports_a_repo_whose_star_count_changed(self) -> None:
        text = "★ 8,882 (actions/checkout) and, separately, ★ 42 (owner/repo)."
        diffs = vs.contract_star_diffs(text, {"actions/checkout": "9,000"})
        self.assertEqual(diffs, [("actions/checkout", "8,882", "9,000")])

    def test_empty_when_the_contract_already_matches(self) -> None:
        text = "★ 9,000 (actions/checkout)"
        diffs = vs.contract_star_diffs(text, {"actions/checkout": "9,000"})
        self.assertEqual(diffs, [])

    def test_a_repo_absent_from_stars_by_repo_produces_no_diff(self) -> None:
        # Same rule as replace_star_refs: an unmatched repo (e.g. the §0
        # example) is not reported as drift, since it is never rewritten.
        text = "★ 42 (owner/repo)"
        diffs = vs.contract_star_diffs(text, {"actions/checkout": "9,000"})
        self.assertEqual(diffs, [])


class MissingContractFileTests(TempTemplateCase):
    """T019: tooling-delta.md §6 -- a missing verbatim contract is not an error.

    ``main()`` decides whether the contract exists inline (it is not split
    into a separate helper), so the finest-grained test available is at the
    ``main()`` level: point ``repo_root()`` at a directory that has no
    ``specs/001-chefs-pick-starter/contracts/guidance-layer.md`` and confirm
    the run still succeeds and reports the file as skipped rather than
    erroring.
    """

    def test_main_succeeds_and_notes_the_skip_when_the_contract_is_absent(self) -> None:
        write_template(self.root)
        fetched = {
            "othneildrew/Best-README-Template": payload(
                "othneildrew/Best-README-Template", stars=16_500
            ),
            "github/gitignore": payload("github/gitignore", stars=176_000),
        }
        with mock.patch.object(
            vs, "repo_root", return_value=self.root
        ), mock.patch.object(vs, "gh_ready", return_value=True), mock.patch.object(
            vs, "fetch_repo", side_effect=lambda slug: fetched[slug]
        ):
            code, output = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("note: contract file not found, skipped:", output)


class RealContractUntouchedTests(TempTemplateCase):
    """Regression guard for the test-isolation bug fixed alongside T018/T019.

    ``main()`` deliberately resolves the verbatim contract (§6 of
    ``specs/002-english-first-docs/contracts/tooling-delta.md``) from
    ``repo_root()``, independent of ``--template-dir`` -- that part is
    correct production behaviour. But it means any test that drives
    ``main(["--write", ...])`` without also pointing ``repo_root()`` at a
    throwaway directory silently writes through to the *real*
    ``specs/001-chefs-pick-starter/contracts/guidance-layer.md``. That is
    exactly what happened before ``TempTemplateCase.run_main`` patched
    ``repo_root()``: a run using fixture data (``★ 16,500`` /
    ``★ 176,000``) corrupted the genuine contract file on disk.

    This test exercises the same ``--write`` + contract-present path against
    a private fixture contract inside ``self.root``, and independently
    confirms the real repository file was not touched at all -- neither its
    content nor its mtime. If ``run_main`` (or any future test) ever drops
    the ``repo_root()`` patch, this is the test that must fail.
    """

    REAL_CONTRACT = Path(__file__).resolve().parents[2] / vs.CONTRACT_REL

    def test_write_run_leaves_the_real_contract_file_untouched(self) -> None:
        before_text = self.REAL_CONTRACT.read_text(encoding="utf-8")
        before_mtime_ns = self.REAL_CONTRACT.stat().st_mtime_ns

        write_template(self.root)
        # A private fixture contract inside the temp root -- using the same
        # star counts the real contract happens to hold for these repos, so
        # a failure to isolate would corrupt the real file the same way the
        # original bug did.
        fixture_contract = self.root / vs.CONTRACT_REL
        fixture_contract.parent.mkdir(parents=True, exist_ok=True)
        fixture_contract.write_text(
            "★ 16,360 (othneildrew/Best-README-Template) and "
            "★ 175,810 (github/gitignore).",
            encoding="utf-8",
        )

        fetched = {
            "othneildrew/Best-README-Template": payload(
                "othneildrew/Best-README-Template", stars=16_500
            ),
            "github/gitignore": payload("github/gitignore", stars=176_000),
        }
        with mock.patch.object(vs, "gh_ready", return_value=True), mock.patch.object(
            vs, "fetch_repo", side_effect=lambda slug: fetched[slug]
        ):
            code, _output = self.run_main("--write")
        self.assertEqual(code, 0)

        # The contract-writing branch did run, against the fixture only.
        after_fixture = fixture_contract.read_text(encoding="utf-8")
        self.assertIn("★ 16,500 (othneildrew/Best-README-Template)", after_fixture)
        self.assertIn("★ 176,000 (github/gitignore)", after_fixture)

        # The real repository contract is byte-for-byte and mtime-for-mtime
        # unchanged.
        after_text = self.REAL_CONTRACT.read_text(encoding="utf-8")
        after_mtime_ns = self.REAL_CONTRACT.stat().st_mtime_ns
        self.assertEqual(after_text, before_text)
        self.assertEqual(after_mtime_ns, before_mtime_ns)


if __name__ == "__main__":
    unittest.main()
