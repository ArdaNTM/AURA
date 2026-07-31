"""Agent improvement planning models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ImprovementPlan:
    """Suggested improvements for future executions."""

    suggestions: list[str] = field(
        default_factory=list,
    )

    target_strategy: str | None = None

    confidence_change: float = 0.0

    risk_adjustment: str | None = None
