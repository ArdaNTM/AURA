from aura.agent import Agent
from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry
from aura.tools import CalculatorTool


def test_agent_executes_autonomous_cycle():

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

    agent = Agent(
        runtime,
    )

    state = agent.execute(
        "5+5 hesapla",
    )

    assert state.completed

    assert agent.state.cycles == 1

    assert agent.state.last_state == state
