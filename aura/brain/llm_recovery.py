"""Recovery layer for invalid LLM reasoning."""

from __future__ import annotations

from aura.brain.intent import IntentEngine
from aura.brain.models import IntentAnalysis
from aura.brain.reasoning import ReasoningResult


class LLMRecovery:
    """Recover from invalid LLM reasoning."""

    def __init__(
        self,
        intent_engine: IntentEngine | None = None,
    ) -> None:
        self._intent_engine = intent_engine or IntentEngine()

    def recover(
        self,
        reasoning: ReasoningResult,
        user_message: str,
    ) -> IntentAnalysis:
        """Fallback to classic intent analysis."""

        return self._intent_engine.classify(
            user_message,
        )
