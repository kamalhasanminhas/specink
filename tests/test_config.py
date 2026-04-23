"""Tests for config module."""

from pathlib import Path

from specink.core.config import Config


def test_config_save_and_load(tmp_path: Path) -> None:
    """Config can be saved and loaded."""
    config_path = tmp_path / "config.yaml"
    config = Config(tool="claude-code")
    config.save(config_path)

    loaded = Config.load(config_path)
    assert loaded.tool == "claude-code"
    assert loaded.version == "1"
    assert loaded.drift_check is True


def test_config_defaults() -> None:
    """Config has correct defaults."""
    config = Config()
    assert config.version == "1"
    assert config.tool == "unknown"
    assert config.drift_check is True
    assert config.conflict_check is True
    assert config.transcript_auto is True
    assert config.created_at is not None


def test_config_creates_parent_dirs(tmp_path: Path) -> None:
    """Config.save creates parent directories."""
    config_path = tmp_path / "nested" / "dir" / "config.yaml"
    config = Config()
    config.save(config_path)
    assert config_path.exists()
