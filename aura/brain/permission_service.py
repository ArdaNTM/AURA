"""Permission lifecycle service."""

from __future__ import annotations

from aura.brain.models import Decision
from aura.brain.permission_request import PermissionRequest


class PermissionService:
    """Manage pending permission requests."""

    def __init__(self) -> None:
        self._pending: PermissionRequest | None = None
        self._decision: Decision | None = None

    @property
    def pending(
        self,
    ) -> PermissionRequest | None:
        """Return pending request."""

        return self._pending

    @property
    def decision(
        self,
    ) -> Decision | None:
        """Return pending decision."""

        return self._decision

    def create(
        self,
        request: PermissionRequest,
        decision: Decision | None = None,
    ) -> None:
        """Store permission request."""

        self._pending = request
        self._decision = decision

    def approve(
        self,
    ) -> bool:
        """Approve pending request."""

        if self._pending is None:
            return False

        self._pending.approve()

        return True

    def deny(
        self,
    ) -> bool:
        """Deny pending request."""

        if self._pending is None:
            return False

        self._pending.deny()

        return True

    def clear(
        self,
    ) -> None:
        """Remove pending permission state."""

        self._pending = None
        self._decision = None
