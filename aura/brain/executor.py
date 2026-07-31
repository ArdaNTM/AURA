"""AURA plan execution layer."""

from __future__ import annotations

from aura.ai.tool_runner import ToolRunner
from aura.brain.models import Decision, PlanStep
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

    def _execute_step(
        self,
        step: PlanStep,
    ) -> ToolResult | None:
        """Execute a single plan step."""

        if step.action is None:
            return None

        if step.action == "calculator":
            expression = step.metadata.get(
                "expression",
                "",
            )

            return self._tool_runner.run(
                "calculator",
                expression,
            )

        return None
