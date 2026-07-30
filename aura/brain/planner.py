"""AURA task planner."""

from __future__ import annotations

from aura.brain.models import Decision, PlanStep


class Planner:
    """Create decisions from user requests."""

    def decide(
        self,
        user_message: str,
    ) -> Decision:
        """Analyze request and create a decision."""

        message = user_message.casefold()

        if any(
            keyword in message
            for keyword in [
                "hesapla",
                "kaç",
                "topla",
                "çıkar",
                "çarp",
                "böl",
            ]
        ):
            return Decision(
                intent="calculation",
                confidence=0.9,
                requires_tool=True,
                plan=[
                    PlanStep(
                        "Analyze calculation request",
                    ),
                    PlanStep(
                        "Use calculator tool",
                    ),
                ],
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
