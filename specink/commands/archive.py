"""Archive command."""

import typer
from rich.console import Console

from specink.core.change import archive_change
from specink.core.config import get_specink_root

console = Console()


def archive_command(name: str, no_drift_check: bool = False) -> None:
    """Archive a completed change."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project. Run `ink init` first.")
        raise typer.Exit(1)

    try:
        archived_path = archive_change(specink_root, name)
        console.print(f"[green]✓[/green] Archived: {name}")
        console.print(f"[cyan]→[/cyan] Location: {archived_path}")
    except FileNotFoundError as e:
        console.print(f"[red]✗[/red] {e}")
        raise typer.Exit(1)
