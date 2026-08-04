"""Self evaluation models for AURA."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SelfEvaluation:
    """AURA internal performance evaluation."""

    overall_score: float

    strongest_skill: str | None = None

    weakest_skill: str | None = None

    best_strategy: str | None = None

    diagnosis: list[str] = field(
        default_factory=list,
    )

    improvement_actions: list[str] = field(
        default_factory=list,
    )

    recommendations: list[str] = field(
        default_factory=list,
    )
