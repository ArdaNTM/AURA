"""AURA task planner."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from aura.brain.models import Decision, PlanStep

if TYPE_CHECKING:
    from aura.core.tools import ToolRegistry


class Planner:
    """Create decisions from user requests."""

    def __init__(
        self,
        tools: ToolRegistry | None = None,
    ) -> None:
        self._tools = tools

    def decide(
        self,
        user_message: str,
        learning: dict[str, object] | None = None,
    ) -> Decision:
        """Analyze request and create a decision."""

        message = user_message.casefold()

        if self._is_calculation_request(
            message,
        ):
            expression = self._extract_expression(
                user_message,
            )

            metadata = {
                "expression": expression,
            }

            if learning:
                metadata["learning"] = learning

            strategy, risk_level, confidence = self._adaptive_strategy(
                learning,
            )

            return Decision(
                intent="calculation",
                confidence=confidence,
                requires_tool=True,
                target=self._select_tool(
                    "calculation",
                ),
                priority="normal",
                risk_level=risk_level,
                strategy=strategy,
                explanation=(
                    "Matematiksel iÅŸlem olduÄŸu iÃ§in "
                    "hesaplama aracÄ± kullanÄ±lmalÄ±."
                ),
                plan=[
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
                ],
                metadata=metadata,
            )

        metadata = {}

        if learning:
            metadata["learning"] = learning

        return Decision(
            intent="conversation",
            confidence=0.7,
            requires_tool=False,
            priority="normal",
            risk_level="low",
            strategy="direct_answer",
            explanation="KullanÄ±cÄ± normal sohbet yanÄ±tÄ± istiyor.",
            plan=[
                PlanStep(
                    description="Generate conversational response",
                    action="respond",
                ),
            ],
            metadata=metadata,
        )

    def _adaptive_strategy(
        self,
        learning: dict[str, object] | None,
    ) -> tuple[str, str, float]:
        """Select strategy based on learning confidence."""

        if learning:
            meta = learning.get(
                "meta_recommendation",
            )

            if isinstance(
                meta,
                dict,
            ):
                recommended_strategy = meta.get(
                    "recommended_strategy",
                )

                meta_risk = meta.get(
                    "risk_level",
                )

                confidence_adjustment = meta.get(
                    "confidence_adjustment",
                    0.0,
                )

                if isinstance(
                    recommended_strategy,
                    str,
                ):
                    base_confidence = 0.8 + float(
                        confidence_adjustment,
                    )

                    if recommended_strategy == "safe_tool_execution":
                        return (
                            "safe_tool_execution",
                            meta_risk or "medium",
                            round(
                                min(
                                    0.95,
                                    base_confidence,
                                ),
                                2,
                            ),
                        )

                    if recommended_strategy == "tool_execution":
                        return (
                            "tool_execution",
                            meta_risk or "low",
                            round(
                                min(
                                    0.95,
                                    base_confidence,
                                ),
                                2,
                            ),
                        )

            quality = learning.get(
                "learning_quality",
                1.0,
            )

            if (
                isinstance(
                    quality,
                    (int, float),
                )
                and quality < 0.5
            ):
                return (
                    "safe_tool_execution",
                    "medium",
                    0.75,
                )

            preferred_strategy = learning.get(
                "preferred_strategy",
            )

            confidence = learning.get(
                "strategy_confidence",
                0.0,
            )

            if (
                isinstance(
                    preferred_strategy,
                    str,
                )
                and confidence
            ):
                if preferred_strategy == "safe_tool_execution":
                    return (
                        "safe_tool_execution",
                        "medium",
                        round(
                            min(
                                0.95,
                                0.7 + float(confidence) * 0.25,
                            ),
                            2,
                        ),
                    )

                if preferred_strategy == "tool_execution":
                    return (
                        "tool_execution",
                        "low",
                        round(
                            min(
                                0.95,
                                0.7 + float(confidence) * 0.25,
                            ),
                            2,
                        ),
                    )

            successful_strategies = learning.get(
                "successful_strategies",
                [],
            )

            for strategy in successful_strategies:
                if "safe_tool_execution" in strategy:
                    return (
                        "safe_tool_execution",
                        "medium",
                        0.85,
                    )

                if "tool_execution" in strategy:
                    return (
                        "tool_execution",
                        "low",
                        0.85,
                    )

        if learning and learning.get(
            "has_failures",
        ):
            return (
                "safe_tool_execution",
                "medium",
                0.8,
            )

        return (
            "tool_execution",
            "low",
            0.9,
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
        """Select available tool for intent."""

        if intent == "calculation":
            if self._tools is None:
                return "calculator"

            if self._tools.has(
                "calculator",
            ):
                return "calculator"

        return None

    def _extract_expression(
        self,
        user_message: str,
    ) -> str:
        """Extract mathematical expression."""

        return re.sub(
            r"[^\d+\-*/().]",
            "",
            user_message,
        )
