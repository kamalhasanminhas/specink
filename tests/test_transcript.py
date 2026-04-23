"""Tests for transcript module."""

from pathlib import Path

from specink.core.transcript import append_transcript, read_transcript


def test_append_transcript(tmp_path: Path) -> None:
    """append_transcript creates and appends to transcript."""
    change_dir = tmp_path / "my-change"
    change_dir.mkdir()

    append_transcript(change_dir, "First entry", "human")
    append_transcript(change_dir, "Second entry", "assistant")

    content = read_transcript(change_dir)
    assert "First entry" in content
    assert "Second entry" in content
    assert "human" in content
    assert "assistant" in content


def test_read_transcript_tail(tmp_path: Path) -> None:
    """read_transcript with tail returns last N lines."""
    change_dir = tmp_path / "my-change"
    change_dir.mkdir()

    transcript = change_dir / "transcript.md"
    transcript.write_text("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")

    content = read_transcript(change_dir, tail=2)
    lines = content.splitlines()
    assert len(lines) == 2
    assert "Line 5" in content


def test_append_creates_file_if_not_exists(tmp_path: Path) -> None:
    """append_transcript creates transcript.md if missing."""
    change_dir = tmp_path / "new-change"
    change_dir.mkdir()

    append_transcript(change_dir, "New content")
    assert (change_dir / "transcript.md").exists()
