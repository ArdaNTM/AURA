from aura.brain.task_memory import TaskMemory
from aura.memory.in_memory import InMemoryMemory


def test_task_memory_stores_success():

    memory = InMemoryMemory()

    task_memory = TaskMemory(
        memory,
    )

    task_memory.store_success(
        "Unity Build",
        "Build completed",
    )

    results = task_memory.recall(
        "Unity Build",
    )

    assert len(results) == 1

    assert "task_success=True" in results[0][1]


def test_task_memory_stores_failure():

    memory = InMemoryMemory()

    task_memory = TaskMemory(
        memory,
    )

    task_memory.store_failure(
        "Unity Build",
        "Missing package",
    )

    failures = task_memory.previous_failures(
        "Unity Build",
    )

    assert len(failures) == 1

    assert "Missing package" in failures[0][1]