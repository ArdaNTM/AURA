from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.runtime import AgentRuntime


class FakeVision:

    def observe(self):
        from aura.vision.models import VisionResult

        return VisionResult(
            description="Test screen",
            objects=["window"],
            confidence=0.9,
            metadata={
                "test": True,
            },
        )


def test_runtime_passes_vision_to_brain():

    brain = Brain()

    runtime = AgentRuntime(
        brain=brain,
        executor=PlanExecutor(
            tool_runner=None,
        ),
        vision_controller=FakeVision(),
    )

    state = runtime.run(
        "ekranda ne var",
    )

    assert "vision" in state.metadata

    assert state.metadata["vision"]["confidence"] == 0.9
