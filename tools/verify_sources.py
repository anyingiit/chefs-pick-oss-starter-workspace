#!/usr/bin/env python3
"""Refresh the adoption data in the Chef's Pick OSS Starter selection list.

Reads the machine-readable table in ``SOURCES.md``, queries each repository
through the ``gh`` CLI, reports what changed, and with ``--write`` updates the
selection list and the template home page.  See
``specs/001-chefs-pick-starter/contracts/tooling.md`` §2 for the contract.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SOURCES_REL = ".github/chefs-pick/SOURCES.md"
README_REL = ".github/README.md"
UPGRADE_REL = ".github/chefs-pick/UPGRADE-TO-TEAM.md"

ADOPTION_START = "<!-- adoption-data:start -->"
ADOPTION_END = "<!-- adoption-data:end -->"
SUMMARY_START = "<!-- summary:start -->"
SUMMARY_END = "<!-- summary:end -->"

TABLE_HEADER = "| Repo | Stars | Forks | Last commit | License | Archived | Verified |"
TABLE_SEP = "|---|---:|---:|---|---|---|---|"

STAR_RE = re.compile(r"★ ([\d,]+) \(([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\)")
DATA_VERIFIED_RE = re.compile(r"(数据核实日期 / Data verified:\s*)(\d{4}-\d{2}-\d{2})")
VERIFIED_CELL_RE = re.compile(r"(\|\s*核实日期 / Verified\s*\|\s*)(\d{4}-\d{2}-\d{2})(\s*\|)")

STALE_DAYS = 365

REMINDER = (
    "Also re-check non-repository evidence manually: official platform "
    "features and the Contributor Covenant adopters list."
)


def gh_ready() -> bool:
    """True when the ``gh`` CLI is installed and logged in."""
    if shutil.which("gh") is None:
        return False
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def parse_adoption_table(text: str) -> list[dict]:
    """Return one dict per data row of the adoption table, in table order."""
    if ADOPTION_START not in text or ADOPTION_END not in text:
        return []
    body = text.split(ADOPTION_START, 1)[1].split(ADOPTION_END, 1)[0]
    rows = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) != 7:
            continue
        if cells[0] == "Repo":
            continue
        if all(c and set(c) <= set("-: ") for c in cells):
            continue
        rows.append(
            {
                "repo": cells[0],
                "stars": cells[1],
                "forks": cells[2],
                "last_commit": cells[3],
                "license": cells[4],
                "archived": cells[5],
                "verified": cells[6],
            }
        )
    return rows


def render_adoption_table(rows: list[dict]) -> str:
    """Render rows back into the table markdown (no adoption-data markers)."""
    lines = [TABLE_HEADER, TABLE_SEP]
    for row in rows:
        lines.append(
            f"| {row['repo']} | {row['stars']} | {row['forks']} | "
            f"{row['last_commit']} | {row['license']} | {row['archived']} | "
            f"{row['verified']} |"
        )
    return "\n".join(lines)


def _gh_json(path: str):
    result = subprocess.run(
        ["gh", "api", path],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def fetch_repo(slug: str) -> dict:
    """Query one repository. Uses the default branch's last commit, not pushed_at."""
    info = _gh_json(f"repos/{slug}")
    default_branch = info.get("default_branch") or "main"
    commit = _gh_json(f"repos/{slug}/commits/{default_branch}")
    date = (commit.get("commit") or {}).get("committer", {}).get("date", "")
    spdx = ((info.get("license") or {}) or {}).get("spdx_id")
    if not spdx or spdx == "NOASSERTION":
        spdx = "unknown"
    return {
        "full_name": info.get("full_name", slug),
        "stars": info.get("stargazers_count", 0),
        "forks": info.get("forks_count", 0),
        "last_commit": date[:10],
        "license": spdx,
        "archived": bool(info.get("archived")),
    }


