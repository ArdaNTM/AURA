"""Reflection engine for AURA agent loop."""

from __future__ import annotations

from aura.brain.observation import Observation
from aura.brain.reflection import Reflection


class ReflectionEngine:
    """Generate reflection from observations."""

    def reflect(
        self,
        observation: Observation,
    ) -> Reflection:
        """Create reflection result."""

        if not observation.success:
            return Reflection(
                success=False,
                summary="Execution failed.",
                improvements=[
                    "Retry execution with a different strategy.",
                ],
                metadata={
                    "retry_needed": True,
                },
            )

        if observation.score < 1.0:
            return Reflection(
                success=True,
                summary="Execution completed with room for improvement.",
                improvements=[
                    "Improve output quality.",
                ],
                metadata={
                    "retry_needed": False,
                },
            )

        return Reflection(
            success=True,
            summary="Execution completed successfully.",
            metadata={
                "retry_needed": False,
            },
        )
