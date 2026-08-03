"""Background task model for AURA."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class BackgroundTask:
    """Persistent autonomous task."""

    description: str

    status: str = "pending"

    progress: float = 0.0

    current_step: str | None = None

    task_id: str = field(
        default_factory=lambda: str(uuid4()),
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    def start(
        self,
    ) -> None:
        self.status = "running"

    def complete(
        self,
    ) -> None:
        self.status = "completed"
        self.progress = 1.0

    def fail(
        self,
        reason: str,
    ) -> None:
        self.status = "failed"
        self.metadata["error"] = reason

    def update_progress(
        self,
        progress: float,
        step: str | None = None,
    ) -> None:

        self.progress = max(
            0.0,
            min(
                1.0,
                progress,
            ),
        )

        if step:
            self.current_step = step
