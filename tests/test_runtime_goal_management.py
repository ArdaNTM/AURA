from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def test_runtime_registers_goal():

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

    runtime.run(
        "2+2 hesapla",
    )

    goals = runtime.goal_manager.list_goals()

    assert len(goals) == 1

    assert goals[0].description == "2+2 hesapla"


def test_runtime_creates_decomposed_execution_plan():

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
        "Mobil oyun yap",
    )

    assert state.execution_plan is not None

    assert (
        len(
            state.execution_plan.steps,
        )
        == 5
    )

    assert state.execution_plan.steps[0].action == "concept"


def test_runtime_creates_scheduler():

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
        "Mobil oyun yap",
    )

    assert state.scheduler is not None

    task = state.scheduler.next_task()

    assert task is not None

    assert task.task == "Define project concept"
