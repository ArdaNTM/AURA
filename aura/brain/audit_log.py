"""Execution audit logging."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AuditEntry:
    action: str
    success: bool
    approved: bool
    details: str
    timestamp: datetime


class AuditLog:
    """Store security events."""

    def __init__(self):
        self._entries: list[AuditEntry] = []

    @property
    def entries(self):
        return self._entries

    def record(
        self,
        action: str,
        success: bool,
        approved: bool,
        details: str = "",
    ):
        self._entries.append(
            AuditEntry(
                action=action,
                success=success,
                approved=approved,
                details=details,
                timestamp=datetime.now(),
            )
        )

    def add(
        self,
        change_type: str,
        description: str,
        allowed: bool,
    ) -> None:
        """Record improvement audit event."""

        self.record(
            action=change_type,
            success=allowed,
            approved=allowed,
            details=description,
        )
