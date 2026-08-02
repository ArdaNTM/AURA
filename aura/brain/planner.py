"""AURA task planner."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aura.brain.capability import CapabilityRegistry
from aura.brain.confidence_fusion import ConfidenceFusion
from aura.brain.decision_context import DecisionContext
from aura.brain.intent import IntentEngine
from aura.brain.learning_profile import LearningProfile
from aura.brain.llm_reasoner import LLMReasoner
from aura.brain.llm_recovery import LLMRecovery
from aura.brain.llm_validator import LLMValidator
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
        llm_recovery: LLMRecovery | None = None,
        llm_validator: LLMValidator | None = None,
        confidence_fusion: ConfidenceFusion | None = None,
        llm_confidence_threshold: float | None = None,
        confidence_guard_threshold: float = 0.5,
        learning_profile: LearningProfile | None = None,
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
        self._llm_recovery = llm_recovery or LLMRecovery(
            self._intent_engine,
        )
        self._llm_validator = llm_validator
        self._confidence_fusion = confidence_fusion or ConfidenceFusion()
        self._llm_confidence_threshold = llm_confidence_threshold
        self._confidence_guard_threshold = confidence_guard_threshold
        self._learning_profile = learning_profile

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
            learning,
        )

        capability = self._capabilities.get(
            analysis.intent,
        )

        if (
            analysis.source_confidence is not None
            and analysis.source_confidence < self._confidence_guard_threshold
            and capability.risk_level == "high"
        ):
            return self._build_risk_review_decision(
                capability,
                learning,
            )

        if (
            analysis.source_confidence is not None
            and analysis.source_confidence < self._confidence_guard_threshold
        ):
            return self._build_low_confidence_decision(
                capability,
                learning,
            )

        if capability.name == "filesystem":
            return self._build_filesystem(
                capability,
                user_message,
                learning,
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

        if capability.name == "filesystem":
            return self._build_filesystem(
                capability,
                user_message,
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
            "llm_permission_checked": True,
        }
        self._add_tool_metadata(
            metadata,
            capability,
        )

        parameters = {}

        if capability.name == "filesystem":
            parameters = {
                "operation": "write",
                "path": "untitled.txt",
                "content": "",
            }

        if learning:
            metadata["learning"] = learning

        reasoning_risk = capability.risk_level
        reasoning_confidence = 0.8

        if learning:
            reasoning = learning.get(
                "llm_reasoning",
            )

            if isinstance(
                reasoning,
                dict,
            ):
                reasoning_risk = reasoning.get(
                    "risk_level",
                    reasoning_risk,
                )

                reasoning_confidence = reasoning.get(
                    "confidence",
                    reasoning_confidence,
                )
        return Decision(
            intent=capability.name,
            confidence=reasoning_confidence,
            requires_tool=True,
            requires_permission=True,
            target=self._resolve_tool(
                capability,
            ),
            priority="normal",
            risk_level=reasoning_risk,
            strategy="permission_required",
            explanation=(f"{capability.name} capability requires permission."),
            plan=self._plan_builder.build_tool_execution(
                tool_name=self._resolve_tool(
                    capability,
                ),
                parameters=parameters,
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

        if analysis.source_confidence is not None:
            metadata["llm_confidence"] = analysis.source_confidence

        metadata["final_confidence"] = analysis.confidence

        self._add_tool_metadata(
            metadata,
            capability,
        )

        if learning:
            metadata["learning"] = learning

        strategy, risk_level, confidence = self._adaptive_strategy(
            learning,
            capability.name,
        )

        if learning is None and not self._learning_profile:
            confidence = analysis.confidence

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

    def _get_learning_confidence(
        self,
        learning: dict[str, object] | None,
    ) -> float | None:
        """Extract learning confidence signal."""

        if not learning:
            return None

        confidence = learning.get(
            "strategy_confidence",
        )

        if isinstance(
            confidence,
            (int, float),
        ):
            return float(
                confidence,
            )

        return None

    def _get_confidence_threshold(
        self,
    ) -> float:
        """Return adaptive confidence threshold."""

        if self._learning_profile:
            return self._learning_profile.calibrated_confidence_threshold()

        if self._llm_confidence_threshold is not None:
            return self._llm_confidence_threshold

        return 0.75

    def _adaptive_strategy(
        self,
        learning: dict[str, object] | None,
        skill_name: str,
    ) -> tuple[str, str, float]:
        """Select strategy based on learning confidence."""

        profile = None

        if learning:
            profile = learning.get(
                "profile",
            )

        if self._learning_profile:
            skill_score = self._learning_profile.skill_scores.get(
                skill_name,
            )

            if skill_score is not None:

                if skill_score < 0.5:
                    return (
                        "safe_tool_execution",
                        "medium",
                        0.75,
                    )

                if skill_score > 0.9:
                    return (
                        "tool_execution",
                        "low",
                        0.95,
                    )

            best_strategy = self._learning_profile.best_strategy()

            if best_strategy == "safe_tool_execution":
                return (
                    "safe_tool_execution",
                    "medium",
                    0.85,
                )

            if best_strategy == "tool_execution":
                return (
                    "tool_execution",
                    "low",
                    0.85,
                )

        if isinstance(profile, dict):

            confidence_error = profile.get(
                "confidence_error",
                0.0,
            )

            if confidence_error > 0.35:
                return (
                    "safe_tool_execution",
                    "medium",
                    0.75,
                )

        if learning:

            self_evaluation = learning.get(
                "self_evaluation",
            )

            if isinstance(
                self_evaluation,
                dict,
            ):
                weakest_skill = self_evaluation.get(
                    "weakest_skill",
                )

                if weakest_skill == skill_name:
                    return (
                        "safe_tool_execution",
                        "medium",
                        0.75,
                    )

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
        learning: dict[str, object] | None = None,
    ) -> IntentAnalysis:
        """Resolve intent using LLM with fallback."""

        if self._llm_reasoner:

            reasoning = self._llm_reasoner.analyze(
                user_message,
            )

            if self._llm_validator:

                validation = self._llm_validator.validate(
                    reasoning,
                )

                if not validation.valid:
                    return self._llm_recovery.recover(
                        reasoning,
                        user_message,
                    )

            if reasoning.confidence < self._get_confidence_threshold():
                fallback = self._intent_engine.classify(
                    user_message,
                )

                fallback.source_confidence = reasoning.confidence

                return fallback

            intent_analysis = self._intent_engine.classify(
                user_message,
            )

            final_confidence = self._confidence_fusion.combine(
                llm_confidence=reasoning.confidence,
                intent_confidence=intent_analysis.confidence,
                learning_confidence=self._get_learning_confidence(
                    learning,
                ),
            )

            return IntentAnalysis(
                intent=reasoning.intent,
                confidence=final_confidence,
                entities=reasoning.entities,
                source_confidence=reasoning.confidence,
            )

        return self._intent_engine.classify(
            user_message,
        )

    def _build_low_confidence_decision(
        self,
        capability,
        learning,
    ) -> Decision:
        """Create safe decision for uncertain intent."""

        metadata = {
            "capability": capability.name,
            "confidence_guard": True,
        }

        if learning:
            metadata["learning"] = learning

        return Decision(
            intent=capability.name,
            confidence=0.0,
            requires_tool=False,
            target=None,
            priority="normal",
            risk_level="medium",
            strategy="confidence_review",
            explanation=("Confidence level is too low for execution."),
            confidence_reason=("LLM confidence below execution threshold."),
            routing_reason=("Execution blocked and sent to review."),
            metadata=metadata,
        )

    def _build_risk_review_decision(
        self,
        capability,
        learning,
    ) -> Decision:
        """Create review decision for risky uncertain actions."""

        metadata = {
            "capability": capability.name,
            "risk_review": True,
            "confidence_guard": True,
        }

        if learning:
            metadata["learning"] = learning

        return Decision(
            intent=capability.name,
            confidence=0.0,
            requires_tool=False,
            requires_permission=True,
            target=None,
            priority="high",
            risk_level="high",
            strategy="risk_review",
            explanation=(
                "High risk capability requires review " "because confidence is low."
            ),
            confidence_reason=("Low confidence detected."),
            routing_reason=("High risk capability requires approval."),
            metadata=metadata,
        )

    def _build_filesystem(
        self,
        capability,
        user_message,
        learning,
    ):
        metadata = {
            "operation": "write",
            "path": self._extract_filename(user_message),
            "content": "",
        }

        return Decision(
            intent="filesystem",
            confidence=0.8,
            requires_tool=True,
            requires_permission=True,
            target="filesystem",
            priority="normal",
            risk_level="medium",
            strategy="tool_execution",
            explanation="Filesystem operation requires tool execution.",
            plan=self._plan_builder.build_tool_execution(
                tool_name="filesystem",
                parameters=metadata,
            ),
            metadata={
                "capability": "filesystem",
                "requires_permission": True,
            },
        )

    def _extract_filename(
        self,
        message: str,
    ) -> str:
        """Extract target filename from filesystem request."""

        tokens = message.split()

        for token in tokens:
            if "." in token:
                return token.strip("\"'.,")

        return "untitled.txt"
