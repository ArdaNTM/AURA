"""Plan builder for agent decisions."""

from __future__ import annotations

from aura.brain.models import PlanStep


class PlanBuilder:
    """Build plan steps for decisions."""

    def build_conversation(
        self,
    ) -> list[PlanStep]:
        """Build a conversational plan."""

        return [
            PlanStep(
                description="Generate conversational response",
                action="respond",
            ),
        ]

    def build_calculation(
        self,
        expression: str,
    ) -> list[PlanStep]:
        """Build a calculation plan."""

        return [
            PlanStep(
                description="Analyze calculation request",
                action="analyze",
            ),
            PlanStep(
                description="Calculate expression",
                action="calculator",
                metadata={
                    "expression": expression,
                },
            ),
        ]

    def build_tool_execution(
        self,
        tool_name: str | None,
        parameters: dict[str, object] | None = None,
    ) -> list[PlanStep]:
        """Build a generic tool execution plan."""

        if tool_name is None:
            return []

        return [
            PlanStep(
                description=f"Execute tool: {tool_name}",
                action=tool_name,
                metadata=parameters or {},
            ),
        ]
