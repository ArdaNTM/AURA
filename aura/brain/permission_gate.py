"""Permission gate for AURA execution."""

from __future__ import annotations

from aura.brain.models import Decision
from aura.brain.permission import PermissionManager
from aura.brain.permission_policy import PermissionPolicy
from aura.brain.safety_policy import SafetyPolicy


class PermissionGate:
    """Control execution permissions."""

    def __init__(
        self,
        permission_manager: PermissionManager | None = None,
        policy: PermissionPolicy | None = None,
        safety_policy: SafetyPolicy | None = None,
    ) -> None:

        self._permission_manager = permission_manager or PermissionManager()

        self._policy = policy or PermissionPolicy()

        self._safety_policy = safety_policy or SafetyPolicy()

    def can_execute(
        self,
        decision: Decision,
    ) -> bool:
        """Check whether decision can execute."""
        safety = self._safety_policy.evaluate(
            decision.intent,
            decision.risk_level,
        )

        if not safety.allowed:
            return False
        policy_result = self._policy.evaluate(
            capability=decision.intent,
            risk_level=decision.risk_level,
            confidence=decision.confidence,
            requires_permission=decision.requires_permission,
        )

        if policy_result.action == "ask":
            return False

        capability = decision.metadata.get(
            "capability",
        )

        if not isinstance(
            capability,
            str,
        ):
            return False

        return self._permission_manager.is_granted(
            capability,
        )
