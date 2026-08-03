from aura.ai.tool_runner import ToolRunner
from aura.brain.executor import PlanExecutor
from aura.brain.models import Decision, PlanStep
from aura.core.tools import Tool, ToolRegistry
from aura.tools import CalculatorTool


class EchoTool(Tool):
    """Simple test tool."""

    @property
    def name(self) -> str:
        return "echo"

    def execute(
        self,
        message: str,
    ) -> str:
        return message


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


def create_dynamic_executor() -> PlanExecutor:
    registry = ToolRegistry()

    registry.register(
        EchoTool(),
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


def test_executor_runs_dynamic_tool_action() -> None:
    executor = create_executor()

    decision = Decision(
        intent="calculation",
        requires_tool=True,
        plan=[
            PlanStep(
                description="Calculate expression",
                action="calculator",
                metadata={
                    "expression": "10/2",
                },
            )
        ],
    )

    results = executor.execute(
        decision,
    )

    assert len(results) == 1

    assert results[0].name == "calculator"

    assert results[0].output == "5.0"


def test_executor_runs_custom_tool_action() -> None:
    executor = create_dynamic_executor()

    decision = Decision(
        intent="custom",
        requires_tool=True,
        plan=[
            PlanStep(
                description="Echo message",
                action="echo",
                metadata={
                    "message": "hello",
                },
            )
        ],
    )

    results = executor.execute(
        decision,
    )

    assert len(results) == 1

    assert results[0].name == "echo"

    assert results[0].output == "hello"


class FailingTool(Tool):
    @property
    def name(self) -> str:
        return "failing"

    def execute(
        self,
    ) -> str:
        raise RuntimeError(
            "temporary failure",
        )


def test_executor_retries_failed_tool():
    registry = ToolRegistry()

    registry.register(
        FailingTool(),
    )

    executor = PlanExecutor(
        ToolRunner(
            registry,
        ),
    )

    decision = Decision(
        intent="test",
        requires_tool=True,
        plan=[
            PlanStep(
                description="Fail tool",
                action="failing",
            )
        ],
    )

    results = executor.execute(
        decision,
    )

    assert len(results) == 1

    assert not results[0].success

    assert results[0].metadata["recovery"]["retry_available"]
