"""Goal management service for AURA."""

from __future__ import annotations

from aura.brain.goal import Goal


class GoalManager:
    """Manage autonomous goals."""

    def __init__(self) -> None:
        self._goals: dict[str, Goal] = {}

    def create_goal(
        self,
        description: str,
        priority: str = "normal",
        success_criteria: list[str] | None = None,
        metadata: dict[str, object] | None = None,
    ) -> Goal:
        """Create and register a new goal."""

        goal = Goal(
            description=description,
            priority=priority,
            success_criteria=success_criteria or [],
            metadata=metadata or {},
        )

        self._goals[goal.goal_id] = goal

        return goal

    def get_goal(
        self,
        goal_id: str,
    ) -> Goal | None:
        """Return goal by id."""

        return self._goals.get(
            goal_id,
        )

    def list_goals(
        self,
    ) -> list[Goal]:
        """Return all goals."""

        return list(
            self._goals.values(),
        )

    def active_goals(
        self,
    ) -> list[Goal]:
        """Return active goals."""

        return [
            goal
            for goal in self._goals.values()
            if goal.is_active
        ]

    def update_progress(
        self,
        goal_id: str,
        progress: float,
    ) -> Goal | None:
        """Update goal progress."""

        goal = self.get_goal(
            goal_id,
        )

        if goal is None:
            return None

        goal.update_progress(
            progress,
        )

        return goal

    def complete_goal(
        self,
        goal_id: str,
    ) -> Goal | None:
        """Mark goal completed."""

        goal = self.get_goal(
            goal_id,
        )

        if goal is None:
            return None

        goal.mark_completed()

        return goal

    def fail_goal(
        self,
        goal_id: str,
    ) -> Goal | None:
        """Mark goal failed."""

        goal = self.get_goal(
            goal_id,
        )

        if goal is None:
            return None

        goal.mark_failed()

        return goal

    def remove_goal(
        self,
        goal_id: str,
    ) -> bool:
        """Remove goal."""

        if goal_id not in self._goals:
            return False

        del self._goals[goal_id]

        return True

    def clear(
        self,
    ) -> None:
        """Remove all goals."""

        self._goals.clear()