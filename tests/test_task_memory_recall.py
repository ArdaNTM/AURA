from aura.brain.brain import Brain
from aura.brain.task_memory import TaskMemory
from aura.memory.in_memory import InMemoryMemory


def test_brain_reads_previous_task_failures():

    memory = InMemoryMemory()

    task_memory = TaskMemory(
        memory,
    )

    task_memory.store_failure(
        "Unity Build",
        "Missing package",
    )

    brain = Brain()

    decision, _ = brain.think(
        "Unity Build",
        memories=memory.history(),
    )

    learning = decision.metadata["learning"]

    assert len(
        learning["task_failures"],
    ) == 1

    assert (
        "Missing package"
        in learning["task_failures"][0]
    )