def apply_updates(files: dict[str, str], results: dict, today: _dt.date) -> dict[str, str]:
    """Rewrite the table, the star counts and the four verification dates."""
    out = dict(files)
    stamp = today.isoformat()

    # 1. The adoption table, row order unchanged.
    sources = out.get(SOURCES_REL, "")
    rows = parse_adoption_table(sources)
    for row in rows:
        data = results.get(row["repo"])
        if not data:
            continue
        row["stars"] = f"{data['stars']:,}"
        row["forks"] = f"{data['forks']:,}"
        row["last_commit"] = data["last_commit"]
        row["license"] = data["license"]
        row["archived"] = "yes" if data["archived"] else "no"
        row["verified"] = stamp
    if rows and ADOPTION_START in sources:
        head, rest = sources.split(ADOPTION_START, 1)
        _body, tail = rest.split(ADOPTION_END, 1)
        sources = (
            head
            + ADOPTION_START
            + "\n"
            + render_adoption_table(rows)
            + "\n"
            + ADOPTION_END
            + tail
        )
        out[SOURCES_REL] = sources

    # 2. Every "★ N (slug)" reference.
    stars_by_repo = {slug: f"{data['stars']:,}" for slug, data in results.items()}

    def replace_star(match: re.Match) -> str:
        repo = match.group(2)
        if repo in stars_by_repo:
            return f"★ {stars_by_repo[repo]} ({repo})"
        return match.group(0)

    for rel in (README_REL, SOURCES_REL, UPGRADE_REL):
        if rel in out:
            out[rel] = STAR_RE.sub(replace_star, out[rel])

    # 3 and 4. The verification dates.
    if SOURCES_REL in out:
        text = DATA_VERIFIED_RE.sub(lambda m: m.group(1) + stamp, out[SOURCES_REL])
        text = VERIFIED_CELL_RE.sub(lambda m: m.group(1) + stamp + m.group(3), text)
        out[SOURCES_REL] = text

    if README_REL in out:
        out[README_REL] = _update_summary_dates(out[README_REL], stamp)

    return out


def _update_summary_dates(text: str, stamp: str) -> str:
    """Rewrite the last column of every data row in the home page summary table."""
    if SUMMARY_START not in text or SUMMARY_END not in text:
        return text
    head, rest = text.split(SUMMARY_START, 1)
    body, tail = rest.split(SUMMARY_END, 1)
    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and re.search(r"\d{4}-\d{2}-\d{2}\s*\|\s*$", stripped):
            line = re.sub(r"\d{4}-\d{2}-\d{2}(\s*\|\s*)$", stamp + r"\1", line)
        lines.append(line)
    return head + SUMMARY_START + "\n".join(lines) + SUMMARY_END + tail


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Refresh the adoption data in the selection list."
    )
    parser.add_argument("--template-dir", default=None)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--today", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.template_dir is None:
        template_dir = Path(__file__).resolve().parent.parent / "template"
    else:
        template_dir = Path(args.template_dir)

    today = (
        _dt.date.fromisoformat(args.today) if args.today else _dt.date.today()
    )

    if not gh_ready():
        print(
            "error: the gh CLI is not installed or not logged in "
            "(run `gh auth login`)",
            file=sys.stderr,
        )
        return 2

    sources_path = template_dir / SOURCES_REL
    if not sources_path.is_file():
        print(f"error: not found: {sources_path}", file=sys.stderr)
        return 2

    files = {SOURCES_REL: sources_path.read_text(encoding="utf-8")}
    for rel in (README_REL, UPGRADE_REL):
        path = template_dir / rel
        if path.is_file():
            files[rel] = path.read_text(encoding="utf-8")

    rows = parse_adoption_table(files[SOURCES_REL])
    results: dict[str, dict] = {}
    failed: list[str] = []

    for row in rows:
        slug = row["repo"]
        try:
            data = fetch_repo(slug)
        except Exception as exc:  # noqa: BLE001 - reported, then counted as failure
            failed.append(slug)
            print(f"{slug}: lookup failed: {exc}")
            continue
        results[slug] = data

        flags = []
        last = data["last_commit"]
        date = None
        try:
            date = _dt.date.fromisoformat(last)
        except ValueError:
            pass
        if date and (today - date).days > STALE_DAYS:
            flags.append("STALE")
        if data["archived"]:
            flags.append("ARCHIVED")
        if data["full_name"].lower() != slug.lower():
            flags.append(f"RENAMED→{data['full_name']}")

        print(
            f"{slug}: stars {row['stars']}→{data['stars']:,} "
            f"forks {row['forks']}→{data['forks']:,} "
            f"last_commit {last} license {data['license']} "
            f"archived {'yes' if data['archived'] else 'no'}"
            + (" " + " ".join(flags) if flags else "")
        )

    print(REMINDER)

    if failed:
        print(
            f"error: {len(failed)} repository lookup(s) failed; nothing was written",
            file=sys.stderr,
        )
        return 1

    if args.write:
        updated = apply_updates(files, results, today)
        for rel, text in updated.items():
            (template_dir / rel).write_text(text, encoding="utf-8")
        print(f"Wrote {len(updated)} file(s).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
