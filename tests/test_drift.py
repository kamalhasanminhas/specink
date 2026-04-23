"""Tests for drift module."""

from pathlib import Path

from specink.core.drift import check_drift, search_codebase


def test_search_codebase_finds_identifier(tmp_path: Path) -> None:
    """search_codebase finds identifier in source files."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "module.py").write_text("def my_function():\n    pass\n")

    matches = search_codebase(tmp_path, "my_function", [".py"])
    assert len(matches) == 1
    assert "module.py" in str(matches[0])


def test_search_codebase_ignores_specink(tmp_path: Path) -> None:
    """search_codebase ignores .specink directory."""
    (tmp_path / ".specink").mkdir()
    (tmp_path / ".specink" / "spec.md").write_text("my_function")

    matches = search_codebase(tmp_path, "my_function", [".md"])
    assert len(matches) == 0


def test_check_drift_found(tmp_path: Path) -> None:
    """check_drift returns found status when identifier exists."""
    change_dir = tmp_path / "change"
    change_dir.mkdir()
    (change_dir / "specs").mkdir()
    (change_dir / "specs" / "spec.md").write_text("**THEN** `my_function` is called")

    project_root = tmp_path
    (project_root / "src").mkdir()
    (project_root / "src" / "code.py").write_text("def my_function(): pass")

    results = check_drift(change_dir, project_root)
    assert len(results) == 1
    assert results[0].identifier == "my_function"
    assert results[0].status == "found"


def test_check_drift_not_found(tmp_path: Path) -> None:
    """check_drift returns not_found when identifier missing."""
    change_dir = tmp_path / "change"
    change_dir.mkdir()
    (change_dir / "specs").mkdir()
    (change_dir / "specs" / "spec.md").write_text("**THEN** `missing_function` is called")

    project_root = tmp_path
    results = check_drift(change_dir, project_root)
    assert len(results) == 1
    assert results[0].status == "not_found"


def test_check_drift_test_only(tmp_path: Path) -> None:
    """check_drift returns test_only when identifier only in tests."""
    change_dir = tmp_path / "change"
    change_dir.mkdir()
    (change_dir / "specs").mkdir()
    (change_dir / "specs" / "spec.md").write_text("**THEN** `my_function` is called")

    project_root = tmp_path
    (project_root / "tests").mkdir()
    (project_root / "tests" / "test_code.py").write_text("assert my_function() == 42")

    results = check_drift(change_dir, project_root)
    assert len(results) == 1
    assert results[0].status == "test_only"
