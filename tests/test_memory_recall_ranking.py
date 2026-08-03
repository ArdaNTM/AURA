from aura.memory.in_memory import InMemoryMemory


def test_recall_prefers_successful_memory():

    memory = InMemoryMemory()

    memory.add(
        "assistant",
        ("intent=test; " "success=True; " "confidence=0.9"),
    )

    memory.add(
        "assistant",
        ("intent=test; " "success=True; " "confidence=0.5"),
    )

    result = memory.recall(
        "test",
    )

    assert "confidence=0.9" in result[0][1]
