"""Screen capture and analysis tool implementation."""

from __future__ import annotations

from typing import Any

from aura.computer.screen import ScreenCapture
from aura.core.tool_result import ToolResult
from aura.core.tools import Tool
from aura.vision.analyzer import VisionAnalyzer


class ScreenCaptureTool(Tool):
    """Capture and analyze computer screen."""

    def __init__(
        self,
        capture: ScreenCapture | None = None,
        analyzer: VisionAnalyzer | None = None,
    ) -> None:
        self._capture = capture or ScreenCapture()
        self._analyzer = analyzer or VisionAnalyzer()

    @property
    def name(
        self,
    ) -> str:
        return "screen_capture"

    @property
    def capability(
        self,
    ) -> str:
        return "screen"

    @property
    def description(
        self,
    ) -> str:
        return "Capture and analyze current computer screen."

    @property
    def risk_level(
        self,
    ) -> str:
        return "medium"

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
                "description": "Action: capture or analyze.",
            },
            "path": {
                "type": "string",
                "description": "Optional screenshot path.",
            },
        }

    def execute(
        self,
        action: str = "capture",
        path: str | None = None,
    ) -> ToolResult:
        """Capture or analyze screen."""

        if action == "capture":
            image_path = self._capture.capture(
                path,
            )

            return ToolResult(
                name=self.name,
                output="Screenshot captured.",
                metadata={
                    "image_path": image_path,
                },
            )

        if action == "analyze":
            image_path = self._capture.capture(
                path,
            )

            result = self._analyzer.analyze(
                image_path,
            )

            return ToolResult(
                name=self.name,
                output=result.description,
                metadata={
                    "image_path": image_path,
                    "vision": {
                        "description": result.description,
                        "objects": result.objects,
                        "confidence": result.confidence,
                        "text": result.text,
                        "regions": result.regions,
                        "elements": [
                            {
                                "name": element.name,
                                "type": element.element_type,
                                "x": element.x,
                                "y": element.y,
                                "confidence": element.confidence,
                                "metadata": element.metadata,
                            }
                            for element in result.elements
                        ],
                        "metadata": result.metadata,
                    },
                },
            )

        raise ValueError(
            f"Unsupported screen action: {action}",
        )
