"""Screen capture service."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PIL import ImageGrab


class ScreenCapture:
    """Capture computer screen."""

    def capture(
        self,
        path: str | None = None,
    ) -> str:
        """Capture screenshot."""

        image = ImageGrab.grab()

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
