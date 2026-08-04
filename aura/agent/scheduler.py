"""Autonomous task scheduler."""

from __future__ import annotations

from aura.agent.autonomous_task import AutonomousTask


class Scheduler:
    """Manage autonomous tasks."""

    def __init__(self) -> None:
        self._tasks: list[AutonomousTask] = []

    @property
    def tasks(
        self,
    ) -> list[AutonomousTask]:
        """Return registered tasks."""

        return self._tasks

    def add(
        self,
        task: AutonomousTask,
    ) -> None:
        """Register autonomous task."""

        self._tasks.append(
            task,
        )

    def remove(
        self,
        task_id: str,
    ) -> bool:
        """Remove task."""

        for task in self._tasks:
            if task.task_id == task_id:
                self._tasks.remove(
                    task,
                )

                return True

        return False

    def pending(
        self,
    ) -> list[AutonomousTask]:
        """Return tasks ready to run."""

        return [task for task in self._tasks if task.should_run()]

    def active(
        self,
    ) -> list[AutonomousTask]:
        """Return enabled tasks."""

        return [task for task in self._tasks if task.enabled]
