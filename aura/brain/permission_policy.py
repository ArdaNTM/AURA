"""Adaptive permission policy for AURA."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class PermissionDecision:
    """Result of permission policy evaluation."""

    action: str

    reason: str


class PermissionPolicy:
    """Evaluate whether an action should be allowed."""

    def evaluate(
        self,
        capability: str,
        risk_level: str,
        confidence: float,
        requires_permission: bool,
    ) -> PermissionDecision:
        """Evaluate execution policy."""

        if not requires_permission:
            return PermissionDecision(
                action="allow",
                reason="Capability does not require permission.",
            )

        if capability == "computer":
            return PermissionDecision(
                action="ask",
                reason="Computer control requires user confirmation.",
            )

        if capability == "filesystem":
            return PermissionDecision(
                action="ask",
                reason="Filesystem access requires user confirmation.",
            )

        if risk_level == "high":
            return PermissionDecision(
                action="ask",
                reason="High risk operation requires confirmation.",
            )

        if confidence < 0.5:
            return PermissionDecision(
                action="ask",
                reason="Low confidence requires confirmation.",
            )

        return PermissionDecision(
            action="allow",
            reason="Permission policy allowed execution.",
        )
