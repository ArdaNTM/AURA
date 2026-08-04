"""Autonomous task model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class AutonomousTask:
    """Background executable task."""

    description: str

    interval: int

    enabled: bool = True

    task_id: str = field(
        default_factory=lambda: str(uuid4()),
    )

    last_run: datetime | None = None

    run_count: int = 0

    def should_run(
        self,
        now: datetime | None = None,
    ) -> bool:
        """Check whether task should execute."""

        if not self.enabled:
            return False

        if self.last_run is None:
            return True

        current = now or datetime.now()

        elapsed = (current - self.last_run).total_seconds()

        return elapsed >= self.interval

    def mark_completed(
        self,
        now: datetime | None = None,
    ) -> None:
        """Mark task execution."""

        self.last_run = now or datetime.now()

        self.run_count += 1
