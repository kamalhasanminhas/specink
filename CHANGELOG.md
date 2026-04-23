# Changelog

All notable changes to SpecInk will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1a] - 2026-04-24

### Added
- GitHub Actions CI/CD pipeline with `uv` support
- CI workflow for lint and test on every push (Python 3.11 and 3.12)
- Release workflow for automated PyPI deployment
- CONTRIBUTING.md with development guidelines and workflow

### Fixed
- GitHub Actions badge in README now points to correct repo and workflow

## [0.1.0] - 2026-04-23

### Added
- Initial release of SpecInk
- Core commands:
  - `ink init` - Initialize SpecInk in a project
  - `ink propose` - Create new change proposals
  - `ink apply` - Mark changes as in progress
  - `ink verify` - Verify task completion
  - `ink archive` - Archive completed changes
- AI observability features:
  - `ink transcript append/show` - Log and view AI session transcripts
  - `ink decision add/list` - Record architectural decisions (ADR-lite)
  - `ink drift` - Detect spec-to-code drift
  - `ink conflicts` - Scan for overlapping spec sections
- Utility commands:
  - `ink list` - Show active changes
  - `ink show` - Display change details
  - `ink status` - Overview of project state
- Template files for proposals, specs, design, tasks, transcripts, decisions
- AGENTS.md generation for AI assistant integration
- Python 3.11+ support
- Zero external API dependencies

[0.1.0]: https://github.com/yourusername/specink/releases/tag/v0.1.0
