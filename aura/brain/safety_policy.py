"""Final safety policy layer for AURA."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SafetyDecision:
    allowed: bool
    requires_permission: bool
    reason: str


class SafetyPolicy:
    """Evaluate execution safety."""

    HIGH_RISK_ACTIONS = {
        "delete_file",
        "format_disk",
        "shutdown",
        "credential_access",
    }

    MEDIUM_RISK_ACTIONS = {
        "write_file",
        "execute_command",
        "install_package",
    }

    def evaluate(
        self,
        action: str,
        risk_level: str | None = None,
    ) -> SafetyDecision:
        """Check action safety."""

        normalized = action.lower()

        if normalized in self.HIGH_RISK_ACTIONS:
            return SafetyDecision(
                allowed=False,
                requires_permission=True,
                reason="High risk action requires approval.",
            )

        if normalized in self.MEDIUM_RISK_ACTIONS:
            return SafetyDecision(
                allowed=True,
                requires_permission=True,
                reason="Medium risk action requires audit.",
            )

        if risk_level == "HIGH":
            return SafetyDecision(
                allowed=False,
                requires_permission=True,
                reason="High risk decision blocked.",
            )

        return SafetyDecision(
            allowed=True,
            requires_permission=False,
            reason="Safe execution.",
        )

    def is_allowed(
        self,
        change_type: str,
    ) -> bool:
        """Check whether autonomous improvement is allowed."""

        blocked_changes = {
            "security",
            "permission",
            "safety",
            "rollback",
        }

        return change_type not in blocked_changes
