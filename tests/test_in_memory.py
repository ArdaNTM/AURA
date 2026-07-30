from aura.memory.in_memory import InMemoryMemory


def test_memory_starts_empty():
    memory = InMemoryMemory()

    assert memory.history() == []


def test_add_message():
    memory = InMemoryMemory()

    memory.add("user", "Hello")
    memory.add("assistant", "Hi!")

    assert memory.history() == [
        ("user", "Hello"),
        ("assistant", "Hi!"),
    ]


def test_history_returns_copy():
    memory = InMemoryMemory()

    memory.add("user", "Hello")

    history = memory.history()
    history.append(("assistant", "Modified"))

    assert memory.history() == [
        ("user", "Hello"),
    ]


def test_clear():
    memory = InMemoryMemory()

    memory.add("user", "Hello")
    memory.clear()

    assert memory.history() == []
