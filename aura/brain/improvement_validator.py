"""Validate autonomous improvement actions."""

from __future__ import annotations

from aura.brain.audit_log import AuditLog
from aura.brain.safety_policy import SafetyPolicy


class ImprovementValidator:
    """Protect autonomous self improvement."""

    def __init__(
        self,
        policy: SafetyPolicy | None = None,
        audit: AuditLog | None = None,
    ) -> None:

        self._policy = policy or SafetyPolicy()

        self._audit = audit or AuditLog()

    @property
    def audit(
        self,
    ) -> AuditLog:
        """Return audit log."""

        return self._audit

    def validate(
        self,
        change_type: str,
        description: str,
    ) -> bool:
        """Validate improvement."""

        allowed = self._policy.is_allowed(
            change_type,
        )

        self._audit.add(
            change_type,
            description,
            allowed,
        )

        return allowed
