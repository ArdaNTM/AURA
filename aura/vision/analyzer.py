from pathlib import Path

from aura.vision.models import VisionResult


class VisionAnalyzer:
    """Analyze captured screens."""

    def analyze(
        self,
        image_path: str,
    ) -> VisionResult:
        """Analyze image."""

        path = Path(image_path)

        if not path.exists():
            return VisionResult(
                description="Image not found.",
                objects=[],
                confidence=0.0,
            )

        return VisionResult(
            description="Screen image analyzed.",
            objects=[
                "screen",
            ],
            confidence=0.5,
            metadata={
                "image_path": str(path),
            },
        )
