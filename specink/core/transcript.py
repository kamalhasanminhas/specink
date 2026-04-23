"""Transcript management."""

import sys
from datetime import datetime
from pathlib import Path


def append_transcript(
    change_dir: Path,
    content: str,
    speaker: str = "assistant",
) -> None:
    """Append an entry to the transcript file."""
    transcript_path = change_dir / "transcript.md"

    if not transcript_path.exists():
        transcript_path.write_text("# Transcript\n\n---\n")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n## {timestamp} — {speaker}\n\n{content.strip()}\n\n---\n"

    with open(transcript_path, "a") as f:
        f.write(entry)


def read_transcript(change_dir: Path, tail: int | None = None) -> str:
    """Read the transcript file."""
    transcript_path = change_dir / "transcript.md"

    if not transcript_path.exists():
        return ""

    content = transcript_path.read_text()

    if tail is not None:
        lines = content.splitlines()
        return "\n".join(lines[-tail:])

    return content


def read_stdin() -> str:
    """Read content from stdin."""
    if sys.stdin.isatty():
        lines: list[str] = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        return "\n".join(lines)
    else:
        return sys.stdin.read()
