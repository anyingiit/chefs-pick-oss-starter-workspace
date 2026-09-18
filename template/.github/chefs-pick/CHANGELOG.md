# Template changelog

This file records changes to the Chef's Pick OSS Starter template itself.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-09-18

### Added

- `README.zh-CN.md` and `SETUP.zh-CN.md`: Simplified Chinese editions of the front page and the setup checklist, each reached from a language selector at the top of its English original and each stating that the English edition governs on disagreement.

### Changed

- Documentation is now English-first: the guide layer is a single-language English edition, with Simplified Chinese supplied as separate `README.zh-CN.md` and `SETUP.zh-CN.md` files reached from a language selector. The previous side-by-side bilingual layout is gone. The reason is that an English canonical README with a separately-filed translation is what open-source projects overwhelmingly do, and a template that recommends community standards should follow them itself.
- The cleanup command now removes three paths rather than two, because the front page's translation sits outside `chefs-pick/` and has to be named explicitly. It is still a single command.

## [1.0.0] - 2026-09-18

### Added

- First version: 16 modules (M01–M16), the setup guide layer, and the selection list.
