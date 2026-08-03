from aura.vision.ui_element import UIElement


def test_ui_element_creation():

    element = UIElement(
        name="button",
        element_type="button",
        x=100,
        y=200,
        confidence=0.9,
    )

    assert element.name == "button"

    assert element.x == 100

    assert element.confidence == 0.9
