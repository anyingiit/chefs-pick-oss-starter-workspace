"""Tests for C12 (selection list).

Contract: ``specs/001-chefs-pick-starter/contracts/tooling.md`` §1.3 C12 and §3;
``specs/001-chefs-pick-starter/contracts/guidance-layer.md`` §1 §4.1 §4.2 §4.3
§4.4 §4.5; ``specs/001-chefs-pick-starter/data-model.md`` (AdoptionEvidence,
SelectionDecision).

Every fixture is built by :func:`build`, so each failing case differs from the
passing one in exactly one place.
"""

from __future__ import annotations

import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import make_ctx, run_one, write_tree  # noqa: E402

import check_template as ct  # noqa: E402


# --------------------------------------------------------------------------
# Dates
# --------------------------------------------------------------------------

TODAY = dt.date(2026, 9, 18)
VERIFIED = "2026-09-18"

# guidance-layer §4.3: the upstream commit date may legitimately be old.
LAST_COMMIT = "2026-09-11"
OLD_LAST_COMMIT = "2019-01-01"

# 256 days before TODAY: over FRESH_DAYS (183).
STALE = "2026-01-05"
# 48 days before TODAY: within 183 but over RELEASE_FRESH_DAYS (30).
RELEASE_STALE = "2026-08-01"


# --------------------------------------------------------------------------
# Module fixtures (guidance-layer §4.2, §4.4, §4.5)
# --------------------------------------------------------------------------

MODULE_IDS = [f"M{i:02d}" for i in range(1, 17)]

MODULE_TITLES = {
    "M01": "项目说明 / README",
    "M02": "许可证 / License",
    "M03": "忽略规则 / Ignore rules",
    "M04": "行为准则 / Code of Conduct",
    "M05": "贡献指南 / Contributing guide",
    "M06": "安全策略 / Security policy",
    "M07": "Issue 表单 / Issue forms",
    "M08": "合并请求模板 / Pull request template",
    "M09": "变更日志与发布说明 / Changelog & release notes",
    "M10": "变更日志自动化 / Changelog automation",
    "M11": "自动检查 / Continuous integration",
    "M12": "依赖自动更新 / Dependency updates",
    "M13": "编辑器格式配置 / EditorConfig",
    "M14": "提交前检查 / Pre-commit hooks",
    "M15": "代码负责人 / Code owners",
    "M16": "赞助入口 / Funding",
}

# guidance-layer §4.2: only the four registered level values may appear.
REQUIRED, RECOMMENDED, OPTIONAL, RECOMMEND_ONLY = ct.LEVEL_VALUES

DEFAULT_LEVELS = {}
for _mid in MODULE_IDS:
    _n = int(_mid[1:])
    if _n <= 3:
        DEFAULT_LEVELS[_mid] = REQUIRED
    elif _mid == "M10":
        DEFAULT_LEVELS[_mid] = RECOMMEND_ONLY
    elif _n <= 11:
        DEFAULT_LEVELS[_mid] = RECOMMENDED
    else:
        DEFAULT_LEVELS[_mid] = OPTIONAL

# Modules whose evidence is a platform feature: no star number at all.
PLATFORM_ONLY = {"M06", "M15"}

# data-model.md: rule "2" claims comparable adoption, so the rationale must
# say so.  Rule "1 + 2" does not claim it and must not be failed for it.
DEFAULT_RULES = {"M12": "2"}

COMPARABLE = "认可度相当"


def repo_slug(mid: str) -> str:
    return f"owner/repo{mid[1:]}"


def repo_stars(mid: str) -> int:
    return 10000 + int(mid[1:]) * 111


def repo_forks(mid: str) -> int:
    return 1000 + int(mid[1:]) * 11


def fmt(number: int) -> str:
    """guidance-layer §0: star and fork counts carry thousands separators."""
    return f"{number:,}"


def star_ref(mid: str) -> str:
    return f"★ {fmt(repo_stars(mid))} ({repo_slug(mid)})"


