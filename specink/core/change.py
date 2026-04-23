"""Change folder management."""

import shutil
from datetime import datetime
from pathlib import Path


def get_changes_dir(specink_root: Path) -> Path:
    """Get the changes directory."""
    return specink_root / "changes"


def get_archive_dir(specink_root: Path) -> Path:
    """Get the archive directory."""
    return get_changes_dir(specink_root) / "archive"


def list_active_changes(specink_root: Path) -> list[str]:
    """List all active (non-archived) change names."""
    changes_dir = get_changes_dir(specink_root)
    if not changes_dir.exists():
        return []

    return [d.name for d in changes_dir.iterdir() if d.is_dir() and d.name != "archive"]


def list_archived_changes(specink_root: Path) -> list[str]:
    """List all archived change names."""
    archive_dir = get_archive_dir(specink_root)
    if not archive_dir.exists():
        return []

    return [d.name for d in archive_dir.iterdir() if d.is_dir()]


def get_change_path(specink_root: Path, name: str) -> Path | None:
    """Get path to a change folder (active or archived)."""
    active_path = get_changes_dir(specink_root) / name
    if active_path.is_dir():
        return active_path

    for archived in list_archived_changes(specink_root):
        if archived.endswith(f"-{name}"):
            return get_archive_dir(specink_root) / archived

    return None


def create_change(specink_root: Path, name: str, templates_dir: Path) -> Path:
    """Create a new change folder with template files."""
    change_dir = get_changes_dir(specink_root) / name
    change_dir.mkdir(parents=True, exist_ok=False)

    (change_dir / "specs").mkdir(exist_ok=True)

    for template_name in [
        "proposal.md",
        "design.md",
        "tasks.md",
        "transcript.md",
        "decisions.md",
    ]:
        template_path = templates_dir / template_name
        dest_path = change_dir / template_name
        if template_path.exists():
            shutil.copy(template_path, dest_path)
        else:
            dest_path.write_text("")

    spec_template = templates_dir / "spec.md"
    spec_dest = change_dir / "specs" / "spec.md"
    if spec_template.exists():
        shutil.copy(spec_template, spec_dest)
    else:
        spec_dest.write_text("")

    return change_dir


def archive_change(specink_root: Path, name: str) -> Path:
    """Archive an active change by moving it to archive with timestamp."""
    active_path = get_changes_dir(specink_root) / name
    if not active_path.is_dir():
        raise FileNotFoundError(f"Active change '{name}' not found")

    archive_dir = get_archive_dir(specink_root)
    archive_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d")
    archived_name = f"{timestamp}-{name}"
    archived_path = archive_dir / archived_name

    shutil.move(str(active_path), str(archived_path))
    return archived_path
