"""AURA plan execution layer."""

from __future__ import annotations

from aura.ai.tool_runner import ToolRunner
from aura.brain.models import Decision, PlanStep
from aura.brain.observation import Observation
from aura.core.tool_result import ToolResult


class PlanExecutor:
    """Execute planned actions."""

    def __init__(
        self,
        tool_runner: ToolRunner,
    ) -> None:
        self._tool_runner = tool_runner

    @property
    def tool_runner(self) -> ToolRunner:
        """Return tool runner."""

        return self._tool_runner

    def execute(
        self,
        decision: Decision,
    ) -> list[ToolResult]:
        """Execute decision plan."""

        results: list[ToolResult] = []

        for step in decision.plan:
            result = self._execute_step(
                step,
            )

            if result is not None:
                results.append(
                    result,
                )

            step.completed = True

        return results

    def execute_with_observation(
        self,
        decision: Decision,
    ) -> list[Observation]:
        """Execute plan and return observations."""

        observations: list[Observation] = []

        for step in decision.plan:
            result = self._execute_step(
                step,
            )

            step.completed = True

            if result is None:
                continue

            observations.append(
                Observation(
                    source=result.name,
                    output=result.output,
                    success=result.success,
                    metadata=(
                        {
                            "error": result.error,
                        }
                        if result.error
                        else None
                    ),
                )
            )

        return observations

    def _execute_step(
        self,
        step: PlanStep,
    ) -> ToolResult | None:
        """Execute a single plan step."""

        if step.action is None:
            return None

        if step.action in (
            "analyze",
            "respond",
        ):
            return None

        return self._tool_runner.run(
            step.action,
            **step.metadata,
        )
