from aura.vision.interpreter import VisionInterpreter
from aura.vision.models import VisionResult
from aura.vision.ui_element import UIElement


def test_vision_interpreter_creates_context():

    result = VisionResult(
        description="Unity window detected.",
        objects=[
            "window",
        ],
        confidence=0.8,
        text=[
            "New Project",
        ],
        elements=[
            UIElement(
                name="New Project",
                element_type="button",
                x=100,
                y=200,
                confidence=0.9,
            )
        ],
    )

    interpreter = VisionInterpreter()

    context = interpreter.interpret(
        result,
    )

    assert context["description"] == ("Unity window detected.")

    assert context["screen_state"] == ("interactive_screen")

    assert "click:New Project" in context["possible_actions"]

    assert (
        len(
            context["ui_elements"],
        )
        == 1
    )
