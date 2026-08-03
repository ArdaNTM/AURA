from __future__ import annotations

from typing import Any

from aura.computer.input import InputController
from aura.core.tools import Tool


class InputTool(Tool):
    """Control keyboard and mouse."""

    def __init__(
        self,
        controller: InputController | None = None,
    ) -> None:
        self._controller = controller or InputController()

    @property
    def name(
        self,
    ) -> str:
        return "input"

    @property
    def capability(
        self,
    ) -> str:
        return "computer"

    @property
    def description(
        self,
    ) -> str:
        return "Control mouse and keyboard input."

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
                "description": "Input action.",
            },
            "value": {
                "type": "string",
                "description": "Action value.",
            },
        }

    def execute(
        self,
        action: str,
        value: str = "",
    ) -> str:
        if action == "click":
            return self._controller.click(
                value or "left",
            )

        if action == "type":
            return self._controller.type_text(
                value,
            )

        if action == "move":
            x, y = value.split(",")

            return self._controller.move_mouse(
                int(x),
                int(y),
            )

        return f"Unsupported input action: {action}"
