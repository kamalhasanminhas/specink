"""Show command."""

import typer
from rich.console import Console

from specink.core.change import get_change_path
from specink.core.config import get_specink_root

console = Console()


def show_command(name: str) -> None:
    """Show change details and artifact summary."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project")
        raise typer.Exit(1)

    change_path = get_change_path(specink_root, name)
    if change_path is None:
        console.print(f"[red]✗[/red] Change '{name}' not found")
        raise typer.Exit(1)

    console.print(f"[cyan]Change: {name}[/cyan]")
    console.print(f"[dim]Path: {change_path}[/dim]\n")

    artifacts = [
        "proposal.md",
        "specs/spec.md",
        "design.md",
        "tasks.md",
        "transcript.md",
        "decisions.md",
    ]

    for artifact in artifacts:
        artifact_path = change_path / artifact
        if artifact_path.exists():
            content = artifact_path.read_text()
            preview = content[:200].replace("\n", " ")
            console.print(f"[green]✓[/green] {artifact} ({len(content)} bytes)")
            if len(content) > 0:
                console.print(f"  [dim]{preview}...[/dim]")
        else:
            console.print(f"[red]✗[/red] {artifact} (missing)")
