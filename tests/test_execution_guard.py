from aura.brain.execution_guard import ExecutionGuard
from aura.brain.models import Decision
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def test_execution_guard_allows_existing_tool():
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    guard = ExecutionGuard(
        registry,
    )

    decision = Decision(
        intent="calculation",
        confidence=0.9,
        requires_tool=True,
        target="calculator",
        priority="normal",
        risk_level="low",
        strategy="tool_execution",
        explanation="test",
        plan=[],
        metadata={},
    )

    assert guard.can_execute(
        decision,
    )


def test_execution_guard_blocks_missing_tool():
    registry = ToolRegistry()

    guard = ExecutionGuard(
        registry,
    )

    decision = Decision(
        intent="calculation",
        confidence=0.9,
        requires_tool=True,
        target="calculator",
        priority="normal",
        risk_level="low",
        strategy="tool_execution",
        explanation="test",
        plan=[],
        metadata={},
    )

    assert not guard.can_execute(
        decision,
    )
