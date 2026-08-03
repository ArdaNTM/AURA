"""Audit records for autonomous changes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AuditEntry:
    """Single improvement audit entry."""

    change_type: str

    description: str

    approved: bool

    timestamp: datetime


@dataclass
class AuditLog:
    """Store autonomous change history."""

    entries: list[AuditEntry] = field(
        default_factory=list,
    )

    def add(
        self,
        change_type: str,
        description: str,
        approved: bool,
    ) -> None:
        """Record change attempt."""

        self.entries.append(
            AuditEntry(
                change_type=change_type,
                description=description,
                approved=approved,
                timestamp=datetime.now(),
            ),
        )
