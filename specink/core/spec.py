"""Spec file parsing."""

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SpecSection:
    """A section in a spec file."""

    heading: str
    level: int
    content: str


@dataclass
class SpecAssertion:
    """A THEN assertion from a BDD scenario."""

    text: str
    identifiers: list[str]


def parse_spec_sections(content: str) -> list[SpecSection]:
    """Parse Markdown sections from spec content."""
    sections: list[SpecSection] = []
    lines = content.splitlines()

    current_heading = ""
    current_level = 0
    current_content: list[str] = []

    for line in lines:
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            if current_heading:
                sections.append(
                    SpecSection(
                        heading=current_heading,
                        level=current_level,
                        content="\n".join(current_content).strip(),
                    )
                )
            current_level = len(heading_match.group(1))
            current_heading = heading_match.group(2).strip()
            current_content = []
        else:
            current_content.append(line)

    if current_heading:
        sections.append(
            SpecSection(
                heading=current_heading,
                level=current_level,
                content="\n".join(current_content).strip(),
            )
        )

    return sections


def parse_then_lines(content: str) -> list[SpecAssertion]:
    """Extract THEN lines and identifiers from spec content."""
    assertions: list[SpecAssertion] = []
    lines = content.splitlines()

    for line in lines:
        if re.match(r"^\*\*THEN\*\*", line, re.IGNORECASE) or line.strip().startswith("THEN"):
            identifiers = extract_identifiers(line)
            assertions.append(SpecAssertion(text=line.strip(), identifiers=identifiers))

    return assertions


def extract_identifiers(text: str) -> list[str]:
    """Extract code identifiers from text (quoted, PascalCase, snake_case)."""
    identifiers: list[str] = []

    quoted = re.findall(r"`([^`]+)`", text)
    identifiers.extend(quoted)

    words = text.split()
    for word in words:
        clean_word = re.sub(r"[^\w]", "", word)
        if re.match(r"^[A-Z][a-z]+[A-Z]", clean_word):
            identifiers.append(clean_word)
        elif "_" in clean_word and re.match(r"^[a-z][a-z0-9_]*[a-z0-9]$", clean_word):
            identifiers.append(clean_word)

    return list(set(identifiers))


def load_spec_file(path: Path) -> str:
    """Load spec file content."""
    return path.read_text()
