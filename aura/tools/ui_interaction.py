"""UI interaction tool."""

from __future__ import annotations

from typing import Any

from aura.computer.keyboard import KeyboardController
from aura.computer.mouse import MouseController
from aura.core.tool_result import ToolResult
from aura.core.tools import Tool


class UIInteractionTool(Tool):
    """Interact with UI elements."""

    def __init__(
        self,
        mouse: MouseController | None = None,
        keyboard: KeyboardController | None = None,
    ) -> None:
        self._mouse = mouse or MouseController()
        self._keyboard = keyboard or KeyboardController()

    @property
    def name(
        self,
    ) -> str:
        return "ui_interaction"

    @property
    def capability(
        self,
    ) -> str:
        return "computer"

    @property
    def description(
        self,
    ) -> str:
        return "Interact with user interface elements."

    @property
    def risk_level(
        self,
    ) -> str:
        return "high"

    @property
    def requires_permission(
        self,
    ) -> bool:
        return True

    @property
    def parameters(
        self,
    ) -> dict[str, Any]:
        return {
            "action": {
                "type": "string",
                "description": "UI action.",
            },
            "x": {
                "type": "integer",
                "description": "X coordinate.",
            },
            "y": {
                "type": "integer",
                "description": "Y coordinate.",
            },
            "text": {
                "type": "string",
                "description": "Text input.",
            },
            "key": {
                "type": "string",
                "description": "Keyboard key.",
            },
        }

    def execute(
        self,
        action: str,
        x: int | None = None,
        y: int | None = None,
        text: str | None = None,
        key: str | None = None,
    ) -> ToolResult:
        """Execute UI action."""

        if action == "click":
            output = self._mouse.click(
                x,
                y,
            )

        elif action == "double_click":
            output = self._mouse.double_click(
                x,
                y,
            )

        elif action == "move":
            output = self._mouse.move(
                x,
                y,
            )

        elif action == "type":
            output = self._keyboard.type_text(
                text or "",
            )

        elif action == "press":
            output = self._keyboard.press(
                key or "",
            )

        else:
            raise ValueError(
                f"Unsupported UI action: {action}",
            )

        return ToolResult(
            name=self.name,
            output=output,
        )
