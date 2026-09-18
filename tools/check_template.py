#!/usr/bin/env python3
"""Structure and release-gate checks for the Chef's Pick OSS Starter template.

Runs C01-C22 against ``template/``.  See
``specs/001-chefs-pick-starter/contracts/tooling.md`` for the contract.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment error path
    print("Missing dependency: PyYAML", file=sys.stderr)
    print("python3 -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# --------------------------------------------------------------------------
# Constants (verbatim from the contracts)
# --------------------------------------------------------------------------

GUIDANCE_FILE = ".github/README.md"
GUIDANCE_DIR = ".github/chefs-pick"

# template-layout.md §2
REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    ".gitignore",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "CHANGELOG.md",
    ".github/release.yml",
    ".github/workflows/ci.yml",
    ".github/dependabot.yml",
    ".editorconfig",
    ".pre-commit-config.yaml",
    ".github/CODEOWNERS",
    ".github/FUNDING.yml",
    ".github/README.md",
    ".github/README.zh-CN.md",
    ".github/chefs-pick/SETUP.md",
    ".github/chefs-pick/SETUP.zh-CN.md",
    ".github/chefs-pick/GUIDE.md",
    ".github/chefs-pick/SOURCES.md",
    ".github/chefs-pick/MAINTAINING.md",
    ".github/chefs-pick/CHANGELOG.md",
    ".github/chefs-pick/LICENSE",
]

OPTIONAL_FILES = [
    ".github/chefs-pick/UPGRADE-TO-TEAM.md",
]

# template-layout.md §1
FORBIDDEN_DIR_NAMES = [
    ".specify",
    ".claude",
    "specs",
    "tools",
    ".git",
    "__pycache__",
    "node_modules",
]

# markers.md §2.2 -- first line of every project file (LICENSE has none).
SOURCE_COMMENTS = {
    "README.md": (
        "<!-- Source: Best-README-Template BLANK_README (Unlicense) — "
        "https://github.com/othneildrew/Best-README-Template -->"
    ),
    "CODE_OF_CONDUCT.md": (
        "<!-- Source: Contributor Covenant 2.1 (CC BY 4.0) — "
        "https://www.contributor-covenant.org/version/2/1/code_of_conduct/ -->"
    ),
    "CONTRIBUTING.md": (
        "<!-- Source: GitHub Open Source Guides (CC BY 4.0, structure only) — "
        "https://opensource.guide/starting-a-project/; GitHub Docs (official) — "
        "https://docs.github.com/en/communities/setting-up-your-project-for-healthy-"
        "contributions/setting-guidelines-for-repository-contributors -->"
    ),
    "SECURITY.md": (
        "<!-- Source: GitHub security policy and private vulnerability reporting "
        "(official) — https://docs.github.com/en/code-security/how-tos/report-and-fix-"
        "vulnerabilities/configure-vulnerability-reporting/add-security-policy -->"
    ),
    "CHANGELOG.md": (
        "<!-- Source: Keep a Changelog 1.1.0 (MIT) — "
        "https://keepachangelog.com/en/1.1.0/ -->"
    ),
    ".github/PULL_REQUEST_TEMPLATE.md": (
        "<!-- Source: GitHub pull request template (official) — "
        "https://docs.github.com/en/communities/using-templates-to-encourage-useful-"
        "issues-and-pull-requests/creating-a-pull-request-template-for-your-repository -->"
    ),
    ".gitignore": (
        "# Source: github/gitignore Global templates (CC0-1.0) — "
        "https://github.com/github/gitignore/tree/"
        "356fd7baab4c05e092194a41f64dbd5afc8817e4/Global"
    ),
    ".editorconfig": (
        "# Source: EditorConfig (official specification) — https://editorconfig.org"
    ),
    ".pre-commit-config.yaml": (
        "# Source: pre-commit and pre-commit-hooks (MIT) — https://pre-commit.com"
    ),
    ".github/CODEOWNERS": (
        "# Source: GitHub code owners (official) — "
        "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-"
        "features/customizing-your-repository/about-code-owners"
    ),
    ".github/FUNDING.yml": (
        "# Source: GitHub sponsor button (official) — "
        "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-"
        "features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository"
    ),
    ".github/ISSUE_TEMPLATE/bug_report.yml": (
        "# Source: GitHub issue forms (official) — "
        "https://docs.github.com/en/communities/using-templates-to-encourage-useful-"
        "issues-and-pull-requests/syntax-for-issue-forms"
    ),
    ".github/ISSUE_TEMPLATE/feature_request.yml": (
        "# Source: GitHub issue forms (official) — "
        "https://docs.github.com/en/communities/using-templates-to-encourage-useful-"
        "issues-and-pull-requests/syntax-for-issue-forms"
    ),
    ".github/ISSUE_TEMPLATE/config.yml": (
        "# Source: GitHub issue template chooser (official) — "
        "https://docs.github.com/en/communities/using-templates-to-encourage-useful-"
        "issues-and-pull-requests/configuring-issue-templates-for-your-repository"
    ),
    ".github/dependabot.yml": (
        "# Source: GitHub Dependabot (official) — "
        "https://docs.github.com/en/code-security/dependabot/working-with-dependabot/"
        "dependabot-options-reference"
    ),
    ".github/release.yml": (
        "# Source: GitHub automatically generated release notes (official) — "
        "https://docs.github.com/en/repositories/releasing-projects-on-github/"
        "automatically-generated-release-notes"
    ),
    ".github/workflows/ci.yml": (
        '# Source: GitHub starter workflow "Simple workflow" (MIT) — '
        "https://github.com/actions/starter-workflows/blob/main/ci/blank.yml"
    ),
}

# markers.md §1.3
LEGACY_MARKERS = [
    "github_username",
    "repo_name",
    "project_title",
    "project_description",
    "project_license",
    "twitter_handle",
    "linkedin_username",
    "email_client",
    "[INSERT CONTACT METHOD]",
    "[year]",
    "[fullname]",
    "TODO",
    "FIXME",
    "$default-branch",
]

# template-layout.md §6 -- module -> (files, referencing project files)
REMOVAL_REFS = {
    "M04": (["CODE_OF_CONDUCT.md"], ["README.md", "CONTRIBUTING.md"]),
    "M05": (["CONTRIBUTING.md"], ["README.md"]),
    "M06": (["SECURITY.md"], ["README.md", "CONTRIBUTING.md"]),
    "M07": (
        [
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/feature_request.yml",
            ".github/ISSUE_TEMPLATE/config.yml",
        ],
        ["README.md"],
    ),
    "M08": ([".github/PULL_REQUEST_TEMPLATE.md"], []),
    "M09": (["CHANGELOG.md", ".github/release.yml"], ["CONTRIBUTING.md", ".github/PULL_REQUEST_TEMPLATE.md"]),
    "M11": ([".github/workflows/ci.yml"], ["README.md"]),
    "M12": ([".github/dependabot.yml"], []),
    "M13": ([".editorconfig"], []),
    "M14": ([".pre-commit-config.yaml"], []),
    "M15": ([".github/CODEOWNERS"], []),
    "M16": ([".github/FUNDING.yml"], []),
}

# guidance-layer.md §4.2 (tooling-delta.md §2)
FIELD_LABELS = [
    "Files",
    "Level",
    "Pick",
    "Version",
    "Upstream license",
    "Evidence",
    "Rule",
    "Verified",
]

LEVEL_VALUES = [
    "Required",
    "Recommended",
    "Optional",
    "Optional (recommendation only)",
]

# guidance-layer.md §2 (tooling-delta.md §2)
PLACEHOLDER_TABLE_HEADER = "| Placeholder | Meaning | Files | Example |"

# guidance-layer.md §1 §3 §5 §6 (tooling-delta.md §2)
GUIDANCE_HOME_TITLE = "# Chef's Pick OSS Starter"
GUIDE_EXTRA_HEADINGS = [
    "Adding language-specific rules",
    "Pinning actions",
    "Account-level default files",
    "Chinese translations",
    "Tracing the template version",
    "Changing the license",
]
# guidance-layer.md §5 -- English half of MAINTAINING.md's six headings.
MAINTAINING_HEADINGS = [
    "Review cadence",
    "How to review",
    "Re-evaluation triggers",
    "Action updates",
    "Recording changes",
    "Release gates",
]
# guidance-layer.md §6 -- English half of UPGRADE-TO-TEAM.md's three headings.
UPGRADE_HEADINGS = [
    "Common additions",
    "When you need foundation-level governance",
    "No longer recommended",
]

# Regular expressions
PLACEHOLDER_RE = re.compile(r"CHANGEME_[A-Z0-9_]+")
# Detects template-author identity leaking into a generated repository. This
# is independent of document language -- "主厨精选" can still appear inside
# the Chinese translations -- so it is kept as-is (tooling-delta.md §2).
IDENTITY_RE = re.compile(r"(?i)chef'?s[ -]?pick|主厨精选")
STAR_RE = re.compile(r"★ ([\d,]+) \(([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\)")
CJK_RE = re.compile(r"[一-鿿]")
LATIN_RE = re.compile(r"[A-Za-z]")
VERSION_HEADING_RE = re.compile(r"^#{1,6} \[(Unreleased|[0-9]+\.[0-9]+\.[0-9]+)\]")

CLEANUP_COMMAND = "git rm -r .github/README.md .github/README.zh-CN.md .github/chefs-pick"

ADOPTION_START = "<!-- adoption-data:start -->"
ADOPTION_END = "<!-- adoption-data:end -->"
SUMMARY_START = "<!-- summary:start -->"
SUMMARY_END = "<!-- summary:end -->"

FRESH_DAYS = 183
RELEASE_FRESH_DAYS = 30

# tooling-delta.md §2 -- language-structure.md-derived constants for
# discovering and validating translations of the bootstrap-guidance layer.
TRANSLATED_DOCS = {".github/README.md", ".github/chefs-pick/SETUP.md"}
SELECTOR_LINES = {  # path -> verbatim language-selector line, language-structure.md §1
    ".github/README.md": "**English** · [简体中文](README.zh-CN.md)",
    ".github/README.zh-CN.md": "[English](README.md) · **简体中文**",
    ".github/chefs-pick/SETUP.md": "**English** · [简体中文](SETUP.zh-CN.md)",
    ".github/chefs-pick/SETUP.zh-CN.md": "[English](SETUP.md) · **简体中文**",
}
ANCHOR_RE = re.compile(r"^<!-- anchor: ([a-z0-9][a-z0-9-]*) -->$")
DIGEST_RE = re.compile(r"^<!-- translation-of: (\S+) sha256:([0-9a-f]{16}) -->$")
ANCHOR_SEQUENCES = {  # language-structure.md §3
    "README": ["chefs-pick-oss-starter", "what-you-get", "required", "recommended",
               "optional", "the-picks-at-a-glance", "how-we-pick", "quick-start",
               "good-to-know", "clean-up-when-done", "feedback-and-contact", "license"],
    "SETUP": ["setup-checklist", "placeholders", "steps"],
}
SINGLE_SOURCE_MARKERS = ["| Placeholder | Meaning | Files | Example |",
                         "<!-- summary:start -->", "<!-- adoption-data:start -->"]

# tooling-delta-003.md §1 -- workspace-structure.md §1, §2-derived constants
# for the workspace homepage (README.md), which lives outside template/.
WORKSPACE_SOURCE = "README.md"
WORKSPACE_TRANSLATION = "README.zh-CN.md"
WORKSPACE_SELECTOR_LINES = {
    "README.md": "**English** · [简体中文](README.zh-CN.md)",
    "README.zh-CN.md": "[English](README.md) · **简体中文**",
}
WORKSPACE_ANCHOR_SEQUENCE = [
    "chefs-pick-oss-starter-workspace", "layout",
    "common-commands", "publishing", "license",
]

# Translation filenames: "<id>.<lang>.md" with a sibling "<id>.md" in the
# same directory (tooling-delta.md §1.3, research.md R12). The language
# list is deliberately not hard-coded.
TRANSLATION_FILENAME_RE = re.compile(
    r"^(?P<id>[A-Za-z-]+)\.(?P<lang>[a-z]{2}(-[A-Z]{2})?)\.md$"
)


# --------------------------------------------------------------------------
# Framework
# --------------------------------------------------------------------------


class SkipCheck(Exception):
    """Raised by a check function when it has nothing to check."""


class WarnCheck(Exception):
    """Raised by a check function to report non-blocking problems.

    ``args[0]`` is the list of problems, exactly like a normal FAIL return.
    See tooling-delta.md §1.1: WARN never affects the exit code unless
    ``--release`` is set, in which case it is counted as FAIL.
    """


@dataclass
class Context:
    template_dir: Path
    release: bool = False
    today: _dt.date = _dt.date.today()
    files: set[str] | None = None


def is_guidance(rel_path: str) -> bool:
    if rel_path == GUIDANCE_FILE or rel_path.startswith(GUIDANCE_DIR + "/"):
        return True
    # A translation of the home page lives directly beside it, outside
    # GUIDANCE_DIR (for example ".github/README.zh-CN.md" next to
    # ".github/README.md") -- tooling-delta.md §1.3, research.md R12. The
    # language tag is deliberately not hard-coded.
    home_dir, _, home_name = GUIDANCE_FILE.rpartition("/")
    path_dir, _, path_name = rel_path.rpartition("/")
    if path_dir == home_dir:
        match = TRANSLATION_FILENAME_RE.match(path_name)
        if match and f"{match.group('id')}.md" == home_name:
            return True
    return False


def iter_files(root: Path) -> list[str]:
    """All files under *root* as sorted POSIX relative paths, minus .DS_Store."""
    out = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.name == ".DS_Store":
            continue
        out.append(path.relative_to(root).as_posix())
    return sorted(out)


def project_files(ctx: Context) -> list[str]:
    return [p for p in iter_files(ctx.template_dir) if not is_guidance(p)]


def find_translations(root: Path) -> dict[str, str]:
    """Discover translations inside the bootstrap-guidance layer.

    Returns ``{translation_rel_path: source_rel_path}``. A file is a
    translation of ``<id>.md`` whenever its name matches
    ``TRANSLATION_FILENAME_RE`` (tooling-delta.md §1.3, research.md R12);
    the paired ``<id>.md`` source is *not* required to already exist for
    the file to be registered here. Whether the declared source actually
    exists is a correctness question for callers to judge -- notably
    C24, which must FAIL (tooling-delta.md §5) rather than silently lose
    track of a translation whose source is missing. The language list is
    not hard-coded: any two-letter (optionally regionalised) language tag
    is accepted.
    """
    translations: dict[str, str] = {}
    for rel in iter_files(root):
        if not is_guidance(rel):
            continue
        match = TRANSLATION_FILENAME_RE.match(Path(rel).name)
        if not match:
            continue
        source_rel = str(Path(rel).with_name(f"{match.group('id')}.md").as_posix())
        translations[rel] = source_rel
    return translations


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path):
    return yaml.safe_load(read_text(path))


def selected(ctx: Context, rel_path: str) -> bool:
    return ctx.files is None or rel_path in ctx.files


def parse_placeholder_registry(text: str) -> dict[str, set[str]]:
    """Parse SETUP.md's placeholder table into {placeholder: {file, ...}}."""
    registry: dict[str, set[str]] = {}
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == PLACEHOLDER_TABLE_HEADER:
            in_table = True
            continue
        if not in_table:
            continue
        if not stripped.startswith("|"):
            break
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 3:
            break
        if set(cells[0]) <= set("-: "):
            continue
        names = re.findall(r"`([^`]+)`", cells[0])
        if not names or not PLACEHOLDER_RE.fullmatch(names[0]):
            break
        registry[names[0]] = set(re.findall(r"`([^`]+)`", cells[2]))
    return registry


