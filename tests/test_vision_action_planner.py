from aura.vision.action_planner import VisionActionPlanner
from aura.vision.models import VisionResult
from aura.vision.ui_element import UIElement


def test_action_planner_creates_click():

    vision = VisionResult(
        description="screen",
        elements=[
            UIElement(
                name="new_project",
                element_type="button",
                x=200,
                y=300,
                confidence=0.8,
            )
        ],
    )

    planner = VisionActionPlanner()

    action = planner.plan(
        vision,
        "new_project",
    )

    assert action is not None

    assert action.action == "click"

    assert action.x == 200

    assert action.y == 300
