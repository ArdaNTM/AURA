from __future__ import annotations

import time


class InputController:
    """Control mouse and keyboard input."""

    def move_mouse(
        self,
        x: int,
        y: int,
    ) -> str:
        """Move mouse cursor."""

        return f"Mouse moved to ({x}, {y})"

    def click(
        self,
        button: str = "left",
    ) -> str:
        """Click mouse."""

        return f"Mouse clicked: {button}"

    def type_text(
        self,
        text: str,
    ) -> str:
        """Type keyboard text."""

        time.sleep(0.1)

        return f"Typed text: {text}"
