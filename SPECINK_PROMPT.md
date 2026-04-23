# SpecInk — SDD System Prompt for Claude

You are building **SpecInk**, a Python CLI tool for Spec-Driven Development (SDD) that extends the OpenSpec workflow with AI observability features that OpenSpec does not have: transcript logging, decision rationale capture, spec drift detection, and cross-change conflict preview.

---

## Project identity

- **Name**: SpecInk
- **Tagline**: "Spec-driven development with ink — every decision, written permanently."
- **Language**: Python 3.11+
- **Package manager**: `uv` (preferred) or `pip`
- **Distribution**: PyPI package named `specink`, CLI command `ink`
- **License**: MIT
- **Target users**: Solo developers and small teams using AI coding assistants (Claude Code, Cursor, Windsurf, Copilot) who want reproducible, auditable AI-assisted development

---

## Philosophy

SpecInk follows the same SDD loop as OpenSpec (`propose → apply → verify → archive`) but adds a **memory layer** that no other tool has:

1. Every AI session leaves a `transcript.md` artifact alongside the spec files
2. Every design decision leaves a `decisions.md` (ADR-lite) recording what was chosen and what was rejected
3. After archive, a drift checker can flag when code diverges from the spec
4. Before apply, a conflict scanner flags overlapping spec sections across active changes

The tool is intentionally lightweight: Markdown files, Git-friendly, no database, no SaaS, no API keys required for core features.

---

## Folder structure to generate

```
specink/
├── specink/
│   ├── __init__.py
│   ├── cli.py                  # Typer CLI entrypoint
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── init.py             # `ink init`
│   │   ├── propose.py          # `ink propose <name>`
│   │   ├── apply.py            # `ink apply [name]`
│   │   ├── verify.py           # `ink verify [name]`
│   │   ├── archive.py          # `ink archive [name]`
│   │   ├── transcript.py       # `ink transcript append|show`
│   │   ├── decision.py         # `ink decision add|list`
│   │   ├── drift.py            # `ink drift [name]`
│   │   └── conflicts.py        # `ink conflicts`
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Load/save .specink/config.yaml
│   │   ├── change.py           # Change folder CRUD
│   │   ├── spec.py             # Spec file parsing (sections, scenarios)
│   │   ├── transcript.py       # Transcript append/read logic
│   │   ├── decisions.py        # ADR record logic
│   │   ├── drift.py            # Drift detection engine
│   │   └── conflicts.py        # Conflict scanner engine
│   └── templates/
│       ├── proposal.md
│       ├── spec.md
│       ├── design.md
│       ├── tasks.md
│       ├── transcript.md
│       └── decisions.md
├── tests/
│   ├── __init__.py
│   ├── test_change.py
│   ├── test_spec.py
│   ├── test_drift.py
│   └── test_conflicts.py
├── pyproject.toml
├── README.md
├── CHANGELOG.md
└── .specink/                # Created at runtime by `ink init`
```

---

## Spec: change folder anatomy

Every `ink propose <name>` creates:

```
.specink/changes/<name>/
├── proposal.md       # Why, what, scope
├── specs/
│   └── spec.md       # Requirements + BDD scenarios (GIVEN/WHEN/THEN)
├── design.md         # Technical approach, constraints
├── tasks.md          # Atomic implementation checklist [ ] items
├── transcript.md     # AI conversation log (append-only, auto-timestamped)
└── decisions.md      # ADR-lite records: decision, rationale, alternatives rejected
```

Archived changes move to `.specink/changes/archive/YYYY-MM-DD-<name>/`.

---

## Feature specs

### Feature 1: `ink init`

**GIVEN** a project directory  
**WHEN** the user runs `ink init`  
**THEN** `.specink/` is created with `config.yaml` and `specs/` directory  
**AND** an `AGENTS.md` file is written to the project root with SpecInk workflow instructions for AI assistants  
**AND** the user is asked to confirm the AI tool they use (Claude Code / Cursor / Windsurf / Copilot / Other)

Config schema (`config.yaml`):
```yaml
version: "1"
tool: claude-code          # detected AI tool
drift_check: true          # enable drift detection on archive
conflict_check: true       # enable conflict scan on propose
transcript_auto: true      # auto-append transcript on every session
created_at: "2025-01-01T00:00:00Z"
```

