"""AURA task planner."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aura.brain.capability import CapabilityRegistry
from aura.brain.decision_context import DecisionContext
from aura.brain.intent import IntentEngine
from aura.brain.llm_reasoner import LLMReasoner
from aura.brain.models import Decision, IntentAnalysis
from aura.brain.plan_builder import PlanBuilder
from aura.brain.tool_discovery import ToolDiscovery

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
        tool_discovery: ToolDiscovery | None = None,
        llm_reasoner: LLMReasoner | None = None,
    ) -> None:
        self._tools = tools
        self._plan_builder = plan_builder or PlanBuilder()
        self._intent_engine = intent_engine or IntentEngine()
        self._capabilities = capability_registry or CapabilityRegistry(
            tools=tools,
        )
        self._tool_discovery = tool_discovery or ToolDiscovery(
            tools,
        )
        self._llm_reasoner = llm_reasoner

    @property
    def capabilities(
        self,
    ) -> CapabilityRegistry:
        """Return capability registry."""

        return self._capabilities

    @property
    def tool_discovery(
        self,
    ) -> ToolDiscovery:
        """Return tool discovery service."""

        return self._tool_discovery

    @property
    def llm_reasoner(
        self,
    ) -> LLMReasoner | None:
        """Return LLM reasoner."""

        return self._llm_reasoner

    def _resolve_tool(
        self,
        capability,
    ) -> str | None:
        """Resolve executable tool for capability."""

        discovered = self._tool_discovery.find_tool(
            capability.name,
        )

        if discovered:
            return discovered

        return capability.default_tool

    def _add_tool_metadata(
        self,
        metadata: dict[str, object],
        capability,
    ) -> None:
        """Add selected tool information."""

        tool = self._resolve_tool(
            capability,
        )

        metadata["selected_tool"] = tool
        metadata["tool_discovered"] = tool is not None

    def decide(
        self,
        user_message: str,
        learning: dict[str, object] | None = None,
    ) -> Decision:
        """Analyze request and create a decision."""

        analysis = self._intent_analysis(
            user_message,
        )

        capability = self._capabilities.get(
            analysis.intent,
        )

        if capability.requires_permission:
            return self._build_permission_capability(
                capability,
                learning,
            )

        elif (
            capability.requires_tool
            and self._tools is not None
            and not self._tool_discovery.is_available(
                capability.name,
            )
        ):
            return self._build_unavailable_capability(
                capability,
                learning,
            )

        if capability.name == "calculation":
            return self._build_calculation(
                capability,
                analysis,
                learning,
            )

        if capability.requires_tool:
            return self._build_tool_capability(
                capability,
                learning,
            )

        return self._build_conversation(
            capability,
            learning,
        )

    def _build_permission_capability(
        self,
        capability,
        learning,
    ) -> Decision:
        """Create permission-required decision."""

        metadata = {
            "capability": capability.name,
            "requires_permission": True,
            "capability_risk_level": capability.risk_level,
        }
        self._add_tool_metadata(
            metadata,
            capability,
        )

        if learning:
            metadata["learning"] = learning

        return Decision(
            intent=capability.name,
            confidence=0.8,
            requires_tool=True,
            requires_permission=True,
            target=self._resolve_tool(
                capability,
            ),
            priority="normal",
            risk_level=capability.risk_level,
            strategy="permission_required",
            explanation=(f"{capability.name} capability requires permission."),
            plan=self._plan_builder.build_tool_execution(
                tool_name=self._resolve_tool(
                    capability,
                ),
                parameters={},
            ),
            metadata=metadata,
        )

    def _build_tool_capability(
        self,
        capability,
        learning,
    ) -> Decision:
        """Create generic tool execution decision."""

        metadata: dict[str, object] = {
            "capability": capability.name,
            "requires_permission": capability.requires_permission,
            "capability_risk_level": capability.risk_level,
        }

        self._add_tool_metadata(
            metadata,
            capability,
        )

        if learning:
            metadata["learning"] = learning

        tool_name = self._resolve_tool(
            capability,
        )

        return Decision(
            intent=capability.name,
            confidence=0.8,
            requires_tool=True,
            requires_permission=capability.requires_permission,
            target=tool_name,
            priority="normal",
            risk_level=capability.risk_level,
            strategy="tool_execution",
            explanation=(f"{capability.name} capability requires tool execution."),
            plan=self._plan_builder.build_tool_execution(
                tool_name=tool_name,
                parameters={},
            ),
            metadata=metadata,
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

        self._add_tool_metadata(
            metadata,
            capability,
        )

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
            target=self._resolve_tool(
                capability,
            ),
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
        self._add_tool_metadata(
            metadata,
            capability,
        )

        if learning:
            metadata["learning"] = learning

        return Decision(
            intent=capability.name,
            confidence=0.7,
            requires_tool=capability.requires_tool,
            requires_permission=capability.requires_permission,
            target=self._resolve_tool(
                capability,
            ),
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

    def _build_unavailable_capability(
        self,
        capability,
        learning: dict[str, object] | None,
    ) -> Decision:
        """Create decision when capability is unavailable."""

        metadata: dict[str, object] = {
            "capability": capability.name,
            "available": False,
        }

        if learning:
            metadata["learning"] = learning

        return Decision(
            intent=capability.name,
            confidence=0.0,
            requires_tool=False,
            target=None,
            priority="normal",
            risk_level=capability.risk_level,
            strategy="unavailable_capability",
            explanation=(f"Capability '{capability.name}' " "is not available."),
            metadata=metadata,
        )

    def _intent_analysis(
        self,
        user_message: str,
    ) -> IntentAnalysis:
        """Resolve intent using LLM when available."""

        if self._llm_reasoner:

            reasoning = self._llm_reasoner.analyze(
                user_message,
            )

            return IntentAnalysis(
                intent=reasoning.intent,
                confidence=reasoning.confidence,
                entities=reasoning.entities,
            )

        return self._intent_engine.classify(
            user_message,
        )
