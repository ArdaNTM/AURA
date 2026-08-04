from __future__ import annotations

from aura.computer.screen import ScreenCapture
from aura.vision.analyzer import VisionAnalyzer


class VisionVerifier:
    """Verify visual actions after execution."""

    def __init__(
        self,
        capture: ScreenCapture | None = None,
        analyzer: VisionAnalyzer | None = None,
    ) -> None:

        self._capture = capture or ScreenCapture()

        self._analyzer = analyzer or VisionAnalyzer()

    def verify(
        self,
        expected_element: str,
    ) -> bool:
        """Check whether expected element exists."""

        image_path = self._capture.capture()

        result = self._analyzer.analyze(
            image_path,
        )

        for element in result.elements:

            if element.name == expected_element:
                return True

        return False
