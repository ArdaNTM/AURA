from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class UIElement:
    """Detected user interface element."""

    name: str

    element_type: str

    x: int

    y: int

    confidence: float = 0.0

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
