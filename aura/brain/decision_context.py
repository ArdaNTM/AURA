"""Decision context for AURA planning."""

from __future__ import annotations

from dataclasses import dataclass, field

from aura.brain.goal import Goal
from aura.brain.user_profile import UserProfile


@dataclass
class DecisionContext:
    """Context provided to the decision system."""

    user_message: str

    goal: Goal | None = None

    learning: dict[str, object] = field(
        default_factory=dict,
    )

    memory: list[tuple[str, str]] = field(
        default_factory=list,
    )

    user_profile: UserProfile | None = None

    environment: dict[str, object] = field(
        default_factory=dict,
    )

    vision: dict[str, object] = field(
        default_factory=dict,
    )

    permissions: dict[str, bool] = field(
        default_factory=dict,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
