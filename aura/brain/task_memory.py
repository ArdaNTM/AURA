"""Task execution memory for AURA."""

from __future__ import annotations

from aura.memory.base import Memory


class TaskMemory:
    """Store and retrieve task experiences."""

    def __init__(
        self,
        memory: Memory,
    ) -> None:
        self._memory = memory

    @property
    def memory(
        self,
    ) -> Memory:
        """Return backing memory."""

        return self._memory

    def store_success(
        self,
        task: str,
        output: str,
        strategy: str = "tool_execution",
    ) -> None:
        """Store successful task execution."""

        self._memory.add(
            "assistant",
            (
                f"task={task}; "
                "task_success=True; "
                "success=True; "
                f"strategy={strategy}; "
                f"output={output}"
            ),
        )

    def store_failure(
        self,
        task: str,
        reason: str,
    ) -> None:
        """Store failed task execution."""

        self._memory.add(
            "assistant",
            (
                f"task={task}; "
                "task_success=False; "
                "success=False; "
                f"reason={reason}"
            ),
        )

    def recall(
        self,
        task: str,
    ) -> list[tuple[str, str]]:
        """Recall previous task experiences."""

        return [item for item in self._memory.history() if f"task={task}" in item[1]]

    def previous_failures(
        self,
        task: str,
    ) -> list[tuple[str, str]]:
        """Return previous failed executions."""

        return [
            item
            for item in self.recall(task)
            if ("task_success=False" in item[1] or "success=False" in item[1])
        ]

    def has_previous_failure(
        self,
        task: str,
    ) -> bool:
        """Check whether task failed before."""

        return bool(
            self.previous_failures(
                task,
            )
        )

    def successful_experiences(
        self,
        task: str,
    ) -> list[tuple[str, str]]:
        """Return successful previous task executions."""

        return [
            item
            for item in self.recall(
                task,
            )
            if ("task_success=True" in item[1] or "success=True" in item[1])
        ]

    def rank_experiences(
        self,
        task: str,
    ) -> list[tuple[str, str]]:
        """Rank task experiences by quality."""

        experiences = self.successful_experiences(
            task,
        )

        return sorted(
            experiences,
            key=self._experience_score,
            reverse=True,
        )

    def _experience_score(
        self,
        experience: tuple[str, str],
    ) -> float:
        """Calculate task experience value."""

        _, content = experience

        score = 0.0

        if "task_success=True" in content:
            score += 1.0

        if "success=True" in content:
            score += 1.0

        if "strategy=safe_tool_execution" in content:
            score += 0.5

        elif "strategy=tool_execution" in content:
            score += 0.1

        return score
