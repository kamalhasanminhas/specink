"""Init command."""

from pathlib import Path

import questionary
import typer
from rich.console import Console

from specink.core.config import Config

console = Console()

AGENTS_MD_TEMPLATE = """# SpecInk — AI assistant instructions

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
"""


def init_command() -> None:
    """Initialize SpecInk in the current project."""
    cwd = Path.cwd()
    specink_dir = cwd / ".specink"

    if specink_dir.exists():
        console.print("[yellow]⚠[/yellow] SpecInk already initialized in this project")
        raise typer.Exit(1)

    tool = questionary.select(
        "Which AI tool are you using?",
        choices=[
            "claude-code",
            "cursor",
            "windsurf",
            "copilot",
            "other",
        ],
        default="claude-code",
    ).ask()

    if tool is None:
        console.print("[red]✗[/red] Initialization cancelled")
        raise typer.Exit(1)

    specink_dir.mkdir()
    (specink_dir / "changes").mkdir()
    (specink_dir / "specs").mkdir()

    config = Config(tool=tool)
    config.save(specink_dir / "config.yaml")

    agents_md = cwd / "AGENTS.md"
    agents_md.write_text(AGENTS_MD_TEMPLATE)

    console.print(f"[green]✓[/green] Initialized SpecInk in {cwd}")
    console.print(f"[cyan]→[/cyan] Config: {specink_dir / 'config.yaml'}")
    console.print(f"[cyan]→[/cyan] AI instructions: {agents_md}")
