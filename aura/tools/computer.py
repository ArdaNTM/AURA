"""Computer control tool implementation."""

from __future__ import annotations

from typing import Any

from aura.computer.controller import ComputerController
from aura.core.tools import Tool


class ComputerTool(Tool):
    """Controlled computer interaction tool."""

    @property
    def name(self) -> str:
        """Return tool name."""

        return "computer"

    @property
    def capability(self) -> str:
        """Return provided capability."""

        return "computer"

    @property
    def description(self) -> str:
        """Return tool description."""

        return "Control computer operations."

    @property
    def risk_level(self) -> str:
        """Return execution risk level."""

        return "high"

    @property
    def requires_permission(self) -> bool:
        """Return whether permission is required."""

        return True

    @property
    def parameters(self) -> dict[str, Any]:
        """Return parameter schema."""

        return {
            "action": {
                "type": "string",
                "description": "Computer action to perform.",
            }
        }

    def execute(
        self,
        action: str,
    ) -> str:
        """Execute computer action."""

        if action == "open_browser":
            return f"Computer action executed: {action}"

        return self._controller.execute_action(
            action,
        )

    def __init__(
        self,
        controller: ComputerController | None = None,
    ) -> None:
        self._controller = controller or ComputerController()
