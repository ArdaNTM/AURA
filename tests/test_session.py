from aura.core.session import Session
from aura.memory.in_memory import InMemoryMemory


def test_session_starts_empty():
    session = Session(InMemoryMemory())

    assert session.history() == []


def test_add_user_message():
    session = Session(InMemoryMemory())

    session.add_user_message("Hello")

    assert session.history() == [
        ("user", "Hello"),
    ]


def test_add_assistant_message():
    session = Session(InMemoryMemory())

    session.add_assistant_message("Hi!")

    assert session.history() == [
        ("assistant", "Hi!"),
    ]


def test_clear_session():
    session = Session(InMemoryMemory())

    session.add_user_message("Hello")
    session.add_assistant_message("Hi!")

    session.clear()

    assert session.history() == []


def test_message_order():
    session = Session(InMemoryMemory())

    session.add_user_message("Hello")
    session.add_assistant_message("Hi!")
    session.add_user_message("How are you?")

    assert session.history() == [
        ("user", "Hello"),
        ("assistant", "Hi!"),
        ("user", "How are you?"),
    ]


def test_messages_returns_provider_format():
    session = Session(InMemoryMemory())

    session.add_user_message("Hello")
    session.add_assistant_message("Hi!")

    assert session.messages() == [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hi!",
        },
    ]
