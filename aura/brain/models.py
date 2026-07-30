"""Models used by AURA decision layer."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlanStep:
    """Single step in an execution plan."""

    description: str
    completed: bool = False


@dataclass
class Decision:
    """Represents AURA's decision about a request."""

    intent: str

    confidence: float = 0.0

    requires_tool: bool = False

    plan: list[PlanStep] = field(
        default_factory=list,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )