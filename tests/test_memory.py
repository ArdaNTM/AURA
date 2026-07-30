from aura.memory.base import Memory


class DummyMemory(Memory):
    def __init__(self):
        self.messages = []

    def add(self, role: str, content: str) -> None:
        self.messages.append((role, content))

    def history(self):
        return list(self.messages)

    def clear(self):
        self.messages.clear()


def test_add():
    memory = DummyMemory()

    memory.add("user", "hello")

    assert memory.history() == [("user", "hello")]


def test_clear():
    memory = DummyMemory()

    memory.add("user", "hello")
    memory.clear()

    assert memory.history() == []