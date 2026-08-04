from aura.brain.vision_controller import VisionController
from aura.vision.models import VisionResult
from aura.vision.ui_element import UIElement


class FakeCapture:

    def capture(
        self,
    ):
        return "screen.png"


class FakeAnalyzer:

    def analyze(
        self,
        path,
    ):
        return VisionResult(
            description="screen",
            elements=[
                UIElement(
                    name="new_project",
                    element_type="button",
                    x=100,
                    y=200,
                    confidence=0.9,
                )
            ],
        )


def test_vision_controller_clicks_element():

    controller = VisionController(
        capture=FakeCapture(),
        analyzer=FakeAnalyzer(),
    )

    result = controller.click_element(
        "new_project",
    )

    assert result is not None

    assert result.success

    assert "100" in result.output
