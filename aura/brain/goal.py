"""Goal model for AURA."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Goal:
    """Represents a goal the agent should achieve."""

    description: str

    priority: str = "normal"

    completed: bool = False

    progress: float = 0.0

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    def mark_completed(
        self,
    ) -> None:
        """Mark goal as completed."""

        self.completed = True
        self.progress = 1.0

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
            self.completed = True
