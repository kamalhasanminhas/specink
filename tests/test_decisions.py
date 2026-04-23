"""Tests for decisions module."""

from pathlib import Path

from specink.core.decisions import add_decision, list_decisions


def test_add_decision(tmp_path: Path) -> None:
    """add_decision appends to decisions.md."""
    change_dir = tmp_path / "my-change"
    change_dir.mkdir()

    add_decision(
        change_dir,
        "Use CSS variables",
        "Store colors as custom properties",
        "Runtime switching",
        "Tailwind dark: prefix",
    )

    decisions_file = change_dir / "decisions.md"
    content = decisions_file.read_text()

    assert "Use CSS variables" in content
    assert "Store colors as custom properties" in content
    assert "Runtime switching" in content
    assert "Tailwind dark: prefix" in content


def test_list_decisions(tmp_path: Path) -> None:
    """list_decisions extracts decision titles."""
    change_dir = tmp_path / "my-change"
    change_dir.mkdir()

    add_decision(change_dir, "Decision A", "A", "Because A", "None")
    add_decision(change_dir, "Decision B", "B", "Because B", "None")

    titles = list_decisions(change_dir)
    assert len(titles) == 2
    assert "Decision A" in titles
    assert "Decision B" in titles


def test_add_decision_creates_file(tmp_path: Path) -> None:
    """add_decision creates decisions.md if missing."""
    change_dir = tmp_path / "new-change"
    change_dir.mkdir()

    add_decision(change_dir, "First", "X", "Y", "Z")
    assert (change_dir / "decisions.md").exists()
