from aura.agent.experience import AgentExperience
from aura.agent.memory_loop import AgentMemoryLoop


def test_agent_memory_tracks_successful_strategy():

    memory = AgentMemoryLoop()

    memory.remember(
        AgentExperience(
            task="calculate",
            success=True,
            strategy="tool_execution",
            score=1.0,
        )
    )

    assert memory.preferred_strategy() == "tool_execution"


def test_agent_memory_ignores_failed_strategy():

    memory = AgentMemoryLoop()

    memory.remember(
        AgentExperience(
            task="calculate",
            success=False,
            strategy="unsafe",
            score=0.0,
        )
    )

    assert memory.preferred_strategy() is None
