from aura.agent.experience import AgentExperience
from aura.agent.memory_loop import AgentMemoryLoop


def test_memory_context_contains_strategy():

    memory = AgentMemoryLoop()

    memory.remember(
        AgentExperience(
            task="calc",
            success=True,
            strategy="tool_execution",
            score=1.0,
        )
    )

    context = memory.context()

    assert context["experience_count"] == 1

    assert context["preferred_strategy"] == "tool_execution"
