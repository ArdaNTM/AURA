from aura.memory.in_memory import InMemoryMemory
from aura.memory.recall import RecallEngine


def test_recall_engine_ranks_memories():

    memory = InMemoryMemory()

    memory.add(
        "assistant",
        ("intent=test; " "strategy=tool_execution; " "confidence=0.5; " "success=True"),
    )

    memory.add(
        "assistant",
        (
            "intent=test; "
            "strategy=safe_tool_execution; "
            "confidence=0.9; "
            "success=True"
        ),
    )

    recall = RecallEngine(
        memory,
    )

    results = recall.rank(
        memory.history(),
    )

    assert "safe_tool_execution" in results[0][1]
