"""Validation layer for LLM reasoning results."""

from __future__ import annotations

from dataclasses import dataclass

from aura.brain.capability import CapabilityRegistry
from aura.brain.reasoning import ReasoningResult


@dataclass(
    frozen=True,
)
class LLMValidationResult:
    """Result of LLM reasoning validation."""

    valid: bool

    reason: str = ""


class LLMValidator:
    """Validate structured LLM reasoning."""

    def __init__(
        self,
        capabilities: CapabilityRegistry,
    ) -> None:
        self._capabilities = capabilities

    def validate(
        self,
        reasoning: ReasoningResult,
    ) -> LLMValidationResult:

        if not self._capabilities.has(
            reasoning.intent,
        ):
            return LLMValidationResult(
                valid=False,
                reason=f"Unknown intent '{reasoning.intent}'.",
            )

        if not isinstance(
            reasoning.entities,
            dict,
        ):
            return LLMValidationResult(
                valid=False,
                reason="Entities must be an object.",
            )

        capability = self._capabilities.get(
            reasoning.intent,
        )

        if reasoning.capability:

            if not self._capabilities.has(
                reasoning.capability,
            ):
                return LLMValidationResult(
                    valid=False,
                    reason=(f"Unknown capability " f"'{reasoning.capability}'."),
                )

            if reasoning.capability != capability.name:
                return LLMValidationResult(
                    valid=False,
                    reason=(
                        "LLM capability mismatch: "
                        f"{reasoning.capability}"
                        f" != {capability.name}"
                    ),
                )
        if reasoning.confidence < 0.0:
            return LLMValidationResult(
                valid=False,
                reason="Confidence cannot be negative.",
            )

        if reasoning.confidence > 1.0:
            return LLMValidationResult(
                valid=False,
                reason="Confidence cannot exceed 1.0.",
            )

        if reasoning.risk_level not in (
            "low",
            "medium",
            "high",
        ):
            return LLMValidationResult(
                valid=False,
                reason=(f"Invalid risk level " f"'{reasoning.risk_level}'."),
            )

        return LLMValidationResult(
            valid=True,
        )
