from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def test_runtime_creates_background_task():

    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
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
        "2+2 hesapla",
    )

    assert state.background_task is not None

    assert state.background_task.status == "completed"

    assert state.background_task.progress == 1.0
