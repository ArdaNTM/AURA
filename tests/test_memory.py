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


def test_rank_experiences_prefers_high_confidence_success():
    memory = DummyMemory()

    memory.add(
        "assistant",
        (
            "intent=calculation; "
            "strategy=tool_execution; "
            "confidence=0.6; "
            "success=True; "
            "output=10"
        ),
    )

    memory.add(
        "assistant",
        (
            "intent=calculation; "
            "strategy=safe_tool_execution; "
            "confidence=0.95; "
            "success=True; "
            "output=10"
        ),
    )

    ranked = memory.rank_experiences(
        "calculation",
    )

    assert "safe_tool_execution" in ranked[0][1]


def test_rank_experiences_ignores_failed_experiences():
    memory = DummyMemory()

    memory.add(
        "assistant",
        (
            "intent=calculation; "
            "strategy=tool_execution; "
            "confidence=0.9; "
            "success=False; "
            "output=error"
        ),
    )

    memory.add(
        "assistant",
        (
            "intent=calculation; "
            "strategy=safe_tool_execution; "
            "confidence=0.7; "
            "success=True; "
            "output=10"
        ),
    )

    ranked = memory.rank_experiences(
        "calculation",
    )

    assert len(ranked) == 1

    assert "safe_tool_execution" in ranked[0][1]
