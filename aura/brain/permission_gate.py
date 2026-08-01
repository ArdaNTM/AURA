"""Permission gate for AURA execution."""

from __future__ import annotations

from aura.brain.models import Decision
from aura.brain.permission import PermissionManager


class PermissionGate:
    """Control execution permissions."""

    def __init__(
        self,
        permission_manager: PermissionManager | None = None,
    ) -> None:
        self._permission_manager = permission_manager or PermissionManager()

    @property
    def permission_manager(
        self,
    ) -> PermissionManager:
        """Return permission manager."""

        return self._permission_manager

    def can_execute(
        self,
        decision: Decision,
    ) -> bool:
        """Check whether decision can execute."""

        if not decision.requires_permission:
            return True

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
