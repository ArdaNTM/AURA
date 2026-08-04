from __future__ import annotations

from aura.vision.models import VisionResult


class VisionInterpreter:
    """
    Convert raw vision results into semantic understanding.
    """

    def interpret(
        self,
        result: VisionResult,
    ) -> dict[str, object]:
        """
        Create semantic context from vision result.
        """

        context: dict[str, object] = {
            "description": result.description,
            "confidence": result.confidence,
            "objects": result.objects,
            "text": result.text,
            "ui_elements": [],
        }

        elements = []

        for element in result.elements:
            elements.append(
                {
                    "name": element.name,
                    "type": element.element_type,
                    "position": {
                        "x": element.x,
                        "y": element.y,
                    },
                    "confidence": element.confidence,
                    "metadata": element.metadata,
                }
            )

        context["ui_elements"] = elements

        context["screen_state"] = self._detect_screen_state(
            result,
        )

        context["possible_actions"] = self._suggest_actions(
            result,
        )

        return context

    def _detect_screen_state(
        self,
        result: VisionResult,
    ) -> str:
        """
        Determine general screen state.
        """

        if result.elements:
            return "interactive_screen"

        if result.text:
            return "text_screen"

        if result.objects:
            return "object_screen"

        return "unknown"

    def _suggest_actions(
        self,
        result: VisionResult,
    ) -> list[str]:
        """
        Suggest possible next actions.
        """

        actions: list[str] = []

        for element in result.elements:

            if element.element_type == "button":
                actions.append(
                    f"click:{element.name}",
                )

            elif element.element_type == "input":
                actions.append(
                    f"fill:{element.name}",
                )

        return actions
