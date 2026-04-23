"""List command."""

import typer
from rich.console import Console
from rich.table import Table

from specink.core.change import list_active_changes
from specink.core.config import get_specink_root

console = Console()


def list_command() -> None:
    """Show all active changes."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project")
        raise typer.Exit(1)

    active = list_active_changes(specink_root)

    if not active:
        console.print("[yellow]⚠[/yellow] No active changes")
        return

    table = Table(title="Active Changes")
    table.add_column("Name", style="cyan")

    for change in sorted(active):
        table.add_row(change)

    console.print(table)
