from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.learning_profile import LearningProfile
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry
from aura.memory.in_memory import InMemoryMemory
from aura.tools import CalculatorTool


def test_full_agent_cycle_with_learning() -> None:
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    profile = LearningProfile()

    memory = InMemoryMemory()

    runtime = AgentRuntime(
        Brain(
            tools=registry,
            learning_profile=profile,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        memory,
        learning_profile=profile,
    )

    state = runtime.run(
        "2+2 hesapla",
    )

    assert state.completed

    assert state.decision is not None

    assert state.decision.strategy in (
        "tool_execution",
        "safe_tool_execution",
    )

    assert (
        len(
            state.observations,
        )
        == 1
    )

    observation = state.observations[0]

    assert observation.success

    assert observation.output == "4"

    assert state.reflection is not None

    assert state.reflection.success

    assert "performance" in state.metadata

    assert profile.total_tasks == 1

    assert profile.successful_tasks == 1

    assert memory.history()
