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

    metadata: dict[str, object] = field(
        default_factory=dict,
    )


class DecisionEngine:
    """Convert decisions into executable actions."""

    def decide(
        self,
        decision: Decision,
    ) -> Action:
        """Select next action."""

        if decision.strategy == "ask_confirmation":
            return Action(
                name="request_confirmation",
                reason=("Decision requires user confirmation " "before execution."),
                metadata=self._build_metadata(
                    decision,
                ),
            )

        if decision.strategy == "tool_execution" or decision.requires_tool:
            return Action(
                name="execute_tool",
                reason=(f"Intent '{decision.intent}' " "requires a tool."),
                tool_name=decision.target,
                parameters=self._build_parameters(
                    decision,
                ),
                metadata=self._build_metadata(
                    decision,
                ),
            )

        return Action(
            name="generate_response",
            reason=(f"Intent '{decision.intent}' " "can be handled conversationally."),
            metadata=self._build_metadata(
                decision,
            ),
        )

    def _build_parameters(
        self,
        decision: Decision,
    ) -> dict[str, object]:
        """Build tool parameters from decision metadata."""

        if decision.intent == "calculation":
            return {
                "expression": decision.metadata.get(
                    "expression",
                    "",
                )
            }

        return {}

    def _build_metadata(
        self,
        decision: Decision,
    ) -> dict[str, object]:
        """Collect decision metadata for action."""

        return {
            "intent": decision.intent,
            "confidence": decision.confidence,
            "priority": decision.priority,
            "risk_level": decision.risk_level,
            "strategy": decision.strategy,
        }
