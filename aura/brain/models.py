"""Models used by AURA decision layer."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlanStep:
    """Single step in an execution plan."""

    description: str

    action: str | None = None

    completed: bool = False

    metadata: dict[str, object] = field(
        default_factory=dict,
    )


@dataclass
class Decision:
    """Represents AURA's decision about a request."""

    intent: str

    confidence: float = 0.0

    requires_tool: bool = False

    target: str | None = None

    priority: str = "normal"

    risk_level: str = "low"

    strategy: str | None = None

    explanation: str | None = None

    plan: list[PlanStep] = field(
        default_factory=list,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
