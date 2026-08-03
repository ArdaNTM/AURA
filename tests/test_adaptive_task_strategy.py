from aura.brain.brain import Brain
from aura.brain.task_memory import TaskMemory
from aura.memory.in_memory import InMemoryMemory


def test_previous_task_failure_changes_strategy():

    memory = InMemoryMemory()

    task_memory = TaskMemory(
        memory,
    )

    task_memory.store_failure(
        "5+5 hesapla",
        "Previous execution failed",
    )

    brain = Brain()

    decision, _ = brain.think(
        "5+5 hesapla",
        memories=memory.history(),
    )

    assert decision.strategy == "safe_tool_execution"
