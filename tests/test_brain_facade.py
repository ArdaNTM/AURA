from aura.brain.brain import Brain
from aura.memory.in_memory import InMemoryMemory


def test_brain_thinks_about_tool_request():
    brain = Brain()

    decision, action = brain.think(
        "5 + 5 hesapla",
    )

    assert decision.intent == "calculation"

    assert decision.requires_tool

    assert action.name == "execute_tool"


def test_brain_thinks_about_conversation():
    brain = Brain()

    decision, action = brain.think(
        "Merhaba AURA",
    )

    assert decision.intent == "conversation"

    assert not decision.requires_tool

    assert action.name == "generate_response"


def test_brain_reads_memory_context():
    memory = InMemoryMemory()

    memory.add(
        "user",
        "Benim adım Arda",
    )

    brain = Brain(
        memory=memory,
    )

    memories = memory.search(
        "Benim adım ne?",
    )

    decision, _ = brain.think(
        "Benim adım ne?",
        memories=memories,
    )

    assert "memory" in decision.metadata

    assert decision.metadata["memory"] == [
        (
            "user",
            "Benim adım Arda",
        )
    ]
