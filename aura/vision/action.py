from dataclasses import dataclass


@dataclass
class VisionAction:
    """Action generated from visual understanding."""

    action: str

    x: int | None = None

    y: int | None = None

    target: str | None = None

    confidence: float = 0.0
