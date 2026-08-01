"""Execution plan for multi-step agent tasks."""

from __future__ import annotations

from dataclasses import dataclass, field

from aura.brain.models import PlanStep


@dataclass
class ExecutionPlan:
    """Represents a multi-step execution plan."""

    goal: str

    steps: list[PlanStep] = field(
        default_factory=list,
    )

    current_step: int = 0

    @property
    def completed(
        self,
    ) -> bool:
        """Return whether all steps are complete."""

        return self.current_step >= len(
            self.steps,
        )

    @property
    def completed_steps(
        self,
    ) -> int:
        """Return completed step count."""

        return self.current_step

    @property
    def remaining_steps(
        self,
    ) -> int:
        """Return remaining step count."""

        return max(
            0,
            len(
                self.steps,
            )
            - self.current_step,
        )

    def current(
        self,
    ) -> PlanStep | None:
        """Return current step."""

        if self.completed:
            return None

        return self.steps[self.current_step]

    def next_step(
        self,
    ) -> PlanStep | None:
        """Advance to the next step."""

        step = self.current()

        if step is None:
            return None

        self.current_step += 1

        return step

    def is_complete(
        self,
    ) -> bool:
        """Return whether execution is complete."""

        return self.completed

    def reset(
        self,
    ) -> None:
        """Restart execution."""

        self.current_step = 0
