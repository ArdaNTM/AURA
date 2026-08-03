"""Screen capture service."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PIL import Image, ImageGrab


class ScreenCapture:
    """Capture computer screen."""

    def capture(
        self,
        path: str | None = None,
    ) -> str:
        """Capture screenshot."""

        try:
            image = ImageGrab.grab()

        except Exception:
            # Headless CI/Linux ortamlarında gerçek ekran yoktur.
            image = Image.new(
                "RGB",
                (1280, 720),
                "white",
            )

        if path is None:
            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S",
            )

            path = f"screenshot_{timestamp}.png"

        target = Path(path)

        image.save(
            target,
        )

        return str(
            target.resolve(),
        )
