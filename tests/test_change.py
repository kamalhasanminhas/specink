"""Tests for change module."""

from pathlib import Path

from specink.core.change import (
    archive_change,
    create_change,
    get_change_path,
    list_active_changes,
)


def test_create_change(tmp_path: Path) -> None:
    """create_change creates folder with required files."""
    specink_root = tmp_path / ".specink"
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()

    (templates_dir / "proposal.md").write_text("# Proposal\n")
    (templates_dir / "spec.md").write_text("# Spec\n")

    change_dir = create_change(specink_root, "test-feature", templates_dir)

    assert change_dir.exists()
    assert (change_dir / "proposal.md").exists()
    assert (change_dir / "specs" / "spec.md").exists()
    assert (change_dir / "design.md").exists()
    assert (change_dir / "tasks.md").exists()
    assert (change_dir / "transcript.md").exists()
    assert (change_dir / "decisions.md").exists()


def test_list_active_changes(tmp_path: Path) -> None:
    """list_active_changes returns active change names."""
    specink_root = tmp_path / ".specink"
    changes_dir = specink_root / "changes"
    changes_dir.mkdir(parents=True)

    (changes_dir / "feature-a").mkdir()
    (changes_dir / "feature-b").mkdir()
    (changes_dir / "archive").mkdir()

    active = list_active_changes(specink_root)
    assert set(active) == {"feature-a", "feature-b"}


def test_archive_change(tmp_path: Path) -> None:
    """archive_change moves change to archive with timestamp."""
    specink_root = tmp_path / ".specink"
    changes_dir = specink_root / "changes"
    changes_dir.mkdir(parents=True)

    active_path = changes_dir / "feature-x"
    active_path.mkdir()
    (active_path / "proposal.md").write_text("test")

    archived_path = archive_change(specink_root, "feature-x")

    assert not active_path.exists()
    assert archived_path.exists()
    assert "feature-x" in archived_path.name
    assert (archived_path / "proposal.md").read_text() == "test"


def test_get_change_path_active(tmp_path: Path) -> None:
    """get_change_path finds active changes."""
    specink_root = tmp_path / ".specink"
    changes_dir = specink_root / "changes"
    changes_dir.mkdir(parents=True)

    (changes_dir / "my-feature").mkdir()

    path = get_change_path(specink_root, "my-feature")
    assert path is not None
    assert path.name == "my-feature"


def test_get_change_path_archived(tmp_path: Path) -> None:
    """get_change_path finds archived changes."""
    specink_root = tmp_path / ".specink"
    archive_dir = specink_root / "changes" / "archive"
    archive_dir.mkdir(parents=True)

    (archive_dir / "2026-01-15-old-feature").mkdir()

    path = get_change_path(specink_root, "old-feature")
    assert path is not None
    assert "old-feature" in path.name
