from aura.context.builder import ContextBuilder
from aura.core.session import Session
from aura.core.tools import ToolRegistry
from aura.memory.in_memory import InMemoryMemory


def test_context_builder_collects_messages():
    memory = InMemoryMemory()

    session = Session(
        memory,
    )

    session.add_user_message(
        "Hello AURA",
    )

    registry = ToolRegistry()

    builder = ContextBuilder(
        session,
        registry,
        memory,
    )

    context = builder.build()

    assert context.messages == [
        {
            "role": "user",
            "content": "Hello AURA",
        }
    ]


def test_context_builder_collects_tools():
    memory = InMemoryMemory()

    session = Session(
        memory,
    )

    registry = ToolRegistry()

    builder = ContextBuilder(
        session,
        registry,
        memory,
    )

    context = builder.build()

    assert context.tools == []


def test_context_builder_collects_memories():
    memory = InMemoryMemory()

    memory.add(
        "user",
        "AURA memory sistemi tamamlandı",
    )

    session = Session(
        memory,
    )

    registry = ToolRegistry()

    builder = ContextBuilder(
        session,
        registry,
        memory,
    )

    context = builder.build(
        query="AURA",
    )

    assert context.memories == [
        (
            "user",
            "AURA memory sistemi tamamlandı",
        )
    ]