def parse_date(value: str) -> _dt.date | None:
    try:
        return _dt.date.fromisoformat(value.strip())
    except ValueError:
        return None


# --------------------------------------------------------------------------
# Language-purity helpers (tooling-delta.md §1.3/§3, research.md R6)
# --------------------------------------------------------------------------

_FENCE_TOGGLE_RE = re.compile(r"^\s*(```|~~~)")
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]*`")
_MD_LINK_TARGET_RE = re.compile(r"(\[[^\]]*\])\([^)]*\)")
_BARE_URL_RE = re.compile(r"https?://\S+")
_ENGLISH_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*")
# The allowed separator between two words in the same "run": the ASCII
# punctuation/space/tab set from research.md R6, plus single newlines (a
# blank line -- two or more newlines -- still breaks the run).
_ALLOWED_RUN_SEP_RE = re.compile(r"^[ \t\n,.;:!?()'\"-]*$")
_PARAGRAPH_BREAK_RE = re.compile(r"\n[ \t]*\n")


def _strip_fenced_code(text: str) -> str:
    """Delete fenced code blocks, including the fence lines themselves.

    Recognises both ``` and ``~~~`` fences, consistent with
    ``_anchor_lines``. A fence opened with one character is only closed by
    that same character -- a stray fence of the other kind nested inside
    does not toggle it back out.
    """
    out = []
    in_fence = False
    fence_char = None
    for line in text.split("\n"):
        match = _FENCE_TOGGLE_RE.match(line)
        if match:
            this_char = match.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_char = this_char
                continue
            if this_char == fence_char:
                in_fence = False
                fence_char = None
                continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def strip_for_purity(text: str, selector_line: str | None) -> str:
    """Strip everything research.md R6 excludes from the purity judgement.

    In order: fenced code blocks (fence lines included), HTML comments,
    inline code, the ``(target)`` half of Markdown links, bare URLs, and
    finally the language-selector line itself. The selector line is
    matched after the same link-target stripping has been applied to it,
    since by the time step 6 runs, step 4 has already rewritten that line
    in *text* the same way -- an exact match against the untouched
    ``selector_line`` string would otherwise never hit.
    """
    text = _strip_fenced_code(text)
    text = _HTML_COMMENT_RE.sub("", text)
    text = _INLINE_CODE_RE.sub("", text)
    text = _MD_LINK_TARGET_RE.sub(r"\1", text)
    text = _BARE_URL_RE.sub("", text)
    if selector_line is not None:
        stripped_selector = _MD_LINK_TARGET_RE.sub(r"\1", selector_line)
        text = "\n".join(
            line for line in text.split("\n") if line != stripped_selector
        )
    return text


def cjk_count(text: str) -> int:
    """Count of CJK Unified Ideographs (U+4E00-U+9FFF) in *text*."""
    return len(CJK_RE.findall(text))


def longest_english_run(text: str) -> int:
    """Longest run of consecutive English words in *text* (research.md R6).

    A word is ``[A-Za-z][A-Za-z'’-]*``. Two words are part of the same
    run when only characters from ``[ \\t,.;:!?()'"-]`` (repeatable) or a
    single newline separate them; a blank line or any other character
    (including CJK text or full-width punctuation) breaks the run.
    """
    words = list(_ENGLISH_WORD_RE.finditer(text))
    if not words:
        return 0
    longest = current = 1
    for prev, nxt in zip(words, words[1:]):
        between = text[prev.end():nxt.start()]
        continues = (
            _ALLOWED_RUN_SEP_RE.match(between) is not None
            and _PARAGRAPH_BREAK_RE.search(between) is None
        )
        current = current + 1 if continues else 1
        longest = max(longest, current)
    return longest


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------


def _todo(ctx: Context) -> list[str]:
    raise SkipCheck("not implemented")


def check_c01(ctx: Context) -> list[str]:
    """Every REQUIRED_FILES entry exists; nothing beyond REQUIRED + OPTIONAL."""
    problems = []
    present = set(iter_files(ctx.template_dir))
    for rel in REQUIRED_FILES:
        if rel not in present:
            problems.append(f"missing required file: {rel}")
    allowed = set(REQUIRED_FILES) | set(OPTIONAL_FILES)
    for rel in sorted(present - allowed):
        problems.append(f"unexpected file: {rel}")
    return problems


def check_c02(ctx: Context) -> list[str]:
    """No development directories or compiled Python files."""
    problems = []
    for path in sorted(ctx.template_dir.rglob("*")):
        rel = path.relative_to(ctx.template_dir).as_posix()
        if path.name == ".DS_Store":
            continue
        parts = rel.split("/")
        for name in FORBIDDEN_DIR_NAMES:
            if name in parts:
                problems.append(f"development path: {rel} (contains {name})")
                break
        else:
            if path.is_file() and rel.endswith(".pyc"):
                problems.append(f"compiled Python file: {rel}")
    return problems


def check_c03(ctx: Context) -> list[str]:
    """Every *.yml / *.yaml file parses with yaml.safe_load."""
    problems = []
    checked = 0
    for rel in iter_files(ctx.template_dir):
        if not rel.endswith((".yml", ".yaml")):
            continue
        if not selected(ctx, rel):
            continue
        checked += 1
        try:
            load_yaml(ctx.template_dir / rel)
        except yaml.YAMLError as exc:
            problems.append(f"{rel}: not valid YAML: {exc}")
        except UnicodeDecodeError as exc:
            problems.append(f"{rel}: not valid UTF-8: {exc}")
    if checked == 0:
        raise SkipCheck("no YAML files present")
    return problems


def _required_ids(form) -> set[str]:
    out = set()
    for item in (form or {}).get("body") or []:
        if not isinstance(item, dict):
            continue
        if ((item.get("validations") or {}).get("required")) is True:
            if item.get("id"):
                out.add(item["id"])
    return out


def check_c04(ctx: Context) -> list[str]:
    """The issue forms match project-files.md M07."""
    base = ".github/ISSUE_TEMPLATE"
    paths = {
        name: ctx.template_dir / f"{base}/{name}.yml"
        for name in ("bug_report", "feature_request", "config")
    }
    if not any(p.is_file() for p in paths.values()):
        raise SkipCheck(f"missing {base}/bug_report.yml and its siblings")

    problems = []
    forms = {}
    for name, path in paths.items():
        if not path.is_file():
            continue
        try:
            forms[name] = load_yaml(path)
        except yaml.YAMLError as exc:
            problems.append(f"{base}/{name}.yml: not valid YAML: {exc}")

    for name in ("bug_report", "feature_request"):
        form = forms.get(name)
        if form is None:
            continue
        rel = f"{base}/{name}.yml"
        if not isinstance(form, dict):
            problems.append(f"{rel}: top level is not a mapping")
            continue
        for key in ("name", "description", "labels", "body"):
            if not form.get(key):
                problems.append(f"{rel}: {key} must not be empty")

    if "bug_report" in forms:
        required = _required_ids(forms["bug_report"])
        for field in ("what-happened", "steps", "expected", "environment"):
            if field not in required:
                problems.append(f"{base}/bug_report.yml: {field} must be required")

    if "feature_request" in forms:
        required = _required_ids(forms["feature_request"])
        for field in ("problem", "solution"):
            if field not in required:
                problems.append(f"{base}/feature_request.yml: {field} must be required")

    config = forms.get("config")
    if config is not None:
        rel = f"{base}/config.yml"
        if not isinstance(config, dict):
            problems.append(f"{rel}: top level is not a mapping")
        else:
            if config.get("blank_issues_enabled") is not False:
                problems.append(f"{rel}: blank_issues_enabled must be false")
            links = config.get("contact_links") or []
            if len(links) < 2:
                problems.append(f"{rel}: expected at least two contact_links")
            prefix = "https://github.com/anyingiit/chefs-pick-oss-starter-workspace/"
            for link in links:
                url = (link or {}).get("url", "") if isinstance(link, dict) else ""
                if not url.startswith(prefix):
                    problems.append(f"{rel}: contact link url must start with {prefix}: {url}")
    return problems


RELEASE_CATEGORIES = [
    {"title": "New Features", "labels": ["enhancement"]},
    {"title": "Bug Fixes", "labels": ["bug"]},
    {"title": "Other Changes", "labels": ["*"]},
]


def check_c07(ctx: Context) -> list[str]:
    """release.yml's three categories match M09 exactly, in order."""
    rel = ".github/release.yml"
    path = ctx.template_dir / rel
    if not path.is_file():
        raise SkipCheck(f"missing {rel}")
    try:
        data = load_yaml(path)
    except yaml.YAMLError as exc:
        return [f"{rel}: not valid YAML: {exc}"]
    categories = ((data or {}).get("changelog") or {}).get("categories")
    if categories != RELEASE_CATEGORIES:
        return [
            f"{rel}: changelog.categories must match M09 exactly (title, labels and order)\n"
            f"    expected: {RELEASE_CATEGORIES}\n"
            f"    found:    {categories}"
        ]
    return []


def check_c16(ctx: Context) -> list[str]:
    """CODE_OF_CONDUCT.md satisfies the five conditions under M04."""
    rel = "CODE_OF_CONDUCT.md"
    path = ctx.template_dir / rel
    if not path.is_file():
        raise SkipCheck(f"missing {rel}")
    text = read_text(path)
    problems = []
    for needed in ("version 2.1", "leoycwan@gmail.com", "## Attribution"):
        if needed not in text:
            problems.append(f"{rel}: missing required text: {needed}")
    if "[INSERT CONTACT METHOD]" in text:
        problems.append(f"{rel}: upstream placeholder not replaced: [INSERT CONTACT METHOD]")
    if any(line.startswith("+++") for line in text.splitlines()):
        problems.append(f"{rel}: TOML front matter (+++) was not removed")
    return problems


def _ordered_headings(text: str, wanted: list[str], rel: str) -> list[str]:
    """Report any of *wanted* that is missing or out of order."""
    problems = []
    position = -1
    for heading in wanted:
        index = text.find(heading + "\n")
        if index < 0:
            problems.append(f"{rel}: missing heading: {heading}")
        elif index < position:
            problems.append(f"{rel}: heading out of order: {heading}")
        else:
            position = index
    return problems


def check_c20(ctx: Context) -> list[str]:
    """SECURITY, CONTRIBUTING, the PR template and README serve contributors."""
    root = ctx.template_dir
    targets = [
        "SECURITY.md",
        "CONTRIBUTING.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        "README.md",
    ]
    if not any((root / rel).is_file() for rel in targets):
        raise SkipCheck("no contributor document present (for example CONTRIBUTING.md)")

    problems = []

    security = root / "SECURITY.md"
    if security.is_file():
        text = read_text(security)
        for needed in (
            "## Supported Versions",
            "## Reporting a Vulnerability",
            "**Please do not report security vulnerabilities through public issues, "
            "discussions, or pull requests.**",
            "security/advisories/new",
            "leoycwan@gmail.com",
        ):
            if needed not in text:
                problems.append(f"SECURITY.md: missing required text: {needed}")

    contributing = root / "CONTRIBUTING.md"
    if contributing.is_file():
        text = read_text(contributing)
        problems.extend(
            _ordered_headings(
                text,
                [
                    "# Contributing",
                    "## Code of Conduct",
                    "## Ways to contribute",
                    "## Reporting bugs",
                    "## Suggesting features",
                    "## Reporting security issues",
                    "## Submitting pull requests",
                    "## Development setup",
                    "## Questions",
                ],
                "CONTRIBUTING.md",
            )
        )
        for needed in (
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "CHANGELOG.md",
            "README.md#getting-started",
        ):
            if needed not in text:
                problems.append(f"CONTRIBUTING.md: missing link to {needed}")
        if "CHANGEME_" in text:
            problems.append("CONTRIBUTING.md: must not contain any placeholder")

    pr_template = root / ".github/PULL_REQUEST_TEMPLATE.md"
    if pr_template.is_file():
        text = read_text(pr_template)
        problems.extend(
            _ordered_headings(
                text,
                ["## Description", "## Related issue", "## Checklist"],
                ".github/PULL_REQUEST_TEMPLATE.md",
            )
        )
        if "Closes #" not in text:
            problems.append(".github/PULL_REQUEST_TEMPLATE.md: missing 'Closes #'")
        count = len([line for line in text.splitlines() if line.startswith("- [ ] ")])
        if count != 3:
            problems.append(
                f".github/PULL_REQUEST_TEMPLATE.md: expected exactly 3 checklist items, found {count}"
            )

    readme = root / "README.md"
    if readme.is_file():
        text = read_text(readme)
        for needed in (
            "issues/new?template=bug_report.yml",
            "issues/new?template=feature_request.yml",
        ):
            if needed not in text:
                problems.append(f"README.md: missing required link: {needed}")

    return problems


def _workflow_triggers(data) -> dict:
    """PyYAML reads the ``on:`` key as the boolean ``True``; accept both."""
    if not isinstance(data, dict):
        return {}
    for key in (True, "on"):
        if key in data:
            value = data[key]
            if isinstance(value, dict):
                return value
            if isinstance(value, list):
                return {item: None for item in value}
            if isinstance(value, str):
                return {value: None}
    return {}


def _iter_uses(node):
    """Yield every ``uses:`` value anywhere in the parsed workflow."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "uses" and isinstance(value, str):
                yield value
            else:
                yield from _iter_uses(value)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_uses(item)


def check_c05(ctx: Context) -> list[str]:
    """The CI workflow matches project-files.md M11."""
    rel = ".github/workflows/ci.yml"
    path = ctx.template_dir / rel
    if not path.is_file():
        raise SkipCheck(f"missing {rel}")
    if not selected(ctx, rel):
        raise SkipCheck(f"{rel} not selected by --files")

    problems = []
    text = read_text(path)
    try:
        data = load_yaml(path)
    except yaml.YAMLError as exc:
        return [f"{rel}: not valid YAML: {exc}"]
    if not isinstance(data, dict):
        return [f"{rel}: top level is not a mapping"]

    triggers = _workflow_triggers(data)
    for name in ("push", "pull_request", "workflow_dispatch"):
        if name not in triggers:
            problems.append(f"{rel}: missing trigger: {name}")

    if data.get("permissions") != {"contents": "read"}:
        problems.append(
            f"{rel}: top-level permissions must be exactly "
            f"{{contents: read}}, got {data.get('permissions')!r}"
        )

    jobs = data.get("jobs")
    if not isinstance(jobs, dict):
        problems.append(f"{rel}: no jobs mapping")
        jobs = {}
    for name in ("lint", "test"):
        if name not in jobs:
            problems.append(f"{rel}: missing job: {name}")

    pin_re = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
    comment_re = re.compile(r"#\s*v?[0-9]")
    for value in _iter_uses(data):
        if not pin_re.match(value):
            problems.append(
                f"{rel}: action not pinned to a full 40-character commit SHA: {value}"
            )
            continue
        pinned_line = None
        for line in text.splitlines():
            if value in line and "uses:" in line:
                pinned_line = line
                break
        if pinned_line is None:
            problems.append(f"{rel}: cannot locate the source line for: {value}")
        elif not comment_re.search(pinned_line.split(value, 1)[1]):
            problems.append(f"{rel}: pinned action has no version comment: {value}")

    for job_name, job in jobs.items() if isinstance(jobs, dict) else []:
        if not isinstance(job, dict):
            continue
        for index, step in enumerate(job.get("steps") or []):
            if not isinstance(step, dict):
                continue
            uses = step.get("uses")
            if not isinstance(uses, str) or not uses.startswith("actions/checkout@"):
                continue
            with_block = step.get("with")
            if not isinstance(with_block, dict) or (
                with_block.get("persist-credentials") is not False
            ):
                problems.append(
                    f"{rel}: jobs.{job_name}.steps[{index}] uses actions/checkout "
                    "without `with: persist-credentials: false`"
                )

    return problems


def check_c06(ctx: Context) -> list[str]:
    """Dependabot keeps the GitHub Actions ecosystem up to date."""
    rel = ".github/dependabot.yml"
    path = ctx.template_dir / rel
    if not path.is_file():
        raise SkipCheck(f"missing {rel}")
    if not selected(ctx, rel):
        raise SkipCheck(f"{rel} not selected by --files")

    problems = []
    try:
        data = load_yaml(path)
    except yaml.YAMLError as exc:
        return [f"{rel}: not valid YAML: {exc}"]
    if not isinstance(data, dict):
        return [f"{rel}: top level is not a mapping"]

    if data.get("version") != 2:
        problems.append(f"{rel}: version must be 2, got {data.get('version')!r}")

    updates = data.get("updates")
    if not isinstance(updates, list):
        problems.append(f"{rel}: updates must be a list")
        return problems

    for entry in updates:
        if not isinstance(entry, dict):
            continue
        if entry.get("package-ecosystem") != "github-actions":
            continue
        if entry.get("directory") != "/":
            continue
        interval = (entry.get("schedule") or {}).get("interval")
        if interval:
            break
    else:
        problems.append(
            f'{rel}: no update entry with package-ecosystem "github-actions", '
            'directory "/" and a non-empty schedule.interval'
        )

    return problems





def check_c08(ctx: Context) -> list[str]:
    """Placeholders match SETUP.md's registry; no legacy markers survive."""
    setup_rel = f"{GUIDANCE_DIR}/SETUP.md"
    setup_path = ctx.template_dir / setup_rel
    if not setup_path.is_file():
        raise SkipCheck(f"missing {setup_rel}")

    registry = parse_placeholder_registry(read_text(setup_path))
    problems = []

    # Where each placeholder actually shows up, across all project files.
    actual: dict[str, set[str]] = {}
    for rel in project_files(ctx):
        text = read_text(ctx.template_dir / rel)
        for name in PLACEHOLDER_RE.findall(text):
            actual.setdefault(name, set()).add(rel)
        if selected(ctx, rel):
            for marker in LEGACY_MARKERS:
                if marker in text:
                    problems.append(f"{rel}: forbidden leftover marker: {marker}")

    for name in sorted(actual):
        if name not in registry:
            problems.append(
                f"unregistered placeholder {name} in: {', '.join(sorted(actual[name]))}"
            )

    # Only compare the file sets during a full run: with --files the tree is
    # deliberately only partly in scope.
    if ctx.files is None:
        present = set(iter_files(ctx.template_dir))
        for name, registered in sorted(registry.items()):
            expected = {rel for rel in registered if rel in present}
            found = actual.get(name, set())
            if expected != found:
                problems.append(
                    f"{name}: registered in {sorted(expected)} but found in {sorted(found)}"
                )

    # Inside the guidance layer only SETUP.md may mention CHANGEME_.
    for rel in iter_files(ctx.template_dir):
        if not is_guidance(rel) or rel == setup_rel:
            continue
        if not selected(ctx, rel):
            continue
        if "CHANGEME_" in read_text(ctx.template_dir / rel):
            problems.append(f"{rel}: guidance file must not contain CHANGEME_")

    return problems


def check_c09(ctx: Context) -> list[str]:
    """Every project file starts with its registered source comment."""
    problems = []
    checked = 0

    for rel, expected in SOURCE_COMMENTS.items():
        path = ctx.template_dir / rel
        if not path.is_file() or not selected(ctx, rel):
            continue
        checked += 1
        first = read_text(path).splitlines()[:1]
        first_line = first[0] if first else ""
        if first_line != expected:
            problems.append(
                f"{rel}: first line does not match the registered source comment\n"
                f"    expected: {expected}\n"
                f"    found:    {first_line}"
            )

    license_path = ctx.template_dir / "LICENSE"
    if license_path.is_file() and selected(ctx, "LICENSE"):
        checked += 1
        first = read_text(license_path).splitlines()[:1]
        first_line = first[0] if first else ""
        if first_line != "MIT License":
            problems.append(
                f"LICENSE: first line must be 'MIT License', found: {first_line}"
            )

    if checked == 0:
        raise SkipCheck("no file with a registered source comment is present")
    return problems


def check_c10(ctx: Context) -> list[str]:
    """No template identity, Chinese text, or template history in project files."""
    problems = []
    checked = 0

    for rel in project_files(ctx):
        if not selected(ctx, rel):
            continue
        checked += 1
        text = read_text(ctx.template_dir / rel)
        for match in IDENTITY_RE.finditer(text):
            problems.append(f"{rel}: template identity in a project file: {match.group(0)}")
            break
        if CJK_RE.search(text):
            problems.append(f"{rel}: project files must be written in English (Chinese found)")

    changelog = ctx.template_dir / "CHANGELOG.md"
    if changelog.is_file() and selected(ctx, "CHANGELOG.md"):
        headings = [
            line for line in read_text(changelog).splitlines() if line.startswith("## ")
        ]
        if headings != ["## [Unreleased]"]:
            problems.append(
                "CHANGELOG.md: expected exactly one '## [Unreleased]' heading, "
                f"found {headings}"
            )

    codeowners = ctx.template_dir / ".github/CODEOWNERS"
    if codeowners.is_file() and selected(ctx, ".github/CODEOWNERS"):
        for number, line in enumerate(read_text(codeowners).splitlines(), start=1):
            if line.strip() and not line.lstrip().startswith("#"):
                problems.append(f".github/CODEOWNERS:{number}: effective rule: {line}")

    funding = ctx.template_dir / ".github/FUNDING.yml"
    if funding.is_file() and selected(ctx, ".github/FUNDING.yml"):
        try:
            data = load_yaml(funding)
        except yaml.YAMLError as exc:
            problems.append(f".github/FUNDING.yml: not valid YAML: {exc}")
        else:
            if not isinstance(data, dict):
                problems.append(".github/FUNDING.yml: expected a mapping")
            else:
                for key, value in data.items():
                    if value is not None:
                        problems.append(
                            f".github/FUNDING.yml: {key} must be empty, got {value!r}"
                        )

    if checked == 0:
        raise SkipCheck("no project file is present")
    return problems


def _heading_lines(text: str) -> list[tuple[int, str]]:
    """Heading lines outside fenced code blocks, as (line number, text)."""
    out = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence and re.match(r"^#{1,6} ", line):
            out.append((number, line))
    return out


def _anchor_lines(text: str) -> list[tuple[int, str]]:
    """Anchor comment lines outside fenced code blocks, as (line number, id)."""
    out = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = ANCHOR_RE.match(line)
        if match:
            out.append((number, match.group(1)))
    return out


def check_c11(ctx: Context) -> list[str]:
    """The bootstrap-guidance layer's language structure (tooling-delta.md §4 C11).

    Ten assertions, checked independently so a single file can fail more
    than one of them; every problem names the file and the assertion it
    violates (language-structure.md, research.md R6).
    """
    problems = []
    root = ctx.template_dir
    home_rel = GUIDANCE_FILE
    setup_rel = f"{GUIDANCE_DIR}/SETUP.md"
    changelog_rel = f"{GUIDANCE_DIR}/CHANGELOG.md"
    license_rel = f"{GUIDANCE_DIR}/LICENSE"

    guidance_all = [
        rel for rel in iter_files(root) if is_guidance(rel) and selected(ctx, rel)
    ]
    if not guidance_all:
        raise SkipCheck(f"no guidance file present (for example {home_rel})")

    guidance_md = [rel for rel in guidance_all if rel.endswith(".md")]
    translations = {
        rel: source for rel, source in find_translations(root).items() if selected(ctx, rel)
    }
    # Assertion 4: the four files with a fixed, ordered anchor sequence.
    anchor_key_by_path = {
        home_rel: "README",
        ".github/README.zh-CN.md": "README",
        setup_rel: "SETUP",
        f"{GUIDANCE_DIR}/SETUP.zh-CN.md": "SETUP",
    }

    for rel in guidance_md:
        path = root / rel
        text = read_text(path)
        is_translation = rel in translations
        selector_line = SELECTOR_LINES.get(rel)

        # --- 1. Purity ---------------------------------------------------
        stripped = strip_for_purity(text, selector_line)
        if is_translation:
            run = longest_english_run(stripped)
            if run >= 6:
                problems.append(
                    f"{rel}: purity: longest run of consecutive English words is "
                    f"{run} (limit is fewer than 6)"
                )
        else:
            count = cjk_count(stripped)
            if count:
                problems.append(
                    f"{rel}: purity: contains {count} CJK character(s) but must "
                    "be English-only"
                )

        # --- 2. Language selector -----------------------------------------
        lines = text.splitlines()
        if rel in SELECTOR_LINES:
            expected = SELECTOR_LINES[rel]
            indices = [i for i, line in enumerate(lines) if line == expected]
            if not indices:
                problems.append(
                    f"{rel}: language selector: missing the verbatim line {expected!r}"
                )
            else:
                if len(indices) > 1:
                    problems.append(
                        f"{rel}: language selector: the line {expected!r} appears "
                        f"{len(indices)} times, expected exactly once"
                    )
                h1_index = next(
                    (i for i, line in enumerate(lines) if line.startswith("# ")), None
                )
                if h1_index is None:
                    problems.append(f"{rel}: language selector: no H1 heading found")
                elif indices[0] != h1_index + 2 or lines[h1_index + 1].strip() != "":
                    problems.append(
                        f"{rel}: language selector: must appear exactly one blank "
                        "line after the H1 heading"
                    )

            # --- 3. Mutual reachability ------------------------------------
            target_match = re.search(r"\(([^)]+)\)", expected)
            if target_match:
                target = target_match.group(1)
                if not (path.parent / target).is_file():
                    problems.append(
                        f"{rel}: mutual reachability: language-selector target "
                        f"does not exist: {target}"
                    )
        else:
            # Fenced code blocks are excluded here for the same reason as in
            # the purity check (research.md R6): a tutorial snippet showing
            # the selector-line convention (for example GUIDE.md's
            # "Translating your own README" section) is not itself a
            # language entry into this document.
            prose = _strip_fenced_code(text)
            for value in SELECTOR_LINES.values():
                if value in prose:
                    problems.append(
                        f"{rel}: language selector: must not contain a "
                        f"language-selector line: {value!r}"
                    )
            for bad in ("](README.zh-CN.md)", "](SETUP.zh-CN.md)"):
                if bad in prose:
                    problems.append(
                        f"{rel}: language selector: must not link to a "
                        f"translation: {bad}"
                    )

        # --- 4. Anchors ------------------------------------------------
        anchors = _anchor_lines(text)
        headings = _heading_lines(text)
        if rel in anchor_key_by_path:
            key = anchor_key_by_path[rel]
            expected_seq = ANCHOR_SEQUENCES[key]
            actual_seq = [anchor_id for _n, anchor_id in anchors]
            if actual_seq != expected_seq:
                missing = [a for a in expected_seq if a not in actual_seq]
                unexpected = [a for a in actual_seq if a not in expected_seq]
                message = (
                    f"{rel}: anchors: sequence does not match the {key} "
                    f"sequence\n    expected: {expected_seq}\n    found:    {actual_seq}"
                )
                if missing:
                    message += f"\n    missing:    {missing}"
                if unexpected:
                    message += f"\n    unexpected: {unexpected}"
                problems.append(message)
            anchor_line_numbers = {number for number, _id in anchors}
            for number, heading_text in headings:
                if (number - 1) not in anchor_line_numbers:
                    problems.append(
                        f"{rel}:{number}: anchors: heading has no anchor line "
                        f"directly above it: {heading_text}"
                    )
            if len(anchors) != len(headings):
                problems.append(
                    f"{rel}: anchors: anchor count ({len(anchors)}) does not "
                    f"equal heading count ({len(headings)})"
                )
        else:
            if anchors:
                found = ", ".join(f"{number}:{anchor_id}" for number, anchor_id in anchors)
                problems.append(
                    f"{rel}: anchors: must not contain anchor lines (only README "
                    f"and SETUP may): {found}"
                )

        # --- 5. Normative-version notice (translation side) -------------
        if is_translation:
            source_name = Path(translations[rel]).name
            notice = (
                f"> 英文版是规范版本。本页与 [{source_name}]({source_name}) "
                "不一致时，以英文版为准。"
            )
            if notice not in text:
                problems.append(
                    f"{rel}: normative notice: missing the verbatim notice: {notice!r}"
                )

        # --- 7. Single-source markers -------------------------------------
        if is_translation:
            for marker in SINGLE_SOURCE_MARKERS:
                if marker in text:
                    problems.append(
                        f"{rel}: single source: must not contain the "
                        f"single-source marker: {marker!r}"
                    )

    # --- 5 (English side) ----------------------------------------------
    for source_rel in TRANSLATED_DOCS:
        source_path = root / source_rel
        if not source_path.is_file() or not selected(ctx, source_rel):
            continue
        source_name = Path(source_rel).name
        notice = (
            f"> 英文版是规范版本。本页与 [{source_name}]({source_name}) "
            "不一致时，以英文版为准。"
        )
        if notice in read_text(source_path):
            problems.append(
                f"{source_rel}: normative notice: the English original must not "
                f"contain the normative-version notice: {notice!r}"
            )

    # --- 6. Home page: first line is an anchor, second is the title -----
    if home_rel in guidance_all:
        lines = read_text(root / home_rel).splitlines()
        first = lines[0] if lines else ""
        second = lines[1] if len(lines) > 1 else ""
        if not ANCHOR_RE.match(first):
            problems.append(
                f"{home_rel}: home page: first line must be an anchor line, "
                f"found {first!r}"
            )
        if second != GUIDANCE_HOME_TITLE:
            problems.append(
                f"{home_rel}: home page: second line must be "
                f"{GUIDANCE_HOME_TITLE!r}, found {second!r}"
            )

        # --- 8. Preserved assertions -------------------------------------
        text = read_text(root / home_rel)
        for needed in (
            CLEANUP_COMMAND,
            "chefs-pick/SETUP.md",
            "chefs-pick/GUIDE.md",
            "## Feedback and contact",
        ):
            if needed not in text:
                problems.append(f"{home_rel}: missing required string: {needed}")

    # --- 9. Template changelog has at least one version heading ---------
    if changelog_rel in guidance_all:
        text = read_text(root / changelog_rel)
        if not any(line.startswith("## [") for line in text.splitlines()):
            problems.append(f"{changelog_rel}: no '## [' version heading")

    # --- 10. Template LICENSE: purity, then line 3 -----------------------
    if license_rel in guidance_all:
        text = read_text(root / license_rel)
        count = cjk_count(text)
        if count:
            problems.append(
                f"{license_rel}: purity: contains {count} CJK character(s) but "
                "must be English-only"
            )
        lines = text.splitlines()
        expected = "Copyright (c) 2026 Chef's Pick OSS Starter contributors"
        found = lines[2] if len(lines) > 2 else ""
        if found != expected:
            problems.append(
                f"{license_rel}: line 3 must be {expected!r}, found {found!r}"
            )

    return problems


def _table_rows(lines: list[str]) -> list[list[str]]:
    """Parse contiguous Markdown table rows, dropping the separator row."""
    rows = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if cells and all(set(c) <= set("-: ") and c for c in cells):
            continue
        rows.append(cells)
    return rows


def _between(text: str, start: str, end: str) -> list[str] | None:
    if start not in text or end not in text:
        return None
    body = text.split(start, 1)[1].split(end, 1)[0]
    return body.splitlines()


def check_c12(ctx: Context) -> list[str]:
    """SOURCES.md documents every pick with fresh, self-consistent evidence."""
    root = ctx.template_dir
    sources_rel = f"{GUIDANCE_DIR}/SOURCES.md"
    sources_path = root / sources_rel
    if not sources_path.is_file():
        raise SkipCheck(f"missing {sources_rel}")

    home_path = root / GUIDANCE_FILE
    home_text = read_text(home_path) if home_path.is_file() else ""
    summary_lines = _between(home_text, SUMMARY_START, SUMMARY_END)
    summary_rows = _table_rows(summary_lines) if summary_lines else []
    # The summary table's header row is not data.
    summary_data = [r for r in summary_rows if r[0] != "Module"]
    if not summary_data:
        raise SkipCheck(
            f"{GUIDANCE_FILE}: the summary table has no data rows yet "
            "(US2 is only half finished)"
        )

    text = read_text(sources_path)
    problems = []
    limit = RELEASE_FRESH_DAYS if ctx.release else FRESH_DAYS

    def check_date(value: str, where: str):
        date = parse_date(value)
        if date is None:
            problems.append(f"{where}: not a valid date: {value}")
            return
        age = (ctx.today - date).days
        if age > limit:
            problems.append(
                f"{where}: verification date {value} is {age} days old (limit {limit})"
            )

    if "chefs-pick/SOURCES.md" not in home_text:
        problems.append(f"{GUIDANCE_FILE}: must link chefs-pick/SOURCES.md")

    # 1. The single "data verified" line.
    match = re.search(r"Data verified:\s*(\d{4}-\d{2}-\d{2})", text)
    if not match:
        problems.append(f"{sources_rel}: missing the 'Data verified:' line")
    else:
        check_date(match.group(1), f"{sources_rel}: data verified line")

    # 2. The machine-readable adoption table.
    adoption_lines = _between(text, ADOPTION_START, ADOPTION_END)
    table: dict[str, dict] = {}
    if adoption_lines is None:
        problems.append(f"{sources_rel}: missing the adoption-data markers")
    else:
        for row in _table_rows(adoption_lines):
            if row and row[0] == "Repo":
                continue
            if len(row) != 7:
                problems.append(
                    f"{sources_rel}: adoption row must have 7 columns, found "
                    f"{len(row)}: {row}"
                )
                continue
            repo, stars, _forks, _last, _lic, archived, verified = row
            table[repo] = {"stars": stars.replace(",", ""), "archived": archived}
            check_date(verified, f"{sources_rel}: adoption row {repo}")

    # 3. Every ★ reference agrees with the table.
    star_files = [GUIDANCE_FILE, sources_rel, f"{GUIDANCE_DIR}/UPGRADE-TO-TEAM.md"]
    for rel in star_files:
        path = root / rel
        if not path.is_file():
            continue
        for stars, repo in STAR_RE.findall(read_text(path)):
            if repo not in table:
                problems.append(f"{rel}: {repo} is not in the adoption data table")
            elif stars.replace(",", "") != table[repo]["stars"]:
                problems.append(
                    f"{rel}: ★ {stars} ({repo}) disagrees with the table "
                    f"({table[repo]['stars']})"
                )

    # 4. One section per module, M01..M16.
    sections: dict[str, str] = {}
    current = None
    buffer: list[str] = []
    for line in text.splitlines():
        if line.startswith("### "):
            if current:
                sections[current] = "\n".join(buffer)
            m = re.match(r"^### (M\d{2})", line)
            current = m.group(1) if m else None
            buffer = []
        elif line.startswith("## "):
            if current:
                sections[current] = "\n".join(buffer)
            current = None
            buffer = []
        elif current:
            buffer.append(line)
    if current:
        sections[current] = "\n".join(buffer)

    evidence_types = [
        "Exact stars",
        "Rounded stars",
        "Estimated users",
        "Official platform feature",
        "De facto standard",
        "Not available",
    ]

    for index in range(1, 17):
        module = f"M{index:02d}"
        section = sections.get(module)
        if section is None:
            problems.append(f"{sources_rel}: missing section '### {module}'")
            continue

        fields = {}
        for row in _table_rows(section.splitlines()):
            if len(row) >= 2 and row[0] != "Field":
                fields[row[0]] = row[1]

        for label in FIELD_LABELS:
            if label not in fields:
                problems.append(f"{sources_rel}: {module} is missing the field: {label}")

        level = fields.get("Level")
        if level is not None and level not in LEVEL_VALUES:
            problems.append(f"{sources_rel}: {module} has an invalid level: {level}")

        verified = fields.get("Verified")
        if verified is not None:
            check_date(verified, f"{sources_rel}: {module} verified cell")

        evidence = fields.get("Evidence", "")
        if evidence and not any(label in evidence for label in evidence_types):
            problems.append(
                f"{sources_rel}: {module} evidence cell has no registered evidence type"
            )
        first_star = STAR_RE.search(evidence)
        if first_star:
            repo = first_star.group(2)
            if repo in table and table[repo]["archived"].lower() == "yes":
                problems.append(
                    f"{sources_rel}: {module}'s chosen source {repo} is archived"
                )

        # Now that SOURCES.md is English-only there is a single "Rationale"
        # paragraph per module (tooling-delta.md §4 C12), not a bilingual pair.
        for marker, label in (("**Rationale**", "Rationale"),):
            if marker not in section:
                problems.append(f"{sources_rel}: {module} has no {label} paragraph")
                continue
            # Only the paragraph itself counts: stop at the first blank line so an
            # empty block cannot borrow text from the one that follows.
            paragraph = section.split(marker, 1)[1].split("\n\n", 1)[0]
            if not paragraph.lstrip(":：").strip():
                problems.append(
                    f"{sources_rel}: {module} has no non-empty {label} paragraph"
                )

        alt = section.split("**Alternatives**", 1)
        if len(alt) < 2 or not re.search(r"^\s*[-*]\s+\S", alt[1], re.MULTILINE):
            problems.append(f"{sources_rel}: {module} needs at least one alternative")

        rule = (fields.get("Rule") or "").strip()
        if rule == "2" and "comparable adoption" not in section:
            problems.append(
                f"{sources_rel}: {module} uses rule 2, so its Rationale must state "
                "comparable adoption"
            )

    # 5. The home page summary table: exactly 16 rows, M01..M16 in order.
    if len(summary_data) != 16:
        problems.append(
            f"{GUIDANCE_FILE}: the summary table must have exactly 16 data rows, "
            f"found {len(summary_data)}"
        )
    for position, row in enumerate(summary_data[:16], start=1):
        expected = f"M{position:02d}"
        if not row[0].startswith(expected):
            problems.append(
                f"{GUIDANCE_FILE}: summary row {position} must start with {expected}, "
                f"found {row[0]!r}"
            )
        if len(row) >= 4:
            check_date(row[3], f"{GUIDANCE_FILE}: summary row {expected}")

    # 6. The excluded-candidates section.
    excluded_heading = "## Excluded candidates"
    if excluded_heading not in text:
        problems.append(f"{sources_rel}: missing the '{excluded_heading}' section")
    else:
        body = text.split(excluded_heading, 1)[1].split("\n## ", 1)[0]
        rows = [
            r
            for r in _table_rows(body.splitlines())
            if r[0] != "Candidate"
        ]
        if len(rows) < 8:
            problems.append(
                f"{sources_rel}: the excluded-candidates table needs at least 8 rows, "
                f"found {len(rows)}"
            )
        for row in rows:
            if len(row) < 3 or not all(cell for cell in row[:3]):
                problems.append(
                    f"{sources_rel}: excluded-candidates row has an empty cell: {row}"
                )

    return problems
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HREF_RE = re.compile(r'href="([^"]+)"')


def _iter_links(text: str):
    text = _strip_fenced_code(text)
    for match in LINK_RE.finditer(text):
        yield match.group(1)
    for match in HREF_RE.finditer(text):
        yield match.group(1)


def _relative_link_problems(root: Path, rels: list[str]) -> list[str]:
    """Shared C14 logic, usable against a copy of the template."""
    problems = []
    for rel in rels:
        if not rel.endswith(".md"):
            continue
        base = (root / rel).parent
        for target in _iter_links(read_text(root / rel)):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            cleaned = target.split("#", 1)[0].split("?", 1)[0]
            if not cleaned:
                continue
            resolved = (base / cleaned).resolve()
            try:
                resolved_rel = resolved.relative_to(root.resolve()).as_posix()
            except ValueError:
                problems.append(f"{rel}: link escapes the template: {target}")
                continue
            if not resolved.exists():
                problems.append(f"{rel}: broken relative link: {target}")
                continue
            if not is_guidance(rel) and is_guidance(resolved_rel):
                problems.append(
                    f"{rel}: project file must not link into the guidance layer: {target}"
                )
    return problems


def check_c13(ctx: Context) -> list[str]:
    """Removing the guidance layer leaves a clean, self-consistent template."""
    import shutil
    import tempfile

    root = ctx.template_dir
    if not (root / "README.md").is_file():
        raise SkipCheck("missing README.md")
    setup_rel = f"{GUIDANCE_DIR}/SETUP.md"
    if not (root / setup_rel).is_file():
        raise SkipCheck(f"missing {setup_rel}")

    registry = parse_placeholder_registry(read_text(root / setup_rel))
    problems = []

    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "template"
        shutil.copytree(root, copy)
        guidance_file = copy / GUIDANCE_FILE
        if guidance_file.exists():
            guidance_file.unlink()
        # language-structure.md §6, tooling-delta.md §4: the cleanup command
        # also removes the home page's translation, which lives beside it
        # outside GUIDANCE_DIR.
        home_translation = copy / ".github/README.zh-CN.md"
        if home_translation.exists():
            home_translation.unlink()
        guidance_dir = copy / GUIDANCE_DIR
        if guidance_dir.exists():
            shutil.rmtree(guidance_dir)

        remaining = iter_files(copy)
        found: set[str] = set()
        for rel in remaining:
            text = read_text(copy / rel)
            for needle in ("chefs-pick/", ".github/README.md", ".github/README.zh-CN.md"):
                if needle in text:
                    problems.append(f"after cleanup, {rel} still references {needle}")
            match = IDENTITY_RE.search(text)
            if match:
                problems.append(
                    f"after cleanup, {rel} still contains template identity: {match.group(0)}"
                )
            found.update(PLACEHOLDER_RE.findall(text))

        extra = sorted(found - set(registry))
        if extra:
            problems.append(f"after cleanup, unregistered placeholders remain: {extra}")

        if not (copy / "README.md").is_file():
            problems.append("after cleanup, README.md is missing")

        problems.extend(
            f"after cleanup, {p}" for p in _relative_link_problems(copy, remaining)
        )

    return problems


def check_c14(ctx: Context) -> list[str]:
    """Every relative link resolves inside the template."""
    rels = [rel for rel in iter_files(ctx.template_dir) if selected(ctx, rel)]
    if not any(rel.endswith(".md") for rel in rels):
        raise SkipCheck("no Markdown file present")
    return _relative_link_problems(ctx.template_dir, rels)


def check_c15(ctx: Context) -> list[str]:
    """The root LICENSE is the MIT text with the two placeholders in place."""
    path = ctx.template_dir / "LICENSE"
    if not path.is_file():
        raise SkipCheck("missing LICENSE")
    if not selected(ctx, "LICENSE"):
        raise SkipCheck("LICENSE not selected by --files")

    problems = []
    text = read_text(path)
    lines = text.splitlines()

    first = lines[0] if lines else ""
    if first != "MIT License":
        problems.append(f"LICENSE: line 1 must be 'MIT License', found {first!r}")

    expected = "Copyright (c) 2026 anyingiit"
    third = lines[2] if len(lines) > 2 else ""
    if third != expected:
        problems.append(f"LICENSE: line 3 must be {expected!r}, found {third!r}")

    for needed in (
        "Permission is hereby granted, free of charge",
        'THE SOFTWARE IS PROVIDED "AS IS"',
    ):
        if needed not in text:
            problems.append(f"LICENSE: missing required text: {needed}")

    for forbidden in ("[year]", "[fullname]"):
        if forbidden in text:
            problems.append(f"LICENSE: upstream placeholder not replaced: {forbidden}")

    return problems





def check_c17(ctx: Context) -> list[str]:
    """GUIDE.md's Remove section names every file that references the module."""
    guide_rel = f"{GUIDANCE_DIR}/GUIDE.md"
    guide = ctx.template_dir / guide_rel
    if not guide.is_file():
        raise SkipCheck(f"missing {guide_rel}")

    text = read_text(guide)
    sections: dict[str, str] = {}
    current = None
    buffer: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current:
                sections[current] = "\n".join(buffer)
            match = re.match(r"^## (M\d{2})", line)
            current = match.group(1) if match else None
            buffer = []
        elif current:
            buffer.append(line)
    if current:
        sections[current] = "\n".join(buffer)

    problems = []
    present = set(project_files(ctx))

    for module, (files, declared) in REMOVAL_REFS.items():
        if module in ("M01", "M02", "M03"):
            continue
        referrers = set(declared)
        # Auto-discover: any other project file that mentions one of the files.
        for rel in files:
            name = rel.rsplit("/", 1)[-1]
            for other in present:
                if other in files:
                    continue
                if name in read_text(ctx.template_dir / other):
                    referrers.add(other)
        section = sections.get(module)
        if section is None:
            if referrers:
                problems.append(f"{guide_rel}: missing section '## {module}'")
            continue
        for referrer in sorted(referrers):
            name = referrer.rsplit("/", 1)[-1]
            if name not in section:
                problems.append(
                    f"{guide_rel}: section '## {module}' does not mention {name}, "
                    "which references this module"
                )
    return problems
def _english_headings(ctx, rel, wanted, what):
    """Shared C18/C19 logic: every wanted English phrase is a level-2 heading."""
    path = ctx.template_dir / rel
    if not path.is_file():
        raise SkipCheck(f"missing {rel}")
    headings = [line for _n, line in _heading_lines(read_text(path))
                if line.startswith("## ")]
    problems = []
    for english in wanted:
        if not any(english in line for line in headings):
            problems.append(f"{rel}: missing the '{english}' heading ({what})")
    return problems


def check_c18(ctx: Context) -> list[str]:
    """MAINTAINING.md carries the six headings from guidance-layer §5.

    Plus two assertions added by tooling-delta.md §4 C18: the ``## Release
    gates`` section must spell out exactly 6 ordered-list items, and the
    page must mention ``--update-digests`` (research.md R9).
    """
    rel = f"{GUIDANCE_DIR}/MAINTAINING.md"
    problems = _english_headings(ctx, rel, MAINTAINING_HEADINGS, "guidance-layer §5")

    path = ctx.template_dir / rel
    if path.is_file():
        text = read_text(path)
        if "--update-digests" not in text:
            problems.append(f"{rel}: must mention --update-digests")

        gates_heading = "## Release gates"
        if gates_heading in text:
            body = text.split(gates_heading, 1)[1].split("\n## ", 1)[0]
            gate_items = re.findall(r"^\d+\.\s", body, re.MULTILINE)
            if len(gate_items) != 6:
                problems.append(
                    f"{rel}: the '{gates_heading}' section must have exactly 6 "
                    f"ordered-list items, found {len(gate_items)}"
                )
    return problems


def check_c19(ctx: Context) -> list[str]:
    """UPGRADE-TO-TEAM.md carries the three headings from guidance-layer §6.

    The page is optional P4 content, so a missing file is a SKIP.
    """
    return _english_headings(
        ctx, f"{GUIDANCE_DIR}/UPGRADE-TO-TEAM.md", UPGRADE_HEADINGS, "guidance-layer §6"
    )



def check_c21(ctx: Context) -> list[str]:
    """UTF-8, one trailing newline, no trailing blanks, no CRLF.

    Read as bytes: ``Path.read_text`` silently turns CRLF into LF under
    universal newlines, which would make the CRLF check always pass.
    """
    problems = []
    checked = 0
    for rel in iter_files(ctx.template_dir):
        if not selected(ctx, rel):
            continue
        checked += 1
        raw = (ctx.template_dir / rel).read_bytes()
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            problems.append(f"{rel}: not valid UTF-8: {exc}")
            continue
        if b"\r\n" in raw:
            problems.append(f"{rel}: contains CRLF line endings")
        if raw == b"":
            problems.append(f"{rel}: empty file (expected a single trailing newline)")
        elif not raw.endswith(b"\n"):
            problems.append(f"{rel}: missing newline at end of file")
        elif raw.endswith(b"\n\n"):
            problems.append(f"{rel}: more than one newline at end of file")
        for number, line in enumerate(raw.split(b"\n"), start=1):
            if line.endswith(b" ") or line.endswith(b"\t"):
                problems.append(f"{rel}:{number}: trailing whitespace")
    if checked == 0:
        raise SkipCheck("no files present")
    return problems


def check_c22(ctx: Context) -> list[str]:
    """Deleting any one recommended/optional module leaves the rest working."""
    import shutil
    import tempfile

    root = ctx.template_dir
    if not (root / "README.md").is_file():
        raise SkipCheck("missing README.md")

    problems = []
    for module, (files, _declared) in REMOVAL_REFS.items():
        present = [rel for rel in files if (root / rel).is_file()]
        if not present:
            continue
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "template"
            shutil.copytree(root, copy)
            for rel in present:
                (copy / rel).unlink()

            remaining = iter_files(copy)
            sub = Context(template_dir=copy, release=ctx.release, today=ctx.today)

            # Same as C03.
            for rel in remaining:
                if not rel.endswith((".yml", ".yaml")):
                    continue
                try:
                    load_yaml(copy / rel)
                except yaml.YAMLError as exc:
                    problems.append(f"after removing {module}, {rel} is not valid YAML: {exc}")

            # Same as C05 / C06, when those files survive.
            if (copy / ".github/workflows/ci.yml").is_file():
                try:
                    for problem in check_c05(sub):
                        problems.append(f"after removing {module}, {problem}")
                except SkipCheck:
                    pass
            if (copy / ".github/dependabot.yml").is_file():
                try:
                    for problem in check_c06(sub):
                        problems.append(f"after removing {module}, {problem}")
                except SkipCheck:
                    pass

            # Same as C14, except that links to the deleted files are expected:
            # C17 guarantees GUIDE.md explains how to fix them.
            deleted_names = {rel.rsplit("/", 1)[-1] for rel in present}
            for problem in _relative_link_problems(copy, remaining):
                if any(name in problem for name in deleted_names):
                    continue
                problems.append(f"after removing {module}, {problem}")

            # No YAML config may still name a deleted file.
            for rel in remaining:
                if not rel.endswith((".yml", ".yaml")):
                    continue
                text = read_text(copy / rel)
                for name in sorted(deleted_names):
                    if name in text:
                        problems.append(
                            f"after removing {module}, {rel} still references {name}"
                        )
    return problems


def check_c23(ctx: Context) -> list[str]:
    """The verbatim 001 contract's star counts agree with ``template/``.

    tooling-delta.md §5 C23: paths are resolved relative to the repository
    root (the script's own parent directory's parent), never to
    ``--template-dir``, so this check always looks at the real contract and
    the real template regardless of ``ctx.template_dir``.

    Every ``★ N (owner/repo)`` occurrence is kept, on both sides, as its own
    ``(file, value)`` pair rather than collapsed into one dict entry per
    repository -- collapsing would let a later file silently overwrite an
    earlier file's drifted value and hide it from the comparison. Each
    template occurrence is compared against the contract's value for that
    repository, and every disagreement is reported individually. A
    repository that itself carries more than one distinct value -- within
    the contract, or within ``template/`` -- is also reported, as an
    internal self-contradiction, independent of any cross-side comparison.
    """
    repo_root = Path(__file__).resolve().parent.parent
    contract_path = (
        repo_root / "specs/001-chefs-pick-starter/contracts/guidance-layer.md"
    )
    if not contract_path.is_file():
        raise SkipCheck(f"missing {contract_path}")

    contract_rel = "specs/001-chefs-pick-starter/contracts/guidance-layer.md"
    contract_stars: dict[str, list[tuple[str, str]]] = {}
    for stars, repo in STAR_RE.findall(read_text(contract_path)):
        contract_stars.setdefault(repo, []).append(
            (contract_rel, stars.replace(",", ""))
        )

    template_stars: dict[str, list[tuple[str, str]]] = {}
    template_root = repo_root / "template"
    if template_root.is_dir():
        for rel in iter_files(template_root):
            if not rel.endswith(".md"):
                continue
            for stars, repo in STAR_RE.findall(read_text(template_root / rel)):
                template_stars.setdefault(repo, []).append(
                    (rel, stars.replace(",", ""))
                )

    cross_problems: list[tuple[str, str, str]] = []
    for repo in sorted(set(contract_stars) & set(template_stars)):
        contract_occurrences = sorted(contract_stars[repo])
        # When the contract itself disagrees with itself, point 3 below
        # reports that self-contradiction; use its first (sorted) value as
        # "the" contract value here so every template occurrence still gets
        # compared against something concrete.
        contract_value = contract_occurrences[0][1]
        for rel, value in sorted(template_stars[repo]):
            if value != contract_value:
                cross_problems.append(
                    (
                        repo,
                        rel,
                        f"{rel}: {repo} has {value}, contract has {contract_value}",
                    )
                )

    self_problems: list[tuple[str, str, str]] = []
    for repo in sorted(set(contract_stars) | set(template_stars)):
        for occurrences in (
            contract_stars.get(repo, []),
            template_stars.get(repo, []),
        ):
            distinct = sorted(set(occurrences))
            for i in range(len(distinct)):
                for j in range(i + 1, len(distinct)):
                    rel_a, value_a = distinct[i]
                    rel_b, value_b = distinct[j]
                    if value_a != value_b:
                        self_problems.append(
                            (
                                repo,
                                rel_a,
                                f"{repo}: {rel_a} has {value_a}, "
                                f"{rel_b} has {value_b}",
                            )
                        )

    problems = [text for _repo, _rel, text in sorted(cross_problems)]
    problems += [text for _repo, _rel, text in sorted(self_problems)]
    seen: set[str] = set()
    deduped: list[str] = []
    for text in problems:
        if text not in seen:
            seen.add(text)
            deduped.append(text)
    return deduped


def check_c24(ctx: Context) -> list[str]:
    """Every translation's source marker matches its current English source.

    tooling-delta.md §5 C24: a stale-but-well-formed digest is a WARN
    (a FAIL under ``--release``); a missing marker, a malformed marker, or
    a marker naming a source file that does not exist is always a FAIL,
    since those are structural problems, not freshness problems.
    """
    root = ctx.template_dir
    translations = find_translations(root)
    if not translations:
        raise SkipCheck("no translation is present")

    problems: list[str] = []
    stale: list[str] = []
    for translation_rel, source_rel in sorted(translations.items()):
        if not (selected(ctx, translation_rel) or selected(ctx, source_rel)):
            continue
        source_name = Path(source_rel).name
        text = read_text(root / translation_rel)

        # Count marker *candidates*, not only well-formed ones: a valid
        # marker sitting next to a malformed duplicate for the same source
        # used to read as exactly one marker here, so the duplicate passed
        # unnoticed while --update-digests refused the same file. The two
        # now agree. See ``_marker_candidates``.
        candidates = _marker_candidates(text, source_name)

        if len(candidates) > 1:
            problems.append(
                f"{translation_rel}: found {len(candidates)} source "
                f"marker lines for {source_name} (expected exactly one line "
                f"'<!-- translation-of: {source_name} sha256:<16 hex> -->')"
            )
            continue

        digest_match = DIGEST_RE.match(candidates[0].group(0)) if candidates else None
        if digest_match is None or digest_match.group(1) != source_name:
            problems.append(
                f"{translation_rel}: missing or malformed source marker for "
                f"{source_name} (expected exactly one line "
                f"'<!-- translation-of: {source_name} sha256:<16 hex> -->')"
            )
            continue

        source_path = root / source_rel
        if not source_path.is_file():
            problems.append(
                f"{translation_rel}: source marker names a file that does not "
                f"exist: {source_rel}"
            )
            continue

        recorded_digest = digest_match.group(2)
        actual_digest = hashlib.sha256(source_path.read_bytes()).hexdigest()[:16]
        if recorded_digest != actual_digest:
            stale.append(
                f"{translation_rel}: source marker is stale for {source_rel} "
                f"(recorded {recorded_digest}, current {actual_digest}); run "
                "python3 tools/check_template.py --update-digests"
            )

    if problems:
        return problems + stale
    if stale:
        if ctx.release:
            return stale
        raise WarnCheck(stale)
    return []


def _workspace_gate(repo_root: Path) -> tuple[str | None, str | None, list[str]]:
    """Resolve README.md / README.zh-CN.md for C25/C26/C27's shared gate.

    tooling-delta-003.md §2 (corrected -- see Finding 2 in
    tooling-delta-003.md §2 for the full rationale): the *only* condition
    under which C25, C26 and C27 raise ``SkipCheck`` is ``template/`` not
    existing at all -- i.e. this is not the workspace repository. A
    missing ``README.md``, or one that lacks the verbatim
    ``WORKSPACE_SELECTOR_LINES["README.md"]`` line, is a structural FAIL,
    never a skip: skipping either of those let a single deleted or
    misspelled line silently turn off all three checks.

    Returns ``(source_text, translation_text, problems)``. When the gate
    itself fails, ``source_text`` is ``None`` and ``problems`` already
    holds the one FAIL message naming what is missing -- callers must
    return ``problems`` as-is in that case. Otherwise ``problems`` is
    ``[]`` and ``translation_text`` is ``None`` only when
    ``README.zh-CN.md`` does not exist (callers decide how to report
    that, since C25/C26/C27 phrase it slightly differently).
    """
    template_dir = repo_root / "template"
    if not template_dir.is_dir():
        raise SkipCheck(f"missing {template_dir}")

    source_path = repo_root / WORKSPACE_SOURCE
    translation_path = repo_root / WORKSPACE_TRANSLATION

    if not source_path.is_file():
        return None, None, [f"{WORKSPACE_SOURCE}: file does not exist"]

    source_text = read_text(source_path)
    expected = WORKSPACE_SELECTOR_LINES[WORKSPACE_SOURCE]
    if expected not in source_text.splitlines():
        return None, None, [
            f"{WORKSPACE_SOURCE}: language selector: missing the verbatim "
            f"line {expected!r}"
        ]

    translation_text = read_text(translation_path) if translation_path.is_file() else None
    return source_text, translation_text, []


def _git_tracked_file_count(repo_root: Path, subpath: str) -> int:
    """Count of git-tracked files under ``repo_root / subpath``.

    tooling-delta-003.md §4 C26 declares the ``template/`` file count as
    "被 git 跟踪的文件数" (the count of git-tracked files), not a raw
    filesystem walk -- ``iter_files`` also counts untracked files, so a
    stray untracked file under ``template/`` (a scratch file, a build
    artefact) would make a correct declaration look wrong. This runs git
    from *repo_root* rather than falling back to a filesystem walk when
    git is unavailable, since a fallback could silently give a different
    (wrong) answer instead of failing loudly.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "ls-files", "--", subpath],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SkipCheck(
            f"unable to run `git -C {repo_root} ls-files -- {subpath}`: {exc}"
        ) from exc
    return len([line for line in result.stdout.splitlines() if line])


def _marker_candidates(text: str, source_name: str) -> list[re.Match]:
    """Lines in *text* that purport to be a ``translation-of`` marker for
    *source_name*, whether or not the digest portion is well-formed.

    ``DIGEST_RE`` alone only recognises a *well-formed* marker line
    (exactly 16 lowercase hex digits), so a well-formed marker sitting
    next to a malformed duplicate for the same source is invisible to
    code that looks only for ``DIGEST_RE`` matches: the malformed line is
    silently ignored instead of tripping the "more than one marker" FAIL.
    Detecting this broader set of *candidate* marker lines first lets a
    duplicate be caught even when it is malformed. Matching group 1 is
    the (possibly malformed) digest text.
    """
    candidate_re = re.compile(
        r"^<!-- translation-of: " + re.escape(source_name) + r" sha256:(\S*) -->$"
    )
    return [m for m in (candidate_re.match(line) for line in text.splitlines()) if m]


def check_c25(ctx: Context) -> list[str]:
    """The workspace homepage's own language structure (tooling-delta-003.md §3 C25).

    tooling-delta-003.md §2: paths are resolved relative to the repository
    root (the script's own parent directory's parent), never to
    ``ctx.template_dir`` -- the workspace homepage (``README.md``) lives
    outside ``template/``, same rationale as check_c23.

    Skip condition (tooling-delta-003.md §2, corrected by Finding 2):
    ``template/`` missing is the *only* SkipCheck condition now. A missing
    ``README.md``, or one that is missing the verbatim language-selector
    line, is a FAIL (see ``_workspace_gate``). A missing translation is
    likewise *not* a skip condition: that is a FAIL, since the selector
    then points at a file that does not exist.
    """
    repo_root = Path(__file__).resolve().parent.parent
    source_text, translation_text, problems = _workspace_gate(repo_root)
    if source_text is None:
        return problems

    texts = {WORKSPACE_SOURCE: source_text}
    if translation_text is not None:
        texts[WORKSPACE_TRANSLATION] = translation_text
    else:
        problems.append(f"{WORKSPACE_TRANSLATION}: file does not exist")

    # --- 2. Language selector -------------------------------------------
    for rel, text in texts.items():
        expected = WORKSPACE_SELECTOR_LINES[rel]
        lines = text.splitlines()
        h1_index = next(
            (i for i, line in enumerate(lines) if line.startswith("# ")), None
        )
        if h1_index is None:
            problems.append(f"{rel}: language selector: no H1 heading found")
        elif (
            h1_index + 2 >= len(lines)
            or lines[h1_index + 1].strip() != ""
            or lines[h1_index + 2] != expected
        ):
            problems.append(
                f"{rel}: language selector: must appear exactly one blank "
                "line after the H1 heading"
            )

        # --- 3, 4. Anchors ------------------------------------------------
        anchors = _anchor_lines(text)
        headings = _heading_lines(text)
        actual_seq = [anchor_id for _n, anchor_id in anchors]
        if actual_seq != WORKSPACE_ANCHOR_SEQUENCE:
            missing = [a for a in WORKSPACE_ANCHOR_SEQUENCE if a not in actual_seq]
            unexpected = [a for a in actual_seq if a not in WORKSPACE_ANCHOR_SEQUENCE]
            message = (
                f"{rel}: anchors: sequence does not match the workspace "
                f"sequence\n    expected: {WORKSPACE_ANCHOR_SEQUENCE}\n    "
                f"found:    {actual_seq}"
            )
            if missing:
                message += f"\n    missing:    {missing}"
            if unexpected:
                message += f"\n    unexpected: {unexpected}"
            problems.append(message)
        anchor_line_numbers = {number for number, _id in anchors}
        for number, heading_text in headings:
            if (number - 1) not in anchor_line_numbers:
                problems.append(
                    f"{rel}:{number}: anchors: heading has no anchor line "
                    f"directly above it: {heading_text}"
                )
        if len(anchors) != len(headings):
            problems.append(
                f"{rel}: anchors: anchor count ({len(anchors)}) does not "
                f"equal heading count ({len(headings)})"
            )

    # --- 5. Normative-version notice ------------------------------------
    notice = (
        "> 英文版是规范版本。本页与 [README.md](README.md) "
        "不一致时，以英文版为准。"
    )
    if WORKSPACE_TRANSLATION in texts and notice not in texts[WORKSPACE_TRANSLATION]:
        problems.append(
            f"{WORKSPACE_TRANSLATION}: normative notice: missing the "
            f"verbatim notice: {notice!r}"
        )
    if notice in texts[WORKSPACE_SOURCE]:
        problems.append(
            f"{WORKSPACE_SOURCE}: normative notice: must not contain the "
            "normative-version notice"
        )

    # --- 6. Language purity ----------------------------------------------
    stripped_source = strip_for_purity(
        texts[WORKSPACE_SOURCE], WORKSPACE_SELECTOR_LINES[WORKSPACE_SOURCE]
    )
    count = cjk_count(stripped_source)
    if count:
        problems.append(
            f"{WORKSPACE_SOURCE}: purity: contains {count} CJK character(s) "
            "but must be English-only"
        )
    if WORKSPACE_TRANSLATION in texts:
        stripped_translation = strip_for_purity(
            texts[WORKSPACE_TRANSLATION], WORKSPACE_SELECTOR_LINES[WORKSPACE_TRANSLATION]
        )
        run = longest_english_run(stripped_translation)
        if run >= 6:
            problems.append(
                f"{WORKSPACE_TRANSLATION}: purity: longest run of consecutive "
                f"English words is {run} (limit is fewer than 6)"
            )

    return problems


def check_c26(ctx: Context) -> list[str]:
    """The workspace homepage's declared facts agree with reality (tooling-delta-003.md §4 C26).

    tooling-delta-003.md §2: paths are resolved relative to the repository
    root (the script's own parent directory's parent), never to
    ``ctx.template_dir`` -- same rationale as check_c23 and check_c25.

    Skip condition (tooling-delta-003.md §2, corrected by Finding 2): same
    as check_c25 -- ``template/`` missing is the only SkipCheck condition;
    a missing ``README.md`` or a missing selector line is a FAIL (see
    ``_workspace_gate``). A missing ``README.zh-CN.md`` is also a FAIL
    (Finding 6), naming the missing file, rather than being silently
    dropped from the set of files this check validates.

    The declared ``template/`` file count (tooling-delta-003.md §4.1) is
    compared against the count of git-tracked files under ``template/``
    (Finding 4), not a filesystem walk -- an untracked scratch file must
    not make a correct declaration look wrong.
    """
    repo_root = Path(__file__).resolve().parent.parent
    source_text, translation_text, problems = _workspace_gate(repo_root)
    if source_text is None:
        return problems

    texts = {WORKSPACE_SOURCE: source_text}
    if translation_text is not None:
        texts[WORKSPACE_TRANSLATION] = translation_text
    else:
        problems.append(f"{WORKSPACE_TRANSLATION}: file does not exist")

    actual_files = _git_tracked_file_count(repo_root, "template")
    actual_checks = len(CHECKS)
    spec_dirs = sorted(
        path.name for path in (repo_root / "specs").iterdir() if path.is_dir()
    )

    file_count_re = {
        WORKSPACE_SOURCE: re.compile(r"`template/` holds (\d+) files"),
        WORKSPACE_TRANSLATION: re.compile(r"`template/` 共 (\d+) 个文件"),
    }
    checks_count_re = {
        WORKSPACE_SOURCE: re.compile(r"(\d+) structural checks"),
        WORKSPACE_TRANSLATION: re.compile(r"(\d+) 项结构校验"),
    }

    for rel, text in texts.items():
        # --- 1. template/ file count -----------------------------------
        match = file_count_re[rel].search(text)
        if match is None:
            problems.append(f"{rel}: no template file count found")
        else:
            declared = int(match.group(1))
            if declared != actual_files:
                problems.append(
                    f"{rel}: template file count says {declared}, actual {actual_files}"
                )

        # --- 2. structural check count -----------------------------------
        match = checks_count_re[rel].search(text)
        if match is None:
            problems.append(f"{rel}: no structural check count found")
        else:
            declared = int(match.group(1))
            if declared != actual_checks:
                problems.append(
                    f"{rel}: structural check count says {declared}, actual {actual_checks}"
                )

        # --- 3. spec directories ------------------------------------------
        for name in spec_dirs:
            if f"`specs/{name}/`" not in text:
                problems.append(f"{rel}: spec directory {name} is not listed")

    return problems


def check_c27(ctx: Context) -> list[str]:
    """The workspace homepage's translation stays fresh (tooling-delta-003.md §5 C27).

    Isomorphic to check_c24, with the workspace homepage (``README.md``)
    as the source instead of a ``template/`` guidance file.

    tooling-delta-003.md §2: paths are resolved relative to the repository
    root (the script's own parent directory's parent), never to
    ``ctx.template_dir`` -- same rationale as check_c23, check_c25 and
    check_c26.

    Skip condition (tooling-delta-003.md §2, corrected by Finding 2): same
    as check_c25 and check_c26 -- ``template/`` missing is the only
    SkipCheck condition; a missing ``README.md`` or a missing selector
    line is a FAIL (see ``_workspace_gate``).

    Finding 5: a valid marker line and a malformed duplicate marker line
    for the same source must both be detected as *candidates* before
    either is validated, so the malformed duplicate cannot hide behind
    the valid one and slip through as a PASS -- see ``_marker_candidates``.
    """
    repo_root = Path(__file__).resolve().parent.parent
    source_text, translation_text, problems = _workspace_gate(repo_root)
    if source_text is None:
        return problems

    malformed_message = [
        f"{WORKSPACE_TRANSLATION}: missing or malformed source marker for "
        f"{WORKSPACE_SOURCE} (expected exactly one line "
        f"'<!-- translation-of: {WORKSPACE_SOURCE} sha256:<16 hex> -->')"
    ]

    if translation_text is None:
        return malformed_message

    candidates = _marker_candidates(translation_text, WORKSPACE_SOURCE)

    if not candidates:
        return malformed_message

    if len(candidates) > 1:
        return [
            f"{WORKSPACE_TRANSLATION}: found {len(candidates)} source "
            f"marker lines for {WORKSPACE_SOURCE} (expected exactly one line "
            f"'<!-- translation-of: {WORKSPACE_SOURCE} sha256:<16 hex> -->')"
        ]

    candidate = candidates[0]
    recorded_digest = candidate.group(1)
    if not re.fullmatch(r"[0-9a-f]{16}", recorded_digest):
        return malformed_message

    source_path = repo_root / WORKSPACE_SOURCE
    actual_digest = hashlib.sha256(source_path.read_bytes()).hexdigest()[:16]
    if recorded_digest != actual_digest:
        message = (
            f"{WORKSPACE_TRANSLATION}: source marker is stale for "
            f"{WORKSPACE_SOURCE} (recorded {recorded_digest}, current "
            f"{actual_digest}); run python3 tools/check_template.py "
            "--update-digests"
        )
        if ctx.release:
            return [message]
        raise WarnCheck([message])
    return []


def _refresh_translation_digest(
    translation_path: Path, translation_rel: str, source_path: Path, source_name: str
) -> bool:
    """Refresh one translation file's source-marker digest in place.

    The single substitution implementation shared by every
    ``--update-digests`` caller (tooling-delta-003.md §7): a single
    in-place regex substitution, a ``write_bytes`` write-back, and --
    with the file left byte-for-byte untouched -- a refusal whenever more
    than one marker line for *source_name* is found. Only the
    ``<!-- translation-of: ... sha256:... -->`` line is ever rewritten;
    every other byte of the file is left untouched (tooling-delta.md
    §1.2). Returns ``True`` when the file's digest was actually rewritten.
    """
    digest = hashlib.sha256(source_path.read_bytes()).hexdigest()[:16]
    text = translation_path.read_bytes().decode("utf-8")

    # Match the marker line's text only, without consuming the line
    # ending -- a lookahead for an optional trailing "\r" (before the
    # "\n" that (?m) $ matches against) means the substitution below
    # never touches a line-ending byte, whatever it is (tooling-delta.md
    # §1.2). Using a regex over the whole decoded text, rather than
    # splitting on a single detected newline, also means a file mixing
    # CRLF and LF still has every one of its marker lines found.
    #
    # Finding 5: the digest group is deliberately permissive (``\S*``,
    # not ``[0-9a-f]{16}``) so that a *malformed* duplicate marker is
    # still counted as a candidate here. Matching only well-formed
    # markers would let a well-formed marker be refreshed in place while
    # a malformed duplicate for the same source is silently left behind
    # -- the file would then have two marker lines for *source_name*, one
    # of them stale garbage, and update-digests would have reported
    # success.
    marker_re = re.compile(
        r"(?m)^<!-- translation-of: "
        + re.escape(source_name)
        + r" sha256:(\S*) -->(?=\r?$)"
    )
    matches = list(marker_re.finditer(text))

    if not matches:
        return False

    if len(matches) > 1:
        print(
            f"{translation_rel}: skipped (found {len(matches)} source "
            f"marker lines for {source_name}; expected exactly one)"
        )
        return False

    match = matches[0]
    old_digest = match.group(1)
    if not re.fullmatch(r"[0-9a-f]{16}", old_digest):
        print(
            f"{translation_rel}: skipped (malformed source marker for "
            f"{source_name})"
        )
        return False
    if old_digest != digest:
        new_line = f"<!-- translation-of: {source_name} sha256:{digest} -->"
        new_text = text[: match.start()] + new_line + text[match.end() :]
        translation_path.write_bytes(new_text.encode("utf-8"))
        print(f"{translation_rel}: {old_digest} -> {digest}")
        return True
    return False


def update_digests(template_dir: Path) -> None:
    """Refresh every translation's source-marker digest in place.

    Only the ``<!-- translation-of: ... sha256:... -->`` line is rewritten;
    every other byte of the file is left untouched
    (tooling-delta.md §1.2).
    """
    any_updated = False
    for translation_rel, source_rel in sorted(find_translations(template_dir).items()):
        source_path = template_dir / source_rel
        if not source_path.is_file():
            # find_translations() registers a translation by filename
            # convention alone (tooling-delta.md §1.3); a missing source is
            # a C24 FAIL to be reported by check_template.py, not something
            # --update-digests can compute a digest for. Skip it here.
            print(
                f"{translation_rel}: skipped (source not found: {source_rel})"
            )
            continue
        translation_path = template_dir / translation_rel
        if _refresh_translation_digest(
            translation_path, translation_rel, source_path, Path(source_rel).name
        ):
            any_updated = True

    # tooling-delta-003.md §7: the workspace homepage's own translation
    # lives outside template/ and is refreshed through the very same
    # substitution helper as above -- not a second implementation.
    # Resolved relative to the repository root (never ctx.template_dir /
    # the *template_dir* parameter here), same rationale as check_c25 ~
    # check_c27. Silently skipped when the workspace translation does not
    # exist yet.
    repo_root = Path(__file__).resolve().parent.parent
    workspace_source = repo_root / WORKSPACE_SOURCE
    workspace_translation = repo_root / WORKSPACE_TRANSLATION
    if workspace_source.is_file() and workspace_translation.is_file():
        if _refresh_translation_digest(
            workspace_translation, WORKSPACE_TRANSLATION, workspace_source, WORKSPACE_SOURCE
        ):
            any_updated = True

    if not any_updated:
        print("No digest needed updating.")


CHECKS = {
    "C01": ("Layout", lambda ctx: check_c01(ctx)),
    "C02": ("No development files", lambda ctx: check_c02(ctx)),
    "C03": ("YAML parses", lambda ctx: check_c03(ctx)),
    "C04": ("Issue forms", lambda ctx: check_c04(ctx)),
    "C05": ("CI workflow", lambda ctx: check_c05(ctx)),
    "C06": ("Dependabot", lambda ctx: check_c06(ctx)),
    "C07": ("Release notes", lambda ctx: check_c07(ctx)),
    "C08": ("Placeholders", lambda ctx: check_c08(ctx)),
    "C09": ("Source comments", lambda ctx: check_c09(ctx)),
    "C10": ("Template identity isolation", lambda ctx: check_c10(ctx)),
    "C11": ("Language structure", lambda ctx: check_c11(ctx)),
    "C12": ("Selection list", lambda ctx: check_c12(ctx)),
    "C13": ("Cleanup simulation", lambda ctx: check_c13(ctx)),
    "C14": ("Relative links", lambda ctx: check_c14(ctx)),
    "C15": ("License", lambda ctx: check_c15(ctx)),
    "C16": ("Code of conduct", lambda ctx: check_c16(ctx)),
    "C17": ("Removal notes", lambda ctx: check_c17(ctx)),
    "C18": ("Maintenance guide", lambda ctx: check_c18(ctx)),
    "C19": ("Team upgrade guide", lambda ctx: check_c19(ctx)),
    "C20": ("Contributor documents", lambda ctx: check_c20(ctx)),
    "C21": ("Text format", lambda ctx: check_c21(ctx)),
    "C22": ("Removal simulation", lambda ctx: check_c22(ctx)),
    "C23": ("Contract parity", lambda ctx: check_c23(ctx)),
    "C24": ("Translation freshness", lambda ctx: check_c24(ctx)),
    "C25": ("Workspace language structure", lambda ctx: check_c25(ctx)),
    "C26": ("Workspace facts", lambda ctx: check_c26(ctx)),
    "C27": ("Workspace translation freshness", lambda ctx: check_c27(ctx)),
}


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check the Chef's Pick OSS Starter template directory."
    )
    parser.add_argument("--template-dir", default=None)
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--today", default=None)
    parser.add_argument("--only", default=None)
    parser.add_argument("--files", default=None)
    parser.add_argument("--update-digests", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.template_dir is None:
        template_dir = Path(__file__).resolve().parent.parent / "template"
    else:
        template_dir = Path(args.template_dir)

    if not template_dir.is_dir():
        print(f"error: template directory not found: {template_dir}", file=sys.stderr)
        return 2

    if args.update_digests:
        update_digests(template_dir)
        return 0

    if args.today is None:
        today = _dt.date.today()
    else:
        today = parse_date(args.today)
        if today is None:
            print(f"error: invalid --today value: {args.today}", file=sys.stderr)
            return 2

    if args.only is None:
        ids = list(CHECKS)
    else:
        ids = [x.strip() for x in args.only.split(",") if x.strip()]
        unknown = [x for x in ids if x not in CHECKS]
        if unknown:
            print(f"error: unknown check id(s): {', '.join(unknown)}", file=sys.stderr)
            return 2
        ids = [cid for cid in CHECKS if cid in ids]

    files = None
    if args.files is not None:
        files = {x.strip() for x in args.files.split(",") if x.strip()}

    ctx = Context(
        template_dir=template_dir, release=args.release, today=today, files=files
    )

    passed = failed = warned = skipped = 0
    for cid in ids:
        title, func = CHECKS[cid]
        try:
            problems = func(ctx)
        except SkipCheck as exc:
            print(f"SKIP {cid} {title}: {exc}")
            skipped += 1
            continue
        except WarnCheck as exc:
            problems = exc.args[0]
            # --release promotes a WARN to a FAIL (tooling-delta.md §1.1).
            if ctx.release:
                print(f"FAIL {cid} {title}")
                for problem in problems:
                    print(f"  - {problem}")
                failed += 1
            else:
                print(f"WARN {cid} {title}")
                for problem in problems:
                    print(f"  - {problem}")
                warned += 1
            continue
        if problems:
            print(f"FAIL {cid} {title}")
            for problem in problems:
                print(f"  - {problem}")
            failed += 1
        else:
            print(f"PASS {cid} {title}")
            passed += 1

    print(f"Summary: {passed} passed, {failed} failed, {warned} warned, {skipped} skipped")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
