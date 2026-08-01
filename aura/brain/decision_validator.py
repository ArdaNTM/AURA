"""Decision validation for AURA."""

from __future__ import annotations

from dataclasses import dataclass

from aura.brain.capability import CapabilityRegistry
from aura.brain.models import Decision


@dataclass(frozen=True)
class ValidationResult:
    """Result of decision validation."""

    valid: bool

    reason: str = ""


class DecisionValidator:
    """Validate decisions before execution."""

    def __init__(
        self,
        capabilities: CapabilityRegistry,
    ) -> None:
        self._capabilities = capabilities

    def validate(
        self,
        decision: Decision,
    ) -> ValidationResult:
        """Validate a decision."""

        if not self._capabilities.has(
            decision.intent,
        ):
            return ValidationResult(
                valid=False,
                reason=f"Unknown capability '{decision.intent}'.",
            )

        capability = self._capabilities.get(
            decision.intent,
        )

        if not capability.requires_tool:
            return ValidationResult(
                valid=True,
            )

        if not decision.target:
            return ValidationResult(
                valid=False,
                reason="Tool required but no target specified.",
            )

        if not self._capabilities.validate_tool(
            decision.intent,
            decision.target,
        ):
            return ValidationResult(
                valid=False,
                reason=(
                    f"Tool '{decision.target}' "
                    f"is not allowed for capability "
                    f"'{decision.intent}'."
                ),
            )

        if not self._capabilities.is_available(
            decision.intent,
        ):
            return ValidationResult(
                valid=False,
                reason=(f"Capability '{decision.intent}' " "is unavailable."),
            )

        return ValidationResult(
            valid=True,
        )
