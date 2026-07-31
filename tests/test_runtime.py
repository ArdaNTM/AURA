from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.runtime import AgentRuntime
from aura.brain.state import AgentState
from aura.core.tools import ToolRegistry
from aura.memory.in_memory import InMemoryMemory
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


def test_agent_runtime_stores_observation_memory():
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    memory = InMemoryMemory()

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        memory,
    )

    runtime.run(
        "2+2 hesapla",
    )

    history = memory.history()

    assert any("4" in content for _, content in history)


def test_agent_runtime_uses_custom_memory_policy():
    class RejectAllPolicy:
        def should_store(
            self,
            observation,
        ) -> bool:
            return False

    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    memory = InMemoryMemory()

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        memory,
        RejectAllPolicy(),
    )

    runtime.run(
        "2+2 hesapla",
    )

    history = memory.history()

    assert not any("4" in content for _, content in history)


def test_agent_runtime_evaluates_observations():
    class TrackingEvaluator:
        def __init__(self) -> None:
            self.called = False

        def evaluate(
            self,
            observation,
        ):
            self.called = True

            observation.score = 0.75
            observation.feedback = "custom evaluation"

            return observation

    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    evaluator = TrackingEvaluator()

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        evaluator=evaluator,
    )

    state = runtime.run(
        "2+2 hesapla",
    )

    assert evaluator.called

    assert (
        len(
            state.observations,
        )
        == 1
    )

    assert state.observations[0].score == 0.75

    assert state.observations[0].feedback == "custom evaluation"
