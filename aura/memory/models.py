from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class MemoryType(StrEnum):
    CONVERSATION = "conversation"
    USER = "user"
    PROJECT = "project"
    TASK = "task"
    PREFERENCE = "preference"
    EVENT = "event"


@dataclass
class MemoryItem:
    content: str

    memory_type: MemoryType

    importance: float = 0.5

    confidence: float = 0.5

    created_at: datetime = field(default_factory=datetime.now)

    tags: list[str] = field(default_factory=list)

    metadata: dict[str, object] = field(default_factory=dict)

    def score(self) -> float:
        age_days = (datetime.now() - self.created_at).days

        decay = min(
            age_days * 0.01,
            0.5,
        )

        return self.importance + self.confidence - decay
