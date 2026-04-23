"""Transcript commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown

from specink.core.change import get_change_path
from specink.core.config import get_specink_root
from specink.core.transcript import append_transcript, read_stdin, read_transcript

console = Console()
app = typer.Typer()


@app.command("append")
def append(
    name: str = typer.Argument(..., help="Change name"),
    speaker: str = typer.Option("assistant", "--speaker", help="Speaker (human/assistant)"),
    file: Path | None = typer.Option(None, "--file", help="Read from file instead of stdin"),
) -> None:
    """Append to the transcript."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project")
        raise typer.Exit(1)

    change_path = get_change_path(specink_root, name)
    if change_path is None:
        console.print(f"[red]✗[/red] Change '{name}' not found")
        raise typer.Exit(1)

    if file is not None:
        content = file.read_text()
    else:
        content = read_stdin()

    if not content.strip():
        console.print("[yellow]⚠[/yellow] No content to append")
        raise typer.Exit(1)

    append_transcript(change_path, content, speaker)
    console.print(f"[green]✓[/green] Appended to transcript for {name}")


@app.command("show")
def show(
    name: str = typer.Argument(..., help="Change name"),
    tail: int | None = typer.Option(None, "--tail", help="Show last N lines"),
) -> None:
    """Show the transcript."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project")
        raise typer.Exit(1)

    change_path = get_change_path(specink_root, name)
    if change_path is None:
        console.print(f"[red]✗[/red] Change '{name}' not found")
        raise typer.Exit(1)

    content = read_transcript(change_path, tail)
    if not content.strip():
        console.print("[yellow]⚠[/yellow] No transcript entries")
        raise typer.Exit(0)

    console.print(Markdown(content))
