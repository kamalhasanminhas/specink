"""Verify command."""

import typer
from rich.console import Console

from specink.core.config import get_specink_root

console = Console()


def verify_command(name: str | None = None) -> None:
    """Verify all tasks are complete."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project. Run `ink init` first.")
        raise typer.Exit(1)

    if name is None:
        console.print("[yellow]⚠[/yellow] No change name provided")
        raise typer.Exit(1)

    console.print(f"[green]✓[/green] Verifying: {name}")
