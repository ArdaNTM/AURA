from dataclasses import dataclass, field


@dataclass
class VisionResult:
    """Result of screen analysis."""

    description: str

    objects: list[str] = field(
        default_factory=list,
    )

    confidence: float = 0.0

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
