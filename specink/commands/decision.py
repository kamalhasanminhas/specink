"""Decision commands."""

import questionary
import typer
from rich.console import Console

from specink.core.change import get_change_path
from specink.core.config import get_specink_root
from specink.core.decisions import add_decision, list_decisions

console = Console()
app = typer.Typer()


@app.command("add")
def add(name: str = typer.Argument(..., help="Change name")) -> None:
    """Record an architectural decision."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project")
        raise typer.Exit(1)

    change_path = get_change_path(specink_root, name)
    if change_path is None:
        console.print(f"[red]✗[/red] Change '{name}' not found")
        raise typer.Exit(1)

    title = questionary.text("Decision title:").ask()
    if not title:
        console.print("[yellow]⚠[/yellow] Cancelled")
        raise typer.Exit(1)

    decided = questionary.text("What was decided:").ask()
    if not decided:
        console.print("[yellow]⚠[/yellow] Cancelled")
        raise typer.Exit(1)

    rationale = questionary.text("Why:").ask()
    if not rationale:
        console.print("[yellow]⚠[/yellow] Cancelled")
        raise typer.Exit(1)

    alternatives = questionary.text("Alternatives rejected:").ask()
    if not alternatives:
        alternatives = "None"

    add_decision(change_path, title, decided, rationale, alternatives)
    console.print(f"[green]✓[/green] Decision recorded for {name}")


@app.command("list")
def list_cmd(name: str = typer.Argument(..., help="Change name")) -> None:
    """List all decisions for a change."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project")
        raise typer.Exit(1)

    change_path = get_change_path(specink_root, name)
    if change_path is None:
        console.print(f"[red]✗[/red] Change '{name}' not found")
        raise typer.Exit(1)

    decisions = list_decisions(change_path)
    if not decisions:
        console.print("[yellow]⚠[/yellow] No decisions recorded")
        raise typer.Exit(0)

    console.print(f"[cyan]Decisions for {name}:[/cyan]")
    for i, title in enumerate(decisions, 1):
        console.print(f"  {i}. {title}")
