<!-- anchor: chefs-pick-oss-starter-workspace -->
# Chef's Pick OSS Starter — development workspace

**English** · [简体中文](README.zh-CN.md)

This is the development and maintenance workspace for the
[chefs-pick-oss-starter](https://github.com/anyingiit/chefs-pick-oss-starter)
template repository. The specification, selection research and validation tooling live
here; the template repository carries only the contents of `template/`.

<!-- anchor: layout -->
## Layout

| Path | What it is | Published |
|---|---|---|
| `template/` | Everything on the template repository's default branch | Yes |
| `specs/001-chefs-pick-starter/` | The original specification, plan, tasks, research and contracts | No |
| `specs/002-english-first-docs/` | The English-first documentation restructure | No |
| `specs/003-workspace-self-compliance/` | Holding this workspace to the rules it ships | No |
| `tools/` | Validation and data-refresh scripts, with their tests | No |
| `.specify/`, `.claude/` | Spec Kit and AI assistant configuration | No |

`template/` holds 28 files. **Only `template/` is ever published.** Check C02 rejects any
development file that finds its way into it.

<!-- anchor: common-commands -->
## Common commands

```bash
python3 tools/check_template.py              # 27 structural checks
python3 tools/check_template.py --release    # release gate; verification dates tighten to 30 days
python3 tools/check_template.py --update-digests  # refresh translation source markers
python3 -m unittest discover -s tools/tests  # unit tests
python3 tools/verify_sources.py              # dry-run refresh of the adoption data
python3 tools/verify_sources.py --write      # write the refreshed adoption data
```

Refreshing adoption data requires an authenticated `gh` CLI. The review cadence,
re-evaluation triggers and release gates are documented in
`template/.github/chefs-pick/MAINTAINING.md`.

<!-- anchor: publishing -->
## Publishing

Publishing means copying the contents of `template/` onto the default branch of the
template repository. Nothing else in this workspace is ever published. The full context is
in parts B, C and D of [quickstart.md](specs/001-chefs-pick-starter/quickstart.md).

Which steps apply depends on whether the template repository already has content.

**First publish, to a newly created empty repository.** Either copy the contents of
`template/` into a clone of the empty repository and commit, or run:

```bash
git subtree split --prefix=template -b publish
git push <template-remote> publish:main
```

**Every publish after that.** Work in a clone of the template repository and add a commit
on top of what is already there:

```bash
# Subsequent publish: replace the content inside a clone, add one commit
git -C <clone-path> fetch origin main
git -C <clone-path> checkout main
cp -a template/. <clone-path>/
git -C <clone-path> add -A
git -C <clone-path> commit -m "docs: sync template content"
git -C <clone-path> push origin main
```

After the copy and before the commit, the clone's working tree should be byte-identical to
`template/`; `diff -r --exclude=.git <clone-path> template` is the way to confirm it.

Three things to know, because getting them wrong damages the published repository:

- Never force-push to the template repository.
- A rejected push means the template repository has commits this workspace does not; stop and investigate rather than forcing.
- `git subtree split` produces a history with no common ancestor with the template repository, so it can only be pushed with `--force`. Use it for the first publish to an empty repository and never afterwards.

That last point is not hypothetical. The template repository carries a `v1.0.0` tag, and
force-pushing a split history would leave the commit that tag points at unreachable from
any branch.

Never merge a Dependabot pull request on the template repository directly — see the
"Action updates" section of MAINTAINING for why.

<!-- anchor: license -->
## License

MIT, same as the template repository. The template's own license and attribution notes are
in `template/.github/chefs-pick/LICENSE`.
