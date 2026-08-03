"""Task decomposition system for AURA."""

from __future__ import annotations

from aura.brain.execution_plan import ExecutionPlan
from aura.brain.goal import Goal
from aura.brain.models import PlanStep


class TaskDecomposer:
    """Decompose high level goals into executable tasks."""

    def decompose(
        self,
        goal: Goal,
    ) -> ExecutionPlan:
        """Create execution plan from goal."""

        tasks = self._generate_tasks(
            goal.description,
        )

        return ExecutionPlan(
            goal=goal.description,
            steps=tasks,
        )

    def _generate_tasks(
        self,
        description: str,
    ) -> list[PlanStep]:
        """Generate task steps."""

        text = description.casefold()

        if any(
            keyword in text
            for keyword in (
                "game",
                "oyun",
            )
        ):
            return [
                PlanStep(
                    description="Define project concept",
                    action="concept",
                ),
                PlanStep(
                    description="Create design structure",
                    action="design",
                ),
                PlanStep(
                    description="Implement code",
                    action="code",
                ),
                PlanStep(
                    description="Test implementation",
                    action="test",
                ),
                PlanStep(
                    description="Build final project",
                    action="build",
                ),
            ]

        if any(
            keyword in text
            for keyword in (
                "app",
                "uygulama",
                "application",
            )
        ):
            return [
                PlanStep(
                    description="Analyze requirements",
                    action="analysis",
                ),
                PlanStep(
                    description="Create architecture",
                    action="architecture",
                ),
                PlanStep(
                    description="Implement application",
                    action="code",
                ),
                PlanStep(
                    description="Run tests",
                    action="test",
                ),
                PlanStep(
                    description="Prepare release",
                    action="release",
                ),
            ]

        return [
            PlanStep(
                description="Analyze goal",
                action="analysis",
            ),
            PlanStep(
                description="Execute goal",
                action="execute",
            ),
        ]