---

### Feature 2: `ink propose <name>`

**GIVEN** an initialised project  
**WHEN** the user runs `ink propose add-dark-mode`  
**THEN** `.specink/changes/add-dark-mode/` is created with all 6 artifact files pre-filled from templates  
**AND** if `conflict_check: true`, SpecInk scans active changes for spec section overlaps and prints a warning if any are found  
**AND** the path to the change folder is printed so the AI can reference it

Conflict check output (if conflicts found):
```
⚠  Conflict detected: specs/ui/spec.md is also modified in active change 'add-theming'
   Review before applying to avoid merge conflicts at archive.
```

---

### Feature 3: `ink transcript append`

**GIVEN** an active change  
**WHEN** the user pipes or passes AI session output  
**THEN** a timestamped entry is appended to `transcript.md`  
**AND** the speaker (human / assistant) is inferred from the `--speaker` flag (default: `assistant`)

```bash
# Append a block from stdin
echo "Here is my plan for the dark mode implementation..." | ink transcript append add-dark-mode

# Append from a file
ink transcript append add-dark-mode --file session.txt --speaker human

# Show the transcript
ink transcript show add-dark-mode
```

Transcript format in `transcript.md`:
```markdown
## 2025-01-23 14:32 — assistant

Here is my plan for the dark mode implementation...

---

## 2025-01-23 14:35 — human

Can you also handle system preference detection?

---
```

---

### Feature 4: `ink decision add`

**GIVEN** an active change  
**WHEN** the user runs `ink decision add <change-name>`  
**THEN** an interactive prompt collects: decision title, what was decided, why, and alternatives rejected  
**AND** a new ADR entry is appended to `decisions.md`

```bash
ink decision add add-dark-mode
# Prompts:
#   Decision title: Use CSS variables for theming
#   What was decided: Store all color tokens as CSS custom properties on :root
#   Why: Allows runtime switching without JS class toggling
#   Alternatives rejected: Tailwind dark: prefix, styled-components ThemeProvider
```

`decisions.md` format:
```markdown
## Decision: Use CSS variables for theming
**Date**: 2025-01-23  
**Status**: Accepted

### What was decided
Store all color tokens as CSS custom properties on `:root`.

### Rationale
Allows runtime switching without JS class toggling. Works with any framework.

### Alternatives rejected
- **Tailwind `dark:` prefix** — requires rebuild on theme switch
- **styled-components ThemeProvider** — adds runtime JS dependency

---
```

---

### Feature 5: `ink drift`

**GIVEN** an archived change with a `specs/spec.md` containing BDD scenarios  
**WHEN** the user runs `ink drift` (or it runs automatically post-archive if `drift_check: true`)  
**THEN** SpecInk scans the project source files for function/class names mentioned in spec scenarios  
**AND** prints a drift report showing which spec assertions have no matching code symbol

Algorithm:
1. Parse `specs/spec.md` for `THEN` lines — extract quoted identifiers and `PascalCase`/`snake_case` tokens
2. Recursively grep source files (`*.py`, `*.ts`, `*.js`, `*.go`, `*.rs`) for those tokens
3. Report: ✓ found / ✗ not found / ⚠ ambiguous (found in test only)

Output:
```
Drift report for 'add-dark-mode' (archived 2025-01-20)
  ✓  ThemeProvider       found in src/theme.ts
  ✓  useColorScheme      found in src/hooks/useColorScheme.ts
  ✗  detectSystemPreference  not found in any source file
  ⚠  toggleTheme         found only in tests/theme.test.ts

2 spec assertions may have drifted from implementation.
Run `ink drift add-dark-mode --verbose` for line references.
```

---

### Feature 6: `ink conflicts`

**GIVEN** 2 or more active (non-archived) changes  
**WHEN** the user runs `ink conflicts`  
**THEN** SpecInk parses each change's `specs/spec.md` and `design.md`  
**AND** identifies section headings that appear in more than one change  
**AND** prints a conflict matrix

