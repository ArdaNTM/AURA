"""Autonomous task scheduler."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aura.agent.autonomous_task import AutonomousTask

if TYPE_CHECKING:
    from aura.agent.task_store import TaskStore


class Scheduler:
    """Manage autonomous tasks."""

    def __init__(
        self,
        store=None,
    ) -> None:
        self._store = store
        self._tasks = []

        if self._store:
            self._tasks = self._store.load_all()

    @property
    def tasks(
        self,
    ) -> list[AutonomousTask]:
        """Return registered tasks."""

        return self._tasks

    @property
    def store(
        self,
    ) -> TaskStore | None:
        """Return task store."""

        return self._store

    def add(
        self,
        task: AutonomousTask,
    ) -> None:
        """Register autonomous task."""

        if self._store:
            self._store.save(
                task,
            )

        self._tasks.append(
            task,
        )

    def remove(
        self,
        task_id: str,
    ) -> bool:
        """Remove task."""

        for task in self._tasks:

            if task.task_id != task_id:
                continue

            self._tasks.remove(
                task,
            )

            if self._store:
                self._store.delete(
                    task_id,
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
