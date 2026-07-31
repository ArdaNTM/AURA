from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.learning import LearningContext
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def test_full_autonomous_improvement_loop():
    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    learning = LearningContext(
        [
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=True; "
                    "output=10"
                ),
            ),
            (
                "assistant",
                (
                    "intent=calculation; "
                    "strategy=safe_tool_execution; "
                    "success=True; "
                    "output=20"
                ),
            ),
        ],
    )

    brain = Brain(
        tools=registry,
        learning_context=learning,
    )

    runtime = AgentRuntime(
        brain,
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
    )

    state = runtime.run(
        "5+5 hesapla",
    )

    assert state.completed

    assert state.improvement_plan is not None

    assert state.improvement_plan.target_strategy == "safe_tool_execution"

    assert state.improvement_plan.risk_adjustment == "low"

    assert state.improvement_plan.confidence_change == 0.1

    assert (
        len(
            state.improvement_plan.suggestions,
        )
        > 0
    )
