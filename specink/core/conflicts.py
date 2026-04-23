"""Conflict detection for active changes."""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from specink.core.change import get_change_path, list_active_changes
from specink.core.spec import parse_spec_sections


@dataclass
class Conflict:
    """A conflict between two changes."""

    change_a: str
    change_b: str
    file_path: str
    section: str


def scan_conflicts(specink_root: Path) -> list[Conflict]:
    """Scan active changes for overlapping spec sections."""
    active = list_active_changes(specink_root)
    if len(active) < 2:
        return []

    section_map: dict[tuple[str, str], list[str]] = defaultdict(list)

    for change_name in active:
        change_path = get_change_path(specink_root, change_name)
        if change_path is None:
            continue

        for file_name in ["design.md", "specs/spec.md"]:
            file_path = change_path / file_name
            if not file_path.exists():
                continue

            content = file_path.read_text()
            sections = parse_spec_sections(content)

            for section in sections:
                key = (file_name, section.heading)
                section_map[key].append(change_name)

    conflicts: list[Conflict] = []
    for (file_name, section_heading), changes in section_map.items():
        if len(changes) > 1:
            for i in range(len(changes)):
                for j in range(i + 1, len(changes)):
                    conflicts.append(
                        Conflict(
                            change_a=changes[i],
                            change_b=changes[j],
                            file_path=file_name,
                            section=section_heading,
                        )
                    )

    return conflicts
