from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Initiative:
    """Autonomous improvement initiative."""

    reason: str

    task: str

    priority: str = "normal"

    strategy: str | None = None
