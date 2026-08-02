"""Reflection engine for AURA agent loop."""

from __future__ import annotations

from aura.brain.models import Decision
from aura.brain.observation import Observation
from aura.brain.reflection import Reflection


class ReflectionEngine:
    """Generate reflection from observations."""

    def reflect(
        self,
        observation: Observation,
        decision: Decision | None = None,
    ) -> Reflection:
        """Create reflection result."""

        context = {}

        if decision:
            context = {
                "intent": decision.intent,
                "strategy": decision.strategy,
            }

        if not observation.success:
            retry_strategy = self._select_retry_strategy(
                decision,
            )

            return Reflection(
                success=False,
                summary="Execution failed.",
                quality_score=0.0,
                quality_level="low",
                intent=context.get(
                    "intent",
                ),
                strategy=context.get(
                    "strategy",
                ),
                retry_needed=True,
                retry_strategy=retry_strategy,
                improvements=[
                    "Retry execution with a different strategy.",
                ],
                metadata={
                    "retry_needed": True,
                    "retry_strategy": retry_strategy,
                    "decision": context,
                },
            )

        if observation.score < 1.0:
            return Reflection(
                success=True,
                summary="Execution completed with room for improvement.",
                quality_score=0.5,
                quality_level="medium",
                intent=context.get(
                    "intent",
                ),
                strategy=context.get(
                    "strategy",
                ),
                retry_needed=False,
                improvements=[
                    "Improve output quality.",
                ],
                metadata={
                    "retry_needed": False,
                    "decision": context,
                },
            )

        return Reflection(
            success=True,
            summary="Execution completed successfully.",
            quality_score=1.0,
            quality_level="high",
            intent=context.get(
                "intent",
            ),
            strategy=context.get(
                "strategy",
            ),
            retry_needed=False,
            metadata={
                "retry_needed": False,
                "decision": context,
            },
        )

    def _select_retry_strategy(
        self,
        decision: Decision | None,
    ) -> str:
        """Select strategy for retry execution."""

        if decision and decision.strategy == "tool_execution":
            return "safe_tool_execution"

        if decision and decision.strategy == "safe_tool_execution":
            return "tool_execution"

        return "safe_tool_execution"
