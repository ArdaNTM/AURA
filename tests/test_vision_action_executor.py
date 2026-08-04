from aura.vision.action import VisionAction
from aura.vision.action_executor import VisionActionExecutor
from aura.vision.verification import VisionVerifier


def test_vision_click_action_executes():

    executor = VisionActionExecutor()

    action = VisionAction(
        action="click",
        x=300,
        y=400,
        target="button",
        confidence=0.9,
    )

    result = executor.execute(
        action,
    )

    assert result.success

    assert "300" in result.output

    assert "400" in result.output


class FakeVerifier(VisionVerifier):

    def verify(
        self,
        target,
    ):
        return False


def test_executor_reports_failed_verification():

    executor = VisionActionExecutor(
        verifier=FakeVerifier(),
    )

    action = VisionAction(
        action="click",
        x=10,
        y=20,
        target="save",
    )

    result = executor.execute(
        action,
        verify=True,
    )

    assert result.metadata["verified"] is False

    assert "recovery" in result.metadata
