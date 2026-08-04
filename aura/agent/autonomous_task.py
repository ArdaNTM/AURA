"""Autonomous task model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
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

    status: str = "pending"

    result: str | None = None

    error: str | None = None

    retry_count: int = 0

    max_retries: int = 3

    next_retry: datetime | None = None

    def should_run(
        self,
        now: datetime | None = None,
    ) -> bool:
        """Check whether task should execute."""

        if not self.enabled:
            return False

        if self.status == "running":
            return False

        if self.next_retry:
            current = now or datetime.now()

            if current < self.next_retry:
                return False

        if self.last_run is None:
            return True

        current = now or datetime.now()

        elapsed = (current - self.last_run).total_seconds()

        return elapsed >= self.interval

    def mark_running(
        self,
    ) -> None:
        """Mark task as running."""

        self.status = "running"

    def mark_completed(
        self,
        result: str | None = None,
        now: datetime | None = None,
    ) -> None:
        """Mark task execution completed."""

        self.last_run = now or datetime.now()

        self.run_count += 1

        self.status = "completed"

        self.result = result

        self.error = None

    def reset(
        self,
    ) -> None:
        """Reset interrupted task back to pending."""

        self.status = "pending"

        self.error = None

    def can_retry(
        self,
    ) -> bool:
        """Check whether retry is available."""

        return self.retry_count < self.max_retries

    def schedule_retry(
        self,
        delay: int = 60,
    ) -> None:
        """Schedule next retry attempt."""

        self.retry_count += 1

        self.next_retry = datetime.now() + timedelta(seconds=delay)

        self.status = "pending"

    def mark_failed(
        self,
        error: str,
        now: datetime | None = None,
    ) -> None:
        """Mark task execution failure."""

        self.last_run = now or datetime.now()

        self.run_count += 1

        self.status = "failed"

        self.error = error
