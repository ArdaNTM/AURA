"""AURA task planner."""

from __future__ import annotations

import re

from aura.brain.models import Decision, PlanStep


class Planner:
    """Create decisions from user requests."""

    def decide(
        self,
        user_message: str,
    ) -> Decision:
        """Analyze request and create a decision."""

        message = user_message.casefold()

        if self._is_calculation_request(
            message,
        ):
            return Decision(
                intent="calculation",
                confidence=0.9,
                requires_tool=True,
                target=self._select_tool(
                    "calculation",
                ),
                plan=[
                    PlanStep(
                        "Analyze calculation request",
                    ),
                    PlanStep(
                        "Use calculator tool",
                    ),
                ],
                metadata={
                    "expression": self._extract_expression(
                        user_message,
                    ),
                },
            )

        return Decision(
            intent="conversation",
            confidence=0.7,
            requires_tool=False,
            plan=[
                PlanStep(
                    "Generate conversational response",
                ),
            ],
        )

    def _is_calculation_request(
        self,
        message: str,
    ) -> bool:
        """Detect calculation intent."""

        return any(
            keyword in message
            for keyword in [
                "hesapla",
                "kaÃ§",
                "topla",
                "Ã§Ä±kar",
                "Ã§arp",
                "bÃ¶l",
            ]
        )

    def _select_tool(
        self,
        intent: str,
    ) -> str | None:
        """Select tool for intent."""

        if intent == "calculation":
            return "calculator"

        return None

    def _extract_expression(
        self,
        user_message: str,
    ) -> str:
        """Extract mathematical expression from message."""

        return re.sub(
            r"[^\d+\-*/().]",
            "",
            user_message,
        )
