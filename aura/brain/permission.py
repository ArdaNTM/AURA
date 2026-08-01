"""Permission management for AURA capabilities."""

from __future__ import annotations


class PermissionManager:
    """Manage AURA capability permissions."""

    def __init__(
        self,
        permissions: dict[str, bool] | None = None,
    ) -> None:
        self._permissions = permissions or {}

    @property
    def permissions(
        self,
    ) -> dict[str, bool]:
        """Return current permissions."""

        return self._permissions

    def grant(
        self,
        capability: str,
    ) -> None:
        """Grant permission for a capability."""

        self._permissions[capability] = True

    def revoke(
        self,
        capability: str,
    ) -> None:
        """Revoke permission for a capability."""

        self._permissions[capability] = False

    def is_granted(
        self,
        capability: str,
    ) -> bool:
        """Return whether capability permission is granted."""

        return self._permissions.get(
            capability,
            False,
        )

    def can_execute(
        self,
        capability,
        context_permissions: dict[str, bool] | None = None,
    ) -> bool:
        """Check whether capability can execute."""

        if not capability.requires_permission:
            return True

        permissions = context_permissions or self._permissions

        return permissions.get(
            capability.name,
            False,
        )
