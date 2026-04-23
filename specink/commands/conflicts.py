"""Conflicts command."""

import typer
from rich.console import Console

from specink.core.config import get_specink_root
from specink.core.conflicts import scan_conflicts

console = Console()


def conflicts_command(verbose: bool = False) -> None:
    """Scan active changes for spec conflicts."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project")
        raise typer.Exit(1)

    conflicts = scan_conflicts(specink_root)

    if not conflicts:
        console.print("[green]✓[/green] No conflicts in active changes")
        return

    console.print("[yellow]Active change conflict scan[/yellow]\n")

    grouped: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for c in conflicts:
        key = (c.change_a, c.change_b)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append((c.file_path, c.section))

    for (change_a, change_b), items in grouped.items():
        console.print(f"  [cyan]{change_a}[/cyan]  ×  [cyan]{change_b}[/cyan]")
        for file_path, section in items:
            console.print(f'    └─ {file_path} § "{section}"')
        console.print()

    console.print(
        "[dim]Tip: archive one change before applying the other, or coordinate the merge.[/dim]"
    )
