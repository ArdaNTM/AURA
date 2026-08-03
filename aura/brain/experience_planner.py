"""Experience based plan modification for AURA."""

from __future__ import annotations

from aura.brain.models import PlanStep


class ExperiencePlanner:
    """Modify plans using previous task experiences."""

    def modify_plan(
        self,
        plan: list[PlanStep],
        learning: dict[str, object] | None = None,
    ) -> list[PlanStep]:
        """Adjust execution plan from previous experience."""

        if not learning:
            return plan

        failures = learning.get(
            "task_failures",
            [],
        )

        if failures:
            recovery_step = PlanStep(
                description="Review previous task failure",
                action="experience_recovery",
                metadata={
                    "reason": failures[0],
                },
            )

            return [
                recovery_step,
                *plan,
            ]

        experiences = learning.get(
            "task_experiences",
            [],
        )

        if experiences:
            experience_step = PlanStep(
                description="Apply successful previous strategy",
                action="experience_strategy",
                metadata={
                    "experience": experiences[0],
                },
            )

            return [
                experience_step,
                *plan,
            ]

        return plan