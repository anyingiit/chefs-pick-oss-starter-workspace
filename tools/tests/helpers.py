"""Shared helpers for the check_template test suite.

No test cases live here.  See
``specs/001-chefs-pick-starter/contracts/tooling.md`` §3.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_template as ct  # noqa: E402


def write_tree(root, files: dict[str, str]) -> Path:
    """Write ``{relative path: text}`` under *root*, creating parents."""
    root = Path(root)
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


def make_ctx(root, **kw) -> "ct.Context":
    """Build a Context for *root*; keyword args override the defaults."""
    kwargs = {"template_dir": Path(root)}
    if "files" in kw and kw["files"] is not None and not isinstance(kw["files"], set):
        kw["files"] = set(kw["files"])
    kwargs.update(kw)
    return ct.Context(**kwargs)


def run_one(check_id: str, ctx) -> tuple[str, list[str]]:
    """Run one check; return ``("PASS"|"FAIL"|"SKIP", problems_or_reason)``."""
    _title, func = ct.CHECKS[check_id]
    try:
        problems = func(ctx)
    except ct.SkipCheck as exc:
        return "SKIP", [str(exc)]
    return ("FAIL" if problems else "PASS"), problems