# guidance-layer §4.1: the excluded list needs at least 8 rows.
EXCLUDED = [
    (f"候选 {j:02d} / Candidate {j:02d}", f"owner/ex{j:02d}", 2000 + j * 7)
    for j in range(1, 9)
]

ALL_ROWS = [
    (repo_slug(mid), repo_stars(mid), repo_forks(mid)) for mid in MODULE_IDS
] + [(slug, stars, stars // 7) for _name, slug, stars in EXCLUDED]


def default_evidence(mid: str) -> str:
    if mid in PLATFORM_ONLY:
        return "平台官方功能 / Official platform feature：GitHub 内置功能"
    return f"精确 Star 数 / Exact stars：{star_ref(mid)}"


def default_adoption(mid: str) -> str:
    """The 认可度 column of the home summary table (guidance-layer §4.5)."""
    if mid in PLATFORM_ONLY:
        return "平台官方功能 / Official platform feature"
    return star_ref(mid)


def default_rationale_zh(mid: str) -> str:
    if DEFAULT_RULES.get(mid) == "2":
        return (
            f"{mid}：两个候选都是事实标准，{COMPARABLE}；"
            "选定来源由平台内置，不需要额外安装，起步更容易。"
        )
    return f"{mid}：社区认可度明显领先于其他候选，开箱即用。"


def default_rationale_en(mid: str) -> str:
    if DEFAULT_RULES.get(mid) == "2":
        return (
            "Both candidates are de facto standards with comparable adoption; "
            "the pick is built into the platform and needs no installation."
        )
    return "Clearly the most widely adopted candidate, and usable out of the box."


def default_alternatives(mid: str) -> list[str]:
    if mid == "M01":
        name, slug, stars = EXCLUDED[0]
        return [
            f"{name} — 精确 Star 数 / Exact stars：★ {fmt(stars)} ({slug}) — "
            "更新已经停滞（中文） / no longer maintained (English)"
        ]
    return [
        f"备选 {mid} / Alternative {mid} — 未取得 / Not available — "
        "需要额外依赖（中文） / needs an extra dependency (English)"
    ]


# --------------------------------------------------------------------------
# Fixture builder
# --------------------------------------------------------------------------


def module_section(mid: str, overrides: dict, verified: str) -> str:
    """One ``### Mxx`` section: field table plus rationale and alternatives."""
    fields = [
        ("文件 / Files", f"`file-{mid.lower()}.md`"),
        ("级别 / Level", overrides.get("level", DEFAULT_LEVELS[mid])),
        ("选定来源 / Pick", f"[Pick {mid}](https://example.com/{mid.lower()})"),
        ("版本或提交 / Version", f"{repo_slug(mid)}@0123abc"),
        ("上游许可证 / Upstream license", "MIT"),
        ("认可度证据 / Evidence", overrides.get("evidence", default_evidence(mid))),
        ("取舍规则 / Rule", overrides.get("rule", DEFAULT_RULES.get(mid, "1"))),
        ("核实日期 / Verified", overrides.get("verified", verified)),
    ]
    dropped = set(overrides.get("drop_fields", ()))
    rows = "\n".join(
        f"| {label} | {value} |" for label, value in fields if label not in dropped
    )

    rationale_zh = overrides.get("rationale_zh", default_rationale_zh(mid))
    rationale_en = overrides.get("rationale_en", default_rationale_en(mid))
    alternatives = overrides.get("alternatives", default_alternatives(mid))
    alt_block = "\n".join(f"- {item}" for item in alternatives)

    return (
        f"### {mid} {MODULE_TITLES[mid]}\n"
        "\n"
        "| 字段 / Field | 内容 / Value |\n"
        "|---|---|\n"
        f"{rows}\n"
        "\n"
        f"**入选理由**：{rationale_zh}\n"
        "\n"
        f"**Rationale**: {rationale_en}\n"
        "\n"
        "**备选方案 / Alternatives**\n"
        "\n"
        f"{alt_block}\n"
    )


def adoption_table(
    *, table_verified: str, last_commit: str, archived: set[str], short_row: bool
) -> str:
    """The machine-readable table between the two adoption markers (§4.3)."""
    lines = [
        ct.ADOPTION_START,
        "| Repo | Stars | Forks | Last commit | License | Archived | Verified |",
        "|---|---:|---:|---|---|---|---|",
    ]
    for index, (slug, stars, forks) in enumerate(ALL_ROWS):
        flag = "yes" if slug in archived else "no"
        if short_row and index == 0:
            # Six cells instead of seven.
            lines.append(
                f"| {slug} | {fmt(stars)} | {fmt(forks)} | {last_commit} | MIT | {flag} |"
            )
            continue
        lines.append(
            f"| {slug} | {fmt(stars)} | {fmt(forks)} | {last_commit} | MIT | "
            f"{flag} | {table_verified} |"
        )
    lines.append(ct.ADOPTION_END)
    return "\n".join(lines)


def excluded_section(*, rows: int, blank_cell: bool) -> str:
    lines = [
        "## 排除的候选 / Excluded candidates",
        "",
        "| 候选 / Candidate | 认可度 / Adoption | 排除理由 / Reason |",
        "|---|---|---|",
    ]
    for index, (name, slug, stars) in enumerate(EXCLUDED[:rows]):
        reason = "需要额外的在线服务 / depends on an extra hosted service"
        if blank_cell and index == 0:
            reason = ""
        lines.append(f"| {name} | ★ {fmt(stars)} ({slug}) | {reason} |")
    return "\n".join(lines)


def sources_md(
    *,
    data_verified: str | None,
    field_verified: str,
    table_verified: str,
    last_commit: str,
    modules: dict,
    archived: set[str],
    excluded_rows: int,
    excluded_blank: bool,
    include_excluded: bool,
    short_table_row: bool,
) -> str:
    head = ["# 选型清单 / Selection list", ""]
    if data_verified is not None:
        head += [f"数据核实日期 / Data verified: {data_verified}", ""]
    head += [
        "## 选型规则 / Selection rules",
        "",
        "三级规则：1 只看认可度；2 认可度相当时看起步难度；3 同样合格时看作者偏好。",
        "Three rules: 1 adoption alone; 2 ease of starting; 3 the author's preference.",
        "",
        "证据类型 / Evidence types：精确 Star 数 / Exact stars、四舍五入 Star 数 / "
        "Rounded stars、估算使用人数 / Estimated users、平台官方功能 / Official "
        "platform feature、事实标准 / De facto standard、未取得 / Not available。",
        "",
        "复核周期 / Review cadence：至少每 6 个月一次，每次发布前也要复核。",
        "",
        "## 模块 / Modules",
        "",
        "",
    ]

    sections = [
        module_section(mid, modules.get(mid, {}), field_verified)
        for mid in MODULE_IDS
        if not modules.get(mid, {}).get("omit")
    ]

    tail = [""]
    if include_excluded:
        tail += [excluded_section(rows=excluded_rows, blank_cell=excluded_blank), ""]
    tail += [
        "## 认可度数据 / Adoption data",
        "",
        adoption_table(
            table_verified=table_verified,
            last_commit=last_commit,
            archived=archived,
            short_row=short_table_row,
        ),
        "",
        "## 数据说明 / About the data",
        "",
        "数据取自 GitHub API，Star 数为精确值。维护说明见 `MAINTAINING.md`。",
        "Data comes from the GitHub API; star counts are exact. "
        "See `MAINTAINING.md` for the maintenance notes.",
        "",
    ]

    return "\n".join(head) + "\n".join(sections) + "\n".join(tail)


def home_readme(
    *,
    summary_verified: str,
    summary_order: list[str],
    summary_header: bool,
    link_to_sources: bool,
) -> str:
    lines = [
        ct.GUIDANCE_HOME_TITLE,
        "",
        "每个模块都选用社区公认的佼佼者。",
        "",
        "Every module uses a widely adopted community pick.",
        "",
        "## 主厨精选一览 / The picks at a glance",
        "",
        ct.SUMMARY_START,
    ]
    if summary_header:
        lines += [
            "| 模块 / Module | 选定来源 / Pick | 认可度 / Adoption | 核实日期 / Verified |",
            "|---|---|---|---|",
        ]
    for mid in summary_order:
        lines.append(
            f"| {mid} {MODULE_TITLES[mid]} | Pick {mid} | "
            f"{default_adoption(mid)} | {summary_verified} |"
        )
    lines.append(ct.SUMMARY_END)
    lines.append("")
    if link_to_sources:
        lines.append("[完整选型清单 / Full selection list](chefs-pick/SOURCES.md)")
    else:
        lines.append("完整清单尚未链接 / The full list is not linked yet.")
    lines.append("")
    return "\n".join(lines)


def upgrade_md(*, stars: int) -> str:
    return (
        "# 升级为团队项目 / Growing into a team project\n"
        "\n"
        "可选参考。 / An optional reference.\n"
        "\n"
        "## 常用增强项 / Common additions\n"
        "\n"
        "| 增强项 / Addition | 作用 / Purpose | 来源 / Source | 认可度 / Adoption |\n"
        "|---|---|---|---|\n"
        f"| Pick M01 | 参考 / Reference | https://github.com/{repo_slug('M01')} | "
        f"★ {fmt(stars)} ({repo_slug('M01')}) |\n"
    )


def build(
    *,
    data_verified: str | None = VERIFIED,
    field_verified: str | None = None,
    table_verified: str | None = None,
    summary_verified: str | None = None,
    verified: str = VERIFIED,
    last_commit: str = LAST_COMMIT,
    modules: dict | None = None,
    archived: set[str] | None = None,
    excluded_rows: int = 8,
    excluded_blank: bool = False,
    include_excluded: bool = True,
    short_table_row: bool = False,
    summary_order: list[str] | None = None,
    summary_header: bool = True,
    link_to_sources: bool = True,
    include_sources: bool = True,
    upgrade_stars: int | None = None,
) -> dict[str, str]:
    """A complete, contract-conforming pair of files, with one knob per case."""
    if data_verified == VERIFIED and verified != VERIFIED:
        data_verified = verified
    tree = {
        ".github/README.md": home_readme(
            summary_verified=summary_verified or verified,
            summary_order=MODULE_IDS if summary_order is None else summary_order,
            summary_header=summary_header,
            link_to_sources=link_to_sources,
        )
    }
    if include_sources:
        tree[f"{ct.GUIDANCE_DIR}/SOURCES.md"] = sources_md(
            data_verified=data_verified,
            field_verified=field_verified or verified,
            table_verified=table_verified or verified,
            last_commit=last_commit,
            modules=modules or {},
            archived=archived or set(),
            excluded_rows=excluded_rows,
            excluded_blank=excluded_blank,
            include_excluded=include_excluded,
            short_table_row=short_table_row,
        )
    if upgrade_stars is not None:
        tree[f"{ct.GUIDANCE_DIR}/UPGRADE-TO-TEAM.md"] = upgrade_md(stars=upgrade_stars)
    return tree


# --------------------------------------------------------------------------
# Base test case
# --------------------------------------------------------------------------


class CheckTestCase(unittest.TestCase):
    """Build a tree in a throwaway directory and run C12 against it."""

    def check(self, tree: dict[str, str], **ctx_kw):
        ctx_kw.setdefault("today", TODAY)
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(tmp, tree)
            return run_one("C12", make_ctx(tmp, **ctx_kw))

    def assertPass(self, tree: dict[str, str], **ctx_kw):
        status, problems = self.check(tree, **ctx_kw)
        self.assertEqual(status, "PASS", f"C12: {problems}")

    def assertFail(self, tree: dict[str, str], **ctx_kw):
        status, problems = self.check(tree, **ctx_kw)
        self.assertEqual(status, "FAIL", f"C12: {problems}")
        self.assertTrue(problems, "C12 failed without reporting a problem")
        return problems

    def assertSkip(self, tree: dict[str, str], **ctx_kw):
        status, reason = self.check(tree, **ctx_kw)
        self.assertEqual(status, "SKIP", f"C12: {reason}")
        return reason


# --------------------------------------------------------------------------
# Passing cases
# --------------------------------------------------------------------------


class TestC12Passes(CheckTestCase):
    def test_minimal_conforming_selection_list(self):
        """The baseline fixture satisfies every C12 clause."""
        self.assertPass(build())

    def test_release_mode_with_fresh_dates(self):
        """--release only tightens the window; fresh data still passes."""
        self.assertPass(build(), release=True)

    def test_old_last_commit_column_is_not_a_freshness_problem(self):
        """guidance-layer §4.3: ``Last commit`` records the upstream commit date.

        tooling.md C12 lists exactly four date fields under the freshness rule
        and ``Last commit`` is not one of them, so a 2019 commit date passes
        even under ``--release``.
        """
        tree = build(last_commit=OLD_LAST_COMMIT)
        self.assertPass(tree)
        self.assertPass(tree, release=True)

    def test_rule_one_plus_two_needs_no_comparable_adoption_wording(self):
        """data-model.md: ``1 + 2`` does not claim comparable adoption.

        Only a bare ``2`` must justify 认可度相当, so this must not be failed
        together with the bare-``2`` case.
        """
        tree = build(
            modules={
                "M04": {
                    "rule": "1 + 2",
                    "rationale_zh": (
                        "M04：第 1 级已经能决定，认可度明显领先；"
                        "第 2 级也指向同一选择，起步更容易。"
                    ),
                    "rationale_en": (
                        "Rule 1 already decides it, and rule 2 points the same way."
                    ),
                }
            }
        )
        self.assertNotIn(
            COMPARABLE,
            tree[f"{ct.GUIDANCE_DIR}/SOURCES.md"].split("### M04")[1].split("### M05")[0],
            "the M04 section must not contain the phrase for this test to mean anything",
        )
        self.assertPass(tree)

    def test_upgrade_page_star_numbers_may_repeat_the_table(self):
        self.assertPass(build(upgrade_stars=repo_stars("M01")))


# --------------------------------------------------------------------------
# Skips (tooling.md C12 preamble)
# --------------------------------------------------------------------------


class TestC12Skips(CheckTestCase):
    def test_skip_when_sources_md_is_missing(self):
        reason = self.assertSkip(build(include_sources=False))
        self.assertTrue(
            any("SOURCES" in text for text in reason),
            f"the skip reason must name the missing file: {reason}",
        )

    def test_skip_when_the_summary_table_has_no_data_rows_yet(self):
        """The half-finished US2 state: markers in place, header only."""
        self.assertSkip(build(summary_order=[]))

    def test_skip_when_the_summary_markers_are_still_empty(self):
        self.assertSkip(build(summary_order=[], summary_header=False))


# --------------------------------------------------------------------------
# Failing cases
# --------------------------------------------------------------------------


class TestC12Failures(CheckTestCase):
    # -- home page ---------------------------------------------------------

    def test_home_page_must_link_the_selection_list(self):
        self.assertFail(build(link_to_sources=False))

    # -- star numbers ------------------------------------------------------

    def test_star_number_disagrees_with_the_stars_column(self):
        self.assertFail(
            build(
                modules={
                    "M03": {
                        "evidence": (
                            "精确 Star 数 / Exact stars：★ 99,999 (owner/repo03)"
                        )
                    }
                }
            )
        )

    def test_star_reference_to_a_repository_missing_from_the_table(self):
        self.assertFail(
            build(
                modules={
                    "M03": {
                        "evidence": (
                            "精确 Star 数 / Exact stars：★ 10,333 (owner/not-listed)"
                        )
                    }
                }
            )
        )

    def test_star_number_in_the_upgrade_page_disagrees_with_the_table(self):
        self.assertFail(build(upgrade_stars=repo_stars("M01") + 5))

    # -- module field tables ----------------------------------------------

    def test_module_is_missing_one_of_the_eight_field_labels(self):
        for label in ct.FIELD_LABELS:
            with self.subTest(label=label):
                self.assertFail(build(modules={"M07": {"drop_fields": [label]}}))

    def test_module_section_is_missing_entirely(self):
        self.assertFail(build(modules={"M09": {"omit": True}}))

    def test_level_value_is_not_one_of_the_registered_four(self):
        self.assertFail(build(modules={"M05": {"level": "很棒 / Great"}}))

    def test_verified_cell_is_not_a_date(self):
        self.assertFail(build(modules={"M05": {"verified": "soon / 待定"}}))

    def test_evidence_cell_has_no_registered_evidence_type(self):
        self.assertFail(
            build(modules={"M03": {"evidence": "很多人用：★ 10,333 (owner/repo03)"}})
        )

    def test_rationale_paragraphs_and_alternatives_must_not_be_empty(self):
        self.assertFail(build(modules={"M08": {"rationale_zh": ""}}))
        self.assertFail(build(modules={"M08": {"rationale_en": ""}}))
        self.assertFail(build(modules={"M08": {"alternatives": []}}))

    # -- archived pick -----------------------------------------------------

    def test_first_starred_repository_of_a_module_is_archived(self):
        self.assertFail(build(archived={repo_slug("M01")}))

    # -- adoption table ----------------------------------------------------

    def test_adoption_table_row_does_not_have_seven_columns(self):
        self.assertFail(build(short_table_row=True))

    def test_data_verified_line_is_missing(self):
        self.assertFail(build(data_verified=None))

    # -- freshness ---------------------------------------------------------

    def test_dates_older_than_183_days_fail(self):
        """All four freshness-constrained fields, one at a time."""
        cases = {
            "数据核实日期 / Data verified": {"data_verified": STALE},
            "核实日期 / Verified cell": {"field_verified": STALE},
            "adoption table Verified column": {"table_verified": STALE},
            "summary table Verified column": {"summary_verified": STALE},
        }
        for name, kwargs in cases.items():
            with self.subTest(field=name):
                self.assertFail(build(**kwargs))

    def test_release_mode_rejects_dates_older_than_30_days(self):
        """Within 183 days, so only ``--release`` may reject it."""
        cases = {
            "数据核实日期 / Data verified": {"data_verified": RELEASE_STALE},
            "核实日期 / Verified cell": {"field_verified": RELEASE_STALE},
            "adoption table Verified column": {"table_verified": RELEASE_STALE},
            "summary table Verified column": {"summary_verified": RELEASE_STALE},
        }
        for name, kwargs in cases.items():
            with self.subTest(field=name):
                tree = build(**kwargs)
                self.assertPass(tree)
                self.assertFail(tree, release=True)

    def test_whole_fixture_48_days_old_passes_normally_and_fails_on_release(self):
        tree = build(verified=RELEASE_STALE)
        self.assertPass(tree)
        self.assertFail(tree, release=True)

    # -- home summary table ------------------------------------------------

    def test_summary_table_has_fewer_than_sixteen_rows(self):
        self.assertFail(build(summary_order=MODULE_IDS[:15]))

    def test_summary_table_rows_are_out_of_order(self):
        swapped = list(MODULE_IDS)
        swapped[3], swapped[4] = swapped[4], swapped[3]
        self.assertFail(build(summary_order=swapped))

    # -- excluded candidates ----------------------------------------------

    def test_excluded_candidates_section_is_missing(self):
        self.assertFail(build(include_excluded=False))

    def test_excluded_candidates_table_has_fewer_than_eight_rows(self):
        self.assertFail(build(excluded_rows=7))

    def test_excluded_candidates_row_has_an_empty_cell(self):
        self.assertFail(build(excluded_blank=True))

    # -- rule 2 ------------------------------------------------------------

    def test_rule_two_without_the_comparable_adoption_wording(self):
        """Constitution principle II: a bare ``2`` must justify 认可度相当."""
        tree = build(
            modules={
                "M12": {
                    "rule": "2",
                    "rationale_zh": "M12：选定来源由平台内置，不需要额外安装，起步更容易。",
                    "rationale_en": (
                        "The pick is built into the platform and needs no installation."
                    ),
                }
            }
        )
        self.assertNotIn(
            COMPARABLE,
            tree[f"{ct.GUIDANCE_DIR}/SOURCES.md"].split("### M12")[1].split("### M13")[0],
        )
        self.assertFail(tree)


if __name__ == "__main__":
    unittest.main()
