from __future__ import annotations

from aura.computer.screen import ScreenCapture
from aura.core.tool_result import ToolResult
from aura.vision.action_executor import VisionActionExecutor
from aura.vision.action_planner import VisionActionPlanner
from aura.vision.analyzer import VisionAnalyzer


class VisionController:
    """Coordinate visual understanding and actions."""

    def __init__(
        self,
        capture: ScreenCapture | None = None,
        analyzer: VisionAnalyzer | None = None,
        planner: VisionActionPlanner | None = None,
        executor: VisionActionExecutor | None = None,
    ) -> None:

        self._capture = capture or ScreenCapture()

        self._analyzer = analyzer or VisionAnalyzer()

        self._planner = planner or VisionActionPlanner()

        self._executor = executor or VisionActionExecutor()

    def observe(
        self,
    ):
        """Capture and analyze current screen."""

        image_path = self._capture.capture()

        return self._analyzer.analyze(
            image_path,
        )

    def click_element(
        self,
        target: str,
    ) -> ToolResult | None:
        """Find element and click."""

        vision = self.observe()

        action = self._planner.plan(
            vision,
            target,
        )

        if action is None:
            return None

        return self._executor.execute(
            action,
        )
