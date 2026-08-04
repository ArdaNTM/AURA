from __future__ import annotations

from aura.vision.action import VisionAction
from aura.vision.models import VisionResult


class VisionActionPlanner:
    """Create actions from vision results."""

    def plan(
        self,
        vision: VisionResult,
        target: str,
    ) -> VisionAction | None:
        """Find target element and create action."""

        for element in vision.elements:

            if target.lower() in element.name.lower():

                return VisionAction(
                    action="click",
                    x=element.x,
                    y=element.y,
                    target=element.name,
                    confidence=element.confidence,
                )

        return None
