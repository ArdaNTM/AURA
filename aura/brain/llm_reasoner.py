"""LLM reasoning layer for AURA."""

from __future__ import annotations

import json

from aura.ai.llm_provider import LLMProvider
from aura.brain.reasoning import ReasoningResult


class LLMReasoner:
    """Convert LLM responses into structured reasoning."""

    def __init__(
        self,
        provider: LLMProvider,
    ) -> None:
        self._provider = provider

    @property
    def provider(
        self,
    ) -> LLMProvider:
        """Return LLM provider."""

        return self._provider

    def analyze(
        self,
        user_message: str,
    ) -> ReasoningResult:
        """Analyze user request with LLM."""

        response = self._provider.complete(
            self._build_prompt(
                user_message,
            ),
        )

        return self._parse_response(
            response,
        )

    def _build_prompt(
        self,
        user_message: str,
    ) -> str:
        """Build reasoning prompt."""

        return (
            "Analyze the user request and return JSON.\n"
            "Required fields:\n"
            "intent, goal, capability, confidence, risk_level\n\n"
            f"User request:\n{user_message}"
        )

    def _parse_response(
        self,
        response: str,
    ) -> ReasoningResult:
        """Parse LLM JSON response."""

        try:
            data = json.loads(
                response,
            )

        except json.JSONDecodeError:
            return ReasoningResult(
                intent="unknown",
                goal=response,
                confidence=0.0,
            )

        return ReasoningResult(
            intent=str(
                data.get(
                    "intent",
                    "unknown",
                )
            ),
            goal=str(
                data.get(
                    "goal",
                    "",
                )
            ),
            capability=data.get(
                "capability",
            ),
            confidence=float(
                data.get(
                    "confidence",
                    0.0,
                )
            ),
            risk_level=str(
                data.get(
                    "risk_level",
                    "low",
                )
            ),
            entities=data.get(
                "entities",
                {},
            ),
        )
