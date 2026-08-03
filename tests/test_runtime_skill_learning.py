from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.learning_profile import LearningProfile
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def test_runtime_updates_skill_registry():

    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    profile = LearningProfile()

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        learning_profile=profile,
    )

    runtime.run(
        "2+2 hesapla",
    )

    skill = profile.skill_registry.get(
        "calculation",
    )

    assert skill is not None

    assert skill.usage_count == 1

    assert skill.success_rate == 1.0

    assert skill.confidence > 0
