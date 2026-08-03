"""Safety rules for autonomous improvement."""

from __future__ import annotations


class SafetyPolicy:
    """Define allowed and restricted improvements."""

    SAFE_CHANGES = {
        "strategy",
        "confidence",
        "prompt",
        "tool_preference",
    }

    HIGH_RISK_CHANGES = {
        "core_code",
        "security",
        "permission_system",
        "execution_guard",
    }

    def is_allowed(
        self,
        change_type: str,
    ) -> bool:
        """Check whether change is allowed."""

        return change_type in self.SAFE_CHANGES

    def requires_permission(
        self,
        change_type: str,
    ) -> bool:
        """Check whether approval is required."""

        return change_type in self.HIGH_RISK_CHANGES
