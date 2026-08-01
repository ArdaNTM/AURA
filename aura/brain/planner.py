"""AURA task planner."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aura.brain.capability import CapabilityRegistry
from aura.brain.decision_context import DecisionContext
from aura.brain.intent import IntentEngine
from aura.brain.models import Decision, IntentAnalysis
from aura.brain.plan_builder import PlanBuilder

if TYPE_CHECKING:
    from aura.core.tools import ToolRegistry


class Planner:
    """Create decisions from user requests."""

    def __init__(
        self,
        tools: ToolRegistry | None = None,
        plan_builder: PlanBuilder | None = None,
        intent_engine: IntentEngine | None = None,
        capability_registry: CapabilityRegistry | None = None,
    ) -> None:
        self._tools = tools
        self._plan_builder = plan_builder or PlanBuilder()
        self._intent_engine = intent_engine or IntentEngine()
        self._capabilities = capability_registry or CapabilityRegistry()

    def decide(
        self,
        user_message: str,
        learning: dict[str, object] | None = None,
    ) -> Decision:
        """Analyze request and create a decision."""

        analysis = self._intent_engine.classify(
            user_message,
        )

        capability = self._capabilities.get(
            analysis.intent,
        )

        if capability.name == "calculation":
            return self._build_calculation(
                capability,
                analysis,
                learning,
            )

        return self._build_conversation(
            capability,
            learning,
        )

    def decide_with_context(
        self,
        context: DecisionContext,
    ) -> Decision:
        """Analyze request using full decision context."""

        return self.decide(
            context.user_message,
            learning=context.learning,
        )

    def _build_calculation(
        self,
        capability,
        analysis: IntentAnalysis,
        learning: dict[str, object] | None,
    ) -> Decision:
        """Create calculation decision."""

        expression = str(
            analysis.entities.get(
                "expression",
                "",
            )
        )

        metadata: dict[str, object] = {
            "expression": expression,
            "capability": capability.name,
            "requires_permission": capability.requires_permission,
            "capability_risk_level": capability.risk_level,
            "intent_confidence": analysis.confidence,
            "intent_entities": analysis.entities,
        }

        if learning:
            metadata["learning"] = learning

        strategy, risk_level, confidence = self._adaptive_strategy(
            learning,
        )

        return Decision(
            intent=capability.name,
            confidence=confidence,
            requires_tool=capability.requires_tool,
            requires_permission=capability.requires_permission,
            target=capability.default_tool,
            priority="normal",
            risk_level=risk_level,
            strategy=strategy,
            explanation=(
                "Matematiksel işlem olduğu için " "hesaplama aracı kullanılmalı."
            ),
            plan=self._plan_builder.build_calculation(
                expression=expression,
            ),
            metadata=metadata,
        )

    def _build_conversation(
        self,
        capability,
        learning: dict[str, object] | None,
    ) -> Decision:
        """Create conversation decision."""

        metadata: dict[str, object] = {
            "capability": capability.name,
            "requires_permission": capability.requires_permission,
            "capability_risk_level": capability.risk_level,
        }

        if learning:
            metadata["learning"] = learning

        return Decision(
            intent=capability.name,
            confidence=0.7,
            requires_tool=capability.requires_tool,
            requires_permission=capability.requires_permission,
            target=capability.default_tool,
            priority="normal",
            risk_level=capability.risk_level,
            strategy="direct_answer",
            explanation="Kullanıcı normal sohbet yanıtı istiyor.",
            plan=self._plan_builder.build_conversation(),
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
                strategy = meta.get(
                    "recommended_strategy",
                )

                risk = meta.get(
                    "risk_level",
                )

                adjustment = float(
                    meta.get(
                        "confidence_adjustment",
                        0.0,
                    )
                )

                if strategy == "safe_tool_execution":
                    return (
                        strategy,
                        risk or "medium",
                        round(
                            min(
                                0.95,
                                0.8 + adjustment,
                            ),
                            2,
                        ),
                    )

                if strategy == "tool_execution":
                    return (
                        strategy,
                        risk or "low",
                        round(
                            min(
                                0.95,
                                0.8 + adjustment,
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

            preferred = learning.get(
                "preferred_strategy",
            )

            confidence = float(
                learning.get(
                    "strategy_confidence",
                    0.0,
                )
            )

            if preferred == "safe_tool_execution":
                return (
                    preferred,
                    "medium",
                    round(
                        min(
                            0.95,
                            0.7 + confidence * 0.25,
                        ),
                        2,
                    ),
                )

            if preferred == "tool_execution":
                return (
                    preferred,
                    "low",
                    round(
                        min(
                            0.95,
                            0.7 + confidence * 0.25,
                        ),
                        2,
                    ),
                )

            for strategy in learning.get(
                "successful_strategies",
                [],
            ):
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
