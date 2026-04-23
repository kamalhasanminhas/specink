"""Drift command."""


import typer
from rich.console import Console

from specink.core.change import get_change_path
from specink.core.config import get_specink_root
from specink.core.drift import check_drift

console = Console()


def drift_command(name: str | None = None, verbose: bool = False) -> None:
    """Check for spec-to-code drift."""
    specink_root = get_specink_root()
    if specink_root is None:
        console.print("[red]✗[/red] Not a SpecInk project")
        raise typer.Exit(1)

    if name is None:
        console.print("[yellow]⚠[/yellow] No change name provided")
        raise typer.Exit(1)

    change_path = get_change_path(specink_root, name)
    if change_path is None:
        console.print(f"[red]✗[/red] Change '{name}' not found")
        raise typer.Exit(1)

    project_root = specink_root.parent
    results = check_drift(change_path, project_root)

    if not results:
        console.print("[yellow]⚠[/yellow] No spec assertions to check")
        raise typer.Exit(0)

    console.print(f"Drift report for '{name}'\n")

    drift_count = 0
    for result in results:
        if result.status == "found":
            console.print(f"  [green]✓[/green]  {result.identifier:<30} found in {result.location}")
        elif result.status == "not_found":
            console.print(f"  [red]✗[/red]  {result.identifier:<30} not found in any source file")
            drift_count += 1
        elif result.status == "test_only":
            console.print(
                f"  [yellow]⚠[/yellow]  {result.identifier:<30} found only in {result.location}"
            )
            drift_count += 1

    if drift_count > 0:
        console.print(f"\n{drift_count} spec assertions may have drifted from implementation.")
        if not verbose:
            console.print(f"Run `ink drift {name} --verbose` for line references.")
        raise typer.Exit(1)
    else:
        console.print("\n[green]✓[/green] All spec assertions match the codebase")
