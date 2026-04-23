"""Decision record management."""

from datetime import datetime
from pathlib import Path


def add_decision(
    change_dir: Path,
    title: str,
    decided: str,
    rationale: str,
    alternatives: str,
) -> None:
    """Add a decision record to decisions.md."""
    decisions_path = change_dir / "decisions.md"

    if not decisions_path.exists():
        decisions_path.write_text("# Decisions\n\n---\n")

    date = datetime.now().strftime("%Y-%m-%d")
    entry = f"""
## Decision: {title}
**Date**: {date}
**Status**: Accepted

### What was decided
{decided.strip()}

### Rationale
{rationale.strip()}

### Alternatives rejected
{alternatives.strip()}

---
"""

    with open(decisions_path, "a") as f:
        f.write(entry)


def list_decisions(change_dir: Path) -> list[str]:
    """List decision titles from decisions.md."""
    decisions_path = change_dir / "decisions.md"

    if not decisions_path.exists():
        return []

    content = decisions_path.read_text()
    titles: list[str] = []

    for line in content.splitlines():
        if line.startswith("## Decision:"):
            title = line.replace("## Decision:", "").strip()
            titles.append(title)

    return titles
