from dataclasses import dataclass, field

from aura.vision.ui_element import UIElement


@dataclass
class VisionResult:
    """Result of screen analysis."""

    description: str

    objects: list[str] = field(
        default_factory=list,
    )

    confidence: float = 0.0

    text: list[str] = field(
        default_factory=list,
    )

    regions: list[dict[str, object]] = field(
        default_factory=list,
    )

    elements: list[UIElement] = field(
        default_factory=list,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
