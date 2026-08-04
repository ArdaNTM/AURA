from __future__ import annotations

from aura.vision.ui_element import UIElement


class ElementDetector:
    """Detect UI elements from vision data."""

    def detect(
        self,
        image_path: str,
    ) -> list[UIElement]:
        """Detect visible UI elements."""

        return [
            UIElement(
                name="unknown_button",
                element_type="button",
                x=100,
                y=100,
                confidence=0.5,
                metadata={
                    "source": image_path,
                },
            )
        ]
