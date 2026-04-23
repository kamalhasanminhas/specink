<div align="center">

<br/>

```
███████╗██████╗ ███████╗ ██████╗    ██╗███╗   ██╗██╗  ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝    ██║████╗  ██║██║ ██╔╝
███████╗██████╔╝█████╗  ██║         ██║██╔██╗ ██║█████╔╝
╚════██║██╔═══╝ ██╔══╝  ██║         ██║██║╚██╗██║██╔═██╗
███████║██║     ███████╗╚██████╗    ██║██║ ╚████║██║  ██╗
╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
```

### Spec-driven development with ink — every decision, written permanently.

**SpecInk adds the one thing missing from AI-assisted development: the ability to remember why.**

<br/>

[![PyPI version](https://img.shields.io/pypi/v/specink?color=0f172a&labelColor=e2e8f0&style=flat-square)](https://pypi.org/project/specink/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-0f172a?labelColor=e2e8f0&style=flat-square)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-0f172a?labelColor=e2e8f0&style=flat-square)](LICENSE)
[![Tests](https://img.shields.io/github/actions/workflow/status/kamalhasanminhas/specink/ci.yml?label=tests&color=0f172a&labelColor=e2e8f0&style=flat-square)](https://github.com/kamalhasanminhas/specink/actions)

</div>

---

## The problem

You're using Claude Code (or Cursor, or Copilot). The code is good. The sessions are fast. But six months later you open a module and think:

> *Why is it done this way? What did we consider? Where is the reasoning?*

It's gone. It lived in a chat thread that was cleared weeks ago.

Tools like [OpenSpec](https://github.com/Fission-AI/OpenSpec) solve the *what* — structured specs, proposals, task checklists. But nobody has solved the *why*.

SpecInk solves the why.

---

## What SpecInk adds

SpecInk is a companion to the OpenSpec/SDD workflow. If you've never heard of Spec-Driven Development, the idea is simple: **agree on what to build before any code is written**, in a structured Markdown file that lives in your repo alongside the code.

SpecInk keeps the same loop — `propose → apply → verify → archive` — but adds four features that no existing tool has:

| Feature | What it does |
|---|---|
| **Transcript logging** | Appends AI session output to `transcript.md` inside each change folder. The reasoning is preserved. Forever. |
| **Decision records** | `ink decision add` captures what was decided, why, and what alternatives were rejected — in an ADR-lite format. |
| **Drift detection** | After archive, `ink drift` checks whether your code still matches what the spec said it would do. |
| **Conflict preview** | Before you start implementing, `ink conflicts` tells you if two active changes are touching the same spec sections. |

---

## Install

```bash
pip install specink
```

Or with `uv`:

```bash
uv tool install specink
```

Requires Python 3.11+. No API keys. No SaaS. No database. Just Markdown files that live in your repo.

---

## Quick start

```bash
# 1. Initialise in your project
cd my-project
ink init

# 2. Propose a change
ink propose add-dark-mode

# 3. Fill in the spec (your AI assistant can do this)
#    .specink/changes/add-dark-mode/specs/spec.md

# 4. Check for conflicts with other active changes
ink conflicts

# 5. Implement the change (with your AI coding assistant)
ink apply add-dark-mode

# 6. Log the AI session transcript
echo "I used CSS variables on :root because..." | ink transcript append add-dark-mode

# 7. Record the key design decision
ink decision add add-dark-mode

# 8. Verify all tasks are done
ink verify add-dark-mode

# 9. Archive (runs drift check automatically)
ink archive add-dark-mode
```

---

## How it works

### Change folder anatomy

Every `ink propose` creates a structured folder:

```
.specink/changes/add-dark-mode/
├── proposal.md       ← why we're doing this, what's in scope
├── specs/
│   └── spec.md       ← BDD scenarios (GIVEN / WHEN / THEN)
├── design.md         ← technical approach, constraints
├── tasks.md          ← atomic implementation checklist
├── transcript.md     ← AI conversation log  ✦ new
└── decisions.md      ← ADR-lite decision records  ✦ new
```

Archived changes move to `.specink/changes/archive/YYYY-MM-DD-add-dark-mode/`. Nothing is deleted.

---

### Transcript logging

After your AI session, pipe the key reasoning into the change:

```bash
ink transcript append add-dark-mode --speaker assistant
# (type or paste, then Ctrl+D)

# Or from a file
ink transcript append add-dark-mode --file session.txt

# Read it back
ink transcript show add-dark-mode
```

The transcript is append-only with automatic timestamps:

```markdown
## 2025-01-23 14:32 — assistant

I chose CSS variables over Tailwind dark: prefix because the app needs
runtime switching without a rebuild. The ThemeProvider approach was
rejected because it adds a React dependency to a framework-agnostic module.

---
```

Three months later, when someone asks *why aren't we using styled-components here*, the answer is one command away.

---

### Decision records

Capture any significant design decision in under a minute:

```bash
ink decision add add-dark-mode
```

```
? Decision title:        Use CSS variables for theming
? What was decided:      Store all color tokens as CSS custom properties on :root
? Why:                   Allows runtime switching without a rebuild
? Alternatives rejected: Tailwind dark: prefix, styled-components ThemeProvider
```

Saved to `decisions.md` in a format your team can read, diff, and link to in PRs.

---

### Drift detection

Spec-to-code drift is silent and insidious. Six months after archiving a change, `ink drift` checks whether the code still matches what the spec said it would do:

```bash
ink drift add-dark-mode
```

```
Drift report for 'add-dark-mode' (archived 2025-01-20)

  ✓  ThemeProvider          found in src/theme.ts
  ✓  useColorScheme         found in src/hooks/useColorScheme.ts
  ✗  detectSystemPreference not found in any source file
  ⚠  toggleTheme            found only in tests/

2 spec assertions may have drifted from implementation.
Run `ink drift add-dark-mode --verbose` for file references.
```

No LLM required. Pure text parsing — fast enough to run in CI.

---

### Conflict preview

Before writing a line of code, know if two changes are going to fight each other at archive time:

```bash
ink conflicts
```

```
Active change conflict scan

  add-dark-mode  ×  add-theming
    └─ specs/ui/spec.md § "Color system"     (both modify)
    └─ design.md § "CSS architecture"        (both modify)

No conflicts in other active changes.
Tip: archive one change before applying the other.
```

---

## Works with your AI assistant

SpecInk writes an `AGENTS.md` to your project root on `ink init`. Every AI coding assistant that reads this file (Claude Code, Cursor, Windsurf, GitHub Copilot) will know how to navigate your change folders, log transcripts, and record decisions — without you having to re-explain the workflow each session.

The file is yours to edit. It's just Markdown.

---

## Command reference

```
ink init                               Initialise SpecInk in a project
ink propose <name>                     Create a new change proposal
ink apply [name]                       Mark a change as in progress
ink verify [name]                      Confirm all tasks are complete
ink archive [name]                     Archive a completed change
ink list                               Show all active changes
ink show <name>                        Show change details and artifact summary
ink status                             Git-style overview of all changes

ink transcript append <name>           Append to AI transcript
ink transcript show <name>             Display transcript with timestamps
ink decision add <name>                Record an architectural decision
ink decision list <name>               List all decisions for a change

ink drift [name]                       Check for spec-to-code drift
ink conflicts                          Scan active changes for spec conflicts
```

All commands accept `--verbose / -v` for detailed output.

---

## FAQ

**Does SpecInk call any LLM?**
No. Transcripts are written by you or your AI assistant — SpecInk just stores and displays them. Drift detection and conflict scanning are pure text parsing.

**Does it replace OpenSpec?**
No. It's a different philosophy — SpecInk is a standalone Python CLI. If you're already using OpenSpec's slash commands in Cursor or Claude Code, SpecInk's drift and conflict features work alongside them (they both just read Markdown files).

**Does it require a specific AI tool?**
No. It works with Claude Code, Cursor, Windsurf, Copilot, or any tool that can read files and run shell commands.

**Can I use it in CI?**
Yes. `ink drift` exits with code 1 if drift is detected, making it suitable as a CI check. All commands support `--no-interaction` for non-TTY environments.

---

## Comparison

| | SpecInk | OpenSpec | GitHub Spec Kit | Kiro |
|---|---|---|---|---|
| Transcript logging | ✅ | ❌ | ❌ | ❌ |
| Decision records (ADR-lite) | ✅ | ❌ | ❌ | ❌ |
| Drift detection | ✅ | ❌ | ❌ | ❌ |
| Conflict preview | ✅ | ❌ (archive only) | ❌ | ❌ |
| Works with any AI tool | ✅ | ✅ | ✅ | ❌ (IDE lock-in) |
| No API key required | ✅ | ✅ | ✅ | ❌ |
| Python / pip install | ✅ | ❌ (Node.js) | ❌ (Python, heavy) | ❌ (IDE plugin) |

---

## CI/CD & Deployment

The project uses GitHub Actions for continuous integration and deployment:

**CI Workflow** (runs on every push):
- Linting with `ruff`
- Type checking with `mypy`
- Tests with `pytest`
- Runs on Python 3.11 and 3.12

**Release Workflow** (runs on push to `main`):
- All CI checks
- Build package with `uv build`
- Publish to PyPI with `uv publish`

**To enable PyPI deployment:**
1. Generate a PyPI API token at https://pypi.org/manage/account/token/
2. Add it as a repository secret named `PYPI_TOKEN` in GitHub Settings → Secrets and variables → Actions

---

## Contributing

Contributions are welcome. Please read the [contributing guide](CONTRIBUTING.md) before opening a PR.

For larger features, run `ink propose <feature-name>` inside the SpecInk repo itself — it's only fair.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">
<sub>Built with ❤️ and too many cleared chat sessions. Leave your ink.</sub>
</div>
