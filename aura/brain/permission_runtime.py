"""Permission runtime controller for AURA."""

from __future__ import annotations

from aura.brain.models import Decision
from aura.brain.permission_gate import PermissionGate
from aura.brain.permission_request import PermissionRequest
from aura.brain.permission_service import PermissionService


class PermissionRuntime:
    """Runtime permission controller."""

    def __init__(
        self,
        gate: PermissionGate | None = None,
        service: PermissionService | None = None,
    ) -> None:
        self._gate = gate or PermissionGate()
        self._service = service or PermissionService()

    @property
    def service(
        self,
    ) -> PermissionService:
        return self._service

    def check(
        self,
        decision: Decision,
    ) -> bool:
        """Check execution permission."""

        if self._gate.can_execute(
            decision,
        ):
            return True

        request = PermissionRequest(
            capability=decision.intent,
            reason=decision.explanation,
            risk_level=decision.risk_level,
        )

        self._service.create(
            request,
            decision,
        )

        return False

    def approve(
        self,
    ) -> bool:
        """Approve pending request."""

        return self._service.approve()

    def deny(
        self,
    ) -> bool:
        """Deny pending request."""

        return self._service.deny()
