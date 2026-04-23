"""Configuration management for SpecInk."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


class Config:
    """SpecInk configuration."""

    def __init__(
        self,
        version: str = "1",
        tool: str = "unknown",
        drift_check: bool = True,
        conflict_check: bool = True,
        transcript_auto: bool = True,
        created_at: str | None = None,
    ) -> None:
        self.version = version
        self.tool = tool
        self.drift_check = drift_check
        self.conflict_check = conflict_check
        self.transcript_auto = transcript_auto
        self.created_at = created_at or datetime.now(UTC).isoformat()

    @classmethod
    def load(cls, path: Path) -> "Config":
        """Load config from YAML file."""
        with open(path) as f:
            data: dict[str, Any] = yaml.safe_load(f) or {}
        return cls(
            version=data.get("version", "1"),
            tool=data.get("tool", "unknown"),
            drift_check=data.get("drift_check", True),
            conflict_check=data.get("conflict_check", True),
            transcript_auto=data.get("transcript_auto", True),
            created_at=data.get("created_at"),
        )

    def save(self, path: Path) -> None:
        """Save config to YAML file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            yaml.dump(
                {
                    "version": self.version,
                    "tool": self.tool,
                    "drift_check": self.drift_check,
                    "conflict_check": self.conflict_check,
                    "transcript_auto": self.transcript_auto,
                    "created_at": self.created_at,
                },
                f,
                default_flow_style=False,
            )


def get_specink_root() -> Path | None:
    """Find .specink directory by walking up from cwd."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        specink_dir = parent / ".specink"
        if specink_dir.is_dir():
            return specink_dir
    return None


def get_config_path() -> Path | None:
    """Get path to config.yaml if it exists."""
    root = get_specink_root()
    if root is None:
        return None
    return root / "config.yaml"


def load_config() -> Config | None:
    """Load config from .specink/config.yaml if it exists."""
    config_path = get_config_path()
    if config_path is None or not config_path.exists():
        return None
    return Config.load(config_path)
