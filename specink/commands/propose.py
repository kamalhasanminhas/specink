"""Propose command."""

from pathlib import Path

import typer
from rich.console import Console

from specink.core.change import create_change, get_changes_dir
from specink.core.config import get_specink_root

console = Console()


def get_templates_dir() -> Path:
    """Get the templates directory."""
    return Path(__file__).parent.parent / "templates"


def propose_command(name: str, no_conflict_check: bool = False) -> None:
    """Create a new change proposal."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project. Run `ink init` first.")
        raise typer.Exit(1)

    changes_dir = get_changes_dir(specink_root)
    if (changes_dir / name).exists():
        console.print(f"[red]✗[/red] Change '{name}' already exists")
        raise typer.Exit(1)

    templates_dir = get_templates_dir()
    change_dir = create_change(specink_root, name, templates_dir)

    console.print(f"[green]✓[/green] Created change: {name}")
    console.print(f"[cyan]→[/cyan] Path: {change_dir}")
    console.print(f"[cyan]→[/cyan] Edit {change_dir / 'proposal.md'} to get started")
