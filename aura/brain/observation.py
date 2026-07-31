"""Observation models for AURA agent loop."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Observation:
    """Result observed after executing an action."""

    source: str

    output: str

    success: bool = True

    score: float = 0.0

    feedback: str | None = None

    retry_needed: bool = False

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
