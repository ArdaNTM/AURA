"""Permission request models for AURA."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PermissionRequest:
    """Represents a pending permission request."""

    capability: str

    reason: str

    risk_level: str

    approved: bool = False

    def approve(
        self,
    ) -> None:
        """Approve permission request."""

        self.approved = True

    def deny(
        self,
    ) -> None:
        """Deny permission request."""

        self.approved = False
