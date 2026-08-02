"""Models used by AURA decision layer."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class IntentAnalysis:
    """Result of intent analysis."""

    intent: str

    confidence: float = 1.0

    entities: dict[str, object] = field(
        default_factory=dict,
    )

    source_confidence: float | None = None


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

    requires_permission: bool = False

    target: str | None = None

    priority: str = "normal"

    risk_level: str = "low"

    strategy: str | None = None

    explanation: str | None = None

    confidence_reason: str | None = None

    routing_reason: str | None = None

    outcome: dict[str, object] = field(
        default_factory=dict,
    )

    plan: list[PlanStep] = field(
        default_factory=list,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
