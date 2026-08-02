"""Reflection models for AURA agent loop."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Reflection:
    """Self evaluation result after an agent cycle."""

    success: bool

    summary: str

    strategy: str | None = None

    intent: str | None = None

    retry_needed: bool = False

    retry_strategy: str | None = None

    quality_score: float = 0.0

    quality_level: str = "unknown"

    improvements: list[str] = field(
        default_factory=list,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
