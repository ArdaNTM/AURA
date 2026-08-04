from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentExperience:
    """Single autonomous execution experience."""

    task: str

    success: bool

    strategy: str | None

    score: float

    output: str | None = None

    reflection: str | None = None
