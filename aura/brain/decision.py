"""Decision engine for AURA brain."""

from __future__ import annotations

from dataclasses import dataclass, field

from aura.brain.models import Decision


@dataclass
class Action:
    """Action selected by the decision engine."""

    name: str

    reason: str

    tool_name: str | None = None

    parameters: dict[str, object] = field(
        default_factory=dict,
    )


class DecisionEngine:
    """Convert decisions into executable actions."""

    def decide(
        self,
        decision: Decision,
    ) -> Action:
        """Select next action."""

        if decision.requires_tool:
            parameters: dict[str, object] = {}

            if decision.intent == "calculation":
                parameters = {
                    "expression": decision.metadata.get(
                        "expression",
                        "",
                    )
                }

            return Action(
                name="execute_tool",
                reason=(f"Intent '{decision.intent}' " "requires a tool."),
                tool_name="calculator",
                parameters=parameters,
            )

        return Action(
            name="generate_response",
            reason=(f"Intent '{decision.intent}' " "can be handled conversationally."),
        )
