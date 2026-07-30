from aura.context.builder import ContextBuilder
from aura.core.session import Session
from aura.core.tools import ToolRegistry
from aura.memory.in_memory import InMemoryMemory


def create_builder():
    memory = InMemoryMemory()

    session = Session(
        memory,
    )

    registry = ToolRegistry()

    return ContextBuilder(
        session,
        registry,
        memory,
    )


def test_context_builder_collects_messages():
    builder = create_builder()

    builder._session.add_user_message(
        "Hello AURA",
    )

    context = builder.build()

    assert context.messages[0]["role"] == "system"

    assert "AURA" in context.messages[0]["content"]

    assert context.messages[1] == {
        "role": "user",
        "content": "Hello AURA",
    }


def test_context_builder_collects_tools():
    builder = create_builder()

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

    assert "AURA" in context.system_prompt


def test_context_builder_contains_identity():
    builder = create_builder()

    context = builder.build()

    system_message = context.messages[0]

    assert system_message["role"] == "system"

    assert "You are AURA" in system_message["content"]
