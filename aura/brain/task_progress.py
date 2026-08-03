"""Task progress tracking for AURA."""

from __future__ import annotations

from aura.brain.task_graph import TaskGraph


class TaskProgressTracker:
    """Track autonomous task progress."""

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

    def total_tasks(
        self,
    ) -> int:
        """Return total task count."""

        return len(
            self._graph.nodes,
        )

    def completed_tasks(
        self,
    ) -> int:
        """Return completed task count."""

        return sum(
            1
            for node in self._graph.nodes.values()
            if node.completed
        )

    def percentage(
        self,
    ) -> float:
        """Return completion percentage."""

        total = self.total_tasks()

        if total == 0:
            return 0.0

        return self.completed_tasks() / total

    def current_task(
        self,
    ) -> str | None:
        """Return active task."""

        available = self._graph.next_available()

        if not available:
            return None

        return available[0].task

    def summary(
        self,
    ) -> dict[str, object]:
        """Return progress summary."""

        return {
            "total": self.total_tasks(),
            "completed": self.completed_tasks(),
            "percentage": self.percentage(),
            "current": self.current_task(),
        }