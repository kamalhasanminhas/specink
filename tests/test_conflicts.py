"""Tests for conflicts module."""

from pathlib import Path

from specink.core.conflicts import scan_conflicts


def test_scan_conflicts_detects_overlap(tmp_path: Path) -> None:
    """scan_conflicts finds overlapping sections."""
    specink_root = tmp_path / ".specink"
    changes_dir = specink_root / "changes"
    changes_dir.mkdir(parents=True)

    change_a = changes_dir / "feature-a"
    change_a.mkdir()
    (change_a / "specs").mkdir()
    (change_a / "specs" / "spec.md").write_text("# Color system\n\nDetails")

    change_b = changes_dir / "feature-b"
    change_b.mkdir()
    (change_b / "specs").mkdir()
    (change_b / "specs" / "spec.md").write_text("# Color system\n\nOther details")

    conflicts = scan_conflicts(specink_root)
    assert len(conflicts) == 1
    assert conflicts[0].section == "Color system"
    assert set([conflicts[0].change_a, conflicts[0].change_b]) == {"feature-a", "feature-b"}


def test_scan_conflicts_no_overlap(tmp_path: Path) -> None:
    """scan_conflicts returns empty when no overlaps."""
    specink_root = tmp_path / ".specink"
    changes_dir = specink_root / "changes"
    changes_dir.mkdir(parents=True)

    change_a = changes_dir / "feature-a"
    change_a.mkdir()
    (change_a / "specs").mkdir()
    (change_a / "specs" / "spec.md").write_text("# Section A\n")

    change_b = changes_dir / "feature-b"
    change_b.mkdir()
    (change_b / "specs").mkdir()
    (change_b / "specs" / "spec.md").write_text("# Section B\n")

    conflicts = scan_conflicts(specink_root)
    assert len(conflicts) == 0


def test_scan_conflicts_single_change(tmp_path: Path) -> None:
    """scan_conflicts returns empty with only one active change."""
    specink_root = tmp_path / ".specink"
    changes_dir = specink_root / "changes"
    changes_dir.mkdir(parents=True)

    change_a = changes_dir / "feature-a"
    change_a.mkdir()

    conflicts = scan_conflicts(specink_root)
    assert len(conflicts) == 0
