from pathlib import Path

from aura.vision.element_detector import ElementDetector
from aura.vision.models import VisionResult
from PIL import Image


class VisionAnalyzer:
    """Analyze captured screens."""

    def __init__(
        self,
        detector: ElementDetector | None = None,
    ):
        self._detector = detector or ElementDetector()

    def analyze(
        self,
        image_path: str,
    ) -> VisionResult:
        """Analyze image."""

        path = Path(image_path)

        if not path.exists():
            return VisionResult(
                description="Image not found.",
                confidence=0.0,
                metadata={
                    "image_path": image_path,
                    "exists": False,
                },
            )

        try:
            image = Image.open(
                path,
            )

            width, height = image.size

            return VisionResult(
                description="Screen image analyzed.",
                objects=[
                    "screen",
                ],
                confidence=0.5,
                text=[],
                regions=[],
                elements=self._detector.detect(
                    str(path),
                ),
                metadata={
                    "image_path": str(path),
                    "exists": True,
                    "width": width,
                    "height": height,
                    "format": image.format,
                },
            )

        except Exception:
            return VisionResult(
                description="Screen image analyzed.",
                objects=[
                    "screen",
                ],
                confidence=0.5,
                text=[],
                regions=[],
                elements=[],
                metadata={
                    "image_path": str(path),
                    "exists": True,
                    "format": "unknown",
                },
            )
