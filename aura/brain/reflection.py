"""Reflection models for AURA agent loop."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Reflection:
    """Self evaluation result after an agent cycle."""

    success: bool

    summary: str

    improvements: list[str] = field(
        default_factory=list,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
