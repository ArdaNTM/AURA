from aura.ai.tool_runner import ToolRunner
from aura.brain.executor import PlanExecutor
from aura.brain.models import Decision, PlanStep
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def create_executor() -> PlanExecutor:
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    return PlanExecutor(
        ToolRunner(
            registry,
        ),
    )


def test_executor_runs_calculator_step() -> None:
    executor = create_executor()

    decision = Decision(
        intent="calculation",
        requires_tool=True,
        target="calculator",
        plan=[
            PlanStep(
                description="Calculate expression",
                action="calculator",
                metadata={
                    "expression": "2+2",
                },
            )
        ],
    )

    results = executor.execute(
        decision,
    )

    assert len(results) == 1

    assert results[0].success

    assert results[0].name == "calculator"

    assert results[0].output == "4"


def test_executor_marks_steps_completed() -> None:
    executor = create_executor()

    step = PlanStep(
        description="Calculate expression",
        action="calculator",
        metadata={
            "expression": "5*5",
        },
    )

    decision = Decision(
        intent="calculation",
        requires_tool=True,
        plan=[
            step,
        ],
    )

    executor.execute(
        decision,
    )

    assert step.completed
