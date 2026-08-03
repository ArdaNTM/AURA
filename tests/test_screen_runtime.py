from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry
from aura.tools.screen import ScreenCaptureTool


def test_runtime_creates_screen_permission():

    registry = ToolRegistry()

    registry.register(
        ScreenCaptureTool(),
    )

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
    )

    state = runtime.run(
        "ekran görüntüsü al",
    )

    assert state.decision.intent == "screen"
    assert state.permission_request is not None


def test_screen_observation_contains_vision_data():

    registry = ToolRegistry()

    registry.register(
        ScreenCaptureTool(),
    )

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
    )

    state = runtime.run(
        "ekran görüntüsü al",
    )

    assert state.permission_request is not None
