"""Research data models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ResearchResult:
    """Collected research result."""

    query: str

    title: str

    content: str

    source: str = ""

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
