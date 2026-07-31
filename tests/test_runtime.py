from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.runtime import AgentRuntime
from aura.brain.state import AgentState
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def test_agent_runtime_executes_cycle():
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

    assert isinstance(
        state,
        AgentState,
    )

    assert state.completed

    assert state.decision is not None

    assert (
        len(
            state.observations,
        )
        == 1
    )

    assert state.observations[0].output == "4"