Output:
```
Active change conflict scan
  add-dark-mode  ×  add-theming
    └─ specs/ui/spec.md § "Color system"   (both modify)
    └─ design.md § "CSS architecture"      (both modify)

No conflicts in other active changes.
Tip: archive one change before applying the other, or coordinate the merge.
```

---

## CLI design (Typer)

```python
# All commands use Typer with rich output (Rich library)
# Color scheme: green = success, yellow = warning, red = error, cyan = info
# All commands accept --verbose / -v flag
# All commands accept --change / -c to target a specific change by name

ink init
ink propose <name> [--no-conflict-check]
ink apply [name]
ink verify [name]
ink archive [name] [--no-drift-check]
ink transcript append <name> [--speaker human|assistant] [--file PATH]
ink transcript show <name> [--tail N]
ink decision add <name>
ink decision list <name>
ink drift [name] [--verbose]
ink conflicts [--verbose]
ink list                          # show all active changes with status
ink show <name>                   # show change details (all artifacts summary)
ink status                        # git-style status: active changes, drift alerts
```

---

## Dependencies

```toml
[project]
name = "specink"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.12",
    "rich>=13",
    "pyyaml>=6",
    "questionary>=2",    # interactive prompts for `ink decision add`
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-tmp-path", "ruff", "mypy"]

[project.scripts]
ink = "specink.cli:app"
```

---

## AGENTS.md template

When `ink init` runs, write this to the project root:

```markdown
# SpecInk — AI assistant instructions

This project uses SpecInk for Spec-Driven Development.
All changes follow the workflow: propose → apply → verify → archive.

## Active changes
Run `ink list` to see all active changes and their current state.

## Starting a new feature
1. Run `ink propose <name>` to create the change folder
2. Review and edit `.specink/changes/<name>/proposal.md`
3. Fill in `.specink/changes/<name>/specs/spec.md` with BDD scenarios
4. Fill in `.specink/changes/<name>/design.md` with technical approach
5. Break work into tasks in `.specink/changes/<name>/tasks.md`

## Logging your session
Append key decisions and reasoning to the transcript:
`ink transcript append <name> --speaker assistant`

## Recording design decisions
When you choose one approach over alternatives, record it:
`ink decision add <name>`

## Finishing a change
Run `ink verify <name>` to confirm all tasks are complete.
Run `ink archive <name>` to merge specs into `.specink/specs/` and archive.

## Checking for drift
Run `ink drift` to check if archived specs match the current codebase.
```

---

## Development constraints

- All file I/O must be tested with `tmp_path` pytest fixtures — no real filesystem side effects in tests
- Drift detection must work without any LLM — pure text parsing only
- Conflict detection must work without any LLM — pure Markdown heading comparison
- The `transcript append` command must be pipeable (read from stdin when no `--file`)
- All output uses `rich` — no bare `print()` calls
- Type annotations on every function
- `ruff` for linting, `mypy --strict` for type checking
- Python 3.11 minimum — use `tomllib` from stdlib (no `tomli` dependency)

---

## Implementation order (follow this sequence)

1. `pyproject.toml` + package scaffold
2. `core/config.py` — load/save config
3. `core/change.py` — create/read/archive change folders
4. `core/spec.py` — parse spec files (sections, THEN lines)
5. `commands/init.py` + `commands/propose.py` + `commands/archive.py`
6. `core/transcript.py` + `commands/transcript.py`
7. `core/decisions.py` + `commands/decision.py`
8. `core/conflicts.py` + `commands/conflicts.py`
9. `core/drift.py` + `commands/drift.py`
10. `commands/list.py`, `commands/show.py`, `commands/status.py`
11. Full test suite
12. README, CHANGELOG

---

## Quality gates before each commit

- [ ] `ruff check .` passes with zero warnings
- [ ] `mypy --strict specink/` passes
- [ ] `pytest -q` passes with 100% of existing tests green
- [ ] New feature has at least 3 tests: happy path, edge case, error path
- [ ] `ink --help` renders correctly in terminal

---

## What SpecInk does NOT do

- Does not call any LLM API (transcripts are written by the user/agent, not generated)
- Does not require a GitHub account or any hosted service
- Does not replace your AI coding assistant — it runs alongside it
- Does not enforce rigid phase gates — all commands work in any order
