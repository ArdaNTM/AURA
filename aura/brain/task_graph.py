"""Task dependency graph for AURA."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class TaskNode:
    """Single task node."""

    task: str

    node_id: str = field(
        default_factory=lambda: str(uuid4()),
    )

    dependencies: list[str] = field(
        default_factory=list,
    )

    completed: bool = False


class TaskGraph:
    """Directed dependency graph for tasks."""

    def __init__(self) -> None:
        self._nodes: dict[str, TaskNode] = {}

    @property
    def nodes(
        self,
    ) -> dict[str, TaskNode]:
        """Return graph nodes."""

        return self._nodes

    def add_task(
        self,
        task: str,
    ) -> str:
        """Add task node."""

        node = TaskNode(
            task=task,
        )

        self._nodes[node.node_id] = node

        return node.node_id

    def add_dependency(
        self,
        task_id: str,
        dependency_id: str,
    ) -> None:
        """Add dependency between tasks."""

        node = self._nodes[task_id]

        if dependency_id not in node.dependencies:
            node.dependencies.append(
                dependency_id,
            )

    def can_execute(
        self,
        task_id: str,
    ) -> bool:
        """Check whether task dependencies are completed."""

        node = self._nodes[task_id]

        return all(
            self._nodes[dependency].completed for dependency in node.dependencies
        )

    def next_available(
        self,
    ) -> list[TaskNode]:
        """Return executable tasks."""

        return [
            node
            for node in self._nodes.values()
            if not node.completed
            and self.can_execute(
                node.node_id,
            )
        ]

    def complete(
        self,
        task_id: str,
    ) -> None:
        """Mark task completed."""

        self._nodes[task_id].completed = True
