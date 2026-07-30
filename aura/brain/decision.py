"""Decision engine for AURA brain."""

from __future__ import annotations

from dataclasses import dataclass

from aura.brain.models import Decision


@dataclass
class Action:
    """Action selected by the decision engine."""

    name: str

    reason: str


class DecisionEngine:
    """Convert decisions into executable actions."""

    def decide(
        self,
        decision: Decision,
    ) -> Action:
        """Select next action."""

        if decision.requires_tool:
            return Action(
                name="execute_tool",
                reason=(f"Intent '{decision.intent}' " "requires a tool."),
            )

        return Action(
            name="generate_response",
            reason=(f"Intent '{decision.intent}' " "can be handled conversationally."),
        )
