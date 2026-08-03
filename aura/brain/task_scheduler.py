"""Task scheduler for AURA."""

from __future__ import annotations

from aura.brain.task_graph import TaskGraph, TaskNode


class TaskScheduler:
    """Select next executable task."""

    def __init__(
        self,
        graph: TaskGraph,
    ) -> None:
        self._graph = graph

    @property
    def graph(
        self,
    ) -> TaskGraph:
        """Return task graph."""

        return self._graph

    def next_task(
        self,
    ) -> TaskNode | None:
        """Return next available task."""

        available = self._graph.next_available()

        if not available:
            return None

        return available[0]

    def complete(
        self,
        task_id: str,
    ) -> None:
        """Complete selected task."""

        self._graph.complete(
            task_id,
        )

    def has_pending_tasks(
        self,
    ) -> bool:
        """Check remaining executable tasks."""

        return bool(
            self._graph.next_available(),
        )
