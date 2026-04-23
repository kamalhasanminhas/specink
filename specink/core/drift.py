"""Drift detection engine."""

import re
from dataclasses import dataclass
from pathlib import Path

from specink.core.spec import parse_then_lines


def _is_test_file(path: Path) -> bool:
    """Check if a file is a test file based on name or parent directory."""
    name_lower = path.name.lower()
    if "test" in name_lower or name_lower.startswith("spec"):
        return True
    if path.parent.name.lower() in ("test", "tests", "spec", "specs", "__tests__"):
        return True
    return False


@dataclass
class DriftResult:
    """Result of drift check for a single identifier."""

    identifier: str
    status: str
    location: str | None = None


def search_codebase(root: Path, identifier: str, extensions: list[str]) -> list[Path]:
    """Search for identifier in source files."""
    matches: list[Path] = []
    pattern = re.compile(rf"\b{re.escape(identifier)}\b")

    for ext in extensions:
        for file_path in root.rglob(f"*{ext}"):
            if ".specink" in file_path.parts or "node_modules" in file_path.parts:
                continue
            if ".venv" in file_path.parts or "__pycache__" in file_path.parts:
                continue

            try:
                content = file_path.read_text()
                if pattern.search(content):
                    matches.append(file_path)
            except (UnicodeDecodeError, PermissionError):
                continue

    return matches


def check_drift(change_dir: Path, project_root: Path) -> list[DriftResult]:
    """Check for drift between spec and codebase."""
    spec_path = change_dir / "specs" / "spec.md"
    if not spec_path.exists():
        return []

    content = spec_path.read_text()
    assertions = parse_then_lines(content)

    if not assertions:
        return []

    extensions = [".py", ".ts", ".js", ".tsx", ".jsx", ".go", ".rs"]
    results: list[DriftResult] = []

    for assertion in assertions:
        for identifier in assertion.identifiers:
            matches = search_codebase(project_root, identifier, extensions)

            if not matches:
                results.append(DriftResult(identifier=identifier, status="not_found"))
            elif all(_is_test_file(m) for m in matches):
                results.append(
                    DriftResult(
                        identifier=identifier,
                        status="test_only",
                        location=str(matches[0].relative_to(project_root)),
                    )
                )
            else:
                src_match = next((m for m in matches if not _is_test_file(m)), matches[0])
                results.append(
                    DriftResult(
                        identifier=identifier,
                        status="found",
                        location=str(src_match.relative_to(project_root)),
                    )
                )

    return results
