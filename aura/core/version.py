"""Version metadata for AURA."""

from __future__ import annotations

from pathlib import Path


def get_version() -> str:
    """Return the version stored in the repository-level VERSION file."""
    version_file = Path(__file__).resolve().parents[2] / "VERSION"
    return version_file.read_text(encoding="utf-8").strip()
