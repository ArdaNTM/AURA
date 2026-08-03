from aura.brain.task_memory import TaskMemory
from aura.memory.in_memory import InMemoryMemory


def test_task_memory_ranks_best_experience():

    memory = InMemoryMemory()

    task_memory = TaskMemory(
        memory,
    )

    task_memory.store_success(
        "Unity Build",
        "Used old strategy",
        strategy="tool_execution",
    )

    task_memory.store_success(
        "Unity Build",
        "Used safe strategy",
        strategy="safe_tool_execution",
    )

    ranked = task_memory.rank_experiences(
        "Unity Build",
    )

    assert len(ranked) == 2

    assert (
        "safe_tool_execution"
        in ranked[0][1]
    )