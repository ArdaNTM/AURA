from aura.vision.models import VisionResult
from aura.vision.ui_element import UIElement
from aura.vision.verification import VisionVerifier


class FakeCapture:

    def capture(self):
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
                    name="save_button",
                    element_type="button",
                    x=10,
                    y=20,
                    confidence=0.9,
                )
            ],
        )


def test_verification_detects_element():

    verifier = VisionVerifier(
        capture=FakeCapture(),
        analyzer=FakeAnalyzer(),
    )

    assert verifier.verify(
        "save_button",
    )
