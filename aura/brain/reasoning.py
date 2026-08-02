"""LLM reasoning models for AURA."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ReasoningResult:
    """Structured reasoning output."""

    intent: str

    goal: str = ""

    capability: str | None = None

    confidence: float = 0.0

    risk_level: str = "low"

    entities: dict[str, object] = field(
        default_factory=dict,
    )
