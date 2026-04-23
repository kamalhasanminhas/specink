"""CLI entrypoint for SpecInk."""

import typer
from rich.console import Console

from specink import __version__
from specink.commands.apply import apply_command
from specink.commands.archive import archive_command
from specink.commands.conflicts import conflicts_command
from specink.commands.decision import app as decision_app
from specink.commands.drift import drift_command
from specink.commands.init import init_command
from specink.commands.list import list_command
from specink.commands.propose import propose_command
from specink.commands.show import show_command
from specink.commands.status import status_command
from specink.commands.transcript import app as transcript_app
from specink.commands.verify import verify_command

app = typer.Typer(
    name="ink",
    help="SpecInk: Spec-driven development with AI observability",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"SpecInk version {__version__}")


@app.command("init")
def init() -> None:
    """Initialize SpecInk in the current project."""
    init_command()


@app.command("propose")
def propose(
    name: str = typer.Argument(..., help="Name of the change"),
    no_conflict_check: bool = typer.Option(False, "--no-conflict-check"),
) -> None:
    """Create a new change proposal."""
    propose_command(name, no_conflict_check)


@app.command("apply")
def apply(name: str | None = typer.Argument(None, help="Name of the change")) -> None:
    """Mark a change as in progress."""
    apply_command(name)


@app.command("verify")
def verify(name: str | None = typer.Argument(None, help="Name of the change")) -> None:
    """Verify all tasks are complete."""
    verify_command(name)


@app.command("archive")
def archive(
    name: str = typer.Argument(..., help="Name of the change"),
    no_drift_check: bool = typer.Option(False, "--no-drift-check"),
) -> None:
    """Archive a completed change."""
    archive_command(name, no_drift_check)


app.add_typer(transcript_app, name="transcript")
app.add_typer(decision_app, name="decision")


@app.command("conflicts")
def conflicts(verbose: bool = typer.Option(False, "--verbose", "-v")) -> None:
    """Scan active changes for spec conflicts."""
    conflicts_command(verbose)


@app.command("drift")
def drift(
    name: str | None = typer.Argument(None, help="Change name"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Check for spec-to-code drift."""
    drift_command(name, verbose)


@app.command("list")
def list_changes() -> None:
    """Show all active changes."""
    list_command()


@app.command("show")
def show(name: str = typer.Argument(..., help="Change name")) -> None:
    """Show change details and artifact summary."""
    show_command(name)


@app.command("status")
def status() -> None:
    """Git-style status overview."""
    status_command()


def main() -> None:
    """Main entrypoint."""
    app()


if __name__ == "__main__":
    main()
