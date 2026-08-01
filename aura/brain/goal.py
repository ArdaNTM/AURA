"""Goal model for AURA."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Goal:
    """Represents a goal the agent should achieve."""

    description: str

    priority: str = "normal"

    completed: bool = False

    progress: float = 0.0

    status: str = "active"

    goal_id: str = field(
        default_factory=lambda: str(
            uuid4(),
        ),
    )

    success_criteria: list[str] = field(
        default_factory=list,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    @property
    def is_active(
        self,
    ) -> bool:
        """Return whether the goal is active."""

        return self.status == "active"

    @property
    def is_completed(
        self,
    ) -> bool:
        """Return whether the goal is completed."""

        return self.completed

    def mark_completed(
        self,
    ) -> None:
        """Mark goal as completed."""

        self.completed = True
        self.progress = 1.0
        self.status = "completed"

    def mark_failed(
        self,
    ) -> None:
        """Mark goal as failed."""

        self.completed = False
        self.status = "failed"

    def reset(
        self,
    ) -> None:
        """Reset goal execution."""

        self.completed = False
        self.progress = 0.0
        self.status = "active"

    def add_success_criterion(
        self,
        criterion: str,
    ) -> None:
        """Register a success criterion."""

        if criterion not in self.success_criteria:
            self.success_criteria.append(
                criterion,
            )

    def update_progress(
        self,
        progress: float,
    ) -> None:
        """Update goal progress."""

        self.progress = max(
            0.0,
            min(
                1.0,
                progress,
            ),
        )

        if self.progress >= 1.0:
            self.mark_completed()
