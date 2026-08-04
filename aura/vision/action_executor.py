from __future__ import annotations

from aura.core.tool_result import ToolResult
from aura.tools.ui_interaction import UIInteractionTool
from aura.vision.action import VisionAction
from aura.vision.recovery import VisionRecovery
from aura.vision.verification import VisionVerifier


class VisionActionExecutor:
    """Execute actions generated from vision system."""

    def __init__(
        self,
        ui_tool: UIInteractionTool | None = None,
        verifier: VisionVerifier | None = None,
        recovery: VisionRecovery | None = None,
    ) -> None:
        self._ui_tool = ui_tool or UIInteractionTool()

        self._verifier = verifier

        self._recovery = recovery or VisionRecovery()

    @property
    def ui_tool(
        self,
    ) -> UIInteractionTool:
        """Return UI interaction tool."""

        return self._ui_tool

    def execute(
        self,
        action: VisionAction,
        verify: bool = False,
    ) -> ToolResult:
        """Execute visual action."""

        result = self._execute_action(
            action,
        )

        if not verify:
            return result

        if self._verifier is None:
            return result

        verified = self._verifier.verify(
            action.target or "",
        )

        if verified:
            result.metadata["verified"] = True

            return result

        recovery = self._recovery.recover(
            action.target or "",
            [],
        )

        result.metadata["verified"] = False
        result.metadata["recovery"] = recovery

        return result

    def _execute_action(
        self,
        action: VisionAction,
    ) -> ToolResult:
        """Execute raw UI action."""

        if action.action == "click":

            return self._ui_tool.execute(
                action="click",
                x=action.x,
                y=action.y,
            )

        if action.action == "double_click":

            return self._ui_tool.execute(
                action="double_click",
                x=action.x,
                y=action.y,
            )

        if action.action == "move":

            return self._ui_tool.execute(
                action="move",
                x=action.x,
                y=action.y,
            )

        if action.action == "type":

            return self._ui_tool.execute(
                action="type",
                text=action.target or "",
            )

        raise ValueError(
            f"Unsupported vision action: {action.action}",
        )
