from aura.brain.brain import Brain
from aura.memory.in_memory import InMemoryMemory


def test_brain_uses_recall_ranking():

    memory = InMemoryMemory()

    memory.add(
        "assistant",
        (
            "intent=calculation; "
            "strategy=safe_tool_execution; "
            "confidence=0.9; "
            "success=True"
        ),
    )

    brain = Brain(
        memory=memory,
    )

    decision, _ = brain.think(
        "calculate 5+5",
        memories=memory.history(),
    )

    learning = decision.metadata["learning"]

    assert learning["retrieved_memories"]

    assert "safe_tool_execution" in learning["retrieved_memories"][0][1]
