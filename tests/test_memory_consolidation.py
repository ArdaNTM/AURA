from aura.memory.consolidation import MemoryConsolidator
from aura.memory.in_memory import InMemoryMemory


def test_memory_consolidator_removes_duplicates():

    memory = InMemoryMemory()

    memory.add(
        "assistant",
        "intent=calculation; success=True; output=10",
    )

    memory.add(
        "assistant",
        "intent=calculation; success=True; output=10",
    )

    consolidator = MemoryConsolidator()

    removed = consolidator.consolidate(
        memory,
    )

    assert removed == 1

    assert memory.history() == [
        (
            "assistant",
            "intent=calculation; success=True; output=10",
        )
    ]


def test_memory_consolidator_preserves_different_experiences():

    memory = InMemoryMemory()

    memory.add(
        "assistant",
        "intent=calculation; strategy=tool_execution; success=True",
    )

    memory.add(
        "assistant",
        "intent=calculation; strategy=safe_tool_execution; success=True",
    )

    consolidator = MemoryConsolidator()

    removed = consolidator.consolidate(
        memory,
    )

    assert removed == 0

    assert len(memory.history()) == 2


def test_memory_groups_by_intent():

    memory = InMemoryMemory()

    memory.add(
        "assistant",
        "intent=calculation; success=True",
    )

    memory.add(
        "assistant",
        "intent=filesystem; success=True",
    )

    consolidator = MemoryConsolidator()

    groups = consolidator.summarize_groups(
        memory,
    )

    assert "calculation" in groups
    assert "filesystem" in groups
