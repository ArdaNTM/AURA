"""Prompt evolution system for AURA."""

from __future__ import annotations

from aura.brain.learning import LearningContext


class PromptEvolution:
    """Generate adaptive LLM instructions from experience."""

    def evolve(
        self,
        context: LearningContext,
    ) -> dict[str, object]:
        """Create improved prompt instructions."""

        instructions: list[str] = []

        strategy = context.preferred_strategy()

        if strategy:
            instructions.append(
                f"Prefer strategy: {strategy}",
            )

        if context.has_previous_failure():
            instructions.append(
                "Analyze previous failures before deciding.",
            )

            instructions.append(
                "Verify assumptions before execution.",
            )

        quality = context.learning_quality()

        if quality >= 0.8:
            instructions.append(
                "Maintain successful reasoning patterns.",
            )

        else:
            instructions.append(
                "Use conservative reasoning.",
            )

        return {
            "instructions": instructions,
            "learning_quality": quality,
            "preferred_strategy": strategy,
        }
