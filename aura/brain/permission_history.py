"""Permission audit history models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PermissionHistoryEntry:
    """Represents a permission decision record."""

    capability: str

    reason: str

    risk_level: str

    approved: bool

    timestamp: datetime
