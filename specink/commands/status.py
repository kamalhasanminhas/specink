"""Status command."""

import typer
from rich.console import Console

from specink.core.change import list_active_changes, list_archived_changes
from specink.core.config import get_specink_root

console = Console()


def status_command() -> None:
    """Git-style status overview."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project")
        raise typer.Exit(1)

    active = list_active_changes(specink_root)
    archived = list_archived_changes(specink_root)

    console.print("[cyan]SpecInk Status[/cyan]\n")

    if active:
        console.print(f"[green]Active changes ({len(active)}):[/green]")
        for change in sorted(active):
            console.print(f"  • {change}")
        console.print()

    if archived:
        console.print(f"[dim]Archived changes ({len(archived)}):[/dim]")
        for change in sorted(archived)[:5]:
            console.print(f"  [dim]• {change}[/dim]")
        if len(archived) > 5:
            console.print(f"  [dim]... and {len(archived) - 5} more[/dim]")
        console.print()

    if not active and not archived:
        console.print("[yellow]⚠[/yellow] No changes yet. Run `ink propose <name>` to start.")
